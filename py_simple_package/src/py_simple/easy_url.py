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
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
    except ValueError as error:
        raise EasyUrlError(f"\n\nERROR: {error}") from None
    if not parsed.scheme or not hostname:
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
            query = dict(parse_qsl(parsed.query))
            query["page"] = "2"
            print(urlunparse(parsed._replace(query=urlencode(query))))
            ```
    """
    if not isinstance(key, str) or not isinstance(value, str) or key == "":
        raise EasyUrlError(
            "\n\nERROR: key and value must be strings, and key cannot be empty."
        ) from None
    parsed = _parsed(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query[key] = value
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


def remove_query_param(url: str, key: str) -> str:
    """
    Remove one query parameter from a link.

    The counterpart to `add_query_param`: where that function sets a
    parameter, this one drops it. All other parameters, and the rest
    of the link, are left unchanged. Removing a parameter that is not
    present returns the link unchanged.

    Args:
        url (str): A full link.
        key (str): Parameter name to remove, such as `"page"`.

    Returns:
        str: The link without that parameter.

    Raises:
        EasyUrlError: If `url` is not a full link, or if `key` is not
            a non-empty string.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import remove_query_param

            print(remove_query_param("https://school.example/clubs?page=2&sort=name", "page"))
            ```

        === "The Traditional Way"
            ```python
            from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

            parsed = urlparse("https://school.example/clubs?page=2&sort=name")
            query = [(k, v) for k, v in parse_qsl(parsed.query) if k != "page"]
            print(urlunparse(parsed._replace(query=urlencode(query))))
            ```
    """
    if not isinstance(key, str) or key == "":
        raise EasyUrlError("\n\nERROR: key must be a non-empty string.") from None
    parsed = _parsed(url)
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    remaining = [(k, v) for k, v in pairs if k != key]
    if len(remaining) == len(pairs):
        return url
    return urlunparse(parsed._replace(query=urlencode(remaining)))


def get_query_values(url: str, key: str) -> list[str]:
    """
    Return all values for one query parameter, in their original order.

    Args:
        url (str): A full link, including a scheme and host.
        key (str): Non-empty, decoded parameter name, such as `"tag"`.
            Names are case-sensitive.

    Returns:
        list[str]: Decoded values, including repeats and empty strings for
            blank values or parameters without `=`. Returns an empty list
            when the name is absent. Percent escapes are decoded as UTF-8
            with replacement for invalid bytes; `+` becomes a space.
            The link is not changed.

    Raises:
        EasyUrlError: If `url` is not a full link, or `key` is not a
            non-empty string.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_query_values

            link = "https://school.example/clubs?tag=python&tag=&tag=art+club#list"
            print(get_query_values(link, "tag"))
            ```

        === "The Traditional Way"
            ```python
            from urllib.parse import parse_qsl, urlparse

            link = "https://school.example/clubs?tag=python&tag=&tag=art+club#list"
            pairs = parse_qsl(urlparse(link).query, keep_blank_values=True)
            print([value for name, value in pairs if name == "tag"])
            ```
    """
    if not isinstance(key, str) or key == "":
        raise EasyUrlError("\n\nERROR: key must be a non-empty string.") from None
    parsed = _parsed(url)
    return [
        value
        for name, value in parse_qsl(parsed.query, keep_blank_values=True)
        if name == key
    ]
