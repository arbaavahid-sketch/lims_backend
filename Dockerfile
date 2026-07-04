# ---------- بک‌اند LIMS — FastAPI ----------
FROM python:3.13-slim

WORKDIR /srv

# نصب وابستگی‌ها (psycopg برای PostgreSQL در استقرار)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt "psycopg[binary]>=3.2"

# کد برنامه + مهاجرت‌ها + فونت فارسی گواهی‌ها
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY fonts ./fonts

EXPOSE 8000

# اول مهاجرت‌های دیتابیس، بعد وب‌سرور
CMD ["sh", "-c", "python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
