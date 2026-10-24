import pytest
import re

from py_simple_package.src.py_simple.easy_bytes import (
    EasyBytesError,
    bytes_to_human,
    human_to_bytes,
    percent_used,
    add_bytes,
)


@pytest.mark.parametrize(
    "num_bytes, expected",
    [
        (0, "0 B"),
        (1, "1 B"),
        (999, "999 B"),
        (1000, "1 KB"),
        (1001, "1 KB"),
        (1500, "1.5 KB"),
        (1549, "1.5 KB"),
        (1551, "1.6 KB"),
        (1999, "2 KB"),
        (2000, "2 KB"),
        (999 * 1000, "999 KB"),
        (10**6, "1 MB"),
        (999 * 10**6, "999 MB"),
        (10**9, "1 GB"),
        (999 * 10**9, "999 GB"),
        (10**12, "1 TB"),
        (1500 * 10**9, "1.5 TB"),
        (10**15, "1000 TB"),
    ],
)
def test_bytes_to_human(num_bytes, expected):
    """Use decimal units by default, one decimal place, and no useless zero."""
    assert bytes_to_human(num_bytes) == expected


@pytest.mark.parametrize(
    "num_bytes, expected",
    [
        (0, "0 B"),
        (1, "1 B"),
        (1000, "1000 B"),
        (1023, "1023 B"),
        (1024, "1 KiB"),
        (1025, "1 KiB"),
        (1536, "1.5 KiB"),
        (1587, "1.5 KiB"),
        (1588, "1.6 KiB"),
        (2047, "2 KiB"),
        (2048, "2 KiB"),
        (1023 * 1024, "1023 KiB"),
        (1024**2, "1 MiB"),
        (1023 * 1024**2, "1023 MiB"),
        (1024**3, "1 GiB"),
        (1023 * 1024**3, "1023 GiB"),
        (1024**4, "1 TiB"),
        (1536 * 1024**3, "1.5 TiB"),
        (1024**5, "1024 TiB"),
    ],
)
def test_bytes_to_human_binary(num_bytes, expected):
    """With binary=True, use IEC units where each step is 1024."""
    assert bytes_to_human(num_bytes, binary=True) == expected


def test_bytes_to_human_binary_false_matches_default():
    """Passing binary=False explicitly is the same as the default."""
    assert bytes_to_human(1500, binary=False) == bytes_to_human(1500) == "1.5 KB"


@pytest.mark.parametrize("num_bytes", [-1, True, False, 1.0, 1.5, "1024", None, [], {}])
@pytest.mark.parametrize("binary", [False, True])
def test_bytes_to_human_rejects_bad_input(num_bytes, binary):
    """Byte counts must be non-negative integers, excluding booleans."""
    with pytest.raises(
        EasyBytesError, match="num_bytes must be a non-negative integer"
    ):
        bytes_to_human(num_bytes, binary=binary)


@pytest.mark.parametrize("binary", [0, 1, "yes", None, [], 1.0])
def test_bytes_to_human_rejects_bad_binary_flag(binary):
    """The binary flag must be a real boolean."""
    with pytest.raises(EasyBytesError, match=re.escape("binary must be a boolean (True or False).")):
        bytes_to_human(1024, binary=binary)


@pytest.mark.parametrize(
    "label, expected",
    [
        ("0 B", 0),
        ("1 B", 1),
        ("512 B", 512),
        ("1.5 B", 1),

        # decimal units: factors of 1000.
        ("1 KB", 1000),
        ("0.1 KB", 100),
        ("1.5 KB", 1500),
        ("2 KB", 2000),
        ("1 MB", 10**6),
        ("1.5 MB", 1_500_000),
        ("1 GB", 10**9),
        ("1.5 GB", 1_500_000_000),
        ("1 TB", 10**12),
        ("1.5 TB", 1_500_000_000_000),
        ("0 TB", 0),

        # binary units: factors of 1024.
        ("1 KiB", 1024),
        ("0.1 KiB", 102),
        ("1.5 KiB", 1536),
        ("2 KiB", 2048),
        ("1 MiB", 1048576),
        ("1.5 MiB", 1572864),
        ("1 GiB", 1073741824),
        ("1.5 GiB", 1610612736),
        ("1 TiB", 1099511627776),
        ("1.5 TiB", 1649267441664),
        ("0 TiB", 0),

        # whitespace handling.
        ("  1.5 KB  ", 1500),
        ("  1.5 KiB  ", 1536),
        ("\t1.5\t KB\n", 1500),
        ("\t1.5\t KiB\n", 1536),

        # very large values.
        ("1267650600228229401496703205376 B", 2**100),
        ("1267650600228229401496703205376 TiB", 2**140),
        (f"{2**1023} B", 2**1023),
    ],
)
def test_human_to_bytes(label, expected):
    """Read supported units and whitespace, returning a whole byte count."""
    result = human_to_bytes(label)
    assert result == expected
    assert isinstance(result, int)


