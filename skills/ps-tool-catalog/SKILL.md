---
name: ps-tool-catalog
description: "Complete catalog of all 323 dedicated Photoshop MCP tools across 36 categories: document operations, layer operations, layer masks, text, selections (30 tools), clipboard, channels, transforms, shapes, painting/drawing, layer styles, adjustment layers (17), direct adjustments, filters (blur 14, sharpen 3, noise 5, distort 12, stylize 10, artistic 14, sketch 12, brush strokes 8, texture 5, pixelate 7, render 4, other 4, special 2), generative AI, paths, color tools, guides, smart objects, document profiles, actions/automation, advanced operations, utility/history/view, and execute_batchplay escape hatch."
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: photoshop-mcp
---

# §3 COMPLETE TOOL CATALOG (323 Tools)

<tool-catalog>
Every tool listed below is a DEDICATED MCP tool. Use these INSTEAD of execute_batchplay.

## 3.1 DOCUMENT OPERATIONS (22 tools)

| Tool                         | Purpose                         | Key Parameters                                    |
| ---------------------------- | ------------------------------- | ------------------------------------------------- |
| `create_document`            | New PSD                         | width, height, resolution, fill_color, color_mode |
| `get_documents`              | List open docs                  | —                                                 |
| `set_active_document`        | Switch active doc               | document_id                                       |
| `get_document_info`          | Doc dimensions/DPI/path         | —                                                 |
| `get_document_image`         | JPEG preview of full doc        | —                                                 |
| `save_document_image_as_png` | Save doc preview as PNG         | file_path                                         |
| `save_document`              | Save current doc                | —                                                 |
| `save_document_as`           | Save as PSD/PNG/JPG             | file_path, file_type                              |
| `open_photoshop_file`        | Open file in PS                 | file_path                                         |
| `duplicate_document`         | Copy entire doc                 | document_name                                     |
| `crop_document`              | Crop to selection               | (requires active selection)                       |
| `resize_image`               | Image Size                      | width, height, resolution, constrain              |
| `resize_canvas`              | Canvas Size (no scaling)        | width, height, anchor, color                      |
| `rotate_canvas`              | Rotate entire doc               | angle                                             |
| `trim_document`              | Trim transparent/colored edges  | trim_type, top/left/bottom/right                  |
| `reveal_all`                 | Expand canvas to fit all layers | —                                                 |
| `flatten_all_layers`         | Flatten to single layer         | layer_name                                        |
| `merge_visible`              | Merge visible layers            | —                                                 |
| `merge_down`                 | Merge layer with one below      | layer_id                                          |
| `merge_layers`               | Merge specific layers           | layer_ids[]                                       |
| `stamp_visible`              | Flattened copy as new layer     | —                                                 |
| `export_layers_as_png`       | Export layers as PNG files      | layers_info[]                                     |

## 3.2 LAYER OPERATIONS (26 tools)

| Tool                              | Purpose                         | Key Parameters                                                            |
| --------------------------------- | ------------------------------- | ------------------------------------------------------------------------- |
| `get_layers`                      | List all layers + hierarchy     | —                                                                         |
| `get_layer_image`                 | JPEG preview of single layer    | layer_id                                                                  |
| `get_layer_bounds`                | Layer pixel bounds              | layer_id                                                                  |
| `create_pixel_layer`              | New empty pixel layer           | layer_name, fill_neutral, opacity, blend_mode                             |
| `delete_layer`                    | Delete layer                    | layer_id                                                                  |
| `duplicate_layer`                 | Copy layer                      | layer_to_duplicate_id, duplicate_layer_name                               |
| `rename_layers`                   | Rename one or more layers       | layer_data[]                                                              |
| `set_layer_visibility`            | Show/hide layer                 | layer_id, visible                                                         |
| `set_layer_properties`            | Blend mode, opacity, fill, clip | layer_id, blend_mode, layer_opacity, fill_opacity, is_clipping_mask       |
| `move_layer`                      | Reorder in stack                | layer_id, position (TOP/BOTTOM/UP/DOWN)                                   |
| `group_layers`                    | Create group from layers        | group_name, layer_ids[]                                                   |
| `ungroup_layers`                  | Dissolve a group                | (batchPlay-based)                                                         |
| `rasterize_layer`                 | Rasterize to pixels             | layer_id                                                                  |
| `rasterize_all_layers`            | Rasterize entire doc            | —                                                                         |
| `convert_to_smart_object`         | Layer → Smart Object            | layer_id                                                                  |
| `select_layer`                    | Make layer active               | layer_id                                                                  |
| `place_image`                     | Place image onto layer          | layer_id, image_path                                                      |
| `harmonize_layer`                 | Match lighting to bg            | layer_id, new_layer_name                                                  |
| `remove_background`               | Auto remove bg                  | layer_id                                                                  |
| `add_solid_color_fill_layer`      | Solid color fill layer          | color_red/green/blue                                                      |
| `set_layer_blend_if`              | Blend If sliders                | layer_id, this_layer_black/white, underlying_black/white + feather points |
| `toggle_layer_effects_visibility` | Show/hide layer effects         | —                                                                         |
| `create_layer_from_effects`       | Convert effects to layers       | —                                                                         |
| `select_linked_layers`            | Select all linked layers        | —                                                                         |
| `apply_auto_blend_layers`         | Auto-blend (panorama/stack)     | —                                                                         |
| `apply_auto_align_layers`         | Auto-align layers               | —                                                                         |

