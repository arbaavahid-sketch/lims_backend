"""فارسی‌سازی کامل گزارش/گواهی (پکیج senaite.impress).

خروجی: translations/impress/senaite.impress.po + .mo (برای override در Dockerfile).
اجرا: python translations/translate_impress.py
"""
from pathlib import Path
import polib

PO = Path(__file__).parent / "impress" / "senaite.impress.po"

T = {
    "Active templates": "قالب‌های فعال",
    "Advanced": "پیشرفته",
    "All": "همه",
    "Allow PDF download": "اجازهٔ دانلود PDF",
    "Allow PDF email share": "اجازهٔ اشتراک PDF با ایمیل",
    "Allow direct download of the generated report": "اجازهٔ دانلود مستقیم گزارش تولیدشده",
    "Allow to share the generated PDF directly via email": "اجازهٔ اشتراک مستقیم PDF تولیدشده از طریق ایمیل",
    "Analysis Report": "گزارش آنالیز",
    "Analysis results relate only to the samples tested.": "نتایج آنالیز فقط به نمونه‌های آزمون‌شده مربوط می‌شوند.",
    "Attachment for": "پیوست برای",
    "Attachments for ${DYNAMIC_CONTENT}": "پیوست‌های ${DYNAMIC_CONTENT}",
    "Attachments per Row": "پیوست در هر ردیف",
    "Available Templates": "قالب‌های موجود",
    "Batch ID": "شناسه بچ",
    "Batch Labels": "برچسب‌های بچ",
    "Client": "مشتری",
    "Client Batch ID": "شناسه بچ مشتری",
    "Client ID": "شناسه مشتری",
    "Client SID": "شناسه نمونهٔ مشتری",
    "Contact": "مخاطب",
    "Date Published": "تاریخ انتشار",
    "Date Received": "تاریخ دریافت",
    "Date Sampled": "تاریخ نمونه‌گیری",
    "Date Verified": "تاریخ تأیید",
    "Default Orientation": "جهت پیش‌فرض",
    "Default Paper Format": "قطع کاغذ پیش‌فرض",
    "Default Template": "قالب پیش‌فرض",
    "Developer Mode": "حالت توسعه‌دهنده",
    "Download the generated PDF to your computer": "دانلود PDF تولیدشده روی رایانهٔ شما",
    "Email sent": "ایمیل ارسال شد",
    "Failed to send Email": "ارسال ایمیل ناموفق بود",
    "Filename:": "نام فایل:",
    "Footer Text": "متن پاورقی",
    "Generated reports for: {}, ": "گزارش‌های تولیدشده برای: {}، ",
    "HTML to PDF report engine for SENAITE": "موتور گزارش HTML به PDF برای سامانه",
    "ID": "شناسه",
    "Impress Settings": "تنظیمات گزارش",
    "Initially loaded orientation": "جهت بارگذاری اولیه",
    "Initially loaded paper format": "قطع کاغذ بارگذاری اولیه",
    "Initially loaded report template": "قالب گزارش بارگذاری اولیه",
    "Methods included in the ${accreditation_body} schedule of Accreditation for this Laboratory. Analysis remarks are not accredited":
        "روش‌ها در دامنهٔ اعتباربخشی ${accreditation_body} این آزمایشگاه گنجانده شده‌اند. ملاحظات آنالیز اعتباربخشی‌شده نیستند",
    "Not invoiced": "فاکتورنشده",
    "Number of attachments rendered within one row per Analysis Request": "تعداد پیوست‌های نمایش‌داده‌شده در یک ردیف برای هر نمونه",
    "PDF attachment is missing": "پیوست PDF موجود نیست",
    "Please choose the templates that can be selected": "قالب‌هایی که قابل انتخاب‌اند را برگزینید",
    "Provisional report": "گزارش موقت",
    "Published by": "منتشرشده توسط",
    "Range": "بازه",
    "Registered": "ثبت‌شده",
    "Reload after reorder": "بارگذاری مجدد پس از مرتب‌سازی",
    "Reload report automatically when items order changed": "بارگذاری خودکار گزارش هنگام تغییر ترتیب آیتم‌ها",
    "Report Options": "گزینه‌های گزارش",
    "Report Settings": "تنظیمات گزارش",
    "Responsibles": "مسئولین",
    "Result": "نتیجه",
    "Result out of client specified range.": "نتیجه خارج از بازهٔ تعیین‌شدهٔ مشتری.",
    "Results": "نتایج",
    "Returns the raw HTML in the report preview.": "HTML خام را در پیش‌نمایش گزارش برمی‌گرداند.",
    "SENAITE IMPRESS": "موتور گزارش",
    "SENAITE IMPRESS Settings": "تنظیمات موتور گزارش",
    "Sample ID": "شناسهٔ نمونه",
    "Sample Point": "نقطهٔ نمونه‌گیری",
    "Sample Type": "نوع نمونه",
    "Share PDF via email": "اشتراک PDF از طریق ایمیل",
    "Show Sample Remarks": "نمایش ملاحظات نمونه",
    "Specification": "مشخصات",
    "Store Multi-Report PDFs Individually": "ذخیرهٔ جداگانهٔ PDFهای چندگزارشی",
    "Store generated multi-report PDFs individually. Turn off to store the multi-report PDF only for the primary item of the report":
        "PDFهای چندگزارشی تولیدشده را جداگانه ذخیره کن. برای ذخیرهٔ فقط برای آیتم اصلی گزارش، خاموش کنید",
    "Summary": "خلاصه",
    "Supervisor": "سرپرست",
    "Test results are at a ${lab_confidence}% confidence level": "نتایج آزمون در سطح اطمینان ${lab_confidence}٪ هستند",
    "The footer text will be rendered on every PDF page and may contain arbitrary HTML":
        "متن پاورقی در هر صفحهٔ PDF نمایش داده می‌شود و می‌تواند شامل HTML دلخواه باشد",
    "This Analysis Request has been invalidated due to erroneously published results":
        "این نمونه به‌دلیل انتشار نادرست نتایج باطل شده است",
    "This Analysis request has been replaced by": "این نمونه جایگزین شده است با",
    "This document shall not be reproduced except in full, without the written approval of ${name_lab}":
        "این سند جز به‌صورت کامل و بدون تأیید کتبی ${name_lab} قابل بازتولید نیست",
    "Title": "عنوان",
    "Unit": "واحد",
    "Workflow State": "وضعیت گردش‌کار",
    "Workflow State ID": "شناسهٔ وضعیت گردش‌کار",
}

po = polib.pofile(str(PO), encoding="utf-8")
n = 0
for e in po:
    if e.msgid in T:
        e.msgstr = T[e.msgid]
        n += 1
po.save(str(PO))
po.save_as_mofile(str(PO.with_suffix(".mo")))
done = len(po.translated_entries())
print(f"ترجمه شد: {n}/{len(T)} | پوشش po: {done}/{done+len(po.untranslated_entries())}")
