import base64

import pytest

from py_simple_package.src.py_simple import (
    decode_text as public_decode_text,
    decode_to_bytes as public_decode_to_bytes,
    decode_to_file as public_decode_to_file,
    encode_bytes as public_encode_bytes,
    encode_file as public_encode_file,
    encode_text as public_encode_text,
    encode_urlsafe_text as public_encode_urlsafe_text,
    is_base64 as public_is_base64,
)
from py_simple_package.src.py_simple.easy_base64 import (
    EasyBase64Error,
    decode_text,
    decode_to_bytes,
    decode_to_file,
    encode_bytes,
    encode_file,
    encode_text,
    encode_urlsafe_text,
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


def test_encode_and_decode_bytes_round_trip():
    raw = b"\x00\x01\x02\xff"
    assert decode_to_bytes(encode_bytes(raw)) == raw
    assert encode_bytes(b"hello") == "aGVsbG8="


def test_encode_bytes_rejects_non_bytes():
    with pytest.raises(EasyBase64Error):
        encode_bytes("not bytes")


def test_decode_to_bytes_rejects_invalid_text():
    with pytest.raises(EasyBase64Error):
        decode_to_bytes("not base64!!!")


def test_decode_to_bytes_rejects_non_string():
    with pytest.raises(EasyBase64Error):
        decode_to_bytes(123)


def test_encode_file(tmp_path):
    file_path = tmp_path / "sample.bin"
    file_path.write_bytes(b"hello world")
    encoded = encode_file(str(file_path))
    assert encoded == encode_text("hello world")
    assert decode_text(encoded) == "hello world"


def test_encode_file_rejects_non_string():
    with pytest.raises(EasyBase64Error):
        encode_file(123)


def test_encode_file_rejects_missing_file(tmp_path):
    with pytest.raises(EasyBase64Error):
        encode_file(str(tmp_path / "nonexistent.bin"))


def test_public_imports_includes_encode_file():
    assert public_encode_file is encode_file


def test_decode_to_file(tmp_path):
    output_file = tmp_path / "restored.txt"
    encoded = encode_text("hello world")
    decode_to_file(encoded, str(output_file))
    assert output_file.read_bytes() == b"hello world"


def test_decode_to_file_binary(tmp_path):
    output_file = tmp_path / "binary.bin"
    raw = b"\x00\x01\x02\xff"
    encoded = encode_bytes(raw)
    decode_to_file(encoded, str(output_file))
    assert output_file.read_bytes() == raw


def test_decode_to_file_rejects_non_string_encoded(tmp_path):
    output_file = tmp_path / "test.txt"
    with pytest.raises(EasyBase64Error):
        decode_to_file(123, str(output_file))


def test_decode_to_file_rejects_non_string_path():
    with pytest.raises(EasyBase64Error):
        decode_to_file("aGVsbG8=", 123)


def test_decode_to_file_rejects_invalid_text(tmp_path):
    output_file = tmp_path / "test.txt"
    with pytest.raises(EasyBase64Error):
        decode_to_file("not base64!!!", str(output_file))


def test_decode_to_file_rejects_invalid_path(tmp_path):
    output_file = tmp_path / "nonexistent_dir" / "nested" / "test.txt"
    with pytest.raises(EasyBase64Error):
        decode_to_file("aGVsbG8=", str(output_file))


def test_public_imports_includes_decode_to_file():
    assert public_decode_to_file is decode_to_file


@pytest.mark.parametrize(
    "text, expected",
    [("", ""), ("f", "Zg=="), ("fo", "Zm8="), ("hello?", "aGVsbG8_"), ("~~~", "fn5-")],
)
def test_encode_urlsafe_text_known_values(text, expected):
    assert encode_urlsafe_text(text) == expected


@pytest.mark.parametrize("text", ["hello?~~~", "café", "नमस्ते", "🎉"])
def test_encode_urlsafe_text_unicode_round_trip(text):
    encoded = encode_urlsafe_text(text)
    assert "+" not in encoded and "/" not in encoded
    assert base64.urlsafe_b64decode(encoded).decode("utf-8") == text


@pytest.mark.parametrize("text", [None, 123, b"hello", ["hello"]])
def test_encode_urlsafe_text_rejects_non_string(text):
    with pytest.raises(EasyBase64Error, match="text must be a string"):
        encode_urlsafe_text(text)


def test_encode_urlsafe_text_wraps_invalid_unicode():
    with pytest.raises(EasyBase64Error):
        encode_urlsafe_text("\ud800")


def test_public_import_includes_encode_urlsafe_text():
    assert public_encode_urlsafe_text is encode_urlsafe_text
