# راهنمای استقرار روی VPS — آزمایشگاه تندیس (TPPC)

هدف: وقتی سرور را گرفتی، اپ در چند دقیقه با **دامنهٔ واقعی و HTTPS دائمی** بالا
بیاید و همان دادهٔ فعلی (۱۱۴ نوع نمونه، ۳۰ دستگاه، ۱۸۱ آزمون با ASTM و…) منتقل شود.

معماری تولیدی:
```
اینترنت → Caddy (پورت 80/443، گواهی خودکار Let's Encrypt، اصلاح VirtualHost) → SENAITE :8080
```

---

## ۰) پیش‌نیازها (قبل از شروع)
- **سرور:** Ubuntu 22.04، حداقل ۲ گیگ رم (پیشنهاد **۴ گیگ**)، ۲۰–۴۰ گیگ دیسک.
- **دامنه:** یک رکورد **DNS نوع A** بساز که مثلاً `lims.tandispars.com` به **IP سرور** اشاره کند.
- **پورت‌ها:** 80 و 443 (و 22 برای SSH) روی سرور باز باشند.

---

## ۱) فایل‌هایی که باید به سرور منتقل کنی
از روی کامپیوتر خودت (با `scp` یا هر ابزار انتقال):
- کل پوشهٔ پروژه یا حداقل این‌ها:
  - `docker-compose.prod.yml`
  - `scripts/Caddyfile.prod`
  - `.env.prod.example`
- **ایمیج اپ:** `backups/tandis-lims.tar` (خودکفا، بدون نیاز به اینترنت/رجیستری)
- **آخرین بک‌آپ داده:** `backups/senaite-data-XXXX.tar.gz`

مثال انتقال:
```bash
scp -r docker-compose.prod.yml scripts .env.prod.example \
    backups/tandis-lims.tar backups/senaite-data-XXXX.tar.gz \
    user@SERVER_IP:/home/user/tandis-lims/
```

---

## ۲) نصب Docker روی سرور (یک‌بار)
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER    # سپس یک‌بار logout/login
```

---

## ۳) بارگذاری ایمیج اپ
```bash
cd /home/user/tandis-lims
docker load -i tandis-lims.tar        # ایمیج tandis/lims:latest لود می‌شود
docker images | grep tandis           # بررسی
```

---

## ۴) انتقال داده (بازیابی در volume)
volume را بساز و بک‌آپ فعلی را داخلش باز کن:
```bash
docker volume create senaite_data
docker run --rm -v senaite_data:/data -v "$(pwd)":/backup alpine \
    sh -c "tar xzf /backup/senaite-data-XXXX.tar.gz -C /data && du -sh /data"
```
> اگر می‌خواهی نصب **تازه و خالی** باشد (بدون داده)، این مرحله را رد کن؛ ولی آن‌وقت
> نوع نمونه/دستگاه/آزمون‌ها خالی خواهند بود. برای انتقال آزمایشگاه واقعی، بازیابی کن.

---

## ۵) تنظیم دامنه و بالا آوردن
```bash
cp .env.prod.example .env
nano .env            # LIMS_DOMAIN را با دامنهٔ واقعی خودت جایگزین کن
docker compose -f docker-compose.prod.yml up -d
```
Caddy به‌صورت **خودکار** برای دامنه‌ات گواهی HTTPS می‌گیرد (چند ثانیه تا یکی دو دقیقه).

بررسی وضعیت و لاگ گواهی:
```bash
docker compose -f docker-compose.prod.yml ps
docker logs tandis-caddy --tail 30
```

---

## ۶) باز کردن و تست
مرورگر → **`https://lims.tandispars.com/senaite/`**
- قفل سبز HTTPS باید باشد.
- ورود کارکنان، ثبت نمونه، امور مشتریان، لینک مشتری — همه باید کار کنند.
- لینک فرم‌های عمومی مشتری حالا با همین دامنه است:
  `https://lims.tandispars.com/senaite/@@sample-request`

---

## ۷) امنیت و نگهداری روی سرور
- **فایروال:** فقط پورت‌های لازم:
  ```bash
  sudo ufw allow 22,80,443/tcp && sudo ufw enable
  ```
- **رمز admin** را (اگر روی سرور تازه است) عوض کن: `…/acl_users/users/manage_users`.
- **بک‌آپ خودکار روی سرور** (cron، هر شب ۲۳):
  ```bash
  (crontab -l 2>/dev/null; echo '0 23 * * * docker run --rm -v senaite_data:/data -v /home/user/tandis-lims/backups:/b alpine tar czf /b/senaite-$(date +\%Y\%m\%d).tar.gz -C /data .') | crontab -
  ```
- **به‌روزرسانی اپ در آینده:** ایمیج جدید را `docker load` کن، سپس
  `docker compose -f docker-compose.prod.yml up -d` (داده در volume دست‌نخورده می‌ماند).

---

## کنار اپ «ارتین» روی همان سرور؟
اگر همین سرور اپ ارتین را هم دارد، فقط مطمئن شو:
- ارتین و این اپ **هم‌زمان پورت 80/443 نگیرند**. اگر ارتین از قبل یک reverse proxy
  (nginx/caddy/traefik) دارد، به‌جای Caddy اینجا، یک **ساب‌دامین جدید** در همان
  پروکسی موجود تعریف کن که به `senaite:8080` (یا پورت publishشده) وصل شود — با همان
  خط rewrite در `scripts/Caddyfile.prod`.
- اگر ارتین پورت 80/443 را نگرفته، همین `docker-compose.prod.yml` مستقیم کار می‌کند.

---

## خلاصهٔ فرمان‌ها (بعد از انتقال فایل‌ها)
```bash
docker load -i tandis-lims.tar
docker volume create senaite_data
docker run --rm -v senaite_data:/data -v "$(pwd)":/backup alpine \
    sh -c "tar xzf /backup/senaite-data-XXXX.tar.gz -C /data"
cp .env.prod.example .env && nano .env      # دامنه
docker compose -f docker-compose.prod.yml up -d
```
