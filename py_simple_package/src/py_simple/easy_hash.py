"""
easy_hash creates checksums for text, bytes, and files without the hashlib boilerplate.
"""

import hashlib
import os
from pathlib import Path


class EasyHashError(Exception):
    """
    Raised when a checksum cannot be created.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


_ALGORITHMS = ("sha256", "sha1", "md5")


def _new_hasher(algorithm: str):
    if algorithm not in _ALGORITHMS:
        raise EasyHashError("\n\nERROR: algorithm must be 'sha256', 'sha1', or 'md5'.")
    return hashlib.new(algorithm)


def hash_bytes(data: bytes, algorithm: str = "sha256") -> str:
    """
    Create a checksum for bytes that are already in memory.

    Args:
        data (bytes): The binary data to hash.
        algorithm (str, optional): One of `"sha256"`, `"sha1"`, or
            `"md5"`. Defaults to `"sha256"`.

    Returns:
        str: The checksum as lowercase hex.

    Raises:
        EasyHashError: If `data` is not bytes or the algorithm is not
            supported.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hash_bytes

            digest = hash_bytes(b"hello")
            print(digest)
            ```

        === "The Traditional Way"
            ```python
            import hashlib

            digest = hashlib.sha256(b"hello").hexdigest()
            print(digest)
            ```
    """
    if not isinstance(data, bytes):
        raise EasyHashError("\n\nERROR: data must be bytes.")
    hasher = _new_hasher(algorithm)
    hasher.update(data)
    return hasher.hexdigest()


def hash_text(text: str, algorithm: str = "sha256") -> str:
    """
    Create a checksum for a piece of text.

    Args:
        text (str): The text to hash.
        algorithm (str, optional): One of `"sha256"`, `"sha1"`, or
            `"md5"`. Defaults to `"sha256"`.

    Returns:
        str: The checksum as lowercase hex.

    Raises:
        EasyHashError: If `text` is not a string or the algorithm is
            not supported.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hash_text

            digest = hash_text("hello")
            ```

        === "The Traditional Way"
            ```python
            import hashlib

            digest = hashlib.sha256("hello".encode("utf-8")).hexdigest()
            ```
    """
    if not isinstance(text, str):
        raise EasyHashError("\n\nERROR: text must be a string.")
    hasher = _new_hasher(algorithm)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def hash_file(filepath: str, algorithm: str = "sha256") -> str:
    """
    Create a checksum for the contents of a file.

    Args:
        filepath (str): Path to the file.
        algorithm (str, optional): One of `"sha256"`, `"sha1"`, or
            `"md5"`. Defaults to `"sha256"`.

    Returns:
        str: The checksum as lowercase hex.

    Raises:
        EasyHashError: If the file cannot be read or the algorithm is
            not supported.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hash_file

            digest = hash_file("notes.txt")
            ```

        === "The Traditional Way"
            ```python
            import hashlib

            hasher = hashlib.sha256()
            with open("notes.txt", "rb") as f:
                hasher.update(f.read())
            digest = hasher.hexdigest()
            ```
    """
    hasher = _new_hasher(algorithm)
    try:
        hasher.update(Path(filepath).read_bytes())
    except OSError as error:
        raise EasyHashError(f"\n\nERROR: {error}") from None
    return hasher.hexdigest()


def hash_files(
    filepaths: list[str | Path] | tuple[str | Path, ...],
    algorithm: str = "sha256",
) -> dict[str, str]:
    """
    Create a checksum for each file in a list.

    Use this when you want a fingerprint per file, rather than one
    checksum for a whole folder. Paths may be strings or `pathlib.Path`
    objects. The returned keys are the paths as strings.

    Args:
        filepaths (list | tuple): Paths of the files to hash.
        algorithm (str, optional): One of `"sha256"`, `"sha1"`, or
            `"md5"`. Defaults to `"sha256"`.

    Returns:
        dict: Each path string mapped to its lowercase hex checksum.

    Raises:
        EasyHashError: If `filepaths` is not a list or tuple of paths, a
            path is not a string or path-like object, a file cannot be
            read, or the algorithm is not supported.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hash_files

            checksums = hash_files(["notes.txt", "backup.txt"])
            ```

        === "The Traditional Way"
            ```python
            import hashlib

            checksums = {}
            for path in ["notes.txt", "backup.txt"]:
                hasher = hashlib.sha256()
                with open(path, "rb") as file:
                    while chunk := file.read(64 * 1024):
                        hasher.update(chunk)
                checksums[path] = hasher.hexdigest()
            ```
    """
    if isinstance(filepaths, (str, bytes)) or not isinstance(filepaths, (list, tuple)):
        raise EasyHashError("\n\nERROR: filepaths must be a list of paths.") from None
    _new_hasher(algorithm)
    checksums = {}
    for filepath in filepaths:
        if not isinstance(filepath, (str, Path)):
            raise EasyHashError(
                "\n\nERROR: each path must be a string or path."
            ) from None
        checksums[os.fspath(filepath)] = _hash_file_chunks(filepath, algorithm)
    return checksums


def hash_directory(dirpath: str | Path, algorithm: str = "sha256") -> str:
    """
    Create a single checksum for a whole directory tree.

    Files are hashed in sorted order by their path relative to the
    directory, so the same tree always produces the same checksum no
    matter what order the files were created in. Each file contributes
    its relative path, a null separator, and the hex digest of its
    contents (fixed length for the chosen algorithm), so record
    boundaries are unambiguous and renaming a file or changing its
    contents changes the checksum.

    Args:
        dirpath (str | Path): Path to the directory.
        algorithm (str, optional): One of `"sha256"`, `"sha1"`, or
            `"md5"`. Defaults to `"sha256"`.

    Returns:
        str: The checksum as lowercase hex.

    Raises:
        EasyHashError: If `dirpath` is not a directory, a directory
            cannot be scanned, a file cannot be read, or the
            algorithm is not supported.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hash_directory

            digest = hash_directory("project")
            print(digest)
            ```

        === "The Traditional Way"
            ```python
            import hashlib
            from pathlib import Path

            hasher = hashlib.sha256()
            root = Path("project")
            for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.relative_to(root).as_posix()):
                hasher.update(path.relative_to(root).as_posix().encode("utf-8"))
                hasher.update(b"\\0")
                hasher.update(hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii"))
            digest = hasher.hexdigest()
            ```
    """
    hasher = _new_hasher(algorithm)
    root = Path(dirpath)
    if not root.is_dir():
        raise EasyHashError("\n\nERROR: dirpath must be an existing directory.")

    def _on_walk_error(error: OSError) -> None:
        raise EasyHashError(f"\n\nERROR: {error}") from None

    try:
        found = [
            Path(dirpath_) / name
            for dirpath_, _dirnames, filenames in os.walk(root, onerror=_on_walk_error)
            for name in filenames
            if (Path(dirpath_) / name).is_file()
        ]
    except EasyHashError:
        raise
    except OSError as error:
        raise EasyHashError(f"\n\nERROR: {error}") from None
    files = sorted(found, key=lambda p: p.relative_to(root).as_posix())
    for path in files:
        hasher.update(path.relative_to(root).as_posix().encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(_hash_file_chunks(path, algorithm).encode("ascii"))
    return hasher.hexdigest()


def _hash_file_chunks(filepath: str | Path, algorithm: str) -> str:
    """Helper to compute hex digest for a file using chunked reads."""
    hasher = _new_hasher(algorithm)
    try:
        with Path(filepath).open("rb") as file:
            while chunk := file.read(64 * 1024):
                hasher.update(chunk)
    except OSError as error:
        raise EasyHashError(f"\n\nERROR: {error}") from None
    return hasher.hexdigest()


def verify_file_hash(
    filepath: str | Path, expected: str, algorithm: str = "sha256"
) -> bool:
    """
    Checks whether a file matches an expected checksum using chunked reads.

    Args:
        filepath (str | Path): Path to the file to check.
        expected (str): Expected hex checksum, ignoring letter case.
            Whitespace is not stripped.
        algorithm (str, optional): One of `"sha256"`, `"sha1"`, or
            `"md5"`. Defaults to `"sha256"`.

    Returns:
        bool: True when the file's checksum equals `expected`. A mismatch,
            malformed checksum, or non-string `expected` returns False.
            Non-string checksums are rejected before reading the file or
            checking the algorithm, as with `hashes_match()`.

    Raises:
        EasyHashError: If the file cannot be read or the algorithm is
            not supported.
        TypeError: If `filepath` is not a string or path-like object.

    Example:
        === "The Py_simple Way"
            ```python
            from pathlib import Path
            from py_simple import verify_file_hash

            Path("notes.txt").write_bytes(b"hello")
            expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            matches = verify_file_hash("notes.txt", expected)
            print(matches)  # True
            ```

        === "The Traditional Way"
            ```python
            import hashlib
            from pathlib import Path

            Path("notes.txt").write_bytes(b"hello")
            expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            hasher = hashlib.sha256()
            with open("notes.txt", "rb") as file:
                while chunk := file.read(64 * 1024):
                    hasher.update(chunk)
            matches = hasher.hexdigest() == expected.lower()
            print(matches)  # True
            ```
    """
    if not isinstance(expected, str):
        return False
    _new_hasher(algorithm)
    return _hash_file_chunks(filepath, algorithm) == expected.lower()


def compare_file_hashes(
    filepath1: str | Path,
    filepath2: str | Path,
    algorithm: str = "sha256",
) -> bool:
    """
    Checks whether two files produce the same checksum using chunked reads.

    Args:
        filepath1 (str | Path): Path to the first file.
        filepath2 (str | Path): Path to the second file.
        algorithm (str, optional): One of `"sha256"`, `"sha1"`, or
            `"md5"`. Defaults to `"sha256"`.

    Returns:
        bool: True when both files have matching checksums, False otherwise.

    Raises:
        EasyHashError: If either file cannot be read or the algorithm is
            not supported.
        TypeError: If either path is not a string or path-like object.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import compare_file_hashes

            identical = compare_file_hashes("file1.txt", "file2.txt")
            print(identical)
            ```

        === "The Traditional Way"
            ```python
            import hashlib

            def get_checksum(filepath):
                hasher = hashlib.sha256()
                with open(filepath, "rb") as f:
                    while chunk := f.read(64 * 1024):
                        hasher.update(chunk)
                return hasher.hexdigest()

            identical = get_checksum("file1.txt") == get_checksum("file2.txt")
            print(identical)
            ```
    """
    _new_hasher(algorithm)
    p1 = Path(filepath1)
    p2 = Path(filepath2)
    return _hash_file_chunks(p1, algorithm) == _hash_file_chunks(p2, algorithm)


def hashes_match(text: str, expected: str, algorithm: str = "sha256") -> bool:
    """
    Check whether text matches an expected checksum.

    Args:
        text (str): The text to check.
        expected (str): The checksum you expected, in hex.
        algorithm (str, optional): Algorithm used to build `expected`.
            Defaults to `"sha256"`.

    Returns:
        bool: True when the checksum of `text` equals `expected`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hashes_match

            expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            hashes_match("hello", expected)
            ```

        === "The Traditional Way"
            ```python
            import hashlib

            digest = hashlib.sha256("hello".encode("utf-8")).hexdigest()
            matches = digest == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            ```
    """
    if not isinstance(expected, str):
        return False
    return hash_text(text, algorithm) == expected.lower()
