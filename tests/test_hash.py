import pytest

from py_simple_package.src.py_simple.easy_hash import (
    EasyHashError,
    hash_file,
    hash_text,
    hashes_match,
)


def test_hash_text_sha256_of_hello():
    assert hash_text("hello") == (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


def test_hash_text_md5():
    assert hash_text("hello", "md5") == "5d41402abc4b2a76b9719d911017c592"


def test_hash_text_rejects_bad_input():
    with pytest.raises(EasyHashError):
        hash_text(5)
    with pytest.raises(EasyHashError):
        hash_text("hello", "sha512")


def test_hash_file(tmp_path):
    note = tmp_path / "notes.txt"
    note.write_text("hello", encoding="utf-8")
    assert hash_file(str(note)) == hash_text("hello")


def test_hash_file_missing(tmp_path):
    with pytest.raises(EasyHashError):
        hash_file(str(tmp_path / "missing.txt"))


def test_hashes_match():
    digest = hash_text("hello")
    assert hashes_match("hello", digest) is True
    assert hashes_match("hello", digest.upper()) is True
    assert hashes_match("hello", "nope") is False
    assert hashes_match("hello", None) is False
