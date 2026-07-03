from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_roles
from ..i18n import bi

router = APIRouter(prefix="/samples", tags=["Samples"])


@router.post("/", response_model=schemas.SampleOut)
def create_sample(
    sample: schemas.SampleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles(models.UserRole.ANALYST, models.UserRole.ADMIN)),
):
    existing = db.query(models.Sample).filter_by(sample_code=sample.sample_code).first()
    if existing:
        raise HTTPException(400, bi("کد نمونه تکراری است", "Duplicate sample code"))
    # ثبت‌کنندهٔ نمونه از توکن گرفته می‌شود (نه از بدنهٔ درخواست)
    db_sample = models.Sample(**sample.model_dump(), submitted_by=current_user.id)
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample


@router.get("/", response_model=list[schemas.SampleOut])
def list_samples(
    status: str | None = None,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    q = db.query(models.Sample)
    if status:
        q = q.filter(models.Sample.status == status)
    return q.order_by(models.Sample.received_date.desc()).all()


@router.get("/{sample_id}", response_model=schemas.SampleOut)
def get_sample(
    sample_id: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    sample = db.query(models.Sample).get(sample_id)
    if not sample:
        raise HTTPException(404, bi("نمونه یافت نشد", "Sample not found"))
    return sample


@router.patch("/{sample_id}/status", response_model=schemas.SampleOut)
def update_sample_status(
    sample_id: str,
    status: models.SampleStatus,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_roles(models.UserRole.ANALYST, models.UserRole.ADMIN)),
):
    sample = db.query(models.Sample).get(sample_id)
    if not sample:
        raise HTTPException(404, bi("نمونه یافت نشد", "Sample not found"))
    sample.status = status
    db.commit()
    db.refresh(sample)
    return sample


@router.get("/{sample_id}/coa")
def generate_coa(
    sample_id: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    """گواهی آنالیز (CoA) دوزبانه به‌صورت PDF.

    طبق ISO/IEC 17025 بند 7.8، گزارش فقط پس از تأیید نهایی همهٔ نتایج صادر می‌شود.
    """
    from ..coa import build_coa_pdf

    sample = db.get(models.Sample, sample_id)
    if not sample:
        raise HTTPException(404, bi("نمونه یافت نشد", "Sample not found"))

    assignments = db.query(models.TestAssignment).filter_by(sample_id=sample_id).all()
    if not assignments:
        raise HTTPException(400, bi(
            "هیچ آزمونی به این نمونه اختصاص نیافته است",
            "No tests have been assigned to this sample",
        ))
    not_approved = [a for a in assignments if a.status != models.TestAssignmentStatus.APPROVED]
    if not_approved:
        raise HTTPException(400, bi(
            f"صدور گواهی ممکن نیست؛ {len(not_approved)} آزمون هنوز تأیید نهایی نشده است",
            f"Cannot issue certificate; {len(not_approved)} test(s) not yet approved",
        ))

    results = [{"method": a.test_method, "result": a.result} for a in assignments]

    # نام تأییدکننده(ها) برای بخش امضای گواهی
    approver_ids = {a.result.approved_by for a in assignments if a.result and a.result.approved_by}
    approvers = db.query(models.User).filter(models.User.id.in_(approver_ids)).all()
    approver_names = "، ".join(u.full_name for u in approvers) or "—"

    pdf_bytes = build_coa_pdf(sample, results, approver_names)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="CoA-{sample.sample_code}.pdf"'},
    )
