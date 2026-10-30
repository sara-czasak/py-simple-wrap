import pytest
import re

from py_simple_package.src.py_simple.easy_bytes import (
    EasyBytesError,
    bytes_to_human,
    human_to_bytes,
    percent_free,
    percent_used,
    remaining_bytes,
    add_bytes,
    average_bytes,
    is_larger,
    is_smaller,
)

BOTH = [False, True]


# --- bytes_to_human -------------------------------------------------------


@pytest.mark.parametrize(
    "num_bytes, expected",
    [
        (0, "0 B"),
        (1, "1 B"),
        (1023, "1023 B"),
        (1024, "1 KB"),
        (1025, "1 KB"),
        (1536, "1.5 KB"),
        (1587, "1.5 KB"),
        (1588, "1.6 KB"),
        (2047, "2 KB"),
        (2048, "2 KB"),
        (1023 * 1024, "1023 KB"),
        (1024**2, "1 MB"),
        (1023 * 1024**2, "1023 MB"),
        (1024**3, "1 GB"),
        (1023 * 1024**3, "1023 GB"),
        (1024**4, "1 TB"),
        (1536 * 1024**3, "1.5 TB"),
        (1024**5, "1024 TB"),
    ],
)
def test_bytes_to_human(num_bytes, expected):
    """The default is unchanged: KB-style labels with factors of 1024."""
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
    """With binary=True, use KiB-style labels (still factors of 1024)."""
    assert bytes_to_human(num_bytes, binary=True) == expected


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
def test_bytes_to_human_decimal(num_bytes, expected):
    """With decimal=True, use KB-style labels with factors of 1000."""
    assert bytes_to_human(num_bytes, decimal=True) == expected


@pytest.mark.parametrize(
    "num_bytes", [0, 1023, 1024, 1536, 1588, 1024**2, 1536 * 1024**3, 1024**5]
)
def test_bytes_to_human_binary_is_default_with_kib_spelling(num_bytes):
    """binary=True gives the default numbers, spelled with KiB, MiB, ..."""
    assert bytes_to_human(num_bytes, binary=True).replace("iB", "B") == (
        bytes_to_human(num_bytes)
    )


def test_bytes_to_human_explicit_false_flags_match_default():
    """Passing both flags as False is the same as passing neither."""
    assert (
        bytes_to_human(1536, binary=False, decimal=False) == bytes_to_human(1536)
    ) and bytes_to_human(1536) == "1.5 KB"


@pytest.mark.parametrize("num_bytes", [-1, True, False, 1.0, 1.5, "1024", None, [], {}])
@pytest.mark.parametrize("flags", [{}, {"binary": True}, {"decimal": True}])
def test_bytes_to_human_rejects_bad_input(num_bytes, flags):
    """Byte counts must be non-negative integers, excluding booleans."""
    with pytest.raises(
        EasyBytesError, match="num_bytes must be a non-negative integer"
    ):
        bytes_to_human(num_bytes, **flags)


@pytest.mark.parametrize("flag", ["binary", "decimal"])
@pytest.mark.parametrize("value", [0, 1, "yes", None, [], 1.0])
def test_bytes_to_human_rejects_bad_flags(flag, value):
    """Each flag must be a real boolean."""
    with pytest.raises(
        EasyBytesError, match=re.escape(f"{flag} must be a boolean (True or False).")
    ):
        bytes_to_human(1024, **{flag: value})


def test_bytes_to_human_rejects_both_flags():
    """KiB labels and 1000-based units cannot be combined."""
    with pytest.raises(EasyBytesError, match="binary and decimal cannot both be True"):
        bytes_to_human(1024, binary=True, decimal=True)


# --- human_to_bytes -------------------------------------------------------


