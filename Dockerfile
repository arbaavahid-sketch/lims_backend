# Internal SENAITE image for Tandis Laboratory.
# The base image is retagged locally as lims/senaite-base:2.x so regular
# rebuilds do not depend directly on the upstream senaite/senaite tag.
# Then our forked Python sources, including Persian translations and RTL
# support, replace the base image's senaite.core sources.
FROM lims/senaite-base:2.x

# فونت فارسی خواناتر برای PDFهای WeasyPrint
COPY translations/fonts/tahoma.ttf translations/fonts/tahomabd.ttf \
     /usr/local/share/fonts/tppc/
RUN fc-cache -f /usr/local/share/fonts/tppc

# جایگزینی سورس senaite.core با فورک ما — github.com/arbaavahid-sketch/senaite.core (برنچ persian)
COPY senaite.core/src/senaite /home/senaite/senaitelims/src/senaite.core/src/senaite
COPY senaite.core/src/bika /home/senaite/senaitelims/src/senaite.core/src/bika

# فارسی‌سازی کامل گزارش/گواهی آنالیز (پکیج senaite.impress)
COPY translations/impress/senaite.impress.po translations/impress/senaite.impress.mo \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/locales/fa/LC_MESSAGES/

# راست‌چین‌سازی (RTL) گزارش‌های فارسی — CSS چاپ senaite.impress
COPY translations/impress/print.css \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/browser/static/css/print.css

# اصلاح CSS داخلی گزارش: انتقال شماره صفحه به چپ و جلوگیری از تداخل با فوتر فارسی
COPY translations/impress/css.pt \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/templates/css.pt

# اصلاح قالب‌های گزارش فارسی: هدر، اطلاعات، خلاصه، نتایج و فوتر
COPY translations/impress/reportview.py \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/reportview.py
COPY translations/impress/header.pt \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/templates/header.pt
COPY translations/impress/info.pt \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/templates/info.pt
COPY translations/impress/summary.pt \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/templates/summary.pt
COPY translations/impress/results.pt \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/templates/results.pt
COPY translations/impress/discreeter.pt \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/templates/discreeter.pt
COPY translations/impress/footer.pt \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/analysisrequest/templates/footer.pt
