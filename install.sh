#!/bin/bash

echo "🚀 Installing NANDA SDK with automatic PATH setup..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to add to PATH if not already there
add_to_path() {
    local dir="$1"
    if [[ ":$PATH:" != *":$dir:"* ]]; then
        echo "Adding $dir to PATH..."
        export PATH="$dir:$PATH"
        
        # Add to shell config files
        for config in ~/.bashrc ~/.zshrc ~/.profile; do
            if [ -f "$config" ]; then
                if ! grep -q "$dir" "$config"; then
                    echo "export PATH=\"$dir:\$PATH\"" >> "$config"
                    echo "✅ Added to $config"
                fi
            fi
        done
    fi
}

# Install pipx if not present
if ! command_exists pipx; then
    echo "📦 Installing pipx..."
    python3 -m pip install --user pipx
fi

# Setup PATH for pipx
LOCAL_BIN="$HOME/.local/bin"
add_to_path "$LOCAL_BIN"

# Run pipx ensurepath to be sure
if command_exists pipx; then
    echo "🔧 Configuring pipx PATH..."
    pipx ensurepath
else
    echo "⚠️  pipx not found in PATH. Adding manually..."
    export PATH="$LOCAL_BIN:$PATH"
fi

# Install nanda-sdk
echo "📦 Installing nanda-sdk..."
if command_exists pipx; then
    pipx install nanda-sdk
else
    # Fallback: try direct path
    "$LOCAL_BIN/pipx" install nanda-sdk 2>/dev/null || {
        echo "❌ Failed to install with pipx. Trying pip..."
        python3 -m pip install --user nanda-sdk
    }
fi

# Verify installation
echo "🧪 Verifying installation..."
if command_exists nanda-sdk; then
    echo "✅ NANDA SDK installed successfully!"
    echo "🎉 You can now run: nanda-sdk --help"
elif [ -f "$LOCAL_BIN/nanda-sdk" ]; then
    echo "✅ NANDA SDK installed at $LOCAL_BIN/nanda-sdk"
    echo "🔄 Please restart your terminal or run: source ~/.bashrc"
    echo "📝 Then you can run: nanda-sdk --help"
else
    echo "❌ Installation may have failed. Please check manually."
    exit 1
fi

echo ""
echo "📖 Usage example:"
echo "nanda-sdk --anthropic-key YOUR_KEY --domain yourdomain.com"
echo ""
echo "🔧 If you get 'command not found', try:"
echo "source ~/.bashrc && nanda-sdk --help" 