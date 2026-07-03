from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from .models import (
    UserRole, SampleStatus, TestAssignmentStatus, ConformityStatus,
    EquipmentStatus, ProductType, SpecType,
)


# ---------------- User ----------------
class UserCreate(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.ANALYST


class UserOut(BaseModel):
    id: str
    username: str
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


# ---------------- Equipment ----------------
class EquipmentCreate(BaseModel):
    name: str
    model: Optional[str] = None
    serial_number: Optional[str] = None
    calibration_certificate: Optional[str] = None
    next_calibration_due: Optional[datetime] = None


class EquipmentOut(EquipmentCreate):
    id: str
    status: EquipmentStatus
    last_calibration_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------------- Test Method ----------------
class TestMethodCreate(BaseModel):
    code: str
    name: str
    standard_ref: Optional[str] = None          # ASTM / IP / ISO
    sop_reference: Optional[str] = None
    unit: Optional[str] = None
    measurement_uncertainty: Optional[float] = None
    accredited: bool = False
    default_equipment_id: Optional[str] = None
    spec_min: Optional[float] = None
    spec_max: Optional[float] = None
    description: Optional[str] = None


class TestMethodOut(TestMethodCreate):
    id: str

    class Config:
        from_attributes = True


# ---------------- Product Grade & Specification ----------------
class ProductGradeCreate(BaseModel):
    name: str
    product_type: ProductType
    standard_reference: Optional[str] = None
    description: Optional[str] = None


class ProductGradeOut(ProductGradeCreate):
    id: str

    class Config:
        from_attributes = True


class SpecificationCreate(BaseModel):
    product_grade_id: str
    test_method_id: str
    spec_type: SpecType = SpecType.RANGE
    spec_min: Optional[float] = None
    spec_max: Optional[float] = None
    unit: Optional[str] = None
    decision_rule: str = "simple_acceptance"


class SpecificationOut(SpecificationCreate):
    id: str

    class Config:
        from_attributes = True


# ---------------- Sample ----------------
class SampleCreate(BaseModel):
    sample_code: str
    product_name: str
    product_type: Optional[ProductType] = None
    product_grade_id: Optional[str] = None
    batch_number: Optional[str] = None
    sampling_point: Optional[str] = None
    source: Optional[str] = None
    sampling_datetime: Optional[datetime] = None
    sampled_by: Optional[str] = None
    quantity: Optional[str] = None
    condition_on_receipt: Optional[str] = None
    storage_location: Optional[str] = None
    customer: Optional[str] = None
    notes: Optional[str] = None


class SampleOut(SampleCreate):
    id: str
    status: SampleStatus
    received_date: datetime

    class Config:
        from_attributes = True


# ---------------- Test Assignment ----------------
class TestAssignmentCreate(BaseModel):
    sample_id: str
    test_method_id: str
    equipment_id: Optional[str] = None
    assigned_to: Optional[str] = None


class TestAssignmentOut(BaseModel):
    id: str
    sample_id: str
    test_method_id: str
    equipment_id: Optional[str]
    assigned_to: Optional[str]
    status: TestAssignmentStatus

    class Config:
        from_attributes = True


# ---------------- Test Result ----------------
class TestResultCreate(BaseModel):
    assignment_id: str
    value: float
    # هویت ثبت‌کننده از توکن JWT گرفته می‌شود؛ در بدنه ارسال نمی‌شود.


class TestResultOut(BaseModel):
    id: str
    assignment_id: str
    value: float
    unit: Optional[str]
    measurement_uncertainty: Optional[float]
    applied_spec_min: Optional[float]
    applied_spec_max: Optional[float]
    conformity: ConformityStatus
    tested_by: Optional[str]
    tested_at: Optional[datetime]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    approved_by: Optional[str]
    approved_at: Optional[datetime]

    class Config:
        from_attributes = True
