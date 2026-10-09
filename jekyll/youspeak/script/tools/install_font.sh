#!/bin/bash
# install_font.sh — install YOUSPEAK font on macOS or Linux
#
# Copies youspeak.otf to the correct user-fonts directory for the host OS
# and refreshes the font cache.
#
# macOS:   ~/Library/Fonts/
# Linux:   ~/.local/share/fonts/ (preferred) or ~/.fonts/
#
# No admin/sudo required — installs per-user.
#
# After install: applications need to be restarted to see the new font.
# Font Book will show it under "User" if you want to verify visually.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# v1 is the living font; v0 kept for compatibility. Install whichever exist.
# Positional params, not a scalar — paths may contain spaces.
set --
for f in "$SCRIPT_DIR/fonts/youspeak-v1.otf" "$SCRIPT_DIR/fonts/youspeak.otf"; do
  [ -f "$f" ] && set -- "$@" "$f"
done

if [ $# -eq 0 ]; then
  echo "error: no font found under $SCRIPT_DIR/fonts/. Build it first:" >&2
  echo "  python3 $SCRIPT_DIR/tools/build_font_v1.py" >&2
  exit 1
fi

case "$(uname -s)" in
  Darwin)
    DEST="$HOME/Library/Fonts"
    mkdir -p "$DEST"
    for f in "$@"; do cp -v "$f" "$DEST/"; done
    echo ""
    echo "✓ YOUSPEAK font(s) installed under $DEST/"
    echo "  Font Book should show them under the 'User' collection."
    echo "  Restart apps to pick them up."
    ;;
  Linux)
    # Prefer modern location
    if [ -d "$HOME/.local/share/fonts" ] || mkdir -p "$HOME/.local/share/fonts" 2>/dev/null; then
      DEST="$HOME/.local/share/fonts"
    else
      DEST="$HOME/.fonts"
      mkdir -p "$DEST"
    fi
    for f in "$@"; do cp -v "$f" "$DEST/"; done
    fc-cache -f "$DEST" 2>&1 | tail -1
    echo ""
    echo "✓ YOUSPEAK font(s) installed under $DEST/"
    echo "  Restart apps to pick them up."
    ;;
  *)
    echo "unsupported OS: $(uname -s). Manual install: copy the fonts/*.otf files into your fonts directory." >&2
    exit 1
    ;;
esac
