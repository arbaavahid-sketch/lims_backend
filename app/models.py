import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Float, DateTime, ForeignKey, Enum, Boolean, Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


def gen_uuid():
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ANALYST = "analyst"          # اپراتور/آزمایش‌گر
    REVIEWER = "reviewer"        # بازبین نتایج
    APPROVER = "approver"        # تأییدکننده نهایی (امضاکنندهٔ مجاز)
    VIEWER = "viewer"


class ProductType(str, enum.Enum):
    """نوع فرآوردهٔ نفتی"""
    CRUDE_OIL = "crude_oil"      # نفت خام
    GASOLINE = "gasoline"        # بنزین
    GASOIL = "gasoil"            # گازوئیل/دیزل
    KEROSENE = "kerosene"        # نفت سفید
    JET_FUEL = "jet_fuel"        # سوخت جت (ATK)
    FUEL_OIL = "fuel_oil"        # نفت کوره (مازوت)
    NAPHTHA = "naphtha"          # نفتا
    LPG = "lpg"                  # گاز مایع
    BITUMEN = "bitumen"          # قیر
    LUBE_OIL = "lube_oil"        # روغن پایه/روانکار
    OTHER = "other"


class SampleStatus(str, enum.Enum):
    RECEIVED = "received"
    IN_TESTING = "in_testing"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class TestAssignmentStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESULT_ENTERED = "result_entered"
    REVIEWED = "reviewed"
    APPROVED = "approved"


class SpecType(str, enum.Enum):
    """نوع حد پذیرش برای یک آزمون در یک گرید"""
    MIN = "min"                  # حداقل (مثلاً عدد اکتان ≥ ۹۱)
    MAX = "max"                  # حداکثر (مثلاً گوگرد ≤ ۱۰ ppm)
    RANGE = "range"              # بازه (min ≤ x ≤ max)
    INFORMATIVE = "informative"  # فقط گزارش، بدون صدور حکم انطباق


class ConformityStatus(str, enum.Enum):
    """بیانیهٔ انطباق طبق ISO/IEC 17025 بند 7.8.6"""
    CONFORM = "conform"              # منطبق با مشخصات
    NONCONFORM = "nonconform"        # نامنطبق
    CONDITIONAL = "conditional"      # مشروط (در نوار عدم‌قطعیت نزدیک حد)
    NOT_EVALUATED = "not_evaluated"  # فاقد مشخصات برای ارزیابی


class EquipmentStatus(str, enum.Enum):
    ACTIVE = "active"
    IN_CALIBRATION = "in_calibration"
    OUT_OF_SERVICE = "out_of_service"


# ---------------------------------------------------------------------------
# جداول اصلی
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ANALYST)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    model = Column(String)
    serial_number = Column(String, unique=True)
    status = Column(Enum(EquipmentStatus), default=EquipmentStatus.ACTIVE)
    last_calibration_date = Column(DateTime, nullable=True)
    next_calibration_due = Column(DateTime, nullable=True)
    # 17025 بند 6.4/6.5 — ردیابی‌پذیری اندازه‌شناختی
    calibration_certificate = Column(String, nullable=True)  # شمارهٔ گواهی کالیبراسیون
    created_at = Column(DateTime, default=datetime.utcnow)


class TestMethod(Base):
    """تعریف استاندارد یک آزمون (SOP) نفتی به همراه مرجع ASTM/IP"""
    __tablename__ = "test_methods"

    id = Column(String, primary_key=True, default=gen_uuid)
    code = Column(String, unique=True, nullable=False)        # مثلا QC-SUL-01
    name = Column(String, nullable=False)                     # مثلا اندازه‌گیری گوگرد کل
    standard_ref = Column(String, nullable=True)              # مثلا ASTM D4294 / IP 336 / ISO 3675
    sop_reference = Column(String, nullable=True)             # مرجع دستورالعمل داخلی
    unit = Column(String, nullable=True)                      # واحد اندازه‌گیری
    measurement_uncertainty = Column(Float, nullable=True)    # 17025 بند 7.6 — عدم‌قطعیت اندازه‌گیری
    accredited = Column(Boolean, default=False)               # آیا زیر دامنهٔ اعتباربخشی 17025 است؟
    default_equipment_id = Column(String, ForeignKey("equipment.id"), nullable=True)
    # حد پیش‌فرض روش (در نبود گرید محصول به‌عنوان fallback استفاده می‌شود)
    spec_min = Column(Float, nullable=True)
    spec_max = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    default_equipment = relationship("Equipment")


class ProductGrade(Base):
    """گرید محصول (مثلاً گازوئیل یورو ۵) — مجموعه‌ای از مشخصات برای یک فرآورده"""
    __tablename__ = "product_grades"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, unique=True, nullable=False)        # «گازوئیل یورو ۵ (EN 590)»
    product_type = Column(Enum(ProductType), nullable=False)
    standard_reference = Column(String, nullable=True)        # EN 590 / ISIRI 19446 / ...
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    specifications = relationship(
        "Specification", back_populates="product_grade", cascade="all, delete-orphan"
    )


