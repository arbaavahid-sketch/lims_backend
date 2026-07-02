# LIMS - سیستم مدیریت اطلاعات آزمایشگاه (کنترل کیفیت صنعتی)

نسخه اولیه بک‌اند با **FastAPI + PostgreSQL + SQLAlchemy**.

## ساختار پروژه

```
lims_backend/
├── requirements.txt
├── app/
│   ├── main.py          # نقطه ورود برنامه
│   ├── database.py       # اتصال دیتابیس
│   ├── models.py         # مدل‌های SQLAlchemy (جداول)
│   ├── schemas.py        # اسکیماهای Pydantic (ورودی/خروجی API)
│   ├── auth.py           # هش پسورد و JWT
│   └── routers/
│       ├── users.py         # کاربران و لاگین
│       ├── samples.py       # مدیریت نمونه
│       ├── test_methods.py  # روش‌های آزمون و اختصاص به نمونه
│       ├── results.py       # ثبت نتیجه، بازبینی، تأیید
│       └── equipment.py     # تجهیزات و کالیبراسیون
```

## راه‌اندازی سریع

```bash
# ۱- ساخت محیط مجازی و نصب پکیج‌ها
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ۲- ساخت دیتابیس PostgreSQL
createdb lims_db

# ۳- تنظیم متغیر محیطی (اختیاری - در غیر این‌صورت مقدار پیش‌فرض استفاده می‌شود)
export DATABASE_URL="postgresql://lims_user:lims_pass@localhost:5432/lims_db"
export LIMS_SECRET_KEY="یک-رشته-تصادفی-امن"

# ۴- اجرای برنامه
uvicorn app.main:app --reload
```

بعد از اجرا، مستندات تعاملی API به‌صورت خودکار در آدرس زیر در دسترس است:
`http://localhost:8000/docs`

## جریان کاری نمونه (Workflow)

1. `POST /samples` → ثبت نمونه جدید با کد بارکد یکتا
2. `POST /test-methods` → تعریف روش‌های آزمون (یک‌بار، در ابتدای کار)
3. `POST /test-methods/assignments` → اختصاص آزمون به نمونه (وضعیت نمونه به `in_testing` تغییر می‌کند)
4. `POST /results` → ثبت نتیجه توسط اپراتور (pass/fail به‌صورت خودکار بر اساس spec_min/spec_max محاسبه می‌شود)
5. `POST /results/{id}/review` → بازبین نتیجه را تأیید می‌کند
6. `POST /results/{id}/approve` → تأییدکننده نهایی امضا می‌کند؛ وقتی همه آزمون‌های یک نمونه تأیید شوند، وضعیت نمونه به `completed` تغییر می‌کند

## قدم‌های بعدی برای تکمیل پروژه

- [ ] افزودن Alembic برای migration مرحله‌ای دیتابیس (به‌جای `create_all`)
- [ ] پیاده‌سازی `AuditLog` به‌صورت خودکار (مثلاً با SQLAlchemy event listener روی `before_update`/`before_insert`)
- [ ] افزودن ماژول Deviation/CAPA به روترها
- [ ] تولید گواهی آنالیز (CoA) به‌صورت PDF - می‌توان از `reportlab` یا `weasyprint` استفاده کرد
- [ ] محافظت از endpointها با `Depends` روی JWT + بررسی نقش کاربر (RBAC)
- [ ] افزودن تست‌های خودکار (pytest)
- [ ] Dockerfile و docker-compose برای استقرار آسان
- [ ] فرانت‌اند (React/Vue) برای پنل کاربری

## انطباق با ISO/IEC 17025
برای استفاده رسمی در آزمایشگاه کنترل کیفیت، این نکات کلیدی هستند:
- هیچ رکوردی نباید حذف فیزیکی شود (فقط تغییر وضعیت / soft delete)
- هر تغییر در نتایج باید در `AuditLog` ثبت شود
- تفکیک نقش‌ها الزامی است: کسی که نتیجه را ثبت می‌کند نباید همان کسی باشد که تأیید نهایی می‌دهد