@pytest.mark.parametrize(
    "label, expected",
    [
        ("0 B", 0),
        ("1 B", 1),
        ("512 B", 512),
        ("1.5 B", 1),
        ("0.1 KB", 102),
        ("1.5 KB", 1536),
        ("2 KB", 2048),
        ("1 MB", 1048576),
        ("1.5 MB", 1572864),
        ("1 GB", 1073741824),
        ("1.5 GB", 1610612736),
        ("1 TB", 1099511627776),
        ("1.5 TB", 1649267441664),
        ("0 TB", 0),
        ("  1.5 KB  ", 1536),
        ("\t1.5\t KB\n", 1536),
        ("1267650600228229401496703205376 B", 2**100),
        ("1267650600228229401496703205376 TB", 2**140),
        (f"{2**1023} B", 2**1023),
        # KiB-style units mean exactly the same thing.
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
        ("  1.5 KiB  ", 1536),
        ("\t1.5\t KiB\n", 1536),
        ("1267650600228229401496703205376 TiB", 2**140),
        # Exact scaling.
        ("1.001 KB", 1025),
        ("1e3 B", 1000),
        ("1e-999999999 KB", 0),
    ],
)
def test_human_to_bytes(label, expected):
    """The default is unchanged: KB-style units use factors of 1024."""
    result = human_to_bytes(label)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize(
    "label, expected",
    [
        ("0 B", 0),
        ("1.5 B", 1),
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
        ("  1.5 KB  ", 1500),
        ("\t1.5\t KB\n", 1500),
        # KiB-style units do not change.
        ("1 KiB", 1024),
        ("1.5 KiB", 1536),
        ("1 MiB", 1048576),
        ("1 TiB", 1099511627776),
        # Exact scaling: all of these lose a byte with binary floats
        # (e.g. 1.001 * 1000 == 1000.9999999999999).
        ("1.001 KB", 1001),
        ("1.001 MB", 1_001_000),
        ("2.01 KB", 2010),
        ("2.03 KB", 2030),
        ("4.1 MB", 4_100_000),
        ("8.2 MB", 8_200_000),
        ("16.4 MB", 16_400_000),
        ("0.0005 KB", 0),
        ("0.9999 KB", 999),
        ("1.001e3 B", 1001),
        ("1e-999999999 KB", 0),
    ],
)
def test_human_to_bytes_decimal(label, expected):
    """With decimal=True, KB-style units use factors of 1000, exactly."""
    result = human_to_bytes(label, decimal=True)
    assert result == expected
    assert isinstance(result, int)


def test_human_to_bytes_pre_kib_behavior_is_preserved():
    """Calls that worked before KiB existed return the same numbers."""
    assert human_to_bytes("1 MB") == 1048576
    assert human_to_bytes("1.5 KB") == 1536
    assert bytes_to_human(1023) == "1023 B"
    assert bytes_to_human(10 * 1024 * 1024) == "10 MB"


def test_human_to_bytes_decimal_differs_from_default_only_for_kb_units():
    """decimal=True changes KB, MB, GB, TB and nothing else."""
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        assert human_to_bytes(f"1 {unit}") == human_to_bytes(f"1 {unit}", decimal=True)
    for unit in ["KB", "MB", "GB", "TB"]:
        assert human_to_bytes(f"1 {unit}", decimal=True) < human_to_bytes(f"1 {unit}")


@pytest.mark.parametrize("value", [0, 1, "yes", None, [], 1.0])
def test_human_to_bytes_rejects_bad_decimal_flag(value):
    """The decimal flag must be a real boolean."""
    with pytest.raises(
        EasyBytesError, match=re.escape("decimal must be a boolean (True or False).")
    ):
        human_to_bytes("1 KB", decimal=value)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize("label", [None, 1024, 1.5, True, False, [], {}])
