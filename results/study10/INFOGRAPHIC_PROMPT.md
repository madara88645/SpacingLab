# Study 10 infographic generation prompt

## QA correction

The first generated image incorrectly showed four teal exposures and omitted one
32-step gap. Rejected after visual inspection. A targeted edit was requested:
exactly five teal circles at relative positions 0,32,64,128,256 with gap labels
32,32,64,128; keep all other typography and verified results unchanged.

Mode: built-in image generation, using the imagegen skill. No input images.
All data verified against six raw logs and the preregistered protocol before generation.
This prompt is a rendering specification, not an additional analysis.

Use case: infographic-diagram
Asset type: Turkish student-friendly SpacingLab research results infographic, one polished high-resolution landscape educational poster.
Primary request: explain a finished small-language-model experiment honestly. Crisp readable Turkish typography, light background, spacious hierarchy, restrained navy and teal for the two policies. Flat diagram style, no brain imagery or promotional claims. Four clearly separated sections, approximately 3:2 landscape canvas. Keep all text below verbatim, Turkish characters intact. No made-up numbers. Do not add significance stars, p-values, CI bars, decorative success medals or extra assertions.

Header:
"SpacingLab • Deney 10"
"Karışık aralıkların üstünlüğü doğrulanmadı."
"6 eğitim koşusu • 3 yeni karşılaştırma • GPT-2 • Yapay bilgiler"

Section 1 title: "Neyi değiştirdik?"
Two aligned horizontal timelines with EXACTLY FIVE dots each, first and last dots aligned vertically, total width identical. Label dots as the five exposures using small identical document icons or circles. Fixed timeline gap widths 1:1:1:1, labels between dots "64", "64", "64", "64"; row label "Sabit aralık".
Variable example timeline widths 0.5:0.5:1:2, labels "32", "32", "64", "128"; row label "Karışık aralık".
Under variable row: "Örnek sıra; her bilgi için karıştırıldı."
Below timelines: "İlk ve son gösterim aynı • 5 gösterim • Toplam 256 adım"
Small explanation: "Boşluklarda başka verilerle eğitim sürüyor."

Section 2 title: "Ana ölçüt: sonraki 7 sınavın ortalaması"
An exact simple table with four columns. No bars necessary because values are close.
Column headings: "Deneme", "Sabit", "Karışık", "Fark"
Rows:
"1 (seed 3)" | "%27,50" | "%26,57" | "−0,93 puan"
"2 (seed 4)" | "%27,50" | "%27,57" | "+0,07 puan"
"3 (seed 5)" | "%30,14" | "%34,43" | "+4,29 puan"
Footnote: "Fark = karışık − sabit"
Below table two modest equal-sized numeric callouts:
"Sabit: %28,38 ± 1,53 puan"
"Karışık: %29,52 ± 4,28 puan"
Then prominent conclusion but not celebratory:
"Ortalama fark: +1,14 puan"
"Farkın standart sapması: 2,77 puan"
"± ve standart sapma koşular arası değişimi gösterir; güven aralığı değildir."

Section 3 title: "Olumlu yan bulgu: NLL"
Explanation text: "NLL, doğru cevaba verilen olasılığı izler; düşük olması daha iyidir."
"Üç denemede de karışık aralık lehine."
"Fark: −0,093 ± 0,032 (standart sapma)"
"Bu yan bulgu, ana ölçütte kesin üstünlük sağlamaz."

Section 4 title: "Ne söyleyemiyoruz?"
"Başlangıçta öğrenilen miktarlar eşit değildi."
"Bu yüzden 'daha az unutuyor' sonucu çıkarılamaz."
"Tek küçük model; insan beyni, kişiselleştirme ve LoRA test edilmedi."
Footer: "Önceden belirlenen kural: sonuç belirsiz. Deney 9 ile birleştirilmedi."
Constraints: accurate five-dot timelines, faithful scale within timelines, signs and decimal commas exactly as supplied, large legible fonts, no dense prose wall, no truncated labels, no extra numbers, no implication of proof of equivalence. The word seed is only in the supplied row labels. No external sources or logos.