## 3.3 LAYER MASKS (7 tools)

| Tool                            | Purpose                          |
| ------------------------------- | -------------------------------- |
| `add_layer_mask_from_selection` | Mask from active selection       |
| `add_layer_mask_reveal_all`     | White mask (show all)            |
| `add_layer_mask_hide_all`       | Black mask (hide all)            |
| `remove_layer_mask`             | Delete mask                      |
| `select_layer_mask`             | Target mask for editing          |
| `select_layer_rgb`              | Target pixels (back from mask)   |
| `fill_mask_with_gradient`       | Gradient on mask for transitions |

## 3.4 TEXT (3 tools)

| Tool                            | Purpose             | Key Parameters                                                          |
| ------------------------------- | ------------------- | ----------------------------------------------------------------------- |
| `create_single_line_text_layer` | Single line text    | layer_name, text, font_size, postscript_font_name, text_color, position |
| `create_multi_line_text_layer`  | Multi-line text box | + bounds, justification                                                 |
| `edit_text_layer`               | Edit existing text  | layer_id, text, font_size, postscript_font_name, text_color             |

## 3.5 SELECTIONS (30 tools)

**Basic Selections:**
| Tool | Purpose |
|------|---------|
| `select_rectangle` | Rectangular selection |
| `select_ellipse` | Elliptical selection |
| `select_polygon` | N-sided polygon selection |
| `select_all` | Select entire canvas |
| `clear_selection` | Deselect all |

**Intelligent Selections:**
| Tool | Purpose |
|------|---------|
| `select_subject` | AI subject detection |
| `select_sky` | AI sky detection |
| `select_object` | Object Selection auto-detect |
| `select_by_quick_selection` | Quick Selection tool |
| `select_color_range` | Select by color + fuzziness |
| `select_focus_area` | Select in-focus areas |
| `select_by_magic_wand` | Magic wand by tolerance |

**Selection Modifiers:**
| Tool | Purpose |
|------|---------|
| `invert_selection` | Invert selection |
| `grow_selection` | Grow to adjacent similar |
| `similar_selection` | Select all similar pixels |
| `expand_selection` | Expand by N pixels |
| `contract_selection` | Contract by N pixels |
| `feather_selection` | Soften edges |
| `smooth_selection` | Smooth edges |
| `border_selection` | Create border from selection |
| `transform_selection` | Scale/rotate selection only |

**Compound Selections (add/subtract):**
| Tool | Purpose |
|------|---------|
| `add_to_selection_rectangle` | Add rect to existing selection |
| `subtract_from_selection_rectangle` | Subtract rect from selection |
| `intersect_selection_rectangle` | Intersect rect with selection |
| `add_to_selection_ellipse` | Add ellipse to selection |
| `subtract_from_selection_ellipse` | Subtract ellipse from selection |
| `add_to_selection_polygon` | Add polygon to selection |
| `subtract_from_selection_polygon` | Subtract polygon from selection |

