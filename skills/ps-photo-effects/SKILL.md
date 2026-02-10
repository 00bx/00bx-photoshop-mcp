---
name: ps-photo-effects
description: "Photoshop background and photo effect recipes: bokeh background, gradient mesh, light leak/flare, cyberpunk/synthwave grading, retro/vintage grading with faded blacks, duotone, double exposure, vignette, color pop, HDR effect, miniature/tilt-shift, skin retouching/frequency separation, day to night. Plus color grading recipes: teal & orange cinematic, Japanese anime style, moody blue, warm vintage."
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# §6 BACKGROUND & PHOTO EFFECTS — 13 Recipes

## 6.1 BOKEH BACKGROUND

Soft brush dabs (800-1200px, opacity 15-30%, hardness 0) → `apply_gaussian_blur(radius=8-15)` → duplicate at 70% scale for depth

## 6.2 GRADIENT MESH BACKGROUND

3-5 pixel layers, each with single soft brush dab of different color → `apply_gaussian_blur(radius=200-350)` each → stack at 70-90% opacity

## 6.3 LIGHT LEAK / FLARE

Soft brush warm colors → `apply_gaussian_blur(radius=80-120)` → SCREEN 50-70%

## 6.4 CYBERPUNK / SYNTHWAVE GRADING

- Color balance: shadows → blue [0,0,50], highlights → pink [30,-10,-20]
- Levels: output_shadow=15
- Vibrance +30

## 6.5 RETRO / VINTAGE GRADING (faded blacks)

1. Curves composite: [{0,30},{255,240}] — raised blacks + capped whites
2. Curves red: [{0,12},{255,255}]
3. Curves blue: [{0,35},{255,220}]
4. Hue/Sat: saturation -25
5. Photo filter: warm (236,138,0) density 22
6. `apply_noise(amount=4, monochromatic=true)` → OVERLAY 35%

## 6.6 DUOTONE

`add_gradient_map_adjustment_layer` with 2 stops
**Combos:** Midnight Blue→Gold, Deep Purple→Pink, Dark Teal→Orange, Black→Cyan

## 6.7 DOUBLE EXPOSURE

Portrait + landscape → SCREEN 70-85% → mask to reveal face details

## 6.8 VIGNETTE

Method 1: `lens_correction(vignette=-80, vignette_midpoint=40)`
Method 2: ellipse select → invert → fill black → reduce opacity 40-60%

## 6.9 COLOR POP

Hue/sat -100 on top → paint black on mask over colored object

## 6.10 HDR EFFECT

S-curve + `apply_high_pass` OVERLAY 50% + vibrance +30 + `shadows_highlights(shadow_amount=50, highlight_amount=30)`

## 6.11 MINIATURE / TILT-SHIFT

Use `apply_tilt_shift_blur` tool directly, or: duplicate → `apply_gaussian_blur(radius=15-25)` → reflected gradient mask

## 6.12 SKIN RETOUCHING (frequency separation)

**Low freq:** Duplicate → `apply_gaussian_blur(radius=6-10)`
**High freq:** Duplicate original → `apply_high_pass(radius=6-10)` → LINEAR_LIGHT
Or use `apply_image_composite` tool for precise separation

## 6.13 DAY TO NIGHT

Curves pull highlights down → blue color balance → desat -30 → paint warm lights on SCREEN layer

---

# §7 COLOR GRADING RECIPES

## 7.1 TEAL & ORANGE (cinematic)

**Red channel curves:** input 60→output 45, input 190→output 210
**Green channel curves:** input 75→output 70, input 180→output 185
**Blue channel curves:** input 50→output 75, input 200→output 175

## 7.2 JAPANESE ANIME STYLE

1. S-curve on composite for contrast
2. Blue shadows: +10 via color balance
3. Selective Color → Reds: saturation +15, lightness +5
4. Selective Color → Cyans: saturation +20
5. Vibrance +20, saturation +5

## 7.3 MOODY BLUE

Blue shadows +40, desaturate -20, lower highlights via curves

## 7.4 WARM VINTAGE

Raise black point to 20, warm photo filter, desat -15

---
