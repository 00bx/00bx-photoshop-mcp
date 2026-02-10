# 00bx-photoshop-mcp

MCP server for Adobe Photoshop control via AI. Forked from [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) with 171 tools and enhanced capabilities for design automation.

## What's improved

- 171 Photoshop tools (vs 50 in original)
- Complete filter support (blur, distortion, artistic, stylize)
- Advanced layer styles (gradients, glows, shadows, bevels)
- Shape drawing tools (rectangles, ellipses, polygons, custom paths)
- Brush and paint tools
- Selection tools (color range, focus area, subject detection)
- Transform tools (perspective, warp, free transform)
- Text manipulation
- Canvas operations
- batchPlay execution for unlimited Photoshop control

## Installation

```bash
npm install -g 00bx-photoshop-mcp
00bx-photoshop-mcp-install
```

This installs everything to `~/.00bx-photoshop-mcp/` and sets up Python + Node environments automatically.

## Setup

### 1. Start the proxy server

```bash
cd ~/.00bx-photoshop-mcp/adb-proxy-socket
npm start
```

Keep this running in a terminal.

### 2. Load the UXP plugin

- Open Adobe UXP Developer Tool (install from Creative Cloud)
- Click "Add Plugin"
- Select `~/.00bx-photoshop-mcp/uxp/ps`
- Click "Load"
- Open Photoshop — plugin connects automatically

### 3. Add to OpenCode config

Edit `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "adobe-photoshop": {
      "type": "local",
      "command": ["~/.00bx-photoshop-mcp/mcp/.venv/bin/python", "~/.00bx-photoshop-mcp/mcp/ps-mcp.py"],
      "timeout": 30000
    }
  }
}
```

OpenCode will expand `~` to your home directory automatically.

## Usage

```bash
opencode
```

Ask OpenCode to do Photoshop tasks:
- "Create a neon text effect"
- "Apply gaussian blur to the active layer"
- "Generate a poster with liquid drip effect"
- "Remove background from this image"

## Architecture

```
AI (OpenCode) ↔ MCP Server (Python) ↔ Proxy (Node) ↔ UXP Plugin ↔ Photoshop
```

The proxy is required because UXP plugins can only connect as clients, not listen as servers.

## Development

To modify the MCP server:

```bash
cd ~/.00bx-photoshop-mcp/mcp
source .venv/bin/activate
# Edit ps-mcp.py
# Changes take effect on next OpenCode restart
```

## Attribution

Forked from [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) — original proof of concept by Mike Chambers. This fork extends the Photoshop MCP with 3× more tools and comprehensive filter/effect coverage for production design workflows.

## License

MIT — Original work by Mike Chambers, enhancements by [00bx](https://github.com/00bx)