**Selection Content Operations:**
| Tool | Purpose |
|------|---------|
| `fill_selection` | Fill selection with color |
| `delete_selection` | Delete pixels in selection |
| `content_aware_fill` | AI content-aware fill |

## 3.6 CLIPBOARD (4 tools)

| Tool                                 | Purpose                  |
| ------------------------------------ | ------------------------ |
| `copy_selection_to_clipboard`        | Copy from one layer      |
| `copy_merged_selection_to_clipboard` | Copy from all visible    |
| `cut_selection_to_clipboard`         | Cut from layer           |
| `paste_from_clipboard`               | Paste clipboard contents |

## 3.7 CHANNELS (7 tools)

| Tool                          | Purpose                                                |
| ----------------------------- | ------------------------------------------------------ |
| `save_selection_as_channel`   | Save selection as alpha                                |
| `load_selection_from_channel` | Load selection from alpha                              |
| `delete_channel`              | Delete alpha channel                                   |
| `split_channels`              | Split into separate docs                               |
| `merge_channels`              | Merge channel docs back                                |
| `duplicate_channel`           | Duplicate a channel                                    |
| `set_channel_restrictions`    | Restrict editing to specific channels (glitch effects) |

## 3.8 TRANSFORMS (10 tools)

| Tool                          | Purpose                         | Key Parameters                                                 |
| ----------------------------- | ------------------------------- | -------------------------------------------------------------- |
| `scale_layer`                 | Scale by percentage             | layer_id, width, height, anchor_position                       |
| `rotate_layer`                | Rotate layer                    | layer_id, angle, anchor_position                               |
| `flip_layer`                  | Flip horizontal/vertical        | layer_id, axis                                                 |
| `translate_layer`             | Move by offset                  | layer_id, x_offset, y_offset                                   |
| `set_layer_position_absolute` | Move to exact x,y               | layer_id, x, y                                                 |
| `free_transform`              | Combined scale+rotate+skew+move | layer_id, width, height, angle, skew_x, skew_y, move_x, move_y |
| `perspective_transform`       | 4-corner perspective            | layer_id, top_left/right_x/y, bottom_left/right_x/y            |
| `warp_transform`              | Preset warp styles              | layer_id, warp_style, bend, h/v_distortion                     |
| `content_aware_scale`         | Intelligent resize              | layer_id, width, height                                        |
| `apply_skew`                  | Skew transform                  | (batchPlay-based)                                              |

## 3.9 SHAPES (6 tools)

| Tool                   | Purpose                | Key Parameters                            |
| ---------------------- | ---------------------- | ----------------------------------------- |
| `draw_rectangle_shape` | Rectangle/rounded rect | bounds, fill_color, stroke, corner_radius |
| `draw_ellipse_shape`   | Ellipse/circle         | bounds, fill_color, stroke                |
| `draw_line_shape`      | Line                   | start/end coords, stroke                  |
| `draw_arrow_shape`     | Arrow with head        | start/end, head_size                      |
| `draw_polygon_shape`   | Regular polygon        | sides, center, radius                     |
| `draw_custom_path`     | Bezier path shape      | points[] (with optional handles)          |

## 3.10 PAINTING & DRAWING (13 tools)

| Tool                       | Purpose                  | Key Parameters                                                 |
| -------------------------- | ------------------------ | -------------------------------------------------------------- |
| `brush_stroke`             | Paint along path         | layer_id, points[], brush_size, color, opacity, hardness, flow |
| `eraser_stroke`            | Erase along path         | layer_id, points[], brush_size, opacity                        |
| `gradient_draw`            | Draw gradient on layer   | layer_id, start/end coords, gradient_type, color_stops         |
| `paint_bucket_fill`        | Flood fill               | layer_id, x, y, color, tolerance, contiguous                   |
| `apply_dodge_tool`         | Lighten areas            | (batchPlay-based)                                              |
| `apply_burn_tool`          | Darken areas             | (batchPlay-based)                                              |
| `apply_smudge_tool`        | Smudge pixels            | (batchPlay-based)                                              |
| `apply_clone_stamp`        | Clone from source point  | layer_id, source/dest coords, brush_size                       |
| `apply_healing_brush`      | Healing with blending    | layer_id, source/dest coords                                   |
| `apply_spot_healing_brush` | Auto blemish removal     | layer_id, points[], brush_size                                 |
| `apply_history_brush`      | Paint from history state | layer_id, points[], brush_size                                 |
| `apply_pattern_stamp`      | Paint with pattern       | layer_id, points[], brush_size                                 |
| `apply_mixer_brush`        | Realistic paint mixing   | layer_id, points[], brush_size, wetness, mix                   |

