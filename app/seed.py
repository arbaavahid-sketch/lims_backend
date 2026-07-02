"""پرکردن دیتابیس با دادهٔ نمونهٔ یک آزمایشگاه نفتی.

اجرا:  python -m app.seed
یک آزمایشگاه فرآوردهٔ نفتی را شبیه‌سازی می‌کند: کاربران با نقش‌های مختلف،
تجهیزات، روش‌های آزمون ASTM، و گرید «گازوئیل یورو ۵ (EN 590)» با مشخصات آن.
"""
from datetime import datetime, timedelta

from .database import SessionLocal, Base, engine
from . import models, auth

Base.metadata.create_all(bind=engine)


def get_or_create(db, model, defaults=None, **kwargs):
    obj = db.query(model).filter_by(**kwargs).first()
    if obj:
        return obj
    params = {**kwargs, **(defaults or {})}
    obj = model(**params)
    db.add(obj)
    db.flush()
    return obj


def run():
    db = SessionLocal()
    try:
        # ---- کاربران با نقش‌های تفکیک‌شده (17025 بند 6.2) ----
        users = {
            "analyst": ("مریم آزمایش‌گر", models.UserRole.ANALYST),
            "reviewer": ("رضا بازبین", models.UserRole.REVIEWER),
            "approver": ("دکتر کریمی (مدیر فنی)", models.UserRole.APPROVER),
            "admin": ("مدیر سیستم", models.UserRole.ADMIN),
        }
        for uname, (full, role) in users.items():
            get_or_create(
                db, models.User, username=uname,
                defaults=dict(
                    full_name=full, email=f"{uname}@refinery-lab.ir",
                    hashed_password=auth.hash_password("secret123"), role=role,
                ),
            )

        # ---- تجهیزات (17025 بند 6.4) ----
        xrf = get_or_create(
            db, models.Equipment, serial_number="XRF-2201",
            defaults=dict(
                name="آنالایزر گوگرد XRF", model="Xplorer S",
                calibration_certificate="CAL-XRF-1404-018",
                last_calibration_date=datetime.utcnow() - timedelta(days=60),
                next_calibration_due=datetime.utcnow() + timedelta(days=120),
            ),
        )
        densmeter = get_or_create(
            db, models.Equipment, serial_number="DM-4500",
            defaults=dict(
                name="چگالی‌سنج دیجیتال", model="DMA 4500",
                calibration_certificate="CAL-DM-1404-007",
                last_calibration_date=datetime.utcnow() - timedelta(days=30),
                next_calibration_due=datetime.utcnow() + timedelta(days=335),
            ),
        )

        # ---- روش‌های آزمون ASTM (17025 بند 7.2 و 7.6) ----
        methods = {
            "SUL": dict(code="QC-SUL-01", name="گوگرد کل", standard_ref="ASTM D4294",
                        unit="mg/kg", measurement_uncertainty=1.5, accredited=True,
                        default_equipment_id=xrf.id),
            "DEN": dict(code="QC-DEN-01", name="چگالی در ۱۵ درجه", standard_ref="ASTM D1298",
                        unit="kg/m³", measurement_uncertainty=0.5, accredited=True,
                        default_equipment_id=densmeter.id),
            "FLP": dict(code="QC-FLP-01", name="نقطهٔ اشتعال", standard_ref="ASTM D93",
                        unit="°C", measurement_uncertainty=1.0, accredited=True),
            "CET": dict(code="QC-CET-01", name="اندیس ستان", standard_ref="ASTM D4737",
                        unit="-", measurement_uncertainty=0.6, accredited=False),
        }
        m = {}
        for k, data in methods.items():
            m[k] = get_or_create(db, models.TestMethod, code=data["code"], defaults=data)

        # ---- گرید محصول: گازوئیل یورو ۵ (EN 590) ----
        grade = get_or_create(
            db, models.ProductGrade, name="گازوئیل یورو ۵ (EN 590)",
            defaults=dict(
                product_type=models.ProductType.GASOIL,
                standard_reference="EN 590",
                description="مشخصات گازوئیل مطابق استاندارد یورو ۵",
            ),
        )

        # ---- مشخصات (specs) گرید (17025 بند 7.8.6) ----
        specs = [
            dict(test_method_id=m["SUL"].id, spec_type=models.SpecType.MAX, spec_max=10.0, unit="mg/kg"),
            dict(test_method_id=m["DEN"].id, spec_type=models.SpecType.RANGE, spec_min=820.0, spec_max=845.0, unit="kg/m³"),
            dict(test_method_id=m["FLP"].id, spec_type=models.SpecType.MIN, spec_min=55.0, unit="°C"),
            dict(test_method_id=m["CET"].id, spec_type=models.SpecType.MIN, spec_min=46.0, unit="-"),
        ]
        for s in specs:
            exists = db.query(models.Specification).filter_by(
                product_grade_id=grade.id, test_method_id=s["test_method_id"]).first()
            if not exists:
                db.add(models.Specification(product_grade_id=grade.id, **s))

        db.commit()
        print("✅ داده‌های اولیه ساخته شد:")
        print(f"   کاربران: {db.query(models.User).count()}")
        print(f"   تجهیزات: {db.query(models.Equipment).count()}")
        print(f"   روش‌های آزمون: {db.query(models.TestMethod).count()}")
        print(f"   گریدها: {db.query(models.ProductGrade).count()}")
        print(f"   مشخصات (specs): {db.query(models.Specification).count()}")
        print(f"   گرید نمونه id={grade.id}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
