# Build a Club Badge with Easy Colors and Easy JSON

Combine **Easy Colors** and **Easy JSON** to pick ink and paper colors
for a club badge, check that they contrast, and save the choice.

## A small real-world example

A club needs a dark ink on a light card. This example writes a temporary
JSON file, so you can run it repeatedly without replacing a real badge
file. The folder is removed when the example ends.

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import contrast_ratio, is_light_color, open_json, save_json_data

ink = "#1B4D3E"
paper = "#F4EFE6"
badge = {
    "ink": ink,
    "paper": paper,
    "ink_is_light": is_light_color(ink),
    "paper_is_light": is_light_color(paper),
    "contrast": round(contrast_ratio(ink, paper), 2),
}

with TemporaryDirectory() as workspace:
    path = str(Path(workspace) / "club_badge.json")
    save_json_data(path, badge)
    saved = open_json(path)
    print(saved["ink"], saved["paper"], saved["contrast"])
```

Example output:

```text
#1B4D3E #F4EFE6 8.42
```

## What happened?

`is_light_color()` says the ink is dark and the paper is light, using
perceived brightness rather than a guess from the hex code.

`contrast_ratio()` returns `8.42`. A ratio of 4.5 or more is the usual
bar for readable body text; 8.42 clears that.

`save_json_data()` writes the badge once and refuses to overwrite an
existing file. `open_json()` reads it back as a dictionary.

## Try it yourself

Swap the ink for `"#88AA99"` and print the new contrast. If it drops
below 4.5, pick a darker ink.

## Why use these helpers?

The standard-library version needs luminance math and a JSON dump with
an exists-check. These helpers let you focus on the useful sequence:
choose colors, check contrast, save the badge. For more examples, see
[Easy Colors](easy_colors.md) and [Easy JSON](easy_json.md).
