import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const outputDir = "D:/Git/lims_backend/outputs/tppc_lims_master";
const inputPath = path.join(outputDir, "TPPC_LIMS_Master_Data.xlsx");
const outputPath = path.join(outputDir, "TPPC_LIMS_Master_Data_units_filled.xlsx");

function norm(value) {
  return String(value ?? "")
    .replace(/\u200c/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

function inferUnit(titleRaw, refsRaw) {
  const t = norm(titleRaw);
  const r = norm(refsRaw);
  const s = `${t} ${r}`;

  if (!t) return "TBD";
  if (/آماده سازی|آماده‌سازی|نمونه سازی|نمونه‌سازی/.test(s)) return "N/A";
  if (/نمونه برداری|نمونه‌برداری/.test(s)) return "N/A";
  if (/درصد عبور|عبور uv|uv/.test(s)) return "% transmittance";

  // Instrumental elemental analysis
  if (/icp|پلاسمای جفت شده|نشر اتمی|آلومینیوم|استرانسیم|باریم|اندازه گیری بور|اندازه‌گیری بور|تیتانیوم|کلسیم|منیزیم|سدیم|پتاسیم|روی|فسفر|سیلیسیم|آهن|مس|نیکل|وانادیم|کروم|سرب|قلع|مولیبدن|منگنز|جیوه|فلز/.test(s)) {
    if (/جیوه/.test(s)) return "mg/kg";
    return "mg/kg";
  }

  // Water and sediments
  if (/کارل فیشر|کلومتری|کولومتری|تیتراسیون.*آب/.test(s)) return "mg/kg";
  if (/آب و رسوب|آب و رسوبات|سانتریفیوژ/.test(s)) return "% vol";
  if (/آب به روش تقطیر|دین استارک|دین استارک|دین.+استارک/.test(s)) return "% vol";
  if (/اندازه گیری آب|اندازه گیری اب|مقدار آب/.test(s)) return "mg/kg";

  // Acidity/basicity
  if (/عدد اسیدی|عدد اسيدی|عدد اسيدى|عدد اسیدى|اسید کل|اسیدیته|عدد خنثی|خنثی سازی|خنثی شدن/.test(s)) return "mg KOH/g";
  if (/عدد قلیایی|عدد قلیائ|قلیایی|قلیائى/.test(s)) return "mg KOH/g";
  if (/اسید آزاد/.test(s)) return "% mass";

  // Common petroleum physical properties
  if (/گرانروی|گرانروى|ویسکوزیته|لزجت/.test(s)) {
    if (/شاخص/.test(s)) return "Index";
    return "mm2/s";
  }
  if (/چگالی نسبی|گراویتی api|api/.test(s)) return "API gravity";
  if (/چگالی|دانسیته|جرم حجمی/.test(s)) return "kg/m3";
  if (/نقطه اشتعال|اشتعال|flash/.test(s)) return "°C";
  if (/نقطه جوش|جوش/.test(s)) return "°C";
  if (/نقطه ریزش|ریزش|pour/.test(s)) return "°C";
  if (/نقطه ابری|ابری|cloud/.test(s)) return "°C";
  if (/نقطه انجماد|انجماد|freeze/.test(s)) return "°C";
  if (/نقطه نرمی|نرم شدن/.test(s)) return "°C";
  if (/تقطیر|بازیافت|تبخیر|درصد تبخیر/.test(s)) return "°C / % vol";
  if (/فشار بخار|بخار.*رید|rvp/.test(s)) return "kPa";

  // Composition/concentration
  if (/گوگرد|سولفور|مرکاپتان|تیول/.test(s)) return "mg/kg";
  if (/خاکستر سولفاته|خاکستر/.test(s)) return "% mass";
  if (/کربن باقی مانده|کربن باقیمانده|کک|باقی مانده کربن/.test(s)) return "% mass";
  if (/نمک/.test(s)) return "mg/L";
  if (/کلر|کلرید/.test(s)) return "mg/kg";
  if (/رسوب|ناخالصی|مواد جامد|ذرات/.test(s)) return "% mass";
  if (/آروماتیک|بنزن|تولوئن|زایلن|اولفین|اشباع|پارافین|نفتن|ترکیبات/.test(s)) return "% vol";

  // Ratings and visual/classification tests
  if (/خوردگی|corrosion/.test(s)) return "Rating / Class";
  if (/رنگ سیبلت|رنگ astm|اندازه گیری رنگ|رنگ/.test(s)) return "Color scale";
  if (/لکه|ظاهر|شفافیت|کدورت ظاهری|مشاهده/.test(s)) return "Rating / Visual";
  if (/بو/.test(s)) return "Rating / Sensory";
  if (/کراکل|crackle/.test(s)) return "Pass / Fail";
  if (/ft-ir|مادون قرمز|فروسرخ|infrared/.test(s)) return "Absorbance / Spectrum";

  // Water lab
  if (/ph|پی اچ|اسیدیته آب/.test(s)) return "pH";
  if (/هدایت|رسانایی|conductivity/.test(s)) return "µS/cm";
  if (/کدورت|turbidity/.test(s)) return "NTU";
  if (/سختی/.test(s)) return "mg/L as CaCO3";
  if (/قلیائیت/.test(s)) return "mg/L as CaCO3";
  if (/cod|اکسیژن خواهی شیمیایی/.test(s)) return "mg/L";
  if (/bod|اکسیژن خواهی زیستی/.test(s)) return "mg/L";

  // Performance/derived values
  if (/عدد اکتان|اکتان/.test(s)) return "Octane Number";
  if (/عدد ستان|ستان/.test(s)) return "Cetane Number";
  if (/شاخص گرانروی/.test(s)) return "Index";
  if (/گرمای احتراق|ارزش حرارتی|حرارت احتراق/.test(s)) return "MJ/kg";
  if (/توزیع کربن|n-d-m|ndm|گروه ساختاری/.test(s)) return "% mass";
  if (/مواد نامحلول|نامحلول در پنتان|پنتان/.test(s)) return "% mass";
  if (/اندازه گیری روغن|مقدار روغن|oil content/.test(s)) return "% mass";
  if (/قابلیت جدا شدن آب|جدا شدن آب|demulsibility/.test(s)) return "min";
  if (/پایداری اکسیداسیون|اکسیداسیون/.test(s)) return "h";
  if (/نفوذپذیری|درجه نفوذ|penetration/.test(s)) return "0.1 mm";
  if (/کف|تمایل به کف/.test(s)) return "mL";
  if (/فرسایش|سایش|wear/.test(s)) return "mm";
  if (/فیلتراسیون|قابلیت فیلتر/.test(s)) return "mL";

  // Generic dimensions
  if (/دما|دمای/.test(s)) return "°C";
  if (/زمان/.test(s)) return "min";
  if (/درصد|مقدار|غلظت/.test(s)) return "% mass";

  return "TBD";
}

const blob = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(blob);
const sheet = workbook.worksheets.getItem("Analysis Services");
const used = sheet.getUsedRange();
const values = used.values;

const headerRowIndex = values.findIndex((row) => row.includes("Analysis Title FA"));
if (headerRowIndex < 0) throw new Error("Could not find Analysis Services header row");
const headers = values[headerRowIndex];
const titleCol = headers.indexOf("Analysis Title FA");
const unitCol = headers.indexOf("Unit");
const refsCol = headers.indexOf("Method References");
if (titleCol < 0 || unitCol < 0) throw new Error("Required columns not found");

const units = [];
let filled = 0;
let tbd = 0;
for (let r = headerRowIndex + 1; r < values.length; r++) {
  const title = values[r][titleCol];
  if (!title) {
    units.push([""]);
    continue;
  }
  const unit = inferUnit(title, refsCol >= 0 ? values[r][refsCol] : "");
  if (unit === "TBD") tbd += 1;
  filled += 1;
  units.push([unit]);
}

const startRow = headerRowIndex + 2; // 1-based Excel row number for first data row
const endRow = startRow + units.length - 1;
sheet.getRange(`C${startRow}:C${endRow}`).values = units;

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "Analysis Services",
  range: "A1:L30",
  scale: 1,
  format: "png",
});
await fs.writeFile(path.join(outputDir, "Analysis_Services_units_preview.png"), new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(JSON.stringify({ outputPath, filled, tbd }, null, 2));
