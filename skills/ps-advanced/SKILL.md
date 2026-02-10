---
name: ps-advanced
description: "Photoshop advanced techniques and reference: wind direction master table (drips down, flames up, streaks left/right with canvas rotation), filter parameter ranges, design principles (60-30-10 color rule, typography, composition, contrast/readability, platform dimensions), workflow templates (poster, photo edit, composite), advanced techniques (high-pass sharpen, dodge & burn, orton effect, blend-if, luminosity masking, stamp visible), 17 critical tool gotchas (verified bugs), failed attempts log (6 entries - DO NOT REPEAT), outer glow parameter reference, quality checklist."
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# §8 TOOL REFERENCE & WIND TABLE

## 8.1 WIND DIRECTION MASTER TABLE

Wind only blows horizontally. Use canvas rotation for vertical effects.
**Now uses dedicated tool: `apply_wind`**

| Desired Effect | Canvas Rotation | Wind Call                                           | Rotate Back | Result           |
| -------------- | --------------- | --------------------------------------------------- | ----------- | ---------------- |
| Drips DOWN     | -90 (CCW)       | `apply_wind(method="wind", direction="left")` x5-7  | +90 (CW)    | Streaks downward |
| Flames UP      | +90 (CW)        | `apply_wind(method="wind", direction="left")` x3-5  | -90 (CCW)   | Streaks upward   |
| Streaks RIGHT  | None            | `apply_wind(method="wind", direction="left")` x3-5  | None        | Horizontal right |
| Streaks LEFT   | None            | `apply_wind(method="wind", direction="right")` x3-5 | None        | Horizontal left  |

**"left" = FROM the left = pushes pixels RIGHT. "right" = FROM the right = pushes pixels LEFT.**

**Wind method comparison:**

- "wind" = controlled thin streaks — **USE THIS** for drip/fire effects
- "blast" = thick aggressive splatter — TOO MUCH for most effects
- "stagger" = randomized jagged streaks — good for lightning/electricity

## 8.2 FILTER PARAMETER RANGES

| Filter        | Parameter                       | Range                       | Default       |
| ------------- | ------------------------------- | --------------------------- | ------------- |
| Gaussian Blur | radius                          | 0.1-10000px                 | 2.5           |
| Motion Blur   | distance                        | 1-2000px                    | 30            |
| Radial Blur   | amount                          | 1-100                       | 10            |
| Surface Blur  | radius/threshold                | 1-100 / 2-255               | 5/15          |
| Lens Blur     | radius                          | 0-100                       | 15            |
| Noise         | amount                          | 0.1-400%                    | 5             |
| Wave          | generators/wavelength/amplitude | 1-999 / 1-999 / 1-999       | 5/10-120/5-35 |
| Unsharp Mask  | amount/radius/threshold         | 1-500% / 0.1-1000px / 0-255 | 100/1.0/0     |
| High Pass     | radius                          | 0.1-1000px                  | 10            |
| Wind          | method                          | wind/blast/stagger          | wind          |
| Liquify       | brush_size                      | 1-15000px                   | 64            |

---

# §9 DESIGN PRINCIPLES

## 9.1 COLOR RULES

**60-30-10 Rule:** 60% dominant, 30% secondary, 10% accent

## 9.2 TYPOGRAPHY RULES

- **Max 2 fonts** per design (3 absolute max)
- **Title: 2-3x body size** minimum
- **ALL CAPS: add tracking +50 to +200**
- **Never use Thin/Light below 24pt**

## 9.3 COMPOSITION

- Rule of Thirds: focal point at grid intersections
- Z-Pattern: Logo top-left → headline top → image bottom-left → CTA bottom-right

## 9.4 CONTRAST & READABILITY

- Body text: minimum 4.5:1 contrast ratio
- Text on images: 50-70% black overlay, or blur background
- Dark bg: off-white (224,225,221) not pure white

## 9.5 DIMENSIONS

| Platform             | Size      |
| -------------------- | --------- |
| Instagram Post       | 1080x1080 |
| Instagram Story/Reel | 1080x1920 |
| Twitter/X            | 1600x900  |
| YouTube Thumb        | 1280x720  |
| LinkedIn             | 1200x627  |
| A4 Print (300dpi)    | 2480x3508 |

---

# §10 WORKFLOW TEMPLATES

## 10.1 POSTER CREATION

```
1. Create canvas (correct dimensions + DPI)
2. Place background image
3. Color grade: curves + color_balance + vibrance
4. Cut out subject: select_subject → mask OR remove_background
5. Add main text → apply text effects (§5)
6. Add secondary text (subtitle, credits)
7. Final color harmony: unified color overlay SOFT_LIGHT 10-20%
8. Verify with get_document_image
9. Export: save_document_as
```

## 10.2 PHOTO EDIT

```
1. Open → duplicate background
2. auto_tone / auto_color OR manual curves+levels
3. Skin retouch: apply_spot_healing_brush or frequency separation (§6.12)
4. Color grade (§7)
5. Local adjustments: apply_dodge_tool / apply_burn_tool
6. Sharpen: apply_high_pass OVERLAY (§11.1)
7. Vignette (§6.8)
8. Optional apply_noise 2-3% OVERLAY
9. Export
```

## 10.3 COMPOSITE

