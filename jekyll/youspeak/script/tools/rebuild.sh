#!/bin/bash
# rebuild.sh — one-command rebuild of the YOUSPEAK script organ's artifacts.
#
# After any change to glyph_specs_v1.py or morphemes.json, run:
#   script/tools/rebuild.sh            # build + previews + tests + espanso
#   script/tools/rebuild.sh --install  # …then install the font user-wide
#
# Steps:
#   1. build youspeak-v1.otf + youspeak-v1.ttf from glyph_specs_v1.py
#   2. regenerate SVG/HTML previews (glyphs/preview/)
#   3. transliterator round-trip tests
#   4. regenerate the espanso keyboard layer from morphemes.json
#   5. (--install) copy fonts into the user font directory

set -e

TOOLS_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_DIR="$(dirname "$TOOLS_DIR")"
PY=python3

echo "── 1/4 font build ──────────────────────────────"
$PY "$TOOLS_DIR/build_font_v1.py"
$PY "$TOOLS_DIR/build_font_v1.py" --ttf

echo "── 2/4 previews ────────────────────────────────"
$PY "$TOOLS_DIR/render_preview_v1.py"

echo "── 3/4 transliterator tests ────────────────────"
$PY "$TOOLS_DIR/transliterate.py" test

echo "── 4/4 espanso keyboard layer ──────────────────"
if [ -f "$TOOLS_DIR/gen_espanso.py" ]; then
  $PY "$TOOLS_DIR/gen_espanso.py"
else
  echo "(gen_espanso.py not present — skipped)"
fi

echo "── agent bundle ────────────────────────────────"
$PY "$TOOLS_DIR/export_agent_bundle.py"

if [ "$1" = "--install" ]; then
  echo "── install ─────────────────────────────────────"
  case "$(uname -s)" in
    Darwin) DEST="$HOME/Library/Fonts" ;;
    Linux)  DEST="$HOME/.local/share/fonts"; mkdir -p "$DEST" ;;
    *) echo "unsupported OS for install: $(uname -s)" >&2; exit 1 ;;
  esac
  cp -v "$SCRIPT_DIR/fonts/youspeak-v1.otf" "$DEST/"
  command -v fc-cache >/dev/null && fc-cache -f "$DEST" || true
  echo "✓ installed — restart apps to pick it up"
fi

echo "✓ rebuild complete"
