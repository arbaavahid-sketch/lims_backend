# Phase 1 Service Scope Crosswalk - Oil Lab PDF

Source PDF: `D:\Documents\SortedDocs\PDF\شرح خدمات آزمایشگاه روغن.pdf`

Generated on: 2026-07-06

## Summary

- PDF service rows reviewed: 61
- Covered: 35
- Review: 15
- Add/Review: 10
- Deferred/Review: 1

## Decision Rules

- `Covered`: a current Analysis Service appears to cover the row after normalizing method notation.
- `Review`: current data is close, but method, product scope, package grouping, or source typo needs a human decision.
- `Add/Review`: no sufficient current Analysis Service was found; add only if the lab confirms the service is active.
- `Deferred/Review`: source says future-capable or otherwise not ready for import.

## Crosswalk

| Group | PDF Row | PDF Test | PDF Method References | Decision | Candidate Current Services | Note |
| --- | ---: | --- | --- | --- | --- | --- |
| Grease | 1 | Grease corrosion | ASTM D 4048; INSO 11291 | Covered | AS_07910_111 - تشخیص خوردگی مس | Covered by the current copper/grease corrosion service. |
| Grease | 2 | Flash point on separated grease oil | ASTM D 92; INSO 198 | Review | AS_05147_149 - نقطه اشتعال | INSO 198 exists, but the current method set is mostly Pensky-Martens/ASTM D93. Confirm Cleveland open-cup D92 service. |
| Grease | 3 | Atmospheric distillation on separated grease oil | ASTM D 86; INSO 6261 | Covered | AS_68987_095 - اندازه‌گیری تقطیر در فشار اتمسفر<br>AS_38527_132 - تقطیر در فشار اتمسفر<br>AS_69862_133 - تقطیر در فشار اتمفسر | Covered by atmospheric distillation services. |
| Grease | 4 | Water content | ASTM D4048; INSO 11291 | Review | AS_07910_111 - تشخیص خوردگی مس | Source row likely has a method/title mismatch; ASTM D4048/INSO11291 are corrosion references, not water content. |
| Bitumen | 1 | Bitumen ductility | ASTM D 113; INSO 3866 | Add/Review | - | No direct service found. Add only if bitumen ductility is in active lab scope. |
| Bitumen | 2 | Bitumen specific gravity | ASTM D 70; INSO 3872 | Add/Review | - | No direct bitumen D70/INSO3872 service found. |
| Bitumen | 3 | Bitumen viscosity | ASTM D 445; INSO 340 | Review | AS_55967_083 - اندازه گیری گرانروی در دماى 100 درجه سانتیگراد<br>AS_33184_085 - اندازه گیری گرانروی و کینماتیک مایعات شفاف و تیره (و محاسبه گرانروی دینامیک)<br>AS_45235_086 - اندازه گیری گرانروی کینماتیک<br>AS_89052_106 - اندازه‌گیری گرانروی کینماتیک<br>... +5 more | Viscosity services exist; confirm product scope includes bitumen for this method. |
| Bitumen | 4 | Extraction solvent distillation | ASTM D 86 | Review | AS_68987_095 - اندازه‌گیری تقطیر در فشار اتمسفر<br>AS_38527_132 - تقطیر در فشار اتمسفر<br>AS_69862_133 - تقطیر در فشار اتمفسر | D86 exists; confirm this bitumen/extraction-solvent scope is intended. |
| Bitumen | 5 | Spot test | AASHTO T102-83; ISIRI 2949 | Covered | AS_74465_005 - آزمون لکه مواد قیری | Covered by existing bitumen spot-test service. |
| Antifreeze | 1 | Antifreeze pH | ASTM D 1287; INSO 1212 | Add/Review | - | No direct antifreeze pH service found. |
| Antifreeze | 2 | Freezing point | ASTM D 1177; INSO 1448 | Add/Review | - | No direct antifreeze freezing-point service found. |
| Antifreeze | 3 | Relative density | ASTM D 1122 | Deferred/Review | - | PDF marks this as future-capable; do not import unless active scope is confirmed. |
| Antifreeze | 4 | Water content | ASTM D 1123; ISIRI 6228 | Add/Review | - | No direct ASTM D1123/ISIRI6228 service found. |
| Antifreeze | 6 | Chloride | ASTM D 3634; ISIRI 5596 | Add/Review | - | Current chloride service uses ASTM E2469 for ethylene glycol; confirm whether D3634/ISIRI5596 is required. |
| Oil | 1 | Color | ASTM D 1500; INSO 203 | Covered | AS_79882_026 - اندازه گیری رنگ<br>AS_30884_120 - تعیین رنگ بر اساس مقیاس ASTM | Covered by color services. |
| Oil | 2 | Flash point open cup | ASTM D 92; INSO 198 | Review | AS_05147_149 - نقطه اشتعال | INSO 198 exists, but ASTM D92/open-cup should be verified separately from D93 closed-cup. |
| Oil | 3 | Pour point | ASTM D 97; INSO 201 | Covered | AS_24745_103 - اندازه‌گیری نقطه ریزش | Covered by pour-point services. |
| Oil | 4 | Viscosity | ASTM D 445; INSO 195 | Covered | AS_33184_085 - اندازه گیری گرانروی و کینماتیک مایعات شفاف و تیره (و محاسبه گرانروی دینامیک)<br>AS_62067_136 - شاخص گرانروی<br>AS_13550_145 - محاسبه شاخص گرانروی با استفاده از گرانروی سینماتیک در دمای 40 درجه و 100 درجه سانتیگراد<br>AS_55958_156 - گرانروی در 40 درجه سانتی گراد<br>... +1 more | Covered by viscosity and viscosity-index services. |
| Oil | 5 | Copper strip corrosion | ASTM D 130; ISIRI 336 | Covered | AS_59922_109 - تشخیص خوردگی تیغة مسی<br>AS_99532_110 - تشخیص خوردگی تیغه مسی<br>AS_07910_111 - تشخیص خوردگی مس<br>AS_80874_112 - تشخیض خوردگی تیغه مسی<br>... +2 more | Covered by copper-corrosion/sulfur method references, but ISIRI336 usage should be checked in final method mapping. |
| Oil | 6 | Total sulfur | ASTM D 4294; INSO 8402 | Covered | AS_94053_023 - اندازه گیری دانسیته و دانسیته نسبی مایعات به وسیله دانسیته متر دیجیتالی<br>AS_99314_088 - اندازه گیری گوگرد<br>AS_76235_123 - تعیین مقدار گوگرد به روش طیف سنجى فلورسانس یرتو ایکس با پاشندگى انرژی<br>AS_69402_124 - تعیین مقدار گوگرد به روش طیف سنجى فلورسانس یرتو ایکس با پاشندگى انرژی- (به غیر از بنزین)<br>... +2 more | Covered by XRF sulfur service. |
| Oil | 7 | Ash | ASTM D 482; INSO 2940 | Covered | AS_09521_020 - اندازه گیری خاکستر<br>AS_39409_059 - اندازه گیری مقدار خاکستر<br>AS_36104_064 - اندازه گیری میزان خاکستر<br>AS_49176_065 - اندازه گیری میزان خاکستر برحسب درصد وزنی | Covered by ash services. |
| Oil | 8 | TBN | ASTM D 2896; INSO 2772 | Covered | AS_13570_036 - اندازه گیری عدد قلیائى کل<br>AS_83735_037 - اندازه گیری عدد قلیایی - روش تیتراسیون<br>AS_44049_038 - اندازه گیری عدد قلیایی-روش پتانسیومتری پرکلریک<br>AS_58729_139 - عدد خنثی شدن کل | Covered by TBN service. |
| Oil | 9 | TAN | ASTM D 664; INSO 18030 | Covered | AS_99825_033 - اندازه گیری عدد اسیدی<br>AS_40113_034 - اندازه گیری عدد اسیدی -روش تیتراسیون پتانسیومتری<br>AS_86966_098 - اندازه‌گیری عدد خنثی سازی - روش تیتراسیون پتانسیومتری | Covered by TAN service. |
| Oil | 10 | Water by Karl Fischer | ASTM D 6304; INSO 18481 | Covered | AS_23337_008 - اندازه گیری آب از طریق تیتراسیون کارل فیشر(کولومتری)<br>AS_88113_055 - اندازه گیری مقدار آب<br>AS_43069_092 - اندازه‌گیری آب به روش کارل فیشر | ASTM D6304 services exist; confirm whether INSO18481 must be attached to the same service. |
| Oil | 11 | Elemental analysis, oil, 19 elements | ASTM D 6595 | Review | - | ICP element services exist, but ASTM D6595 as a single 19-element oil package is not explicit. |
| Oil | 12 | Water separability | ASTM D1401; INSO 3169 | Review | - | Current water-separability service uses ISO 6614. Confirm D1401/INSO3169 method mapping. |
| Oil | 13 | Ramsbottom carbon residue | ASTM D524; INSO 200 | Add/Review | - | No direct carbon-residue service found. |
| Oil | 14 | Corrosion at 135 C | ASTM D6594 | Covered | AS_80528_003 - آزمون خوردگی در دمای 135 درجه سانتی گراد | Covered by the current 135 C corrosion service. |
| Oil | 15 | Corrosion at 125 C | ASTM D5968 | Covered | AS_45859_002 - آزمون خوردگی در دمای 121 درجه سانتی گراد | Covered after notation cleanup; current source uses ASTM 5968 without D. |
| Hydrocarbon | 1 | Color | ASTM D1500-156; INSO 203; INSO 2932 | Covered | AS_79882_026 - اندازه گیری رنگ<br>AS_63324_027 - اندازه گیری رنگ سیبلت<br>AS_30884_120 - تعیین رنگ بر اساس مقیاس ASTM | Color services exist; confirm dual D1500/D156 notation if this is a combined row. |
| Hydrocarbon | 2 | Flash point closed cup | ASTM D 93; INSO 19695 | Covered | AS_79390_068 - اندازه گیری نقطه اشتعال با دستگاه سربسته پنسکى مارتنز<br>AS_96932_069 - اندازه گیری نقطه اشتعال با دستگاه سربسته پنسکی مارتنز<br>AS_81768_070 - اندازه گیری نقطه اشتعال به روش بسته با دستگاه مقیاس کوچک - روش الف<br>AS_58943_102 - اندازه‌گیری نقطه اشتعال با دستگاه سربسته پنسکی - مارتنز<br>... +1 more | Covered by closed-cup flash-point services. |
| Hydrocarbon | 3 | Flash point open cup | ASTM D 92; INSO 198 | Review | AS_05147_149 - نقطه اشتعال | Open-cup D92 should be verified separately from D93 closed-cup. |
| Hydrocarbon | 4 | Atmospheric distillation | ASTM D 86; INSO 6261 | Covered | AS_68987_095 - اندازه‌گیری تقطیر در فشار اتمسفر<br>AS_38527_132 - تقطیر در فشار اتمسفر<br>AS_69862_133 - تقطیر در فشار اتمفسر | Covered by D86 distillation services. |
| Hydrocarbon | 5 | Cloud point | ASTM D 2500; INSO 5438 | Covered | AS_71450_125 - تعیین مقدار گوگرد به روش طیف سنجی فلورسانس پرتو ایکس با پاشندگی انرژی<br>AS_53330_126 - تعیین نقطه ابری شدن | Covered by cloud-point service. |
| Hydrocarbon | 6 | Pour point | ASTM D 97; INSO 201 | Covered | AS_24745_103 - اندازه‌گیری نقطه ریزش | Covered by pour-point services. |
| Hydrocarbon | 7 | Viscosity | ASTM D 445; ISIRI 340 | Covered | AS_33184_085 - اندازه گیری گرانروی و کینماتیک مایعات شفاف و تیره (و محاسبه گرانروی دینامیک)<br>AS_55958_156 - گرانروی در 40 درجه سانتی گراد<br>AS_90904_159 - گرانروی کینماتیک در دمای 50 درجه سانتی گراد | Covered by viscosity services; normalize ISIRI/INSO 340 naming. |
| Hydrocarbon | 8 | Copper strip corrosion | ASTM D 130; ISIRI 336 | Covered | AS_59922_109 - تشخیص خوردگی تیغة مسی<br>AS_99532_110 - تشخیص خوردگی تیغه مسی<br>AS_07910_111 - تشخیص خوردگی مس<br>AS_80874_112 - تشخیض خوردگی تیغه مسی<br>... +2 more | Covered by copper-corrosion services. |
| Hydrocarbon | 9 | Total sulfur | ASTM D 4294; INSO 8402 | Covered | AS_94053_023 - اندازه گیری دانسیته و دانسیته نسبی مایعات به وسیله دانسیته متر دیجیتالی<br>AS_99314_088 - اندازه گیری گوگرد<br>AS_76235_123 - تعیین مقدار گوگرد به روش طیف سنجى فلورسانس یرتو ایکس با پاشندگى انرژی<br>AS_69402_124 - تعیین مقدار گوگرد به روش طیف سنجى فلورسانس یرتو ایکس با پاشندگى انرژی- (به غیر از بنزین)<br>... +2 more | Covered by XRF sulfur service. |
| Hydrocarbon | 10 | Mercaptan | ASTM D 3227; INSO 9379 | Covered | AS_98807_089 - اندازه گیری گوگرد (تیول مرکاپتان) - روش پتانسیومتری<br>AS_77015_090 - اندازه گیری گوگرد (تیول مرکاپتان) به روش پتانسیومتری<br>AS_71182_091 - اندازه گیری گوگرد (تیول مرکاپتان) حاصل از تقطیر و توربین های هواپیما به روش پتانسیومتری<br>AS_68870_131 - تعیین گوگرد (تیول مرکاپتان) - روش پتانسیومتری<br>... +1 more | Covered by mercaptan sulfur services. |
| Hydrocarbon | 11 | Hydrogen sulfide | ASTM D 3227; INSO 9379 | Review | AS_98807_089 - اندازه گیری گوگرد (تیول مرکاپتان) - روش پتانسیومتری<br>AS_77015_090 - اندازه گیری گوگرد (تیول مرکاپتان) به روش پتانسیومتری<br>AS_71182_091 - اندازه گیری گوگرد (تیول مرکاپتان) حاصل از تقطیر و توربین های هواپیما به روش پتانسیومتری<br>AS_68870_131 - تعیین گوگرد (تیول مرکاپتان) - روش پتانسیومتری<br>... +1 more | Method reference overlaps mercaptan; title is hydrogen sulfide. Confirm actual method/service. |
| Hydrocarbon | 12 | Chlorine | ISO 15597; ISIRI 13378 | Add/Review | - | No direct ISO15597/ISIRI13378 chlorine service found. |
| Hydrocarbon | 13 | Doctor test | ASTM D 4952; ISIRI 8722 | Add/Review | - | No direct doctor-test service found. |
| Hydrocarbon | 14 | Ash | ASTM D 482; INSO 2940 | Covered | AS_09521_020 - اندازه گیری خاکستر<br>AS_39409_059 - اندازه گیری مقدار خاکستر<br>AS_36104_064 - اندازه گیری میزان خاکستر<br>AS_49176_065 - اندازه گیری میزان خاکستر برحسب درصد وزنی | Covered by ash services. |
| Hydrocarbon | 15 | Water by distillation | ASTM D 95; ISIRI 8139; ISIRI 4081 | Covered | AS_02327_009 - اندازه گیری آب به روش تقطیر<br>AS_68987_095 - اندازه‌گیری تقطیر در فشار اتمسفر | Covered by water-distillation service. |
| Hydrocarbon | 16 | Water by Karl Fischer | ASTM D 1796; INSO 18481 | Review | - | Title says Karl Fischer, but ASTM D1796 is centrifuge-style water/sediment. Confirm/correct source row. |
| Hydrocarbon | 17 | Elemental analysis, oil, 19 elements | ASTM D 6595 | Review | - | ICP element services exist, but ASTM D6595 package is not explicit. |
| Hydrocarbon | 18 | GC benzene/aromatic/olefin | ASTM D 6730; ASTM D 5134; ASTM D 6729 | Review | AS_90066_113 - تعیین آروماتیک کل به روش کروماتوگرافی گازی<br>AS_10666_114 - تعیین اجزای منفرد در سوخت موتورهای احتراق جرقه ای به وسیله کروماتوگرافی گازی با تفکیک پذیری بالا و ستون مویین 100 متری (با پیش ستون)<br>AS_30166_115 - تعیین بنزن به روش کروماتوگرافی گازی<br>AS_74429_116 - تعیین ترکیبات هیدروکربنی در سوخت (بنزینی) به روش کروماتوگرافی گازی به صورت جزء به جزء | D6730 exists; D5134/D6729 are not explicit in current service references. |
| Hydrocarbon | 19 | PONA | ASTM D 1319-GC; ISIRI 8403 | Review | AS_71450_125 - تعیین مقدار گوگرد به روش طیف سنجی فلورسانس پرتو ایکس با پاشندگی انرژی | D1319 reference appears, but PONA/GC scope and ISIRI8403 should be confirmed. |
| Hydrocarbon | 20 | Sediment by extraction | ASTM D473; INSO 1210; ISIRI 4188 | Covered | AS_87712_025 - اندازه گیری رسوب به روش استخراج | ASTM D473 sediment service exists; INSO1210/ISIRI4188 need method-link review. |
| Crude Oil | 1 | Specific gravity at 15.6 C | ASTM A1298; INSO 197 | Review | AS_45240_077 - اندازه گیری چگالی<br>AS_45447_080 - اندازه گیری چگالی،چگالی نسبی یا گراویتی API با استفاده از روش هیدرومتر<br>AS_62644_155 - چگالی در 15 درجه سانتی گراد | Likely source typo for ASTM D1298; D1298/INSO197 service exists. |
| Crude Oil | 2 | API Gravity | ASTM D 1298; INZO 197 | Covered | AS_45240_077 - اندازه گیری چگالی<br>AS_45447_080 - اندازه گیری چگالی،چگالی نسبی یا گراویتی API با استفاده از روش هیدرومتر<br>AS_62644_155 - چگالی در 15 درجه سانتی گراد | Covered by D1298/INSO197 after correcting INZO typo to INSO. |
| Crude Oil | 3 | Total sulfur | ASTM D 4294; INSO 8402 | Covered | AS_94053_023 - اندازه گیری دانسیته و دانسیته نسبی مایعات به وسیله دانسیته متر دیجیتالی<br>AS_99314_088 - اندازه گیری گوگرد<br>AS_76235_123 - تعیین مقدار گوگرد به روش طیف سنجى فلورسانس یرتو ایکس با پاشندگى انرژی<br>AS_69402_124 - تعیین مقدار گوگرد به روش طیف سنجى فلورسانس یرتو ایکس با پاشندگى انرژی- (به غیر از بنزین)<br>... +2 more | Covered by XRF sulfur service. |
| Crude Oil | 4 | Mercaptan | ASTM D 3227; INSO 9379 | Covered | AS_98807_089 - اندازه گیری گوگرد (تیول مرکاپتان) - روش پتانسیومتری<br>AS_77015_090 - اندازه گیری گوگرد (تیول مرکاپتان) به روش پتانسیومتری<br>AS_71182_091 - اندازه گیری گوگرد (تیول مرکاپتان) حاصل از تقطیر و توربین های هواپیما به روش پتانسیومتری<br>AS_68870_131 - تعیین گوگرد (تیول مرکاپتان) - روش پتانسیومتری<br>... +1 more | Covered by mercaptan sulfur services. |
| Crude Oil | 5 | Water and sediment by centrifuge | ASTM D4007; INSO 15342 | Covered | AS_36513_011 - اندازه گیری آب و رسوبات به روش سانتریفیوژ | ASTM D4007 service exists; INSO15342 should be added/checked in method links. |
| Crude Oil | 6 | Water by distillation | ISO 9029; ISIRI 8139 | Review | AS_02327_009 - اندازه گیری آب به روش تقطیر | Water-distillation service exists via ASTM D95/ISIRI8139; ISO9029 is not explicit. |
| Crude Oil | 7 | Viscosity | ASTM D 445; ISIRI 340 | Covered | AS_33184_085 - اندازه گیری گرانروی و کینماتیک مایعات شفاف و تیره (و محاسبه گرانروی دینامیک)<br>AS_55958_156 - گرانروی در 40 درجه سانتی گراد<br>AS_90904_159 - گرانروی کینماتیک در دمای 50 درجه سانتی گراد | Covered by viscosity services; normalize ISIRI/INSO 340 naming. |
| Crude Oil | 8 | Pour point | ASTM D 97; INSO 201 | Covered | AS_24745_103 - اندازه‌گیری نقطه ریزش | Covered by pour-point services. |
| Crude Oil | 9 | Vapor pressure | ASTM D 323; INSO 5439 | Covered | AS_85250_047 - اندازه گیری فشار بخار (روش رید) | Covered by RVP/vapor-pressure service. |
| Crude Oil | 10 | Ramsbottom carbon residue | ASTM D5424; INSO 200 | Add/Review | - | No direct carbon-residue service found. Also confirm whether PDF meant ASTM D524. |
| Crude Oil | 11 | TAN | ASTM D 664; INSO 18030 | Covered | AS_99825_033 - اندازه گیری عدد اسیدی<br>AS_40113_034 - اندازه گیری عدد اسیدی -روش تیتراسیون پتانسیومتری<br>AS_86966_098 - اندازه‌گیری عدد خنثی سازی - روش تیتراسیون پتانسیومتری | Covered by TAN service. |
| Crude Oil | 12 | Atmospheric distillation | ASTM D 86; INSO 6261 | Covered | AS_68987_095 - اندازه‌گیری تقطیر در فشار اتمسفر<br>AS_38527_132 - تقطیر در فشار اتمسفر<br>AS_69862_133 - تقطیر در فشار اتمفسر | Covered by D86 distillation services. |

