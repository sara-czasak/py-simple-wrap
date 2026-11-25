# Build an RPG Inventory Loadout with Easy Dict and Easy Json

Combine **Easy Dict** and **Easy Json** to manage character gear, merge loot drops, upgrade weapons, and save game progress.

## A small real-world example

Game developers, text-adventure authors, and RPG hobbyists frequently need to manage character inventories, loot bags, and player stats. This example loads a character sheet from a temporary JSON save file, merges newly discovered dungeon loot into the bag, renames an upgraded weapon, sorts equipment by quantity, and safely checks nested combat stats. The sample uses Python's standard `tempfile.TemporaryDirectory` so it never leaves junk files behind on disk.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `rpg_inventory.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import (
    find_keys,
    get_nested_value,
    merge_dicts,
    open_json,
    rename_key,
    save_json_data,
    sort_dict_by_value,
)

with TemporaryDirectory() as workspace:
    save_dir = Path(workspace)
    save_file = save_dir / "character_sheet.json"

    # 1. Starting character sheet with equipment and nested combat attributes
    character = {
        "name": "Aria the Ranger",
        "gear": {
            "wooden_bow": 1,
            "leather_cap": 1,
            "health_potion": 3,
            "bread": 5,
        },
        "stats": {
            "combat": {
                "agility": 18,
                "stamina": 14,
            },
            "magic": {
                "mana": 5,
            },
        },
    }
    save_json_data(str(save_file), character)

    # 2. Load character data back from JSON
    loaded_data = open_json(str(save_file))

    # 3. Retrieve loot chest items and merge into player inventory
    loot_chest = {
        "arrows": 25,
        "health_potion": 5,
        "torch": 4,
    }
    current_gear = loaded_data["gear"]
    updated_gear = merge_dicts(current_gear, loot_chest)

    # 4. Upgrade starter weapon: rename wooden_bow to composite_bow
    upgraded_gear = rename_key(updated_gear, "wooden_bow", "composite_bow")

    # 5. Sort inventory items by quantity in descending order
    sorted_gear = sort_dict_by_value(upgraded_gear, reverse=True)

    # 6. Read nested attributes safely using dot notation
    agility = get_nested_value(loaded_data, "stats.combat.agility", default=0)
    stealth = get_nested_value(loaded_data, "stats.combat.stealth", default=10)

    # 7. Find all items where quantity equals 1 (unique single equipment pieces)
    single_items = find_keys(1, sorted_gear)

    print("=== RPG Character Inventory ===")
    print(f"Player: {loaded_data['name']}")
    print(f"Agility: {agility} | Stealth (defaulted): {stealth}")
    print("Organized Bag (by quantity):")
    for item, qty in sorted_gear.items():
        print(f"  - {item}: {qty}")
    print(f"Single equipped items: {single_items}")
```

Run the script from your terminal:

```bash
python rpg_inventory.py
```

Example output:

```text
=== RPG Character Inventory ===
Player: Aria the Ranger
Agility: 18 | Stealth (defaulted): 10
Organized Bag (by quantity):
  - arrows: 25
  - health_potion: 5
  - bread: 5
  - torch: 4
  - leather_cap: 1
  - composite_bow: 1
Single equipped items: ['leather_cap', 'composite_bow']
```

## What happened?

`save_json_data()` writes the initial character profile and nested inventory dictionary to a JSON file on disk, safeguarding against partial writes or accidental overwrites.

`open_json()` loads the character state back from disk into a native Python dictionary.

`merge_dicts()` combines the existing player equipment with new loot chest items, updating existing item quantities and adding new entries without mutating the original dictionary.

`rename_key()` upgrades `"wooden_bow"` to `"composite_bow"`, keeping the associated quantity while safely validating that the old item exists and the new item name is not already taken.

`sort_dict_by_value()` re-orders the bag in descending quantity order (`reverse=True`) so supplies and ammunition appear at the top.

`get_nested_value()` traverses nested dictionary structures using dot-separated keys (`"stats.combat.agility"`), cleanly falling back to a default value (`default=10`) when a stat key like `"stealth"` has not yet been unlocked.

`find_keys()` scans the dictionary for items matching a specific target value, identifying all single-quantity gear items currently in the loadout.

## Try it yourself

- **Invert dictionary for slot lookups:** Use `invert_dict()` on a character's equipped equipment slots (`{"head": "leather_cap", "weapon": "composite_bow"}`) to quickly look up which body slot holds a specific item name.
- **Track inventory item variety:** Use `count_values()` to count how many distinct items share each stack quantity.
- **Persist upgraded save:** Call `save_json_data()` with a new filename like `character_sheet_v2.json` to store the updated, sorted inventory.

## Why use these helpers?

Without `py-simple-wrap`, managing nested game data structures in Python requires considerable defensive boilerplate:
- Writing custom file-opening context managers (`with open(...) as f: json.dump(...)`) while manually checking for path collisions and serializing safely.
- Merging dictionaries with manual deep-copying (`copy.deepcopy()`) or dict unpacking (`{**dict_a, **dict_b}`) to prevent mutating shared state.
- Manually popping and reassigning keys (`d[new] = d.pop(old)`) while writing manual guards against missing keys or overwritten items.
- Writing chained `.get()` lookups (`data.get("stats", {}).get("combat", {}).get("agility")`) or `try...except (KeyError, TypeError)` blocks for deeply nested paths.
- Constructing `sorted(d.items(), key=lambda item: item[1], reverse=True)` lambda expressions and dictionary comprehensions just to filter or sort.

Combining `easy_dict` and `easy_json` eliminates this boilerplate, letting game builders manage and persist character states with clean, single-line helpers.

For more examples and detailed function references, see [Easy Dict](easy_dict.md) and [Easy Json](easy_json.md).