def test_human_to_bytes_decimal_and_binary_differ():
    """KB and KiB (and so on) must not be mixed up."""
    units  = [("KB", "KiB"), ("MB", "MiB"), ("GB", "GiB"), ("TB", "TiB")]
    for decimal, binary in units:
        assert human_to_bytes(f"1 {decimal}") < human_to_bytes(f"1 {binary}")


@pytest.mark.parametrize("label", [None, 1024, 1.5, True, False, [], {}])
def test_human_to_bytes_rejects_non_string(label):
    """Reject non-string labels with the module's exception."""
    with pytest.raises(EasyBytesError, match="label must be a string"):
        human_to_bytes(label)


@pytest.mark.parametrize(
    "label", ["", "  ", "lots", "1.5", "KB", "1.5KB", "1.5KiB", "1 KB extra"]
)
def test_human_to_bytes_rejects_bad_label(label):
    """A label must contain a number and a separate unit."""
    with pytest.raises(EasyBytesError, match="use a form like '1.5 KB'"):
        human_to_bytes(label)


@pytest.mark.parametrize(
    "label", ["5 XB", "1 kb", "1 mb", "1 kib", "1 KIB", "1 Kib", "1 KiKB", "1 PiB"]
)
def test_human_to_bytes_rejects_unknown_unit(label):
    """Only the documented units, with exact capitalization, are supported."""
    with pytest.raises(
        EasyBytesError,
        match="unit must be B, KB, MB, GB, TB, KiB, MiB, GiB, or TiB",
    ):
        human_to_bytes(label)


@pytest.mark.parametrize("label", ["many KB", "1.2.3 MB", "--1 B", "many KiB"])
def test_human_to_bytes_rejects_malformed_number(label):
    """Invalid numeric text should be wrapped in EasyBytesError."""
    with pytest.raises(EasyBytesError, match="could not convert string to float"):
        human_to_bytes(label)


@pytest.mark.parametrize(
    "label",
    ["-1 B", "-0.5 KB", "-0.5 KiB", "-inf KB", "-Infinity TB", "-1e309 MB"],
)
def test_human_to_bytes_rejects_negative_size(label):
    """Reject negative sizes, including fractional ones."""
    with pytest.raises(EasyBytesError, match="size cannot be negative"):
        human_to_bytes(label)


@pytest.mark.parametrize(
    "label",
    [
        "nan KB",
        "NaN B",
        "+nan MB",
        "-NaN GB",
        "nan KiB",
        "inf KB",
        "inf KiB",
        "+inf B",
        "Infinity MB",
        "+INFINITY GB",
        "1e309 KB",
        "1e309 TB",
        "1e309 TiB",
        "  NaN\tKB\n",
    ],
)
def test_human_to_bytes_rejects_nonfinite_size(label):
    """Non-finite numeric labels must use the public conversion error."""
    with pytest.raises(
        EasyBytesError, match="size must convert to a finite byte count"
    ):
        human_to_bytes(label)


@pytest.mark.parametrize("unit", ["KB", "MB", "GB", "TB", "KiB", "MiB", "GiB", "TiB"])
def test_human_to_bytes_rejects_scaled_overflow(unit):
    """A finite number can still overflow when scaled to bytes."""
    with pytest.raises(
        EasyBytesError, match="size must convert to a finite byte count"
    ):
        human_to_bytes(f"1e308 {unit}")


