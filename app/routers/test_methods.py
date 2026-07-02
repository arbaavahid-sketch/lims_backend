from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/test-methods", tags=["Test Methods"])


@router.post("/", response_model=schemas.TestMethodOut)
def create_test_method(method: schemas.TestMethodCreate, db: Session = Depends(get_db)):
    existing = db.query(models.TestMethod).filter_by(code=method.code).first()
    if existing:
        raise HTTPException(400, "کد آزمون تکراری است")
    db_method = models.TestMethod(**method.dict())
    db.add(db_method)
    db.commit()
    db.refresh(db_method)
    return db_method


@router.get("/", response_model=list[schemas.TestMethodOut])
def list_test_methods(db: Session = Depends(get_db)):
    return db.query(models.TestMethod).all()


@router.post("/assignments", response_model=schemas.TestAssignmentOut)
def assign_test_to_sample(payload: schemas.TestAssignmentCreate, db: Session = Depends(get_db)):
    sample = db.query(models.Sample).get(payload.sample_id)
    method = db.query(models.TestMethod).get(payload.test_method_id)
    if not sample or not method:
        raise HTTPException(404, "نمونه یا روش آزمون یافت نشد")

    assignment = models.TestAssignment(**payload.dict())
    db.add(assignment)

    # وقتی اولین آزمون به نمونه اختصاص داده می‌شود، وضعیت نمونه به‌روزرسانی شود
    if sample.status == models.SampleStatus.RECEIVED:
        sample.status = models.SampleStatus.IN_TESTING

    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/assignments/{sample_id}", response_model=list[schemas.TestAssignmentOut])
def list_assignments_for_sample(sample_id: str, db: Session = Depends(get_db)):
    return db.query(models.TestAssignment).filter_by(sample_id=sample_id).all()