def test_human_to_bytes_rejects_non_string(label, decimal):
    """Reject non-string labels with the module's exception."""
    with pytest.raises(EasyBytesError, match="label must be a string"):
        human_to_bytes(label, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize(
    "label", ["", "  ", "lots", "1.5", "KB", "1.5KB", "1.5KiB", "1 KB extra"]
)
def test_human_to_bytes_rejects_bad_label(label, decimal):
    """A label must contain a number and a separate unit."""
    with pytest.raises(EasyBytesError, match="use a form like '1.5 KB'"):
        human_to_bytes(label, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize(
    "label", ["5 XB", "1 kb", "1 mb", "1 kib", "1 KIB", "1 Kib", "1 KiKB", "1 PiB"]
)
def test_human_to_bytes_rejects_unknown_unit(label, decimal):
    """Only the documented units, with exact capitalization, are supported."""
    with pytest.raises(
        EasyBytesError,
        match="unit must be B, KB, MB, GB, TB, KiB, MiB, GiB, or TiB",
    ):
        human_to_bytes(label, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize("label", ["many KB", "1.2.3 MB", "--1 B", "many KiB"])
def test_human_to_bytes_rejects_malformed_number(label, decimal):
    """Invalid numeric text should be wrapped in EasyBytesError."""
    with pytest.raises(EasyBytesError, match="could not convert string to float"):
        human_to_bytes(label, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize(
    "label",
    ["-1 B", "-0.5 KB", "-0.5 KiB", "-inf KB", "-Infinity TB", "-1e309 MB"],
)
def test_human_to_bytes_rejects_negative_size(label, decimal):
    """Reject negative sizes, including fractional ones."""
    with pytest.raises(EasyBytesError, match="size cannot be negative"):
        human_to_bytes(label, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
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
def test_human_to_bytes_rejects_nonfinite_size(label, decimal):
    """Non-finite numeric labels must use the public conversion error."""
    with pytest.raises(
        EasyBytesError, match="size must convert to a finite byte count"
    ):
        human_to_bytes(label, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize("unit", ["KB", "MB", "GB", "TB", "KiB", "MiB", "GiB", "TiB"])
def test_human_to_bytes_rejects_scaled_overflow(unit, decimal):
    """A finite number can still overflow when scaled to bytes."""
    with pytest.raises(
        EasyBytesError, match="size must convert to a finite byte count"
    ):
        human_to_bytes(f"1e308 {unit}", decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize(
    "label",
    [
        "1e-9999999999999999999 B",
        "1e-9999999999999999999 KB",
        "1e-9999999999999999999 TiB",
        "0e-9999999999999999999 MB",
    ],
)
def test_human_to_bytes_wraps_unrepresentable_decimal(label, decimal):
    """Extreme exponents must raise EasyBytesError, not decimal.InvalidOperation."""
    with pytest.raises(
        EasyBytesError, match="size could not be converted to a whole byte count"
    ):
        human_to_bytes(label, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize(
    "label", ["1e-9999999999999999999 B", "1e-9999999999999999999 KB"]
)
def test_add_bytes_wraps_unrepresentable_decimal(label, decimal):
    """add_bytes must surface the same public error, wherever the label sits."""
    with pytest.raises(
        EasyBytesError, match="size could not be converted to a whole byte count"
    ):
        add_bytes([label], decimal=decimal)
    with pytest.raises(
        EasyBytesError, match="size could not be converted to a whole byte count"
    ):
        add_bytes([1, "1 KB", label], decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
def test_human_to_bytes_extreme_but_representable_exponents_still_work(decimal):
    """Only inputs Decimal cannot hold are rejected; tiny ones it can hold are 0."""
    assert human_to_bytes("1e-999999999 KB", decimal=decimal) == 0
    assert human_to_bytes("1e-400000000000 KB", decimal=decimal) == 0


# --- add_bytes ------------------------------------------------------------


@pytest.mark.parametrize(
    "values, expected",
    [
        ([], 0),
        ([0], 0),
        ([1024], 1024),
        ([1, 2, 3], 6),
        (["0 B"], 0),
        (["512 B"], 512),
        (["1 KB"], 1024),
        (["1 KiB"], 1024),
        (["1 KB", "1 KiB"], 2048),
        (["1.5 KB", "1.5 KiB"], 1536 + 1536),
        ([512, "1 KB", "1.5 KiB"], 512 + 1024 + 1536),
        (["  2 MB  ", 1], 2 * 1024**2 + 1),
        (["1 MB", "1 MiB"], 2 * 1024**2),
        (["1 GB", "1 GiB"], 2 * 1024**3),
        (["1 TB", "1 TiB"], 2 * 1024**4),
        ([2**100, "1 B"], 2**100 + 1),
        ([10, 20, "30 B"], 60),
        ((1, "1 KB"), 1025),
    ],
)
def test_add_bytes(values, expected):
    """By default, KB-style labels use factors of 1024, like human_to_bytes."""
    result = add_bytes(values)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize(
    "values, expected",
    [
        ([], 0),
        ([1, 2, 3], 6),
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
        ((1, "1 KB"), 1001),
        (["1.001 KB"], 1001),
        (["4.1 MB", "1.001 KB"], 4_100_000 + 1001),
    ],
)
def test_add_bytes_decimal(values, expected):
    """With decimal=True, "1 KB" is 1000 bytes and "1 KiB" is 1024 bytes."""
    result = add_bytes(values, decimal=True)
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


@pytest.mark.parametrize("value", [0, 1, "yes", None, [], 1.0])
def test_add_bytes_rejects_bad_decimal_flag(value):
    """The decimal flag is checked even when the list is empty."""
    with pytest.raises(
        EasyBytesError, match=re.escape("decimal must be a boolean (True or False).")
    ):
        add_bytes([], decimal=value)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize("values", [None, 5, 1.5, "1 KB", b"1 KB", {}, {1: 2}, {1, 2}])
def test_add_bytes_rejects_non_list(values, decimal):
    """A bare string must not be iterated character by character."""
    with pytest.raises(EasyBytesError, match="values must be a list or a tuple"):
        add_bytes(values, decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
@pytest.mark.parametrize(
    "bad_item", [-1, True, False, 1.0, 1.5, None, [], {}, b"1 KB", ["1 KB"]]
)
def test_add_bytes_rejects_bad_item(bad_item, decimal):
    """Items must be non-negative ints (not bools) or strings."""
    with pytest.raises(
        EasyBytesError,
        match="each value must be a non-negative integer or a size string",
    ):
        add_bytes([1, bad_item], decimal=decimal)


@pytest.mark.parametrize("decimal", BOTH)
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
def test_add_bytes_propagates_label_errors(bad_label, message, decimal):
    """Invalid labels raise the same error human_to_bytes would raise."""
    with pytest.raises(EasyBytesError, match=message):
        add_bytes([1, bad_label], decimal=decimal)


def test_add_bytes_public_imports():
    """Both documented import paths expose the same helper."""
    from py_simple import add_bytes as public_helper
    from py_simple.easy_bytes import add_bytes as module_helper

    assert public_helper is module_helper
    assert public_helper([512, "1 KB", "1 KiB"]) == 2560
    assert public_helper([512, "1 KB", "1 KiB"], decimal=True) == 2536


# --- percent_used ---------------------------------------------------------


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


def test_percent_used_with_add_bytes():
    """percent_used works on counts produced by add_bytes."""
    used = add_bytes(["250 KB"], decimal=True)
    total = add_bytes(["1 MB"], decimal=True)
    assert percent_used(used, total) == 25.0


# --- remaining_bytes ------------------------------------------------------


@pytest.mark.parametrize(
    "used, total, expected",
    [
        (250, 1000, 750),
        (0, 1000, 1000),
        (1000, 1000, 0),
        (0, 0, 0),
        (1, 2, 1),
        (2**100, 2**100 + 1, 1),
    ],
)
def test_remaining_bytes(used, total, expected):
    """Return an exact integer, including empty, full, and large capacities."""
    result = remaining_bytes(used, total)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize(
    "invalid", [-1, True, False, 1.0, "1", None, [], {}, float("nan"), float("inf")]
)
@pytest.mark.parametrize("argument", ["used", "total"])
def test_remaining_bytes_rejects_bad_input(invalid, argument):
    """Validate both arguments before performing arithmetic."""
    counts = {"used": 0, "total": 100}
    counts[argument] = invalid
    with pytest.raises(
        EasyBytesError, match="used and total must be non-negative integers"
    ):
        remaining_bytes(**counts)


@pytest.mark.parametrize("used, total", [(1, 0), (1001, 1000)])
def test_remaining_bytes_rejects_usage_above_capacity(used, total):
    """An inconsistent storage report must not produce a negative remainder."""
    with pytest.raises(EasyBytesError, match="used cannot exceed total"):
        remaining_bytes(used, total)


def test_remaining_bytes_public_imports():
    """Both documented import paths expose the same helper."""
    from py_simple import remaining_bytes as public_helper
    from py_simple.easy_bytes import remaining_bytes as module_helper

    assert public_helper is module_helper
    assert public_helper(250, 1000) == 750


@pytest.mark.parametrize(
    "used, total, expected",
    [
        (0, 1000, 100.0),
        (0, 1, 100.0),
        (1, 1, 0.0),
        (1000, 1000, 0.0),
        (250, 1000, 75.0),
        (1, 3, 66.7),
        (2, 3, 33.3),
        (1, 8, 87.5),
    ],
)
def test_percent_free(used, total, expected):
    """Return the free share as a float rounded to one decimal place."""
    result = percent_free(used, total)
    assert result == expected
    assert isinstance(result, float)


@pytest.mark.parametrize(
    "invalid",
    [-1, True, False, 1.0, 1.5, "1", None, [], {}, float("nan"), float("inf")],
)
@pytest.mark.parametrize("argument", ["used", "total"])
def test_percent_free_rejects_bad_input(invalid, argument):
    """Validate each byte count independently, excluding booleans and non-ints."""
    counts = {"used": 1, "total": 100}
    counts[argument] = invalid
    with pytest.raises(
        EasyBytesError, match="used and total must be non-negative integers"
    ):
        percent_free(**counts)


@pytest.mark.parametrize("used", [0, 1])
def test_percent_free_rejects_zero_total(used):
    """Even zero used bytes require a positive total."""
    with pytest.raises(EasyBytesError, match="total must be at least 1"):
        percent_free(used, 0)


@pytest.mark.parametrize("used, total", [(1001, 1000), (2, 1)])
def test_percent_free_rejects_usage_above_capacity(used, total):
    """Usage exceeding total cannot produce negative free percentages."""
    with pytest.raises(EasyBytesError, match="used cannot exceed total"):
        percent_free(used, total)


def test_percent_free_public_imports():
    """Both documented import paths expose the percent_free helper."""
    from py_simple import percent_free as public_helper
    from py_simple.easy_bytes import percent_free as module_helper

    assert public_helper is module_helper
    assert public_helper(250, 1000) == 75.0


# --- average_bytes --------------------------------------------------------


@pytest.mark.parametrize(
    "values, expected",
    [
        ([512], 512),
        ([512, "1 KB", "1 KiB"], 853),
        (("1 KB", "1 KiB"), 1024),
        ([0, 0], 0),
        ([1, 2], 1),
        ([1024, 2048, 3072], 2048),
        ([], None),
    ],
)
def test_average_bytes(values, expected):
    """Average a mix of byte counts and size labels, truncating fractions."""
    if values == []:
        with pytest.raises(EasyBytesError, match="values must not be empty"):
            average_bytes(values)
        return
    result = average_bytes(values)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize(
    "values, expected",
    [
        ([512, "1 KB", "1 KiB"], 845),
        (("1 KB",), 1000),
    ],
)
def test_average_bytes_decimal(values, expected):
    """With decimal=True, KB style labels count in factors of 1000."""
    assert average_bytes(values, decimal=True) == expected


@pytest.mark.parametrize("value", [0, 1, "yes", None, [], 1.0])
def test_average_bytes_rejects_bad_decimal_flag(value):
    """The decimal flag must be a real boolean."""
    with pytest.raises(
        EasyBytesError, match=re.escape("decimal must be a boolean (True or False).")
    ):
        average_bytes([512], decimal=value)


@pytest.mark.parametrize("values", ["1 KB", 512, {"a": 1}, None])
def test_average_bytes_rejects_non_list(values):
    """The input must be a list or a tuple."""
    with pytest.raises(EasyBytesError, match="values must be a list or a tuple"):
        average_bytes(values)


@pytest.mark.parametrize("bad_item", [-1, True, False, 1.5, None, [], {}, float("nan")])
def test_average_bytes_rejects_bad_item(bad_item):
    """Each item must be a non-negative integer or a valid size label."""
    with pytest.raises(
        EasyBytesError,
        match="each value must be a non-negative integer or a size string",
    ):
        average_bytes([512, bad_item])


@pytest.mark.parametrize("bad_label", ["1 XB", "KB", "1.5", "-1 KB", "1.5 KB extra"])
def test_average_bytes_propagates_label_errors(bad_label):
    """An invalid size label raises EasyBytesError, not a raw parse error."""
    with pytest.raises(EasyBytesError):
        average_bytes([bad_label])


def test_average_bytes_public_imports():
    """Both documented import paths expose the average_bytes helper."""
    from py_simple import average_bytes as public_helper
    from py_simple.easy_bytes import average_bytes as module_helper

    assert public_helper is module_helper
    assert public_helper([512, "1 KB", "1 KiB"]) == 853


def test_is_larger():
    # Basic comparisons
    assert is_larger("1.5 GB", "1000 MB") is True
    assert is_larger("500 B", "1 KB") is False
    assert is_larger(2048, "1 KB") is True

    # Edge cases (equal values)
    assert is_larger("1 KB", 1024) is False

    # Decimal flag
    assert is_larger("1 KB", 1000, decimal=True) is False

    # Invalid decimal flag
    for bad in [0, 1, "yes", None, [], 1.0]:
        with pytest.raises(
            EasyBytesError, match=re.escape("decimal must be a boolean")
        ):
            is_larger("1 KB", "2 KB", decimal=bad)

    # Boolean inputs (fall through to human_to_bytes as a non-string label)
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_larger(True, "1 KB")
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_larger("1 KB", False)

    # Negative values: a negative label fails the negative-size check, while a
    # negative int fails the int branch and reaches human_to_bytes as a
    # non-string label. Both sides are covered for each form.
    with pytest.raises(EasyBytesError, match="size cannot be negative"):
        is_larger("-1 KB", "1 KB")
    with pytest.raises(EasyBytesError, match="size cannot be negative"):
        is_larger("1 KB", "-1 KB")
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_larger(-10, "1 KB")
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_larger("1 KB", -10)

    # Mixed unit types: KB (1024) and KiB (1024) are equal by default...
    assert is_larger("1 KB", "1 KiB") is False
    # ...but decimal=True shrinks only KB, so KB is still not larger.
    assert is_larger("1 KB", "1 KiB", decimal=True) is False
    assert is_larger("1 GiB", "1000 MB") is True
    assert is_larger("1025 B", "1 KiB") is True

    # Errors handling
    with pytest.raises(EasyBytesError):
        is_larger(-10, "1 KB")

    with pytest.raises(EasyBytesError):
        is_larger("1 KB", "invalid_size")


def test_is_smaller():
    # Basic comparisons
    assert is_smaller("500 B", "1 KB") is True
    assert is_smaller("500 GB", "1 KiB") is False
    assert is_smaller("1.5 GB", "1000 MB") is False
    assert is_smaller("1.5 TB", "1000 TiB") is True
    assert is_smaller(512, "1 KB") is True

    # Edge cases (equal values)
    assert is_smaller("1 KB", 1024) is False

    # Invalid decimal flag
    for bad in [0, 1, "yes", None, [], 1.0]:
        with pytest.raises(
            EasyBytesError, match=re.escape("decimal must be a boolean")
        ):
            is_smaller("1 KB", "2 KB", decimal=bad)

    # Boolean inputs (fall through to human_to_bytes as a non-string label)
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_smaller(True, "1 KB")
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_smaller("1 KB", False)

    # Negative values: a negative label fails the negative-size check, while a
    # negative int fails the int branch and reaches human_to_bytes as a
    # non-string label. Both sides are covered for each form.
    with pytest.raises(EasyBytesError, match="size cannot be negative"):
        is_smaller("-1 KB", "1 KB")
    with pytest.raises(EasyBytesError, match="size cannot be negative"):
        is_smaller("1 KB", "-1 KB")
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_smaller(-10, "1 KB")
    with pytest.raises(EasyBytesError, match="label must be a string"):
        is_smaller("1 KB", -10)

    # Mixed unit types: KB (1024) and KiB (1024) are equal by default...
    assert is_smaller("1 KB", "1 KiB") is False
    # ...but decimal=True shrinks only KB, so KB is then smaller.
    assert is_smaller("1 KB", "1 KiB", decimal=True) is True
    assert is_smaller("1000 MB", "1 GiB") is True
    assert is_smaller(1024, "1 KiB") is False
    assert is_smaller(1023, "1 KiB") is True

    # Errors handling
    with pytest.raises(EasyBytesError):
        is_smaller("invalid_size", "1 KB")
