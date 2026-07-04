"""بازرس صحت ترجمه‌ها — غلط‌های واقعی (نه سلیقه‌ای) را می‌گیرد.

بررسی می‌کند برای هر رشته‌ای که ما ترجمه کرده‌ایم:
  1) یکپارچگی متغیرها: ${x}, $x, {x}, %s, %(x)s باید در ترجمه هم باشند.
  2) یکپارچگی برچسب‌های HTML: <b>, <br/>, <a ...> باید حفظ شوند.
  3) فاصله/علامت انتهایی: اگر msgid با «فاصله» یا «, » تمام شود، ترجمه هم باید.
  4) ترجمه‌نشده: msgstr نباید عیناً برابر msgid انگلیسی باشد (به‌جز استثناها).
  5) خالی: msgstr نباید خالی باشد.

اجرا:  python translations/qa_check.py
"""
import json
import re
from pathlib import Path

import polib

base = Path(__file__).parent
locales = base.parent / "senaite.core" / "src" / "senaite" / "core" / "locales"

# رشته‌هایی که ما ترجمه کرده‌ایم (از همهٔ batchها)
ours = {}
for d in ["batches", "batches_plone"]:
    for f in sorted((base / d).glob("*.json")):
        ours.update(json.loads(f.read_text(encoding="utf-8")))

# الگوهای متغیر که باید عیناً حفظ شوند
VAR_PATTERNS = [
    r"\$\{[^}]+\}",        # ${recipients}
    r"\{[^}{}]*\}",        # {sid}, {} , {0}
    r"%\([^)]+\)[sdifr]",  # %(name)s
    r"%[sdifr]",           # %s
    r"\$[a-zA-Z_][a-zA-Z0-9_]*",  # $sample_id
]
HTML_RE = re.compile(r"</?[a-zA-Z][^>]*>")

# استثنا: رشته‌هایی که عمداً همان انگلیسی می‌مانند (اختصارات، کد)
IDENTICAL_OK = {
    "DL", "IBN", "NIB", "PDF", "UID", "CBID", "HTML", "html", "WSGI:",
    "${action/title}", "Copy",
}


def tokens(s):
    found = []
    for pat in VAR_PATTERNS:
        found += re.findall(pat, s)
    return sorted(found)


def html_tags(s):
    # نام تگ‌ها را برای مقایسه نرمال می‌کنیم (attrs را نادیده می‌گیریم)
    return sorted(re.findall(r"</?([a-zA-Z][a-zA-Z0-9]*)", s))


def check(po_path):
    po = polib.pofile(str(po_path), encoding="utf-8")
    issues = []
    for e in po:
        if e.obsolete or e.msgid not in ours:
            continue
        mid, mstr = e.msgid, e.msgstr
        if not mstr.strip():
            issues.append(("EMPTY", mid, "")); continue
        if mid == mstr and mid not in IDENTICAL_OK:
            issues.append(("UNTRANSLATED", mid, mstr)); continue
        if tokens(mid) != tokens(mstr):
            issues.append(("VAR-MISMATCH", mid,
                           f"id={tokens(mid)} str={tokens(mstr)}")); continue
        if html_tags(mid) != html_tags(mstr):
            issues.append(("HTML-MISMATCH", mid,
                           f"id={html_tags(mid)} str={html_tags(mstr)}")); continue
        if mid.endswith("  ") and not mstr.endswith(" "):
            issues.append(("TRAIL-SPACE", mid, repr(mstr[-8:])))
        elif mid.endswith(", ") and not mstr.rstrip().endswith("،") \
                and not mstr.endswith(", ") and not mstr.endswith("، "):
            issues.append(("TRAIL-COMMA", mid, repr(mstr[-8:])))
    return issues


all_issues = check(locales / "fa" / "LC_MESSAGES" / "senaite.core.po")
all_issues += check(locales / "fa" / "LC_MESSAGES" / "plone.po")

print(f"بررسی {len(ours)} ترجمهٔ ما...")
if not all_issues:
    print("✅ هیچ غلط ساختاری یافت نشد.")
else:
    print(f"⚠️  {len(all_issues)} مورد:")
    for kind, mid, detail in all_issues:
        print(f"  [{kind}] {mid[:60]!r}")
        print(f"        → {detail[:120]}")
