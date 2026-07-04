import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = "D:/Git/lims_backend/outputs/tppc_lims_master";
const data = JSON.parse(await fs.readFile(path.join(outputDir, "lims_master_data.json"), "utf8"));

const workbook = Workbook.create();

const colors = {
  navy: "#12355B",
  teal: "#0F766E",
  lightTeal: "#DDF7F2",
  amber: "#FEF3C7",
  red: "#FEE2E2",
  gray: "#F3F4F6",
  border: "#CBD5E1",
  white: "#FFFFFF",
};

function colName(n) {
  let s = "";
  while (n > 0) {
    const m = (n - 1) % 26;
    s = String.fromCharCode(65 + m) + s;
    n = Math.floor((n - 1) / 26);
  }
  return s;
}

function addTableSheet(name, title, headers, rows, tableName, options = {}) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  const cols = headers.length;
  const lastCol = colName(cols);
  sheet.getRange(`A1:${lastCol}1`).merge();
  sheet.getRange("A1").values = [[title]];
  sheet.getRange("A1").format = {
    fill: options.titleFill || colors.navy,
    font: { bold: true, color: colors.white, size: 14 },
  };
  sheet.getRange("A2").values = [[options.note || ""]];
  sheet.getRange(`A2:${lastCol}2`).merge();
  sheet.getRange("A2").format = {
    fill: options.noteFill || colors.gray,
    font: { color: "#374151", italic: true },
    wrapText: true,
  };
  const matrix = [headers, ...rows];
  const range = sheet.getRangeByIndexes(3, 0, matrix.length, cols);
  range.values = matrix;
  const headerRange = sheet.getRangeByIndexes(3, 0, 1, cols);
  headerRange.format = {
    fill: options.headerFill || colors.teal,
    font: { bold: true, color: colors.white },
    wrapText: true,
  };
  sheet.getRangeByIndexes(4, 0, Math.max(rows.length, 1), cols).format = {
    borders: { preset: "inside", style: "thin", color: colors.border },
    wrapText: true,
  };
  sheet.getRangeByIndexes(3, 0, matrix.length, cols).format.borders = {
    preset: "outside",
    style: "thin",
    color: colors.border,
  };
  const tableRange = `A4:${lastCol}${matrix.length + 3}`;
  const table = sheet.tables.add(tableRange, true, tableName);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  sheet.freezePanes.freezeRows(4);
  range.format.autofitColumns();
  range.format.autofitRows();
  // Keep long text usable without making the workbook sprawl endlessly.
  const widthCaps = options.widthCaps || {};
  for (let c = 1; c <= cols; c++) {
    const letter = colName(c);
    const width = widthCaps[headers[c - 1]] || 24;
    sheet.getRange(`${letter}:${letter}`).format.columnWidth = width;
  }
  return sheet;
}

const summary = workbook.worksheets.add("Summary");
summary.showGridLines = false;
summary.getRange("A1:H1").merge();
summary.getRange("A1").values = [["TPPC LIMS Master Data"]];
summary.getRange("A1").format = {
  fill: colors.navy,
  font: { bold: true, color: colors.white, size: 16 },
};
summary.getRange("A2:H2").merge();
summary.getRange("A2").values = [["Prepared from TPPC equipment and registered scope workbooks for SENAITE setup."]];
summary.getRange("A2").format = { fill: colors.gray, font: { italic: true, color: "#374151" } };

