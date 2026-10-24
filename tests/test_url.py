import pytest

from py_simple_package.src.py_simple import (
    get_path as public_get_path,
)
from py_simple_package.src.py_simple.easy_url import (
    EasyUrlError,
    add_query_param,
    get_domain,
    get_path,
    is_https,
)


def test_get_domain():
    assert get_domain("https://school.example/clubs") == "school.example"


def test_is_https():
    assert is_https("https://school.example") is True
    assert is_https("http://school.example") is False


def test_add_query_param_sets_and_replaces():
    start = "https://school.example/clubs"
    with_page = add_query_param(start, "page", "2")
    assert with_page == "https://school.example/clubs?page=2"
    assert add_query_param(with_page, "page", "3") == "https://school.example/clubs?page=3"


def test_get_path():
    assert get_path("https://school.example/clubs/art") == "/clubs/art"
    assert get_path("https://school.example/") == "/"
    assert get_path("https://school.example") == "/"
    assert get_path("https://school.example/search?q=test") == "/search"


def test_get_path_public_export():
    assert public_get_path is get_path


def test_rejects_incomplete_url():
    with pytest.raises(EasyUrlError):
        get_domain("school.example")
    with pytest.raises(EasyUrlError):
        get_path("school.example")
    with pytest.raises(EasyUrlError):
        add_query_param("https://school.example", "", "2")


@pytest.mark.parametrize(
    "query,key,value,expected",
    [
        ("tag=python&tag=beginner", "page", "2", "tag=python&tag=beginner&page=2"),
        ("tag=python&page=1&tag=beginner&page=3", "page", "2", "tag=python&page=2&tag=beginner"),
        ("tag=&tag=python&empty=", "page", "2", "tag=&tag=python&empty=&page=2"),
        ("tag=c%2B%2B&tag=a%26b", "q", "hello world", "tag=c%2B%2B&tag=a%26b&q=hello+world"),
    ],
)
def test_add_query_param_preserves_other_repeated_parameters(query, key, value, expected):
    url = f"https://school.example/clubs?{query}#results"
    assert add_query_param(url, key, value) == f"https://school.example/clubs?{expected}#results"
