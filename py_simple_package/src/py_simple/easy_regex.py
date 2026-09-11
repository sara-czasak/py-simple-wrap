"""
easy_regex is built to simplify pulling common patterns (emails, URLs,
numbers) out of text without writing your own regex.
"""

import re


def extract_emails(text: str) -> list | None:
    r"""
    Returns a list of all email addresses found in the text.

    Arguments:
        text (str): Text to search for email addresses.

    Returns:
        list: All email addresses found in the text. Empty list if none found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import extract_emails

            result = extract_emails("Contact us at hello@example.com or support@test.org")
            # -> ['hello@example.com', 'support@test.org']
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = r'[a-zA-Z_.%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+'
            result = re.findall(pattern, "Contact us at hello@example.com or support@test.org")
            # -> ['hello@example.com', 'support@test.org']
            ```
    """
    pattern = r"[a-zA-Z0-9_.%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+"
    return re.findall(pattern, text)


def extract_urls(text: str) -> list | None:
    r"""
    Returns a list of all URLs found in the text.

    Arguments:
        text (str): Text to search for URLs.

    Returns:
        list: All URLs found in the text. Empty list if none found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import extract_urls

            result = extract_urls("Visit https://www.example.com or www.test.org today")
            # -> ['https://www.example.com', 'www.test.org']
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = (r'(?:https?://(?:www\.)?|www\.)[a-zA-Z0-9-]+\.
            (?:(?:[a-zA-Z0-9-]+\.)*)?(?:(?:[a-zA-Z0-9-]+\\)*)?[a-zA-Z]{2,}
            (?:\.[a-zA-Z]{2,})?(?:/\S*)?')
            result = re.findall(pattern, "Visit https://www.example.com or www.test.org today")
            # -> ['https://www.example.com', 'www.test.org']
            ```
    """
    pattern = (
        r"(?:https?://(?:www\.)?|www\.)[a-zA-Z0-9-]+\.(?:(?:[a-zA-Z0-9-]+\.)*)?(?:(?:[a-zA-Z0-9-]+\\)*)?[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?"
        r"(?:/\S*)?"
    )
    return re.findall(pattern, text)


def extract_number_sequences(text: str) -> list | None:
    r"""
    Returns a list of number sequences found in the text, where numbers are
    joined by a separator such as -, _, : or . (e.g. dates, times, IP addresses,
    version numbers, or IDs).

    Arguments:
        text (str): Text to search for number sequences.

    Returns:
        list: All number sequences found in the text. Empty list if none found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import extract_number_sequences

            result = extract_number_sequences("Server 192.168.1.1 logged in at 14:32 on 04-08-2026")
            # -> ['192.168.1.1', '14:32', '04-08-2026']
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = r'[0-9]+(?:(?:-|_|:|\.)?[0-9]+)+'
            result = re.findall(pattern, "Server 192.168.1.1 logged in at 14:32 on 04-08-2026")
            # -> ['192.168.1.1', '14:32', '04-08-2026']
            ```
    """
    pattern = r"[0-9]+(?:(?:-|_|:|\.)?[0-9]+)+"
    return re.findall(pattern, text)


def extract_numbers(text: str) -> list | None:
    r"""
    Returns a list of all standalone digit sequences found in the text.

    Arguments:
        text (str): Text to search for numbers.

    Returns:
        list: All digit sequences found in the text. Empty list if none found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import extract_numbers

            result = extract_numbers("I have 3 cats and 12 fish")
            # -> ['3', '12']
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = r'[0-9]+'
            result = re.findall(pattern, "I have 3 cats and 12 fish")
            # -> ['3', '12']
            ```
    """
    pattern = r"[0-9]+"
    return re.findall(pattern, text)


def extract_hex_colors(text: str) -> list | None:
    r"""
    Returns a list of CSS-style hexadecimal color codes found in the text.

    Supports the 3, 4, 6, and 8 digit forms, including their leading `#`.

    Arguments:
        text (str): Text to search for hexadecimal color codes.

    Returns:
        list: All hexadecimal color codes found in the text. Empty list if
            none are found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import extract_hex_colors

            result = extract_hex_colors("Use #fff on #1a2b3c")
            # -> ['#fff', '#1a2b3c']
            ```

        === "The Traditional Way"
            ```python
            import re

            pattern = (
                r'(?<![\\w#])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|'
                r'[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\\b'
            )
            result = re.findall(pattern, "Use #fff on #1a2b3c")
            # -> ['#fff', '#1a2b3c']
            ```
    """
    pattern = (
        r"(?<![\w#])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|"
        r"[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b"
    )
    return re.findall(pattern, text)
