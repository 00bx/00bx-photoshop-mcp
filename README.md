# 00bx-photoshop-mcp

MCP server for Adobe Photoshop control via AI. Forked from [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) with 171 tools and enhanced capabilities for design automation.

## What's improved

- **171 Photoshop tools** (vs 50 in original)
- **Complete filter support** (blur, distortion, artistic, stylize)
- **Advanced layer styles** (gradients, glows, shadows, bevels)
- **Shape drawing tools** (rectangles, ellipses, polygons, custom paths)
- **Brush and paint tools**
- **Selection tools** (color range, focus area, subject detection)
- **Transform tools** (perspective, warp, free transform)
- **Text manipulation**
- **Canvas operations**
- **batchPlay execution** for unlimited Photoshop control
- **🎨 OpenCode Skill included** - Automatic installation of photoshop-designer skill with exact effect recipes

## Prerequisites

Before installing, ensure you have:

- **macOS** (Windows/Linux support coming soon)
- **Adobe Photoshop 2025/2026** installed
- **Adobe UXP Developer Tool** (install from Creative Cloud)
- **Python 3.10+** installed
- **Node.js 18+** installed
- **OpenCode CLI** installed

## Quick Start (3 Steps)

### Step 1: Install the Package

```bash
npm install -g 00bx-photoshop-mcp
00bx-photoshop-mcp-install
```

This installs everything to `~/.00bx-photoshop-mcp/` and sets up Python + Node environments automatically.

### Step 2: Start the Proxy Server

Open a terminal and run:

```bash
cd ~/.00bx-photoshop-mcp/adb-proxy-socket
node proxy.js
```

**Keep this terminal open.** The proxy must stay running while you use Photoshop with OpenCode.

**Optional - Run in background:**
```bash
nohup node proxy.js > /tmp/ps-proxy.log 2>&1 &
```

**Verify it's working:**
```bash
lsof -i :3001  # Should show node proxy.js listening
```

### Step 3: Load the UXP Plugin

