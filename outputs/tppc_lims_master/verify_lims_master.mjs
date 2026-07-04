import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const outputDir = "D:/Git/lims_backend/outputs/tppc_lims_master";
const workbookPath = path.join(outputDir, "TPPC_LIMS_Master_Data.xlsx");
const blob = await FileBlob.load(workbookPath);
const workbook = await SpreadsheetFile.importXlsx(blob);

const overview = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 8000,
  tableMaxRows: 3,
  tableMaxCols: 8,
});
console.log(overview.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const sheets = [
  "Summary",
  "Instruments",
  "Sample Types",
  "Analysis Services",
  "Method References",
  "Specifications Missing",
  "Data Cleanup Needed",
];

for (const sheetName of sheets) {
  const preview = await workbook.render({
    sheetName,
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(
    path.join(outputDir, `${sheetName.replace(/[^A-Za-z0-9]+/g, "_")}_preview.png`),
    new Uint8Array(await preview.arrayBuffer()),
  );
}

console.log("verified", workbookPath);