## 3.11 LAYER STYLES (11 tools)

| Tool                               | Purpose              |
| ---------------------------------- | -------------------- |
| `add_drop_shadow_layer_style`      | Drop shadow          |
| `add_inner_shadow_layer_style`     | Inner shadow         |
| `add_outer_glow_layer_style`       | Outer glow           |
| `add_inner_glow_layer_style`       | Inner glow           |
| `add_bevel_emboss_layer_style`     | Bevel & Emboss       |
| `add_satin_layer_style`            | Satin effect         |
| `add_color_overlay_layer_style`    | Color overlay        |
| `add_gradient_overlay_layer_style` | Gradient overlay     |
| `add_stroke_layer_style`           | Stroke               |
| `create_gradient_layer_style`      | Gradient layer style |
| `clear_layer_styles`               | Remove all styles    |

## 3.12 ADJUSTMENT LAYERS (17 tools)

| Tool                                       | Purpose                          |
| ------------------------------------------ | -------------------------------- |
| `add_brightness_contrast_adjustment_layer` | Brightness/Contrast              |
| `add_levels_adjustment_layer`              | Levels (shadows/mids/highlights) |
| `add_curves_adjustment_layer`              | Curves (per-channel control)     |
| `add_exposure_adjustment_layer`            | Exposure/Offset/Gamma            |
| `add_vibrance_adjustment_layer`            | Vibrance/Saturation              |
| `add_hue_saturation_adjustment_layer`      | Hue/Saturation/Lightness         |
| `add_color_balance_adjustment_layer`       | Color Balance                    |
| `add_photo_filter_adjustment_layer`        | Photo Filter (warming/cooling)   |
| `add_channel_mixer_adjustment_layer`       | Channel Mixer                    |
| `add_selective_color_adjustment_layer`     | Selective Color                  |
| `add_gradient_map_adjustment_layer`        | Gradient Map (duotone etc.)      |
| `add_black_and_white_adjustment_layer`     | B&W conversion                   |
| `add_posterize_adjustment_layer`           | Posterize                        |
| `add_threshold_adjustment_layer`           | Threshold                        |
| `add_invert_adjustment_layer`              | Invert colors                    |
| `add_color_lookup_adjustment_layer`        | Color Lookup / LUT               |
| `shadows_highlights`                       | Shadows/Highlights recovery      |

## 3.13 DIRECT ADJUSTMENTS (10 tools)

| Tool                     | Purpose                    |
| ------------------------ | -------------------------- |
| `auto_tone`              | Auto tonal correction      |
| `auto_color`             | Auto color correction      |
| `auto_contrast`          | Auto contrast correction   |
| `apply_desaturate`       | Remove all color           |
| `apply_equalize`         | Equalize histogram         |
| `apply_invert_image`     | Invert entire image        |
| `apply_posterize_direct` | Direct posterize           |
| `apply_threshold_direct` | Direct threshold           |
| `apply_match_color`      | Match color between images |
| `apply_replace_color`    | Replace specific colors    |

## 3.14 FILTERS — BLUR (14 tools)

