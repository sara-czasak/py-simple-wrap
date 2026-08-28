# Easy Archive

Backing up a small folder should not require learning the details of Python's
`zipfile` module. `easy_archive` provides straightforward helpers for creating,
inspecting, and extracting `.zip` files.

## A small real-world example

Imagine you want to send a week's notes to a teammate. Before sharing the
archive, you can check that it contains both files and then restore a copy to
confirm it opens correctly.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import list_zip_contents, unzip_file, zip_folder

with TemporaryDirectory() as workspace:
    source = Path(workspace) / "weekly_notes"
    source.mkdir()
    (source / "monday.txt").write_text("Plan the week.")
    (source / "friday.txt").write_text("Review the week.")

    archive = zip_folder(str(source), str(Path(workspace) / "weekly_notes.zip"))
    print(Path(archive).name)
    print(list_zip_contents(archive))

    restored = unzip_file(archive, str(Path(workspace) / "restored"))
    print(sorted(path.name for path in Path(restored).iterdir()))
```

Example output:

```text
weekly_notes.zip
['monday.txt', 'friday.txt']
['friday.txt', 'monday.txt']
```

## What happened?

`zip_folder()` collected every file in `weekly_notes` and created one archive.
It also keeps files in any subfolders, so it is useful for saving a small
project instead of only a single file.

`list_zip_contents()` let us check the archive before sharing it. If you only
need selected files rather than a whole folder, use `zip_files()` instead.

`unzip_file()` created the `restored` folder when needed and extracted the
archive into it. `is_zip_file()` is useful when you want to check a path before
trying to extract it, and `add_to_zip()` adds one more file to an archive that
already exists. If a path is missing or an archive is invalid, the helpers raise
`EasyArchiveError` with a clear explanation.

## Why use these helpers?

With the standard library, you need to create a `ZipFile`, choose the correct
mode, walk folders yourself, and create the extraction directory. These helpers
keep those steps behind descriptive function names, so a beginner can focus on
the files they want to save.
