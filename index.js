#!/usr/bin/env node

/**
 * 00bx-photoshop-mcp
 * MCP server for Adobe Photoshop control via AI
 */

const path = require("path");
const fs = require("fs");

const packageJson = require("./package.json");

console.log(`
  00bx-photoshop-mcp v${packageJson.version}

  323 Photoshop tools + 7 AI skills
  Filters, layer styles, shapes, text, selections,
  transforms, AI features, and batchPlay.

  To complete installation:
    00bx-photoshop-mcp-install

  Docs: https://github.com/00bx/00bx-photoshop-mcp
`);

const installDir = path.join(process.env.HOME, ".00bx-photoshop-mcp");
if (!fs.existsSync(installDir)) {
  console.log("  Installation not complete. Run: 00bx-photoshop-mcp-install");
  process.exit(1);
} else {
  console.log("  Installed at:", installDir);
  console.log("");
  console.log("  Next:");
  console.log(
    "  1. Start proxy:  cd ~/.00bx-photoshop-mcp/adb-proxy-socket && node proxy.js",
  );
  console.log("  2. Load UXP plugin in Adobe UXP Developer Tool");
  console.log("  3. Add MCP config to opencode.json");
  console.log("");
}
