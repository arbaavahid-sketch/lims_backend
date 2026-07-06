# Phase 1 Service Scope Source - Oil Lab PDF

Source document:

- `D:\Documents\SortedDocs\PDF\شرح خدمات آزمایشگاه روغن.pdf`

Imported/reviewed on: 2026-07-06

## Why This Source Matters

This PDF is useful as a service-scope evidence document for Phase 1 master data.
It lists the lab service scope by product family and test method, so it can be
used to cross-check:

- Analysis Services
- Method References
- Sample/Product Types
- Laboratory service scope for ISO 17025 evidence
- Missing or renamed tests before final SENAITE import

## PDF Structure

The document has 4 pages and covers these service groups:

- Grease laboratory
- Bitumen laboratory
- Antifreeze laboratory
- Oil laboratory
- Hydrocarbon laboratory
- Crude oil laboratory

## Initial Findings

Text extraction found about 81 standard/method references in the PDF.

An initial normalized comparison against
`outputs\tppc_lims_master\TPPC_AnalysisServices_final.xlsx` found:

- 47 references with direct normalized coverage in current Analysis Services.
- 34 references that need review.

Some of the 34 items are likely spelling/format differences, for example method
references written with or without spaces, or source typos such as `INZO` instead
of `INSO`. Others may represent missing or incomplete service coverage.

## Review Candidates

The following references were not found by direct normalized comparison and need
human/master-data review:

- ASTM A1298
- ASTM D 1122
- ASTM D 1123
- ASTM D 113
- ASTM D 1177
- ASTM D 1287
- ASTM D1401
- ASTM D 1796
- ASTM D 3634
- ASTM D 4952
- ASTM D524
- ASTM D5424
- ASTM D5968
- ASTM D 6595
- ASTM D 92
- INSO 1210
- INSO 1212
- INSO 1448
- INSO 15342
- INSO 18481
- INSO 200
- INSO 3169
- INSO 3866
- INSO 3872
- ISIRI 13378
- ISIRI 2949
- ISIRI 340
- ISIRI 4188
- ISIRI 5596
- ISIRI 6228
- ISIRI 8403
- ISIRI 8722
- ISO 15597
- ISO 9029

## How To Use This In Phase 1

1. Keep the PDF as a source of service-scope evidence.
2. Normalize obvious typos/variants before deciding that a service is missing.
3. Compare each product family in the PDF with reviewed Sample Types.
4. Compare each listed test with Analysis Services and Method References.
5. Only add new services after confirming the lab actually performs them and has
   the required method/instrument/responsible-person evidence.

## Current Decision

Use this PDF as a Phase 1 source document, not as an automatic import source.
It is strong evidence for service-scope review, but final master-data changes
should be made only after the review candidates above are resolved.
