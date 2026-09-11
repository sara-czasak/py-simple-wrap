"""One-time backfill: reconstruct star history from GitHub's stargazers timestamp endpoint.

Uses the special `starred_at` media type to get the exact date each star was given.
If this fails (403/422), GitHub's restriction is still affecting this endpoint too —
fall back to manual entries in .github/star-history.json (see bottom of file).
"""

import json
import os
from collections import Counter
from pathlib import Path

import requests

REPO = os.environ.get("REPO", "sara-czasak/py-simple-wrap")
TOKEN = os.environ.get("GITHUB_TOKEN")
DATA_PATH = Path(".github/star-history.json")


def fetch_all_stargazers_with_dates() -> list[str]:
    headers = {"Accept": "application/vnd.github.star+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    dates = []
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/repos/{REPO}/stargazers",
            headers=headers,
            params={"per_page": 100, "page": page},
            timeout=15,
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        dates.extend(entry["starred_at"][:10] for entry in batch)
        page += 1
    return dates


def build_cumulative_history(star_dates: list[str]) -> list[dict]:
    counts = Counter(star_dates)
    running_total = 0
    history = []
    for day in sorted(counts):
        running_total += counts[day]
        history.append({"date": day, "stars": running_total})
    return history


def main() -> None:
    try:
        star_dates = fetch_all_stargazers_with_dates()
    except requests.HTTPError as exc:
        print(
            f"Backfill failed ({exc}). GitHub may still be restricting this endpoint."
        )
        print('Fall back to manual entries: {"date": "2026-06-01", "stars": 5}')
        return

    history = build_cumulative_history(star_dates)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(history, indent=2))
    print(f"Backfilled {len(history)} days from {len(star_dates)} stargazers.")


if __name__ == "__main__":
    main()
