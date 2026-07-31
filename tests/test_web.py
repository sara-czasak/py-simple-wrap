from unittest.mock import MagicMock, patch
import pytest
import requests

from py_simple_package.src.py_simple.easy_web import (
    get_page_content, is_page_up, count_tags, get_tag_list,
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

        content = get_page_content("https://invalid-url.com")
        assert content is None
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

        result = is_page_up("https://example.com/404")
        assert result is False
        mock_get.assert_called_once_with("https://example.com/404", timeout=10)

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_is_page_up_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("Connection Failed")

        result = is_page_up("https://offline-site.com")
        assert result is False
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
    def test_count_tags(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><a href='/one'></a><a href='/two'></a><img src='a.png' /></body></html>"
        mock_get.return_value = mock_response

        assert count_tags("https://example.com", "a") == 2
        assert count_tags("https://example.com", "img") == 1
        assert count_tags("https://example.com", "script") is None

    @patch("py_simple_package.src.py_simple.easy_web.requests.get")
    def test_get_tag_list(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><a href='/one'></a><a href='/two'></a><img src='a.png' /><img src='' /></body></html>"
        mock_get.return_value = mock_response

        assert get_tag_list("https://example.com", "a") == ["/one", "/two"]
        assert get_tag_list("https://example.com", "img") == ["a.png"]
        assert get_tag_list("https://example.com", "script") is None
