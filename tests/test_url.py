import pytest

from py_simple_package.src.py_simple import (
    get_path as public_get_path,
)
from py_simple_package.src.py_simple.easy_url import (
    EasyUrlError,
    add_query_param,
    get_domain,
    get_path,
    get_query_values,
    is_https,
    remove_query_param,
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
    assert (
        add_query_param(with_page, "page", "3") == "https://school.example/clubs?page=3"
    )


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


def test_remove_query_param():
    start = "https://school.example/clubs?page=2&sort=name"
    assert remove_query_param(start, "page") == "https://school.example/clubs?sort=name"
    assert remove_query_param(start, "sort") == "https://school.example/clubs?page=2"
    assert (
        remove_query_param("https://school.example/clubs?page=2", "page")
        == "https://school.example/clubs"
    )
    assert remove_query_param(start, "missing") == start


def test_remove_query_param_keeps_repeated_keys():
    start = "https://school.example/clubs?tag=python&page=2&tag=beginner"
    assert (
        remove_query_param(start, "page")
        == "https://school.example/clubs?tag=python&tag=beginner"
    )


def test_remove_query_param_missing_key_leaves_encoded_url_untouched():
    start = "https://school.example/search?q=art%20club"
    assert remove_query_param(start, "missing") == start


def test_remove_query_param_rejects_bad_key_and_url():
    with pytest.raises(EasyUrlError):
        remove_query_param("https://school.example/clubs?page=2", "")
    with pytest.raises(EasyUrlError):
        remove_query_param("https://school.example/clubs?page=2", 2)
    with pytest.raises(EasyUrlError):
        remove_query_param("school.example/clubs", "page")


def test_remove_query_param_public_imports():
    from py_simple import remove_query_param as public_remove
    from py_simple.easy_url import remove_query_param as module_remove

    assert public_remove is module_remove
    assert (
        public_remove("https://school.example/clubs?page=2", "page")
        == "https://school.example/clubs"
    )


@pytest.mark.parametrize(
    "url,key,expected",
    [
        (
            "https://school.example/?tag=a&other=x&tag=&tag=a&tag",
            "tag",
            ["a", "", "a", ""],
        ),
        (
            "https://school.example/?tag=art+club&tag=art%20club&tag=%2B",
            "tag",
            ["art club", "art club", "+"],
        ),
        ("https://school.example/?%74ag=one&tag=two&Tag=three", "tag", ["one", "two"]),
        (
            "https://school.example/?%E5%90%8D=%E9%9B%AA&%E5%90%8D=caf%C3%A9",
            "名",
            ["雪", "café"],
        ),
        ("https://school.example/?a+b=one&a%2Bb=two", "a b", ["one"]),
        ("https://school.example/?a+b=one&a%2Bb=two", "a+b", ["two"]),
        ("https://school.example/?%2574ag=encoded&tag=plain", "%74ag", ["encoded"]),
        ("https://school.example/?key=a%26b%3Dc&key=%2520", "key", ["a&b=c", "%20"]),
        ("https://school.example/?key=%FF&key=%ZZ", "key", ["�", "%ZZ"]),
        ("https://school.example/?key=first;key=second", "key", ["first;key=second"]),
        ("https://school.example/?key=query#key=fragment", "key", ["query"]),
        ("https://school.example/?=unnamed&%20=space", " ", ["space"]),
        ("https://school.example/?other=value", "key", []),
        ("https://school.example/?Tag=value", "tag", []),
        ("https://school.example/?", "tag", []),
        ("https://school.example/", "tag", []),
        ("https://school.example/#?tag=fragment", "tag", []),
    ],
)
def test_get_query_values(url, key, expected):
    assert get_query_values(url, key) == expected


@pytest.mark.parametrize("key", ["", None, 1, True, [], b"tag"])
def test_get_query_values_rejects_invalid_keys(key):
    with pytest.raises(EasyUrlError, match="key must be a non-empty string"):
        get_query_values("https://school.example/?tag=a", key)


@pytest.mark.parametrize(
    "url",
    [
        None,
        1,
        True,
        [],
        b"https://school.example",
        "",
        "  ",
        "school.example",
        "/clubs",
        "https:///clubs",
    ],
)
def test_get_query_values_rejects_invalid_urls(url):
    with pytest.raises(EasyUrlError, match="url must"):
        get_query_values(url, "tag")


def test_get_query_values_key_validation_precedes_url_validation():
    with pytest.raises(EasyUrlError, match="key must"):
        get_query_values(None, "")


def test_get_query_values_does_not_change_url_or_share_results():
    link = "HTTPS://School.example/clubs;params?tag=art%20club&tag=&tag#list"
    values = get_query_values(link, "tag")
    values.append("new")
    assert get_query_values(link, "tag") == ["art club", "", ""]
    assert link == "HTTPS://School.example/clubs;params?tag=art%20club&tag=&tag#list"


def test_get_query_values_public_imports():
    from py_simple import get_query_values as public_get
    from py_simple.easy_url import get_query_values as module_get

    assert public_get is module_get
    assert public_get(url="https://school.example/?tag=one&tag=two", key="tag") == [
        "one",
        "two",
    ]


@pytest.mark.parametrize("url", ["https://[", "https://[invalid]", "https://example.com／path", "https://user@", "https://:443"])
@pytest.mark.parametrize("helper", [get_domain, get_path, is_https, lambda url: add_query_param(url, "page", "2")])
def test_url_helpers_wrap_malformed_or_missing_hosts(url, helper):
    with pytest.raises(EasyUrlError):
        helper(url)


def test_get_domain_accepts_ipv6_and_user_information():
    assert get_domain("https://[::1]:443/path") == "::1"
    assert get_domain("https://user:password@school.example/path") == "school.example"