| Tool                    | Purpose                        | Key Parameters                         |
| ----------------------- | ------------------------------ | -------------------------------------- |
| `apply_gaussian_blur`   | Standard blur                  | radius (0.1-10000)                     |
| `apply_motion_blur`     | Directional motion             | angle, distance                        |
| `apply_radial_blur`     | Spin or zoom blur              | amount, method (spin/zoom), quality    |
| `apply_surface_blur`    | Blur preserving edges          | radius, threshold                      |
| `apply_lens_blur`       | Bokeh/DOF blur                 | radius, brightness, threshold          |
| `apply_smart_blur`      | Edge-aware blur                | (batchPlay-based)                      |
| `apply_box_blur`        | Simple box average             | (batchPlay-based)                      |
| `apply_shape_blur`      | Shape-kernel blur              | (batchPlay-based)                      |
| `apply_average_blur`    | Average color of area          | (batchPlay-based)                      |
| `apply_field_blur`      | Blur Gallery: field            | (batchPlay-based)                      |
| `apply_iris_blur`       | Blur Gallery: iris/elliptical  | center_x/y, blur_amount                |
| `apply_tilt_shift_blur` | Blur Gallery: tilt-shift       | blur_amount, focus_top/bottom, feather |
| `apply_spin_blur`       | Blur Gallery: rotational       | center_x/y, spin_angle                 |
| `apply_path_blur`       | Blur Gallery: directional path | speed, path points                     |

## 3.15 FILTERS — SHARPEN (3 tools)

| Tool                  | Purpose       | Key Parameters                                       |
| --------------------- | ------------- | ---------------------------------------------------- |
| `apply_sharpen`       | Basic sharpen | —                                                    |
| `apply_unsharp_mask`  | Unsharp Mask  | amount (1-500), radius (0.1-1000), threshold (0-255) |
| `apply_smart_sharpen` | Smart Sharpen | amount, radius, noise_reduction, remove_type         |

## 3.16 FILTERS — NOISE (5 tools)

| Tool                       | Purpose                  | Key Parameters                                |
| -------------------------- | ------------------------ | --------------------------------------------- |
| `apply_noise`              | Add noise                | amount (0.1-400), distribution, monochromatic |
| `apply_despeckle`          | Remove speckle noise     | —                                             |
| `apply_median_noise`       | Median filter            | radius                                        |
| `apply_dust_and_scratches` | Remove dust/scratches    | radius, threshold                             |
| `apply_reduce_noise`       | Advanced noise reduction | (batchPlay-based)                             |

## 3.17 FILTERS — DISTORT (12 tools)

| Tool                       | Purpose              | Key Parameters                           |
| -------------------------- | -------------------- | ---------------------------------------- |
| `apply_twirl_distortion`   | Twirl/spiral         | angle (-999 to 999)                      |
| `apply_zig_zag_distortion` | ZigZag/ripple pond   | amount, ridges, style                    |
| `apply_wave`               | Wave distortion      | generators, wavelength, amplitude, type  |
| `apply_ripple`             | Ripple               | amount, size                             |
| `apply_ocean_ripple`       | Ocean water surface  | ripple_size, ripple_magnitude            |
| `apply_sphere`             | Spherize             | amount (-100 to 100), mode               |
| `apply_pinch`              | Pinch inward/outward | amount (-100 to 100)                     |
| `apply_polar_coordinates`  | Polar conversion     | conversion type                          |
| `apply_shear`              | Shear along curve    | points[], undefined_area                 |
| `apply_displace`           | Displacement map     | h/v_scale, stretch_to_fit, wrap_around   |
| `apply_glass_distortion`   | Glass refraction     | distortion, smoothness, texture, scaling |
| `liquify_forward`          | Liquify push         | start/end coords, brush_size, pressure   |

## 3.18 FILTERS — STYLIZE (10 tools)

| Tool                  | Purpose                    | Key Parameters                                      |
| --------------------- | -------------------------- | --------------------------------------------------- |
| `apply_wind`          | Wind streaks               | method (wind/blast/stagger), direction (left/right) |
| `apply_emboss`        | Emboss 3D relief           | angle, height, amount                               |
| `apply_find_edges`    | Edge detection             | —                                                   |
| `apply_solarize`      | Solarization               | —                                                   |
| `apply_diffuse_glow`  | Soft glow effect           | graininess, glow_amount, clear_amount               |
| `apply_glowing_edges` | Neon edge glow             | edge_width, edge_brightness, smoothness             |
| `apply_diffuse`       | Diffuse scatter            | mode                                                |
| `apply_tiles`         | Tile segments              | tile_count, offset                                  |
| `apply_trace_contour` | Trace contour lines        | level, edge                                         |
| `apply_extrude`       | 3D extrude blocks/pyramids | type, size, depth                                   |

## 3.19 FILTERS — ARTISTIC (14 tools)