## Next Actions

1. Resolve all `Add/Review` rows with the lab technical owner.
2. Resolve `Review` rows by either normalizing method references, expanding product scope, or marking the PDF row as source-only evidence.
3. Do not import new Analysis Services until method document links and responsible instruments/people are known.

## Resolution Log

Decisions confirmed with the lab technical owner, row by row. Rows not yet
listed here are still open.

- 2026-07-06: Grease-2 (Flash point on separated grease oil, ASTM D92/INSO198,
  open cup). Confirmed the lab only has closed-cup Pensky-Martens (D93) via
  `AS_05147_149`. Decision: gap confirmed, open-cup D92 service does not exist.
  Action: add a new Analysis Service for Cleveland open-cup D92 if the lab
  wants to offer this test; otherwise mark the PDF row as not currently
  offered.
- 2026-07-06: Grease-4 (Water content, PDF cites D4048/INSO11291 which are
  corrosion references). Left open; owner will decide later whether this is a
  source typo needing a real water-content method or should be dropped.
- 2026-07-06: Bitumen-1 (Ductility, ASTM D113/INSO3866). Left open, owner will
  decide later.
- 2026-07-06: Bitumen-2 (Specific gravity, ASTM D70/INSO3872). Left open,
  owner will decide later.
- 2026-07-06: Bitumen-3 (Viscosity, ASTM D445/INSO340). Confirmed: existing
  viscosity services also cover bitumen. Decision: `Covered`, no new service
  needed; add bitumen to the documented product scope of the viscosity
  services.
