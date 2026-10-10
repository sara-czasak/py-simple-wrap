import pytest

from py_simple_package.src.py_simple import (
    decode_text as public_decode_text,
    encode_text as public_encode_text,
    is_base64 as public_is_base64,
)
from py_simple_package.src.py_simple.easy_base64 import (
    EasyBase64Error,
    decode_text,
    encode_text,
    is_base64,
)


def test_encode_and_decode_round_trip():
    assert decode_text(encode_text("hello")) == "hello"
    assert encode_text("hello") == "aGVsbG8="


def test_encode_rejects_non_string():
    with pytest.raises(EasyBase64Error):
        encode_text(5)


def test_decode_rejects_invalid_text():
    with pytest.raises(EasyBase64Error):
        decode_text("not base64!!!")


def test_is_base64():
    assert is_base64("aGVsbG8=") is True
    assert is_base64("hello") is False
    assert is_base64("") is False
    assert is_base64(None) is False


def test_public_imports():
    assert public_encode_text is encode_text
    assert public_decode_text is decode_text
    assert public_is_base64 is is_base64
