"""
easy_web is built to simplify getting information from the web.
"""

import requests
from bs4 import BeautifulSoup

_TAGS = {"a": "href", "img": "src"}


class SomethingWentWrongError(Exception):
    """
    Raised when a py_simple web function fails to complete its request.

    This covers network failures, invalid URLs, timeouts, and any other
    error that prevents a function from returning a real result. Functions
    that can succeed with "nothing found" (like an empty list) return
    None in that case instead of raising - this error is only for when
    something actually went wrong.

    Args:
        message (str): Description of what went wrong, usually including
            the original error message.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_page_content(url: str) -> str | None:
    """
    Returns content of the website or None if an error occurs.

    Args:
        url (str): Website to be parsed.

    Returns:
        str | None: The page's prettified HTML content, or None if the
            request failed.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_page_content

            content = get_page_content("https://google.com")
            ```

        === "The Traditional Way"
            ```python
            import requests
            from bs4 import BeautifulSoup

            response = requests.get("https://google.com")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.prettify()
            ```
    """
    try:
        response = requests.get(url, timeout=10)
        if response.ok:
            return BeautifulSoup(response.text, "html.parser").prettify()
        else:
            return None
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def is_page_up(url: str) -> bool:
    """
    Returns true if HTTP status code is 200 else returns false.

    Args:
        url (str): Website to check.

    Returns:
        bool: True if the site responded with status 200, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_page_up

            if is_page_up("https://github.com"):
                print("The site is active!")
            ```

        === "The Traditional Way"
            ```python
            import requests

            try:
                response = requests.get("https://github.com")
                if response.status_code == 200:
                    print("The site is active!")
            except Exception:
                print("The site is down or address is invalid.")
            ```
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return bool(response.status_code == 200)
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def get_page_title(url: str) -> str | None:
    """
    Returns web page title or None if an error occurs.

    Args:
        url (str): Website to check.

    Returns:
        str | None: Page title or None if an error occurs.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_page_title

            print(get_page_title("https://github.com")) #-> "GitHub ·
            Change is constant. GitHub keeps you ahead. · GitHub
            ```

        === "The Traditional Way"
            ```python
            import requests

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                page = BeautifulSoup(response.content, 'html.parser')
                title = page.title.string
                return title
            except Exception as e:
                print("The site is down or address is invalid.")
            ```
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        page = BeautifulSoup(response.content, "html.parser")
        title = page.title.string
        return title
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def count_links(url: str) -> int | None:
    """
    Returns number of links in the website or None if an error occurs.

    Args:
        url (str): Website to count links from.

    Returns:
        int | None: number of links or None if an error occurs.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_links

            print(count_links("https://github.com")) #-> 144
            ```
        === "The Traditional Way"
            ```python
            import requests
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                link_count = 0
                if response is not None:
                    for link in soup.find_all('a'):
                        link_count += 1
                    return link_count
            except Exception as e:
                print(f"Something went wrong with {url}")
                return None
            ```
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        link_count = 0
        if response is not None:
            for link in soup.find_all("a"):
                link_count += 1
            return link_count
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def get_link_list(url: str) -> list[str] | None:
    """
    Returns a list of links on website or None if an error occurs.

    Args:
        url (str): Website to get links from.

    Returns:
        list[str] | None: list of links or None if the request fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_link_list
            print(get_link_list("https://github.com")) #-> [...]
            ```
        === "The Traditional Way"
            ```python
            import requests
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                link_list = []
                if response is not None:
                    for link in soup.find_all('a'):
                        link_list.append(link.get('href'))
                    return link_list
            except Exception as e:
                print(f"Something went wrong with {url}")
                return None
            ```
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        link_list = []
        if response is not None:
            for link in soup.find_all("a"):
                link_list.append(link.get("href"))
            return link_list
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def count_tags(url: str, tag: str) -> int | None:
    """
    Returns the number of tags of a given type on a page, or None if an
    error occurs.

    Raises ValueError if the tag is not in the allowed tags list
    (see print_allowed_tags).

    Args:
        url (str): Website to count tags from.
        tag (str): HTML tag to count (e.g. 'a', 'img').

    Returns:
        int | None: number of matching tags, or None if an error occurs.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_tags

            print(count_tags("https://github.com", "img")) #-> 12
            ```
        === "The Traditional Way"
            ```python
            import requests
            from bs4 import BeautifulSoup

            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            tag_count = len(soup.find_all('img'))
            ```
    """
    if tag not in _TAGS:
        raise ValueError(f"Unsupported tag: '{tag}'. Allowed tags: {', '.join(_TAGS)}")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        if response is not None:
            return len(soup.find_all(tag))
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def get_tag_list(url: str, tag: str) -> list[str] | None:
    """
    Returns a list of the useful info from each matching tag on the page,
    or None if an error occurs.

    For `a` tags this is the link (`href`); for `img` tags it is the
    image source (`src`). See print_allowed_tags for supported tags.

    Raises ValueError if the tag is not in the allowed tags list.

    Args:
        url (str): Website to get tags from.
        tag (str): HTML tag to list (e.g. 'a', 'img').

    Returns:
        list[str] | None: list of attribute values from matching tags,
            or None if an error occurs.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_tag_list

            print(get_tag_list("https://github.com", "img")) #-> ["logo.png", ...]
            ```
        === "The Traditional Way"
            ```python
            import requests
            from bs4 import BeautifulSoup

            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            tag_list = []
            for tag in soup.find_all('img'):
                tag_list.append(tag.get('src'))
            ```
    """
    if tag not in _TAGS:
        raise ValueError(f"Unsupported tag: '{tag}'. Allowed tags: {', '.join(_TAGS)}")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        attribute = _TAGS[tag]
        tag_list = []
        if response is not None:
            for element in soup.find_all(tag):
                tag_list.append(element.get(attribute))
            return tag_list
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def print_allowed_tags() -> None:
    """
    Prints the dictionary of tags supported by count_tags and get_tag_list.

    Each entry maps a tag name to the attribute that get_tag_list returns
    for that tag.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import print_allowed_tags

            print_allowed_tags()
            # {'a': 'href', 'img': 'src'}
            ```
    """
    print(_TAGS)


