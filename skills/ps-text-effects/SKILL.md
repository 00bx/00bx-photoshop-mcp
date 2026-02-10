---
name: ps-text-effects
description: "19 verified Photoshop text effect recipes with exact parameters: liquid drip/melting, chrome/metallic, neon glow, glass/frosted, fire/flame, ice/frozen, gold/luxury, holographic/iridescent, glitch, emboss/letterpress, outline/stroke, 3D extrude, watercolor, smoke, retro/vintage, gradient fill, lava/molten, liquid gaussian+wave+liquify, liquid bevel+emboss stacking. Includes wind direction logic, MCP tool chains, and common mistakes."
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# §5 TEXT EFFECTS — 19 Verified Recipes

## 5.1 LIQUID DRIP / MELTING TEXT

**Result:** Flowing tendrils/streams dripping DOWNWARD from text bottom

**CRITICAL DIRECTION LOGIC (verified by testing):**

```
CORRECT: Rotate -90 CCW → apply_wind("left") x 5-7 → Rotate +90 CW back = DRIPS DOWN
WRONG:   Rotate +90 CW  → apply_wind("right") x 5 → Rotate -90 CCW back = DRIPS UP
```

**Why:** Rotate -90 CCW → text bottom faces RIGHT → Wind "from left" pushes pixels RIGHT (toward bottom) → Rotate +90 CW back → RIGHT streaks become DOWNWARD

**CRITICAL: White text on BLACK background (not transparent) — SCREEN blend removes black**

**MCP Tool Chain:**

```
1. duplicate_layer (preserve original text)
2. rasterize_layer
3. Create BLACK pixel layer → merge with text (white on black)
4. scale_layer 300% height from TOPCENTER (elongate before wind)
5. rotate_canvas(angle=-90)
6. apply_wind(method="wind", direction="left") x 5-7 times
7. rotate_canvas(angle=90)
8. apply_gaussian_blur(radius=2-3)
9. set_layer_properties(blend_mode="SCREEN", layer_opacity=90)
10. add_gradient_map_adjustment_layer (clipped — colorize)
11. add_outer_glow_layer_style (neon color glow)
12. add_layer_mask + fill_mask_with_gradient (hide top, show bottom)
```

**Common Mistakes:**

- Rotating CW (+90) first → drips go UP
- Wind "from right" after CW rotation → drips go UP
- Using "blast" method → too messy/aggressive, layer goes off-canvas
- White on TRANSPARENT + SCREEN → colors invisible
- Wave amplitude too high (>40) → text destroyed

---

## 5.2 CHROME / METALLIC TEXT

**Gradient Overlay:** reflected, angle: 90

- stops: {0: (26,26,26)}, {25: (216,216,216)}, {50: (26,26,26)}, {75: (250,250,250)}, {100: (26,26,26)}

**Bevel & Emboss:** innerBevel, chiselHard, depth: 300, size: 5, angle: 120, altitude: 30

- highlight: SCREEN white 90%, shadow: MULTIPLY black 75%

---

## 5.3 NEON GLOW TEXT

**Neon Color Palette:**
| Color | RGB |
|-------|-----|
| Pink | (255, 17, 119) |
| Blue | (0, 212, 255) |
| Green | (57, 255, 20) |
| Red | (255, 7, 58) |
| Yellow | (255, 229, 0) |
| Cyan | (5, 217, 255) |
| Purple | (204, 0, 255) |

**Layer Styles on text:**

1. `add_inner_glow_layer_style(blend_mode="NORMAL", opacity=100, color=NEON_COLOR, source="center", choke=0, size=8)`
2. `add_outer_glow_layer_style(blend_mode="SCREEN", opacity=100, color=NEON_COLOR, spread=0, size=20)`
3. `add_drop_shadow_layer_style(blend_mode="SCREEN", color=NEON_COLOR, opacity=100, distance=0, spread=0, size=60)`
   - drop shadow with SCREEN + distance=0 = wide ambient glow

