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

# Install OpenCode skills (7 topic-based skills for on-demand loading)
echo "Installing OpenCode skills..."
OPENCODE_SKILLS_DIR="$HOME/.config/opencode/skills"
mkdir -p "$OPENCODE_SKILLS_DIR"

# Remove old monolithic skill if present (replaced by 7 split skills)
if [ -d "$OPENCODE_SKILLS_DIR/photoshop-designer" ]; then
    rm -rf "$OPENCODE_SKILLS_DIR/photoshop-designer"
    echo "  Removed old monolithic photoshop-designer skill"
fi

SKILL_COUNT=0
for skill_dir in ps-fundamentals ps-blend-modes ps-tool-catalog ps-batchplay ps-text-effects ps-photo-effects ps-advanced; do
    if [ -d "$PACKAGE_DIR/skills/$skill_dir" ]; then
        cp -r "$PACKAGE_DIR/skills/$skill_dir" "$OPENCODE_SKILLS_DIR/"
        SKILL_COUNT=$((SKILL_COUNT + 1))
    fi
done

if [ "$SKILL_COUNT" -eq 7 ]; then
    echo "✅ All 7 Photoshop skills installed to: $OPENCODE_SKILLS_DIR/"
    echo "   ps-fundamentals, ps-blend-modes, ps-tool-catalog, ps-batchplay,"
    echo "   ps-text-effects, ps-photo-effects, ps-advanced"
else
    echo "⚠️  Only $SKILL_COUNT of 7 skill directories found in package"
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
