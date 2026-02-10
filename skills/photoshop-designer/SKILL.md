---
name: photoshop-designer
description: Complete Photoshop design knowledge base with exact effect recipes, filter chains, parameters, and MCP tool mappings. Load this skill before creating ANY visual effect in Photoshop to execute perfectly on first try with zero trial-and-error.
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# PHOTOSHOP DESIGNER SKILL — COMPLETE REFERENCE

Execute ANY Photoshop design effect perfectly on first try — zero trial-and-error.

## WHEN TO USE THIS SKILL

Load this skill when:
- Creating ANY visual effect in Photoshop (text effects, photo grading, composites)
- Using the adobe-photoshop MCP tools (adb-mcp)
- Applying filters, layer styles, or batchplay commands
- Building posters, social media graphics, photo edits, or composites

## HOW TO USE

1. **Before creating ANY effect** → find the recipe in the relevant section
2. **Follow exact parameters** — do NOT guess or "adjust to taste"
3. **Each recipe maps directly to available MCP tools**
4. If a recipe requires a tool you don't have → use `execute_batchplay`
5. **Read the CRITICAL GOTCHAS section BEFORE executing anything**

---

# §1 FUNDAMENTALS

## 1.1 COORDINATE SYSTEM

- Origin (0,0) = **top-left** corner of canvas
- X increases → RIGHT
- Y increases → DOWN
- Layer bounds: `{left, top, right, bottom}` in pixels from origin
- Center of canvas: `(width/2, height/2)`
- **All MCP position tools use this coordinate system**

## 1.2 LAYER STACK ORDER

- Layers are drawn **bottom-up** — bottom layer renders first, top layer renders last
- `move_layer(position="TOP")` = above all layers (renders last = visually on top)
- `move_layer(position="BOTTOM")` = below all layers (renders first = visually behind)
- When creating layers, they appear ABOVE the currently active layer
- **Adjustment layers affect ALL layers below them** unless clipped

## 1.3 CANVAS ROTATION RULES

- `rotate_canvas` rotates the **entire document** including all layers
- Rotation is **destructive** — pixels are resampled
- Always rotate back by the exact negative amount
- **Plan filter directions BEFORE rotating** — see Wind direction table §7.2
- After rotate+filter+rotate-back, the layer bounds may change slightly

## 1.4 SELECTION FUNDAMENTALS

- Selection = marching ants defining which pixels are affected
- Feather = soft edges (pixels partially selected)
- Anti-alias = smooth diagonal/curved selection edges
- **Selection MUST exist before:** fill_selection, delete_selection, content_aware_fill, generative_fill, add_layer_mask_from_selection
- `select_all` = entire canvas, `clear_selection` = deselect everything
- Selections are per-document, not per-layer

## 1.5 MASK FUNDAMENTALS

- Layer mask = grayscale image controlling layer visibility
- **White = fully visible**, Black = fully hidden, Gray = partially visible
- `add_layer_mask_reveal_all` = white mask (everything shows)
- `add_layer_mask_hide_all` = black mask (everything hidden)
- `fill_mask_with_gradient` = smooth transition between visible/hidden
- To paint on mask: `select_layer_mask` → brush/fill → `select_layer_rgb` to go back
- **Gradient mask direction:** start point = BLACK (hidden), end point = WHITE (visible)

## 1.6 SMART OBJECTS vs RASTERIZED LAYERS

- Smart Objects preserve original data but BLOCK most filters
- **Rasterize BEFORE applying:** Wind, Wave, Twirl, Spherize, Crystallize, Noise, Sharpen, etc.
- Text layers must be rasterized before ANY filter
- `rasterize_layer` is irreversible — always duplicate first
- Shape layers behave like Smart Objects for filters

## 1.7 FILL OPACITY vs LAYER OPACITY

- **Layer Opacity** = affects layer content + ALL layer styles
- **Fill Opacity** = affects ONLY layer content, NOT layer styles (drop shadow, glow, bevel stay at full)
- **Key trick:** Fill 0% + layer styles = invisible content with visible effects (used for glass text)
- Set via: `set_layer_properties(layer_id=X, fill_opacity=0)`

---

# §2 BLEND MODE SCIENCE

Every blend mode is a **math formula** combining the current layer (top) with layers below (bottom).

## DARKEN GROUP — Result is always darker or same

| Mode | Formula | Use For |
|------|---------|---------|
| DARKEN | min(top, bottom) | Composite dark elements, remove white backgrounds |
| MULTIPLY | top × bottom / 255 | Shadows, dark overlays, multiply textures. **Black stays black, white disappears** |
| COLOR_BURN | 1 - (1-bottom)/top | Intense dark contrast, dramatic shadows |
| LINEAR_BURN | top + bottom - 255 | Darker than Multiply, harsh dark blending |

## LIGHTEN GROUP — Result is always lighter or same

| Mode | Formula | Use For |
|------|---------|---------|
| LIGHTEN | max(top, bottom) | Composite light elements, remove black backgrounds |
| SCREEN | 1 - (1-top)(1-bottom) | Glow effects, light leaks, **neon text**. **White stays white, black disappears** |
| COLOR_DODGE | bottom / (1-top) | Intense highlights, glowing edges |
| LINEAR_DODGE | top + bottom | Brightest additive blend, lens flares |

## CONTRAST GROUP — Darken darks, lighten lights

| Mode | Formula | Use For |
|------|---------|---------|
| OVERLAY | Multiply if bottom<128, Screen if >128 | **Most versatile.** Texture overlay, high-pass sharpen, color grading |
| SOFT_LIGHT | Gentle Overlay | Subtle color tinting, gentle light/shadow. **Best for color grading** |
| HARD_LIGHT | Multiply if top<128, Screen if >128 | Like Overlay but keyed to TOP layer |
| VIVID_LIGHT | Color Burn/Dodge combo | ⚠️ **NOT SUPPORTED** by MCP tool — use batchplay |

## COMPONENT GROUP — Blend specific color properties

| Mode | Formula | Use For |
|------|---------|---------|
| HUE | Hue from top, Sat+Lum from bottom | Change colors without affecting light/shadow |
| SATURATION | Sat from top, Hue+Lum from bottom | Desaturate/saturate specific areas |
| COLOR | Hue+Sat from top, Lum from bottom | **Colorize.** Tinting photos, hand-coloring B&W |
| LUMINOSITY | Lum from top, Hue+Sat from bottom | Apply brightness changes without color shifts |

## SCREEN BLEND GOTCHA (CRITICAL)

**SCREEN removes BLACK pixels and keeps WHITE/BRIGHT pixels.**

