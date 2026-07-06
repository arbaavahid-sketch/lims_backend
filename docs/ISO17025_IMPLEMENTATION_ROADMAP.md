# ISO 17025 LIMS Implementation Roadmap

This roadmap is the working plan for turning the current internal SENAITE LIMS
deployment into the requested four-module ISO/IEC 17025-aligned laboratory
system.

## Current Baseline

- The real project path is `D:\Git\lims_backend`.
- The application is an internal SENAITE-based deployment with Persian
  localization, RTL assets, custom Impress report templates, Docker runtime, and
  prepared TPPC/Tandis master-data workbooks.
- Core SENAITE already covers many base LIMS features: samples, analysis
  requests, worksheets, results, verification, publishing, reports, clients,
  contacts, users, roles, methods, calculations, prices, invoices, instruments,
  suppliers, storage locations, lab products, and setup import.
- Prepared data currently includes 31 equipment rows, 84 sample/product types,
  161 analysis services, 127 method/reference rows, and 657 specification rows
  that still need limits before automated pass/fail decisions can be trusted.
- The local container is expected at `http://localhost:8080/senaite`.

## Operating Rule

Work one item at a time. For each item:

1. Inspect the existing SENAITE feature or project customization.
2. Decide whether the need is configuration, data import, template change, or
   custom add-on development.
3. Implement the smallest durable change.
4. Verify in code and, when relevant, in the running container.
5. Record what changed and what remains blocked.

## Phase 0 - Runtime And Safety Baseline

Goal: make sure future work is done on a stable, recoverable local system.

- [x] Confirm `docker compose up -d` starts the SENAITE container cleanly.
- [x] Verify login, dashboard, setup pages, samples, clients, instruments, and
  reports load in the browser.
- [x] Fix any current runtime errors found in container logs.
- [x] Confirm backup and restore commands for the `senaite_data` volume.
- [x] Create a dated backup before each import or schema-changing task.
- [x] Add a short `docs/RUNBOOK.md` for start, stop, backup, restore, rebuild,
  and smoke checks.

Phase 0 notes:

- 2026-07-06: `docker compose up -d` kept service `senaite` running.
- 2026-07-06: GET smoke check returned `200 http://localhost:8080/senaite/login`.
- 2026-07-06: Browser login with the local admin account succeeded and opened
  `http://localhost:8080/senaite/senaite-dashboard`.
- 2026-07-06: Browser checks passed for dashboard, setup, samples, clients,
  instruments, worksheets, report publishing queue, and published samples list.
- 2026-07-06: `docker compose config --volumes` confirmed external volume
  `senaite_data`.
- 2026-07-06: Created data backup
  `backups/senaite-data-20260706-0656.tar.gz`.
- 2026-07-06: Restored that backup into test volume
  `senaite_data_restore_test_20260706_0656`; restored data size was 40.8M and
  expected storage folders existed.
- 2026-07-06: Logs show normal startup and `Ready to handle requests`.
- 2026-07-06: Fixed active runtime error
  `User 'manager' is bound to multiple Contacts` by keeping the first imported
  Lab Contact records for `analyst`, `sampler`, `manager`, and `verifier`, and
  changing the duplicate later-imported records (`labcontact-5` through
  `labcontact-8`) to archived unique usernames.
- 2026-07-06: Rechecked `/senaite/samples?samples_review_state=published` and
  `/senaite/senaite-dashboard`; both returned 200 and the duplicate-contact
  error did not recur in fresh logs.
- 2026-07-06: Known follow-ups remain: HEAD requests to `/senaite` can log a
  Waitress hop-by-hop header assertion, and one previous report render request
  for missing UID `9c445f328b3748ec834046d099eed50f` returned 500.
- 2026-07-06: Before any future Lab Contacts import, make the import/review step
  idempotent so existing usernames are not imported a second time.

Definition of done:

- App opens locally, login works, container logs have no active blocking error,
  and a restore-tested backup exists.

## Phase 1 - Master Data Completion

Goal: finish the one-time system setup data needed before production use.

- [x] Review instrument duplicate codes and missing fields in the generated
  cleanup sheet.
- [ ] Finalize instrument manufacturer, model, serial number, location,
  responsible person, status, calibration date, and calibration interval.
- [x] Review sample/product tree and merge entries that are too granular or
  duplicated.
- [ ] Finalize analysis services: keyword, title, unit, department, method,
  instrument, turnaround, price, and accreditation status.
- [ ] Finalize method references: ASTM, ISO, INSO, internal method code, version,
  and document link.
- [ ] Complete all missing specification limits before using automated
  acceptance/range decisions.