def get_meta_description(url: str) -> list[str] | None:
    """
    Returns a list of meta tag contents found on the page, or None if
    the page has no meta tags.

    Raises SomethingWentWrongError if the request fails (invalid URL,
    network issue, timeout, etc).

    Args:
        url (str): Website to get meta descriptions from.

    Returns:
        list[str] | None: list of meta tag contents, or None if the
            page has no meta tags with content.

    Example:
        === "The Py_simple Way"
            ```python
                from py_simple import get_meta_description

                print(get_meta_description("https://github.com")) #-> [...]
            ```
        === "The Traditional Way"
            ```python
            import requests
            from bs4 import BeautifulSoup

            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_description_list = []
            for meta in soup.find_all('meta'):
                if meta.get('content') is not None:
                    meta_description_list.append(meta.get('content'))
            ```
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        meta_description_list = []
        if response is not None:
            for meta in soup.find_all("meta"):
                if meta.get("content") is not None:
                    meta_description_list.append(meta.get("content"))
            return meta_description_list
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None


def get_all_headers(url: str) -> list[str] | None:
    """
    Returns a list of cleaned-up text from every <header> tag on the
    page, or None if the page has no header tags.

    Raises SomethingWentWrongError if the request fails (invalid URL,
    network issue, timeout, etc).

    Args:
        url (str): Website to get headers from.

    Returns:
        list[str] | None: list of header text with whitespace and
            newlines stripped, or None if the page has no headers.

    Example:
        === "The Py_simple Way"
            ```python
                from py_simple import get_all_headers

                print(get_all_headers("https://github.com")) #-> [...]
            ```
        === "The Traditional Way"
            ```python
                import requests
                from bs4 import BeautifulSoup

                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                header_list = []
                for header in soup.find_all('header'):
                    header_list.append(header.text.strip().replace("\\n", ""))
            ```
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        header_list = []
        clean_headers = []
        if response is not None:
            for header in soup.find_all("header"):
                header_list.append(header.text)
            for header in header_list:
                clean_headers.append(header.strip().replace("\n", ""))
            return clean_headers
    except Exception as e:
        raise SomethingWentWrongError(f"\n\n\nERROR: {e}") from None
