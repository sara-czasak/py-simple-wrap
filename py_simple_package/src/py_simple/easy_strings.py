"""Beginner-friendly helpers for common string operations."""

import re


def remove_extra_spaces(text: str) -> str:
    """
    Removes leading, trailing, and repeated spaces from text.

    Args:
        text (str): Text to clean up.

    Returns:
        str: Text with extra whitespace removed.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import remove_extra_spaces

            result = remove_extra_spaces("  hello   world  ")
            # -> "hello world"
            ```

        === "The Traditional Way"
            ```python
            text = "  hello   world  "
            result = " ".join(text.split())
            ```
    """
    return " ".join(text.split())


def to_snake_case(text: str) -> str:
    """
    Converts text to snake_case.

    Args:
        text (str): Text to convert.

    Returns:
        str: Text converted to snake_case.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import to_snake_case

            result = to_snake_case("Hello World")  # -> "hello_world"
            ```

        === "The Traditional Way"
            ```python
            import re

            text = "Hello World"
            cleaned = re.sub(r"[^\\w\\s]", " ", text)
            result = "_".join(cleaned.lower().split())
            ```
    """
    cleaned_text = _separate_words(text)
    return cleaned_text.lower().replace(" ", "_")


def to_kebab_case(text: str) -> str:
    """
    Converts text to kebab-case.

    Args:
        text (str): Text to convert.

    Returns:
        str: Text converted to kebab-case.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import to_kebab_case

            result = to_kebab_case("Hello World")  # -> "hello-world"
            ```

        === "The Traditional Way"
            ```python
            import re

            text = "Hello World"
            cleaned = re.sub(r"[^\\w\\s]", " ", text)
            result = "-".join(cleaned.lower().split())
            ```
    """
    cleaned_text = _separate_words(text)
    return cleaned_text.lower().replace(" ", "-")


def to_title_case(text: str) -> str:
    """
        Converts text to Title Case, where the first letter of each word
        is capitalized and the rest are lowercased. Preserves apostrophes so
        contractions like "don't" stay intact.

        Args:
            text (str): Text to convert.

        Returns:
            str: Text converted to Title Case.

        Example:
            === "The Py_simple Way"
    ```python
                from py_simple import to_title_case
                result = to_title_case("hello world")  # -> "Hello World"
    ```
            === "The Traditional Way"
    ```python
                text = "hello world"
                result = " ".join(word.capitalize() for word in text.split())
    ```
    """
    # Same normalization pipeline as _separate_words, but preserve
    # apostrophes so contractions like "don't" survive.
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    text = re.sub(r"[_\-]+", " ", text)
    text = re.sub(r"[^\w\s']", " ", text)
    text = remove_extra_spaces(text)

    result_words = []
    for word in text.split():
        result_words.append(_capitalize_word(word))
    return " ".join(result_words)


def is_palindrome(text: str) -> bool:
    """
    Returns True when text reads the same forwards and backwards.

    Spaces, punctuation, and letter casing are ignored.

    Args:
        text (str): Text to check.

    Returns:
        bool: True if text is a palindrome, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_palindrome

            result = is_palindrome("Never odd or even")  # -> True
            ```

        === "The Traditional Way"
            ```python
            text = "Never odd or even"
            cleaned = "".join(c.lower() for c in text if c.isalnum())
            result = cleaned == cleaned[::-1]
            ```
    """
    cleaned_text = "".join(
        character.lower() for character in text if character.isalnum()
    )
    return cleaned_text == cleaned_text[::-1]


def is_alphanumeric(text: str) -> bool:
    """
    Returns True if text only contains letters and numbers,
    and False otherwise.

    Args:
        text (str): Text to check.

    Returns:
        bool: True if text is alphanumeric, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_palindrome

            result = is_alphanumeric("Something123")  # -> True
            ```

        === "The Traditional Way"
            ```python
            text = "Something123"
                if text.isalnum():
                    return True
                else:
                    return False
            ```
    """
    return bool(text.isalnum())


def count_words(text: str) -> int:
    """
    Counts the total number of words in a text string.

    Args:
        text (str): Text to process.

    Returns:
        int: Number of words found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_words

            result = count_words("Hello world! How are you?") # -> 5
            ```

        === "The Traditional Way"
            ```python
            import re

            text = "Hello world! How are you?"
            cleaned = re.sub(r"[^\\w\\s]", " ", text)
            result = len(cleaned.split())
            ```
    """
    cleaned_text = _separate_words(text)
    if not cleaned_text:
        return 0
    return len(cleaned_text.split())


def _separate_words(text: str) -> str:
    """Normalizes common word separators and separates camel-case words."""
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    text = re.sub(r"[_\-]+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return remove_extra_spaces(text)


def _capitalize_word(word: str) -> str:
    """Uppercases the first alphabetic character, lowercases the rest."""
    for i, character in enumerate(word):
        if character.isalpha():
            return word[:i] + character.upper() + word[i + 1 :].lower()
    return word
