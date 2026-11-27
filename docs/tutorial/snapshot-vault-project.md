# Build a Snapshot Archive Vault with Easy Archive and Easy Hash

Combine **Easy Archive** and **Easy Hash** to package game save files, logs, or project configurations into a compressed snapshot and cryptographically verify its data integrity.

## A small real-world example

When backing up critical game state or application data, packaging files into a zip archive is only half the job. You also need to verify that the archive is intact, inspect its contents without manual decompression, and calculate an integrity checksum (such as SHA-256) so you can confirm later that the archive has not been corrupted or tampered with.

This project creates sample game configuration files inside an isolated temporary directory, bundles them into a zip archive, computes a baseline checksum, and confirms that subsequent tampering is detected.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `snapshot_vault.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import (
    get_zip_file_count,
    hash_file,
    is_zip_file,
    list_zip_contents,
    verify_file_hash,
    zip_files,
)

with TemporaryDirectory() as workspace:
    vault = Path(workspace)
    save_file = vault / "hero_save.json"
    config_file = vault / "settings.cfg"

    save_file.write_text(
        '{"level": 42, "class": "Paladin", "gold": 9500}\n', encoding="utf-8"
    )
    config_file.write_text("difficulty=hard\nmusic_volume=80\n", encoding="utf-8")

    archive_path = vault / "savegame_snapshot.zip"

    # 1. Package files into a compressed zip snapshot
    zip_files([str(save_file), str(config_file)], str(archive_path))

    # 2. Verify archive validity and inspect contents
    print("Is valid archive:", is_zip_file(str(archive_path)))
    print("Archive item count:", get_zip_file_count(str(archive_path)))
    print("Contained files:", list_zip_contents(str(archive_path)))

    # 3. Compute cryptographic SHA-256 integrity checksum at creation time
    # Store this baseline digest (e.g., in a database or cloud manifest)
    baseline_checksum = hash_file(str(archive_path), algorithm="sha256")
    print(f"Computed SHA-256 digest ({len(baseline_checksum)} characters)")

    # 4. Verify integrity later: confirms the archive has not been corrupted
    print(
        "Snapshot intact before modification:",
        verify_file_hash(str(archive_path), baseline_checksum),
    )

    # 5. Simulate file corruption or bit rot
    with open(archive_path, "ab") as f:
        f.write(b"\x00tampered_bytes")

    print(
        "Snapshot intact after tampering:",
        verify_file_hash(str(archive_path), baseline_checksum),
    )
```

Run the script from your terminal:

```bash
python snapshot_vault.py
```

Example output:

```text
Is valid archive: True
Archive item count: 2
Contained files: ['hero_save.json', 'settings.cfg']
Computed SHA-256 digest (64 characters)
Snapshot intact before modification: True
Snapshot intact after tampering: False
```

## What happened?

`zip_files([str(save_file), str(config_file)], str(archive_path))` bundles the files into a `.zip` archive at the destination path without manual zipfile handling.

`is_zip_file(str(archive_path))` inspects the file signature and header to confirm that the file is an authentic, readable ZIP archive.

`get_zip_file_count(str(archive_path))` returns the number of archive members without extracting the files.

`list_zip_contents(str(archive_path))` lists the filenames preserved inside the archive.

`hash_file(str(archive_path), algorithm="sha256")` computes a 64-character SHA-256 cryptographic digest of the archive bytes. Because zip metadata (such as timestamps) varies across environments and creation times, saving this baseline hash at creation time is essential for later verification.

`verify_file_hash(str(archive_path), baseline_checksum)` recalculates the file digest and compares it against the recorded baseline. It returns `True` when the archive is unaltered, and `False` if any bytes have been corrupted or tampered with.

## Try it yourself

- **Extract and inspect:** Use `extract_file_from_zip()` from `Easy Archive` to restore just `hero_save.json` to verify its json content independently.
- **Compare multiple hash algorithms:** Call `hash_file(..., algorithm="md5")` or `"sha512"` to experiment with different cryptographic standards.
- **Automate snapshot rotation:** Use `open_dir()` and `list_files()` from `Easy File Manager` to automatically bundle and checksum all files in an active game save directory.

## Why use these helpers?

Without `py-simple`, creating and verifying an archive requires juggling Python's standard `zipfile` module (managing context managers, writing relative arcnames, opening file handles) and the `hashlib` module (reading file chunks in binary mode, updating hasher states, and converting digests to hex strings).

`py_simple` unifies these into concise, single-line functions that handle file opening, error checking, and cleanup automatically—letting developers focus on the core workflow.

For more examples and detailed function references, see [Easy Archive](easy_archive.md) and [Easy Hash](easy_hash.md).
