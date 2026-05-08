#!/bin/bash
# 🌌 VOID-SHELL ELITE INSTALLER
# THE GHOST IN THE TERMINAL BOOTSTRAPPER

set -e

echo -e "\033[1;35m🌌 INITIATING VOID-SHELL PROTOCOL...\033[0m"

# 1. Environment Check
if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;31m[!] Python 3 not found. Install it first.\033[0m"
    exit 1
fi

# 2. Cleanup & Sync
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$ROOT_DIR"

echo -e "\033[1;34m[+] Synchronizing modules...\033[0m"
# Ensure all __init__.py files exist
find void_shell -type d -exec touch {}/__init__.py \;

# 3. Dependencies
echo -e "\033[1;34m[+] Installing high-speed dependencies...\033[0m"
pip install -r requirements.txt --quiet
pip install -e . --quiet

# 4. Final Verification
echo -e "\033[1;32m[+] Protocol synchronized.\033[0m"
echo -e "\033[1;33m[!] Run 'v' to enter the Abyss.\033[0m"

# Auto-alias injection check
if ! grep -q "alias v=" ~/.bashrc; then
    echo "alias v='python3 -m void_shell.main'" >> ~/.bashrc
    echo -e "\033[1;36m[+] Added 'v' alias to ~/.bashrc\033[0m"
fi

echo -e "\033[1;35m🌌 VOID-SHELL IS READY.\033[0m"
