import hashlib
import io
from contextlib import contextmanager
from pathlib import Path

import pytest

from py_simple_package.src.py_simple.easy_hash import (
    EasyHashError,
    hash_file,
    hash_text,
    hashes_match,
    verify_file_hash,
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


@pytest.mark.parametrize(
    "algorithm, expected",
    [
        ("sha256", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"),
        ("sha1", "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"),
        ("md5", "5d41402abc4b2a76b9719d911017c592"),
    ],
)
@pytest.mark.parametrize("as_path", [False, True])
def test_verify_file_hash_supported_algorithms(tmp_path, algorithm, expected, as_path):
    """String and Path inputs accept checksums in either hex case."""
    note = tmp_path / "notes.txt"
    note.write_bytes(b"hello")
    filepath = note if as_path else str(note)

    assert verify_file_hash(filepath, expected, algorithm) is True
    assert verify_file_hash(filepath, expected.upper(), algorithm) is True
    assert verify_file_hash(filepath, "0" * len(expected), algorithm) is False


@pytest.mark.parametrize("content", [b"", bytes(range(256))])
@pytest.mark.parametrize("algorithm", ["sha256", "sha1", "md5"])
def test_verify_file_hash_empty_and_binary_files(tmp_path, content, algorithm):
    """Hash the exact bytes, including empty files and non-text data."""
    file = tmp_path / "data.bin"
    file.write_bytes(content)
    expected = hashlib.new(algorithm, content).hexdigest()

    assert verify_file_hash(file, expected, algorithm) is True


@pytest.mark.parametrize(
    "expected",
    ["", "nope", "0" * 64, "g" * 64, "a" * 63, "a" * 65],
)
def test_verify_file_hash_invalid_checksum_returns_false(tmp_path, expected):
    """Malformed checksums behave like nonmatches, as in hashes_match."""
    note = tmp_path / "notes.txt"
    note.write_bytes(b"hello")

    assert verify_file_hash(note, expected) is False
    assert hashes_match("hello", expected) is False


@pytest.mark.parametrize("whitespace", [" ", "\n", "\t"])
def test_verify_file_hash_does_not_strip_checksum(tmp_path, whitespace):
    """Only hex letter case is normalized, matching hashes_match."""
    note = tmp_path / "notes.txt"
    note.write_bytes(b"hello")
    expected = hashlib.sha256(b"hello").hexdigest()

    assert verify_file_hash(note, expected + whitespace) is False
    assert verify_file_hash(note, whitespace + expected) is False


@pytest.mark.parametrize("expected", [None, 5, 1.5, True, b"abc", [], {}])
def test_verify_file_hash_non_string_checksum_returns_false(tmp_path, expected):
    """Non-string checksums return False before path or algorithm validation."""
    assert verify_file_hash(tmp_path / "missing", expected, "sha512") is False
    assert hashes_match("hello", expected, "sha512") is False


@pytest.mark.parametrize("algorithm", ["sha512", "SHA256", "", None, 5, []])
def test_verify_file_hash_unsupported_algorithm(tmp_path, algorithm):
    """Use the existing algorithm allowlist and error before opening a file."""
    with pytest.raises(
        EasyHashError, match="algorithm must be 'sha256', 'sha1', or 'md5'"
    ):
        verify_file_hash(tmp_path / "missing", "0" * 64, algorithm)


@pytest.mark.parametrize("filepath", [None, 1, True, 1.5, b"notes.txt", []])
def test_verify_file_hash_invalid_path_type(filepath):
    """Invalid path types retain the Path error convention of hash_file."""
    with pytest.raises(TypeError):
        verify_file_hash(filepath, "0" * 64)


def test_verify_file_hash_missing_file(tmp_path):
    """A missing path reports an I/O error rather than a checksum mismatch."""
    with pytest.raises(EasyHashError, match="ERROR:") as exc_info:
        verify_file_hash(tmp_path / "missing.bin", "0" * 64)

    assert "missing.bin" in str(exc_info.value)
    assert exc_info.value.__cause__ is None


def test_verify_file_hash_directory(tmp_path):
    """A directory cannot be read as file contents."""
    with pytest.raises(EasyHashError, match="ERROR:"):
        verify_file_hash(tmp_path, "0" * 64)


def test_verify_file_hash_permission_error(tmp_path, monkeypatch):
    """Wrap permission errors deterministically across platforms/users."""

    def denied_open(*args, **kwargs):
        raise PermissionError("access denied")

    monkeypatch.setattr(Path, "open", denied_open)
    with pytest.raises(EasyHashError, match="access denied") as exc_info:
        verify_file_hash(tmp_path / "restricted.bin", "0" * 64)

    assert exc_info.value.__cause__ is None


@pytest.mark.parametrize("size", [65536, 65537, 2 * 65536 + 17])
@pytest.mark.parametrize("matches", [True, False])
def test_verify_file_hash_bounded_reads_and_cleanup(
    tmp_path, monkeypatch, size, matches
):
    """Read real files in bounded chunks and close on matches and mismatches."""
    content = (bytes(range(256)) * (size // 256 + 1))[:size]
    file = tmp_path / "chunks.bin"
    file.write_bytes(content)
    expected = hashlib.sha256(content).hexdigest() if matches else "0" * 64
    original_open = Path.open
    handles = []
    read_sizes = []
    chunks = []

    @contextmanager
    def tracked_open(path, mode):
        assert path == file
        assert mode == "rb"
        with original_open(path, mode) as handle:
            handles.append(handle)

            class Reader:
                def read(self, requested=-1):
                    assert 0 < requested <= 64 * 1024
                    read_sizes.append(requested)
                    chunk = handle.read(requested)
                    chunks.append(chunk)
                    return chunk

            yield Reader()

    monkeypatch.setattr(Path, "open", tracked_open)

    assert verify_file_hash(file, expected) is matches
    assert len(handles) == 1 and handles[0].closed
    assert len(read_sizes) >= 2
    assert chunks[-1] == b""
    assert b"".join(chunks) == content
    assert len([chunk for chunk in chunks if chunk]) >= (1 if size == 65536 else 2)


def test_verify_file_hash_closes_file_after_read_error(tmp_path, monkeypatch):
    """Close the handle even when a later read fails after partial progress."""

    class FailingReader(io.BytesIO):
        def read(self, size=-1):
            if self.tell():
                raise OSError("read failed")
            return super().read(1)

    reader = FailingReader(b"hello")
    monkeypatch.setattr(Path, "open", lambda *args, **kwargs: reader)

    with pytest.raises(EasyHashError, match="read failed") as exc_info:
        verify_file_hash(tmp_path / "broken.bin", "0" * 64)

    assert reader.closed
    assert exc_info.value.__cause__ is None


def test_verify_file_hash_public_imports(tmp_path):
    """Expose the helper through both documented public import paths."""
    from py_simple import verify_file_hash as public_verify
    from py_simple.easy_hash import verify_file_hash as module_verify

    note = tmp_path / "notes.txt"
    note.write_bytes(b"hello")
    expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    assert public_verify is module_verify
    assert public_verify(note, expected) is True
    assert module_verify(note, "0" * 64) is False
