# ایمیج SENAITE ساخته‌شده از سورس فورک خودمان
# پایه: ایمیج رسمی (که سورسش دقیقاً روی همان کامیتی است که فورک ما از آن منشعب شده)
# سپس سورس پایتون با نسخهٔ فورک ما (شامل ترجمه‌های فارسی) جایگزین می‌شود.
FROM senaite/senaite:2.x

# جایگزینی سورس senaite.core با فورک ما — github.com/arbaavahid-sketch/senaite.core (برنچ persian)
COPY senaite.core/src/senaite /home/senaite/senaitelims/src/senaite.core/src/senaite
COPY senaite.core/src/bika /home/senaite/senaitelims/src/senaite.core/src/bika