- [ ] Import or re-import setup sheets into SENAITE after review.

Definition of done:

- Setup import succeeds, all mandatory setup objects exist in SENAITE, and the
  cleanup sheet has no high-priority production blockers.

Phase 1 notes:

- 2026-07-06: Reviewed `outputs/tppc_lims_master/TPPC_Instruments_final.xlsx`.
  The final instrument sheet has 30 instruments and no duplicate instrument
  codes.
- 2026-07-06: Remaining instrument data gaps are concentrated on `FTIR`:
  missing model, manufacturer, country, serial number, calibration date, next
  calibration due, and responsible person. `SE` and `saybolt` also need
  `Name FA` review.
- 2026-07-06: Updated `finalize_instruments.py` and regenerated
  `TPPC_Instruments_final.xlsx` so `SE` and `saybolt` have Persian names. The
  only remaining instrument data gap is `FTIR`: manufacturer, country, model,
  serial number, calibration date, next calibration due, and responsible person.
- 2026-07-06: Updated `FTIR` from the Artin Azma product page for
  `INFRALUM FT-08`: manufacturer `Lumex`, country `روسیه`, model
  `INFRALUM FT-08`, and English name `InfraLUM FT-08 FT mid-IR Spectrometer`.
  Regenerated `TPPC_Instruments_final.xlsx`; remaining FTIR QA items are serial
  number, calibration date, next calibration due, and responsible person.
- 2026-07-06: Reviewed
  `outputs/tppc_lims_master/TPPC_AnalysisServices_final.xlsx`: 158 analysis
  services, 0 `REVIEW` mappings, and 6 intentionally blank instrument mappings
  marked as no-device/manual/computational tests.
- 2026-07-06: Reviewed the main `Sample Types` sheet: 84 sample/product rows,
  82 active and 2 inactive, with no exact duplicate codes or titles. The main
  cleanup issue is hierarchy/granularity, not literal duplicates: 22 oil-related
  rows and 30 fuel/naphtha/gasoline rows need product-family decisions.
- 2026-07-06: Reviewed `TPPC_Families_Import.xlsx`; it already prepares a
  family/grade import for antifreeze, grease, gasoline engine oil, and diesel
  engine oil with 30 grade-level sample types and 44 specification rows. Use
  this pattern to finish the product tree instead of flattening every product
  title as a peer sample type.
- 2026-07-06: Added `docs/PHASE1_PRODUCT_TREE_DECISION.md` with the working
  product-family decision. The next implementation step is to generate a
  reviewed sample-type import workbook from that decision, while keeping broad
  source-scope labels out of day-to-day selectable sample types unless the lab
  confirms them.
- 2026-07-06: Added `build_reviewed_sample_types.py` and generated
  `TPPC_SampleTypes_reviewed.xlsx`. Result: 84 source rows, 65 import-ready
  sample types, 17 rows requiring human review, and 2 inactive rows excluded.
  This closes the duplicate/granularity review step; the 17 review rows must be
  approved or remapped before final import.
- 2026-07-06: Reviewed finalized analysis services. `TPPC_AnalysisServices_final.xlsx`
  has 158 services with no missing keyword, title, unit, department,
  turnaround, or method-reference text. Six services intentionally have no
  instrument because they are manual, visual, preparation, sampling, or
  computational steps. `TPPC_SENAITE_Setup.xlsx` still uses placeholder price
  `0` for all services, so financial price finalization remains open.
- 2026-07-06: Added `build_methods_import.py` and generated
  `TPPC_Methods_Import.xlsx`: 170 method records, 374 analysis-service/method
  links, and 5 QA rows where registered-scope keywords are not present in the
  finalized service list. Method document files/links are still empty and must
  be attached before the method-reference item is fully done.
- 2026-07-06: Reviewed specifications. The master `Specifications Missing`
  sheet still has 657 rows with empty `Spec Min`, `Spec Max`, `Unit`, and
  `Acceptance Text`; 54 rows also miss reference year and 570 rows miss
  reference clause. Current prepared specification imports cover 79 data rows:
  9 gasoil rows, 41 family/grade rows, and 29 bitumen rows. Automated pass/fail
  must stay disabled or limited to those reviewed imports until the remaining
  limits are completed.
- 2026-07-06: Added `PHASE1_SERVICE_SCOPE_CROSSWALK.md` from the oil-lab service
  PDF. Row-level result: 61 PDF service rows reviewed, 35 covered by current
  Analysis Services, 15 review rows, 10 add/review rows, and 1 deferred/review
  row. Use this as service-scope evidence and decision support, not as an
  automatic import source.

## Phase 2 - Base Module

