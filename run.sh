#!/usr/bin/env bash
# Bhanu AI Terminal Assistant Launcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if command -v python3 &>/dev/null; then
    python3 main.py "$@"
else
    echo "Error: Python 3 is not installed or not in PATH."
    exit 1
fi
