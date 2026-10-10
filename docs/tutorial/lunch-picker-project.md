# Building a Lunch Picker with Easy CSV and Easy Random

Combine **Easy CSV** and **Easy Random** to keep a short lunch menu in a
spreadsheet and pick one meal without staring at the list.

## What we are building

A class list of lunches is easier to edit in a CSV than inside the program.
This small script writes that menu, reads it back, and chooses one row at
random.

```python
from py_simple import pick_random_item, read_csv_to_list, write_csv_from_list

lunches = [
    {"meal": "Pasta", "side": "Apple"},
    {"meal": "Rice bowl", "side": "Carrots"},
    {"meal": "Sandwich", "side": "Yogurt"},
]

write_csv_from_list("lunches.csv", lunches)
rows = read_csv_to_list("lunches.csv")
choice = pick_random_item(rows)

print(f"{choice['meal']} with {choice['side']}")
```

Example output (one of the three meals):

```text
Rice bowl with Carrots
```

## What happened?

1. `write_csv_from_list()` saves the menu as `lunches.csv`, using the
   dictionary keys as column names.
2. `read_csv_to_list()` loads that file back into a list of dictionaries, so
   each lunch still has a `meal` and a `side`.
3. `pick_random_item()` chooses one of those dictionaries. Run the script
   again and you may get a different lunch.

## Why use these helpers?

Writing and reading CSV usually means opening the file, creating a
`DictWriter`, and remembering `newline=""`. Picking a random row means
importing `random` and calling `choice`. Here the script stays on the task:
save the menu, read it, pick one.