Goal: complete the main sample workflow from request to report and invoice.

- [ ] Verify sample request creation for internal staff.
- [ ] Configure sample ID and analysis request ID formats based on customer,
  sample type, test, date, and sequence.
- [ ] Configure analysis request workflow states: request, receive/sample,
  assign, result entry, submit, verify, publish, invoice, dispatch/archive.
- [ ] Verify Excel/multi-upload path for bulk sample registration.
- [ ] Verify barcode/label printing for physical samples.
- [ ] Configure worksheet assignment and distribution of tests between analysts.
- [ ] Verify result entry, interim fields, calculations, limits, flags, and
  verification.
- [ ] Verify report templates show client, sample, result, unit, range, method,
  instrument, remarks, accreditation notes, signature, logo, and bilingual/RTL
  behavior.
- [ ] Configure price lists, member discounts, invoice fields, VAT behavior,
  receipt workflow, and printable invoice.
- [ ] Add or configure financial fields that are missing for local banking and
  invoice requirements.
- [ ] Verify audit trail and history are visible for sample, result, report, and
  invoice changes.
- [ ] Define dashboard metrics for analyst workload and monthly test counts.
- [ ] Design analyst revenue reporting if it cannot be configured from existing
  price and worksheet data.

Definition of done:

- A realistic request can be registered, labeled, assigned, tested, verified,
  reported, invoiced, and traced end to end.

## Phase 3 - Documents Module

Goal: provide usable document handling for ISO 17025 forms, checklists, and
method documents.

- [ ] Inventory current document-related capabilities: attachments, method
  documents, simple files, client attachments, instrument documents, and search.
- [ ] Define document types: procedures, methods, forms, checklists, templates,
  certificates, safety sheets, and controlled records.
- [ ] Decide which document needs versioning, approval, review date, owner,
  department, and retirement state.
- [ ] Implement missing controlled-document metadata if SENAITE does not provide
  enough structure.
- [ ] Add search/filter views for document type, owner, code, method, status,
  and review date.
- [ ] Add reminders for documents near review or expiry.
- [ ] Link method documents to methods and analysis services.

Definition of done:

- Staff can find current approved documents, see obsolete documents separated,
  and link test methods to controlled documents.

## Phase 4 - Instrument Maintenance Module

Goal: complete device registry, calibration, maintenance, and result import.

- [ ] Verify instrument fields: type, brand/manufacturer, model, serial number,
  asset number, supplier, location, supported methods, photo, installation
  certificate, and status.
- [ ] Configure calibration records and certificates.
- [ ] Configure preventive maintenance procedures and maintenance tasks.
- [ ] Configure scheduled tasks for calibration and preventive maintenance.
- [ ] Implement or configure reminder rule for three days before due date.
- [ ] Verify device availability is affected by expired certificate, active
  calibration, validation, QC failure, or maintenance status.
- [ ] Review available instrument import adapters and map them to actual devices.
- [ ] Implement custom result import adapter for NXA devices if no existing
  parser matches the exported file format.
- [ ] Verify GC/GCMS import path, especially Chromatec/Shimadzu export formats.
- [ ] Archive imported device result files and link imported rows to samples,
  analyses, instruments, and analysts.

Definition of done:

- Each active device is traceable, maintenance/calibration due dates are visible,
  reminders work, and supported device outputs can be imported or deliberately
  marked as manual.

## Phase 5 - Inventory Module

Goal: turn the current supplier/storage/lab-product base into a practical
consumables inventory module.

- [ ] Inventory current SENAITE objects: suppliers, storage locations, lab
  products, units, prices, and attachments.
- [ ] Define required consumable fields: category, unit, pack size, lot/batch,
  supplier, expiry date, SDS/MSDS, storage condition, minimum stock, current
  stock, reserved stock, and status.
- [ ] Design stock transactions: receipt, issue/consume, return, adjustment,
  transfer, disposal, and expiry.
- [ ] Link consumable usage to analysis services or methods.
- [ ] Add low-stock and near-expiry reminders.
- [ ] Add supplier evaluation form and supplier status.
- [ ] Add inventory reports: current stock, low stock, expiry, consumption by
  test, and supplier performance.

Definition of done:

- Materials can be received, consumed, traced by lot, warned before shortage or
  expiry, and reported by supplier/test.

## Phase 6 - Customer Panel

Goal: provide customer-facing workflows without exposing internal-only screens.

- [ ] Verify current Client and Contact login behavior.
- [ ] Define what customers may see: own requests, own samples, status, reports,
  invoices, support requests, complaints, and surveys.
