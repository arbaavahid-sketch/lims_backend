"""تولید گواهی آنالیز (Certificate of Analysis) دوزبانه به‌صورت PDF.

اقلام الزامی گزارش طبق ISO/IEC 17025 بند 7.8.2 پوشش داده شده است:
عنوان، مشخصات آزمایشگاه، شناسهٔ یکتای گواهی، مشخصات نمونه و نمونه‌گیری،
روش‌های آزمون (با مرجع استاندارد)، نتایج با واحد و عدم‌قطعیت، بیانیهٔ انطباق،
امضاکنندهٔ مجاز و تاریخ صدور، و نشانگر پایان گزارش.
"""
import io
import os
from datetime import datetime

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from . import models

# ---------------------------------------------------------------------------
# فونت فارسی — Tahoma در ویندوز؛ برای استقرار لینوکسی بعداً فونت Vazirmatn
# را در پوشهٔ fonts/ پروژه قرار می‌دهیم (candidates پشتیبانی می‌کند).
# ---------------------------------------------------------------------------
_FONT = "Helvetica"
_FONT_BOLD = "Helvetica-Bold"

_CANDIDATES = [
    ("Vazirmatn", os.path.join(os.path.dirname(__file__), "..", "fonts", "Vazirmatn-Regular.ttf"),
     os.path.join(os.path.dirname(__file__), "..", "fonts", "Vazirmatn-Bold.ttf")),
    ("Tahoma", r"C:\Windows\Fonts\tahoma.ttf", r"C:\Windows\Fonts\tahomabd.ttf"),
]
for name, regular, bold in _CANDIDATES:
    if os.path.exists(regular):
        pdfmetrics.registerFont(TTFont(name, regular))
        _FONT = name
        if os.path.exists(bold):
            pdfmetrics.registerFont(TTFont(name + "-Bold", bold))
            _FONT_BOLD = name + "-Bold"
        else:
            _FONT_BOLD = name
        break


def fa(text: str) -> str:
    """متن فارسی را برای رندر صحیح راست‌به‌چپ در PDF آماده می‌کند."""
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(str(text)))


_CONFORMITY_LABELS = {
    models.ConformityStatus.CONFORM: ("منطبق", "Conforms"),
    models.ConformityStatus.NONCONFORM: ("نامنطبق", "Does NOT conform"),
    models.ConformityStatus.CONDITIONAL: ("مشروط", "Conditional"),
    models.ConformityStatus.NOT_EVALUATED: ("ارزیابی‌نشده", "Not evaluated"),
}

# مشخصات آزمایشگاه (بعداً از تنظیمات/دیتابیس خوانده می‌شود)
LAB_NAME_EN = "Petroleum Products Quality Control Laboratory"
LAB_NAME_FA = "آزمایشگاه کنترل کیفیت فرآورده‌های نفتی"


def _spec_text(r: models.TestResult) -> str:
    lo, hi = r.applied_spec_min, r.applied_spec_max
    if lo is not None and hi is not None:
        return f"{lo} – {hi}"
    if lo is not None:
        return f"min {lo}"
    if hi is not None:
        return f"max {hi}"
    return "—"


