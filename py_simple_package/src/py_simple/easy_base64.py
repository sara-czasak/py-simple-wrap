"""
easy_base64 turns text into Base64 and back without the encoding boilerplate.
"""

import base64
import binascii


class EasyBase64Error(Exception):
    """
    Raised when text cannot be encoded or decoded as Base64.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def encode_text(text: str) -> str:
    """
    Encode a piece of text as a Base64 string.

    Args:
        text (str): The text to encode.

    Returns:
        str: The Base64 text, safe to paste into a file or a message.

    Raises:
        EasyBase64Error: If `text` is not a string.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import encode_text

            secret = encode_text("hello")
            ```

        === "The Traditional Way"
            ```python
            import base64

            secret = base64.b64encode("hello".encode("utf-8")).decode("ascii")
            ```
    """
    if not isinstance(text, str):
        raise EasyBase64Error("\n\nERROR: text must be a string.")
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def decode_text(encoded: str) -> str:
    """
    Decode a Base64 string back into text.

    Args:
        encoded (str): Base64 text, such as the result of `encode_text`.

    Returns:
        str: The original text.

    Raises:
        EasyBase64Error: If `encoded` is not valid Base64 text.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import decode_text

            message = decode_text("aGVsbG8=")
            ```

        === "The Traditional Way"
            ```python
            import base64

            message = base64.b64decode("aGVsbG8=").decode("utf-8")
            ```
    """
    if not isinstance(encoded, str):
        raise EasyBase64Error("\n\nERROR: encoded text must be a string.")
    try:
        return base64.b64decode(encoded, validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as error:
        raise EasyBase64Error(f"\n\nERROR: {error}") from None


def is_base64(value: str) -> bool:
    """
    Check whether a string is valid Base64.

    Args:
        value (str): The text to check.

    Returns:
        bool: True when `value` can be decoded as Base64, otherwise False.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_base64

            is_base64("aGVsbG8=")  # True
            ```

        === "The Traditional Way"
            ```python
            import base64

            try:
                base64.b64decode("aGVsbG8=", validate=True)
                ok = True
            except ValueError:
                ok = False
            ```
    """
    if not isinstance(value, str) or value == "":
        return False
    try:
        base64.b64decode(value, validate=True)
    except ValueError:
        return False
    return True


def encode_bytes(data: bytes) -> str:
    """
    Encode raw bytes as a Base64 string.

    Useful when working with binary data such as images, audio, or file
    contents that are already in bytes form and not text.

    Args:
        data (bytes): The bytes to encode.

    Returns:
        str: The Base64 text, safe to paste into a file or a message.

    Raises:
        EasyBase64Error: If `data` is not bytes.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import encode_bytes

            encoded = encode_bytes(b"\\x00\\x01\\x02")
            ```

        === "The Traditional Way"
            ```python
            import base64

            encoded = base64.b64encode(b"\\x00\\x01\\x02").decode("ascii")
            ```
    """
    if not isinstance(data, bytes):
        raise EasyBase64Error("\n\nERROR: data must be bytes.")
    return base64.b64encode(data).decode("ascii")


def decode_to_bytes(encoded: str) -> bytes:
    """
    Decode a Base64 string back into raw bytes.

    The counterpart of `encode_bytes`. Use this when you need the original
    bytes rather than text (for example when the encoded data is an image
    or a binary file).

    Args:
        encoded (str): Base64 text, such as the result of `encode_bytes`.

    Returns:
        bytes: The original bytes.

    Raises:
        EasyBase64Error: If `encoded` is not valid Base64 text.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import decode_to_bytes

            raw = decode_to_bytes("AAEC")
            ```

        === "The Traditional Way"
            ```python
            import base64

            raw = base64.b64decode("AAEC")
            ```
    """
    if not isinstance(encoded, str):
        raise EasyBase64Error("\n\nERROR: encoded text must be a string.")
    try:
        return base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError, UnicodeDecodeError) as error:
        raise EasyBase64Error(f"\n\nERROR: {error}") from None


def encode_file(file_path: str) -> str:
    """
    Encode the contents of a file as a Base64 string.

    Reads a file in binary mode and returns its contents encoded as Base64.
    Useful for embedding icons, images, or documents into JSON, HTML, or API payloads.

    Args:
        file_path (str): Path to the file to encode.

    Returns:
        str: The Base64 text representing the file's contents.

    Raises:
        EasyBase64Error: If `file_path` is not a string, the file is not found,
            or an error occurs reading the file.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import encode_file

            data = encode_file("logo.png")
            ```

        === "The Traditional Way"
            ```python
            import base64

            with open("logo.png", "rb") as file:
                data = base64.b64encode(file.read()).decode("ascii")
            ```
    """
    if not isinstance(file_path, str):
        raise EasyBase64Error("\n\nERROR: file_path must be a string.")
    try:
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("ascii")
    except (FileNotFoundError, OSError) as error:
        raise EasyBase64Error(f"\n\nERROR: {error}") from None


def decode_to_file(encoded: str, file_path: str) -> None:
    """
    Decode a Base64 string and save the decoded bytes to a file.

    Useful for saving images, documents, or downloaded assets received as Base64
    directly to disk without juggling binary file handling and decoding manually.

    Args:
        encoded (str): Base64 text to decode.
        file_path (str): Path to the destination file.

    Raises:
        EasyBase64Error: If `encoded` or `file_path` is not a string, `encoded`
            is not valid Base64 text, or an error occurs writing the file.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import decode_to_file

            decode_to_file("aGVsbG8gd29ybGQ=", "greeting.txt")
            ```

        === "The Traditional Way"
            ```python
            import base64

            raw = base64.b64decode("aGVsbG8gd29ybGQ=", validate=True)
            with open("greeting.txt", "wb") as file:
                file.write(raw)
            ```
    """
    if not isinstance(encoded, str):
        raise EasyBase64Error("\n\nERROR: encoded text must be a string.")
    if not isinstance(file_path, str):
        raise EasyBase64Error("\n\nERROR: file_path must be a string.")

    data = decode_to_bytes(encoded)

    try:
        with open(file_path, "wb") as file:
            file.write(data)
    except (FileNotFoundError, OSError) as error:
        raise EasyBase64Error(f"\n\nERROR: {error}") from None


def encode_urlsafe_text(text: str) -> str:
    """
    Encode text as Base64 using the URL-safe alphabet.

    Uses '-' and '_' instead of '+' and '/'. Standard '=' padding is kept;
    use a URL query builder when placing the result in a query string.
    Base64 is reversible encoding, not encryption.

    Args:
        text (str): Text to encode as UTF-8, including Unicode text.

    Returns:
        str: URL-safe Base64 text, or an empty string for empty input.

    Raises:
        EasyBase64Error: If `text` is not a string or cannot be UTF-8 encoded.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import encode_urlsafe_text

            encoded = encode_urlsafe_text("hello?")  # 'aGVsbG8_'
            ```

        === "The Traditional Way"
            ```python
            import base64

            encoded = base64.urlsafe_b64encode("hello?".encode("utf-8")).decode("ascii")
            ```

    Note:
        Decode with `base64.urlsafe_b64decode(encoded).decode("utf-8")`.
        `decode_text` accepts the standard Base64 alphabet, not '-' and '_'.
    """
    if not isinstance(text, str):
        raise EasyBase64Error("\n\nERROR: text must be a string.")
    try:
        return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii")
    except UnicodeEncodeError as error:
        raise EasyBase64Error(f"\n\nERROR: {error}") from None