| Tool                   | Purpose               |
| ---------------------- | --------------------- |
| `apply_colored_pencil` | Colored pencil sketch |
| `apply_cutout`         | Paper cutout poster   |
| `apply_dry_brush`      | Dry brush painting    |
| `apply_film_grain`     | Film grain texture    |
| `apply_fresco`         | Fresco painting       |
| `apply_neon_glow`      | Neon glow filter      |
| `apply_paint_daubs`    | Paint daubs           |
| `apply_palette_knife`  | Palette knife strokes |
| `apply_poster_edges`   | Posterize with edges  |
| `apply_rough_pastels`  | Rough pastel texture  |
| `apply_smudge_stick`   | Smudge stick effect   |
| `apply_sponge_filter`  | Sponge texture        |
| `apply_underpainting`  | Underpainting base    |
| `apply_watercolor`     | Watercolor painting   |

## 3.20 FILTERS — SKETCH (12 tools)

| Tool                       | Purpose                   |
| -------------------------- | ------------------------- |
| `apply_bas_relief`         | Bas relief carving        |
| `apply_chalk_and_charcoal` | Chalk & charcoal drawing  |
| `apply_charcoal`           | Charcoal sketch           |
| `apply_graphic_pen`        | Graphic pen strokes       |
| `apply_halftone_pattern`   | Halftone dot/line pattern |
| `apply_note_paper`         | Note paper texture        |
| `apply_photocopy`          | Photocopy effect          |
| `apply_plaster`            | Plaster relief            |
| `apply_reticulation`       | Film reticulation         |
| `apply_stamp_filter`       | Rubber stamp              |
| `apply_torn_edges`         | Torn paper edges          |
| `apply_water_paper`        | Water paper texture       |

## 3.21 FILTERS — BRUSH STROKES (8 tools)

| Tool                    | Purpose                     |
| ----------------------- | --------------------------- |
| `apply_accented_edges`  | Accented edge strokes       |
| `apply_angled_strokes`  | Angled brush strokes        |
| `apply_crosshatch`      | Crosshatch drawing          |
| `apply_dark_strokes`    | Dark ink strokes            |
| `apply_ink_outlines`    | Ink outline drawing         |
| `apply_spatter`         | Spatter spray               |
| `apply_sprayed_strokes` | Sprayed directional strokes |
| `apply_sumi_e`          | Japanese ink painting       |

## 3.22 FILTERS — TEXTURE (5 tools)

| Tool                  | Purpose               |
| --------------------- | --------------------- |
| `apply_craquelure`    | Cracked surface       |
| `apply_grain`         | Film/texture grain    |
| `apply_patchwork`     | Patchwork squares     |
| `apply_stained_glass` | Stained glass cells   |
| `apply_texturizer`    | Apply surface texture |

## 3.23 FILTERS — PIXELATE (7 tools)

| Tool                   | Purpose            | Key Parameters     |
| ---------------------- | ------------------ | ------------------ |
| `apply_pixelate`       | Mosaic squares     | cell_size          |
| `apply_crystallize`    | Crystal polygons   | cell_size          |
| `apply_color_halftone` | CMYK halftone dots | max_radius, angles |
| `apply_facet`          | Facet clumps       | —                  |
| `apply_fragment`       | Fragment copies    | —                  |
| `apply_mezzotint`      | Mezzotint pattern  | type               |
| `apply_pointillize`    | Pointillist dots   | cell_size          |

## 3.24 FILTERS — RENDER (4 tools)

| Tool                      | Purpose           | Key Parameters                |
| ------------------------- | ----------------- | ----------------------------- |
| `apply_clouds`            | Render clouds     | (uses fg/bg colors)           |
| `apply_difference_clouds` | Difference clouds | (uses fg/bg colors)           |
| `apply_fibers`            | Render fibers     | variance, strength            |
| `apply_lens_flare`        | Lens flare        | brightness, center, lens_type |

## 3.25 FILTERS — OTHER (4 tools)

| Tool                  | Purpose                  |
| --------------------- | ------------------------ |
| `apply_maximum`       | Maximum (expand whites)  |
| `apply_minimum`       | Minimum (expand blacks)  |
| `apply_offset_filter` | Offset/tile filter       |
| `apply_high_pass`     | High-pass for sharpening |

