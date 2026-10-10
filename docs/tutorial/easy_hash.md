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
