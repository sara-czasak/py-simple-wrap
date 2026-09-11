"""
Drift checker for the Big Book of Modules.

MODULES.md is the source of truth for: icon, name, one-line summary,
category, and Docs/Tutorial links. data/modules.js duplicates all of that
(plus useCases, which has no source elsewhere and is never touched here).

This script does NOT rewrite modules.js. It reports where the two files
have drifted, so a human can fix modules.js by hand with full context -
same as the manual review that first caught the easy_random/easy_sql
mismatches.

Run with: python check_sync.py
Exit code is non-zero if any mismatch is found (usable in CI/pre-commit).
"""

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[3]
MODULES_MD = REPO_ROOT / "MODULES.md"
MODULES_JS = REPO_ROOT / "module-book" / "data" / "modules.js"

CATEGORY_ID_BY_HEADER = {
    "Files & data": "files-data",
    "Text & validation": "text-validation",
    "Numbers & math": "numbers-math",
    "Time & control flow": "time-flow",
    "Web & visuals": "web-visuals",
    "Fun & generators": "fun-generators",
}


def slug_id_from_name(name: str) -> str:
    words = name.split()
    if words and words[0].lower() == "easy":
        words = words[1:]
    return "easy_" + "_".join(w.lower() for w in words)


def parse_modules_md(text: str) -> dict:
    entries = {}
    current_category = None
    for line in text.splitlines():
        header_match = re.match(r"^## (.+)$", line)
        if header_match:
            current_category = CATEGORY_ID_BY_HEADER.get(header_match.group(1).strip())
            continue

        row_match = re.match(
            r"^\|\s*(\S+)\s+([A-Za-z0-9 ]+?)\s*\|\s*(.+?)\s*\|\s*"
            r"\[Docs\]\(([^)]+)\)\s*·\s*\[Tutorial\]\(([^)]+)\)\s*\|$",
            line,
        )
        if not row_match or current_category is None:
            continue

        icon, name, summary, docs_url, tutorial_url = row_match.groups()
        entries[slug_id_from_name(name)] = {
            "icon": icon,
            "name": name,
            "summary": summary.replace("`", ""),
            "category": current_category,
            "docs_url": docs_url,
            "tutorial_url": tutorial_url,
        }
    return entries


def parse_modules_js(text: str) -> dict:
    modules_section = text.split("modules: [", 1)[1]
    chunks = re.split(r"(?=\{\s*\n\s*id: \")", modules_section)

    entries = {}
    for chunk in chunks:
        id_match = re.search(r'id:\s*"([^"]+)"', chunk)
        if not id_match:
            continue
        name_match = re.search(r'name:\s*"([^"]+)"', chunk)
        icon_match = re.search(r'icon:\s*"([^"]+)"', chunk)
        category_match = re.search(r'category:\s*"([^"]+)"', chunk)
        summary_match = re.search(r'summary:\s*"([^"]*)"', chunk)
        docs_match = re.search(r'label:\s*"Docs".*?url:\s*"([^"]+)"', chunk, re.DOTALL)
        tutorial_match = re.search(
            r'label:\s*"Tutorial".*?url:\s*"([^"]+)"', chunk, re.DOTALL
        )

        entries[id_match.group(1)] = {
            "icon": icon_match.group(1) if icon_match else None,
            "name": name_match.group(1) if name_match else None,
            "summary": summary_match.group(1) if summary_match else None,
            "category": category_match.group(1) if category_match else None,
            "docs_url": docs_match.group(1) if docs_match else None,
            "tutorial_url": tutorial_match.group(1) if tutorial_match else None,
        }
    return entries


def main() -> int:
    md_entries = parse_modules_md(MODULES_MD.read_text(encoding="utf-8"))
    js_entries = parse_modules_js(MODULES_JS.read_text(encoding="utf-8"))

    problems = []

    for module_id, md_entry in md_entries.items():
        if module_id not in js_entries:
            problems.append(f"MISSING from modules.js: {module_id}")
            continue
        js_entry = js_entries[module_id]
        for field in ("icon", "summary", "category", "docs_url", "tutorial_url"):
            if md_entry[field] != js_entry[field]:
                problems.append(
                    f"MISMATCH {module_id}.{field}:\n"
                    f"    MODULES.md : {md_entry[field]!r}\n"
                    f"    modules.js : {js_entry[field]!r}"
                )

    for module_id in js_entries:
        if module_id not in md_entries:
            problems.append(f"EXTRA in modules.js, no MODULES.md row: {module_id}")

    if problems:
        print(f"Found {len(problems)} issue(s):\n")
        for p in problems:
            print(f"- {p}")
        return 1

    print("modules.js matches MODULES.md for all checked fields.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
