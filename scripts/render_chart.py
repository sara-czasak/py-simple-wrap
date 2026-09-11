"""Render .github/star-history.json into a full-width, animated SVG line chart."""

import json
import math
from pathlib import Path

DATA_PATH = Path(".github/star-history.json")
OUTPUT_PATH = Path("assets/star-history.svg")

WIDTH, HEIGHT = 1000, 280
PADDING_X, PADDING_Y = 24, 40


def load_history() -> list[dict]:
    return json.loads(DATA_PATH.read_text())


def build_svg(history: list[dict]) -> str:
    if not history:
        return "<svg xmlns='http://www.w3.org/2000/svg'></svg>"

    stars = [entry["stars"] for entry in history]
    dates = [entry["date"] for entry in history]
    max_stars = max(stars) or 1
    min_stars = min(stars)
    star_range = max(max_stars - min_stars, 1)

    plot_w = WIDTH - 2 * PADDING_X
    plot_h = HEIGHT - 2 * PADDING_Y
    n = len(history)

    def point(i: int, value: int) -> tuple[float, float]:
        x = PADDING_X + (i / max(n - 1, 1)) * plot_w
        y = HEIGHT - PADDING_Y - ((value - min_stars) / star_range) * plot_h
        return x, y

    points = [point(i, s) for i, s in enumerate(stars)]
    polyline_points = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

    # total path length, for the draw-on animation
    total_length = (
        sum(math.dist(points[i], points[i + 1]) for i in range(len(points) - 1)) or 1
    )

    circles = "\n".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#2f81f7">'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{(i / max(n - 1, 1)) * 2:.2f}s" dur="0.2s" fill="freeze" />'
        f"</circle>"
        for i, (x, y) in enumerate(points)
    )

    first_date, last_date = dates[0], dates[-1]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="{HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#0d1117" rx="8" />
  <text x="{PADDING_X}" y="24" fill="#c9d1d9" font-family="sans-serif" font-size="14">
    py-simple-wrap star history
  </text>
  <polyline points="{polyline_points}" fill="none" stroke="#2f81f7" stroke-width="2"
    stroke-dasharray="{total_length:.1f}" stroke-dashoffset="{total_length:.1f}">
    <animate attributeName="stroke-dashoffset" from="{total_length:.1f}" to="0"
      dur="2s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" />
  </polyline>
  {circles}
  <text x="{PADDING_X}" y="{HEIGHT - 10}" fill="#8b949e" font-family="sans-serif" font-size="11">{first_date}</text>
  <text x="{WIDTH - PADDING_X - 70}" y="{HEIGHT - 10}" fill="#8b949e" font-family="sans-serif" font-size="11">{last_date}</text>
  <text x="{PADDING_X}" y="{PADDING_Y - 10}" fill="#8b949e" font-family="sans-serif" font-size="11">{max_stars} stars</text>
</svg>"""
    return svg


def main() -> None:
    history = load_history()
    svg = build_svg(history)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(svg)
    print(f"Wrote chart to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
