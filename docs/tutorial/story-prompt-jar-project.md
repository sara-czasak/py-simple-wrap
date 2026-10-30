# Build a Story Prompt Jar

Stuck staring at a blank page? Combine **Easy Random** and **Easy JSON** to
pick a character, a setting and a challenge for a short story. Save the idea
so you can come back to it instead of losing it when the program closes.

## Set up the project

Use Python 3.11 or later. In a new project folder, install the package:

```bash
python -m pip install py-simple-wrap
```

The helpers used here are available in version 0.9.0. They use Python's
standard library, so this example does not need any optional extras or
an internet connection after installation.

## Build the jar

Save this as `story_jar.py` in your project folder:

```python
from pathlib import Path

from py_simple import open_json, pick_random_item, save_json_data

characters = ["curious robot", "sleepy dragon", "tiny detective"]
places = ["a floating library", "a moon garden", "an underwater bakery"]
challenges = [
    "find a missing key",
    "deliver a mysterious parcel",
    "stop a clock running backwards",
]

prompt_file = Path(__file__).resolve().with_name("story_prompt.json")

if prompt_file.exists():
    prompt = open_json(str(prompt_file))
    print("Back to your saved idea:")
else:
    prompt = {
        "character": pick_random_item(characters),
        "place": pick_random_item(places),
        "challenge": pick_random_item(challenges),
    }
    save_json_data(str(prompt_file), prompt)
    print("A new idea for your jar:")

print(f"A {prompt['character']} in {prompt['place']} must {prompt['challenge']}.")
```

Run it from that folder:

```bash
python story_jar.py
```

One first run produced this output. Your choices may be different:

```text
A new idea for your jar:
A tiny detective in an underwater bakery must deliver a mysterious parcel.
```

Run the script again and it loads the same idea from `story_prompt.json`.
The first line becomes `Back to your saved idea:`; the story starter stays
the same. Write a few sentences about what happens next!

To draw a new idea, delete only this example's `story_prompt.json` file and
run the script again. A new draw can still choose the same combination.

## What happened?

### Drawing three ingredients

`pick_random_item()` chooses one item from each list. The dictionary keeps
the three ingredients under descriptive keys, ready to save together.
Try adding your own characters and places, but keep each list nonempty:
choosing from an empty list raises `ValueError`.

### Keeping the idea

`save_json_data()` creates the JSON file beside `story_jar.py`, even if you
run the script from another directory. Its keys and string values are the
same ones in the `prompt` dictionary.

This helper refuses to overwrite an existing file. The `exists()` check
therefore sends later runs to `open_json()`, which reads the saved data
instead of drawing and saving another prompt. The example assumes the
saved file still has the three keys written by the script.

JSON stores data between runs; it does not run Python code. If you edit
the file, keep it valid JSON. Invalid JSON or a file that cannot be read
raises `EasyJsonError` from `py_simple.easy_json`. A failed save also raises
that error. The script lets these errors surface rather than replacing a
saved idea. Keep any writing you want to preserve somewhere safe before
deleting this example's file.

### Turning data into a story starter

The final f-string reads the dictionary's three keys to assemble one
sentence. On the first run it uses the newly generated dictionary; on
later runs it uses the dictionary loaded from disk.

## Try it yourself

- Add a new ingredient, such as a surprising object. Give it a list, a
  dictionary key and a place in the printed sentence. Delete the old
  example JSON before running your changed version so its saved keys match.
- Include characters or places in another language. JSON preserves the
  strings when they are loaded again, even if the file shows Unicode escapes.
- Write a different ending for the same saved prompt each time you return.

## Why use these helpers?

Without these helpers, you would call `random.choice()` and write the JSON
file-opening, encoding and serialization code yourself. Here you can focus
on the little creative loop: draw an idea, keep it, and return to write.

For more examples, see [Easy Random](easy_random.md) and
[Easy JSON](easy_json.md).
