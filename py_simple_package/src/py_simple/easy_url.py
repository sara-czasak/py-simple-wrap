"""
easy_url reads and edits links without the urllib boilerplate.
"""

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


class EasyUrlError(Exception):
    """
    Raised when a link cannot be read or updated.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _parsed(url: str):
    if not isinstance(url, str) or not url.strip():
        raise EasyUrlError("\n\nERROR: url must be a non-empty string.") from None
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise EasyUrlError("\n\nERROR: url must include a scheme and a host.") from None
    return parsed


def get_domain(url: str) -> str:
    """
    Return the host name from a link.

    Args:
        url (str): A full link, such as `"https://school.example/clubs"`.

    Returns:
        str: The host, such as `"school.example"`.

    Raises:
        EasyUrlError: If `url` is not a full link.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_domain

            print(get_domain("https://school.example/clubs"))
            ```

        === "The Traditional Way"
            ```python
            from urllib.parse import urlparse

            print(urlparse("https://school.example/clubs").hostname)
            ```
    """
    return _parsed(url).hostname or ""


def is_https(url: str) -> bool:
    """
    Check whether a link uses HTTPS.

    Args:
        url (str): A full link.

    Returns:
        bool: True when the scheme is `https`.

    Raises:
        EasyUrlError: If `url` is not a full link.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_https

            is_https("https://school.example")
            ```

        === "The Traditional Way"
            ```python
            from urllib.parse import urlparse

            urlparse("https://school.example").scheme == "https"
            ```
    """
    return _parsed(url).scheme == "https"


def add_query_param(url: str, key: str, value: str) -> str:
    """
    Add or replace one query parameter on a link.

    Replaces all occurrences of the selected key with one value at its
    first position, or appends it if absent. Other parameters retain
    their order, repeated values, and blank values.

    Args:
        url (str): A full link.
        key (str): Parameter name, such as `"page"`.
        value (str): Parameter value, such as `"2"`.

    Returns:
        str: The link with that parameter set.

    Raises:
        EasyUrlError: If `url` is not a full link, or if `key` or
            `value` is not a string.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import add_query_param

            print(add_query_param("https://school.example/clubs", "page", "2"))
            ```

        === "The Traditional Way"
            ```python
            from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

            parsed = urlparse("https://school.example/clubs")
            pairs = parse_qsl(parsed.query, keep_blank_values=True)
            query = []
            replaced = False
            for key, value in pairs:
                if key == "page":
                    if not replaced:
                        query.append(("page", "2"))
                        replaced = True
                else:
                    query.append((key, value))
            if not replaced:
                query.append(("page", "2"))
            print(urlunparse(parsed._replace(query=urlencode(query))))
            ```
    """
    if not isinstance(key, str) or not isinstance(value, str) or key == "":
        raise EasyUrlError(
            "\n\nERROR: key and value must be strings, and key cannot be empty."
        ) from None
    parsed = _parsed(url)
    query = []
    replaced = False
    for name, current_value in parse_qsl(parsed.query, keep_blank_values=True):
        if name == key:
            if not replaced:
                query.append((key, value))
                replaced = True
        else:
            query.append((name, current_value))
    if not replaced:
        query.append((key, value))
    return urlunparse(parsed._replace(query=urlencode(query)))


def get_path(url: str) -> str:
    """
    Return the path component from a link.

    Args:
        url (str): A full link, such as `"https://school.example/clubs/art"`.

    Returns:
        str: The path, such as `"/clubs/art"`. Returns `"/"` if no path is given.

    Raises:
        EasyUrlError: If `url` is not a full link.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_path

            print(get_path("https://school.example/clubs/art"))
            ```

        === "The Traditional Way"
            ```python
            from urllib.parse import urlparse

            print(urlparse("https://school.example/clubs/art").path or "/")
            ```
    """
    return _parsed(url).path or "/"
