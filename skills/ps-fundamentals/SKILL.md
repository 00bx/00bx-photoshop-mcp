---
name: ps-fundamentals
description: "Photoshop MCP mandatory workflow rules (R1-R7), coordinate system, layer stack order, canvas rotation, selection fundamentals, mask fundamentals (white=visible black=hidden), smart objects vs rasterized layers, fill opacity vs layer opacity. LOAD THIS FIRST for any Photoshop operation."
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# PHOTOSHOP DESIGNER SKILL — FUNDAMENTALS & RULES

Execute ANY Photoshop design effect perfectly on first try — zero trial-and-error.

## WHEN TO USE THIS SKILL

Load this skill FIRST for any Photoshop operation. It contains the mandatory rules and core concepts needed before using any other Photoshop skill.

---

# MANDATORY WORKFLOW RULES

<rules>
<rule id="R1" severity="CRITICAL">
ALWAYS use a DEDICATED TOOL when one exists. NEVER use execute_batchplay for an operation that has its own tool.
There are 323 dedicated tools. Check this catalog FIRST.
</rule>

<rule id="R2" severity="CRITICAL">
ALWAYS verify visual results after multi-step operations using get_layer_image (single layer) or get_document_image (full composite).
Do NOT assume success from return status alone.
</rule>

<rule id="R3" severity="CRITICAL">
ALWAYS pass layer_id when calling execute_batchplay. The tool has an optional layer_id parameter that ensures the correct layer is targeted.
Without it, batchPlay may silently operate on the wrong layer.
</rule>

<rule id="R4" severity="HIGH">
For ROUNDED CORNERS on any element: use draw_rectangle_shape(corner_radius=N) + set_layer_properties(is_clipping_mask=true).
Do NOT attempt rounded rect selections via batchPlay — the corner radius keys are unreliable.
</rule>

<rule id="R5" severity="HIGH">
RASTERIZE layers before applying filters. Text, Shape, and Smart Object layers will fail silently with most filters.
Always duplicate_layer first (preserve original), then rasterize_layer on the copy.
</rule>

<rule id="R6" severity="HIGH">
SCREEN blend mode requires BLACK background, not transparent.
White on TRANSPARENT + SCREEN = invisible. White on BLACK + SCREEN = correct.
</rule>

<rule id="R7" severity="MEDIUM">
execute_batchplay is the LAST RESORT escape hatch. Use it only when:
- No dedicated tool exists for the operation
- You need to combine multiple atomic operations in one call
- A dedicated tool has a known limitation for a specific parameter
</rule>
</rules>

---

# §1 FUNDAMENTALS

## 1.1 COORDINATE SYSTEM

- Origin (0,0) = **top-left** corner of canvas
- X increases RIGHT, Y increases DOWN
- Layer bounds: `{left, top, right, bottom}` in pixels from origin
- Center of canvas: `(width/2, height/2)`

## 1.2 LAYER STACK ORDER

- Layers are drawn **bottom-up** — bottom layer renders first, top layer renders last
- `move_layer(position="TOP")` = above all (visually on top)
- `move_layer(position="BOTTOM")` = below all (visually behind)
- New layers appear ABOVE the currently active layer
- **Adjustment layers affect ALL layers below them** unless clipped

## 1.3 CANVAS ROTATION RULES

- `rotate_canvas` rotates the **entire document** including all layers
- Rotation is **destructive** — pixels are resampled
- Always rotate back by the exact negative amount
- **Plan filter directions BEFORE rotating** — see Wind direction table §7.2

## 1.4 SELECTION FUNDAMENTALS

- Selection = marching ants defining which pixels are affected
- Feather = soft edges (pixels partially selected)
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

## 1.7 FILL OPACITY vs LAYER OPACITY

- **Layer Opacity** = affects layer content + ALL layer styles
- **Fill Opacity** = affects ONLY layer content, NOT layer styles (drop shadow, glow, bevel stay at full)
- **Key trick:** Fill 0% + layer styles = invisible content with visible effects (used for glass text)
- Set via: `set_layer_properties(layer_id=X, fill_opacity=0)`

---
