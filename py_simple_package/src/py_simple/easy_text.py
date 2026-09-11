"""Beginner-friendly helpers for common text formatting and cleaning."""

import re


def truncate(text: str, length: int) -> str:
    """
    Shortens text to the given length and adds an ellipsis character.

    Args:
        text (str): Text to shorten.
        length (int): Maximum number of characters to keep.

    Returns:
        str: Shortened text, or the original text if it is short enough.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import truncate

            result = truncate("Hello world!", 5)  # -> "Hello…"
            ```

        === "The Traditional Way"
            ```python
            text, length = "Hello world!", 5
            result = text[:length] + "…" if len(text) > length else text
            ```
    """
    if len(text) <= length:
        return text
    return text[:length] + "…"


def remove_punctuation(text: str) -> str:
    """
    Removes punctuation from text, keeping letters, numbers, and spaces.

    Args:
        text (str): Text to clean.

    Returns:
        str: Text without punctuation.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import remove_punctuation

            result = remove_punctuation("Hello, world!")  # -> "Hello world"
            ```

        === "The Traditional Way"
            ```python
            import string

            text = "Hello, world!"
            result = "".join(c for c in text if c not in string.punctuation)
            ```
    """
    return "".join(
        character for character in text if character.isalnum() or character.isspace()
    )


def reverse_words(text: str) -> str:
    """
    Reverses the order of words in text.

    Args:
        text (str): Text to reverse.

    Returns:
        str: Text with words in reverse order.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import reverse_words

            result = reverse_words("Hello world")  # -> "world Hello"
            ```

        === "The Traditional Way"
            ```python
            text = "Hello world"
            result = " ".join(text.split()[::-1])
            ```
    """
    return " ".join(text.split()[::-1])


def capitalize_title(text: str) -> str:
    """
    Capitalizes the first letter of every word in text.

    Args:
        text (str): Text to capitalize.

    Returns:
        str: Text with every word capitalized.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import capitalize_title

            result = capitalize_title("the great gatsby")  # -> "The Great Gatsby"
            ```

        === "The Traditional Way"
            ```python
            text = "the great gatsby"
            result = text.title()
            ```
    """
    return text.title()


def count_letters(text: str) -> int:
    """
    Counts the number of letters in text.

    Args:
        text (str): Text to count.

    Returns:
        int: Number of letters (a-z, A-Z, and accented letters).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_letters

            result = count_letters("Hello 123!")  # -> 5
            ```

        === "The Traditional Way"
            ```python
            text = "Hello 123!"
            result = sum(1 for c in text if c.isalpha())
            ```
    """
    return sum(1 for character in text if character.isalpha())


def count_digits(text: str) -> int:
    """
    Counts the number of digits in text.

    Args:
        text (str): Text to count.

    Returns:
        int: Number of digits (0-9).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_digits

            result = count_digits("Hello 123!")  # -> 3
            ```

        === "The Traditional Way"
            ```python
            text = "Hello 123!"
            result = sum(1 for c in text if c.isdigit())
            ```
    """
    return sum(1 for character in text if character.isdigit())


def mask_part(text: str, visible: int = 4) -> str:
    """
    Hides part of text (like a card number) behind asterisks.

    The first `visible` characters stay visible, the rest are masked.

    Args:
        text (str): Text to mask.
        visible (int): Number of characters to keep visible. Defaults to 4.

    Returns:
        str: Masked text.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import mask_part

            result = mask_part("1234567890", 4)  # -> "1234 ******"
            ```

        === "The Traditional Way"
            ```python
            text, visible = "1234567890", 4
            result = text[:visible] + " " + "*" * len(text[visible:])
            ```
    """
    if visible >= len(text):
        return text
    return text[:visible] + " " + "*" * len(text[visible:])


def pluralize(word: str, count: int) -> str:
    """
    Returns the singular or plural form of a word based on the count.

    Args:
        word (str): Word to pluralize.
        count (int): Number of items.

    Returns:
        str: Singular word if count is 1, plural word otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import pluralize

            result = pluralize("cat", 3)  # -> "cats"
            ```

        === "The Traditional Way"
            ```python
            word, count = "cat", 3
            result = word if count == 1 else word + "s"
            ```
    """
    if count == 1:
        return word
    if word.endswith("s"):
        return word + "es"
    return word + "s"


def extract_hashtags(text: str) -> list:
    """
    Extracts all hashtags from text, without the # symbol.

    Args:
        text (str): Text to search.

    Returns:
        list: Hashtag words found in the text.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import extract_hashtags

            result = extract_hashtags("Loving #python and #coding!")
            # -> ["python", "coding"]
            ```

        === "The Traditional Way"
            ```python
            import re

            text = "Loving #python and #coding!"
            result = re.findall(r"#(\\w+)", text)
            ```
    """
    return re.findall(r"#(\w+)", text)


def word_frequency(text: str) -> dict:
    """
    Counts how often each word appears in text.

    Punctuation is ignored and words are counted in lowercase.

    Args:
        text (str): Text to analyze.

    Returns:
        dict: Word counts, keyed by word.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import word_frequency

            result = word_frequency("the cat and the dog")
            # -> {"the": 2, "cat": 1, "and": 1, "dog": 1}
            ```

        === "The Traditional Way"
            ```python
            import re
            from collections import Counter

            text = "the cat and the dog"
            words = re.sub(r"[^\\w\\s]", "", text).lower().split()
            result = dict(Counter(words))
            ```
    """
    frequency = {}
    for word in remove_punctuation(text).lower().split():
        frequency[word] = frequency.get(word, 0) + 1
    return frequency
