"""اعمال ترجمه‌های دسته‌ای (batches/*.json) روی فایل .po و کامپایل .mo.

اجرا:  python translations/apply.py
سپس:   docker compose restart senaite
"""
import json
from pathlib import Path

import polib

base = Path(__file__).parent
po_path = base / "fa" / "LC_MESSAGES" / "senaite.core.po"
po = polib.pofile(str(po_path), encoding="utf-8")

# همهٔ دسته‌ها را به یک دیکشنری واحد تبدیل کن (دسته‌های بعدی، قبلی‌ها را override می‌کنند)
mapping = {}
for batch_file in sorted(base.glob("batches/*.json")):
    data = json.loads(batch_file.read_text(encoding="utf-8"))
    mapping.update(data)
    print(f"{batch_file.name}: {len(data)} ترجمه")

applied = skipped = 0
for entry in po:
    if entry.obsolete:
        continue
    if entry.msgid in mapping:
        new = mapping[entry.msgid]
        if entry.msgstr != new:
            entry.msgstr = new
            applied += 1
        else:
            skipped += 1

po.save(str(po_path))
po.save_as_mofile(str(po_path.with_suffix(".mo")))

done = len(po.translated_entries())
total = done + len(po.untranslated_entries())
print(f"\nاعمال شد: {applied} | بدون تغییر: {skipped}")
print(f"پوشش فعلی: {done}/{total} ({done/total*100:.1f}%)")