**Multi-Layer Glow Stacking (for INTENSE glow):**

1. Duplicate text → fill_opacity=0, layer_opacity=20% → Gaussian Blur 15px → SCREEN
2. Duplicate again → Gaussian Blur 40px → SCREEN 50%
3. Duplicate again → Gaussian Blur 80px → SCREEN 30%
4. Result: 4 layers creating photorealistic multi-radius glow

---

## 5.4 GLASS / FROSTED TEXT

**Key:** `set_layer_properties(fill_opacity=0)` — NOT layer opacity

1. `add_bevel_emboss_layer_style(style="innerBevel", technique="smooth", depth=150, size=10, soften=2, angle=120, altitude=30, highlight_mode="SCREEN", highlight_opacity=85, shadow_mode="MULTIPLY", shadow_opacity=50)`
2. `add_inner_shadow_layer_style(blend_mode="MULTIPLY", opacity=30, angle=120, distance=3, choke=0, size=5)`
3. `add_inner_glow_layer_style(blend_mode="SCREEN", color={255,255,255}, opacity=30, source="edge", choke=0, size=8)`
4. `add_stroke_layer_style(size=1, position="INSIDE", blend_mode="SCREEN", color={255,255,255}, opacity=50)`

---

## 5.5 FIRE / FLAME TEXT

**Same Wind technique as drip but OPPOSITE direction:**

```
Rotate +90 CW → apply_wind("left") x 3-5 → Rotate -90 CCW back = FLAMES UP
```

**Steps:**

1. White text on black background → rasterize → merge to single layer
2. `rotate_canvas(angle=90)` → CW
3. `apply_wind(method="wind", direction="left")` x 3-5
4. `rotate_canvas(angle=-90)` → back
5. `apply_gaussian_blur(radius=1.5)`
6. Optional: `apply_ripple(amount=110, size="medium")` for flicker
7. Gradient Map fire colors:
   - {0: (0,0,0)}, {30: (255,0,0)}, {55: (255,102,0)}, {80: (255,204,0)}, {100: (255,255,255)}

---

## 5.6 ICE / FROZEN TEXT

**Text color:** RGB (168, 216, 234)

1. `add_bevel_emboss_layer_style(style="innerBevel", technique="chiselHard", depth=250, size=5, angle=120, altitude=30, highlight_mode="SCREEN", highlight_opacity=90, shadow_mode="MULTIPLY", shadow_color={26,58,92}, shadow_opacity=70)`
2. `add_inner_glow_layer_style(blend_mode="SCREEN", color={200,232,255}, opacity=50, source="edge", size=12)`
3. `add_satin_layer_style(blend_mode="SCREEN", color={200,232,255}, opacity=30, angle=19, distance=11, size=14, invert=true)`

**Frost texture:** Duplicate → rasterize → `apply_crystallize(cell_size=5)` → OVERLAY 40% → `apply_noise(5)`

---

## 5.7 GOLD / LUXURY TEXT

**Gold Gradient Stops:**

- {0: (191,149,63)}, {25: (252,246,186)}, {50: (179,135,40)}, {75: (251,245,183)}, {100: (170,119,28)}

1. `add_gradient_overlay_layer_style` with gold stops, angle: 90, type: "linear"
2. `add_bevel_emboss_layer_style(style="innerBevel", technique="smooth", depth=200, size=3, highlight_color={252,246,186}, shadow_color={92,58,10})`
3. `add_stroke_layer_style(size=2, position="OUTSIDE")` with same gold gradient
4. `add_satin_layer_style(blend_mode="MULTIPLY", color={92,58,10}, opacity=25, angle=19, distance=8, size=10)`

---

## 5.8 HOLOGRAPHIC / IRIDESCENT TEXT

**Rainbow Gradient:**

