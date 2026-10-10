import pytest

from py_simple_package.src.py_simple.easy_bytes import (
    EasyBytesError,
    bytes_to_human,
    human_to_bytes,
    percent_used,
)


def test_bytes_to_human():
    assert bytes_to_human(0) == "0 B"
    assert bytes_to_human(1536) == "1.5 KB"
    assert bytes_to_human(2048) == "2 KB"
    assert bytes_to_human(1024 * 1024) == "1 MB"


def test_bytes_to_human_rejects_bad_input():
    with pytest.raises(EasyBytesError):
        bytes_to_human(-1)
    with pytest.raises(EasyBytesError):
        bytes_to_human(True)


def test_human_to_bytes():
    assert human_to_bytes("1.5 KB") == 1536
    assert human_to_bytes("2 KB") == 2048


def test_human_to_bytes_rejects_bad_label():
    with pytest.raises(EasyBytesError):
        human_to_bytes("lots")
    with pytest.raises(EasyBytesError):
        human_to_bytes("5 XB")


def test_percent_used():
    assert percent_used(250, 1000) == 25.0


def test_percent_used_rejects_zero_total():
    with pytest.raises(EasyBytesError):
        percent_used(1, 0)
