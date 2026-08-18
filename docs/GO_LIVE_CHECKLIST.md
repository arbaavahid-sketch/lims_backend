# چک‌لیست راه‌اندازی (Go-Live) — آزمایشگاه تندیس (TPPC)

این فهرست کارهایی است که پیش از تحویل/استفادهٔ واقعی باید تیک بخورد.
وضعیت هر مورد را همین‌جا به‌روز نگه دارید.

## ۱) امنیت
- [x] رمز کاربر `admin` (روت Zope) عوض شد — از `admin/admin` خارج شد.
- [ ] رمز همهٔ کاربران کارمندی قوی شد
      (`http://localhost:8080/senaite/@@usergroup-userprefs` → هر کاربر → رمز).
- [ ] حساب‌های نمونه/آزمایشی که استفاده نمی‌شوند غیرفعال یا حذف شدند.
- [ ] برای کار روزمره از حساب `admin` استفاده نمی‌شود؛ فقط برای تنظیمات سیستم.
      (راهنمای نقش‌ها و ساخت حساب: `docs/ROLES_AND_ACCESS.md`)
- [ ] تنظیم ایمیل خروجی (SMTP) انجام شد — راهنما: `docs/EMAIL_SETUP.md`.

## ۲) بک‌آپ و بازیابی
- [x] اسکریپت بک‌آپ خودکار آماده است: `scripts\backup.ps1` (چرخش N نسخهٔ آخر).
- [x] تمرین بازیابی با موفقیت انجام شد (`scripts\restore.ps1` روی volume تست؛
      فایل `Data.fs` سالم بازیابی شد).
- [ ] بک‌آپ روزانه در Windows Task Scheduler زمان‌بندی شد (راهنما پایین همین صفحه).
- [ ] یک نسخهٔ بک‌آپ خارج از این سیستم هم نگه‌داری می‌شود (فلش/درایو دیگر/فضای ابری).

## ۳) دادهٔ واقعی آزمایشگاه (پیش‌نیاز عملیات واقعی)
- [ ] قیمت آزمون‌ها وارد شد → فاکتور و گزارش درآمد فعال می‌شود.
- [ ] حدود مشخصات (Spec limits) کامل شد → قبول/رد خودکار نتایج معتبر می‌شود.
- [ ] گواهی‌های کالیبراسیون واقعی دستگاه‌ها وارد شد → داشبورد کالیبراسیون معنادار می‌شود.
- [ ] اسناد روش/SOP در «اسناد کنترل‌شده» بارگذاری شد.
- [ ] دادهٔ آزمایشی/دمو پاک شد (انجام‌شده برای امور مشتریان و اسناد).

## ۴) گردش کار مشتری (هستهٔ تحویل)
- [x] فرم عمومی ثبت درخواست کار می‌کند (`@@customer-feedback`).
- [x] درخواست‌ها در «امور مشتریان» می‌آیند و کارمند پاسخ می‌دهد و می‌بندد.
- [x] لینک اختصاصی جواب (توکن یکتا) برای هر درخواست ساخته می‌شود؛ کارمند آن را
      از ستون «لینک مشتری» کپی و برای مشتری می‌فرستد.
- [ ] (اختیاری) ارسال خودکار ایمیل جواب/لینک — نیاز به تنظیم SMTP (فاز ۷).
      پس از آماده‌شدن SMTP (`docs/EMAIL_SETUP.md`) قابل فعال‌سازی است.

## ۵) انتشار/دسترسی
- [ ] HTTPS فعال است (روی سرور reverse proxy؛ یا تونل برای نمایش موقت).
- [ ] آدرس دسترسی به تیم/مشتری اعلام شد.
- [ ] نسخهٔ مستقل ایمیج آماده است: `backups\tandis-lims.tar` (`docker load`).

## ۶) آزمون نهایی (Smoke test) پیش از تحویل
- [ ] ورود کارمند با رمز جدید.
- [ ] ثبت یک درخواست آزمایشی توسط مشتری (InPrivate) → دریافت شمارهٔ پیگیری.
- [ ] مشاهدهٔ درخواست در داشبورد امور مشتریان.
- [ ] نوشتن پاسخ + بستن درخواست.
- [ ] باز کردن «لینک مشتری» و دیدن پاسخ توسط مشتری.
- [ ] گرفتن یک بک‌آپ تازه بلافاصله پیش از تحویل.

---

## زمان‌بندی بک‌آپ روزانه (Windows Task Scheduler)

یک‌بار این دستور را در PowerShell با دسترسی Administrator اجرا کنید تا بک‌آپ هر
روز ساعت ۲۳:۰۰ گرفته شود:

```powershell
$action  = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-ExecutionPolicy Bypass -File `"D:\Git\lims_backend\scripts\backup.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 11:00PM
Register-ScheduledTask -TaskName "TandisLIMS-Backup" -Action $action -Trigger $trigger `
  -Description "Daily backup of SENAITE data volume"
```

بررسی: `Get-ScheduledTask -TaskName "TandisLIMS-Backup"`
اجرای دستی برای تست: `Start-ScheduledTask -TaskName "TandisLIMS-Backup"`

## بازیابی در مواقع اضطراری
```powershell
# ۱) کانتینر را متوقف کنید
docker compose stop
# ۲) بازیابی روی volume اصلی (داده‌های فعلی جایگزین می‌شوند)
powershell -ExecutionPolicy Bypass -File scripts\restore.ps1 `
  -BackupFile backups\senaite-data-XXXX.tar.gz -TargetVolume senaite_data -Confirm
# ۳) دوباره بالا بیاورید
docker compose up -d
```
