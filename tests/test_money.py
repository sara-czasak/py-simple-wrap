import pytest

from py_simple_package.src.py_simple.easy_money import (
    EasyMoneyError,
    add_tax,
    format_money,
    split_bill,
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
    assert add_tax(10, 8.5) == 10.85


def test_add_tax_rejects_negative_rate():
    with pytest.raises(EasyMoneyError):
        add_tax(10, -1)


def test_split_bill():
    assert split_bill(48, 3) == 16.0
    assert split_bill(10, 3) == 3.33


def test_split_bill_rejects_bad_people():
    with pytest.raises(EasyMoneyError):
        split_bill(10, 0)
    with pytest.raises(EasyMoneyError):
        split_bill(10, True)