- White on BLACK background + SCREEN = ✅ white text visible, black gone
- White on TRANSPARENT background + SCREEN = ❌ colors washed out / invisible
- **ALWAYS put content on a BLACK background before using SCREEN blend mode**
- This applies to: neon drip layers, fire layers, smoke layers, light leak layers

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
Merge textures           → OVERLAY
```

---

# §3 BATCHPLAY DESCRIPTOR REFERENCE

## 3.1 DESCRIPTOR FORMAT

```javascript
// Every batchPlay command is an array of descriptor objects
[{
  _obj: "commandName",           // Event string code (required)
  _target: [{                    // What to target (optional)
    _ref: "layer",               // Reference class
    _id: 5                       // By ID (preferred — stable across operations)
  }],
  paramName: value,              // Simple value
  enumParam: {                   // Enum value
    _enum: "enumType",
    _value: "enumValue"
  },
  unitParam: {                   // Value with unit
    _unit: "pixelsUnit",
    _value: 10.0
  }
}]
```

## 3.2 REFERENCE FORMS

```javascript
{_ref: "layer", _id: 42}                                          // By ID (best)
{_ref: "layer", _index: 3}                                        // By index (1-based)
{_ref: "layer", _name: "Background"}                               // By name
{_ref: "layer", _enum: "ordinal", _value: "targetEnum"}           // Currently active
{_ref: "document", _enum: "ordinal", _value: "targetEnum"}        // Active document
{_ref: "channel", _enum: "channel", _value: "red"}                // Red channel
{_ref: "channel", _enum: "channel", _value: "RGB"}                // Composite RGB
```

## 3.3 UNIT TYPES

```javascript
{_unit: "pixelsUnit", _value: 10}      // Pixels
{_unit: "percentUnit", _value: 50}     // Percentage
{_unit: "angleUnit", _value: 90}       // Degrees
{_unit: "densityUnit", _value: 72}     // PPI/DPI
{_unit: "distanceUnit", _value: 5}     // Distance (points)
{_unit: "noneUnit", _value: 1.5}       // Unitless number
```

## 3.4 ALL FILTER BATCHPLAY DESCRIPTORS

### BLUR FILTERS

**Gaussian Blur** (tool: `apply_gaussian_blur`)
```json
[{"_obj": "gaussianBlur", "radius": {"_unit": "pixelsUnit", "_value": 5.0}}]
```

**Motion Blur** (tool: `apply_motion_blur`)
```json
[{"_obj": "motionBlur", "angle": {"_unit": "angleUnit", "_value": 0}, "distance": {"_unit": "pixelsUnit", "_value": 30}}]
```

**Radial Blur** (tool: `apply_radial_blur`)
```json
[{"_obj": "radialBlur", "amount": 10, "blurMethod": {"_enum": "blurMethod", "_value": "spin"}, "blurQuality": {"_enum": "blurQuality", "_value": "good"}}]
```

**Surface Blur** (tool: `apply_surface_blur`)
```json
[{"_obj": "surfaceBlur", "radius": {"_unit": "pixelsUnit", "_value": 5}, "threshold": 15}]
```

**Lens Blur** (tool: `apply_lens_blur`)
```json
[{"_obj": "lensBlur", "iris": {"_obj": "iris", "irisShape": {"_enum": "irisShape", "_value": "hexagon"}, "irisRadius": {"_unit": "pixelsUnit", "_value": 15}, "irisBrightness": 0, "irisRoundness": 0}}]
```

### BLUR GALLERY FILTERS (batchplay only — `blurbTransform`)

⚠️ **Blur Gallery may force dialog** despite `dialogOptions: "dontDisplay"` — known Adobe bug. If it opens dialog, the filter still works.

**Field Blur**
```json
[{"_obj": "blurbTransform", "blurbWidgetType": 0, "blurbGeneralBlurAmount": 15.0, "blurbWidgetLocationX": 500.0, "blurbWidgetLocationY": 500.0}]
```
- blurbGeneralBlurAmount: 0-500px

**Iris Blur**
```json
[{"_obj": "blurbTransform", "blurbWidgetType": 1, "blurbIrisBlurAmount": 25.0, "blurbWidgetLocationX": 500.0, "blurbWidgetLocationY": 500.0}]
```
- Define corner points for ellipse shape, feather 0.0-1.0

**Tilt-Shift Blur**
```json
[{"_obj": "blurbTransform", "blurbWidgetType": 2, "blurbTiltShiftBlurAmount": 30.0, "blurbTiltShiftFocusTop": 300, "blurbTiltShiftFocusBottom": 500, "blurbTiltShiftFeatherTop": 100, "blurbTiltShiftFeatherBottom": 100, "blurbTiltShiftSymmetric": true, "blurbTiltShiftAngle": 0}]
```

**Spin Blur**
```json
[{"_obj": "blurbTransform", "blurbWidgetType": 3, "blurbSpinBlurAngle": 15.0}]
```
- blurbSpinBlurAngle: 0-360

**Path Blur**
```json
[{"_obj": "blurbTransform", "blurbWidgetType": 4, "blurbPathBlurSpeed": 50.0}]
```

### DISTORTION FILTERS

**Wave** (tool: `apply_wave`)
```json
[{"_obj": "wave", "numberOfGenerators": 5, "minimumWavelength": 10, "maximumWavelength": 120, "minimumAmplitude": 5, "maximumAmplitude": 35, "horizontalScale": {"_unit": "percentUnit", "_value": 100}, "verticalScale": {"_unit": "percentUnit", "_value": 100}, "waveType": {"_enum": "waveType", "_value": "sine"}, "undefinedArea": {"_enum": "undefinedArea", "_value": "wrapAround"}, "randomSeed": 0}]
```

**Twirl** (tool: `apply_twirl_distortion`)
```json
[{"_obj": "twirl", "angle": {"_unit": "angleUnit", "_value": 50}}]
```

**Spherize** (tool: `apply_sphere`)
```json
[{"_obj": "spherize", "amount": {"_unit": "percentUnit", "_value": 100}, "spherizeMode": {"_enum": "spherizeMode", "_value": "normal"}}]
```

**Polar Coordinates** (tool: `apply_polar_coordinates`)
```json
[{"_obj": "polar", "conversion": {"_enum": "polarConversionType", "_value": "rectangularToPolar"}}]
```

**Ripple** (tool: `apply_ripple`)
```json
[{"_obj": "ripple", "amount": {"_unit": "percentUnit", "_value": 100}, "rippleSize": {"_enum": "rippleSize", "_value": "medium"}}]
```

**Ocean Ripple** (tool: `apply_ocean_ripple`)
```json
[{"_obj": "oceanRipple", "rippleSize": 9, "rippleMagnitude": 9}]
```

**Pinch** (tool: `apply_pinch`)
```json
[{"_obj": "pinch", "amount": {"_unit": "percentUnit", "_value": 50}}]
```

**Shear** (tool: `apply_shear`)
```json
[{"_obj": "shear", "undefinedArea": {"_enum": "undefinedArea", "_value": "wrapAround"}, "shearPoints": [{"_obj": "point", "x": 0, "y": 0}, {"_obj": "point", "x": 127, "y": 255}]}]
```

**ZigZag** (tool: `apply_zig_zag_distortion`)
```json
[{"_obj": "zigZag", "amount": 10, "zigZagRidges": 5, "zigZagType": {"_enum": "zigZagType", "_value": "aroundCenter"}}]
```

**Displace** (tool: `apply_displace`)
```json
[{"_obj": "displace", "horizontalScale": 10, "verticalScale": 10, "displacementMode": {"_enum": "displacementMode", "_value": "stretchToFit"}, "undefinedArea": {"_enum": "undefinedArea", "_value": "wrapAround"}}]
```

**Glass** (tool: `apply_glass_distortion`)
```json
[{"_obj": "glass", "distortion": 5, "smoothness": 3, "textureType": {"_enum": "textureType", "_value": "frosted"}, "scaling": {"_unit": "percentUnit", "_value": 100}, "invertTexture": false}]
```

### STYLIZE FILTERS

**Wind** (⚠️ NO dedicated tool — MUST use `execute_batchplay`)
```json
[{"_obj": "wind", "windMethod": {"_enum": "windMethod", "_value": "wind"}, "direction": {"_enum": "windDirection", "_value": "left"}}]
```
- windMethod: "wind" | "blast" | "stagger"
- direction: "left" | "right"
- **Wind only blows HORIZONTALLY** — use canvas rotation for vertical effects
- "wind" method = controlled thin streaks. "blast" = thick aggressive (TOO MUCH). "stagger" = randomized.

**Emboss** (tool: `apply_emboss`)
```json
[{"_obj": "emboss", "angle": {"_unit": "angleUnit", "_value": 135}, "height": 3, "amount": {"_unit": "percentUnit", "_value": 100}}]
```

**Find Edges** (tool: `apply_find_edges`)
```json
[{"_obj": "findEdges"}]
```

**Solarize** (tool: `apply_solarize`)
```json
[{"_obj": "solarize"}]
```

**Diffuse Glow** (NO dedicated tool)
```json
[{"_obj": "diffuseGlow", "graininess": 6, "glowAmount": 10, "clearAmount": 15}]
```

**Glowing Edges** (NO dedicated tool)
```json
[{"_obj": "glowingEdges", "edgeWidth": 2, "edgeBrightness": 6, "smoothness": 5}]
```
- edgeWidth: 1-14, edgeBrightness: 0-20, smoothness: 1-15

### SKETCH FILTERS

**Chrome** (tool: `apply_chrome_filter`)
```json
[{"_obj": "chrome", "detail": 4, "smoothness": 7}]
```

### ARTISTIC FILTERS

**Plastic Wrap** (tool: `apply_plastic_wrap`)
```json
[{"_obj": "plasticWrap", "highlightStrength": 15, "detail": 9, "smoothness": 7}]
```

**Oil Paint** (tool: `apply_oil_paint`)
```json
[{"_obj": "oilPaint", "stylization": 4.0, "cleanliness": 5.0, "brushScale": 0.5, "bristleDetail": 2.0, "lightingOn": true}]
```

**Neon Glow FILTER** (NOT layer style — different effect)
```json
[{"_obj": "neonGlow", "glowSize": 5, "glowBrightness": 15, "color": {"_obj": "RGBColor", "red": 72.0, "grain": 35.0, "blue": 142.0}}]
```
- ⚠️ "grain" = green channel internally (Photoshop quirk)
- glowSize: -24 to 24, glowBrightness: 0-50

### NOISE FILTERS

**Add Noise** (tool: `apply_noise`)
```json
[{"_obj": "addNoise", "amount": {"_unit": "percentUnit", "_value": 5}, "distribution": {"_enum": "distribution", "_value": "gaussian"}, "monochromatic": true}]
```

**Despeckle** (tool: `apply_despeckle`)
```json
[{"_obj": "despeckle"}]
```

**Dust & Scratches** (tool: `apply_dust_and_scratches`)
```json
[{"_obj": "dustAndScratches", "radius": {"_unit": "pixelsUnit", "_value": 1}, "threshold": 0}]
```

**Median** (tool: `apply_median_noise`)
```json
[{"_obj": "median", "radius": {"_unit": "pixelsUnit", "_value": 1}}]
```

### SHARPEN FILTERS

**Unsharp Mask** (tool: `apply_unsharp_mask`)
```json
[{"_obj": "unsharpMask", "amount": {"_unit": "percentUnit", "_value": 100}, "radius": {"_unit": "pixelsUnit", "_value": 1.0}, "threshold": 0}]
```

**High Pass** (tool: `apply_high_pass`)
```json
[{"_obj": "highPass", "radius": {"_unit": "pixelsUnit", "_value": 10.0}}]
```

**Smart Sharpen** (tool: `apply_smart_sharpen`)
```json
[{"_obj": "smartSharpen", "amount": {"_unit": "percentUnit", "_value": 100}, "radius": {"_unit": "pixelsUnit", "_value": 1.0}, "noiseReduction": {"_unit": "percentUnit", "_value": 0}, "blur": {"_enum": "blurType", "_value": "gaussianBlur"}}]
```

### PIXELATE FILTERS

**Mosaic** (tool: `apply_pixelate`)
```json
[{"_obj": "mosaic", "cellSize": {"_unit": "pixelsUnit", "_value": 10}}]
```

**Crystallize** (tool: `apply_crystallize`)
```json
[{"_obj": "crystallize", "cellSize": 10}]
```

**Color Halftone** (tool: `apply_color_halftone`)
```json
[{"_obj": "colorHalftone", "radius": {"_unit": "pixelsUnit", "_value": 8}, "angle1": {"_unit": "angleUnit", "_value": 108}, "angle2": {"_unit": "angleUnit", "_value": 162}, "angle3": {"_unit": "angleUnit", "_value": 90}, "angle4": {"_unit": "angleUnit", "_value": 45}}]
```

### RENDER FILTERS (batchplay only)

**Clouds**
```json
[{"_obj": "clouds"}]
```
- Uses current foreground/background colors

**Difference Clouds**
```json
[{"_obj": "$DrfC"}]
```

**Lens Flare**
```json
[{"_obj": "lensFlare", "brightness": 100, "flareCenter": {"_obj": "point", "horizontal": {"_unit": "pixelsUnit", "_value": 500}, "vertical": {"_unit": "pixelsUnit", "_value": 500}}, "lensType": {"_enum": "lensType", "_value": "moviePrime"}}]
```
- lensType: "zoomLens" (50-300mm) | "moviePrime" (105mm) | "prime35" (35mm)

**Fibers** (HAS seed control)
```json
[{"_obj": "fibers", "variance": 16, "strength": 4, "randomSeed": 12345}]
```
- Also accepts `{"_obj": "$Fbrs", ...}` — both work

**Lighting Effects**
```json
[{"_obj": "lightingEffects", "lightList": [{"_obj": "lightSource", "lightType": {"_enum": "lightType", "_value": "spotLight"}, "intensity": 50, "focus": 60, "posX": 500, "posY": 300}]}]
```
- lightType: "spotLight" | "omniLight" | "directionalLight"
- ⚠️ Complex descriptor — may require dialog for full control

### CORE OPERATIONS

**Apply Image** (for frequency separation)
```json
[{"_obj": "applyImageEvent", "with": {"_obj": "calculation", "to": {"_ref": [{"_ref": "channel", "_enum": "channel", "_value": "RGB"}, {"_ref": "layer", "_name": "Low"}]}, "calculation": {"_enum": "calculationType", "_value": "subtract"}, "scale": 2, "offset": 128}, "_target": [{"_ref": "layer", "_name": "High"}]}]
```

**Select layer by ID**
```json
[{"_obj": "select", "_target": [{"_ref": "layer", "_id": 42}], "makeVisible": false}]
```

**Set channel restrictions (for glitch effect)**
```json
[{"_obj": "set", "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}], "to": {"_obj": "layer", "channelRestrictions": [{"_ref": "channel", "_enum": "channel", "_value": "red"}]}}]
```

**Reset channel restrictions**
```json
[{"_obj": "set", "_target": [{"_ref": "layer", "_enum": "ordinal", "_value": "targetEnum"}], "to": {"_obj": "layer", "channelRestrictions": [{"_ref": "channel", "_enum": "channel", "_value": "RGB"}]}}]
```

**Invert layer (not selection)**
```json
[{"_obj": "invert"}]
```

**Desaturate**
```json
[{"_obj": "desaturate"}]
```

**Halftone Pattern**
```json
[{"_obj": "halftonePattern", "size": 1, "contrast": 50, "patternType": {"_enum": "halftonePatternType", "_value": "line"}}]
```

## 3.5 FILTER SCRIPTABILITY TABLE

| Filter | Headless (no dialog) | Notes |
|--------|---------------------|-------|
| All standard filters | ✅ Yes | gaussianBlur, wave, wind, etc. |
| Blur Gallery (Field/Iris/Tilt/Spin/Path) | ⚠️ May force dialog | Known Adobe bug |
| Camera Raw Filter | ❌ No | Always requires dialog. Use Curves/Levels instead |
| Liquify (full mesh) | ❌ No | Mesh is binary data. Only `liquify_forward` works |
| Adaptive Wide Angle | ❌ No | Requires dialog |
| Vanishing Point | ❌ No | Requires dialog |
| Lens Correction (auto) | ❌ No | Manual lens_correction tool works fine |
| Neural Filters | ❌ No | Cloud-based, requires dialog |

## 3.6 CharID → StringID MAP (obscure filters)

```
NGlw = neonGlow        GlwE = glowingEdges
DfsG = diffuseGlow     LghE = lightingEffects
Fbrs = fibers          Clds = clouds
DfrC = differenceClouds
```

## 3.7 EVENT CODE TABLE

**Blur:** gaussianBlur, motionBlur, radialBlur, smartBlur, surfaceBlur, lensBlur, blurEvent, blurbTransform
**Distort:** wave, twirl, spherize, polar, ripple, oceanRipple, pinch, shear, zigZag, displace, glass
**Stylize:** wind, emboss, findEdges, diffuse, tiles, extrude, solarize, glowingEdges
**Sketch:** chrome, basRelief, chalkCharcoal, charcoal, photocopy, stamp, tornEdges, waterPaper, notePaper, plaster, reticulation, halftonePattern, graphicPen
**Artistic:** plasticWrap, diffuseGlow, dryBrush, filmGrain, fresco, neonGlow, paletteKnife, paintDaubs, roughPastels, smudgeStick, sponge, underpainting, watercolor, posterEdges
**Noise:** addNoise, despeckle, dustAndScratches, median
**Sharpen:** sharpen, sharpenEdges, sharpenMore, unsharpMask, highPass, smartSharpen
**Render:** clouds, $DrfC (diff clouds), lensFlare, fibers/$Fbrs
**Texture:** craquelure, grain, mosaicPlugin, patchwork, stainedGlass, texturizer
**Pixelate:** colorHalftone, crystallize, facet, fragment, mezzotint, mosaic, pointillize
**Operations:** make, set, get, delete, select, move, duplicate, hide, show, transform, crop, canvasSize, imageSize
**Adjustments:** curves, levels, hueSaturation, colorBalance, brightnessEvent, channelMixer, selectiveColor, posterization, thresholdClassEvent, invert, desaturate, gradientMapEvent

---

# §4 TEXT EFFECTS — 19 Verified Recipes

## 4.1 LIQUID DRIP / MELTING TEXT

**Result:** Flowing tendrils/streams dripping DOWNWARD from text bottom

**⚠️ CRITICAL DIRECTION LOGIC (verified by testing):**
```
CORRECT: Rotate -90 CCW → Wind "from left" × 5-7 → Rotate +90 CW back = DRIPS DOWN ✅
WRONG:   Rotate +90 CW  → Wind "from right" × 5 → Rotate -90 CCW back = DRIPS UP ❌
```

**Why:** Rotate -90 CCW → text bottom faces RIGHT → Wind "from left" pushes pixels RIGHT (toward bottom) → Rotate +90 CW back → RIGHT streaks become DOWNWARD

**⚠️ CRITICAL: White text on BLACK background (not transparent) — SCREEN blend removes black**

**MCP Tool Chain:**
```
1. duplicate_layer (preserve original text)
2. rasterize_layer
3. Create BLACK pixel layer → merge with text (white on black)
4. scale_layer 300% height from TOPCENTER (elongate before wind)
5. rotate_canvas(angle=-90)
6. execute_batchplay (Wind "from left", "wind" method) × 5-7 times
7. rotate_canvas(angle=90)
8. apply_gaussian_blur(radius=2-3)
9. set_layer_properties(blend_mode="SCREEN", layer_opacity=90)
10. add_gradient_map_adjustment_layer (clipped — colorize)
11. add_outer_glow_layer_style (neon color glow)
12. add_layer_mask + fill_mask_with_gradient (hide top, show bottom)
```

**Wind batchPlay (execute 5-7 times for medium-long drips):**
```json
[{"_obj": "wind", "windMethod": {"_enum": "windMethod", "_value": "wind"}, "direction": {"_enum": "windDirection", "_value": "left"}}]
```

**Common Mistakes:**
- ❌ Rotating CW (+90) first → drips go UP
- ❌ Wind "from right" after CW rotation → drips go UP
- ❌ Using "blast" method → too messy/aggressive, layer goes off-canvas
- ❌ "blast" × 10 → WAY too much, layer bounds explode
- ❌ Using Motion Blur → symmetrical, goes BOTH directions
- ❌ White on TRANSPARENT + SCREEN → colors invisible
- ❌ Wave amplitude too high (>40) → text destroyed
- ❌ Forgetting gradient mask → top of text gets distorted
- ❌ Scale 400%+ → too much stretch

---

## 4.2 CHROME / METALLIC TEXT

**Gradient Overlay:** reflected, angle: 90
- stops: {0: (26,26,26)}, {25: (216,216,216)}, {50: (26,26,26)}, {75: (250,250,250)}, {100: (26,26,26)}

**Bevel & Emboss:** innerBevel, chiselHard, depth: 300, size: 5, angle: 120, altitude: 30
- highlight: SCREEN white 90%, shadow: MULTIPLY black 75%

---

## 4.3 NEON GLOW TEXT

**Result:** Realistic neon sign on dark background

**Neon Color Palette (hex → RGB):**
| Color | Hex | RGB |
|-------|-----|-----|
| Pink | #FF1177 | (255, 17, 119) |
| Blue | #00D4FF | (0, 212, 255) |
| Green | #39FF14 | (57, 255, 20) |
| Red | #FF073A | (255, 7, 58) |
| Yellow | #FFE500 | (255, 229, 0) |
| Cyan | #05D9FF | (5, 217, 255) |
| Purple | #CC00FF | (204, 0, 255) |
| Red Authentic | #FF2A6D | (255, 42, 109) |
| Green Authentic | #00F5A8 | (0, 245, 168) |

**Layer Styles on text:**
1. `add_inner_glow_layer_style(blend_mode="NORMAL", opacity=100, color=NEON_COLOR, source="center", choke=0, size=8)`
2. `add_outer_glow_layer_style(blend_mode="SCREEN", opacity=100, color=NEON_COLOR, spread=0, size=20)`
3. `add_drop_shadow_layer_style(blend_mode="SCREEN", color=NEON_COLOR, opacity=100, distance=0, spread=0, size=60)`
   - drop shadow with SCREEN + distance=0 = wide ambient glow

**Multi-Layer Glow Stacking (Korean/Russian technique for INTENSE glow):**
1. Duplicate text layer → set fill_opacity=0, layer_opacity=20% → Gaussian Blur 15px → SCREEN
2. Duplicate again → Gaussian Blur 40px → SCREEN 50%
3. Duplicate again → Gaussian Blur 80px → SCREEN 30%
4. Result: 4 layers creating photorealistic multi-radius glow

**Background glow:** Large soft brush (800px+) neon color on new layer below text → Lighten or Linear Light 20-40%

**Noise for realism:** `apply_noise(amount=2-5, monochromatic=true)` on final composite

---

## 4.4 GLASS / FROSTED TEXT

**Key:** `set_layer_properties(fill_opacity=0)` — NOT layer opacity

1. `add_bevel_emboss_layer_style(style="innerBevel", technique="smooth", depth=150, size=10, soften=2, angle=120, altitude=30, highlight_mode="SCREEN", highlight_opacity=85, shadow_mode="MULTIPLY", shadow_opacity=50)`
2. `add_inner_shadow_layer_style(blend_mode="MULTIPLY", opacity=30, angle=120, distance=3, choke=0, size=5)`
3. `add_inner_glow_layer_style(blend_mode="SCREEN", color={255,255,255}, opacity=30, source="edge", choke=0, size=8)`
4. `add_stroke_layer_style(size=1, position="INSIDE", blend_mode="SCREEN", color={255,255,255}, opacity=50)`

---

## 4.5 FIRE / FLAME TEXT

**Same Wind technique as drip but OPPOSITE direction:**
```
Rotate +90 CW → Wind "from left" × 3-5 → Rotate -90 CCW back = FLAMES UP
```

**Steps:**
1. White text on black background → rasterize → merge to single layer
2. `rotate_canvas(angle=90)` → CW
3. Wind "from left" via batchplay × 3-5
4. `rotate_canvas(angle=-90)` → back
5. `apply_gaussian_blur(radius=1.5)`
6. Optional: `apply_ripple(amount=110, size="medium")` for flicker
7. Gradient Map fire colors:
   - {0: (0,0,0)}, {30: (255,0,0)}, {55: (255,102,0)}, {80: (255,204,0)}, {100: (255,255,255)}

**Chinese fire text (CSDN verified):** After gradient map, convert to Grayscale → Indexed Color → Color Table "Black Body" for authentic flame palette

---

## 4.6 ICE / FROZEN TEXT

**Text color:** RGB (168, 216, 234)

1. `add_bevel_emboss_layer_style(style="innerBevel", technique="chiselHard", depth=250, size=5, angle=120, altitude=30, highlight_mode="SCREEN", highlight_opacity=90, shadow_mode="MULTIPLY", shadow_color={26,58,92}, shadow_opacity=70)`
2. `add_inner_glow_layer_style(blend_mode="SCREEN", color={200,232,255}, opacity=50, source="edge", size=12)`
3. `add_satin_layer_style(blend_mode="SCREEN", color={200,232,255}, opacity=30, angle=19, distance=11, size=14, invert=true)`

**Frost texture:** Duplicate → rasterize → `apply_crystallize(cell_size=5)` → OVERLAY 40% → `apply_noise(5)`

**Ice text (Chinese method):** Chrome filter Detail 4 Smoothness 7 → Wind ×2 → Gradient White→Ice Blue → Bevel depth 150% size 8

---

## 4.7 GOLD / LUXURY TEXT

**Gold Gradient Stops:**
- {0: (191,149,63)}, {25: (252,246,186)}, {50: (179,135,40)}, {75: (251,245,183)}, {100: (170,119,28)}

1. `add_gradient_overlay_layer_style` with gold stops, angle: 90, type: "linear"
2. `add_bevel_emboss_layer_style(style="innerBevel", technique="smooth", depth=200, size=3, highlight_color={252,246,186}, shadow_color={92,58,10})`
3. `add_stroke_layer_style(size=2, position="OUTSIDE")` with same gold gradient
4. `add_satin_layer_style(blend_mode="MULTIPLY", color={92,58,10}, opacity=25, angle=19, distance=8, size=10)`

---

## 4.8 HOLOGRAPHIC / IRIDESCENT TEXT

**Rainbow Gradient:**
- {0: (255,0,153)}, {15: (255,102,0)}, {30: (255,255,0)}, {45: (0,255,102)}, {60: (0,204,255)}, {75: (102,51,255)}, {100: (255,0,153)}

Gradient Overlay angle: 135 + innerBevel smooth depth: 150, size: 4, soften: 2 + Satin LINEAR_DODGE white 30%

---

## 4.9 GLITCH EFFECT TEXT

1. Duplicate text 3× (Red, Green, Blue) + rasterize each
2. Red layer: channel restrict to red → translate 5px left, 2px up → SCREEN
3. Blue layer: channel restrict to blue → translate 5px right, 2px down → SCREEN
4. Green layer: keep position, channel to green → SCREEN
5. Scan lines: new layer → halftone pattern (line, size:1) → OVERLAY 15%
6. Color bands: thin rects, red/cyan, SCREEN 60-80%
7. Noise: addNoise 15% → SCREEN 30%

---

## 4.10 EMBOSS / LETTERPRESS TEXT

Dark bg: white text, fill_opacity=0, pillowEmboss direction=down depth=150 size=2, inner shadow 30%
Light bg: same but direction=up, swap highlight/shadow

---

## 4.11 OUTLINE / STROKE TEXT

fill_opacity=0 + `add_stroke_layer_style(size=2, position="CENTER", color=DESIRED)`

---

## 4.12 3D EXTRUDE TEXT

Duplicate 20+ times, each translate 1px right+down, merge all copies, place below original, color overlay darker shade

---

## 4.13 WATERCOLOR TEXT

Rasterize → duplicate → blur copy MULTIPLY 80% → wave on original (low amplitude) → ripple edge bleed MULTIPLY 40%

---

## 4.14 SMOKE TEXT

White on black → rasterize → wave (gen 5, wavelength 10-80, amplitude 5-20) → Gaussian 3px → liquify upward → gradient mask → SCREEN

**Smoke text (Chinese method):** Motion Blur 90° Distance 40px → Wind → Wave generators 5 wavelength 10-120 amplitude 1-5 → Gaussian 2px

---

## 4.15 RETRO / VINTAGE TEXT

Warm off-white (240,230,210), stroke 3px red, hard shadow (spread=100, distance=4, size=0), noise 8%

---

## 4.16 GRADIENT FILL TEXT (scene colors)

Method A: `add_gradient_overlay_layer_style` with sampled colors
Method B: place image above text → clip to text (`is_clipping_mask=true`)

---

## 4.17 LAVA / MOLTEN TEXT (Chinese Sener method)

**3-layer stack technique:**
1. Base text layer with layer styles:
   - Inner Glow: color #FF6600, SCREEN 75%, size 15
   - Outer Glow: color #FF3300, SCREEN 80%, size 25
   - Bevel & Emboss: innerBevel, smooth, depth 300%, size 7
2. Duplicate text → rasterize → Gaussian blur 3px → COLOR_DODGE 60%
3. Gradient Map on top: {0: (0,0,0)}, {30: (128,0,0)}, {60: (255,100,0)}, {85: (255,200,0)}, {100: (255,255,200)}
4. `apply_noise(amount=3)` for texture

---

## 4.18 LIQUID TEXT — METHOD B: GAUSSIAN + TILT-SHIFT + LIQUIFY

**Alternative to Wind+Rotate for organic liquid look:**
1. Rasterize text → duplicate
2. `apply_gaussian_blur(radius=8-12)` on copy
3. `apply_wave(generators=3, wavelength_min=10, wavelength_max=80, amplitude_min=5, amplitude_max=25)`
4. `liquify_forward` — brush 80-150, pressure 50-70, push downward at text edges
5. Gradient mask: show bottom, hide top
6. Gradient Map: dark→mid→neon for colorization
7. SCREEN blend 85%

---

## 4.19 LIQUID TEXT — METHOD C: BEVEL & EMBOSS STACKING (Bilibili)

**Pure layer styles — no filters needed:**
1. Text layer with 2px stroke (any color)
2. `add_bevel_emboss_layer_style(style="innerBevel", technique="smooth", depth=100, size=20, angle=120, altitude=47, highlight_mode="SCREEN", highlight_opacity=100, shadow_mode="MULTIPLY", shadow_opacity=100)`
3. `add_inner_glow_layer_style(blend_mode="SCREEN", size=15, opacity=50, source="edge")`
4. `add_outer_glow_layer_style(blend_mode="SCREEN", size=30, opacity=60)`
5. Set fill_opacity=0 for glass-liquid hybrid
6. Place gradient/texture below for color

---

# §5 BACKGROUND & PHOTO EFFECTS — 13 Recipes

## 5.1 BOKEH BACKGROUND

Soft brush dabs (800-1200px, opacity 15-30%, hardness 0) → Gaussian blur 8-15px → duplicate at 70% scale for depth

## 5.2 GRADIENT MESH BACKGROUND

3-5 pixel layers, each with single soft brush dab (800-1200px) of different color → Gaussian blur 200-350px each → stack at 70-90% opacity

**Popular colors:** Magenta (220,50,180), Cyan (0,200,255), Purple (130,50,220), Deep Blue (10,10,80)

## 5.3 LIGHT LEAK / FLARE

Soft brush warm colors → blur 80-120px → SCREEN 50-70% → position at corners

## 5.4 CYBERPUNK / SYNTHWAVE GRADING

- Color balance: shadows → blue [0,0,50], highlights → pink [30,-10,-20]
- Levels: output_shadow=15 (raised black point)
- Vibrance +30

## 5.5 RETRO / VINTAGE GRADING (faded blacks)

1. Curves composite: [{0,30},{255,240}] — raised blacks + capped whites
2. Curves red: [{0,12},{255,255}]
3. Curves blue: [{0,35},{255,220}]
4. Hue/Sat: saturation -25
5. Photo filter: warm (236,138,0) density 22
6. Noise 4% mono → OVERLAY 35%

## 5.6 DUOTONE

`add_gradient_map_adjustment_layer` with 2 stops
**Combos:** Midnight Blue→Gold, Deep Purple→Pink, Dark Teal→Orange, Black→Cyan

## 5.7 DOUBLE EXPOSURE

Portrait + landscape → SCREEN 70-85% → mask to reveal face details

## 5.8 VIGNETTE

Method 1: `lens_correction(vignette=-80, vignette_midpoint=40)`
Method 2: ellipse select → invert → fill black → reduce opacity 40-60%

## 5.9 COLOR POP

Hue/sat -100 on top → paint black on mask over colored object

## 5.10 HDR EFFECT

S-curve + high_pass OVERLAY 50% + vibrance +30 + shadows_highlights(50,30)

## 5.11 MINIATURE / TILT-SHIFT

Duplicate → blur 15-25px → reflected gradient mask (sharp band center) → boost vibrance/saturation

## 5.12 SKIN RETOUCHING (frequency separation)

**Low freq:** Duplicate → blur 6-10px
**High freq:** Duplicate original → high_pass 6-10px → LINEAR_LIGHT
Or use Apply Image batchplay (§3.4 Core Operations)

## 5.13 DAY TO NIGHT

Curves pull highlights down → blue color balance → desat -30 → paint warm lights on SCREEN layer

---

# §6 COLOR GRADING RECIPES

## 6.1 TEAL & ORANGE (cinematic — exact curve points)

**Red channel curves:** input 60→output 45, input 190→output 210
**Green channel curves:** input 75→output 70, input 180→output 185
**Blue channel curves:** input 50→output 75, input 200→output 175

Result: warm skin tones + cool teal shadows — Hollywood standard

## 6.2 JAPANESE ANIME STYLE

1. S-curve on composite for contrast
2. Blue shadows: +10 via color balance
3. Blue highlights: -5
4. Selective Color → Reds: saturation +15, lightness +5
5. Selective Color → Cyans: saturation +20
6. Vibrance +20, saturation +5

## 6.3 MOODY BLUE

Blue shadows +40, desaturate -20, lower highlights via curves

## 6.4 WARM VINTAGE

Raise black point to 20, warm photo filter, desat -15

---

# §7 TOOL REFERENCE & WIND TABLE

## 7.1 TOOL-TO-EFFECT QUICK REFERENCE

| Effect | Primary Tool | Key Parameters |
|--------|-------------|----------------|
| Liquid drip DOWN | execute_batchplay (Wind) | rotate -90, Wind "left" ×5-7, rotate +90 |
| Flames UP | execute_batchplay (Wind) | rotate +90, Wind "left" ×3-5, rotate -90 |
| Chrome text | gradient_overlay + bevel_emboss | reflected gradient, chiselHard depth 300 |
| Neon glow | outer_glow + inner_glow + drop_shadow(SCREEN) | SCREEN blend, neon colors |
| Glass text | fill_opacity=0 + bevel | innerBevel smooth |
| Gold text | gradient_overlay + bevel + satin | Gold gradient stops |
| Blur bg | gaussian_blur or lens_blur | 12-20px depth, 15+ lens |
| Color grade | curves + color_balance | Per-channel curves |
| Duotone | gradient_map | Two-color gradient |
| Vignette | lens_correction OR ellipse+invert+fill | vignette=-80 or manual |
| HDR | curves S + high_pass OVERLAY + vibrance | high_pass 10px, OVERLAY 50% |
| Retro faded | curves (raised blacks) + desat + warm filter | output_shadow:30, sat:-25 |
| Halftone | color_halftone | max_radius: 4-12 |
| Smoke/fog | brush + blur + SCREEN | low opacity, high blur |

## 7.2 WIND DIRECTION MASTER TABLE

Wind only blows horizontally. Use canvas rotation for vertical effects.

| Desired Effect | Canvas Rotation | Wind Direction | Rotate Back | Result |
|---------------|----------------|----------------|-------------|--------|
| Drips DOWN | -90 (CCW) | "left" ×5-7 | +90 (CW) | ✅ Streaks downward |
| Flames UP | +90 (CW) | "left" ×3-5 | -90 (CCW) | ✅ Streaks upward |
| Streaks RIGHT | None needed | "left" ×3-5 | None | ✅ Horizontal right |
| Streaks LEFT | None needed | "right" ×3-5 | None | ✅ Horizontal left |

**"left" = FROM the left = pushes pixels RIGHT. "right" = FROM the right = pushes pixels LEFT.**

**Wind method comparison:**
- "wind" = controlled thin streaks — **USE THIS** for drip/fire effects
- "blast" = thick aggressive splatter — TOO MUCH for most effects, layer bounds explode
- "stagger" = randomized jagged streaks — good for lightning/electricity

## 7.3 FILTER PARAMETER RANGES

| Filter | Parameter | Range | Default |
|--------|-----------|-------|---------|
| Gaussian Blur | radius | 0.1-250px | 2.5 |
| Motion Blur | distance | 1-2000px | 30 |
| Radial Blur | amount | 1-100 | 10 |
| Surface Blur | radius/threshold | 1-100 / 2-255 | 5/15 |
| Lens Blur | radius | 0-100 | 15 |
| Noise | amount | 0.1-400% | 5 |
| Wave | generators/wavelength/amplitude | 1-999 / 1-999 / 1-999 | 5/10-120/5-35 |
| Unsharp Mask | amount/radius/threshold | 1-500% / 0.1-1000px / 0-255 | 100/1.0/0 |
| High Pass | radius | 0.1-1000px | 10 |
| Liquify brush | size | 1-15000px | 64 |
| Wind | method | wind/blast/stagger | wind |

---

# §8 DESIGN PRINCIPLES

## 8.1 COLOR RULES

**60-30-10 Rule:** 60% dominant, 30% secondary, 10% accent

**Color Psychology:** Red=urgency, Blue=trust, Green=growth, Purple=luxury, Black=power, Orange=energy

## 8.2 TYPOGRAPHY RULES

- **Max 2 fonts** per design (3 absolute max)
- **Title: 2-3x body size** minimum
- **ALL CAPS: add tracking +50 to +200**
- **Line height:** Headlines 1.0-1.2x, Body 1.4-1.6x
- **Never use Thin/Light below 24pt**

## 8.3 COMPOSITION

- Rule of Thirds: focal point at grid intersections
- Z-Pattern: Logo top-left → headline top → image bottom-left → CTA bottom-right
- White space: when in doubt, add MORE

## 8.4 CONTRAST & READABILITY

- Body text: minimum 4.5:1 contrast ratio
- Large text (18pt+ bold): minimum 3:1
- Text on images: 50-70% black overlay, or blur background
- Dark bg: off-white (224,225,221) not pure white
- Light bg: dark gray (51,51,51) not pure black

## 8.5 DIMENSIONS

| Platform | Size |
|----------|------|
| Instagram Post | 1080×1080 |
| Instagram Story/Reel | 1080×1920 |
| Twitter/X | 1600×900 |
| YouTube Thumb | 1280×720 |
| LinkedIn | 1200×627 |
| Facebook | 1200×630 |
| A4 Print (300dpi) | 2480×3508 |

---

# §9 WORKFLOW TEMPLATES

## 9.1 POSTER CREATION

```
1. Create canvas (correct dimensions + DPI)
2. Place background image
3. Color grade: curves S-curve + color balance + vibrance
4. Cut out subject: select_subject → mask OR remove_background
5. Add main text: create_text_layer → position
6. Apply text effects (per recipes §4)
7. Add secondary text (subtitle, credits)
8. Add logos (place_image — ignore the error)
9. Final color harmony: unified color overlay SOFT_LIGHT 10-20%
10. Export: save_document_as
```

## 9.2 PHOTO EDIT

```
1. Open → duplicate background
2. auto_tone / auto_color OR manual curves+levels
3. Skin retouch (§5.12)
4. Color grade (§6)
5. Local adjustments (dodge/burn §10.2)
6. Sharpen (high_pass OVERLAY §10.1)
7. Vignette (§5.8)
8. Optional noise 2-3% OVERLAY
9. Export
```

## 9.3 COMPOSITE

```
1. Background plate
2. Subject (select_subject or remove_background)
3. Match lighting: harmonize_layer OR manual curves
4. Cast shadow: duplicate subject → flip vertical → blur → MULTIPLY 30-40%
5. Color unification: photo_filter or solid fill SOFT_LIGHT 10-15%
6. Final adjustments
```

---

# §10 ADVANCED TECHNIQUES

## 10.1 HIGH-PASS SHARPENING

`stamp_visible` → `apply_high_pass(radius=2-5)` → `set_layer_properties(blend_mode="OVERLAY")` → opacity 50-80%

## 10.2 DODGE & BURN (non-destructive)

`create_pixel_layer(fill_neutral=true, blend_mode="OVERLAY")` → paint WHITE to dodge, BLACK to burn, opacity 10-15% per stroke

## 10.3 ORTON EFFECT (dreamy glow)

`stamp_visible` → `apply_gaussian_blur(radius=20-40)` → SCREEN 40-60%

## 10.4 BLEND-IF COMPOSITING

`set_layer_blend_if` for seamless tone-based blending:
- Remove dark bg: this_layer_black=20, black_feather=50
- Show in bright areas: underlying_white=180, white_feather=220
- **Feather points:** black_feather > black, white_feather < white

## 10.5 LUMINOSITY MASKING

Load RGB as selection via batchplay → save as Highlights channel → invert for Shadows → intersect for targeted masks

## 10.6 STAMP VISIBLE

`stamp_visible` = flattened copy of all visible layers as new layer on top. Use BEFORE destructive effects.

---

# §11 CRITICAL TOOL GOTCHAS — 17 VERIFIED

These are verified bugs/behaviors that WILL cause failures if ignored:

1. **`select_layer` CAN DELETE LAYERS** — Use `set_layer_properties` or `execute_batchplay` to target layers instead
2. **`set_layer_properties` RESETS clipping mask** — Always pass `is_clipping_mask=false` (or true if clipped) to preserve state
3. **`place_image` always throws error** — But the layer IS created. **Ignore the error and continue.**
4. **`VIVID_LIGHT` blend mode is rejected** — MCP tool doesn't support it. Use batchplay.
5. **`scale_layer` fails silently on Smart Objects** — Use `free_transform` instead
6. **`generate_image`/`generative_fill` return success but produce nothing** — Adobe Firefly AI tools unreliable in MCP
7. **Canvas rotation affects ALL layers** — Every layer rotates. Plan accordingly.
8. **Wind filter has NO dedicated tool** — Must use `execute_batchplay`
9. **Filters require rasterized layers** — Text, shape, Smart Object layers will fail. Always rasterize first.
10. **`translate_layer` Y axis is inverted in description** — Positive Y moves DOWN (standard screen coords), despite doc saying "up"
11. **SCREEN blend requires BLACK background** — White on transparent + SCREEN = invisible. White on BLACK + SCREEN = correct.
12. **Wind "blast" method is TOO aggressive** — Use "wind" method for controlled streaks. Blast causes layer bounds to explode.
13. **Global Light is shared** — Bevel and Drop Shadow share angle by default. Uncheck "Use Global Light" in batchplay if you need independent angles.
14. **File tokens required for file paths** — batchPlay won't trust raw file paths in some contexts. Use `localFileSystem.createSessionToken()` in UXP.
15. **All modifying batchPlay in UXP needs executeAsModal** — Direct execution without modal wrapper will fail silently.
16. **Blur Gallery may force dialog** — Field/Iris/Tilt-Shift/Spin/Path blur `blurbTransform` may open dialog despite `dialogOptions: "dontDisplay"`.
17. **Camera Raw Filter NOT scriptable headless** — Always requires dialog. Use Curves + Levels + Color Balance for equivalent results.

---

# §12 FAILED POSTER ATTEMPTS LOG — DO NOT REPEAT

| # | What Went Wrong | Why | Correct Approach |
|---|----------------|-----|------------------|
| 1 | Wave distorted entire text horizontally | Wave without directional control | Use Wind (directional) not Wave |
| 2 | Stretch 400% + blur + wave = sideways | Wave goes ALL directions | Wind + canvas rotation |
| 3 | Motion blur 90° = streams UP and DOWN | Motion blur is symmetric | Wind is one-directional |
| 4 | Rotate +90 CW + Wind right = UP | Wrong rotation direction | -90 CCW + Wind left = DOWN |
| 5 | Texture overlay clipped to text | User said NO texture inside | Effect extends BEYOND text |
| 6 | Rotate +90 CW + Wind right ×5 = UP | Same mistake as #4 | -90 CCW + Wind left = DOWN |
| 7 | Too short/thin/wrong color/wavy | Insufficient passes + bad params | 5-7× "wind" method, not "blast" |
| 8 | White on TRANSPARENT + SCREEN | Colors invisible | White on BLACK + SCREEN |
| 9 | Wind "blast" ×10 = off-canvas | blast too aggressive + too many | "wind" method × 5-7 |

---

# §13 OUTER GLOW COMPLETE PARAMETER REFERENCE

For batchplay or understanding tool parameters:

| Parameter | Range | Default | Notes |
|-----------|-------|---------|-------|
| BlendMode | any | SCREEN | SCREEN for glow, MULTIPLY for dark halo |
| Opacity | 0-100% | 75 | |
| Noise | 0-100% | 0 | Adds texture to glow |
| Color | RGB or Gradient | yellow | Single color or gradient glow |
| Technique | Softer / Precise | Softer | Precise = hard-edged glow |
| Spread | 0-100% | 0 | Higher = more solid center |
| Size | 0-250px | 5 | Blur radius of glow |
| Contour | preset curves | Linear | Shapes the falloff |
| Range | 1-100% | 50 | Which tonal range gets glow |
| Jitter | 0-100% | 0 | Randomizes gradient glow |

---

# §14 QUALITY CHECKLIST

Before finalizing ANY design:

- [ ] Text is readable at target viewing distance
- [ ] Color palette has max 3-5 colors (60-30-10 rule)
- [ ] Visual hierarchy is clear (title → image → details)
- [ ] White space is sufficient
- [ ] All effects look intentional (not overdone)
- [ ] Alignment is pixel-perfect
- [ ] Export format matches use case (PNG=transparency, JPG=photos, PSD=editing)
- [ ] No artifacts from filter operations
- [ ] Layer order is logical (bg → subject → text → effects → adjustments)
- [ ] Color grading is consistent across all elements
- [ ] Canvas dimensions match target platform

---

# §15 BATCHPLAY PRO TIPS

**Record your own descriptors:**
1. Open Photoshop Actions panel
2. Record the effect manually
3. Panel flyout → "Copy As JavaScript"
4. Gives exact descriptor you can paste into `execute_batchplay`

**Action listener (captures descriptors in real-time):**
```javascript
action.addNotificationListener(['all'], (event, descriptor) => { console.log(event, descriptor); });
```

**UXP Photoshop API docs (Chinese):** kihlh.github.io/uxp-photoshop-zh-cn
