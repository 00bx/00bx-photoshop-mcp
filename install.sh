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

# Remove existing installation if present to avoid permission issues
if [ -d "$INSTALL_DIR/mcp" ]; then
    rm -rf "$INSTALL_DIR/mcp"
fi
if [ -d "$INSTALL_DIR/uxp" ]; then
    rm -rf "$INSTALL_DIR/uxp"
fi
if [ -d "$INSTALL_DIR/adb-proxy-socket" ]; then
    rm -rf "$INSTALL_DIR/adb-proxy-socket"
fi

# Copy directories, excluding .venv if it exists in source
if [ -d "$PACKAGE_DIR/mcp/.venv" ]; then
    # Copy mcp without .venv
    mkdir -p "$INSTALL_DIR/mcp"
    find "$PACKAGE_DIR/mcp" -mindepth 1 -maxdepth 1 ! -name '.venv' -exec cp -r {} "$INSTALL_DIR/mcp/" \;
else
    cp -r "$PACKAGE_DIR/mcp" "$INSTALL_DIR/"
fi

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

# Install OpenCode skill
echo "Installing OpenCode skill..."
OPENCODE_SKILLS_DIR="$HOME/.config/opencode/skills"
mkdir -p "$OPENCODE_SKILLS_DIR"

if [ -d "$PACKAGE_DIR/skills/photoshop-designer" ]; then
    cp -r "$PACKAGE_DIR/skills/photoshop-designer" "$OPENCODE_SKILLS_DIR/"
    echo "✅ Skill installed to: $OPENCODE_SKILLS_DIR/photoshop-designer"
else
    echo "⚠️  Skill files not found in package"
fi

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
