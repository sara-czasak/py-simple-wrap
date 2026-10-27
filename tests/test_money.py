from decimal import (
    Decimal,
    FloatOperation,
    Inexact,
    InvalidOperation,
    ROUND_DOWN,
    localcontext,
)

import pytest

from py_simple_package.src.py_simple.easy_money import (
    EasyMoneyError,
    add_tax,
    calculate_discount,
    calculate_tip,
    format_money,
    split_bill,
    split_bill_exact,
)


def test_format_money():
    assert format_money(12.5) == "$12.50"
    assert format_money("3", symbol="€") == "€3.00"


def test_format_money_rejects_bad_amount():
    with pytest.raises(EasyMoneyError):
        format_money("nope")
    with pytest.raises(EasyMoneyError):
        format_money(True)


def test_add_tax():
    assert add_tax(10, 8.5) == Decimal("10.85")


def test_add_tax_rejects_negative_rate():
    with pytest.raises(EasyMoneyError):
        add_tax(10, -1)


def test_split_bill():
    assert split_bill(48, 3) == Decimal("16.00")
    assert split_bill(10, 3) == Decimal("3.33")


def test_split_bill_rejects_bad_people():
    with pytest.raises(EasyMoneyError):
        split_bill(10, 0)
    with pytest.raises(EasyMoneyError):
        split_bill(10, True)


def test_calculate_discount():
    assert calculate_discount(2000, 15) == Decimal("1700.00")
    assert calculate_discount(100, 10) == Decimal("90.00")


def test_calculate_discount_with_zero_percent():
    assert calculate_discount(100, 0) == Decimal("100.00")


def test_calculate_discount_with_full_discount():
    assert calculate_discount(100, 100) == Decimal("0.00")


def test_calculate_discount_rejects_invalid_rate():
    with pytest.raises(EasyMoneyError):
        calculate_discount(100, -1)

    with pytest.raises(EasyMoneyError):
        calculate_discount(100, 101)


def test_calculate_discount_rejects_invalid_amount():
    with pytest.raises(EasyMoneyError):
        calculate_discount("invalid", 10)

    with pytest.raises(EasyMoneyError):
        calculate_discount(True, 10)


def test_calculate_tip():
    assert calculate_tip(50, 18) == Decimal("9.00")
    assert calculate_tip("100.00", 20) == Decimal("20.00")
    assert calculate_tip(33.50, 15) == Decimal("5.03")
    assert calculate_tip(0, 15) == Decimal("0.00")
    assert calculate_tip(50, 0) == Decimal("0.00")


def test_calculate_tip_rejects_negative_rate():
    with pytest.raises(EasyMoneyError):
        calculate_tip(50, -1)


def test_calculate_tip_rejects_invalid_amount():
    with pytest.raises(EasyMoneyError):
        calculate_tip("invalid", 15)
    with pytest.raises(EasyMoneyError):
        calculate_tip(True, 15)
    with pytest.raises(EasyMoneyError):
        calculate_tip(50, "invalid")
    with pytest.raises(EasyMoneyError):
        calculate_tip(50, True)


def test_calculate_tip_public_imports():
    from py_simple import calculate_tip as public_helper
    from py_simple.easy_money import calculate_tip as module_helper

    assert public_helper is module_helper



@pytest.mark.parametrize(
    "total,people,expected",
    [
        (10, 3, ["3.34", "3.33", "3.33"]),
        ("0.01", 3, ["0.01", "0.00", "0.00"]),
        (48, 3, ["16.00"] * 3),
        (0, 3, ["0.00"] * 3),
        ("-0.000", 2, ["0.00"] * 2),
        ("12.345", 1, ["12.35"]),
        ("0.005", 2, ["0.01", "0.00"]),
        ("0.015", 2, ["0.01", "0.01"]),
        ("0.0049", 2, ["0.00", "0.00"]),
        (2.675, 3, ["0.90", "0.89", "0.89"]),
        (-10, 3, ["-3.34", "-3.33", "-3.33"]),
        ("-0.01", 3, ["-0.01", "0.00", "0.00"]),
        ("-0.005", 2, ["-0.01", "0.00"]),
        ("-0.015", 2, ["-0.01", "-0.01"]),
        (Decimal("-0.0049"), 2, ["0.00", "0.00"]),
        (
            Decimal("99999999999999999999999999.99"),
            3,
            ["33333333333333333333333333.33"] * 3,
        ),
    ],
)
def test_split_bill_exact_shares(total, people, expected):
    shares = split_bill_exact(total, people)
    assert shares == [Decimal(value) for value in expected]
    assert [str(share) for share in shares] == expected
    assert all(
        isinstance(share, Decimal) and share.as_tuple().exponent == -2
        for share in shares
    )


@pytest.mark.parametrize("total", [10, 10.0, "10.00", Decimal("10.00")])
def test_split_bill_exact_supported_amount_types(total):
    assert split_bill_exact(total, 3) == [
        Decimal("3.34"),
        Decimal("3.33"),
        Decimal("3.33"),
    ]


