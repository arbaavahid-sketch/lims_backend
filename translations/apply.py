"""اعمال ترجمه‌های دسته‌ای روی سورس فورک senaite.core.

ترجمه‌ها مستقیم داخل submodule نوشته می‌شوند (fa و fa_IR) و .mo هم کامپایل می‌شود.
دو دامنه:
  - batches/*.json        → دامنهٔ senaite.core (رابط اصلی LIMS)
  - batches_plone/*.json  → دامنهٔ plone (رابط مدیریتی فریم‌ورک)

چرخهٔ کار:
    python translations/apply.py
    docker compose up -d --build          # ساخت مجدد ایمیج از سورس
    cd senaite.core && git add -A && git commit && git push   # ثبت در فورک
"""
import json
from pathlib import Path

import polib

base = Path(__file__).parent
locales = base.parent / "senaite.core" / "src" / "senaite" / "core" / "locales"


def load_mapping(subdir):
    mapping = {}
    for batch_file in sorted((base / subdir).glob("*.json")):
        data = json.loads(batch_file.read_text(encoding="utf-8"))
        mapping.update(data)
        print(f"{subdir}/{batch_file.name}: {len(data)} ترجمه")
    return mapping


def apply_domain(domain, mapping):
    if not mapping:
        return
    for lang in ["fa", "fa_IR"]:
        po_path = locales / lang / "LC_MESSAGES" / f"{domain}.po"
        po = polib.pofile(str(po_path), encoding="utf-8")

        existing = {e.msgid: e for e in po if not e.obsolete}
        applied = added = 0
        for msgid, msgstr in mapping.items():
            entry = existing.get(msgid)
            if entry is None:
                # msgid جدید (عنوان محتوای پویا که در .pot استخراج نشده) → افزودن
                po.append(polib.POEntry(msgid=msgid, msgstr=msgstr))
                added += 1
            elif entry.msgstr != msgstr:
                entry.msgstr = msgstr
                applied += 1

        po.save(str(po_path))
        po.save_as_mofile(str(po_path.with_suffix(".mo")))

        done = len(po.translated_entries())
        total = done + len(po.untranslated_entries())
        print(f"{domain} [{lang}]: {applied} به‌روز، {added} افزوده → پوشش {done}/{total} ({done/total*100:.1f}%)")


apply_domain("senaite.core", load_mapping("batches"))
apply_domain("plone", load_mapping("batches_plone"))
