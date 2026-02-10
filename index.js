#!/usr/bin/env node

/**
 * 00bx-photoshop-mcp
 * MCP server for Adobe Photoshop control via AI
 * 
 * This package provides 171 Photoshop tools for OpenCode AI integration.
 * 
 * Installation:
 *   npm install -g 00bx-photoshop-mcp
 *   00bx-photoshop-mcp-install
 * 
 * For detailed setup instructions, see README.md
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const packageJson = require('./package.json');

console.log(`
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║     00bx-photoshop-mcp v${packageJson.version}                      ║
║                                                            ║
║     MCP Server for Adobe Photoshop Control via AI          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

171 tools for design automation including:
  • Complete filter support (blur, distortion, artistic)
  • Advanced layer styles (gradients, shadows, bevels)
  • Shape drawing tools
  • AI-powered features (Firefly integration)
  • batchPlay execution for unlimited control

To complete installation, run:
  00bx-photoshop-mcp-install

For setup instructions:
  https://github.com/00bx/00bx-photoshop-mcp#readme
`);

// Check if install has been run
const installDir = path.join(process.env.HOME, '.00bx-photoshop-mcp');
if (!fs.existsSync(installDir)) {
  console.log('⚠️  Installation not complete!');
  console.log('   Run: 00bx-photoshop-mcp-install');
  process.exit(1);
} else {
  console.log('✅ Installation complete at:', installDir);
  console.log('');
  console.log('Next steps:');
  console.log('  1. Start the proxy: cd ~/.00bx-photoshop-mcp/adb-proxy-socket && node proxy.js');
  console.log('  2. Load UXP plugin in Adobe UXP Developer Tool');
  console.log('  3. Add MCP config to ~/.config/opencode/opencode.json');
  console.log('  4. Start OpenCode and enjoy 171 Photoshop tools!');
}