- 2026-07-06: Bitumen-4 (Extraction solvent distillation, ASTM D86).
  Confirmed: existing D86 atmospheric distillation services are sufficient
  for this scope. Decision: `Covered`.
- 2026-07-06: Antifreeze-1 (pH, ASTM D1287/INSO1212). Confirmed the lab has a
  pH meter and takes this measurement. Decision: add a new Analysis Service
  for antifreeze pH (device: pH meter); not yet registered in SENAITE.
- 2026-07-06: Antifreeze-2 (Freezing point, ASTM D1177/INSO1448). Confirmed
  active capability. Decision: add a new Analysis Service.
- 2026-07-06: Antifreeze-3 (Relative density, ASTM D1122). PDF marked this
  future-capable/not ready, but owner confirmed it is now active. Decision:
  add a new Analysis Service (supersedes the PDF's Deferred marking).
- 2026-07-06: Antifreeze-4 (Water content, ASTM D1123/ISIRI6228). Confirmed
  active capability. Decision: add a new Analysis Service.
- 2026-07-06: Antifreeze-6 (Chloride, ASTM D3634/ISIRI5596). Confirmed the
  existing ASTM E2469 chloride service is sufficient. Decision: `Covered`.
- 2026-07-06: Oil-2 (Flash point open cup, ASTM D92). Same gap as Grease-2:
  lab only has closed-cup D93. Decision: add a new Analysis Service for
  open-cup D92 (can likely be the same new service as Grease-2/Hydrocarbon-3
  if product scope is shared).
- 2026-07-06: Oil-11 (Elemental analysis, 19 elements, ASTM D6595). Confirmed
  the existing ICP service is the same package. Decision: `Covered`.
- 2026-07-06: Oil-12 (Water separability, ASTM D1401/INSO3169). Confirmed
  ISO 6614 is the same test. Decision: `Covered`.
- 2026-07-06: Oil-13 (Ramsbottom carbon residue, ASTM D524/INSO200).
  Confirmed active capability. Decision: add a new Analysis Service.
- 2026-07-06: Hydrocarbon-3 (Flash point open cup, ASTM D92). Same confirmed
  gap as Grease-2/Oil-2: only closed-cup D93 exists. Decision: add a new
  Analysis Service for open-cup D92, shared across grease/oil/hydrocarbon
  product scope.
- 2026-07-06: Hydrocarbon-11 (Hydrogen sulfide, ASTM D3227/INSO9379).
  Confirmed the existing mercaptan sulfur service is the same service.
  Decision: `Covered`.
- 2026-07-06: Hydrocarbon-12 (Chlorine, ISO15597/ISIRI13378). Confirmed
  active capability. Decision: add a new Analysis Service.
- 2026-07-06: Hydrocarbon-13 (Doctor test, ASTM D4952/ISIRI8722). Confirmed
  active capability. Decision: add a new Analysis Service.
- 2026-07-06: Hydrocarbon-16 (Water, PDF cites ASTM D1796 but calls it Karl
  Fischer; D1796 is actually centrifuge water/sediment). Confirmed the lab
  really means Karl Fischer and has a dedicated Karl Fischer service (same
  family as Oil-10, ASTM D6304). Decision: `Covered` by the existing Karl
  Fischer service; the PDF's D1796 reference is a source error and should be
  corrected to D6304 in any documentation.
- 2026-07-06: Hydrocarbon-17 (Elemental analysis, 19 elements, ASTM D6595,
  duplicate of Oil-11). Confirmed the same ICP package is sufficient.
  Decision: `Covered`.
- 2026-07-06: Hydrocarbon-18 (GC benzene/aromatic/olefin, ASTM
  D6730/D5134/D6729). Confirmed the current GC services cover all three
  method references. Decision: `Covered`.
- 2026-07-06: Hydrocarbon-19 (PONA, ASTM D1319-GC/ISIRI8403). Confirmed the
  current GC service covers PONA. Decision: `Covered`.
- 2026-07-06: Crude Oil-1 (Specific gravity at 15.6 C, PDF cites "ASTM
  A1298"). Confirmed source typo for ASTM D1298; the existing D1298/INSO197
  service is sufficient. Decision: `Covered`.
- 2026-07-06: Crude Oil-6 (Water by distillation, ISO 9029/ISIRI8139).
  Confirmed the existing ASTM D95/ISIRI8139 service is sufficient. Decision:
  `Covered`.
- 2026-07-06: Crude Oil-10 (Ramsbottom carbon residue, ASTM D5424/INSO200,
  duplicate of Oil-13). Confirmed active capability. Decision: covered by the
  same new Analysis Service being added for Oil-13.

## Crosswalk Resolution Summary (2026-07-06)

All 26 open rows (15 Review, 10 Add/Review, 1 Deferred) have been discussed
with the lab technical owner, except three left open for a later session.

Resolved to `Covered` (no new service needed, only method-reference/product
scope cleanup where noted): Bitumen-3, Bitumen-4, Antifreeze-6, Oil-11,
Oil-12, Hydrocarbon-11, Hydrocarbon-16 (source method reference should be
corrected from D1796 to D6304), Hydrocarbon-17, Hydrocarbon-18,
Hydrocarbon-19, Crude Oil-1 (correct source typo A1298 to D1298), Crude
Oil-6.

Resolved to `Add` (new Analysis Service needed, not yet created in SENAITE):

- Open-cup flash point, ASTM D92 (shared scope: Grease-2, Oil-2,
  Hydrocarbon-3).
- Antifreeze pH, ASTM D1287/INSO1212 (device: pH meter).
- Antifreeze freezing point, ASTM D1177/INSO1448.
- Antifreeze relative density, ASTM D1122 (now active; supersedes the PDF's
  "future-capable"/Deferred marking).
- Antifreeze water content, ASTM D1123/ISIRI6228.
- Ramsbottom carbon residue, ASTM D524/D5424/INSO200 (shared scope: Oil-13,
  Crude Oil-10).
- Chlorine, ISO15597/ISIRI13378 (Hydrocarbon-12).
- Doctor test, ASTM D4952/ISIRI8722 (Hydrocarbon-13).

Still open, owner will decide later:

- Grease-4 (Water content; PDF method reference looks like a source typo).
- Bitumen-1 (Ductility, ASTM D113/INSO3866).
- Bitumen-2 (Specific gravity, ASTM D70/INSO3872).

Next step: create the 8 new Analysis Services listed above in the setup
workbook (or directly in SENAITE), including method, unit, department, and
instrument/device fields, then re-run the crosswalk check once the 3 open
rows are decided.
