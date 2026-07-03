from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_roles
from ..i18n import bi

router = APIRouter(prefix="/test-methods", tags=["Test Methods"])


@router.post("/", response_model=schemas.TestMethodOut)
def create_test_method(
    method: schemas.TestMethodCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_roles(models.UserRole.ADMIN)),
):
    existing = db.query(models.TestMethod).filter_by(code=method.code).first()
    if existing:
        raise HTTPException(400, bi("کد آزمون تکراری است", "Duplicate test method code"))
    db_method = models.TestMethod(**method.model_dump())
    db.add(db_method)
    db.commit()
    db.refresh(db_method)
    return db_method


@router.get("/", response_model=list[schemas.TestMethodOut])
def list_test_methods(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return db.query(models.TestMethod).all()


@router.post("/assignments", response_model=schemas.TestAssignmentOut)
def assign_test_to_sample(
    payload: schemas.TestAssignmentCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_roles(models.UserRole.ANALYST, models.UserRole.ADMIN)),
):
    sample = db.query(models.Sample).get(payload.sample_id)
    method = db.query(models.TestMethod).get(payload.test_method_id)
    if not sample or not method:
        raise HTTPException(404, bi("نمونه یا روش آزمون یافت نشد", "Sample or test method not found"))

    assignment = models.TestAssignment(**payload.model_dump())
    db.add(assignment)

    # وقتی اولین آزمون به نمونه اختصاص داده می‌شود، وضعیت نمونه به‌روزرسانی شود
    if sample.status == models.SampleStatus.RECEIVED:
        sample.status = models.SampleStatus.IN_TESTING

    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/assignments/{sample_id}", response_model=list[schemas.TestAssignmentOut])
def list_assignments_for_sample(
    sample_id: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return db.query(models.TestAssignment).filter_by(sample_id=sample_id).all()
