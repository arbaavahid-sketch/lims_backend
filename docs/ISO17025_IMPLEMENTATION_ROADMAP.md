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
- 2026-07-06: Resolved 23 of the 26 open crosswalk rows with the lab technical
  owner (see the Resolution Log and Summary in
  `docs/PHASE1_SERVICE_SCOPE_CROSSWALK.md`). 12 rows confirmed `Covered` by
  existing services (some need a method-reference/product-scope correction
  only). 8 new Analysis Services were confirmed as needed: open-cup flash
  point D92 (shared by grease/oil/hydrocarbon), antifreeze pH, antifreeze
  freezing point, antifreeze relative density, antifreeze water content,
  Ramsbottom carbon residue (shared by oil/crude oil), chlorine, and doctor
  test. 3 rows remain open for a later session: Grease-4 water content,
  Bitumen-1 ductility, Bitumen-2 specific gravity.

- 2026-07-06: Created the confirmed new Analysis Services via
  `outputs/tppc_lims_master/TPPC_NewServices_Import.xlsx` (incremental import,
  keywords `NEW_*`). Service count went 176 -> 181. Added: open-cup Cleveland
  flash point ASTM D92 (dept هیدروکربن, shared), Ramsbottom carbon residue ASTM
  D524 (dept روغن), total chlorine ISO 15597 (dept هیدروکربن), doctor test ASTM
  D4952 (dept هیدروکربن), and antifreeze water content ASTM D1123 (dept ضدیخ).
  The other 3 of the 8 confirmed rows (antifreeze pH, freezing point, relative
  density) were NOT recreated because equivalents already exist from the earlier
  family import (`pH محلول 50%`, `نقطه انجماد محلول 33%/50%`, `دانسیته/چگالی
  نسبی` services) — avoided duplicates. Backup `before-newservices.tar.gz` taken
  before import. Still open (deferred to a later session per crosswalk):
  Grease-4 water content, Bitumen-1 ductility, Bitumen-2 specific gravity, plus
  method-document links and remaining specification limits.

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

Phase 2 notes:

- 2026-07-05: Verified end-to-end workflow live (client -> contact -> sample
  register -> receive -> result entry -> submit -> verify by a different user ->
  publish -> Persian RTL CoA PDF). Segregation of duties held: verifier could
  not be the submitter.
- 2026-07-05: Sample/AnalysisRequest ID format changed in the UI (Setup edit)
  to `{clientId}-{sampleType}-{year}-{seq:04d}`. Note: the setupdata IDFormatting
  importer is commented out (`# setIDFormatting`), so ID format is UI-only, not
  importable. Clients need a Client ID set for `{clientId}` to populate.
- 2026-07-05: Configured ISO-17025 workflow settings via Setup import
  (`TPPC_ISO_Settings_Import.xlsx`): `EnableGlobalAuditlog=1` (clause 8.4),
  `SelfVerificationEnabled=0` (segregation of duties), and
  `NumberOfRequiredVerifications=1`. bika_setup Setup importer converts booleans
  via `to_bool`, so "0"/"1" map correctly. `getNumberOfRequiredVerifications`
  confirmed `1` after import.
- 2026-07-05: Built the analyst performance dashboard as a custom view
  `@@analyst-performance` (senaite.core fork,
  `browser/analystperformance/`). Per-analyst count of performed analyses
  (result captured) + revenue (sum of analysis prices), optional date range
  (`?from=&to=`), RTL Persian. Verified live: دکتر مدیرفنی 20, منصور آزمایش‌گر 1,
  total 21; revenue 0 until service prices are entered. Gotcha: `getAnalyst` is
  an index but NOT catalog metadata, so read it from the object, not the brain.
  TODO: add a nav/dashboard link to this view; consider indexing price for perf.
- Still open in Phase 2: price lists/per-service prices (all 0, need data),
  printable invoice + receipt workflow, and bulk Excel sample upload
  verification.

## Phase 3 - Documents Module

