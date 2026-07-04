"""اعمال ترجمه‌های دسته‌ای (batches/*.json) روی سورس فورک senaite.core.

ترجمه‌ها مستقیم داخل submodule نوشته می‌شوند (fa و fa_IR) و .mo هم کامپایل می‌شود.

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

# همهٔ دسته‌ها را به یک دیکشنری واحد تبدیل کن (دسته‌های بعدی، قبلی‌ها را override می‌کنند)
mapping = {}
for batch_file in sorted(base.glob("batches/*.json")):
    data = json.loads(batch_file.read_text(encoding="utf-8"))
    mapping.update(data)
    print(f"{batch_file.name}: {len(data)} ترجمه")

for lang in ["fa", "fa_IR"]:
    po_path = locales / lang / "LC_MESSAGES" / "senaite.core.po"
    po = polib.pofile(str(po_path), encoding="utf-8")

    applied = 0
    for entry in po:
        if entry.obsolete:
            continue
        if entry.msgid in mapping and entry.msgstr != mapping[entry.msgid]:
            entry.msgstr = mapping[entry.msgid]
            applied += 1

    po.save(str(po_path))
    po.save_as_mofile(str(po_path.with_suffix(".mo")))

    done = len(po.translated_entries())
    total = done + len(po.untranslated_entries())
    print(f"{lang}: {applied} اعمال شد → پوشش {done}/{total} ({done/total*100:.1f}%)")
