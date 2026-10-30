# Build a Backup Checker with Easy Archive and Easy Hash

Combine **Easy Archive** and **Easy Hash** to zip a note, restore it, and
check whether the restored contents match the original. This is a small
practice version of checking that a backup can actually be read back.

## A small real-world example

Imagine saving your game ideas before editing them. This example creates
its own temporary folder, so you can run it repeatedly without replacing
your real notes. The folder and its files are removed when the example ends.

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import extract_file_from_zip, hash_file, verify_file_hash, zip_files

with TemporaryDirectory() as workspace:
    folder = Path(workspace)
    note = folder / "ideas.txt"
    note.write_text("Build a moon garden game.\n", encoding="utf-8")
    original_checksum = hash_file(str(note))

    archive = zip_files([str(note)], str(folder / "ideas.zip"))
    restored = extract_file_from_zip(archive, "ideas.txt", str(folder / "restored"))

    print("Restored note matches:", verify_file_hash(restored, original_checksum))

    Path(restored).write_text("Build an underwater garden game.\n", encoding="utf-8")
    print("Edited note matches:", verify_file_hash(restored, original_checksum))
```

Example output:

```text
Restored note matches: True
Edited note matches: False
```

## What happened?

`hash_file()` records a SHA-256 checksum of the original file's bytes.
Keep this value from before editing: calculating a new checksum after
changing the file would give you a different baseline.

`zip_files()` puts the note into a ZIP archive. With this single input,
the archive member is named `ideas.txt`, without its temporary parent path.
`extract_file_from_zip()` restores that member into a separate directory
and returns the restored file's path. We extract only the archive we just
created in this example.

`verify_file_hash()` compares the restored file with the saved checksum.
The first check succeeds. After we change the restored note, the second
check fails. A missing or unreadable file raises `EasyHashError` rather
than returning `False`; `False` means the checksum did not match.

## Try it yourself

Add another note to the list passed to `zip_files()`. Record its checksum,
restore it by its own filename, and check that one too. Keep filenames
distinct so each archive member is easy to identify.

## Why use these helpers?

The standard-library version needs ZIP member handling and checksum
calculation code. These helpers let you focus on the useful sequence:
save a baseline, archive, restore, and compare. For more examples, see
[Easy Archive](easy_archive.md) and [Easy Hash](easy_hash.md).