- [ ] Configure or build a simplified customer dashboard.
- [ ] Add request registration for customers.
- [ ] Add sample/test selection workflow for customers.
- [ ] Add read-only status tracking for submitted requests.
- [ ] Add report download after publication.
- [ ] Add support request form.
- [ ] Add complaint form with tracking number and internal response workflow.
- [ ] Add satisfaction survey form after report delivery.
- [ ] Verify permissions so customers cannot see other customers' data.

Definition of done:

- A customer can log in, submit a request, track progress, receive reports, and
  submit support/complaint/survey records within strict data isolation.

## Phase 7 - External Integrations

Goal: integrate with local operational systems only after core workflows are
stable.

- [ ] Define SMS provider, message templates, trigger events, and opt-out rules.
- [ ] Implement SMS events for request received, sample accepted, invoice ready,
  report published, and support/complaint updates.
- [ ] Define LAB's net integration requirements, authentication, request format,
  result format, and error handling.
- [ ] Build a test adapter or import/export job for LAB's net.
- [ ] Add retry, logging, and manual reconciliation screens for integrations.
- [ ] Document integration credentials and operational checks without committing
  secrets.

Definition of done:

- Integration events are logged, retryable, and testable without losing sample
  traceability.

## Phase 8 - ISO 17025 Evidence And Reporting

Goal: make compliance evidence easy to retrieve during audits.

- [ ] Map ISO 17025 clauses to system evidence: personnel, equipment, methods,
  calibration, samples, results, reports, complaints, suppliers, and documents.
- [ ] Verify audit trail coverage for key records.
- [ ] Add missing evidence fields where SENAITE defaults are not enough.
- [ ] Create audit-oriented reports for samples, result changes, instrument
  validity, method usage, document review, supplier evaluation, complaints, and
  nonconformities.
- [ ] Add management review data exports where useful.

Definition of done:

- For each major ISO 17025 evidence area, staff know where to enter data and how
  to retrieve it for audit.

## Phase 9 - Security, Roles, And Permissions

Goal: make access control deliberate and testable.

- [ ] Define role matrix: admin, lab manager, technical manager, analyst,
  sampler, finance, document controller, inventory manager, customer, and guest.
- [ ] Map each role to allowed actions and forbidden actions.
- [ ] Configure users, groups, and local roles.
- [ ] Test access for representative users.
- [ ] Review password policy, admin account handling, and backup access.
- [ ] Add permission regression checks for customer data isolation.

Definition of done:

- Each role can do required work, cannot access unrelated data, and the role
  matrix is documented.

## Phase 10 - Production Readiness

Goal: prepare the system for reliable daily use.

- [ ] Finalize Docker image build and internal base image process.
- [ ] Confirm volume backup schedule and restore drill.
- [ ] Configure persistent mail/SMS/integration settings.
- [ ] Add monitoring for container health, disk usage, backups, and errors.
- [ ] Prepare user training checklist.
- [ ] Prepare go-live checklist.
- [ ] Freeze production master data after approval.
- [ ] Run an end-to-end pilot with real-like samples.
- [ ] Record known limitations and post-go-live improvement queue.

Definition of done:

- The lab can use the system daily with a backup plan, support process, and
  agreed limitations.

## Suggested Execution Order

1. Phase 0: runtime and backup safety.
2. Phase 1: master-data cleanup and import.
3. Phase 2: base workflow end-to-end.
4. Phase 4: instruments, calibration, maintenance, and device imports.
5. Phase 3: documents.
6. Phase 5: inventory.
7. Phase 6: customer panel.
8. Phase 7: SMS and LAB's net.
9. Phase 8: audit evidence and compliance reports.
10. Phase 9 and Phase 10: security hardening and production readiness.

## Immediate Next Step

Continue Phase 1 with the remaining master-data blockers:

- Fill remaining real `FTIR` device data: serial number, calibration date,
  next calibration due, and responsible person.
- Review the 17 `review` rows in `TPPC_SampleTypes_reviewed.xlsx` and decide
  whether each is a real selectable sample type, a family label, or source-data
  noise.
- Review the 5 QA rows in `TPPC_Methods_Import.xlsx` and attach or link the
  controlled method documents for each Method.
- Resolve the 26 non-covered rows in
  `docs/PHASE1_SERVICE_SCOPE_CROSSWALK.md`: 15 `Review`, 10 `Add/Review`, and
  1 `Deferred/Review`. Treat the source PDF as service-scope evidence, not as an
  automatic import source.
- Complete specification limits beyond the currently prepared 79 rows before
  enabling broad automated acceptance decisions.
- After those decisions, regenerate the import workbooks and create a fresh
  `senaite_data` backup before importing.
