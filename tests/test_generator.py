import itertools
import string
import uuid

import pytest

from py_simple_package.src.py_simple.easy_generator import (
    EasyGeneratorError,
    generate_api_key,
    generate_otp,
    generate_password,
    generate_qr_code,
    generate_slug,
    generate_uuid,
)


@pytest.mark.parametrize(
    "length, uppercase, digits, special",
    [
        (12, 2, 2, 2),
        (16, 3, 3, 3),
        (20, 5, 2, 4),
        (8, 1, 1, 1),
        (4, 0, 0, 0),
    ],
)
def test_generate_password_length(length, uppercase, digits, special):
    password = generate_password(
        length,
        uppercase_chars=uppercase,
        digit_chars=digits,
        special_chars=special,
    )

    assert len(password) == length


@pytest.mark.parametrize(
    "length, uppercase, digits, special",
    [
        (12, 2, 2, 2),
        (16, 3, 3, 3),
        (20, 5, 2, 4),
    ],
)
def test_generate_password_character_counts(length, uppercase, digits, special):
    password = generate_password(
        length,
        uppercase_chars=uppercase,
        digit_chars=digits,
        special_chars=special,
    )

    assert sum(char in string.ascii_uppercase for char in password) == uppercase

    assert sum(char in string.digits for char in password) == digits

    assert sum(char in string.punctuation for char in password) == special

    lowercase = length - (uppercase + digits + special)

    assert sum(char in string.ascii_lowercase for char in password) == lowercase


@pytest.mark.parametrize(
    "length",
    [8, 12, 16, 20],
)
def test_generate_password_no_adjacent_duplicates(length):
    password = generate_password(length)

    assert all(first != second for first, second in itertools.pairwise(password))


@pytest.mark.parametrize(
    "text, expected_slug",
    [
        ("Hello World", "hello-world"),
        ("Fiancé", "fiance"),
        ("What_a!string  name ", "what-a-string-name"),
        ("   spaces at start", "spaces-at-start"),
        ("test-slug", "test-slug"),
    ],
)
def test_generate_slug_passing(text, expected_slug):
    actual_slug = generate_slug(text)

    assert actual_slug == expected_slug


@pytest.mark.parametrize(
    "text",
    [
        "",
        "  ",
        "!!!",
        None,
        456,
        -421.99,
    ],
)
def test_generate_slug_rejects_invalid_string(text):
    with pytest.raises(EasyGeneratorError):
        generate_slug(text)


@pytest.mark.parametrize(
    "data",
    [
        "https://example.com",
        "Hello World",
        "123456789",
        "test@example.com",
    ],
)
def test_generate_qr_code(tmp_path, monkeypatch, data):
    monkeypatch.chdir(tmp_path)

    generate_qr_code(data)

    assert (tmp_path / "qrcode0.png").exists()


@pytest.mark.parametrize(
    "data",
    ["", None],
)
def test_generate_qr_code_rejects_empty_data(data):
    with pytest.raises(EasyGeneratorError):
        generate_qr_code(data)


def test_generate_qr_code_avoids_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "qrcode0.png").touch()

    generate_qr_code("https://example.com")

    assert (tmp_path / "qrcode0.png").exists()
    assert (tmp_path / "qrcode1.png").exists()


def test_generate_qr_code_wraps_generation_error(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("QR generation failed")

    monkeypatch.setattr(
        "py_simple_package.src.py_simple.easy_generator.qrcode.make",
        fail,
    )

    with pytest.raises(
        EasyGeneratorError,
        match="QR generation failed",
    ):
        generate_qr_code("hello")


def test_generate_uuid():
    result = generate_uuid()

    parsed_uuid = uuid.UUID(result)

    assert parsed_uuid.version == 4
    assert str(parsed_uuid) == result


def test_generate_api_key():
    api_key = generate_api_key()

    assert isinstance(api_key, str)
    assert len(api_key) > 0
    assert all(char.isalnum() or char in "-_=" for char in api_key)


def test_generate_api_key_uses_64_bytes(monkeypatch):
    captured = {}

    def fake_token_urlsafe(length):
        captured["length"] = length
        return "fake-api-key"

    monkeypatch.setattr(
        "py_simple_package.src.py_simple.easy_generator.secrets.token_urlsafe",
        fake_token_urlsafe,
    )

    assert generate_api_key() == "fake-api-key"
    assert captured["length"] == 64


@pytest.mark.parametrize(
    "length",
    [4, 5, 6, 8, 10],
)
def test_generate_otp(length):
    otp = generate_otp(length)

    assert len(otp) == length
    assert otp.isdigit()


@pytest.mark.parametrize(
    "length",
    [4, 6, 8, 10],
)
def test_generate_otp_with_letters(length):
    otp = generate_otp(length, with_letters=True)

    assert len(otp) == length
    assert all(char in string.ascii_letters + string.digits for char in otp)


@pytest.mark.parametrize(
    "length",
    [0, 1, 2, 3],
)
def test_generate_otp_rejects_short_length(length):
    with pytest.raises(EasyGeneratorError, match="at least 4"):
        generate_otp(length)


def test_generate_otp_accepts_minimum_length():
    otp = generate_otp(4)

    assert len(otp) == 4
    assert otp.isdigit()