class Specification(Base):
    """حد پذیرش یک آزمون مشخص برای یک گرید مشخص (17025 بند 7.8.6)"""
    __tablename__ = "specifications"
    __table_args__ = (
        UniqueConstraint("product_grade_id", "test_method_id", name="uq_grade_method"),
    )

    id = Column(String, primary_key=True, default=gen_uuid)
    product_grade_id = Column(String, ForeignKey("product_grades.id"), nullable=False)
    test_method_id = Column(String, ForeignKey("test_methods.id"), nullable=False)
    spec_type = Column(Enum(SpecType), nullable=False, default=SpecType.RANGE)
    spec_min = Column(Float, nullable=True)
    spec_max = Column(Float, nullable=True)
    unit = Column(String, nullable=True)                     # در صورت تفاوت با واحد روش
    # قاعدهٔ تصمیم: simple_acceptance (پیش‌فرض) یا guard_band (لحاظ‌کردن عدم‌قطعیت)
    decision_rule = Column(String, default="simple_acceptance")
    created_at = Column(DateTime, default=datetime.utcnow)

    product_grade = relationship("ProductGrade", back_populates="specifications")
    test_method = relationship("TestMethod")


class Sample(Base):
    __tablename__ = "samples"

    id = Column(String, primary_key=True, default=gen_uuid)
    sample_code = Column(String, unique=True, nullable=False, index=True)  # شناسهٔ یکتا/بارکد (7.4)
    product_name = Column(String, nullable=False)
    product_type = Column(Enum(ProductType), nullable=True)
    product_grade_id = Column(String, ForeignKey("product_grades.id"), nullable=True)
    batch_number = Column(String, nullable=True)

    # اطلاعات نمونه‌گیری (17025 بند 7.3)
    sampling_point = Column(String, nullable=True)           # نقطهٔ نمونه‌گیری
    source = Column(String, nullable=True)                   # مخزن/واحد/خط لوله
    sampling_datetime = Column(DateTime, nullable=True)
    sampled_by = Column(String, nullable=True)               # نام نمونه‌بردار

    # مدیریت آیتم آزمون (17025 بند 7.4)
    quantity = Column(String, nullable=True)                 # مقدار/حجم نمونه
    condition_on_receipt = Column(String, nullable=True)     # وضعیت هنگام دریافت
    storage_location = Column(String, nullable=True)         # محل نگهداری
    customer = Column(String, nullable=True)                 # واحد/مشتری درخواست‌کننده

    received_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(SampleStatus), default=SampleStatus.RECEIVED)
    submitted_by = Column(String, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)

    product_grade = relationship("ProductGrade")
    test_assignments = relationship("TestAssignment", back_populates="sample")


class TestAssignment(Base):
    """اختصاص یک آزمون مشخص به یک نمونه"""
    __tablename__ = "test_assignments"

    id = Column(String, primary_key=True, default=gen_uuid)
    sample_id = Column(String, ForeignKey("samples.id"), nullable=False)
    test_method_id = Column(String, ForeignKey("test_methods.id"), nullable=False)
    equipment_id = Column(String, ForeignKey("equipment.id"), nullable=True)
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(TestAssignmentStatus), default=TestAssignmentStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    sample = relationship("Sample", back_populates="test_assignments")
    test_method = relationship("TestMethod")
    result = relationship("TestResult", back_populates="assignment", uselist=False)


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(String, primary_key=True, default=gen_uuid)
    assignment_id = Column(String, ForeignKey("test_assignments.id"), unique=True, nullable=False)

    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)                     # snapshot واحد در زمان ثبت
    measurement_uncertainty = Column(Float, nullable=True)   # 17025 بند 7.6

    # snapshot حد پذیرشی که حکم بر اساس آن صادر شده (17025 بند 7.8.3 — گزارش‌پذیری)
    applied_spec_min = Column(Float, nullable=True)
    applied_spec_max = Column(Float, nullable=True)
    conformity = Column(Enum(ConformityStatus), default=ConformityStatus.NOT_EVALUATED)

    tested_by = Column(String, ForeignKey("users.id"), nullable=True)
    tested_at = Column(DateTime, nullable=True)

    reviewed_by = Column(String, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    assignment = relationship("TestAssignment", back_populates="result")


class Deviation(Base):
    """ثبت انحراف/کار نامنطبق و اقدام اصلاحی — CAPA (17025 بند 7.10 و 8.7)"""
    __tablename__ = "deviations"

    id = Column(String, primary_key=True, default=gen_uuid)
    sample_id = Column(String, ForeignKey("samples.id"), nullable=True)
    description = Column(Text, nullable=False)
    raised_by = Column(String, ForeignKey("users.id"), nullable=True)
    corrective_action = Column(Text, nullable=True)
    status = Column(String, default="open")  # open / in_progress / closed
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)


class AuditLog(Base):
    """لاگ تغییرات برای انطباق با ISO/IEC 17025 بند 8.4 — هیچ رکوردی حذف فیزیکی نمی‌شود"""
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=gen_uuid)
    table_name = Column(String, nullable=False)
    record_id = Column(String, nullable=False)
    action = Column(String, nullable=False)  # create / update / delete
    changed_by = Column(String, ForeignKey("users.id"), nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
