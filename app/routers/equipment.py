from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.post("/", response_model=schemas.EquipmentOut)
def create_equipment(item: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    db_item = models.Equipment(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.EquipmentOut])
def list_equipment(db: Session = Depends(get_db)):
    return db.query(models.Equipment).all()


@router.get("/due-for-calibration", response_model=list[schemas.EquipmentOut])
def equipment_due_for_calibration(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    soon = datetime.utcnow() + timedelta(days=30)
    return db.query(models.Equipment).filter(
        models.Equipment.next_calibration_due <= soon
    ).all()
