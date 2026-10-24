# Easy Bytes

File sizes arrive as large numbers of bytes. `1500` is harder to read than
`1.5 KB`, and the other direction matters when a form asks you to type a
size. `easy_bytes` converts both ways, adds sizes together, and can tell you
what percent of a drive is full.

## Two families of units

Sizes come in two flavors, and the unit name tells you which one you get:

| Unit  | Bytes                | Family  |
| ----- | -------------------- | ------- |
| `B`   | 1                    | both    |
| `KB`  | 1,000                | decimal |
| `MB`  | 1,000,000            | decimal |
| `GB`  | 1,000,000,000        | decimal |
| `TB`  | 1,000,000,000,000    | decimal |
| `KiB` | 1,024                | binary  |
| `MiB` | 1,048,576            | binary  |
| `GiB` | 1,073,741,824        | binary  |
| `TiB` | 1,099,511,627,776    | binary  |

Units are case-sensitive: `"1 kb"` and `"1 kib"` are rejected.

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

## Adding sizes together

`add_bytes()` takes a list that mixes plain byte counts and size labels, and
returns the total in bytes.

```python
from py_simple import add_bytes, bytes_to_human

total = add_bytes([512, "1 KB", "1 KiB"])

print(total)
print(bytes_to_human(total))
```

Example output:

```text
2536
2.5 KB
```

Here `512` is already a byte count, `"1 KB"` is 1000 bytes, and `"1 KiB"` is
1024 bytes.

## What happened?

`human_to_bytes()` reads a label like `"2.5 MB"` and returns the byte count.
`KB`, `MB`, `GB` and `TB` count in thousands, while `KiB`, `MiB`, `GiB` and
`TiB` count in 1024s. A fractional result is cut down to whole bytes, so
`"0.1 KiB"` becomes `102`.

`bytes_to_human()` turns a count back into a short label. It uses decimal
units by default. Pass `binary=True` to get `KiB`, `MiB`, `GiB` and `TiB`
instead. Whole numbers drop the decimal, so `2000` bytes becomes `"2 KB"`
and `2048` bytes with `binary=True` becomes `"2 KiB"`.

```python
from py_simple import bytes_to_human

print(bytes_to_human(1536))
print(bytes_to_human(1536, binary=True))
```

```text
1.5 KB
1.5 KiB
```

`add_bytes()` converts each string with `human_to_bytes()` first, then adds
everything up. Each item must be a non-negative whole number or a valid size
label. An empty list adds up to `0`.

`percent_used()` compares the two counts and returns the filled share rounded
to one decimal place.

## Why use these helpers?

Mixing up 1000 and 1024 is easy once the unit climbs from KB to MB to GB.
These functions keep the unit list in one place, tell `KB` and `KiB` apart,
and reject a negative size, a unit they do not know, or an item that is not a
number or a size label.