Goal: provide usable document handling for ISO 17025 forms, checklists, and
method documents.

- [x] Inventory current document-related capabilities: attachments, method
  documents, simple files, client attachments, instrument documents, and search.
- [x] Define document types: procedures, methods, forms, checklists, templates,
  certificates, safety sheets, and controlled records.
- [x] Decide which document needs versioning, approval, review date, owner,
  department, and retirement state.
- [x] Implement missing controlled-document metadata if SENAITE does not provide
  enough structure.
- [x] Add search/filter views for document type, owner, code, method, status,
  and review date.
- [~] Add reminders for documents near review or expiry.
- [~] Link method documents to methods and analysis services.

Definition of done:

- Staff can find current approved documents, see obsolete documents separated,
  and link test methods to controlled documents.

Phase 3 notes:

- 2026-07-06: Inventory. SENAITE natively has: `Method.MethodDocument` (single
  file per method), the `Multifile` Dexterity type (only used for instrument
  documents; fields document_id/file/version/location/type), sample & analysis
  attachments, published reports, and `Method.Accredited`. It has NO controlled
  document register, no approval workflow, no owner/department/effective/review
  dates, no cross-document search, and no review reminders. User chose the FULL
  ISO 17025 build.
- 2026-07-06: Built the Controlled Documents module in the senaite.core fork:
  - Two Dexterity content types: `ControlledDocuments` (setup container) and
    `ControlledDocument` (item). Item fields: document_id (code), title,
    document_type (SOP/method/form/checklist/template/certificate/SDS/record),
    version, owner, department, effective_date, review_date, related_methods,
    file, notes. Files: content/controlleddocument.py, controlleddocuments.py;
    FTIs types/ControlledDocument.xml + ControlledDocuments.xml; registered in
    types.xml; container added to setuphandlers add_senaite_setup_items.
  - Approval workflow `senaite_controlleddocument_workflow`: draft (initial) ->
    approve -> effective -> retire -> obsolete; effective/obsolete -> revise ->
    draft. approve/retire guarded by "Review portal content" and revise too, so
    an author with only "Modify portal content" cannot approve their own draft
    (segregation of duties). effective/obsolete states remove Modify/Delete in
    place. Bound in workflows.xml.
  - Register listing view in the setup control panel
    (browser/controlpanel/controlleddocuments) with All/Effective/Draft/Obsolete
    filters and columns code/title/type/version/next-review/state.
  - Bilingual (fa/en, RTL/LTR) "Document Review Status" dashboard
    `@@document-review-status` (browser/documentstatus): per-document next review
    date, days-left, colour-coded status (up to date / due soon / overdue / no
    review date), configurable `?days=` window, summary badges. Setup tile added.
  - Live installer view `@@install-documents-module` (Manager-only,
    browser/installdocuments) that re-runs the typeinfo/workflow/rolemap import
    steps and creates the container in the existing ZODB, because baking the FTI
    into the image is not enough for an already-installed site.
- 2026-07-06: Installed and verified live. Container at
  `/senaite/setup/controlleddocuments`. Created a doc via JSON API, confirmed
  initial state draft, drove approve->effective->retire->obsolete->revise->draft
  through content_status_modify, and confirmed the review dashboard lists it.
  Gotchas: (1) `--` is illegal inside XML comments (broke the workflow import
  first time, fixed the ASCII arrows); (2) senaite.jsonapi cannot set schema.Date
  fields from a string (WrongType) and its "delete" route performs a deactivate
  transition our type does not have — set dates and delete from the UI instead.
- Still open / partial in Phase 3: (a) review/expiry reminders are visual only
  in the dashboard; push notifications (email/SMS) deferred to Phase 7. (b)
  related_methods is a free-text field for now, not a hard UIDReference to Method
  / AnalysisService objects - a real reference link is a follow-up. (c) one demo
  ControlledDocument ("ST75 - density method", draft) remains in the register;
  it can be deleted from the UI. Real controlled documents (files + review dates)
  need to be entered by the lab.

