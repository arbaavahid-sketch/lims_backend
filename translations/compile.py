"""کامپایل فایل‌های ترجمهٔ .po به .mo (فرمتی که Plone/SENAITE می‌خواند).

اجرا:  python translations/compile.py
بعد از هر تغییر ترجمه، این را اجرا و سپس کانتینر را ری‌استارت کنید:
    docker compose restart senaite
"""
from pathlib import Path

import polib

base = Path(__file__).parent
for po_path in base.glob("*/LC_MESSAGES/*.po"):
    po = polib.pofile(str(po_path), encoding="utf-8")
    mo_path = po_path.with_suffix(".mo")
    po.save_as_mofile(str(mo_path))
    done = len(po.translated_entries())
    total = done + len(po.untranslated_entries())
    print(f"{po_path.relative_to(base)}: {done}/{total} ترجمه → {mo_path.name}")
