import hashlib
import io
import os
import textwrap
from contextlib import contextmanager
from pathlib import Path

import pytest

from py_simple_package.src.py_simple import (
    compare_file_hashes as public_compare_file_hashes,
)
from py_simple_package.src.py_simple.easy_hash import (
    EasyHashError,
    compare_file_hashes,
    hash_bytes,
    hash_directory,
    hash_file,
    hash_files,
    hash_text,
    hashes_match,
    verify_file_hash,
)


@pytest.mark.parametrize(
    "algorithm, expected",
    [
        ("sha256", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"),
        ("sha1", "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"),
        ("md5", "5d41402abc4b2a76b9719d911017c592"),
    ],
)
def test_hash_bytes_supported_algorithms(algorithm, expected):
    assert hash_bytes(b"hello", algorithm) == expected


@pytest.mark.parametrize("data", [b"", b"\x00\xffbinary data"])
def test_hash_bytes_handles_empty_and_binary_data(data):
    assert hash_bytes(data) == hashlib.sha256(data).hexdigest()


@pytest.mark.parametrize(
    "data", [None, "hello", bytearray(b"hello"), memoryview(b"hello")]
)
def test_hash_bytes_rejects_non_bytes(data):
    with pytest.raises(EasyHashError, match="data must be bytes"):
        hash_bytes(data)


def test_hash_bytes_rejects_unsupported_algorithm():
    with pytest.raises(
        EasyHashError, match="algorithm must be 'sha256', 'sha1', or 'md5'"
    ):
        hash_bytes(b"hello", "sha512")


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


def test_hash_bytes_public_imports():
    from py_simple import hash_bytes as public_hash
    from py_simple.easy_hash import hash_bytes as module_hash

    assert public_hash is module_hash
    assert public_hash(b"hello") == module_hash(b"hello")


@pytest.mark.parametrize("algorithm", ["sha256", "sha1", "md5"])
@pytest.mark.parametrize("as_path", [False, True])
def test_compare_file_hashes_identical_files(tmp_path, algorithm, as_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    content = b"identical content for comparison"
    file1.write_bytes(content)
    file2.write_bytes(content)

    p1 = file1 if as_path else str(file1)
    p2 = file2 if as_path else str(file2)

    assert compare_file_hashes(p1, p2, algorithm=algorithm) is True


def test_compare_file_hashes_different_files(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("content A", encoding="utf-8")
    file2.write_text("content B", encoding="utf-8")

    assert compare_file_hashes(str(file1), str(file2)) is False


def test_compare_file_hashes_empty_files(tmp_path):
    file1 = tmp_path / "empty1.txt"
    file2 = tmp_path / "empty2.txt"
    file1.write_bytes(b"")
    file2.write_bytes(b"")

    assert compare_file_hashes(file1, file2) is True


def test_compare_file_hashes_mixed_path_types(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_bytes(b"same bytes")
    file2.write_bytes(b"same bytes")

    assert compare_file_hashes(str(file1), file2) is True
    assert compare_file_hashes(file1, str(file2)) is True


@pytest.mark.parametrize("size", [65536, 65537, 2 * 65536 + 17])
def test_compare_file_hashes_large_chunked(tmp_path, size):
    content = (bytes(range(256)) * (size // 256 + 1))[:size]
    file1 = tmp_path / "large1.bin"
    file2 = tmp_path / "large2.bin"
    file3 = tmp_path / "large3.bin"

    file1.write_bytes(content)
    file2.write_bytes(content)
    file3.write_bytes(content + b"extra_byte")

    assert compare_file_hashes(file1, file2) is True
    assert compare_file_hashes(file1, file3) is False


def test_compare_file_hashes_missing_files(tmp_path):
    existing = tmp_path / "exists.txt"
    existing.write_text("hello", encoding="utf-8")
    missing = tmp_path / "missing.txt"

    with pytest.raises(EasyHashError, match="ERROR:"):
        compare_file_hashes(missing, existing)

    with pytest.raises(EasyHashError, match="ERROR:"):
        compare_file_hashes(existing, missing)


@pytest.mark.parametrize("algorithm", ["sha512", "SHA256", "", None, 123])
def test_compare_file_hashes_unsupported_algorithm(tmp_path, algorithm):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("hello", encoding="utf-8")
    file2.write_text("hello", encoding="utf-8")

    with pytest.raises(
        EasyHashError, match="algorithm must be 'sha256', 'sha1', or 'md5'"
    ):
        compare_file_hashes(file1, file2, algorithm=algorithm)


@pytest.mark.parametrize("bad_path", [None, 1, True, 1.5, b"file.txt", []])
def test_compare_file_hashes_invalid_path_types(tmp_path, bad_path):
    valid = tmp_path / "valid.txt"
    valid.write_text("hello", encoding="utf-8")

    with pytest.raises(TypeError):
        compare_file_hashes(bad_path, valid)

    with pytest.raises(TypeError):
        compare_file_hashes(valid, bad_path)


def test_compare_file_hashes_public_imports(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_bytes(b"hello")
    file2.write_bytes(b"hello")

    assert public_compare_file_hashes is compare_file_hashes
    assert public_compare_file_hashes(file1, file2) is True


def test_hash_directory_matches_manual_digest(tmp_path):
    root = tmp_path / "project"
    (root / "sub").mkdir(parents=True)
    (root / "a.txt").write_bytes(b"hello")
    (root / "sub" / "b.txt").write_bytes(b"world")
    expected = hashlib.sha256()
    for rel, data in [(b"a.txt", b"hello"), (b"sub/b.txt", b"world")]:
        expected.update(rel)
        expected.update(b"\0")
        expected.update(hashlib.sha256(data).hexdigest().encode("ascii"))
    assert hash_directory(root) == expected.hexdigest()


def test_hash_directory_deterministic_and_order_independent(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    (first / "sub").mkdir(parents=True)
    (second / "sub").mkdir(parents=True)
    (first / "a.txt").write_bytes(b"hello")
    (first / "sub" / "b.txt").write_bytes(b"world")
    (second / "sub" / "b.txt").write_bytes(b"world")
    (second / "a.txt").write_bytes(b"hello")
    assert hash_directory(first) == hash_directory(second)
    assert hash_directory(first) == hash_directory(first)


def test_hash_directory_changes_on_rename_or_content_change(tmp_path):
    root = tmp_path / "project"
    note = root / "note.txt"
    root.mkdir()
    note.write_bytes(b"hello")
    original = hash_directory(root)
    note.write_bytes(b"goodbye")
    assert hash_directory(root) != original
    note.write_bytes(b"hello")
    renamed = root / "renamed.txt"
    note.rename(renamed)
    assert hash_directory(root) != original


def test_hash_directory_empty_directory(tmp_path):
    root = tmp_path / "empty"
    root.mkdir()
    assert hash_directory(root) == hashlib.sha256(b"").hexdigest()


def test_hash_directory_rejects_non_directory_and_bad_algorithm(tmp_path):
    note = tmp_path / "note.txt"
    note.write_bytes(b"hello")
    with pytest.raises(EasyHashError, match="existing directory"):
        hash_directory(note)
    with pytest.raises(EasyHashError, match="existing directory"):
        hash_directory(tmp_path / "missing")
    with pytest.raises(
        EasyHashError, match="algorithm must be 'sha256', 'sha1', or 'md5'"
    ):
        hash_directory(tmp_path, "sha512")


def test_hash_directory_public_imports(tmp_path):
    from py_simple import hash_directory as public_hash_directory
    from py_simple.easy_hash import (
        hash_directory as module_hash_directory,
    )

    root = tmp_path / "project"
    root.mkdir()
    (root / "a.txt").write_bytes(b"hello")
    assert public_hash_directory is module_hash_directory
    assert public_hash_directory(root) == module_hash_directory(root)


def test_hash_directory_no_record_boundary_collision(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    (first / "a").write_bytes(b"b\x00x")
    second.mkdir()
    (second / "a").write_bytes(b"")
    (second / "b").write_bytes(b"x")
    assert hash_directory(first) != hash_directory(second)


def test_hash_directory_unreadable_root_raises(tmp_path, monkeypatch):
    root = tmp_path / "project"
    (root / "sub").mkdir(parents=True)
    (root / "a.txt").write_bytes(b"hello")
    real_scandir = os.scandir

    def failing_scandir(path):
        if Path(path) == root:
            raise PermissionError("permission denied")
        return real_scandir(path)

    monkeypatch.setattr(os, "scandir", failing_scandir)
    with pytest.raises(EasyHashError):
        hash_directory(root)


def test_hash_directory_unreadable_subdirectory_raises(tmp_path, monkeypatch):
    root = tmp_path / "project"
    blocked = root / "blocked"
    blocked.mkdir(parents=True)
    (root / "a.txt").write_bytes(b"hello")
    (blocked / "b.txt").write_bytes(b"world")
    real_scandir = os.scandir

    def failing_scandir(path):
        if Path(path) == blocked:
            raise PermissionError("permission denied")
        return real_scandir(path)

    monkeypatch.setattr(os, "scandir", failing_scandir)
    with pytest.raises(EasyHashError):
        hash_directory(root)


@pytest.mark.parametrize(
    "layout",
    [
        {"a.txt": b"hello", "sub/b.txt": b"world"},
        {"a.txt": b"hello", "a/b": b"world"},
    ],
)
def test_hash_directory_docstring_examples_agree(tmp_path, monkeypatch, layout):
    project = tmp_path / "project"
    for relative, content in layout.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    monkeypatch.chdir(tmp_path)
    blocks = [
        textwrap.dedent(part.split("```")[0])
        for part in hash_directory.__doc__.split("```python")[1:]
    ]
    assert len(blocks) == 2
    digests = []
    for block in blocks:
        namespace = {}
        exec(block, namespace)
        digests.append(namespace["digest"])
    assert digests[0] == digests[1] == hash_directory(project)


def test_hash_files_returns_checksum_per_path(tmp_path):
    notes = tmp_path / "notes.txt"
    backup = tmp_path / "backup.txt"
    notes.write_bytes(b"hello")
    backup.write_bytes(b"world")

    checksums = hash_files([str(notes), str(backup)])

    assert checksums == {
        str(notes): hash_file(str(notes)),
        str(backup): hash_file(str(backup)),
    }


def test_hash_files_accepts_path_objects_and_tuple(tmp_path):
    notes = tmp_path / "notes.txt"
    notes.write_bytes(b"hello")

    checksums = hash_files((notes,))

    assert checksums == {str(notes): hash_text("hello")}


def test_hash_files_empty_list_returns_empty_dict():
    assert hash_files([]) == {}


@pytest.mark.parametrize("filepaths", ["notes.txt", None, 123, {"notes.txt"}])
def test_hash_files_rejects_non_list_paths(filepaths):
    with pytest.raises(EasyHashError, match="filepaths must be a list of paths"):
        hash_files(filepaths)


def test_hash_files_rejects_non_path_item(tmp_path):
    notes = tmp_path / "notes.txt"
    notes.write_bytes(b"hello")
    with pytest.raises(EasyHashError, match="each path must be a string or path"):
        hash_files([str(notes), 123])


def test_hash_files_missing_file_raises(tmp_path):
    with pytest.raises(EasyHashError):
        hash_files([str(tmp_path / "missing.txt")])


def test_hash_files_rejects_unsupported_algorithm(tmp_path):
    notes = tmp_path / "notes.txt"
    notes.write_bytes(b"hello")
    with pytest.raises(
        EasyHashError, match="algorithm must be 'sha256', 'sha1', or 'md5'"
    ):
        hash_files([str(notes)], "sha512")


def test_hash_files_public_imports(tmp_path):
    from py_simple import hash_files as public_hash_files
    from py_simple.easy_hash import hash_files as module_hash_files

    notes = tmp_path / "notes.txt"
    notes.write_bytes(b"hello")

    assert public_hash_files is module_hash_files
    assert public_hash_files([notes]) == module_hash_files([notes])