```
1. Background plate
2. Subject (select_subject or remove_background)
3. Match lighting: harmonize_layer OR manual curves
4. Cast shadow: duplicate → flip vertical → blur → MULTIPLY 30-40%
5. Color unification: photo_filter or solid fill SOFT_LIGHT 10-15%
6. Final adjustments
```

---

# §11 ADVANCED TECHNIQUES

## 11.1 HIGH-PASS SHARPENING

`stamp_visible` → `apply_high_pass(radius=2-5)` → `set_layer_properties(blend_mode="OVERLAY")` → opacity 50-80%

## 11.2 DODGE & BURN (non-destructive)

`create_pixel_layer(fill_neutral=true, blend_mode="OVERLAY")` → paint WHITE to dodge, BLACK to burn, opacity 10-15% per stroke

## 11.3 ORTON EFFECT (dreamy glow)

`stamp_visible` → `apply_gaussian_blur(radius=20-40)` → SCREEN 40-60%

## 11.4 BLEND-IF COMPOSITING

`set_layer_blend_if` for seamless tone-based blending:

- Remove dark bg: this_layer_black=20, black_feather=50
- Show in bright areas: underlying_white=180, white_feather=220

## 11.5 LUMINOSITY MASKING

Load RGB as selection via batchplay → save as Highlights channel → invert for Shadows

## 11.6 STAMP VISIBLE

`stamp_visible` = flattened copy of all visible layers as new layer on top. Use BEFORE destructive effects.

---

# §12 CRITICAL TOOL GOTCHAS — 17 VERIFIED

These are verified bugs/behaviors that WILL cause failures if ignored:

1. **`select_layer` CAN DELETE LAYERS** — Use `set_layer_properties` or `execute_batchplay` to target layers instead
2. **`set_layer_properties` RESETS clipping mask** — Always pass `is_clipping_mask=false` (or true if clipped) to preserve state
3. **`place_image` always throws error** — But the layer IS created. **Ignore the error and continue.**
4. **`VIVID_LIGHT` blend mode is rejected** — MCP tool doesn't support it. Use batchplay.
5. **`scale_layer` fails silently on Smart Objects** — Use `free_transform` instead
6. **`generate_image`/`generative_fill` return success but produce nothing** — Adobe Firefly AI tools unreliable in MCP
7. **Canvas rotation affects ALL layers** — Every layer rotates. Plan accordingly.
8. **`apply_wind` only blows HORIZONTALLY** — Use canvas rotation for vertical effects (see §8.1)
9. **Filters require rasterized layers** — Text, shape, Smart Object layers will fail. Always rasterize first.
10. **`translate_layer` Y axis** — Positive Y moves DOWN (standard screen coords)
11. **SCREEN blend requires BLACK background** — White on transparent + SCREEN = invisible.
12. **Wind "blast" method is TOO aggressive** — Use "wind" method for controlled streaks.
13. **Global Light is shared** — Bevel and Drop Shadow share angle by default.
14. **File tokens required for file paths** — batchPlay won't trust raw file paths in some contexts.
15. **All modifying batchPlay in UXP needs executeAsModal** — Direct execution without modal wrapper will fail silently.
16. **Blur Gallery may force dialog** — Field/Iris/Tilt-Shift/Spin/Path blur may open dialog despite suppression.
17. **Camera Raw Filter NOT scriptable headless** — Always requires dialog. Use Curves + Levels + Color Balance instead.

---

# §13 FAILED ATTEMPTS LOG — DO NOT REPEAT

| #   | What Went Wrong                         | Correct Approach                        |
| --- | --------------------------------------- | --------------------------------------- |
| 1   | Wave distorted entire text horizontally | Use Wind (directional) not Wave         |
| 2   | Stretch 400% + blur + wave = sideways   | Wind + canvas rotation                  |
| 3   | Motion blur 90 = streams UP and DOWN    | Wind is one-directional (not symmetric) |
| 4   | Rotate +90 CW + Wind right = UP         | -90 CCW + Wind left = DOWN              |
| 5   | White on TRANSPARENT + SCREEN           | White on BLACK + SCREEN                 |
| 6   | Wind "blast" x10 = off-canvas           | "wind" method x 5-7                     |

---

# §14 OUTER GLOW PARAMETER REFERENCE

| Parameter | Range   | Default | Notes                                   |
| --------- | ------- | ------- | --------------------------------------- |
| BlendMode | any     | SCREEN  | SCREEN for glow, MULTIPLY for dark halo |
| Opacity   | 0-100%  | 75      |                                         |
| Noise     | 0-100%  | 0       | Adds texture to glow                    |
| Color     | RGB     | yellow  | Single color                            |
| Spread    | 0-100%  | 0       | Higher = more solid center              |
| Size      | 0-250px | 5       | Blur radius of glow                     |

---

# §15 QUALITY CHECKLIST

Before finalizing ANY design:

- [ ] Text is readable at target viewing distance
- [ ] Color palette has max 3-5 colors (60-30-10 rule)
- [ ] Visual hierarchy is clear (title → image → details)
- [ ] White space is sufficient
- [ ] All effects look intentional (not overdone)
- [ ] No artifacts from filter operations
- [ ] Layer order is logical (bg → subject → text → effects → adjustments)
- [ ] Canvas dimensions match target platform
- [ ] Verified with `get_document_image` or `get_layer_image`

---
