"""YOUSPEAK glyph specifications.

Each morpheme's glyph defined as a list of *strokes*. A stroke is a line
segment (x1, y1, x2, y2) drawn with a fixed stroke-width. Coordinates are
in EM units (1000-unit EM square, standard TrueType convention).

The build_font.py tool converts strokes into closed polygon contours
(rectangles along the stroke-axis) and bundles them into an OTF/TTF
font file.

Design principles (from script/glyphs/README.md):
- 1000-unit EM square
- Body from y=50 to y=800 (750 units tall; leaves room for descent/ascent)
- Horizontal body from x=100 to x=900 (800 units wide; 100-unit sidebearings)
- Stroke width: 60 units (medium weight, legible at 12pt)
- Dots: small 80x80 squares centered at specified points

Each entry keys on the Latin name (matches morphemes.json `latin` field).
"""

from __future__ import annotations

STROKE_WIDTH = 60
DOT_SIZE = 80
EM = 1000


def dot(x: int, y: int, size: int = DOT_SIZE) -> list[tuple[int, int]]:
    """Return a filled square (4 corner points) centered at (x, y)."""
    h = size // 2
    return [(x - h, y - h), (x + h, y - h), (x + h, y + h), (x - h, y + h)]


# Each glyph is a dict with:
#   "strokes": list of (x1, y1, x2, y2) line segments
#   "polygons": list of list-of-(x,y) for arbitrary filled shapes (e.g., dots)
GLYPHS = {
    # ===== CONTENT MORPHEMES (U+E100+) =====

    "doxa": {  # U+E100 — downward triangle + horizontal bar (weight+manifestation)
        "strokes": [
            (150, 700, 850, 700),   # top edge of inverted triangle
            (850, 700, 500, 150),   # right diagonal
            (500, 150, 150, 700),   # left diagonal
            (80,  430, 920, 430),   # horizontal bar through the middle
        ],
    },

    "kallos": {  # U+E101 — vertical + two upward-opening arms
        "strokes": [
            (500, 80,  500, 700),   # central vertical
            (200, 500, 500, 780),   # left wing
            (800, 500, 500, 780),   # right wing
        ],
    },

    "ortho": {  # U+E102 — cross (vertical + top horizontal)
        "strokes": [
            (500, 80,  500, 800),   # vertical
            (200, 700, 800, 700),   # horizontal at top
        ],
    },

    "phanes": {  # U+E103 — three rays from central point (shining)
        "strokes": [
            (500, 200, 200, 700),
            (500, 200, 500, 800),
            (500, 200, 800, 700),
            (500, 200, 150, 400),
            (500, 200, 850, 400),
        ],
    },

    "algia": {  # U+E104 — bent line with ache-mark
        "strokes": [
            (400, 750, 400, 450),   # upper vertical
            (400, 450, 650, 200),   # bend downward-right
        ],
        "polygons": [dot(400, 450, 120)],  # mark at bend
    },

    "anagno": {  # U+E105 — two parallels with vertical connector
        "strokes": [
            (200, 750, 800, 750),   # top parallel
            (200, 250, 800, 250),   # bottom parallel
            (500, 750, 500, 250),   # connector
        ],
    },

    "stasis": {  # U+E106 — two short verticals on a horizontal anchor
        "strokes": [
            (350, 200, 350, 700),   # left vertical
            (650, 200, 650, 700),   # right vertical
            (200, 200, 800, 200),   # anchor
        ],
    },

    "meta": {  # U+E107 — left-pointing wedge
        "strokes": [
            (250, 450, 850, 450),   # horizontal arrow-shaft
            (250, 450, 450, 650),   # upper arm
            (250, 450, 450, 250),   # lower arm
        ],
    },

    "strophe": {  # U+E108 — spiral (approximated as two arcs)
        "strokes": [
            # outer arc (as straight segments approximating a circle)
            (800, 450, 750, 700),
            (750, 700, 500, 800),
            (500, 800, 250, 700),
            (250, 700, 200, 450),
            (200, 450, 250, 250),
            (250, 250, 500, 200),
            # tail
            (500, 200, 700, 250),
            (700, 250, 700, 400),
        ],
    },

    "thauma": {  # U+E109 — eye shape (wondering gaze)
        "strokes": [
            # eye outline approximated
            (200, 450, 400, 600),
            (400, 600, 600, 600),
            (600, 600, 800, 450),
            (800, 450, 600, 300),
            (600, 300, 400, 300),
            (400, 300, 200, 450),
        ],
        "polygons": [dot(500, 450, 160)],  # pupil
    },

    "syn": {  # U+E10A — inverted V (converging)
        "strokes": [
            (200, 700, 500, 200),
            (800, 700, 500, 200),
        ],
    },

    "phora": {  # U+E10B — L-shape (carrying bracket)
        "strokes": [
            (200, 400, 700, 400),
            (700, 400, 700, 650),
        ],
    },

    "cand": {  # U+E10C — sun with soft radiance
        "strokes": [
            # small radiating strokes at top
            (400, 700, 350, 800),
            (500, 730, 500, 830),
            (600, 700, 650, 800),
            # circle approximation (octagon)
            (350, 450, 450, 600),
            (450, 600, 550, 600),
            (550, 600, 650, 450),
            (650, 450, 550, 300),
            (550, 300, 450, 300),
            (450, 300, 350, 450),
        ],
    },

    "dokim": {  # U+E10D — crucible (cup shape)
        "strokes": [
            (250, 500, 300, 250),   # left wall slanting inward
            (300, 250, 700, 250),   # bottom
            (700, 250, 750, 500),   # right wall slanting outward
            # flame above
            (500, 550, 500, 750),
        ],
    },

    "arti": {  # U+E10E — pentagon (five pre-domain qualities)
        "strokes": [
            (500, 750, 800, 550),
            (800, 550, 680, 250),
            (680, 250, 320, 250),
            (320, 250, 200, 550),
            (200, 550, 500, 750),
        ],
    },

    "veri": {  # U+E10F — balanced cross
        "strokes": [
            (500, 100, 500, 700),   # vertical
            (200, 400, 800, 400),   # horizontal (extends slightly beyond)
        ],
    },

    "compler": {  # U+E110 — two opposing curves (mutual filling)
        "strokes": [
            # left half-circle (approx)
            (250, 650, 450, 650),
            (450, 650, 450, 250),
            (450, 250, 250, 250),
            # right half-circle
            (750, 650, 550, 650),
            (550, 650, 550, 250),
            (550, 250, 750, 250),
        ],
    },

    "diplos": {  # U+E111 — two parallel verticals
        "strokes": [
            (350, 100, 350, 750),
            (650, 100, 650, 750),
        ],
    },

    "sema": {  # U+E112 — square with central dot
        "strokes": [
            (300, 300, 700, 300),
            (700, 300, 700, 700),
            (700, 700, 300, 700),
            (300, 700, 300, 300),
        ],
        "polygons": [dot(500, 500, 140)],
    },

    "anastro": {  # U+E113 — reverse spiral (mirror of strophe)
        "strokes": [
            (200, 450, 250, 700),
            (250, 700, 500, 800),
            (500, 800, 750, 700),
            (750, 700, 800, 450),
            (800, 450, 750, 250),
            (750, 250, 500, 200),
            (500, 200, 300, 250),
            (300, 250, 300, 400),
        ],
    },

    "kalypt": {  # U+E114 — box with dot (enclosing)
        "strokes": [
            (250, 250, 750, 250),
            (750, 250, 750, 700),
            (750, 700, 250, 700),
            (250, 700, 250, 250),
        ],
        "polygons": [dot(500, 475, 120)],
    },

    "haphe": {  # U+E115 — two fingertips touching
        "strokes": [
            (300, 250, 450, 500),
            (450, 500, 500, 600),
            (700, 250, 550, 500),
            (550, 500, 500, 600),
        ],
    },

    "allos": {  # U+E116 — Y shape (bifurcation)
        "strokes": [
            (500, 200, 500, 500),
            (500, 500, 300, 750),
            (500, 500, 700, 750),
        ],
    },

    "parallax": {  # U+E117 — two parallel lines with offset
        "strokes": [
            (200, 600, 800, 600),
            (200, 300, 800, 300),
            (450, 450, 550, 450),  # small offset-arrow
            (500, 500, 550, 450),
            (500, 400, 550, 450),
        ],
    },

    "hypo": {  # U+E118 — horizontal with descending vertical
        "strokes": [
            (200, 550, 800, 550),
            (500, 550, 500, 200),
        ],
    },

    "stix": {  # U+E119 — single dot
        "strokes": [],
        "polygons": [dot(500, 450, 180)],
    },

    "kairos": {  # U+E11A — hourglass
        "strokes": [
            (200, 700, 800, 700),   # top
            (800, 700, 200, 200),   # right-to-left diagonal
            (200, 200, 800, 200),   # bottom
            (800, 200, 200, 700),   # left-to-right diagonal
        ],
    },

    "morphe": {  # U+E11B — irregular closed shape
        "strokes": [
            (300, 700, 550, 750),
            (550, 750, 750, 500),
            (750, 500, 700, 250),
            (700, 250, 400, 200),
            (400, 200, 250, 400),
            (250, 400, 300, 700),
        ],
    },

    "klimax": {  # U+E11C — small staircase
        "strokes": [
            (200, 250, 400, 250),
            (400, 250, 400, 400),
            (400, 400, 600, 400),
            (600, 400, 600, 550),
            (600, 550, 800, 550),
            (800, 550, 800, 700),
        ],
    },

    "lanthes": {  # U+E11D — dashed outline (hidden-but-present)
        "strokes": [
            (250, 700, 400, 700),
            (500, 700, 650, 700),
            (750, 700, 750, 550),
            (750, 450, 750, 300),
            (750, 250, 600, 250),
            (500, 250, 350, 250),
            (250, 250, 250, 400),
            (250, 500, 250, 650),
        ],
    },

    "sleight": {  # U+E11E — crossed diagonals
        "strokes": [
            (250, 250, 750, 700),
            (750, 250, 250, 700),
        ],
    },

    "seem": {  # U+E11F — lenticular lens (appearance-through)
        "strokes": [
            (250, 450, 400, 600),
            (400, 600, 600, 600),
            (600, 600, 750, 450),
            (750, 450, 600, 300),
            (600, 300, 400, 300),
            (400, 300, 250, 450),
        ],
    },

    # ===== GRAMMATICAL MORPHEMES (U+E140+) =====

    "a": {  # U+E140 — privative: circle with slash
        "strokes": [
            # circle approximation
            (350, 450, 450, 600),
            (450, 600, 550, 600),
            (550, 600, 650, 450),
            (650, 450, 550, 300),
            (550, 300, 450, 300),
            (450, 300, 350, 450),
            # slash
            (250, 250, 750, 650),
        ],
    },

    "sis": {  # U+E141 — short vertical with terminal bar
        "strokes": [
            (500, 300, 500, 650),
            (400, 300, 600, 300),
        ],
    },

    "ance": {  # U+E142 — small hook
        "strokes": [
            (400, 550, 400, 300),
            (400, 300, 600, 150),
        ],
    },

    "mance": {  # U+E143 — hook with dot (variant of -ance)
        "strokes": [
            (400, 550, 400, 300),
            (400, 300, 600, 150),
        ],
        "polygons": [dot(600, 500, 70)],
    },

    "ence": {  # U+E144 — softer hook
        "strokes": [
            (400, 500, 400, 300),
            (400, 300, 550, 200),
        ],
    },

    "ma": {  # U+E145 — small curl (result-of-action)
        "strokes": [
            (400, 450, 450, 550),
            (450, 550, 550, 550),
            (550, 550, 600, 450),
            (600, 450, 550, 350),
            (550, 350, 450, 350),
            (450, 350, 400, 450),
        ],
    },

    "iance": {  # U+E146 — hook with upward luminous ray
        "strokes": [
            (400, 500, 400, 300),
            (400, 300, 600, 150),
            (500, 550, 500, 750),
        ],
    },

    "escence": {  # U+E147 — open-ended hook
        "strokes": [
            (400, 500, 400, 300),
            (400, 300, 700, 250),
        ],
    },

    "mia": {  # U+E148 — state suffix (alternative short form)
        "strokes": [
            (400, 500, 400, 300),
            (400, 300, 500, 200),
            (500, 200, 600, 300),
        ],
    },

    "ana": {  # U+E149 — upward arrow (prefix)
        "strokes": [
            (500, 250, 500, 650),
            (500, 650, 400, 550),
            (500, 650, 600, 550),
        ],
    },

    "en": {  # U+E14A — inward bracket
        "strokes": [
            (300, 650, 550, 650),
            (550, 650, 550, 250),
            (550, 250, 300, 250),
        ],
    },

    "com": {  # U+E14B — joining marks (> <)
        "strokes": [
            (250, 250, 400, 450),
            (400, 450, 250, 650),
            (750, 250, 600, 450),
            (600, 450, 750, 650),
        ],
    },

    "y": {  # U+E14C — noun-abstract suffix (small Y)
        "strokes": [
            (400, 700, 500, 500),
            (600, 700, 500, 500),
            (500, 500, 500, 300),
        ],
    },
}


# Map from Latin-name to Unicode codepoint (read from morphemes.json)
def load_codepoint_map() -> dict[str, int]:
    """Load {latin: codepoint_int} from morphemes.json."""
    import json
    from pathlib import Path
    morphemes_path = Path(__file__).resolve().parent.parent / "morphemes.json"
    with morphemes_path.open() as f:
        data = json.load(f)
    out: dict[str, int] = {}
    for m in data["morphemes"]:
        latin = m["latin"].strip("-")
        cp_str = m["codepoint"].replace("U+", "")
        out[latin] = int(cp_str, 16)
    return out
