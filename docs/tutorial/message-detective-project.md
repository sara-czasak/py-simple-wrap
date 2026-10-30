# Build a Message Detective with Easy Base64 and Easy Hash

Combine **Easy Base64** and **Easy Hash** in a tiny clue-solving game:
decode a message, then spot a changed clue using its original checksum.

## A small real-world example

Your detective club has a meeting place hidden in a Base64 clue. Someone
has changed the destination! Keep a checksum of the original message so
you can check which version matches.

Base64 is an encoding anyone can reverse, not encryption. This is a
learning game, so use a fictional message rather than a real secret.

Install the package with `python -m pip install py-simple-wrap`, then save
this as `message_detective.py` and run `python message_detective.py`.
It works entirely in memory and does not create files or contact a service.

```python
from py_simple import decode_text, encode_text, hash_text, hashes_match

original_clue = "Meet at the moon garden."
original_checksum = hash_text(original_clue)
encoded_clue = encode_text(original_clue)

decoded_clue = decode_text(encoded_clue)
print("Encoded clue:", encoded_clue)
print("Decoded clue:", decoded_clue)
print("Original clue matches:", hashes_match(decoded_clue, original_checksum))

# Change the clue, but keep the checksum from before the edit.
changed_clue = decoded_clue.replace("moon", "star")
print("Changed clue:", changed_clue)
print("Changed clue matches:", hashes_match(changed_clue, original_checksum))
```

Example output:

```text
Encoded clue: TWVldCBhdCB0aGUgbW9vbiBnYXJkZW4u
Decoded clue: Meet at the moon garden.
Original clue matches: True
Changed clue: Meet at the star garden.
Changed clue matches: False
```

## What happened?

`hash_text()` records a SHA-256 checksum, a fingerprint of the original
text. Keep that value: making a new checksum after editing the clue would
replace the baseline you are trying to compare against.

`encode_text()` turns the clue into Base64 text. `decode_text()` reverses
that encoding, giving back the original sentence. Both helpers handle
UTF-8, so clues can contain accented letters and other Unicode characters.

`hashes_match()` compares the text with the saved checksum. The decoded
clue matches; replacing `moon` with `star` makes the second check return
`False`. Spaces, punctuation and letter case also affect the checksum.

A plain checksum alone does not prove who sent a message. If someone
replaces both the message and the expected checksum, they can make the
check pass. This example detects a change against a baseline you already
trust; it does not authenticate a sender or keep the clue private.

## Try it yourself

Change `original_clue` to `"Meet at the moon café."` and run it again.
The decoded text should keep the accent, and the changed destination
should still fail the checksum check.

Next, replace the `changed_clue = ...` line with
`changed_clue = decoded_clue.replace(".", "!")`. Changing only punctuation
should also give `False`. Keep using the original checksum for each
comparison.

## Why use these helpers?

With Python's `base64` and `hashlib` modules, you would convert text to
bytes, encode or hash it, and convert the results back to strings. These
helpers handle those steps so you can focus on the game: prepare a clue,
decode it, and check for changes. See [Easy Base64](easy_base64.md) and
[Easy Hash](easy_hash.md) for more examples.
