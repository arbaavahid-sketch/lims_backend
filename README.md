# SENAITE LIMS — استقرار و فارسی‌سازی

استقرار [SENAITE](https://www.senaite.com) (LIMS متن‌باز سازمانی) برای آزمایشگاه کنترل کیفیت فرآورده‌های نفتی، به‌همراه پروژهٔ **فارسی‌سازی** آن.

Deployment & Persian localization of SENAITE LIMS for a petroleum QC laboratory.

## اجرا / Run

```bash
docker compose up -d
```

- رابط کاربری: `http://localhost:8080/senaite`
- ورود اولیه: `admin` / `admin` — **حتماً بعد از اولین ورود عوضش کنید**
- داده‌ها در volume دائمی `senaite_data` نگهداری می‌شوند

## پشتیبان‌گیری / Backup

```bash
docker run --rm -v senaite_data:/data -v "$PWD/backups":/backup alpine \
  tar czf /backup/senaite-$(date +%Y%m%d).tar.gz -C /data .
```

## ساختار ریپو

```
├── docker-compose.yml    # استقرار SENAITE
└── translations/         # فارسی‌سازی (فایل‌های .po تکمیل‌شده) — در حال انجام
```

## نقشهٔ راه فارسی‌سازی

- [ ] استخراج ترجمهٔ فارسی موجود (`fa`) از senaite.core و ارزیابی میزان پوشش
- [ ] تکمیل ترجمه‌های ناقص (فایل‌های `.po`)
- [ ] تزریق ترجمه‌ها به کانتینر (volume mount روی locales)
- [ ] بررسی امکان راست‌چین‌سازی (RTL) با CSS سفارشی
- [ ] پیکربندی نفتی: Sample Types، Analysis Services با ASTM specs، پنل EN 590

## پروژهٔ قبلی (LIMS اختصاصی FastAPI + React)

نسخه‌ای که از صفر ساختیم (FastAPI، ISO/IEC 17025، CoA دوزبانه، Audit Trail و…) در برنچ
[`custom-fastapi-lims`](https://github.com/arbaavahid-sketch/lims_backend/tree/custom-fastapi-lims)
نگهداری می‌شود.
