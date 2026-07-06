# Phase 1 Product Tree Decision

Date: 2026-07-06

This note records the working decision for the SENAITE sample/product tree.
The source review used:

- `outputs/tppc_lims_master/TPPC_LIMS_Master_Data_units_filled.xlsx`
- `outputs/tppc_lims_master/TPPC_Families_Import.xlsx`
- `outputs/tppc_lims_master/build_senaite_setupdata.py`
- `outputs/tppc_lims_master/build_all_families.py`

## Summary

The main `Sample Types` sheet has 84 sample/product rows:

- 82 active rows.
- 2 inactive rows.
- No exact duplicate sample type codes.
- No exact duplicate sample/product titles.

The production risk is not literal duplication. The risk is importing broad
families, product classes, and grade-level products as one flat list. That would
make sample selection noisy and make specifications harder to maintain.

## Decision

Use a product-family plus grade pattern where limits/specifications are grade
specific. Keep broad generic product names only when they are truly used as a
general sample type.

`TPPC_Families_Import.xlsx` already follows this pattern for:

- Antifreeze.
- Grease.
- Gasoline engine oil.
- Diesel engine oil.

It currently prepares 30 grade-level sample types and 44 specification rows.
Use the same pattern for the remaining product families before final import.

## Recommended Families

### Oil And Lubricants

Source review found 25 oil/lubricant related rows with 323 source scope rows.

Recommended handling:

- Keep top family: `روغن و روانکار`.
- Use grade or application-level sample types for real incoming samples.
- Keep generic rows such as `روغن موتور`, `روغن روانکار`, and
  `روغن های روان کننده` only if the lab actually receives samples under those
  generic names.
- Prefer explicit sample types for `روغن موتور بنزینی`,
  `روغن موتور دیزلی`, `روغن هیدرولیک`, `روغن ترانسفورماتور`,
  `روغن دنده`, `روغن پایه`, `روغن کارکرده`, and `روغن کار نکرده`.

Already prepared:

- Gasoline engine oil grades in `TPPC_Families_Import.xlsx`.
- Diesel engine oil grades in `TPPC_Families_Import.xlsx`.
- Grease grades in `TPPC_Families_Import.xlsx`.

### Fuel, Naphtha, And Distillates

Source review found 32 fuel/naphtha/distillate related rows with 123 source
scope rows.

Recommended handling:

- Keep top family: `سوخت، نفتا و فرآورده های تقطیری`.
- Split into practical subfamilies:
  `بنزین`, `نفتا`, `نفت سفید`, `سوخت جت`, `سوخت دیزل/نفت گاز`,
  `بیودیزل`, `سوخت دریایی`, `سوخت کوره/مشعل`, and `سوخت توربین`.
- Merge near-duplicate wording only after checking the standard/specification
  context. Examples needing review:
  `سوخت حاصل از بخش میانی برج تقطیر`,
  `سوخت های حاصل از بخش میانی برج تقطیر`,
  `سوخت های حاصل از تقطیر`,
  `سوخت های نفتی حاصل از تقطیر`.

### Crude Oil And Heavy Products

Source review found 5 crude/heavy product rows with 61 source scope rows.

Recommended handling:

- Keep explicit sample types for `نفت خام`, `نفت کوره`, and `نفت گاز`.
- Review broad rows such as `نفت`, `نفت و گاز`, and
  `نفت خام و فرآورده های نفتی` before importing as selectable sample types.

### Solvents And Hydrocarbons

Source review found 8 solvent/hydrocarbon rows with 23 source scope rows.

Recommended handling:

- Keep top family: `حلال و هیدروکربن`.
- Keep explicit sample types for `حلال های سبک`, `حلال های نفتی ویژه`,
  `پارافین مایع`, and `پارافین مایع صنعتی`.
- Review generic rows `حلال`, `هیدروکربن`, and `هیدروکربن ها`; these may be
  useful as families but too broad as day-to-day sample types.

### Bitumen

Source review found 2 bitumen rows with 6 source scope rows.

Recommended handling:

- Keep `مواد قیری` as family.
- Keep `قیر خالص درجه بندی شده براساس درجه نفوذ` as a specific sample type.
- Use `TPPC_Bitumen_Import.xlsx` for bitumen-specific limits/import work.

### Coolant And Glycol

Source review found 2 coolant/glycol rows with 12 source scope rows.

Recommended handling:

- Keep top family: `ضدیخ / مایعات خنک کننده`.
- Use grade/mixture sample types such as 33 percent and 50 percent antifreeze
  solutions where specifications differ.
- `TPPC_Families_Import.xlsx` already prepares antifreeze grade-level sample
  types and limits.

## Rows Requiring Human Decision

These rows should not be blindly imported as peer sample types until the lab
confirms whether they are real incoming sample names, broad families, or source
scope wording:

- `فرآورده های نفتی` because it has 92 source rows and is probably a broad
  family, not a practical single sample type.
- `فرآورده های میوه ها و سبزی ها` because it appears outside the petroleum
  product domain and may be source-data noise.
- `سایر فرآورده های تقطیری` because it is a catch-all category.
- `نفت خام و فرآورده های نفتی` because it combines family and product wording.
- `فرآورده های نفتی و سوخت های مایع` because it overlaps with fuel families.
- `موتور گازسوز` because it sounds like equipment/application wording, not a
  sample material.
- `پرایمر اصلاح شده` because it may belong under bitumen/coatings and needs
  lab confirmation.
- `گاز` because gas sample workflow/container handling may differ from liquid
  petroleum products.

## Import Rule

Before importing sample types into SENAITE:

1. Keep the original 84-row source list as traceability evidence.
2. Build a reviewed import workbook with family/grade decisions applied.
3. Do not import broad source-scope wording as selectable sample types unless
   the lab confirms they are used in real requests.
4. Keep grade-level sample types wherever specification limits differ.
5. Create a fresh `senaite_data` backup immediately before import.

