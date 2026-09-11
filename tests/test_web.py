from unittest.mock import MagicMock, patch

import pytest
import requests

from py_simple_package.src.py_simple.easy_web import (
    SomethingWentWrongError,
    count_links,
    count_tags,
    get_all_headers,
    get_link_list,
    get_meta_description,
    get_page_content,
    get_page_title,
    get_tag_list,
    is_page_up,
    print_allowed_tags,
)


class TestEasyWeb:
    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_page_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "<html><body><h1>Hello World</h1></body></html>"
        mock_get.return_value = mock_response

        content = get_page_content("https://example.com")
        assert content is not None
        assert "Hello World" in content
        assert "<h1>" in content
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_page_content_not_ok(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_get.return_value = mock_response

        content = get_page_content("https://example.com/not-found")
        assert content is None
        mock_get.assert_called_once_with("https://example.com/not-found", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_page_content_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network Error")

        with pytest.raises(SomethingWentWrongError):
            get_page_content("https://invalid-url.com")
        mock_get.assert_called_once_with("https://invalid-url.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_is_page_up_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = is_page_up("https://example.com")
        assert result is True
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_is_page_up_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with pytest.raises(SomethingWentWrongError):
            is_page_up("https://example.com/404")
        mock_get.assert_called_once_with("https://example.com/404", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_is_page_up_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("Connection Failed")

        with pytest.raises(SomethingWentWrongError):
            is_page_up("https://offline-site.com")
        mock_get.assert_called_once_with("https://offline-site.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_is_page_up_non_200_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = is_page_up("https://example.com/created")
        assert result is False
        mock_get.assert_called_once_with("https://example.com/created", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_meta_description_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><head>"
            b'<meta name="description" content="A simple test page">'
            b'<meta name="keywords" content="python, pytest">'
            b'<meta name="viewport">'
            b"</head></html>"
        )
        mock_get.return_value = mock_response

        result = get_meta_description("https://example.com")
        assert result == ["A simple test page", "python, pytest"]
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_meta_description_empty(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><head><title>No meta</title></head></html>"
        mock_get.return_value = mock_response

        result = get_meta_description("https://example.com")
        assert result == []
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_meta_description_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Request Timed Out")

        with pytest.raises(SomethingWentWrongError):
            get_meta_description("https://invalid-url.com")
        mock_get.assert_called_once_with("https://invalid-url.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_all_headers_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><body>"
            b"<header>\n  Welcome to Py_simple  \n</header>"
            b"<header>Documentation Header</header>"
            b"</body></html>"
        )
        mock_get.return_value = mock_response

        result = get_all_headers("https://example.com")
        assert result == ["Welcome to Py_simple", "Documentation Header"]
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_all_headers_empty(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><div>No header tag</div></body></html>"
        mock_get.return_value = mock_response

        result = get_all_headers("https://example.com")
        assert result == []
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_all_headers_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Connection Refused")

        with pytest.raises(SomethingWentWrongError):
            get_all_headers("https://offline-site.com")
        mock_get.assert_called_once_with("https://offline-site.com", timeout=10)


class TestGetPageTitle:
    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_page_title_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><head><title>Example Title</title></head></html>"
        )
        mock_get.return_value = mock_response

        result = get_page_title("https://example.com")
        assert result == "Example Title"
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_page_title_no_title_tag(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><p>No title here</p></body></html>"
        mock_get.return_value = mock_response

        with pytest.raises(SomethingWentWrongError):
            get_page_title("https://example.com")
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_page_title_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network Error")

        with pytest.raises(SomethingWentWrongError):
            get_page_title("https://invalid-url.com")
        mock_get.assert_called_once_with("https://invalid-url.com", timeout=10)


class TestCountTags:
    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_count_tags_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><body>"
            b'<a href="/one">One</a>'
            b'<a href="/two">Two</a>'
            b'<a href="/three">Three</a>'
            b'<img src="logo.png">'
            b"</body></html>"
        )
        mock_get.return_value = mock_response

        result = count_tags("https://example.com", "a")
        assert result == 3
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_count_tags_img(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b'<html><body><img src="logo.png"><img src="banner.png"></body></html>'
        )
        mock_get.return_value = mock_response

        result = count_tags("https://example.com", "img")
        assert result == 2
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_count_tags_none_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><p>No links here</p></body></html>"
        mock_get.return_value = mock_response

        result = count_tags("https://example.com", "a")
        assert result == 0
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    def test_count_tags_unsupported_tag(self):
        with pytest.raises(ValueError, match="Unsupported tag"):
            count_tags("https://example.com", "div")

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_count_tags_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network Error")

        with pytest.raises(SomethingWentWrongError):
            count_tags("https://invalid-url.com", "a")
        mock_get.assert_called_once_with("https://invalid-url.com", timeout=10)


class TestCountLinks:
    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_count_links_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><body>"
            b'<a href="/one">One</a>'
            b'<a href="/two">Two</a>'
            b'<a href="/three">Three</a>'
            b"</body></html>"
        )
        mock_get.return_value = mock_response

        result = count_links("https://example.com")
        assert result == 3
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_count_links_none_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><p>No links here</p></body></html>"
        mock_get.return_value = mock_response

        result = count_links("https://example.com")
        assert result == 0
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_count_links_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network Error")

        with pytest.raises(SomethingWentWrongError):
            count_links("https://invalid-url.com")
        mock_get.assert_called_once_with("https://invalid-url.com", timeout=10)


class TestGetTagList:
    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_tag_list_hrefs(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><body>"
            b'<a href="/one">One</a>'
            b'<a href="/two">Two</a>'
            b'<img src="logo.png">'
            b"</body></html>"
        )
        mock_get.return_value = mock_response

        result = get_tag_list("https://example.com", "a")
        assert result == ["/one", "/two"]
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_tag_list_srcs(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><body>"
            b'<img src="logo.png">'
            b'<img src="banner.png">'
            b'<a href="/one">One</a>'
            b"</body></html>"
        )
        mock_get.return_value = mock_response

        result = get_tag_list("https://example.com", "img")
        assert result == ["logo.png", "banner.png"]
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_tag_list_none_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><p>No images</p></body></html>"
        mock_get.return_value = mock_response

        result = get_tag_list("https://example.com", "img")
        assert result == []
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    def test_get_tag_list_unsupported_tag(self):
        with pytest.raises(ValueError, match="Unsupported tag"):
            get_tag_list("https://example.com", "script")

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_tag_list_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Timeout")

        with pytest.raises(SomethingWentWrongError):
            get_tag_list("https://invalid-url.com", "a")
        mock_get.assert_called_once_with("https://invalid-url.com", timeout=10)


class TestGetLinkList:
    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_link_list_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b'<html><body><a href="/one">One</a><a href="/two">Two</a></body></html>'
        )
        mock_get.return_value = mock_response

        result = get_link_list("https://example.com")
        assert result == ["/one", "/two"]
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_link_list_none_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><p>No links here</p></body></html>"
        mock_get.return_value = mock_response

        result = get_link_list("https://example.com")
        assert result == []
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_link_list_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Timeout")

        with pytest.raises(SomethingWentWrongError):
            get_link_list("https://invalid-url.com")
        mock_get.assert_called_once_with("https://invalid-url.com", timeout=10)


class TestPrintAllowedTags:
    def test_print_allowed_tags(self, capsys):
        result = print_allowed_tags()
        captured = capsys.readouterr()
        assert "'a': 'href'" in captured.out
        assert "'img': 'src'" in captured.out
        assert result is None
