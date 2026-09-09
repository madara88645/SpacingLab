# Exact correction prompt

Edit the supplied infographic with one precise correction only. Preserve every other panel, all text, numerical results, colours, fonts, spacing, and headings unchanged.
In panel 1, the teal "Karışık aralık" timeline currently incorrectly has FOUR document circles and THREE gap labels. Replace ONLY that teal timeline with EXACTLY FIVE document circles and FOUR separate labels.
The first and last circles must remain aligned with the navy row first and last circles. Positions across the same 482 pixel total span should be approximately x=207,267,327,448,689, all at y=402 in the original 1536x1024 image. These are cumulative positions 0,32,64,128,256. Thus the four widths are 60,60,121,241, ratio 1:1:2:4.
Place the four labels centered below each respective connecting segment, in this exact order:
"32" between circle1 and circle2,
"32" between circle2 and circle3,
"64" between circle3 and circle4,
"128" between circle4 and circle5.
Use slightly smaller teal circles if needed to avoid overlap, but make all five identical. The adjacent two 32 labels must BOTH appear. Do not remove or change any text below the timeline. Do not change any result values, ± signs, decimal commas, or any other element. This is a scientific correction: five exposures must be visually apparent.

## Final visual QA

Corrected output: exec-3d835874-82d2-4771-9a54-74dac01e9f9e.png, copied without
alteration to infographic-tr.png. Inspected the rendered image: both rows have
five markers; variable-gap labels are 32,32,64,128; first and last align. Main
table values, signs, means/SDs, NLL and limitations match verified source values.
Timeline geometry is schematic, not a precision scale: the numeric labels specify
the actual training-step gaps. No error bars or confidence intervals are drawn.
All other panels and text were preserved by the edit. The initial four-marker
draft was rejected and is not the project deliverable.