summary.getRange("A4:B10").values = [
  ["Metric", "Value"],
  ["Equipment rows", data.summary.equipment_rows],
  ["Registered scope rows", data.summary.domain_rows],
  ["Sample types / products", data.summary.sample_types],
  ["Unique analysis services", data.summary.analysis_services],
  ["Unique references", data.summary.references],
  ["Specification rows needing limits", data.summary.spec_missing],
];
summary.getRange("A4:B4").format = { fill: colors.teal, font: { bold: true, color: colors.white } };
summary.getRange("A4:B10").format.borders = { preset: "all", style: "thin", color: colors.border };
summary.getRange("A12:H12").merge();
summary.getRange("A12").values = [["Recommended workflow"]];
summary.getRange("A12").format = { fill: colors.lightTeal, font: { bold: true, color: "#064E3B" } };
summary.getRange("A13:H19").values = [
  ["1", "Review Instruments and fill serial number, calibration, location, and responsible person.", "", "", "", "", "", ""],
  ["2", "Review Sample Types and merge product names that are duplicates or too granular.", "", "", "", "", "", ""],
  ["3", "Review Analysis Services and fill unit, department, instrument, turnaround, and final keyword.", "", "", "", "", "", ""],
  ["4", "Use Method References as the traceable source table for standards and clauses.", "", "", "", "", "", ""],
  ["5", "Complete Specifications Missing before using automated pass/fail decisions in SENAITE.", "", "", "", "", "", ""],
  ["6", "Keep NOTICE and GPL attribution in the repo because this remains an internal SENAITE derivative.", "", "", "", "", "", ""],
  ["7", "After review, use these sheets as import/preparation tables for SENAITE setup.", "", "", "", "", "", ""],
];
summary.getRange("A13:A19").format = { fill: colors.navy, font: { bold: true, color: colors.white } };
summary.getRange("B13:H19").format = { fill: colors.gray, wrapText: true };
summary.getRange("A13:H19").format.borders = { preset: "all", style: "thin", color: colors.border };
summary.getRange("A21:B23").values = [
  ["Source file", data.summary.source_files[0]],
  ["Source file", data.summary.source_files[1]],
  ["Generated", new Date().toISOString().slice(0, 10)],
];
summary.getRange("A21:A23").format = { fill: colors.teal, font: { bold: true, color: colors.white } };
summary.getRange("B21:B23").format = { fill: colors.gray };
summary.getRange("A:B").format.columnWidth = 28;
summary.getRange("B:H").format.columnWidth = 22;
summary.freezePanes.freezeRows(4);

addTableSheet(
  "Instruments",
  "Instruments / Equipment",
  data.instruments.headers,
  data.instruments.rows,
  "InstrumentsTable",
  {
    note: "Fill the blank operational columns before production: serial number, calibration, location, and owner.",
    widthCaps: {
      "Instrument Code": 18,
      "Name FA": 24,
      "Name EN": 28,
      "Manufacturer / Country": 24,
      "Application Area": 28,
      "Notes": 30,
    },
  },
);

addTableSheet(
  "Sample Types",
  "Sample Types / Products",
  data.sample_types.headers,
  data.sample_types.rows,
  "SampleTypesTable",
  {
    note: "Review product names before importing; some product categories may need merging or hierarchy.",
    widthCaps: {
      "Sample Type Code": 20,
      "Sample Type / Product": 36,
      "Notes": 34,
    },
  },
);

addTableSheet(
  "Analysis Services",
  "Analysis Services / Tests",
  data.analysis_services.headers,
  data.analysis_services.rows,
  "AnalysisServicesTable",
  {
    note: "Fill Unit, Department, Instrument Code, turnaround, and final keywords before import.",
    widthCaps: {
      "Analysis Keyword": 20,
      "Analysis Title FA": 52,
      "Method References": 56,
      "Example Products": 48,
      "Notes": 34,
    },
  },
);

addTableSheet(
  "Method References",
  "Method References / Registered Scope Rows",
  data.method_references.headers,
  data.method_references.rows,
  "MethodReferencesTable",
  {
    note: "Traceability table from the registered scope workbook. It preserves row-level product, test, standard, year, and clause.",
    widthCaps: {
      "Product": 34,
      "Analysis Title FA": 52,
      "Reference Name": 22,
      "Reference Clause": 18,
    },
  },
);

addTableSheet(
  "Specifications Missing",
  "Specifications Needing Limits",
  data.spec_missing.headers,
  data.spec_missing.rows,
  "SpecificationsMissingTable",
  {
    note: "These rows need min/max/unit or acceptance text before SENAITE can make reliable pass/fail decisions.",
    titleFill: "#7C2D12",
    headerFill: "#B45309",
    noteFill: colors.amber,
    widthCaps: {
      "Product": 34,
      "Analysis Title FA": 52,
      "Acceptance Text": 34,
      "Reason": 30,
    },
  },
);

addTableSheet(
  "Data Cleanup Needed",
  "Data Cleanup Needed",
  data.cleanup.headers,
  data.cleanup.rows,
  "DataCleanupTable",
  {
    note: "Review these issues before production import.",
    titleFill: "#7F1D1D",
    headerFill: "#991B1B",
    noteFill: colors.red,
    widthCaps: {
      "Issue Type": 28,
      "Item": 26,
      "Details": 54,
      "Recommended Action": 42,
    },
  },
);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "Summary",
  autoCrop: "all",
  scale: 1,
  format: "png",
});
await fs.writeFile(path.join(outputDir, "summary_preview.png"), new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outputDir, "TPPC_LIMS_Master_Data.xlsx"));
console.log(path.join(outputDir, "TPPC_LIMS_Master_Data.xlsx"));
