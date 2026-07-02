from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/grades", tags=["Product Grades & Specs"])


@router.post("/", response_model=schemas.ProductGradeOut)
def create_grade(grade: schemas.ProductGradeCreate, db: Session = Depends(get_db)):
    existing = db.query(models.ProductGrade).filter_by(name=grade.name).first()
    if existing:
        raise HTTPException(400, "این گرید محصول قبلا تعریف شده است")
    db_grade = models.ProductGrade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.get("/", response_model=list[schemas.ProductGradeOut])
def list_grades(db: Session = Depends(get_db)):
    return db.query(models.ProductGrade).all()


@router.post("/specifications", response_model=schemas.SpecificationOut)
def create_specification(spec: schemas.SpecificationCreate, db: Session = Depends(get_db)):
    grade = db.get(models.ProductGrade, spec.product_grade_id)
    method = db.get(models.TestMethod, spec.test_method_id)
    if not grade or not method:
        raise HTTPException(404, "گرید یا روش آزمون یافت نشد")

    existing = (
        db.query(models.Specification)
        .filter_by(product_grade_id=spec.product_grade_id, test_method_id=spec.test_method_id)
        .first()
    )
    if existing:
        raise HTTPException(400, "برای این گرید و روش آزمون قبلا مشخصات تعریف شده است")

    db_spec = models.Specification(**spec.model_dump())
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec


@router.get("/{grade_id}/specifications", response_model=list[schemas.SpecificationOut])
def list_specifications(grade_id: str, db: Session = Depends(get_db)):
    return db.query(models.Specification).filter_by(product_grade_id=grade_id).all()