## Phase 4 - Instrument Maintenance Module

Goal: complete device registry, calibration, maintenance, and result import.

- [x] Verify instrument fields: type, brand/manufacturer, model, serial number,
  asset number, supplier, location, supported methods, photo, installation
  certificate, and status.
- [x] Configure calibration records and certificates.
- [x] Configure preventive maintenance procedures and maintenance tasks.
- [x] Configure scheduled tasks for calibration and preventive maintenance.
- [~] Implement or configure reminder rule for three days before due date.
- [x] Verify device availability is affected by expired certificate, active
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

Phase 4 notes:

- 2026-07-06: Inspected native instrument model. SENAITE already provides the
  full registry: Instrument (Manufacturer, Supplier, Model, SerialNo, Methods,
  AssetNumber, InstrumentLocation, Photo, InstallationCertificate) plus
  InstrumentCalibration, InstrumentCertification, InstrumentMaintenanceTask,
  InstrumentScheduledTask, InstrumentValidation, InstrumentType,
  InstrumentLocation. So instrument fields, calibration/certificate records,
  maintenance procedures/tasks, and scheduled tasks are configuration, not
  development. Availability logic is native too: `Instrument.isValid()`,
  `isOutOfDate()`, `isQCValid()`, `getLatestValidCertification()`,
  `getCertificateExpireDate()`, and `InstrumentCertification.getDaysToExpire()`.
- 2026-07-06: Built a custom cross-instrument calibration status dashboard
  `@@instrument-status` (senaite.core fork, `browser/instrumentstatus/`).
  SENAITE only had a per-instrument certifications tab; this view lists every
  instrument with its latest certificate ValidTo, days-to-expire, and a status
  flag (valid / due soon / expired / no certificate), colour-coded, with a
  configurable warning window (`?days=`, default 30) and a summary badge row.
  Bilingual fa/en with RTL/LTR switch. Added a bilingual setup-overview tile for
  it (and one for `@@analyst-performance`).
- 2026-07-06: Live result with current master data: 30 instruments, ALL 30 in
  state "no certificate" (0 valid / 0 due / 0 expired). This is a real ISO 17025
  finding: no calibration certification records have been entered for any device
  yet. The dashboard now makes that gap visible at a glance.
- 2026-07-06: Reminder rule (three days before due) marked `[~]` partial: the
  status window surfaces due/expired instruments visually, but automatic
  push reminders (email/SMS) are deferred to Phase 7 (External Integrations).
- Still open in Phase 4 (need USER data / device files): enter real calibration
  certificates (ValidFrom/ValidTo, provider) per instrument; FTIR serial +
  calibration dates + responsible person; map instrument import adapters to the
  actual device export formats (NXA, GC/GCMS Chromatec/Shimadzu) — blocked until
  sample export files are provided.

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

- [x] Verify current Client and Contact login behavior.
- [x] Define what customers may see: own requests, own samples, status, reports,
  invoices, support requests, complaints, and surveys.
- [x] Configure or build a simplified customer dashboard.
- [x] Add request registration for customers.
- [x] Add sample/test selection workflow for customers.
- [x] Add read-only status tracking for submitted requests.
- [x] Add report download after publication.
- [x] Add support request form.
- [x] Add complaint form with tracking number and internal response workflow.
- [x] Add satisfaction survey form after report delivery.
- [~] Verify permissions so customers cannot see other customers' data.

Definition of done:

- A customer can log in, submit a request, track progress, receive reports, and
  submit support/complaint/survey records within strict data isolation.

Phase 6 notes:

- 2026-07-06: Inventory. Native SENAITE already provides most of the customer
  panel: Client Contacts can be given a Plone login with the "Client" role
  (browser/clients/client/contacts/login_details.py); the Client/local-role +
  senaite_sample_workflow scope each contact to their own Client only (data
  isolation); logged-in clients can register ARs, select tests, track status and
  download published reports. What was missing entirely: complaints, surveys and
  support requests (no native content types).
