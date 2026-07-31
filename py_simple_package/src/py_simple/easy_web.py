"""
easy_web is built to simplify getting information from the web.
"""
import requests
from bs4 import BeautifulSoup

SUPPORTED_TAG_ATTRIBUTES = {
    "a": "href",
    "img": "src",
}


def print_allowed_tags() -> None:
    """Print the supported HTML tags and attributes."""
    print("Supported tags: " + ", ".join(SUPPORTED_TAG_ATTRIBUTES.keys()))
    for tag, attr in SUPPORTED_TAG_ATTRIBUTES.items():
        print(f"  <{tag}> -> {attr}")


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
            return BeautifulSoup(response.text, 'html.parser').prettify()
        else:
            return None
    except Exception as e:
        print(f"Something went wrong with {url}\nERROR: {e}")
        return None


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
        print(f"Something went wrong with {url}\nERROR: {e}")
        return False


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
        page = BeautifulSoup(response.content, 'html.parser')
        title = page.title.string
        return title
    except Exception as e:
        print(f"Something went wrong with {url}\nERROR: {e}")
        return None


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
        soup = BeautifulSoup(response.content, 'html.parser')
        link_count = 0
        if response is not None:
            for link in soup.find_all('a'):
                link_count += 1
            return link_count
    except Exception as e:
        print(f"Something went wrong with {url}\nERROR: {e}")
        return None


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
        soup = BeautifulSoup(response.content, 'html.parser')
        link_list = []
        if response is not None:
            for link in soup.find_all('a'):
                link_list.append(link.get('href'))
            return link_list
    except Exception as e:
        print(f"Something went wrong with {url}\nERROR: {e}")
        return None


def count_tags(url: str, tag: str) -> int | None:
    """Count matching tags on the page."""
    if tag not in SUPPORTED_TAG_ATTRIBUTES:
        print(f"Unsupported tag: {tag}. Call print_allowed_tags() first.")
        return None

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        return len(soup.find_all(tag))
    except Exception as e:
        print(f"Something went wrong with {url}\nERROR: {e}")
        return None


def get_tag_list(url: str, tag: str) -> list[str] | None:
    """Get values for the configured attribute of a supported tag."""
    if tag not in SUPPORTED_TAG_ATTRIBUTES:
        print(f"Unsupported tag: {tag}. Call print_allowed_tags() first.")
        return None

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        value_attr = SUPPORTED_TAG_ATTRIBUTES[tag]
        values: list[str] = []
        for item in soup.find_all(tag):
            value = item.get(value_attr)
            if value:
                values.append(value)
        return values
    except Exception as e:
        print(f"Something went wrong with {url}\nERROR: {e}")
        return None
