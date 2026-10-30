# Easy Bytes

File sizes arrive as large numbers of bytes. `1536` is harder to read than
`1.5 KB`, and the other direction matters when a form asks you to type a
size. `easy_bytes` converts both ways, adds sizes together, and can tell you
what percent of a drive is full or how many bytes remain.

## Which units mean what

By default, `KB`, `MB`, `GB` and `TB` count in factors of 1024. This is how
`easy_bytes` has always worked, so existing code keeps returning the same
numbers. The `KiB`, `MiB`, `GiB` and `TiB` units are also accepted, and they
mean exactly the same thing as the default `KB`-style units.

If you need `KB` to mean 1000 bytes (the way drive makers and many websites
count), pass `decimal=True`.

| Unit  | Default           | With `decimal=True` |
| ----- | ----------------- | ------------------- |
| `B`   | 1                 | 1                   |
| `KB`  | 1,024             | 1,000               |
| `MB`  | 1,048,576         | 1,000,000           |
| `GB`  | 1,073,741,824     | 1,000,000,000       |
| `TB`  | 1,099,511,627,776 | 1,000,000,000,000   |
| `KiB` | 1,024             | 1,024               |
| `MiB` | 1,048,576         | 1,048,576           |
| `GiB` | 1,073,741,824     | 1,073,741,824       |
| `TiB` | 1,099,511,627,776 | 1,099,511,627,776   |

Units are case-sensitive: `"1 kb"` and `"1 kib"` are rejected.

## A small real-world example

Imagine a homework folder that can hold 10 MB, and the files inside already
use 2.5 MB.

```python
from py_simple import (
    bytes_to_human,
    human_to_bytes,
    percent_free,
    percent_used,
    remaining_bytes,
)

used = human_to_bytes("2.5 MB")
total = human_to_bytes("10 MB")

print(bytes_to_human(used))
print(percent_used(used, total))
print(percent_free(used, total))
print(bytes_to_human(remaining_bytes(used, total)))
```

Example output:

```text
2.5 MB
25.0
75.0
7.5 MB
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
2560
2.5 KB
```

Here `512` is already a byte count, and `"1 KB"` and `"1 KiB"` are both 1024 bytes,
in order to preserve beckwards compatibility. To count `"1 KB"` as 1000 bytes, pass `decimal=True`.
The `decimal=True` parameter only works with values such as `KB, MB, GB and TB`.
`KiB, MiB, GiB and TiB` are binary by default, so the `decimal=True` parameter doesn't affect them.
Here's an example:

```python
from py_simple import add_bytes

print(add_bytes([512, "1 KB", "1 KiB"], decimal=True))
```

```text
2536
```

## Averaging sizes together

`average_bytes()` takes the same kind of list as `add_bytes()` and
returns the average size in bytes. A fractional average is truncated to a
whole byte count.

```python
from py_simple import average_bytes, bytes_to_human

average = average_bytes([512, "1 KB", "1 KiB"])

print(average)
print(bytes_to_human(average))
```

Example output:

```text
853
853 B
```

## Comparing two sizes

`is_smaller()` and `is_larger()` answer a yes-or-no question: is one size
strictly smaller (or larger) than the other? Each side can be a plain byte
count or a size label, and both sides can be different kinds.

```python
from py_simple import is_smaller, is_larger

print(is_smaller("500 B", "1 KB"))
print(is_smaller("1.5 GB", "1000 MB"))
print(is_larger("1.5 GB", "1000 MB"))
print(is_larger("500 B", "1 KB"))
```

Example output:

```text
True
False
True
False
```

Both functions take the same optional `decimal=True` switch as the rest of
the module, and it works the same way: it changes what `KB`-style units mean,
and leaves `KiB`-style units alone. This is a good way to see the difference:

```python
from py_simple import is_smaller

print(is_smaller("1 KB", "1 KiB"))
print(is_smaller("1 KB", "1 KiB", decimal=True))
```

```text
False
True
```

By default `"1 KB"` and `"1 KiB"` are both 1024 bytes, so neither is smaller.
With `decimal=True`, `"1 KB"` drops to 1000 bytes while `"1 KiB"` stays at
1024, so the first one is now smaller.

## What happened?

`human_to_bytes()` reads a label like `"2.5 MB"` and returns the byte count.
The scaling is exact, so `"1.001 KB"` is `1001` bytes with `decimal=True`.
A real fractional byte is cut off, so `"0.1 KiB"` becomes `102`.

`bytes_to_human()` turns a count back into a short label. Whole numbers drop
the decimal, so `2048` bytes becomes `"2 KB"`. It has two optional switches:

```python
from py_simple import bytes_to_human

print(bytes_to_human(1536))
print(bytes_to_human(1536, binary=True))
print(bytes_to_human(1500, decimal=True))
```

```text
1.5 KB
1.5 KiB
1.5 KB
```

`binary=True` writes the same numbers with `KiB`, `MiB`, `GiB` and `TiB`.
`decimal=True` counts in thousands instead. The two cannot be combined.

`add_bytes()` converts each string with `human_to_bytes()` first, then adds
everything up. Each item must be a non-negative whole number or a valid size
label, and the input must be a list or a tuple. An empty list adds up to `0`.

`average_bytes()` works on the same kind of list, but divides the total by
how many items there are. An empty list raises `EasyBytesError`, since an
average of nothing is undefined.

`percent_used()` compares the two counts and returns the filled share rounded
to one decimal place.

`percent_free()` returns the percentage of capacity still free.

`remaining_bytes()` subtracts used bytes from the total. It accepts whole,
non-negative byte counts, including a total of zero when usage is also zero.
Booleans and usage greater than the total raise `EasyBytesError` instead of
returning a misleading count. A full storage total returns zero.

`is_smaller()` and `is_larger()` convert both sides to bytes and compare them.
They are strict: two equal sizes are neither smaller nor larger, so both
return `False`. A size that cannot be converted raises `EasyBytesError`, the
same as everywhere else in the module.

## Why use these helpers?

Mixing up 1000 and 1024 is easy once the unit climbs from KB to MB to GB.
These functions keep the unit list in one place, let you choose which one you
mean, and reject a negative size, a unit they do not know, or an item that is
not a number or a size label.
