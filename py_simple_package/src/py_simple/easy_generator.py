"""
easy_generator helps generate things faster.
"""

import os
import random
import re
import secrets
import string
import unicodedata
import uuid

import qrcode


class EasyGeneratorError(Exception):
    """
    Raised when a value can't be generated.

    Wraps whatever the underlying operation raises internally (bad
    length/character counts, missing data, qrcode/PIL errors, etc.)
    so py_simple functions can fail with one consistent,
    easy-to-read exception instead of a random builtin or
    library-specific one.

    Args:
        message (str): Human-readable description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def generate_password(
    pass_length: int = 12,
    uppercase_chars: int = 2,
    digit_chars: int = 2,
    special_chars: int = 2,
) -> str:
    """
    Generates a randomized password of a given length in one call,
    handling the character-pool selection, shuffling, and
    repeated-character checks every password generator needs, instead
    of writing that logic by hand each time.

    Args:
        pass_length (int, optional): Total number of characters in the
            generated password. Defaults to `12`.
        uppercase_chars (int, optional): Number of uppercase letters to
            include. Defaults to `2`.
        digit_chars (int, optional): Number of digits to include.
            Defaults to `2`.
        special_chars (int, optional): Number of punctuation characters
            to include. Defaults to `2`.

    Returns:
        str: The generated password, made up of lowercase letters,
            uppercase letters, digits, and special characters shuffled
            together, with no two identical characters placed next to
            each other. The number of lowercase letters is calculated
            as `pass_length - (uppercase_chars + digit_chars + special_chars)`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import generate_password

            password = generate_password(16, uppercase_chars=3, digit_chars=3, special_chars=3)
            ```

        === "The Traditional Way"
            ```python
            import string
            import random

            length = 16
            uppercase_chars = 3
            digit_chars = 3
            special_chars = 3
            lowercase_chars = length - (uppercase_chars + digit_chars + special_chars)

            chars = (
                [random.choice(string.ascii_lowercase) for _ in range(lowercase_chars)]
                + [random.choice(string.ascii_uppercase) for _ in range(uppercase_chars)]
                + [random.choice(string.digits) for _ in range(digit_chars)]
                + [random.choice(string.punctuation) for _ in range(special_chars)]
            )
            random.shuffle(chars)
            password = ''.join(chars)
            ```
    """
    lowercase_chars = pass_length - (special_chars + digit_chars + uppercase_chars)
    lower_chars = [
        secrets.choice(string.ascii_lowercase) for _ in range(lowercase_chars)
    ]
    upper_chars = [
        secrets.choice(string.ascii_uppercase) for _ in range(uppercase_chars)
    ]
    digit_chars = [secrets.choice(string.digits) for _ in range(digit_chars)]
    special_chars = [secrets.choice(string.punctuation) for _ in range(special_chars)]

    pass_chars = [i for i in lower_chars + upper_chars + digit_chars + special_chars]

    all_clear = False
    while not all_clear:
        last_char = None
        random.shuffle(pass_chars)
        for char in pass_chars:
            if char == last_char:
                all_clear = False
                break
            else:
                last_char = char
            all_clear = True

    return "".join(pass_chars)


def generate_slug(text: str) -> str:
    """
    Generates a slug(URL-friendly string) from string.

    Args:
        text (str): The text to be converted to a slug.

    Returns:
        str: A URL-friendly slug.

    Raises:
        EasyGeneratorError: If `str` is empty, or if the
        slug conversion fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import generate_slug

            text = "Hello This-Becomes_A slug"
            slug = generate_slug(text)
            print(slug)  # 'hello-this-becomes-a-slug'
            ```

        === "The Traditional Way"
            ```python
            import re
            import unicodedata

            text = "Hello This-Becomes_A slug"

            normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
            lowercased = normalized.lower()
            slug = re.sub(r"[^a-z0-9]+", "-", lowercased).strip("-")
            print(slug)
    """
    if not isinstance(text, str):
        raise EasyGeneratorError("You need to provide a string.")
    # Unicode Normalization Form KD (NFKD) is the most aggressive normalization form
    normalized_text = (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    )
    lowercased_text = normalized_text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowercased_text).strip("-")
    if not slug:
        raise EasyGeneratorError("This string has no valid characters to convert.")
    return slug


def generate_qr_code(data_to_encode: str) -> None:
    """
    Generates a QR code image from the given data and saves it to disk
    in one call, handling the qrcode image creation and non-overwriting
    filename selection every QR code generator needs.

    Args:
        data_to_encode (str): The text or data to encode in the QR
            code (e.g. a URL, message, or other string).

    Returns:
        None: The QR code is saved directly to disk as
            `qrcode{num}.png`, where `num` is the smallest
            non-negative integer that does not collide with an
            existing file in the current directory.

    Raises:
        EasyGeneratorError: If `data_to_encode` is empty, or if the
            QR code image can't be created or saved (e.g. an
            underlying qrcode/PIL error).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import generate_qr_code

            generate_qr_code("https://example.com")
            ```

        === "The Traditional Way"
            ```python
            import qrcode
            import os

            data = "https://example.com"
            img = qrcode.make(data)

            num = 0
            while os.path.exists(f'qrcode{num}.png'):
                num += 1
            img.save(f'qrcode{num}.png')
            ```
    """
    if not data_to_encode:
        raise EasyGeneratorError("You need to provide some data to encode")
    try:
        img = qrcode.make(data_to_encode)

        num = 0
        good_filename = False
        while not good_filename:
            if os.path.exists(f"qrcode{num}.png"):
                num += 1
            else:
                good_filename = True
        img.save(f"qrcode{num}.png")
    except Exception as e:
        raise EasyGeneratorError(f"\n\n\nERROR: {e}")


def generate_uuid() -> str:
    """
    Generates a random UUID (version 4) as a string in one call, so
    you don't need to import `uuid` and remember which version to use.

    Returns:
        str: A randomly generated UUID, formatted as the standard
            `8-4-4-4-12` hex string (e.g.
            `"3f2504e0-4f89-11d3-9a0c-0305e82c3301"`).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import generate_uuid

            result = generate_uuid()  # -> "3f2504e0-4f89-11d3-9a0c-0305e82c3301"
            ```

        === "The Traditional Way"
            ```python
            import uuid

            result = str(uuid.uuid4())
            ```
    """

    return str(uuid.uuid4())


def generate_api_key() -> str:
    """
    Generates a secure, random, URL-safe API key in one call, using
    Python's `secrets` module so the result is safe for tokens,
    API keys, and other security-sensitive values.

    Returns:
        str: A random, URL-safe text string suitable for use as an
            API key or access token.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import generate_api_key

            key = generate_api_key()
            ```

        === "The Traditional Way"
            ```python
            import secrets

            key = secrets.token_urlsafe(64)
            ```
    """
    return secrets.token_urlsafe(64)


def generate_otp(length: int = 4, with_letters: bool = False) -> str:
    """
    Generates a random one-time password (OTP) code of a given length
    in one call, handling the character-pool selection every OTP
    generator needs.

    Args:
        length (int, optional): Number of characters in the generated
            code. Defaults to `4`.
        with_letters (bool, optional): If `True`, the code is drawn
            from both letters and digits. If `False`, the code is
            digits only. Defaults to `False`.

    Returns:
        str: The generated OTP code.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import generate_otp

            code = generate_otp(6, with_letters=True)
            ```

        === "The Traditional Way"
            ```python
            import random
            import string

            length = 6
            otp_chars = string.ascii_letters + string.digits
            code = "".join(random.choice(otp_chars) for _ in range(length))
            ```
    """
    otp = ""
    if length >= 4:
        if with_letters:
            otp_chars = string.ascii_letters + string.digits
            for i in range(length):
                otp += str(secrets.choice(otp_chars))
        else:
            for i in range(length):
                otp += str(secrets.randbelow(10))
        return otp
    else:
        raise EasyGeneratorError("\n\n\nERROR: OTP length must be at least 4") from None
