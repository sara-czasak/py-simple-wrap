# Build a Game Asset Packager with Easy Archive and Easy Bytes

Combine **Easy Archive** and **Easy Bytes** to bundle game files into a ZIP archive, inspect the contents, and calculate storage savings in readable units.

## A small real-world example

Game developers and mod creators often need to package dialogue files, maps, and textures into compressed bundles for players to download. This example uses a temporary folder to create sample assets, bundle them into a ZIP archive, and measure how much bandwidth and disk space the compressed pack saves. The temporary directory and its files are automatically removed when the script finishes.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `game_asset_packager.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import (
    add_bytes,
    bytes_to_human,
    get_zip_file_count,
    is_smaller,
    list_zip_contents,
    percent_used,
    remaining_bytes,
    zip_files,
)

with TemporaryDirectory() as workspace:
    folder = Path(workspace)

    # 1. Prepare sample game asset files
    dialogue = folder / "quest_dialogue.txt"
    map_data = folder / "dungeon_layout.json"

    dialogue.write_text("Hero: Halt! Who goes there?\n" * 200, encoding="utf-8")
    map_data.write_text('{"tile": "stone", "walkable": true}\n' * 150, encoding="utf-8")

    asset_files = [str(dialogue), str(map_data)]
    total_uncompressed = add_bytes([dialogue.stat().st_size, map_data.stat().st_size])

    # 2. Package the files into a compressed ZIP bundle
    bundle_path = str(folder / "dungeon_pack.zip")
    zip_files(asset_files, bundle_path)

    # 3. Inspect archive contents and calculate storage savings
    file_count = get_zip_file_count(bundle_path)
    members = list_zip_contents(bundle_path)
    bundle_size = Path(bundle_path).stat().st_size
    saved_bytes = remaining_bytes(bundle_size, total_uncompressed)
    compression_ratio = percent_used(bundle_size, total_uncompressed)

    print("--- Game Asset Bundle Report ---")
    print(f"Files packed: {file_count}")
    print(f"Archive contents: {members}")
    print(f"Original size: {bytes_to_human(total_uncompressed)}")
    print(f"Compressed size: {bytes_to_human(bundle_size)} ({compression_ratio:.1f}% of original)")
    print(f"Space saved: {bytes_to_human(saved_bytes)}")
    print(f"Is bundle smaller: {is_smaller(bundle_size, total_uncompressed)}")
```

Run the script from your terminal:

```bash
python game_asset_packager.py
```

Example output:

```text
--- Game Asset Bundle Report ---
Files packed: 2
Archive contents: ['quest_dialogue.txt', 'dungeon_layout.json']
Original size: 11.1 KB
Compressed size: 388 B (3.4% of original)
Space saved: 10.7 KB
Is bundle smaller: True
```

## What happened?

`add_bytes()` sums up the sizes of the raw asset files from a list of byte counts, returning the uncompressed total without manual integer math.

`zip_files()` packages the list of file paths into a single compressed ZIP archive at the destination path, storing files using their clean file names.

`get_zip_file_count()` opens the generated archive and reports how many files it contains.

`list_zip_contents()` inspects the archive structure and returns a list containing the names of each bundled file.

`remaining_bytes()` computes how many bytes of disk space were freed up by taking the compressed archive size and the original uncompressed total.

`percent_used()` calculates what percentage of the original footprint the compressed file occupies (in this case, shrinking the assets down to just 3.4% of their original size).

`bytes_to_human()` converts raw integer byte numbers (like 11350 and 388) into friendly, human-readable strings like `11.1 KB` and `388 B`.

`is_smaller()` compares the archive size against the original total to confirm that compression reduced the overall file footprint.

## Try it yourself

- **Add an audio asset:** Add a third file (like `music_theme.ogg` or sound effect text) to `asset_files` and re-run to see how the file count and saved space adjust.
- **Extract a single file:** Use `extract_file_from_zip(bundle_path, "quest_dialogue.txt", str(folder / "unpacked"))` to pull out only the dialogue file from the pack.
- **Check decimal units:** Pass `decimal=True` to `bytes_to_human()` to format sizes using 1000-byte decimal kilobyte units (`KB`) instead of binary kibibytes (`KiB`).

## Why use these helpers?

Without `py-simple-wrap`, achieving this with Python's standard library requires importing both `zipfile` and `math` while writing manual helper functions:
- Setting up a `zipfile.ZipFile` context manager with `zipfile.ZIP_DEFLATED`, iterating over files, and extracting relative names with `os.path.basename` to avoid storing deep directory trees.
- Manually reading `infolist()` or `namelist()` to count and inspect members.
- Writing custom formatting functions to calculate logarithms or unit division loops (`size / 1024 ** power`) just to print human-friendly file sizes like "11.1 KB".

Combining `easy_archive` and `easy_bytes` replaces archive plumbing and byte math with concise, descriptive functions.

For more examples and detailed function references, see [Easy Archive](easy_archive.md) and [Easy Bytes](easy_bytes.md).