@pytest.mark.parametrize(
    "people", [True, False, 0, -1, 3.0, "3", Decimal(3), None, [], 1 + 0j]
)
def test_split_bill_exact_rejects_people(people):
    with pytest.raises(EasyMoneyError, match="people must be an integer of at least 1"):
        split_bill_exact(10, people)


@pytest.mark.parametrize(
    "total", [True, False, None, [], {}, b"10", 1 + 0j, object(), "nope", ""]
)
def test_split_bill_exact_rejects_amount(total):
    with pytest.raises(EasyMoneyError):
        split_bill_exact(total, 3)


@pytest.mark.parametrize(
    "total",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
        Decimal("NaN"),
        Decimal("sNaN"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
        "NaN",
        "sNaN",
        "Infinity",
        "-Infinity",
    ],
)
def test_split_bill_exact_rejects_nonfinite(total):
    with pytest.raises(EasyMoneyError, match="amount must be finite"):
        split_bill_exact(total, 3)


def test_split_bill_exact_allocation_invariants():
    for cents in range(-101, 102):
        total = Decimal(cents).scaleb(-2)
        for people in range(1, 8):
            shares = split_bill_exact(total, people)
            assert len(shares) == people
            assert sum(shares) == total
            assert max(shares) - min(shares) <= Decimal("0.01")
            assert all(share.as_tuple().exponent == -2 for share in shares)
            magnitudes = [abs(share) for share in shares]
            assert magnitudes == sorted(magnitudes, reverse=True)
            assert magnitudes.count(max(magnitudes)) == (abs(cents) % people or people)
            assert all(share >= 0 if cents >= 0 else share <= 0 for share in shares)


def test_split_bill_exact_uses_half_up_and_no_float_arithmetic():
    with localcontext() as context:
        context.rounding = ROUND_DOWN
        context.traps[FloatOperation] = True
        assert split_bill_exact(2.675, 2) == [Decimal("1.34"), Decimal("1.34")]
        assert split_bill_exact("-0.005", 2) == [Decimal("-0.01"), Decimal("0.00")]
        assert context.rounding == ROUND_DOWN


def test_split_bill_exact_does_not_overflow_by_scaling_total():
    with localcontext() as context:
        context.Emax = 2
        assert split_bill_exact("999.99", 3) == [Decimal("333.33")] * 3


def test_split_bill_exact_retains_two_places_with_clamped_context():
    with localcontext() as context:
        context.prec = 6
        context.Emax = 2
        context.clamp = 1
        shares = split_bill_exact("-999.99", 3)
        assert [str(share) for share in shares] == ["-333.33"] * 3
        assert all(share.as_tuple().exponent == -2 for share in shares)


def test_split_bill_exact_rejects_invalid_with_disabled_decimal_trap():
    with localcontext() as context:
        context.traps[InvalidOperation] = False
        with pytest.raises(EasyMoneyError):
            split_bill_exact("invalid", 3)
        with pytest.raises(EasyMoneyError):
            split_bill_exact("1E+999", 3)


def test_split_bill_exact_wraps_decimal_precision_error():
    with localcontext() as context:
        context.prec = 2
        with pytest.raises(EasyMoneyError):
            split_bill_exact("10.00", 3)


def test_split_bill_exact_wraps_decimal_rounding_trap():
    with localcontext() as context:
        context.traps[Inexact] = True
        with pytest.raises(EasyMoneyError):
            split_bill_exact("1.005", 2)


def test_split_bill_exact_wraps_unrepresentable_total():
    with pytest.raises(EasyMoneyError):
        split_bill_exact(Decimal("1E+999"), 2)


def test_split_bill_exact_keeps_split_bill_compatible():
    assert split_bill(10, 3) == Decimal("3.33")
    assert sum(split_bill_exact(10, 3)) == Decimal("10.00")


def test_split_bill_exact_public_imports():
    from py_simple import split_bill_exact as public_split
    from py_simple.easy_money import split_bill_exact as module_split

    assert public_split is module_split
    assert public_split("10.00", 3) == split_bill_exact("10.00", 3)


@pytest.mark.parametrize("amount", [float("nan"), float("inf"), float("-inf"), "NaN", "Infinity", Decimal("sNaN"), Decimal("-Infinity")])
@pytest.mark.parametrize("operation", [format_money, lambda value: add_tax(value, 10), lambda value: calculate_discount(value, 10), lambda value: calculate_tip(value, 10), lambda value: split_bill(value, 2), lambda value: split_bill_exact(value, 2)])
def test_money_helpers_reject_non_finite_amounts(amount, operation):
    with pytest.raises(EasyMoneyError, match="finite"):
        operation(amount)


@pytest.mark.parametrize("rate", [float("nan"), float("inf"), "NaN", Decimal("sNaN")])
@pytest.mark.parametrize("operation", [add_tax, calculate_discount, calculate_tip])
def test_money_helpers_reject_non_finite_rates(rate, operation):
    with pytest.raises(EasyMoneyError, match="finite"):
        operation(100, rate)