1. Open **Adobe UXP Developer Tool** (install from Creative Cloud if you don't have it)
2. Click **"Add Plugin"**
3. Select the folder: `~/.00bx-photoshop-mcp/uxp/ps`
4. Click **"Load"**
5. Open **Adobe Photoshop** — the plugin will connect automatically

**Verify connection:** Look for "MCP Plugin Connected" in the UXP Developer Tool console.

## OpenCode Configuration

Add this to your `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "adobe-photoshop": {
      "type": "local",
      "command": ["~/.00bx-photoshop-mcp/mcp/.venv/bin/python", "~/.00bx-photoshop-mcp/mcp/ps-mcp.py"],
      "timeout": 30000,
      "enabled": true
    }
  }
}
```

**Note:** OpenCode automatically expands `~` to your home directory.

### Verification

After configuring, restart OpenCode and verify the MCP loads:

```bash
opencode
# Ask: "What Photoshop tools do you have available?"
```

## Usage Examples

Once everything is set up, start OpenCode and ask for Photoshop tasks:

### Image Editing
- "Apply gaussian blur to the active layer"
- "Remove background from this image using AI"
- "Apply oil paint filter with stylization 8"
- "Create a smart sharpen effect with radius 2.5"

### Text & Typography
- "Create a neon text effect saying 'HELLO'"
- "Add a drop shadow to the text layer"
- "Apply gradient overlay to the text layer"

### Design & Effects
- "Generate a poster with liquid drip effect"
- "Apply plastic wrap filter"
- "Create a motion blur effect"
- "Apply bevel and emboss with inner bevel style"

### Shapes & Drawing
- "Draw a red rectangle with rounded corners"
- "Create a polygon shape with 6 sides"
- "Draw an arrow pointing to the top-right"

### Layer Operations
- "Create a new solid color fill layer with blue"
- "Add an adjustment layer for brightness and contrast"
- "Group the selected layers"
- "Merge visible layers"

### Selections
- "Select the subject in this photo"
- "Select the sky in the current layer"
- "Create a color range selection for red tones"

### Transformations
- "Apply perspective transform to this layer"
- "Warp the layer with arc style"
- "Rotate the layer 45 degrees"

### Canvas Operations
- "Resize the canvas to 2000x1500 pixels"
- "Crop to the active selection"
- "Resize the image to 50%"

## Architecture

```
AI (OpenCode) ↔ MCP Server (Python) ↔ Proxy (Node) ↔ UXP Plugin ↔ Photoshop
```

The proxy is required because UXP plugins can only connect as clients, not listen as servers.

## Troubleshooting

### Issue: "Could not connect to photoshop"

**Check 1:** Is the proxy running?
```bash
lsof -i :3001
```
If not, restart it: `cd ~/.00bx-photoshop-mcp/adb-proxy-socket && node proxy.js`

**Check 2:** Is the UXP plugin loaded?
- Open Adobe UXP Developer Tool
- Check if the ps plugin shows as "Loaded"
- Check the console for connection messages

**Check 3:** Is Photoshop running?
- Photoshop must be open before the plugin connects

### Issue: "ModuleNotFoundError: No module named 'numpy'"

The Python dependencies weren't installed correctly. Fix:
```bash
cd ~/.00bx-photoshop-mcp/mcp
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: MCP not showing in OpenCode

**Check 1:** Verify your config file syntax:
```bash
cat ~/.config/opencode/opencode.json | python3 -m json.tool
```

**Check 2:** Check OpenCode logs for MCP loading errors:
```bash
opencode --verbose
```

### Issue: Commands timeout

Increase the timeout in your OpenCode config:
```json
"timeout": 60000
```

### Issue: Photoshop doesn't respond

**Check 1:** Open a document in Photoshop first (some commands require an open document)

**Check 2:** Restart the proxy and reload the UXP plugin:
1. Stop the proxy (Ctrl+C)
2. Unload the UXP plugin
3. Start the proxy again
4. Reload the UXP plugin
5. Restart OpenCode

## Development

To modify the MCP server:

```bash
cd ~/.00bx-photoshop-mcp/mcp
source .venv/bin/activate
# Edit ps-mcp.py
# Changes take effect on next OpenCode restart
```

To add new tools, edit `ps-mcp.py` and follow the existing pattern:

```python
@mcp.tool()
def your_tool_name(param1: str, param2: int):
    """
    Description of what your tool does.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    """
    command = createCommand("actionName", {
        "param1": param1,
        "param2": param2
    })
    return sendCommand(command)
```

## Available Commands Reference

### Filters
- `apply_gaussian_blur`, `apply_motion_blur`, `apply_radial_blur`
- `apply_smart_sharpen`, `apply_unsharp_mask`, `apply_sharpen`
- `apply_oil_paint`, `apply_plastic_wrap`
- `apply_emboss`, `apply_find_edges`
- `apply_noise`, `apply_despeckle`, `apply_median_noise`
- `apply_pixelate`, `apply_crystallize`, `apply_color_halftone`
- `apply_twirl_distortion`, `apply_zig_zag_distortion`, `apply_ripple`
- `apply_wave`, `apply_sphere`, `apply_pinch`

### Layer Styles
- `add_drop_shadow`, `add_inner_shadow`
- `add_outer_glow`, `add_inner_glow`
- `add_bevel_emboss`, `add_satin`
- `add_color_overlay`, `add_gradient_overlay`
- `add_stroke`

### Shapes
- `draw_rectangle_shape`, `draw_ellipse_shape`
- `draw_polygon_shape`, `draw_line_shape`
- `draw_arrow_shape`, `draw_custom_path`

### Selections
- `select_subject`, `select_sky`
- `select_color_range`, `select_focus_area`
- `select_all`, `invert_selection`
- `expand_selection`, `contract_selection`
- `feather_selection`

### Text
- `create_single_line_text_layer`, `create_multi_line_text_layer`
- `edit_text_layer`

### Layers
- `create_pixel_layer`, `duplicate_layer`
- `delete_layer`, `group_layers`
- `merge_layers`, `merge_visible`
- `set_layer_visibility`, `set_layer_properties`
- `move_layer`, `set_layer_position_absolute`

### Canvas
- `create_document`, `crop_document`
- `resize_canvas`, `resize_image`
- `rotate_canvas`, `trim_document`

### Adjustments
- `add_brightness_contrast_adjustment_layer`
- `add_hue_saturation_adjustment_layer`
- `add_color_balance_adjustment_layer`
- `add_vibrance_adjustment_layer`
- `add_levels_adjustment_layer`, `add_curves_adjustment_layer`
- `add_black_and_white_adjustment_layer`
- `add_photo_filter_adjustment_layer`
- `add_gradient_map_adjustment_layer`

### AI Features
- `generate_image` - Generate images using Adobe Firefly
- `generative_fill` - Fill selections with AI-generated content
- `remove_background` - AI-powered background removal
- `harmonize_layer` - Match lighting and colors

### Transformations
- `scale_layer`, `rotate_layer`, `flip_layer`
- `translate_layer`, `free_transform`
- `perspective_transform`, `warp_transform`
- `content_aware_scale`

### Advanced
- `execute_batchplay` - Run any Photoshop batchPlay command
- `get_documents`, `set_active_document`
- `get_layers`, `get_document_info`

## Attribution

Forked from [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) — original proof of concept by Mike Chambers. This fork extends the Photoshop MCP with 3× more tools and comprehensive filter/effect coverage for production design workflows.

## License

MIT — Original work by Mike Chambers, enhancements by [00bx](https://github.com/00bx)

## Support

- **Issues:** [GitHub Issues](https://github.com/00bx/00bx-photoshop-mcp/issues)
- **Discussions:** [GitHub Discussions](https://github.com/00bx/00bx-photoshop-mcp/discussions)

## Changelog

### v1.0.0
- Initial release with 171 Photoshop tools
- Complete filter support
- Advanced layer styles
- Shape drawing tools
- AI-powered features (Firefly integration)
- Full OpenCode MCP compatibility
