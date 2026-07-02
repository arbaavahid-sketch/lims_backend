from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/samples", tags=["Samples"])


@router.post("/", response_model=schemas.SampleOut)
def create_sample(sample: schemas.SampleCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Sample).filter_by(sample_code=sample.sample_code).first()
    if existing:
        raise HTTPException(400, "کد نمونه تکراری است")
    db_sample = models.Sample(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample


@router.get("/", response_model=list[schemas.SampleOut])
def list_samples(status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Sample)
    if status:
        q = q.filter(models.Sample.status == status)
    return q.order_by(models.Sample.received_date.desc()).all()


@router.get("/{sample_id}", response_model=schemas.SampleOut)
def get_sample(sample_id: str, db: Session = Depends(get_db)):
    sample = db.query(models.Sample).get(sample_id)
    if not sample:
        raise HTTPException(404, "نمونه یافت نشد")
    return sample


@router.patch("/{sample_id}/status", response_model=schemas.SampleOut)
def update_sample_status(sample_id: str, status: models.SampleStatus, db: Session = Depends(get_db)):
    sample = db.query(models.Sample).get(sample_id)
    if not sample:
        raise HTTPException(404, "نمونه یافت نشد")
    sample.status = status
    db.commit()
    db.refresh(sample)
    return sample
