---
name: ps-batchplay
description: "BatchPlay/batchplay reference for Photoshop MCP execute_batchplay tool. Descriptor format, reference forms (by ID, active layer, document, channel), unit types (pixels, percent, angle, density), operations requiring batchplay (lighting effects, VIVID_LIGHT blend mode, select layer by ID, invert pixels), filter scriptability table, event code table for all filter categories, pro tips for recording descriptors and action listener."
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# §4 BATCHPLAY REFERENCE

Use this section ONLY when no dedicated tool exists for your operation (Rule R7).

## 4.1 DESCRIPTOR FORMAT

```javascript
[
  {
    _obj: "commandName", // Event string code (required)
    _target: [{ _ref: "layer", _id: 5 }], // Target (optional)
    paramName: value, // Simple value
    enumParam: { _enum: "enumType", _value: "enumValue" }, // Enum
    unitParam: { _unit: "pixelsUnit", _value: 10.0 }, // Unit value
  },
];
```

## 4.2 REFERENCE FORMS

```javascript
{_ref: "layer", _id: 42}                                    // By ID (best)
{_ref: "layer", _enum: "ordinal", _value: "targetEnum"}     // Active layer
{_ref: "document", _enum: "ordinal", _value: "targetEnum"}  // Active document
{_ref: "channel", _enum: "channel", _value: "RGB"}          // RGB composite
```

## 4.3 UNIT TYPES

```javascript
{_unit: "pixelsUnit", _value: 10}      // Pixels
{_unit: "percentUnit", _value: 50}     // Percentage
{_unit: "angleUnit", _value: 90}       // Degrees
{_unit: "densityUnit", _value: 72}     // PPI
```

## 4.4 OPERATIONS THAT STILL NEED BATCHPLAY

These operations have NO dedicated tool — use execute_batchplay:

**Lighting Effects:**

```json
[
  {
    "_obj": "lightingEffects",
    "lightList": [
      {
        "_obj": "lightSource",
        "lightType": { "_enum": "lightType", "_value": "spotLight" },
        "intensity": 50,
        "focus": 60,
        "posX": 500,
        "posY": 300
      }
    ]
  }
]
```

**VIVID_LIGHT blend mode** (not supported by set_layer_properties):

```json
[
  {
    "_obj": "set",
    "_target": [
      { "_ref": "layer", "_enum": "ordinal", "_value": "targetEnum" }
    ],
    "to": {
      "_obj": "layer",
      "mode": { "_enum": "blendMode", "_value": "vividLight" }
    }
  }
]
```

**Select layer by ID:**

```json
[
  {
    "_obj": "select",
    "_target": [{ "_ref": "layer", "_id": 42 }],
    "makeVisible": false
  }
]
```

**Invert layer pixels (not selection):**

```json
[{ "_obj": "invert" }]
```

## 4.5 FILTER SCRIPTABILITY TABLE

| Filter               | Headless (no dialog) | Notes                                             |
| -------------------- | -------------------- | ------------------------------------------------- |
| All standard filters | Yes                  | gaussianBlur, wave, wind, etc.                    |
| Blur Gallery         | May force dialog     | Known Adobe bug                                   |
| Camera Raw Filter    | No                   | Always requires dialog. Use Curves/Levels instead |
| Liquify (full mesh)  | No                   | Only `liquify_forward` works headless             |
| Neural Filters       | No                   | Cloud-based, requires dialog                      |

## 4.6 EVENT CODE TABLE

**Blur:** gaussianBlur, motionBlur, radialBlur, smartBlur, surfaceBlur, lensBlur, blurbTransform
**Distort:** wave, twirl, spherize, polar, ripple, oceanRipple, pinch, shear, zigZag, displace, glass
**Stylize:** wind, emboss, findEdges, diffuse, diffuseGlow, glowingEdges, tiles, extrude, solarize
**Sketch:** chrome, basRelief, chalkCharcoal, charcoal, photocopy, stamp, tornEdges, waterPaper, notePaper, plaster, reticulation, halftonePattern, graphicPen
**Artistic:** plasticWrap, dryBrush, filmGrain, fresco, neonGlow, paletteKnife, paintDaubs, roughPastels, smudgeStick, sponge, underpainting, watercolor, posterEdges, coloredPencil, cutout
**Noise:** addNoise, despeckle, dustAndScratches, median, reduceNoise
**Sharpen:** sharpen, unsharpMask, highPass, smartSharpen
**Render:** clouds, $DrfC (diff clouds), lensFlare, fibers/$Fbrs
**Texture:** craquelure, grain, mosaicPlugin, patchwork, stainedGlass, texturizer
**Pixelate:** colorHalftone, crystallize, facet, fragment, mezzotint, mosaic, pointillize
**Brush Strokes:** accentedEdges, angledStrokes, crosshatch, darkStrokes, inkOutlines, spatter, sprayedStrokes, sumi_e
**Operations:** make, set, get, delete, select, move, duplicate, hide, show, transform, crop, canvasSize, imageSize
**Adjustments:** curves, levels, hueSaturation, colorBalance, brightnessEvent, channelMixer, selectiveColor, posterization, thresholdClassEvent, invert, desaturate, gradientMapEvent

---

# §16 BATCHPLAY PRO TIPS

**Record your own descriptors:**

1. Open Photoshop Actions panel
2. Record the effect manually
3. Panel flyout → "Copy As JavaScript"
4. Gives exact descriptor for `execute_batchplay`

**Action listener (captures descriptors in real-time):**

```javascript
action.addNotificationListener(["all"], (event, descriptor) => {
  console.log(event, descriptor);
});
```

---