- 2026-07-06: Built the Customer Care module in the senaite.core fork (all three,
  user picked full scope):
  - Container `CustomerCare` (setup folder) + three item types: `Complaint`
    (ISO 7.9: subject, client, contact, related sample, category, severity,
    received date, description, internal investigation + resolution),
    `SupportRequest` (subject, client, contact, category, description, internal
    response) and `Survey` (client, contact, related report, date, 1-5 ratings
    for overall/timeliness/quality/communication, comments). content/*.py, FTIs,
    types.xml, container in setuphandlers.
  - Shared workflow `senaite_customerrequest_workflow` for Complaint +
    SupportRequest: received -> process -> in_progress -> resolve -> resolved ->
    close -> closed, with reopen; transitions guarded by "Review portal content"
    (staff), customer only creates. Survey uses one_state_workflow. Bound in
    workflows.xml.
  - Control-panel register `CustomerCareView` listing all three types with
    Type/Subject/Client/Created/State columns and All/Open/Closed filters.
  - Bilingual (fa/en, RTL/LTR) `@@customer-care-status` dashboard: open vs closed
    complaint/support counts and average survey satisfaction scores + a live list
    of open complaints. Setup tile added.
  - Installer `@@install-customercare-module` (Manager-only) to register the FTIs
    + workflow and create the container in an existing ZODB.
  - Persian translations (73 msgids x fa/fa_IR) for all fields, vocabularies,
    listing, FTI titles and workflow state/transition titles.
- 2026-07-06: Installed and verified live. Created Complaint/Survey/SupportRequest
  via JSON API; complaint drove received -> process -> in_progress; dashboard
  showed complaints total/open, support total/open, survey responses; add form,
  view page (state badge "در حال بررسی") and dashboard all render Persian. Three
  demo records remain in the register (deletable from the UI).
- 2026-07-06: Built the public customer submission form `@@customer-feedback`
  (browser/customerfeedback, permission zope2.View, bilingual in-view labels).
  A customer picks complaint / support / survey, fills the form (JS toggles the
  complaint category+severity and the survey rating sections), and on submit the
  record is created in setup/customercare via `api.security.as_privileged_user()`
  + `api.create` (so a low-privilege / anonymous submitter can write), CSRF
  disabled for the POST via IDisableCSRFProtection. The customer gets the new id
  as a tracking number. Verified live: an ANONYMOUS POST created complaint-2 with
  title/description/client/category=result/severity=high, review_state=received,
  received_date auto-set to today; empty-subject POST is rejected without
  creating a record. So the full loop works now:
    * customer submits: /senaite/@@customer-feedback
    * staff sees: setup overview tile "Customer Care" (/senaite/setup/customercare)
      + dashboard @@customer-care-status
    * staff responds: open item -> Edit -> fill investigation/resolution (or
      support response) -> Save
    * staff closes: item toolbar state menu -> Process -> Resolve -> Close
- Still open / partial in Phase 6: (a) the form is public (no auth/anti-spam yet)
  and does not auto-link the record to the logged-in client's Client object - it
  stores a free-text client_name; wiring it to the authenticated contact's Client
  + adding a link from the client portal is a follow-up. (b) live re-verification
  of client data isolation with a real client login was inventoried by code, not
  exercised end-to-end this session.

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
- Create the 8 new Analysis Services confirmed in
  `docs/PHASE1_SERVICE_SCOPE_CROSSWALK.md` (open-cup D92 flash point,
  antifreeze pH/freezing point/relative density/water content, Ramsbottom
  carbon residue, chlorine, doctor test), then decide the last 3 open rows
  (Grease-4, Bitumen-1, Bitumen-2).
- Complete specification limits beyond the currently prepared 79 rows before
  enabling broad automated acceptance decisions.
- After those decisions, regenerate the import workbooks and create a fresh
  `senaite_data` backup before importing.
