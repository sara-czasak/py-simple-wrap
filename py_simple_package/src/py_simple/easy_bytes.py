"""
easy_bytes turns byte counts into readable sizes and back.
"""

import math
from decimal import MAX_EMAX, MIN_EMIN, Context, Decimal


class EasyBytesError(Exception):
    """
    Raised when a size cannot be converted.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


_KB_UNITS = ("B", "KB", "MB", "GB", "TB")  # KB-style names
_KIB_UNITS = ("B", "KiB", "MiB", "GiB", "TiB")  # KiB-style names (always 1024)

_UNITS = _KB_UNITS + _KIB_UNITS[1:]  # Every accepted unit name

# How many bytes are in each unit. KiB-style names always mean 1024. KB-style
# names mean 1024 by default (the original behavior) and 1000 when the caller
# asks for decimal units.
_KIB_MULTIPLIERS = {unit: 1024**power for power, unit in enumerate(_KIB_UNITS)}
_LEGACY_MULTIPLIERS = {
    **{unit: 1024**power for power, unit in enumerate(_KB_UNITS)},
    **_KIB_MULTIPLIERS,
}
_DECIMAL_MULTIPLIERS = {
    **{unit: 1000**power for power, unit in enumerate(_KB_UNITS)},
    **_KIB_MULTIPLIERS,
}


def _check_flag(name: str, value) -> None:
    """Raise `EasyBytesError` unless `value` is a real boolean."""
    if not isinstance(value, bool):
        raise EasyBytesError(
            f"\n\nERROR: {name} must be a boolean (True or False)."
        ) from None


def _scale_to_bytes(number_text: str, multiplier: int) -> int:
    """
    Multiply a numeric string by `multiplier` without float rounding loss.

    The product is computed exactly with `Decimal`, so `"1.001"` times 1000 is
    1001 and not 1000.9999999999999. Any real fractional byte is truncated.
    Raises `EasyBytesError` if `Decimal` cannot represent the number.
    """
    context = Context(
        prec=len(number_text) + len(str(multiplier)) + 2,
        Emax=MAX_EMAX,
        Emin=MIN_EMIN,
    )
    try:
        return int(context.multiply(Decimal(number_text), multiplier))
    except ArithmeticError:
        # Decimal cannot represent some extreme inputs, such as an exponent
        # with hundreds of digits, even though float() accepted them.
        raise EasyBytesError(
            "\n\nERROR: size could not be converted to a whole byte count."
        ) from None


def bytes_to_human(num_bytes: int, binary: bool = False, decimal: bool = False) -> str:
    """
    Turn a byte count into a short label such as `"1.5 KB"`.

    By default, `KB`, `MB`, `GB` and `TB` count in factors of 1024, as they
    always have. Use `binary=True` to get the same numbers spelled with `KiB`,
    `MiB`, `GiB` and `TiB`, or `decimal=True` to count in factors of 1000.

    Args:
        num_bytes (int): Number of bytes. Must be zero or greater.
        binary (bool): When `True`, label the size with `KiB`, `MiB`, `GiB` and
            `TiB` (1 KiB is 1024 bytes). Defaults to `False`.
        decimal (bool): When `True`, use decimal units where 1 KB is 1000
            bytes. Defaults to `False`, where 1 KB is 1024 bytes. Cannot be
            combined with `binary=True`.

    Returns:
        str: A size label using B, KB, MB, GB, or TB (or KiB, MiB, GiB, TiB
            when `binary` is `True`).

    Raises:
        EasyBytesError: If `num_bytes` is not a non-negative integer, if
            `binary` or `decimal` is not a boolean, or if both are `True`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import bytes_to_human

            print(bytes_to_human(1536))
            print(bytes_to_human(1536, binary=True))
            print(bytes_to_human(1500, decimal=True))
            ```

        === "The Traditional Way"
            ```python
            size = 1536
            label = f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} B"

            size = 1536
            label = f"{size / 1024:.1f} KiB" if size >= 1024 else f"{size} B"

            size = 1500
            label = f"{size / 1000:.1f} KB" if size >= 1000 else f"{size} B"
            ```
    """
    if isinstance(num_bytes, bool) or not isinstance(num_bytes, int) or num_bytes < 0:
        raise EasyBytesError(
            "\n\nERROR: num_bytes must be a non-negative integer."
        ) from None
    _check_flag("binary", binary)
    _check_flag("decimal", decimal)
    if binary and decimal:
        raise EasyBytesError(
            "\n\nERROR: binary and decimal cannot both be True."
        ) from None

    units = _KIB_UNITS if binary else _KB_UNITS
    base = 1000 if decimal else 1024

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


def human_to_bytes(label: str, decimal: bool = False) -> int:
    """
    Turn a size label such as `"1.5 KB"` back into a byte count.

    By default, `KB`, `MB`, `GB` and `TB` count in factors of 1024, as they
    always have, so `"1 KB"` is 1024 bytes. `KiB`, `MiB`, `GiB` and `TiB`
    always count in factors of 1024. Pass `decimal=True` to make `KB`, `MB`,
    `GB` and `TB` count in factors of 1000 instead, so `"1 KB"` is 1000 bytes.
    A fractional byte is truncated.

    Args:
        label (str): A number plus a unit: B, KB, MB, GB, TB, KiB, MiB, GiB
            or TiB.
        decimal (bool): When `True`, `KB`-style units use factors of 1000.
            Defaults to `False`.

    Returns:
        int: The size in bytes.

    Raises:
        EasyBytesError: If `label` is not a recognized size, does not
            convert to a finite byte count, or if `decimal` is not a boolean.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import human_to_bytes

            print(human_to_bytes("1.5 KB"))
            print(human_to_bytes("1.5 KB", decimal=True))
            print(human_to_bytes("1.5 KiB"))
            ```

        === "The Traditional Way"
            ```python
            number, unit = "1.5 KB".split()
            print(int(float(number) * 1024))

            number, unit = "1.5 KB".split()
            print(int(float(number) * 1000))

            number, unit = "1.5 KiB".split()
            print(int(float(number) * 1024))
            ```
    """
    _check_flag("decimal", decimal)
    if not isinstance(label, str):
        raise EasyBytesError("\n\nERROR: label must be a string.") from None
    parts = label.strip().split()
    if len(parts) != 2:
        raise EasyBytesError("\n\nERROR: use a form like '1.5 KB'.") from None
    number_text, unit = parts
    multipliers = _DECIMAL_MULTIPLIERS if decimal else _LEGACY_MULTIPLIERS
    if unit not in multipliers:
        raise EasyBytesError(
            "\n\nERROR: unit must be B, KB, MB, GB, TB, KiB, MiB, GiB, or TiB."
        ) from None
    try:
        number = float(number_text)
    except ValueError as error:
        raise EasyBytesError(f"\n\nERROR: {error}") from None
    if number < 0:
        raise EasyBytesError("\n\nERROR: size cannot be negative.") from None
    multiplier = multipliers[unit]
    # The float is only used to validate the input (nan, inf, overflow). The
    # actual byte count is computed exactly below.
    if not math.isfinite(number * multiplier):
        raise EasyBytesError(
            "\n\nERROR: size must convert to a finite byte count."
        ) from None
    return _scale_to_bytes(number_text, multiplier)


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


def remaining_bytes(used: int, total: int) -> int:
    """
    Calculates how many bytes remain in a storage total.

    Args:
        used (int): Bytes already used. Must be a non-negative integer
            no greater than `total`.
        total (int): Total capacity in bytes. Must be a non-negative integer.

    Returns:
        int: Unused bytes, such as 750 for 250 used out of 1000.
            A zero-capacity or full storage total has zero remaining bytes.

    Raises:
        EasyBytesError: If either count is negative, is not an integer,
            is a boolean, or if `used` exceeds `total`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import remaining_bytes

            print(remaining_bytes(250, 1000))
            ```

        === "The Traditional Way"
            ```python
            used = 250
            total = 1000
            print(total - used)
            ```
    """
    for value in (used, total):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise EasyBytesError(
                "\n\nERROR: used and total must be non-negative integers."
            ) from None
    if used > total:
        raise EasyBytesError("\n\nERROR: used cannot exceed total.") from None
    return total - used


def add_bytes(values: list, decimal: bool = False) -> int:
    """
    Add up a list of sizes and return the total in bytes.

    Each value is either an integer (already a byte count) or a size label
    such as `"1 KiB"` (1024 bytes). Labels such as `"1 KB"` follow the same
    rule as `human_to_bytes`: 1024 bytes by default, or 1000 bytes with
    `decimal=True`.

    Args:
        values (list): Byte counts (non-negative integers) and/or size
            labels. A tuple is accepted too. An empty list adds up to 0.
        decimal (bool): When `True`, `KB`-style units use factors of 1000.
            Defaults to `False`.

    Returns:
        int: The sum of all the values, in bytes.

    Raises:
        EasyBytesError: If `values` is not a list or a tuple, if an item is
            neither a non-negative integer nor a string, if a string is not
            a valid size label, or if `decimal` is not a boolean.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import add_bytes

            print(add_bytes([512, "1 KB", "1 KiB"]))
            print(add_bytes([512, "1 KB", "1 KiB"], decimal=True))
            ```

        === "The Traditional Way"
            ```python
            print(512 + 1024 + 1024)
            print(512 + 1000 + 1024)
            ```
    """
    _check_flag("decimal", decimal)
    if not isinstance(values, (list, tuple)):
        raise EasyBytesError("\n\nERROR: values must be a list or a tuple.") from None

    total = 0
    for value in values:
        if isinstance(value, str):
            total += human_to_bytes(value, decimal=decimal)
        elif isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            total += value
        else:
            raise EasyBytesError(
                "\n\nERROR: each value must be a non-negative integer or a size string."
            ) from None
    return total


def percent_free(used: int, total: int) -> float:
    """
    Report how much of a storage total is still free.

    Args:
        used (int): Bytes already used. Must be a non-negative integer
            no greater than `total`.
        total (int): Bytes available in total. Must be greater than 0.

    Returns:
        float: The free share as a percent, rounded to one decimal place.

    Raises:
        EasyBytesError: If the numbers are not valid byte counts, if
            `total` is not positive, or if `used` exceeds `total`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import percent_free

            print(percent_free(250, 1000))
            ```

        === "The Traditional Way"
            ```python
            used = 250
            total = 1000
            print(round((total - used) / total * 100, 1))
            ```
    """
    for value in (used, total):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise EasyBytesError(
                "\n\nERROR: used and total must be non-negative integers."
            ) from None
    if total < 1:
        raise EasyBytesError("\n\nERROR: total must be at least 1.") from None
    if used > total:
        raise EasyBytesError("\n\nERROR: used cannot exceed total.") from None
    return round((total - used) / total * 100, 1)


def average_bytes(values: list, decimal: bool = False) -> int:
    """
    Return the average size of a list of sizes, in bytes.

    Each value is either an integer (already a byte count) or a size label
    such as `"1 KiB"` (1024 bytes). Labels such as `"1 KB"` follow the same
    rule as `human_to_bytes`: 1024 bytes by default, or 1000 bytes with
    `decimal=True`. The average is a whole byte count, so a fractional
    average is truncated, and each label is converted to bytes first, the
    same way `add_bytes` converts it.

    Args:
        values (list): Byte counts (non-negative integers) and/or size
            labels. A tuple is accepted too. Must not be empty.
        decimal (bool): When `True`, `KB`-style units use factors of 1000.
            Defaults to `False`.

    Returns:
        int: The average of all the values, in bytes.

    Raises:
        EasyBytesError: If `values` is not a list or a tuple, if it is
            empty, if an item is neither a non-negative integer nor a
            string, if a string is not a valid size label, or if
            `decimal` is not a boolean.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import average_bytes

            print(average_bytes([512, "1 KB", "1 KiB"]))
            print(average_bytes([512, "1 KB", "1 KiB"], decimal=True))
            ```

        === "The Traditional Way"
            ```python
            print((512 + 1024 + 1024) // 3)
            print((512 + 1000 + 1024) // 3)
            ```
    """
    _check_flag("decimal", decimal)
    if not isinstance(values, (list, tuple)):
        raise EasyBytesError("\n\nERROR: values must be a list or a tuple.") from None
    if len(values) == 0:
        raise EasyBytesError("\n\nERROR: values must not be empty.") from None
    return add_bytes(values, decimal=decimal) // len(values)


def is_larger(a: int | str, b: int | str, decimal: bool = False) -> bool:
    """
    Check if size `a` is strictly larger than size `b`.

    Each size can be a non-negative integer (byte count) or a size label
    such as `"1.5 GB"`.

    Args:
        a (int | str): First size (byte count or label like `"1.5 GB"`).
        b (int | str): Second size to compare against (byte count or label).
        decimal (bool): When `True`, `KB`-style units use factors of 1000.
            Defaults to `False`.

    Returns:
        bool: `True` if `a` is strictly greater than `b`, `False` otherwise.

    Raises:
        EasyBytesError: If `a` or `b` cannot be converted to bytes, or if
            `decimal` is not a boolean.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_larger

            print(is_larger("1.5 GB", "1000 MB"))  # Returns True
            print(is_larger("500 B", "1 KB"))      # Returns False
            ```

        === "The Traditional Way"
            ```python
            size_a = 1.5 * 1024 * 1024 * 1024
            size_b = 1000 * 1024 * 1024
            print(size_a > size_b)
            ```
    """

    _check_flag("decimal", decimal)

    bytes_a = (
        a
        if isinstance(a, int) and not isinstance(a, bool) and a >= 0
        else human_to_bytes(a, decimal=decimal)
    )
    bytes_b = (
        b
        if isinstance(b, int) and not isinstance(b, bool) and b >= 0
        else human_to_bytes(b, decimal=decimal)
    )

    return bytes_a > bytes_b


def is_smaller(a: int | str, b: int | str, decimal: bool = False) -> bool:
    """
    Check if size `a` is strictly smaller than size `b`.

    Each size can be a non-negative integer (byte count) or a size label
    such as `"500 MB"`.

    Args:
        a (int | str): First size (byte count or label like `"500 MB"`).
        b (int | str): Second size to compare against (byte count or label).
        decimal (bool): When `True`, `KB`-style units use factors of 1000.
            Defaults to `False`.

    Returns:
        bool: `True` if `a` is strictly less than `b`, `False` otherwise.

    Raises:
        EasyBytesError: If `a` or `b` cannot be converted to bytes, or if
            `decimal` is not a boolean.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_smaller

            print(is_smaller("500 B", "1 KB"))     # Returns True
            print(is_smaller("1.5 GB", "1000 MB")) # Returns False
            ```

        === "The Traditional Way"
            ```python
            size_a = 500
            size_b = 1024
            print(size_a < size_b)
            ```
    """

    _check_flag("decimal", decimal)

    bytes_a = (
        a
        if isinstance(a, int) and not isinstance(a, bool) and a >= 0
        else human_to_bytes(a, decimal=decimal)
    )
    bytes_b = (
        b
        if isinstance(b, int) and not isinstance(b, bool) and b >= 0
        else human_to_bytes(b, decimal=decimal)
    )

    return bytes_a < bytes_b