- {0: (255,0,153)}, {15: (255,102,0)}, {30: (255,255,0)}, {45: (0,255,102)}, {60: (0,204,255)}, {75: (102,51,255)}, {100: (255,0,153)}

Gradient Overlay angle: 135 + innerBevel smooth depth: 150, size: 4, soften: 2 + Satin LINEAR_DODGE white 30%

---

## 5.9 GLITCH EFFECT TEXT

1. Duplicate text 3x (Red, Green, Blue) + rasterize each
2. Red layer: `set_channel_restrictions` to red → translate 5px left, 2px up → SCREEN
3. Blue layer: `set_channel_restrictions` to blue → translate 5px right, 2px down → SCREEN
4. Green layer: keep position, channel to green → SCREEN
5. Scan lines: new layer → `apply_halftone_pattern` (line, size:1) → OVERLAY 15%
6. Color bands: thin rects, red/cyan, SCREEN 60-80%
7. `apply_noise(amount=15)` → SCREEN 30%

---

## 5.10 EMBOSS / LETTERPRESS TEXT

Dark bg: white text, fill_opacity=0, pillowEmboss direction=down depth=150 size=2, inner shadow 30%
Light bg: same but direction=up, swap highlight/shadow

---

## 5.11 OUTLINE / STROKE TEXT

fill_opacity=0 + `add_stroke_layer_style(size=2, position="CENTER", color=DESIRED)`

---

## 5.12 3D EXTRUDE TEXT

Duplicate 20+ times, each translate 1px right+down, merge all copies, place below original, color overlay darker shade

---

## 5.13 WATERCOLOR TEXT

Rasterize → duplicate → blur copy MULTIPLY 80% → wave on original (low amplitude) → ripple edge bleed MULTIPLY 40%

---

## 5.14 SMOKE TEXT

White on black → rasterize → wave (gen 5, wavelength 10-80, amplitude 5-20) → Gaussian 3px → liquify upward → gradient mask → SCREEN

---

## 5.15 RETRO / VINTAGE TEXT

Warm off-white (240,230,210), stroke 3px red, hard shadow (spread=100, distance=4, size=0), noise 8%

---

## 5.16 GRADIENT FILL TEXT (scene colors)

Method A: `add_gradient_overlay_layer_style` with sampled colors
Method B: place image above text → clip to text (`is_clipping_mask=true`)

---

## 5.17 LAVA / MOLTEN TEXT

**3-layer stack:**

1. Base text with Inner Glow #FF6600 SCREEN 75% size 15, Outer Glow #FF3300 SCREEN 80% size 25, Bevel innerBevel depth 300% size 7
2. Duplicate → rasterize → Gaussian blur 3px → COLOR_DODGE 60%
3. Gradient Map: {0: (0,0,0)}, {30: (128,0,0)}, {60: (255,100,0)}, {85: (255,200,0)}, {100: (255,255,200)}

---

## 5.18 LIQUID TEXT — GAUSSIAN + WAVE + LIQUIFY

1. Rasterize text → duplicate
2. `apply_gaussian_blur(radius=8-12)` on copy
3. `apply_wave(generators=3, wavelength_min=10, wavelength_max=80, amplitude_min=5, amplitude_max=25)`
4. `liquify_forward` — push downward at text edges
5. Gradient mask: show bottom, hide top
6. Gradient Map for colorization → SCREEN 85%

---

## 5.19 LIQUID TEXT — BEVEL & EMBOSS STACKING

**Pure layer styles — no filters needed:**

1. Text layer with 2px stroke
2. `add_bevel_emboss_layer_style(style="innerBevel", technique="smooth", depth=100, size=20, angle=120, altitude=47, highlight_mode="SCREEN", highlight_opacity=100, shadow_mode="MULTIPLY", shadow_opacity=100)`
3. `add_inner_glow_layer_style(size=15, opacity=50, source="edge")`
4. `add_outer_glow_layer_style(size=30, opacity=60)`
5. Set fill_opacity=0 for glass-liquid hybrid

---
