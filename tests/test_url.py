import pytest

from py_simple_package.src.py_simple.easy_url import (
    EasyUrlError,
    add_query_param,
    get_domain,
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


def test_rejects_incomplete_url():
    with pytest.raises(EasyUrlError):
        get_domain("school.example")
    with pytest.raises(EasyUrlError):
        add_query_param("https://school.example", "", "2")
