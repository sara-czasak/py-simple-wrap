"""Fetch today's star count for the repo and append it to the history file."""

import json
import os
from datetime import date
from pathlib import Path

import requests

REPO = os.environ.get("REPO", "sara-czasak/py-simple-wrap")
TOKEN = os.environ.get("GITHUB_TOKEN")
DATA_PATH = Path(".github/star-history.json")


def fetch_star_count() -> int:
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    response = requests.get(
        f"https://api.github.com/repos/{REPO}", headers=headers, timeout=10
    )
    response.raise_for_status()
    return response.json()["stargazers_count"]


def load_history() -> list[dict]:
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text())
    return []


def save_history(history: list[dict]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(history, indent=2))


def main() -> None:
    today = date.today().isoformat()
    star_count = fetch_star_count()
    history = load_history()

    # Replace today's entry if it already exists, otherwise append
    history = [entry for entry in history if entry["date"] != today]
    history.append({"date": today, "stars": star_count})
    history.sort(key=lambda entry: entry["date"])

    save_history(history)
    print(f"Recorded {star_count} stars for {today}")


if __name__ == "__main__":
    main()
