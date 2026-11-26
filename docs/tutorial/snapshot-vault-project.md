# Building a Snapshot Archive Vault with Easy Archive and Easy Hash

Combine **Easy Archive** and **Easy Hash** to package game save files, logs, or project configurations into a compressed snapshot and cryptographically verify its data integrity.

## What we are building

When backing up critical game state or application data, packaging files into a zip archive is only half the job. You also need to verify that the archive is intact, inspect its contents without manual decompression, and calculate an integrity checksum (such as SHA-256) so you can confirm later that the archive has not been corrupted or tampered with.

```python
import os
import shutil
import tempfile
from py_simple import (
    get_zip_file_count,
    hash_file,
    is_zip_file,
    list_zip_contents,
    verify_file_hash,
    zip_files,
)

# Set up sample game save files in a temporary folder
vault_dir = tempfile.mkdtemp()
save_file = os.path.join(vault_dir, "hero_save.json")
config_file = os.path.join(vault_dir, "settings.cfg")

with open(save_file, "w") as f:
    f.write('{"level": 42, "class": "Paladin", "gold": 9500}')
with open(config_file, "w") as f:
    f.write("difficulty=hard\nmusic_volume=80\n")

archive_path = os.path.join(vault_dir, "savegame_snapshot.zip")

# 1. Package files into a compressed zip snapshot
zip_files([save_file, config_file], archive_path)

# 2. Verify archive validity and inspect contents
print(f"Is valid archive: {is_zip_file(archive_path)}")
print(f"Archive item count: {get_zip_file_count(archive_path)}")
contents = list_zip_contents(archive_path)
print(f"Contained files: {contents}")

# 3. Compute cryptographic SHA-256 integrity checksum
archive_hash = hash_file(archive_path, algorithm="sha256")
print(f"Snapshot SHA-256: {archive_hash[:16]}...")

# 4. Verify integrity before restoration
is_intact = verify_file_hash(archive_path, archive_hash, algorithm="sha256")
print(f"Snapshot integrity verified: {is_intact}")

shutil.rmtree(vault_dir)
```

Example output:

```text
Is valid archive: True
Archive item count: 2
Contained files: ['hero_save.json', 'settings.cfg']
Snapshot SHA-256: 94638427ffa05ffc...
Snapshot integrity verified: True
```

## What happened?

1. `zip_files([save_file, config_file], archive_path)` bundles the target files into a compressed `.zip` archive at the designated output destination.
2. `is_zip_file(archive_path)` validates the archive header format to confirm it is a readable, uncorrupted zip file.
3. `get_zip_file_count(archive_path)` inspects the archive metadata and counts how many files are stored inside.
4. `list_zip_contents(archive_path)` extracts the member filenames without having to unpack the archive to disk.
5. `hash_file(archive_path, algorithm="sha256")` computes a cryptographic SHA-256 digest of the entire archive file.
6. `verify_file_hash(archive_path, archive_hash, algorithm="sha256")` recalculates the digest and compares it against the expected checksum, returning `True` when the file matches exactly.

## Why use these helpers?

Without `py-simple`, creating and verifying an archive requires juggling Python's standard `zipfile` module (managing context managers, writing relative arcnames, opening file handles) and the `hashlib` module (reading file chunks in binary mode, updating hasher states, and converting digests to hex strings).

`py_simple` unifies these into concise, single-line functions that handle file opening, error checking, and cleanup automatically—letting developers focus on the core workflow.
