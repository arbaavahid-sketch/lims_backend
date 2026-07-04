# LIMS نفتی — سامانه مدیریت اطلاعات آزمایشگاه پالایشگاه و پتروشیمی

Bilingual (FA/EN) Petroleum LIMS — FastAPI + React, aligned with **ISO/IEC 17025**.

سیستم دوزبانه (فارسی/انگلیسی) مدیریت اطلاعات آزمایشگاه کنترل کیفیت فرآورده‌های نفتی، منطبق با الزامات **ISO/IEC 17025**.

## امکانات

- 🧪 مدیریت نمونه‌های نفتی: نقطهٔ نمونه‌گیری، مخزن/واحد، شرایط دریافت (بند 7.3 و 7.4)
- 📏 روش‌های آزمون ASTM/IP با عدم‌قطعیت اندازه‌گیری (بند 7.6)
- 📋 گرید محصول (مثل گازوئیل EN 590) + حدود پذیرش هر آزمون (Specification)
- ⚖️ بیانیهٔ انطباق خودکار conform/nonconform/conditional با قاعدهٔ تصمیم (بند 7.8.6)
- 🔐 JWT + RBAC و تفکیک وظایف: ثبت‌کننده ≠ بازبین ≠ تأییدکننده (بند 6.2)
- 📜 گواهی آنالیز (CoA) دوزبانه به‌صورت PDF — فقط پس از تأیید نهایی همهٔ آزمون‌ها (بند 7.8)
- 🧾 Audit Trail خودکار روی همهٔ جداول با هویت کاربر (بند 8.4)
- 🌐 فرانت‌اند React دوزبانه با چرخش خودکار RTL/LTR

## ساختار

```
lims_backend/
├── app/                  # بک‌اند FastAPI
│   ├── main.py           # نقطهٔ ورود + CORS
│   ├── models.py         # جداول SQLAlchemy
│   ├── schemas.py        # اسکیماهای Pydantic
│   ├── auth.py           # bcrypt + JWT
│   ├── deps.py           # احراز هویت و RBAC
│   ├── audit.py          # لاگ خودکار تغییرات
│   ├── coa.py            # تولید PDF گواهی آنالیز
│   ├── i18n.py           # پیام‌های دوزبانه
│   ├── seed.py           # دادهٔ دمو (آزمایشگاه نفتی)
│   └── routers/          # endpoint ها
├── alembic/              # مهاجرت‌های دیتابیس
├── fonts/                # فونت Vazirmatn برای PDF
├── frontend/             # فرانت‌اند React (Vite)
└── docker-compose.yml    # استقرار کامل
```

## اجرای محلی (توسعه)

**بک‌اند** (پایتون ۳.۱۲+؛ دیتابیس دِو SQLite است، چیزی لازم نیست نصب کنید):

```powershell
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\python -m alembic upgrade head     # ساخت جداول
.\venv\Scripts\python -m app.seed                 # دادهٔ دمو (اختیاری)
.\venv\Scripts\python -m uvicorn app.main:app --reload
```

مستندات API: `http://127.0.0.1:8000/docs`

**فرانت‌اند** (در ترمینال دوم):

```powershell
cd frontend
npm install
npm run dev
```

رابط کاربری: `http://localhost:5173`

**کاربران دمو** (رمز همه: `secret123`): `analyst` / `reviewer` / `approver` / `admin`

## استقرار (Docker)

```bash
cp .env.example .env      # سپس POSTGRES_PASSWORD و LIMS_SECRET_KEY را مقداردهی کنید
docker compose up -d --build
docker compose exec backend python -m app.seed   # دادهٔ دمو (اختیاری)
```

سایت روی پورت 80 بالا می‌آید؛ nginx درخواست‌های `/api` را به بک‌اند پروکسی می‌کند (بدون CORS). دیتابیس استقرار PostgreSQL 16 است و مهاجرت‌ها هنگام شروع کانتینر خودکار اجرا می‌شوند.

## چرخهٔ کاری (Workflow)

1. **analyst**: ثبت نمونه → اختصاص آزمون‌ها → ثبت نتیجه (حکم انطباق خودکار صادر می‌شود)
2. **reviewer**: بازبینی نتیجه (نمی‌تواند ثبت‌کنندهٔ همان نتیجه باشد)
3. **approver**: تأیید نهایی → با تأیید همهٔ آزمون‌ها، نمونه `completed` می‌شود
4. دانلود **گواهی آنالیز (CoA)** از صفحهٔ نمونه — PDF دوزبانه با حدود پذیرش و عدم‌قطعیت
5. **admin**: مرور کامل Audit Trail در `/audit-logs`

## تغییر ساختار دیتابیس

```powershell
# بعد از تغییر مدل‌ها در app/models.py:
.\venv\Scripts\python -m alembic revision --autogenerate -m "توضیح تغییر"
.\venv\Scripts\python -m alembic upgrade head
```

## قدم‌های بعدی (Backlog)

- [ ] ماژول Deviation/CAPA در روترها (مدل آماده است — بند 7.10 و 8.7)
- [ ] صلاحیت پرسنل per-test-method (بند 6.2) و ماتریس آموزش
- [ ] تست‌های خودکار (pytest)
- [ ] نمودار روند (trend) نتایج و کارت کنترل
- [ ] HTTPS با Let's Encrypt در استقرار
