# Easy Hash

A checksum is a short fingerprint of some text or a file. People use one to
notice when a download changed or when a note was edited. Building that
fingerprint with `hashlib` means remembering encoder names and hex output.
`easy_hash` names the job directly.

## A small real-world example

Imagine you saved a class note and want a fingerprint you can compare later.
If the fingerprint changes, the file changed.

```python
from py_simple import hash_file, hash_text, hashes_match

note = "Bring a pencil and a notebook"
fingerprint = hash_text(note)

print(fingerprint)
print(hashes_match(note, fingerprint))
print(hash_file("notes.txt"))
```

`hash_file("notes.txt")` reads whatever is in that file. The other two lines
work on the sentence itself.

## What happened?

`hash_text()` turns the sentence into a SHA-256 checksum.

`hashes_match()` compares a sentence with a checksum you already have, and
accepts uppercase or lowercase hex.

`hash_file()` does the same job for a file on disk. You can pass `"md5"` or
`"sha1"` when a tool asks for that kind of checksum instead.

## Check a file against a checksum

`verify_file_hash()` compares a file with an expected checksum. It reads in
64 KiB chunks, so a large file does not need to fit in memory.

```python
from pathlib import Path
from py_simple import verify_file_hash

Path("notes.txt").write_bytes(b"hello")
expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

print(verify_file_hash("notes.txt", expected))  # True
print(verify_file_hash("notes.txt", "0" * 64))  # False
```

Pass a string path or a `pathlib.Path`, and use `algorithm="sha1"` or
`algorithm="md5"` if that is how the expected checksum was made. Hex letters
can be uppercase or lowercase. Non-string or malformed checksums return
`False`; surrounding whitespace is not stripped. A non-string checksum
returns `False` before the file or algorithm is checked. With a string
checksum, missing/unreadable files and unsupported algorithms raise
`EasyHashError`, just as `hash_file()` does.

Checksums help detect changed contents. Compare against a checksum from a
trusted source; a matching checksum alone does not prove who made the file.

## Why use these helpers?

The usual version is a few steps every time:

```python
import hashlib

fingerprint = hashlib.sha256(note.encode("utf-8")).hexdigest()
same = fingerprint == expected.lower()
```

`easy_hash` keeps the algorithm choice in one argument and raises a clear
error when the file is missing or the algorithm name is not one of the three
it supports.