def build_coa_pdf(sample: models.Sample, results: list[dict], approver_names: str) -> bytes:
    """PDF گواهی آنالیز را می‌سازد و بایت‌های آن را برمی‌گرداند.

    ``results`` لیستی از dict با کلیدهای method (TestMethod) و result (TestResult).
    """
    from reportlab.pdfgen import canvas as _canvas

    buf = io.BytesIO()
    c = _canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    M = 18 * mm  # حاشیه
    y = H - M

    # ---------- سربرگ ----------
    c.setFillColor(colors.HexColor("#1a3c6e"))
    c.rect(0, H - 22 * mm, W, 22 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(_FONT_BOLD, 13)
    c.drawString(M, H - 10 * mm, LAB_NAME_EN)
    c.setFont(_FONT_BOLD, 12)
    c.drawRightString(W - M, H - 17 * mm, fa(LAB_NAME_FA))
    c.setFillColor(colors.black)
    y = H - 32 * mm

    # ---------- عنوان و شمارهٔ گواهی ----------
    c.setFont(_FONT_BOLD, 14)
    c.drawCentredString(W / 2, y, "CERTIFICATE OF ANALYSIS")
    y -= 6.5 * mm
    c.setFont(_FONT_BOLD, 12)
    c.drawCentredString(W / 2, y, fa("گواهی آنالیز"))
    y -= 8 * mm

    issue_dt = datetime.utcnow()
    cert_no = f"CoA-{sample.sample_code}"
    c.setFont(_FONT, 9)
    c.drawString(M, y, f"Certificate No. / {fa('شمارهٔ گواهی')}: {cert_no}")
    c.drawRightString(W - M, y, f"Issue date / {fa('تاریخ صدور')}: {issue_dt.strftime('%Y-%m-%d %H:%M')} UTC")
    y -= 9 * mm

    # ---------- مشخصات نمونه (17025: 7.3 و 7.4) ----------
    c.setFont(_FONT_BOLD, 10)
    c.setFillColor(colors.HexColor("#1a3c6e"))
    c.drawString(M, y, "Sample Information")
    c.drawRightString(W - M, y, fa("مشخصات نمونه"))
    c.setFillColor(colors.black)
    y -= 2 * mm
    c.line(M, y, W - M, y)
    y -= 6 * mm

    rows = [
        ("Sample code", "کد نمونه", sample.sample_code),
        ("Product", "فرآورده", sample.product_name),
        ("Grade", "گرید", sample.product_grade.name if sample.product_grade else "—"),
        ("Batch No.", "شمارهٔ بچ", sample.batch_number or "—"),
        ("Sampling point", "نقطهٔ نمونه‌گیری", sample.sampling_point or "—"),
        ("Source (tank/unit)", "منبع (مخزن/واحد)", sample.source or "—"),
        ("Sampled by", "نمونه‌بردار", sample.sampled_by or "—"),
        ("Sampling date", "تاریخ نمونه‌گیری",
         sample.sampling_datetime.strftime("%Y-%m-%d %H:%M") if sample.sampling_datetime else "—"),
        ("Received date", "تاریخ دریافت", sample.received_date.strftime("%Y-%m-%d %H:%M")),
        ("Customer", "مشتری/واحد", sample.customer or "—"),
    ]
    c.setFont(_FONT, 9)
    for en_label, fa_label, value in rows:
        c.drawString(M, y, f"{en_label}:")
        c.setFont(_FONT_BOLD, 9)
        c.drawString(M + 38 * mm, y, fa(str(value)) if any("؀" <= ch <= "ۿ" for ch in str(value)) else str(value))
        c.setFont(_FONT, 9)
        c.drawRightString(W - M, y, fa(fa_label))
        y -= 5.2 * mm
    y -= 4 * mm

    # ---------- جدول نتایج (17025: 7.8.2 و 7.8.6) ----------
    c.setFont(_FONT_BOLD, 10)
    c.setFillColor(colors.HexColor("#1a3c6e"))
    c.drawString(M, y, "Test Results")
    c.drawRightString(W - M, y, fa("نتایج آزمون"))
    c.setFillColor(colors.black)
    y -= 2 * mm
    c.line(M, y, W - M, y)
    y -= 7 * mm

    # ستون‌ها: روش | استاندارد | نتیجه | واحد | عدم‌قطعیت | حد پذیرش | حکم
    cols = [M, M + 42 * mm, M + 76 * mm, M + 94 * mm, M + 110 * mm, M + 128 * mm, M + 152 * mm]
    headers = [("Test / آزمون", 0), ("Method", 1), ("Result", 2), ("Unit", 3),
               ("±U", 4), ("Spec.", 5), ("Conformity", 6)]
    c.setFont(_FONT_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#eef2f8"))
    c.rect(M - 2, y - 2.5 * mm, W - 2 * M + 4, 6.5 * mm, fill=1, stroke=0)
    c.setFillColor(colors.black)
    for text, i in headers:
        parts = text.split(" / ")
        if len(parts) == 2:
            c.drawString(cols[i], y, parts[0] + " / " + fa(parts[1]))
        else:
            c.drawString(cols[i], y, text)
    y -= 7 * mm

    for item in results:
        method: models.TestMethod = item["method"]
        r: models.TestResult = item["result"]
        conf_fa, conf_en = _CONFORMITY_LABELS[r.conformity]
        c.setFont(_FONT, 8.5)
        c.drawString(cols[0], y, fa(method.name))
        c.drawString(cols[1], y, method.standard_ref or method.code)
        c.setFont(_FONT_BOLD, 8.5)
        c.drawString(cols[2], y, f"{r.value:g}")
        c.setFont(_FONT, 8.5)
        c.drawString(cols[3], y, r.unit or "—")
        c.drawString(cols[4], y, f"{r.measurement_uncertainty:g}" if r.measurement_uncertainty else "—")
        c.drawString(cols[5], y, _spec_text(r))
        if r.conformity == models.ConformityStatus.CONFORM:
            c.setFillColor(colors.HexColor("#1e7d32"))
        elif r.conformity == models.ConformityStatus.NONCONFORM:
            c.setFillColor(colors.HexColor("#c62828"))
        else:
            c.setFillColor(colors.HexColor("#b26a00"))
        c.setFont(_FONT_BOLD, 8.5)
        c.drawString(cols[6], y, f"{conf_en} / " )
        c.drawString(cols[6] + c.stringWidth(f"{conf_en} / ", _FONT_BOLD, 8.5), y, fa(conf_fa))
        c.setFillColor(colors.black)
        y -= 6 * mm

    y -= 4 * mm
    # ---------- یادداشت عدم‌قطعیت و قاعدهٔ تصمیم (7.8.6) ----------
    c.setFont(_FONT, 7.5)
    c.drawString(M, y, "±U: expanded measurement uncertainty (k=2, ~95%). "
                       "Decision rule as per applicable specification.")
    y -= 4.5 * mm
    c.drawRightString(W - M, y, fa("±U: عدم‌قطعیت توسعه‌یافتهٔ اندازه‌گیری (k=2). قاعدهٔ تصمیم مطابق مشخصات مربوطه."))
    y -= 12 * mm

    # ---------- امضا (7.8.2: صادرکنندهٔ مجاز) ----------
    c.setFont(_FONT_BOLD, 9)
    c.drawString(M, y, "Authorized by / " )
    c.drawString(M + c.stringWidth("Authorized by / ", _FONT_BOLD, 9), y, fa("تأییدکنندهٔ مجاز"))
    y -= 5.5 * mm
    c.setFont(_FONT, 9)
    c.drawString(M, y, fa(approver_names) if any("؀" <= ch <= "ۿ" for ch in approver_names) else approver_names)
    y -= 10 * mm
    c.line(M, y, M + 55 * mm, y)
    c.setFont(_FONT, 7.5)
    y -= 4 * mm
    c.drawString(M, y, "Signature / " )
    c.drawString(M + c.stringWidth("Signature / ", _FONT, 7.5), y, fa("امضا"))

    # ---------- پایان گزارش ----------
    c.setFont(_FONT_BOLD, 8.5)
    c.drawCentredString(W / 2, 20 * mm, f"*** END OF REPORT / {fa('پایان گزارش')} ***")
    c.setFont(_FONT, 7)
    c.drawCentredString(W / 2, 15 * mm,
                        "Results relate only to the item tested. This certificate shall not be "
                        "reproduced except in full without written approval of the laboratory.")
    c.drawCentredString(W / 2, 11 * mm,
                        fa("نتایج صرفاً مربوط به آیتم آزمون‌شده است. بازتولید این گواهی جز به‌صورت کامل، بدون تأیید کتبی آزمایشگاه مجاز نیست."))
    c.drawCentredString(W / 2, 6.5 * mm, "Page 1 of 1")

    c.showPage()
    c.save()
    return buf.getvalue()
