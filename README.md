# 00bx-photoshop-mcp

![00bx-photoshop-mcp](poster.jpg)

MCP server for Adobe Photoshop. 323 tools + 7 AI skills for design automation via OpenCode.

## Install

```bash
npm install -g 00bx-photoshop-mcp
00bx-photoshop-mcp-install
```

Installs everything to `~/.00bx-photoshop-mcp/` and 7 OpenCode skills to `~/.config/opencode/skills/`.

## Setup

### 1. Start the proxy

```bash
cd ~/.00bx-photoshop-mcp/adb-proxy-socket && node proxy.js
```

Keep this running. Background alternative:

```bash
nohup node proxy.js > /tmp/ps-proxy.log 2>&1 &
```

### 2. Load the UXP plugin

1. Open **Adobe UXP Developer Tool** (from Creative Cloud)
2. Add Plugin -> select `~/.00bx-photoshop-mcp/uxp/ps`
3. Click Load
4. Open Photoshop

### 3. Add MCP config

Add to `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "adobe-photoshop": {
      "type": "local",
      "command": [
        "~/.00bx-photoshop-mcp/mcp/.venv/bin/python",
        "~/.00bx-photoshop-mcp/mcp/ps-mcp.py"
      ],
      "timeout": 30000,
      "enabled": true
    }
  }
}
```

Restart OpenCode. Done.

## What's included

### 323 Tools

| Category     | Examples                                                                    |
| ------------ | --------------------------------------------------------------------------- |
| Filters      | Gaussian blur, motion blur, oil paint, sharpen, noise, pixelate, distortion |
| Layer styles | Drop shadow, inner glow, bevel, gradient overlay, stroke                    |
| Shapes       | Rectangle, ellipse, polygon, line, arrow, custom path                       |
| Selections   | Subject, sky, color range, focus area, expand, feather                      |
| Text         | Single/multi-line, edit properties                                          |
| Transforms   | Scale, rotate, flip, perspective, warp, content-aware scale                 |
| Adjustments  | Brightness, hue/sat, curves, levels, color balance, vibrance                |
| Canvas       | Create, crop, resize, rotate, trim                                          |
| Layers       | Create, duplicate, delete, group, merge, visibility, position               |
| batchPlay    | Execute any Photoshop command directly                                      |

### 7 AI Skills (auto-installed)

Skills load on-demand so they don't eat your context window.

| Skill              | What it covers                                                |
| ------------------ | ------------------------------------------------------------- |
| `ps-fundamentals`  | Core rules, coordinate system, masks, smart objects           |
| `ps-blend-modes`   | All blend mode formulas and quick reference                   |
| `ps-tool-catalog`  | Complete 323-tool reference by category                       |
| `ps-batchplay`     | BatchPlay descriptors, reference forms, event codes           |
| `ps-text-effects`  | 19 verified text effect recipes with exact parameters         |
| `ps-photo-effects` | 13 photo effects + 4 color grading recipes                    |
| `ps-advanced`      | Filter ranges, workflow templates, gotchas, quality checklist |

## Architecture

```
OpenCode <-> MCP Server (Python) <-> Proxy (Node) <-> UXP Plugin <-> Photoshop
```

## Requirements

- Adobe Photoshop 2025/2026
- Adobe UXP Developer Tool
- Python 3.10+
- Node.js 18+
- OpenCode

## Troubleshooting

**"Could not connect to photoshop"**

- Check proxy is running: `lsof -i :3001`
- Check UXP plugin is loaded
- Make sure Photoshop is open

**MCP not showing in OpenCode**

- Validate config: `cat ~/.config/opencode/opencode.json | python3 -m json.tool`
- Restart OpenCode

**Commands timeout**

- Increase timeout to `60000` in your config
- Open a document in Photoshop first (some commands need one)

## Attribution

Forked from [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp). Extended from 50 to 323 tools with full filter/effect coverage.

## License

MIT
