# -*- coding: utf-8 -*-
"""Rasterise the two-key authority figure for the Word / PowerPoint deliverables.

Why this exists
---------------
`docs/two-key-authority.svg` is the source of truth. GitHub renders SVG, and so
does every browser, so the Markdown deliverable just links the .svg.

python-docx and python-pptx cannot embed SVG, so the .docx/.pptx need a raster
version. svglib + reportlab would convert it directly, but reportlab's renderPM
has no working raster backend on this machine (`cannot import desired renderPM
backend rlPyCairo`), so the figure is re-drawn here with matplotlib using the
*same* coordinates, colours and text as the SVG. Keep the two in sync by hand:
if you edit the SVG, edit LAYOUT below.

Usage:  python _build/svg2png.py [dpi]     (default 300 -> 2833 x 1425 px)
"""
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, PathPatch, Polygon
from matplotlib.path import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs', 'two-key-authority.png')

# viewBox from the SVG: 0 0 680 342
W, H = 680.0, 342.0
# SVG user unit -> matplotlib point (figsize 6.8x3.42 in, 1 unit = 0.01 in)
PT = 0.72

BLUE = '#185FA5'
BLUE_DARK = '#0C447C'
BLUE_BG = '#E6F1FB'
GREEN = '#0F6E56'
GREEN_DARK = '#085041'
GREEN_BG = '#E1F5EE'
SAND_BG = '#F1EFE8'
SAND = '#5F5E5A'
SAND_DARK = '#2C2C2A'
RED_BG = '#FCEBEB'
RED = '#A32D2D'
RED_DARK = '#791F1F'
GREY = '#444441'


def box(ax, x, y, w, h, fc, ec):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle='round,pad=0,rounding_size=10',
        linewidth=0.5, edgecolor=ec, facecolor=fc, zorder=2))


def txt(ax, x, y, s, size, color, weight='normal'):
    ax.text(x, y, s, ha='center', va='center', fontsize=size * PT,
            color=color, fontweight=weight, zorder=3)


def curve(ax, verts, codes, color):
    ax.add_patch(PathPatch(Path(verts, codes), fill=False,
                           edgecolor=color, linewidth=1.5, zorder=2))
    # arrowhead: triangle built from the direction of the final segment
    (x0, y0), (x1, y1) = verts[-2], verts[-1]
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    L, Wd = 9.0, 4.2
    tip = (x1, y1)
    base = (x1 - L * math.cos(ang), y1 - L * math.sin(ang))
    nx, ny = -math.sin(ang), math.cos(ang)
    p1 = (base[0] + Wd * nx, base[1] + Wd * ny)
    p2 = (base[0] - Wd * nx, base[1] - Wd * ny)
    ax.add_patch(Polygon([tip, p1, p2], closed=True, facecolor=color,
                         edgecolor=color, linewidth=0, zorder=3))


def draw(ax):
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)                      # SVG y grows downwards
    ax.set_aspect('equal')
    ax.axis('off')

    # --- row 1: the two authorities -------------------------------------
    box(ax, 40, 40, 280, 76, BLUE_BG, BLUE)
    txt(ax, 180, 66, 'gstack orchestration', 14, BLUE_DARK, '500')
    txt(ax, 180, 86, 'CEO · PM · Engineer · QC · DevOps', 12, BLUE)
    txt(ax, 180, 103, 'process authority', 12, BLUE)

    box(ax, 360, 40, 280, 76, GREEN_BG, GREEN)
    txt(ax, 500, 66, 'Two domain agents', 14, GREEN_DARK, '500')
    txt(ax, 500, 86, 'AI GDS-Architect · Analog IC Architect', 12, GREEN)
    txt(ax, 500, 103, 'physics authority', 12, GREEN)

    # --- arrows into the referee ----------------------------------------
    M, L, Q = Path.MOVETO, Path.LINETO, Path.CURVE3
    curve(ax, [(180, 116), (180, 146), (180, 162), (200, 168), (288, 172)],
          [M, L, Q, Q, L], BLUE)
    curve(ax, [(500, 116), (500, 146), (500, 162), (480, 168), (392, 172)],
          [M, L, Q, Q, L], GREEN)
    txt(ax, 340, 150, 'on conflict, physics wins', 12, GREY)

    # --- row 2: the neutral referee --------------------------------------
    box(ax, 170, 182, 340, 64, SAND_BG, SAND)
    txt(ax, 340, 206, 'Gate chain — neutral referee', 14, SAND_DARK, '500')
    txt(ax, 340, 226, 'Magic · Netgen · SKY130A · Microlane', 12, SAND)

    # --- row 3: the evidence rule ----------------------------------------
    box(ax, 40, 270, 600, 52, RED_BG, RED)
    txt(ax, 340, 288, '"PASS" is a string. The log is the evidence.',
        14, RED_DARK, '500')
    txt(ax, 340, 307, 'Domain agent reads the log · QC reports the status · '
        'human signs', 12, RED)


def main():
    dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    fig = plt.figure(figsize=(W / 100.0, H / 100.0))
    ax = fig.add_axes([0, 0, 1, 1])
    draw(ax)
    fig.savefig(OUT, dpi=dpi, facecolor='white')
    plt.close(fig)
    print('WROTE %s (dpi=%d)' % (OUT, dpi))


if __name__ == '__main__':
    main()
