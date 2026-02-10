#!/bin/bash
set -e

echo "Installing 00bx-photoshop-mcp..."

# Get the package installation directory (where npm installed the package)
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || realpath "${BASH_SOURCE[0]}" 2>/dev/null || echo "${BASH_SOURCE[0]}")"
PACKAGE_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

# Target installation directory
INSTALL_DIR="$HOME/.00bx-photoshop-mcp"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy files
echo "Copying MCP server files..."
cp -r "$PACKAGE_DIR/mcp" "$INSTALL_DIR/"
cp -r "$PACKAGE_DIR/uxp" "$INSTALL_DIR/"
cp -r "$PACKAGE_DIR/adb-proxy-socket" "$INSTALL_DIR/"

# Set up Python virtual environment
echo "Setting up Python environment..."
cd "$INSTALL_DIR/mcp"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install proxy dependencies
echo "Setting up proxy server..."
cd "$INSTALL_DIR/adb-proxy-socket"
npm install

echo ""
echo "✅ Installation complete!"
echo ""
echo "Files installed to: $INSTALL_DIR"
echo ""
echo "Next steps:"
echo "1. Install Adobe UXP Developer Tool from Creative Cloud"
echo "2. Load the plugin from: $INSTALL_DIR/uxp/ps"
echo "3. Start the proxy server:"
echo "   cd $INSTALL_DIR/adb-proxy-socket && npm start"
echo ""
echo "4. Add to OpenCode config (~/.config/opencode/opencode.json):"
echo ""
echo '  "mcp": {'
echo '    "adobe-photoshop": {'
echo '      "type": "local",'
echo '      "command": ["~/.00bx-photoshop-mcp/mcp/.venv/bin/python", "~/.00bx-photoshop-mcp/mcp/ps-mcp.py"],'
echo '      "timeout": 30000'
echo '    }'
echo '  }'
echo ""
