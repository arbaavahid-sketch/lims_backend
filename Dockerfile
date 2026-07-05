# Internal SENAITE image for Tandis Laboratory.
# The base image is retagged locally as lims/senaite-base:2.x so regular
# rebuilds do not depend directly on the upstream senaite/senaite tag.
# Then our forked Python sources, including Persian translations and RTL
# support, replace the base image's senaite.core sources.
FROM lims/senaite-base:2.x

# جایگزینی سورس senaite.core با فورک ما — github.com/arbaavahid-sketch/senaite.core (برنچ persian)
COPY senaite.core/src/senaite /home/senaite/senaitelims/src/senaite.core/src/senaite
COPY senaite.core/src/bika /home/senaite/senaitelims/src/senaite.core/src/bika

# فارسی‌سازی کامل گزارش/گواهی آنالیز (پکیج senaite.impress)
COPY translations/impress/senaite.impress.po translations/impress/senaite.impress.mo \
     /home/senaite/senaitelims/src/senaite.impress/src/senaite/impress/locales/fa/LC_MESSAGES/