## 3.26 FILTERS — SPECIAL (2 tools)

| Tool                  | Purpose                 | Key Parameters                         |
| --------------------- | ----------------------- | -------------------------------------- |
| `apply_plastic_wrap`  | Liquid/wet plastic look | highlight_strength, detail, smoothness |
| `apply_chrome_filter` | Chrome/metallic look    | detail, smoothness                     |

## 3.27 GENERATIVE AI (2 tools)

| Tool              | Purpose                            |
| ----------------- | ---------------------------------- |
| `generate_image`  | AI image generation (Firefly)      |
| `generative_fill` | AI fill within selection (Firefly) |

## 3.28 PATHS (5 tools)

| Tool                | Purpose                   |
| ------------------- | ------------------------- |
| `stroke_path`       | Stroke along path         |
| `fill_path`         | Fill path area            |
| `path_to_selection` | Convert path to selection |
| `selection_to_path` | Convert selection to path |
| `delete_path`       | Delete work path          |

## 3.29 COLOR TOOLS (3 tools)

| Tool                   | Purpose                         |
| ---------------------- | ------------------------------- |
| `set_foreground_color` | Set FG color (red, green, blue) |
| `set_background_color` | Set BG color                    |
| `swap_colors`          | Swap FG/BG                      |

## 3.30 GUIDES (2 tools)

| Tool               | Purpose           |
| ------------------ | ----------------- |
| `add_guide`        | Add ruler guide   |
| `clear_all_guides` | Remove all guides |

## 3.31 SMART OBJECT & LAYER TYPE (3 tools)

| Tool                            | Purpose                    |
| ------------------------------- | -------------------------- |
| `replace_smart_object_contents` | Replace SO from file       |
| `rasterize_all_layers`          | Rasterize entire doc       |
| `convert_layer_to_frame`        | Convert to animation frame |

## 3.32 DOCUMENT & PROFILE (5 tools)

| Tool                     | Purpose                       |
| ------------------------ | ----------------------------- |
| `assign_icc_profile`     | Assign ICC without conversion |
| `convert_to_icc_profile` | Convert colors to new profile |
| `define_brush_preset`    | Create brush from selection   |
| `apply_image_composite`  | Apply Image (freq separation) |
| `calculations`           | Image > Calculations          |

## 3.33 ACTIONS & AUTOMATION (3 tools)

| Tool                  | Purpose              |
| --------------------- | -------------------- |
| `play_action`         | Play recorded action |
| `record_action_start` | Start recording      |
| `record_action_stop`  | Stop recording       |

## 3.34 ADVANCED OPERATIONS (2 tools)

| Tool                 | Purpose                      |
| -------------------- | ---------------------------- |
| `content_aware_fill` | AI fill (requires selection) |
| `lens_correction`    | Distortion/vignette/CA fix   |

## 3.35 UTILITY / HISTORY / VIEW (16 tools)

| Tool                              | Purpose                   |
| --------------------------------- | ------------------------- |
| `undo`                            | Undo last action          |
| `redo`                            | Redo last undo            |
| `step_backward`                   | Step backward in history  |
| `step_forward`                    | Step forward in history   |
| `fade_last_filter`                | Fade last filter effect   |
| `purge_all`                       | Purge clipboard/history   |
| `create_snapshot`                 | Create history snapshot   |
| `set_ruler_units`                 | Set ruler unit type       |
| `fit_on_screen`                   | Fit view to screen        |
| `zoom_to_100`                     | 100% actual pixels        |
| `toggle_layer_effects_visibility` | Show/hide layer effects   |
| `create_layer_from_effects`       | Convert effects to layers |
| `ungroup_layers`                  | Dissolve group            |
| `select_linked_layers`            | Select linked layers      |
| `apply_auto_blend_layers`         | Auto-blend (panorama)     |
| `apply_auto_align_layers`         | Auto-align layers         |

## 3.36 ESCAPE HATCH (1 tool)

| Tool                | Purpose                                                               |
| ------------------- | --------------------------------------------------------------------- |
| `execute_batchplay` | Raw batchPlay commands — LAST RESORT. Always pass layer_id parameter. |

</tool-catalog>

---
