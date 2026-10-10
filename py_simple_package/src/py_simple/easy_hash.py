"""
easy_hash creates checksums for text and files without the hashlib boilerplate.
"""

import hashlib
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
        raise EasyHashError(
            "\n\nERROR: algorithm must be 'sha256', 'sha1', or 'md5'."
        )
    return hashlib.new(algorithm)


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

            hashes_match("hello", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
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
