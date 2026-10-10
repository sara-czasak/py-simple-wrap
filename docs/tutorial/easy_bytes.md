# Easy Bytes

File sizes arrive as large numbers of bytes. `1536` is harder to read than
`1.5 KB`, and the other direction matters when a form asks you to type a
size. `easy_bytes` converts both ways and can tell you what percent of a
drive is full.

## A small real-world example

Imagine a homework folder that can hold 10 MB, and the files inside already
use 2.5 MB.

```python
from py_simple import bytes_to_human, human_to_bytes, percent_used

used = human_to_bytes("2.5 MB")
total = human_to_bytes("10 MB")

print(bytes_to_human(used))
print(percent_used(used, total))
```

Example output:

```text
2.5 MB
25.0
```

## What happened?

`human_to_bytes()` reads a label like `"2.5 MB"` and returns the byte count.

`bytes_to_human()` turns that count back into a short label. Whole numbers
drop the decimal, so `2048` bytes becomes `"2 KB"`.

`percent_used()` compares the two counts and returns the filled share rounded
to one decimal place.

## Why use these helpers?

Dividing by 1024 yourself is easy to get wrong once the unit climbs from KB
to MB to GB. These functions keep the unit list in one place and reject a
negative size or a unit they do not know.
