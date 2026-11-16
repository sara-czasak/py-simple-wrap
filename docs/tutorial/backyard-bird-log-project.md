# Build a Backyard Bird Log with Easy CSV and Easy Lists

Combine **Easy CSV** and **Easy Lists** to turn a few bird sightings into
a quick summary of what you spotted.

## A small real-world example

You watched the yard on two mornings and wrote down a row each time you
spotted a bird. This example saves those notes in a temporary CSV, then
shows the species in the order you first spotted them and which one you
logged most often. The CSV is removed when the script finishes.

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import (
    most_common_item,
    read_csv_column,
    unique_items,
    write_csv_from_list,
)

sightings = [
    {"day": "Saturday", "species": "Robin"},
    {"day": "Saturday", "species": "Blue jay"},
    {"day": "Sunday", "species": "Robin"},
    {"day": "Sunday", "species": "Chickadee"},
]

with TemporaryDirectory() as workspace:
    log_file = str(Path(workspace) / "bird_sightings.csv")
    write_csv_from_list(log_file, sightings)
    species = read_csv_column(log_file, "species")

species_names = ", ".join(unique_items(species))
print(f"Total sightings: {len(species)}")
print(f"Species spotted: {species_names}")
print(f"Most logged species: {most_common_item(species)}")
```

Example output:

```text
Total sightings: 4
Species spotted: Robin, Blue jay, Chickadee
Most logged species: Robin
```

## What happened?

`write_csv_from_list()` uses the dictionary keys as column headers and
writes one row for each sighting. `read_csv_column()` reads just the
`species` column back, keeping both entries for Robin.

`unique_items()` removes the repeated Robin from the list you print.
It preserves the order of the first sighting of each species.

`most_common_item()` uses the original list so it can count both Robin
entries. If two species have the same highest count, it returns the one
you logged first.

## Try it yourself

Add a Blue jay sighting for Sunday. Blue jay and Robin now each appear
twice. Move the first Blue jay row above the first Robin row and run the
script again to see how the tie changes.

## Why use these helpers?

The standard-library version needs a CSV reader and writer, a way to
remove duplicates without losing order, and a counter. These helpers let
you focus on your sightings and the questions you want to ask about them.
See [Easy CSV](easy_csv.md) and [Easy Lists](easy_lists.md) for more examples.
