---
name: ps-blend-modes
description: "Photoshop blend mode science with math formulas: darken group (darken, multiply, color burn, linear burn), lighten group (lighten, screen, color dodge, linear dodge), contrast group (overlay, soft light, hard light, vivid light), component group (hue, saturation, color, luminosity). Quick reference for removing black/white backgrounds, adding glow/shadow, texture overlay, color tinting, high-pass sharpen."
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# §2 BLEND MODE SCIENCE

Every blend mode is a **math formula** combining the current layer (top) with layers below (bottom).

## DARKEN GROUP — Result is always darker or same

| Mode        | Formula            | Use For                                                                            |
| ----------- | ------------------ | ---------------------------------------------------------------------------------- |
| DARKEN      | min(top, bottom)   | Composite dark elements, remove white backgrounds                                  |
| MULTIPLY    | top x bottom / 255 | Shadows, dark overlays, multiply textures. **Black stays black, white disappears** |
| COLOR_BURN  | 1 - (1-bottom)/top | Intense dark contrast, dramatic shadows                                            |
| LINEAR_BURN | top + bottom - 255 | Darker than Multiply, harsh dark blending                                          |

## LIGHTEN GROUP — Result is always lighter or same

| Mode         | Formula               | Use For                                                                           |
| ------------ | --------------------- | --------------------------------------------------------------------------------- |
| LIGHTEN      | max(top, bottom)      | Composite light elements, remove black backgrounds                                |
| SCREEN       | 1 - (1-top)(1-bottom) | Glow effects, light leaks, **neon text**. **White stays white, black disappears** |
| COLOR_DODGE  | bottom / (1-top)      | Intense highlights, glowing edges                                                 |
| LINEAR_DODGE | top + bottom          | Brightest additive blend, lens flares                                             |

## CONTRAST GROUP — Darken darks, lighten lights

| Mode        | Formula                                | Use For                                                               |
| ----------- | -------------------------------------- | --------------------------------------------------------------------- |
| OVERLAY     | Multiply if bottom<128, Screen if >128 | **Most versatile.** Texture overlay, high-pass sharpen, color grading |
| SOFT_LIGHT  | Gentle Overlay                         | Subtle color tinting, gentle light/shadow. **Best for color grading** |
| HARD_LIGHT  | Multiply if top<128, Screen if >128    | Like Overlay but keyed to TOP layer                                   |
| VIVID_LIGHT | Color Burn/Dodge combo                 | Use batchplay for this blend mode                                     |

## COMPONENT GROUP — Blend specific color properties

| Mode       | Formula                           | Use For                                         |
| ---------- | --------------------------------- | ----------------------------------------------- |
| HUE        | Hue from top, Sat+Lum from bottom | Change colors without affecting light/shadow    |
| SATURATION | Sat from top, Hue+Lum from bottom | Desaturate/saturate specific areas              |
| COLOR      | Hue+Sat from top, Lum from bottom | **Colorize.** Tinting photos, hand-coloring B&W |
| LUMINOSITY | Lum from top, Hue+Sat from bottom | Apply brightness changes without color shifts   |

## QUICK REFERENCE

```
Remove black background  → SCREEN
Remove white background  → MULTIPLY
Add glow/light           → SCREEN or LINEAR_DODGE
Add shadow/darkness      → MULTIPLY
Texture overlay          → OVERLAY or SOFT_LIGHT
Color tinting            → SOFT_LIGHT or COLOR
High-pass sharpen        → OVERLAY
Color grading            → SOFT_LIGHT
```

---
