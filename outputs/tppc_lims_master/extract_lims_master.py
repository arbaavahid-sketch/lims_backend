import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl


ROOT = Path(r"D:\Git\lims_backend")
OUT = ROOT / "outputs" / "tppc_lims_master"
EQUIP_FILE = Path(r"D:\TPPC equipments.xlsx")
DOMAIN_FILE = Path(r"D:\لیست دامنه_های ثبت شده.xlsx")


def read_rows(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = [str(v).strip() if v is not None else "" for v in rows[0]]
    data = []
    for row in rows[1:]:
        if not any(v not in (None, "") for v in row):
            continue
        item = {headers[i]: row[i] if i < len(row) else None for i in range(len(headers))}
        data.append(item)
    return headers, data


def clean(value):
    if value is None:
        return ""
    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def latin_code(text, fallback):
    text = clean(text)
    if not text:
        return fallback
    text = text.replace("&", " and ")
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    text = re.sub(r"_+", "_", text)
    return text[:48] or fallback


def fa_hash_code(prefix, text, index):
    # Stable enough for a preparation workbook; final SENAITE keywords can be edited.
    base = abs(hash(clean(text))) % 100000
    return f"{prefix}_{base:05d}_{index:03d}"


equip_headers, equip = read_rows(EQUIP_FILE)
domain_headers, domain_rows = read_rows(DOMAIN_FILE)

equipment_code_counts = Counter(clean(r.get("نام اختصاری دستگاه (لاتین)")) for r in equip)
equipment_seen = Counter()
instruments = []
cleanup = []

for idx, row in enumerate(equip, 1):
    raw_code = clean(row.get("نام اختصاری دستگاه (لاتین)"))
    equipment_seen[raw_code] += 1
    proposed = latin_code(raw_code, f"INST_{idx:03d}")
    if raw_code and equipment_code_counts[raw_code] > 1:
        proposed = f"{proposed}_{equipment_seen[raw_code]:02d}"
        cleanup.append([
            "Instrument duplicate code",
            "Instruments",
            raw_code,
            f"Duplicate code appears {equipment_code_counts[raw_code]} times; proposed unique code: {proposed}",
            "Review and approve final SENAITE code",
        ])
    missing = []
    for src, label in [
        ("نام اختصاری دستگاه (لاتین)", "Instrument code"),
        ("نام دستگاه (فارسی)", "Persian name"),
        ("نام دستگاه (لاتین)", "English name"),
        ("مدل دستگاه", "Model"),
        ("حوزه  تخصصی کاربرد", "Application area"),
    ]:
        if not clean(row.get(src)):
            missing.append(label)
    if missing:
        cleanup.append([
            "Instrument missing field",
            "Instruments",
            proposed,
            ", ".join(missing),
            "Complete before production use",
        ])

    instruments.append([
        proposed,
        raw_code,
        clean(row.get("نام دستگاه (فارسی)")),
        clean(row.get("نام دستگاه (لاتین)")),
        clean(row.get("نام کشور و شرکت سازنده")),
        clean(row.get("مدل دستگاه")),
        clean(row.get("حوزه  تخصصی کاربرد")),
        "",
        "",
        "",
        "",
        "",
        "Active",
        "",
    ])

products_counter = Counter(clean(r.get("محصول")) for r in domain_rows if clean(r.get("محصول")))
sample_types = []
for idx, (product, count) in enumerate(sorted(products_counter.items()), 1):
    sample_types.append([
        fa_hash_code("ST", product, idx),
        product,
        "تجهیزات و فرآورده های نفتی",
        count,
        "Active",
        "",
    ])

tests = defaultdict(lambda: {"refs": set(), "products": set(), "rows": 0})
for row in domain_rows:
    test = clean(row.get("آزمون"))
    if not test:
        continue
    tests[test]["rows"] += 1
    tests[test]["products"].add(clean(row.get("محصول")))
    ref = " ".join(x for x in [
        clean(row.get("نام مرجع")),
        clean(row.get("سال مرجع")),
        clean(row.get("بند مرجع")),
    ] if x)
    if ref:
        tests[test]["refs"].add(ref)

analysis_services = []
test_keywords = {}
for idx, (test, meta) in enumerate(sorted(tests.items()), 1):
    keyword = fa_hash_code("AS", test, idx)
    test_keywords[test] = keyword
    refs = "; ".join(sorted(meta["refs"]))
    products = "; ".join(sorted(p for p in meta["products"] if p)[:8])
    analysis_services.append([
        keyword,
        test,
        "",
        "",
        "",
        "",
        refs,
        len(meta["products"]),
        products,
        meta["rows"],
        "Needs Review",
        "",
    ])

method_refs = []
spec_missing = []
for idx, row in enumerate(domain_rows, 1):
    product = clean(row.get("محصول"))
    test = clean(row.get("آزمون"))
    low = clean(row.get("محدوده از"))
    high = clean(row.get("محدوده تا"))
    keyword = test_keywords.get(test, "")
    ref_row = [
        idx,
        clean(row.get("دامنه")),
        product,
        keyword,
        test,
        clean(row.get("نام مرجع")),
        clean(row.get("سال مرجع")),
        clean(row.get("بند مرجع")),
        low,
        high,
        "Range Missing" if not low and not high else "Has Range",
    ]
    method_refs.append(ref_row)
    if not low and not high:
        spec_missing.append([
            product,
            keyword,
            test,
            clean(row.get("نام مرجع")),
            clean(row.get("سال مرجع")),
            clean(row.get("بند مرجع")),
            "",
            "",
            "",
            "",
            "Missing limits in source workbook",
            "High",
        ])

if spec_missing:
    cleanup.append([
        "Specification limits missing",
        "Specifications Missing",
        f"{len(spec_missing)} rows",
        "All source rows have empty 'محدوده از' and 'محدوده تا'",
        "Provide EN/ASTM/INSO/internal acceptance limits",
    ])

payload = {
    "summary": {
        "equipment_rows": len(equip),
        "domain_rows": len(domain_rows),
        "sample_types": len(sample_types),
        "analysis_services": len(analysis_services),
        "references": len(set(clean(r.get("نام مرجع")) for r in domain_rows if clean(r.get("نام مرجع")))),
        "spec_missing": len(spec_missing),
        "source_files": [str(EQUIP_FILE), str(DOMAIN_FILE)],
    },
    "instruments": {
        "headers": [
            "Instrument Code",
            "Original Short Name",
            "Name FA",
            "Name EN",
            "Manufacturer / Country",
            "Model",
            "Application Area",
            "Serial Number",
            "Calibration Date",
            "Calibration Interval Months",
            "Location",
            "Responsible Person",
            "Status",
            "Notes",
        ],
        "rows": instruments,
    },
    "sample_types": {
        "headers": ["Sample Type Code", "Sample Type / Product", "Domain", "Source Row Count", "Status", "Notes"],
        "rows": sample_types,
    },
    "analysis_services": {
        "headers": [
            "Analysis Keyword",
            "Analysis Title FA",
            "Unit",
            "Department",
            "Instrument Code",
            "Turnaround Days",
            "Method References",
            "Product Count",
            "Example Products",
            "Source Row Count",
            "Status",
            "Notes",
        ],
        "rows": analysis_services,
    },
    "method_references": {
        "headers": [
            "Source Row",
            "Domain",
            "Product",
            "Analysis Keyword",
            "Analysis Title FA",
            "Reference Name",
            "Reference Year",
            "Reference Clause",
            "Range From",
            "Range To",
            "Range Status",
        ],
        "rows": method_refs,
    },
    "spec_missing": {
        "headers": [
            "Product",
            "Analysis Keyword",
            "Analysis Title FA",
            "Reference Name",
            "Reference Year",
            "Reference Clause",
            "Spec Min",
            "Spec Max",
            "Unit",
            "Acceptance Text",
            "Reason",
            "Priority",
        ],
        "rows": spec_missing,
    },
    "cleanup": {
        "headers": ["Issue Type", "Sheet", "Item", "Details", "Recommended Action"],
        "rows": cleanup,
    },
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "lims_master_data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(OUT / "lims_master_data.json")