@pytest.mark.parametrize(
    "values, expected",
    [
        ([], 0),
        ([0], 0),
        ([1024], 1024),
        ([1, 2, 3], 6),
        (["0 B"], 0),
        (["512 B"], 512),
        (["1 KB"], 1000),
        (["1 KiB"], 1024),
        (["1 KB", "1 KiB"], 2024),
        (["1.5 KB", "1.5 KiB"], 1500 + 1536),
        ([512, "1 KB", "1.5 KiB"], 512 + 1000 + 1536),
        (["  2 MB  ", 1], 2_000_001),
        (["1 MB", "1 MiB"], 10**6 + 1024**2),
        (["1 GB", "1 GiB"], 10**9 + 1024**3),
        (["1 TB", "1 TiB"], 10**12 + 1024**4),
        ([2**100, "1 B"], 2**100 + 1),
        ([10, 20, "30 B"], 60),
        ((1, "1 KB"), 1001),
    ],
)
def test_add_bytes(values, expected):
    """Sum ints and size labels into a single whole byte count."""
    result = add_bytes(values)
    assert result == expected
    assert isinstance(result, int)


def test_add_bytes_truncates_each_label_before_summing():
    """Each label is converted to whole bytes first, then added."""
    # "0.1 KiB" is 102.4 bytes -> 102, so three of them give 306, not 307.
    assert add_bytes(["0.1 KiB", "0.1 KiB", "0.1 KiB"]) == 306


def test_add_bytes_does_not_modify_input():
    """The caller's list must be left untouched."""
    values = [1, "1 KB", "1 KiB"]
    add_bytes(values)
    assert values == [1, "1 KB", "1 KiB"]


@pytest.mark.parametrize("values", [None, 5, 1.5, "1 KB", b"1 KB", {}, {1: 2}, {1, 2}])
def test_add_bytes_rejects_non_list(values):
    """A bare string must not be iterated character by character."""
    with pytest.raises(EasyBytesError, match="values must be a list"):
        add_bytes(values)


@pytest.mark.parametrize(
    "bad_item", [-1, True, False, 1.0, 1.5, None, [], {}, b"1 KB", ["1 KB"]]
)
def test_add_bytes_rejects_bad_item(bad_item):
    """Items must be non-negative ints (not bools) or strings."""
    with pytest.raises(
        EasyBytesError,
        match="each value must be a non-negative integer or a size string",
    ):
        add_bytes([1, bad_item])


@pytest.mark.parametrize(
    "bad_label, message",
    [
        ("lots", "use a form like '1.5 KB'"),
        ("1.5", "use a form like '1.5 KB'"),
        ("1 XB", "unit must be B, KB, MB, GB, TB, KiB, MiB, GiB, or TiB"),
        ("1 kib", "unit must be B, KB, MB, GB, TB, KiB, MiB, GiB, or TiB"),
        ("many KB", "could not convert string to float"),
        ("-1 KB", "size cannot be negative"),
        ("inf KiB", "size must convert to a finite byte count"),
        ("1e308 TiB", "size must convert to a finite byte count"),
    ],
)
def test_add_bytes_propagates_label_errors(bad_label, message):
    """Invalid labels raise the same error human_to_bytes would raise."""
    with pytest.raises(EasyBytesError, match=message):
        add_bytes([1, bad_label])


@pytest.mark.parametrize(
    "used, total, expected",
    [
        (0, 1000, 0.0),
        (0, 1, 0.0),
        (1, 1, 100.0),
        (1000, 1000, 100.0),
        (250, 1000, 25.0),
        (1, 3, 33.3),
        (2, 3, 66.7),
        (1, 8, 12.5),
        (1500, 1000, 150.0),
    ],
)
def test_percent_used(used, total, expected):
    """Return the used share as a float rounded to one decimal place."""
    result = percent_used(used, total)
    assert result == expected
    assert isinstance(result, float)


@pytest.mark.parametrize("invalid", [-1, True, False, 1.0, 1.5, "1", None, [], {}])
@pytest.mark.parametrize("argument", ["used", "total"])
def test_percent_used_rejects_bad_input(invalid, argument):
    """Validate each byte count independently, excluding booleans."""
    counts = {"used": 1, "total": 100}
    counts[argument] = invalid
    with pytest.raises(
        EasyBytesError, match="used and total must be non-negative integers"
    ):
        percent_used(**counts)


@pytest.mark.parametrize("used", [0, 1])
def test_percent_used_rejects_zero_total(used):
    """Even zero used bytes require a positive total."""
    with pytest.raises(EasyBytesError, match="total must be at least 1"):
        percent_used(used, 0)


def test_percent_used_with_mixed_unit_labels():
    """percent_used works on counts produced by add_bytes."""
    used = add_bytes(["250 KB"])
    total = add_bytes(["1 MB"])
    assert percent_used(used, total) == 25.0