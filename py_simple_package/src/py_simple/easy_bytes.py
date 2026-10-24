"""
easy_bytes turns byte counts into readable sizes and back.
"""

import math


class EasyBytesError(Exception):
    """
    Raised when a size cannot be converted.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

_DECIMAL_UNITS = ("B", "KB", "MB", "GB", "TB") # decimal units (1000-based)
_BINARY_UNITS = ("B", "KiB", "MiB", "GiB", "TiB") # binary units (1024-based)


# how many bytes are in each unit, for both decimal and binary units
_MULTIPLIERS = {
    **{unit: 1000 ** power for power, unit in enumerate(_DECIMAL_UNITS)},
    **{unit: 1024 ** power for power, unit in enumerate(_BINARY_UNITS)},
}


def bytes_to_human(num_bytes: int, binary: bool = False) -> str:
    """
    Turn a byte count into a short label such as `"1.5 KB"`.

    Args:
        num_bytes (int): Number of bytes. Must be zero or greater.
        binary (bool): When `False` (the default value), use decimal units (KB, MB, GB, TB) where 1 KB is 1000 bytes.\n
                       When `True`, use binary units (KiB, MiB, GiB, TiB) where 1 KiB is 1024 bytes.

    Returns:
        str: A size label using B, KB, MB, GB, or TB (or KiB, MiB, GiB, TiB when `binary` is `True`).

    Raises:
        EasyBytesError: If `num_bytes` is not a non-negative integer, or if `binary` is not a boolean.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import bytes_to_human

            print(bytes_to_human(1500))
            print(bytes_to_human(1536, binary=True))
            ```

        === "The Traditional Way"
            ```python
            size = 1500
            label = f"{size / 1000:.1f} KB" if size >= 1000 else f"{size} B"

            size = 1536
            label = f"{size / 1024:.1f} KiB" if size >= 1024 else f"{size} B"
            ```
    """
    if isinstance(num_bytes, bool) or not isinstance(num_bytes, int) or num_bytes < 0:
        raise EasyBytesError(
            "\n\nERROR: num_bytes must be a non-negative integer."
        ) from None

    if not isinstance(binary, bool):
        raise EasyBytesError(
            "\n\nERROR: binary must be a boolean (True or False)."
        ) from None

    units = _BINARY_UNITS if binary else _DECIMAL_UNITS
    base = 1024 if binary else 1000

    size = float(num_bytes)
    unit = units[0]
    for name in units:
        unit = name
        if size < base or name == units[-1]:
            break
        size /= base

    if unit == "B":
        return f"{int(size)} B"
    rounded = round(size, 1)
    if rounded == int(rounded):
        return f"{int(rounded)} {unit}"
    return f"{rounded} {unit}"


def human_to_bytes(label: str) -> int:
    """
    Turn a size label such as `"1.5 KB"` back into a byte count.

    Decimal units (KB, MB, GB, TB) use factors of 1000, so `"1 KB"` is 1000 bytes.
    Binary units (KiB, MiB, GiB, TiB) use factors of 1024, so `"1 KiB"` is 1024 bytes.

    Args:
        label (str): A number plus a unit: B, KB, MB, GB, TB, KiB, MiB, GiB or TiB.

    Returns:
        int: The size in bytes.

    Raises:
        EasyBytesError: If `label` is not a recognized size or does not
            convert to a finite byte count.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import human_to_bytes

            print(human_to_bytes("1.5 KB"))
            print(human_to_bytes("1.5 KiB"))
            ```

        === "The Traditional Way"
            ```python
            number, unit = "1.5 KB".split()
            print(int(float(number) * 1000))

            number, unit = "1.5 KiB".split()
            print(int(float(number) * 1024))
            ```
    """
    if not isinstance(label, str):
        raise EasyBytesError("\n\nERROR: label must be a string.") from None
    parts = label.strip().split()
    if len(parts) != 2:
        raise EasyBytesError("\n\nERROR: use a form like '1.5 KB'.") from None
    number_text, unit = parts
    if unit not in _MULTIPLIERS:
        raise EasyBytesError("\n\nERROR: unit must be B, KB, MB, GB, TB, KiB, MiB, GiB, or TiB.") from None
    try:
        number = float(number_text)
    except ValueError as error:
        raise EasyBytesError(f"\n\nERROR: {error}") from None
    if number < 0:
        raise EasyBytesError("\n\nERROR: size cannot be negative.") from None
    size_in_bytes = number * _MULTIPLIERS[unit]
    if not math.isfinite(size_in_bytes):
        raise EasyBytesError(
            "\n\nERROR: size must convert to a finite byte count."
        ) from None
    return int(size_in_bytes)


def percent_used(used: int, total: int) -> float:
    """
    Report how much of a storage total is already used.

    Args:
        used (int): Bytes already used.
        total (int): Bytes available in total. Must be greater than 0.

    Returns:
        float: The used share as a percent, rounded to one decimal place.

    Raises:
        EasyBytesError: If the numbers are not valid byte counts, or if
            `total` is not positive.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import percent_used

            print(percent_used(250, 1000))
            ```

        === "The Traditional Way"
            ```python
            print(round(250 / 1000 * 100, 1))
            ```
    """
    for value in (used, total):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise EasyBytesError(
                "\n\nERROR: used and total must be non-negative integers."
            ) from None
    if total < 1:
        raise EasyBytesError("\n\nERROR: total must be at least 1.") from None
    return round(used / total * 100, 1)


def add_bytes(values: list) -> int:
    """
    Add up a list of sizes and return the total in bytes.

    Each value is either an integer (already a byte count) or a size label such as `"1 KB"` (1000 bytes)
    or `"1 KiB"` (1024 bytes).

    Args:
        values (list): Byte counts (non-negative integers) and/or size labels. A tuple is accepted too. An empty list adds up to 0.

    Returns:
        int: The sum of all the values, in bytes.

    Raises:
        EasyBytesError: If `values` is not a list, if an item is neither a non-negative integer nor a string, or if a string is not a valid size label.

    Example:
        === "The Py_simple Way"
        ```python
            from py_simple import add_bytes

            print(add_bytes([512, "1 KB", "1 KiB"]))
        ```

        === "The Traditional Way"
        ```python
            total = 512 + int(float("1") * 1000) + int(float("1") * 1024)
            print(total)
        ```
    """
    if not isinstance(values, (list, tuple)):
        raise EasyBytesError("\n\nERROR: values must be a list or a tuple.")

    total = 0
    for value in values:
        if isinstance(value, str):
            total += human_to_bytes(value)
        elif isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            total += value
        else:
            raise EasyBytesError("\n\nERROR: each value must be a non-negative integer or a size string.") from None
    return total