"""
easy_bytes turns byte counts into readable sizes and back.
"""


class EasyBytesError(Exception):
    """
    Raised when a size cannot be converted.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


_UNITS = ("B", "KB", "MB", "GB", "TB")


def bytes_to_human(num_bytes: int) -> str:
    """
    Turn a byte count into a short label such as `"1.5 KB"`.

    Args:
        num_bytes (int): Number of bytes. Must be zero or greater.

    Returns:
        str: A size label using B, KB, MB, GB, or TB.

    Raises:
        EasyBytesError: If `num_bytes` is not a non-negative integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import bytes_to_human

            print(bytes_to_human(1536))
            ```

        === "The Traditional Way"
            ```python
            size = 1536
            label = f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} B"
            ```
    """
    if isinstance(num_bytes, bool) or not isinstance(num_bytes, int) or num_bytes < 0:
        raise EasyBytesError("\n\nERROR: num_bytes must be a non-negative integer.")

    size = float(num_bytes)
    unit = _UNITS[0]
    for name in _UNITS:
        unit = name
        if size < 1024 or name == _UNITS[-1]:
            break
        size /= 1024

    if unit == "B":
        return f"{int(size)} B"
    rounded = round(size, 1)
    if rounded == int(rounded):
        return f"{int(rounded)} {unit}"
    return f"{rounded} {unit}"


def human_to_bytes(label: str) -> int:
    """
    Turn a size label such as `"1.5 KB"` back into a byte count.

    Args:
        label (str): A number plus a unit: B, KB, MB, GB, or TB.

    Returns:
        int: The size in bytes.

    Raises:
        EasyBytesError: If `label` is not a recognized size.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import human_to_bytes

            print(human_to_bytes("1.5 KB"))
            ```

        === "The Traditional Way"
            ```python
            number, unit = "1.5 KB".split()
            print(int(float(number) * 1024))
            ```
    """
    if not isinstance(label, str):
        raise EasyBytesError("\n\nERROR: label must be a string.")
    parts = label.strip().split()
    if len(parts) != 2:
        raise EasyBytesError("\n\nERROR: use a form like '1.5 KB'.")
    number_text, unit = parts
    if unit not in _UNITS:
        raise EasyBytesError("\n\nERROR: unit must be B, KB, MB, GB, or TB.")
    try:
        number = float(number_text)
    except ValueError as error:
        raise EasyBytesError(f"\n\nERROR: {error}") from None
    if number < 0:
        raise EasyBytesError("\n\nERROR: size cannot be negative.")
    multiplier = 1024 ** _UNITS.index(unit)
    return int(number * multiplier)


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
            raise EasyBytesError("\n\nERROR: used and total must be non-negative integers.")
    if total < 1:
        raise EasyBytesError("\n\nERROR: total must be at least 1.")
    return round(used / total * 100, 1)
