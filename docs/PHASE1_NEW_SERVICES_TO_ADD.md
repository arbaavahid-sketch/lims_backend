# Phase 1 - New Analysis Services To Add

Prepared: 2026-07-06
Source of decisions: `docs/PHASE1_SERVICE_SCOPE_CROSSWALK.md` (Resolution Log +
Crosswalk Resolution Summary).

These are the 8 Analysis Services confirmed with the lab technical owner as
gaps that must be created in SENAITE. This document is the staging spec used to
append rows to the setup workbook
(`outputs/tppc_lims_master/TPPC_AnalysisServices_final.xlsx` and
`TPPC_SENAITE_Setup.xlsx`).

## Field status

Fully specified from the crosswalk: title (FA), method references, product
scope, source crosswalk rows, and device/instrument intent.

Must be reconciled with the existing workbook once the Python sandbox is back
(marked `TBC` below): final `keyword` value (existing convention is
`AS_<5 digits>_<3 digit sequence>`), exact `Department` string, exact `Category`
string, canonical `Unit` string, `Instrument` key, `Method` object key,
turnaround days, price, and accreditation flag. Numbers here continue the
existing sequence (last used `_159`), so the next 8 are proposed as `_160`
through `_167` — confirm against the live max before writing.

## Services

### 1. Open-cup flash point (Cleveland), ASTM D92
- Title FA: نقطه اشتعال به روش کاپ باز (کلیولند)
- Method references: ASTM D92; INSO 198
- Unit: °C (درجه سانتی‌گراد)
- Product scope: grease (separated oil), lubricating oil, hydrocarbon
- Covers crosswalk rows: Grease-2, Oil-2, Hydrocarbon-3
- Instrument/device: open-cup (Cleveland) flash point apparatus - TBC against
  instrument list; distinct from the closed-cup Pensky-Martens device used by
  `AS_05147_149`
- Department: physical/flammability - TBC
- Proposed keyword: AS_XXXXX_160 - TBC
- Notes: this is a single shared service for all three product families; do not
  create three separate services.

### 2. Antifreeze pH, ASTM D1287
- Title FA: اندازه‌گیری pH ضدیخ
- Method references: ASTM D1287; INSO 1212
- Unit: pH (بدون واحد)
- Product scope: antifreeze/coolant
- Covers crosswalk row: Antifreeze-1
- Instrument/device: pH meter (confirmed owned by lab)
- Department: chemistry/wet chemistry - TBC
- Proposed keyword: AS_XXXXX_161 - TBC

### 3. Antifreeze freezing point, ASTM D1177
- Title FA: اندازه‌گیری نقطه انجماد ضدیخ
- Method references: ASTM D1177; INSO 1448
- Unit: °C (درجه سانتی‌گراد)
- Product scope: antifreeze/coolant
- Covers crosswalk row: Antifreeze-2
- Instrument/device: freezing-point apparatus/bath - TBC
- Department: physical - TBC
- Proposed keyword: AS_XXXXX_162 - TBC

### 4. Antifreeze relative density, ASTM D1122
- Title FA: اندازه‌گیری چگالی نسبی ضدیخ
- Method references: ASTM D1122
- Unit: (dimensionless ratio) / g/cm3 if reported as density - TBC
- Product scope: antifreeze/coolant
- Covers crosswalk row: Antifreeze-3 (now active; supersedes the PDF's
  "future-capable"/Deferred marking)
- Instrument/device: hydrometer / digital density meter - TBC
- Department: physical - TBC
- Proposed keyword: AS_XXXXX_163 - TBC

### 5. Antifreeze water content, ASTM D1123
- Title FA: اندازه‌گیری درصد آب ضدیخ
- Method references: ASTM D1123; ISIRI 6228
- Unit: % (درصد وزنی)
- Product scope: antifreeze/coolant
- Covers crosswalk row: Antifreeze-4
- Instrument/device: Karl Fischer titrator (D1123 is a K.F. procedure) -
  confirm whether it reuses the existing K.F. device - TBC
- Department: chemistry - TBC
- Proposed keyword: AS_XXXXX_164 - TBC

### 6. Ramsbottom carbon residue, ASTM D524
- Title FA: اندازه‌گیری کربن باقی‌مانده رامزباتم
- Method references: ASTM D524; INSO 200 (PDF Crude Oil-10 cites D5424, treated
  as a typo for D524)
- Unit: % (درصد وزنی)
- Product scope: lubricating oil, crude oil
- Covers crosswalk rows: Oil-13, Crude Oil-10
- Instrument/device: Ramsbottom carbon residue apparatus - TBC
- Department: physical/chemistry - TBC
- Proposed keyword: AS_XXXXX_165 - TBC
- Notes: single shared service for oil + crude oil.

### 7. Chlorine, ISO 15597
- Title FA: اندازه‌گیری کلر
- Method references: ISO 15597; ISIRI 13378
- Unit: mg/kg (or ppm) - TBC
- Product scope: hydrocarbon
- Covers crosswalk row: Hydrocarbon-12
- Instrument/device: XRF (ISO 15597 is an XRF chlorine method) - confirm
  whether it reuses an existing XRF instrument key - TBC
- Department: instrumental - TBC
- Proposed keyword: AS_XXXXX_166 - TBC

### 8. Doctor test, ASTM D4952
- Title FA: آزمون دکتر (تشخیص مرکاپتان/گوگرد فعال)
- Method references: ASTM D4952; ISIRI 8722
- Unit: pass/fail (قبول/رد) - qualitative
- Product scope: hydrocarbon
- Covers crosswalk row: Hydrocarbon-13
- Instrument/device: none (manual/visual chemical test) - like the other 6
  manual services already marked no-device
- Department: wet chemistry - TBC
- Proposed keyword: AS_XXXXX_167 - TBC

## Still open (not in this batch)

Owner will decide later - do NOT add yet:

- Grease-4: water content (PDF method reference D4048/INSO11291 looks like a
  source typo for a corrosion method).
- Bitumen-1: ductility, ASTM D113 / INSO 3866.
- Bitumen-2: specific gravity, ASTM D70 / INSO 3872.

## Next mechanical steps (need Python sandbox)

1. Read `TPPC_AnalysisServices_final.xlsx` to confirm exact column headers,
   the live max keyword sequence, and the canonical Department/Category/Unit/
   Instrument strings.
2. Fill the `TBC` fields to match those conventions.
3. Append the 8 rows; expect service count 158 -> 166.
4. Mirror into `TPPC_SENAITE_Setup.xlsx` (with price placeholder policy).
5. Update roadmap Phase 1 and the crosswalk log.
