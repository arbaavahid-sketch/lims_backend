from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_roles
from ..i18n import bi

router = APIRouter(prefix="/results", tags=["Results"])


def _resolve_spec(db: Session, assignment: models.TestAssignment):
    """حد پذیرش قابل‌اعمال را برمی‌گرداند.

    ترتیب اولویت طبق ISO 17025:
    ۱) مشخصات گریدِ محصولِ نمونه (Specification)
    ۲) در نبود آن، حد پیش‌فرض خودِ روش آزمون (fallback)
    خروجی: (spec_type, spec_min, spec_max, unit, decision_rule)
    """
    method = assignment.test_method
    sample = assignment.sample

    if sample and sample.product_grade_id:
        spec = (
            db.query(models.Specification)
            .filter_by(
                product_grade_id=sample.product_grade_id,
                test_method_id=assignment.test_method_id,
            )
            .first()
        )
        if spec:
            return (
                spec.spec_type,
                spec.spec_min,
                spec.spec_max,
                spec.unit or method.unit,
                spec.decision_rule,
            )

    if method.spec_min is not None or method.spec_max is not None:
        return (models.SpecType.RANGE, method.spec_min, method.spec_max,
                method.unit, "simple_acceptance")

    return (None, None, None, method.unit, "simple_acceptance")


def _evaluate_conformity(
    value: float,
    spec_type: Optional[models.SpecType],
    spec_min: Optional[float],
    spec_max: Optional[float],
    uncertainty: Optional[float],
    decision_rule: str,
) -> models.ConformityStatus:
    """بیانیهٔ انطباق طبق ISO/IEC 17025 بند 7.8.6.

    - simple_acceptance: اگر مقدار داخل حدود باشد → منطبق.
    - guard_band: نوار محافظ به اندازهٔ عدم‌قطعیت؛ اگر مقدار داخل حدود ولی
      در فاصلهٔ عدم‌قطعیت از یک حد باشد → مشروط (conditional).
    """
    if spec_type is None or spec_type == models.SpecType.INFORMATIVE:
        return models.ConformityStatus.NOT_EVALUATED

    guard = (uncertainty or 0.0) if decision_rule == "guard_band" else 0.0

    if spec_min is not None:
        if value < spec_min:
            return models.ConformityStatus.NONCONFORM
        if guard and value < spec_min + guard:
            return models.ConformityStatus.CONDITIONAL

    if spec_max is not None:
        if value > spec_max:
            return models.ConformityStatus.NONCONFORM
        if guard and value > spec_max - guard:
            return models.ConformityStatus.CONDITIONAL

    return models.ConformityStatus.CONFORM


@router.get("/by-sample/{sample_id}", response_model=list[schemas.TestResultOut])
def results_for_sample(
    sample_id: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    """همهٔ نتایج ثبت‌شدهٔ یک نمونه (برای نمایش در فرانت‌اند)."""
    return (
        db.query(models.TestResult)
        .join(models.TestAssignment, models.TestResult.assignment_id == models.TestAssignment.id)
        .filter(models.TestAssignment.sample_id == sample_id)
        .all()
    )


@router.post("/", response_model=schemas.TestResultOut)
def submit_result(
    payload: schemas.TestResultCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(models.UserRole.ANALYST, models.UserRole.ADMIN)),
):
    assignment = db.get(models.TestAssignment, payload.assignment_id)
    if not assignment:
        raise HTTPException(404, bi("اختصاص آزمون یافت نشد", "Test assignment not found"))

    existing = db.query(models.TestResult).filter_by(assignment_id=payload.assignment_id).first()
    if existing:
        raise HTTPException(400, bi(
            "برای این آزمون قبلا نتیجه ثبت شده است",
            "A result has already been submitted for this assignment",
        ))

    method = assignment.test_method
    spec_type, spec_min, spec_max, unit, decision_rule = _resolve_spec(db, assignment)
    conformity = _evaluate_conformity(
        payload.value, spec_type, spec_min, spec_max,
        method.measurement_uncertainty, decision_rule,
    )

    result = models.TestResult(
        assignment_id=payload.assignment_id,
        value=payload.value,
        unit=unit,
        measurement_uncertainty=method.measurement_uncertainty,
        applied_spec_min=spec_min,
        applied_spec_max=spec_max,
        conformity=conformity,
        tested_by=current_user.id,          # از توکن، نه از بدنهٔ درخواست
        tested_at=datetime.utcnow(),
    )
    db.add(result)
    assignment.status = models.TestAssignmentStatus.RESULT_ENTERED
    db.commit()
    db.refresh(result)
    return result


@router.post("/{result_id}/review", response_model=schemas.TestResultOut)
def review_result(
    result_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(models.UserRole.REVIEWER, models.UserRole.ADMIN)),
):
    result = db.get(models.TestResult, result_id)
    if not result:
        raise HTTPException(404, bi("نتیجه یافت نشد", "Result not found"))
    # 17025 بند 6.2 — تفکیک وظایف: بازبین نباید همان ثبت‌کننده باشد
    if result.tested_by and result.tested_by == current_user.id:
        raise HTTPException(400, bi(
            "ثبت‌کنندهٔ نتیجه نمی‌تواند بازبینِ همان نتیجه باشد",
            "The person who entered the result cannot review it (segregation of duties)",
        ))
    result.reviewed_by = current_user.id
    result.reviewed_at = datetime.utcnow()
    result.assignment.status = models.TestAssignmentStatus.REVIEWED
    db.commit()
    db.refresh(result)
    return result


@router.post("/{result_id}/approve", response_model=schemas.TestResultOut)
def approve_result(
    result_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(models.UserRole.APPROVER, models.UserRole.ADMIN)),
):
    result = db.get(models.TestResult, result_id)
    if not result:
        raise HTTPException(404, bi("نتیجه یافت نشد", "Result not found"))
    if not result.reviewed_by:
        raise HTTPException(400, bi("نتیجه باید ابتدا بازبینی شود", "Result must be reviewed first"))
    # 17025 بند 6.2 — تفکیک وظایف: تأییدکننده نباید همان بازبین یا ثبت‌کننده باشد
    if current_user.id in (result.reviewed_by, result.tested_by):
        raise HTTPException(400, bi(
            "تأییدکنندهٔ نهایی نمی‌تواند بازبین یا ثبت‌کنندهٔ همان نتیجه باشد",
            "The final approver cannot be the reviewer or tester of the same result (segregation of duties)",
        ))

    result.approved_by = current_user.id
    result.approved_at = datetime.utcnow()
    result.assignment.status = models.TestAssignmentStatus.APPROVED

    # اگر همهٔ آزمون‌های نمونه تأیید شده باشند، وضعیت نمونه تکمیل می‌شود
    sample = result.assignment.sample
    all_assignments = db.query(models.TestAssignment).filter_by(sample_id=sample.id).all()
    if all(a.status == models.TestAssignmentStatus.APPROVED for a in all_assignments):
        sample.status = models.SampleStatus.COMPLETED

    db.commit()
    db.refresh(result)
    return result
