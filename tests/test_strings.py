import pytest

from py_simple_package.src.py_simple.easy_strings import (
    count_words,
    is_alphanumeric,
    is_palindrome,
    remove_extra_spaces,
    to_kebab_case,
    to_snake_case,
    to_title_case,
)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("  hello   world  ", "hello world"),
        ("hello world", "hello world"),
        ("", ""),
        ("   ", ""),
        ("hello\tworld\nagain", "hello world again"),
    ],
)
def test_remove_extra_spaces(text, expected):
    assert remove_extra_spaces(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello World", "hello_world"),
        ("hello-world", "hello_world"),
        ("hello_world", "hello_world"),
        ("helloWorld", "hello_world"),
        ("  Multiple   Spaces  ", "multiple_spaces"),
        ("Python 3 Basics", "python_3_basics"),
        ("", ""),
        ("HELLO WORLD", "hello_world"),
        ("XMLParser", "xmlparser"),
    ],
)
def test_to_snake_case(text, expected):
    assert to_snake_case(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello World", "hello-world"),
        ("hello_world", "hello-world"),
        ("hello-world", "hello-world"),
        ("helloWorld", "hello-world"),
        ("  Multiple   Spaces  ", "multiple-spaces"),
        ("Python 3 Basics", "python-3-basics"),
        ("", ""),
        ("HELLO WORLD", "hello-world"),
    ],
)
def test_to_kebab_case(text, expected):
    assert to_kebab_case(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("racecar", True),
        ("RaceCar", True),
        ("Never odd or even", True),
        ("A man, a plan, a canal: Panama!", True),
        ("hello", False),
        ("", True),
        ("a", True),
        ("12321", True),
        ("1a2a1", True),
    ],
)
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Something123", True),
        ("Python3", True),
        ("12345", True),
        ("abc", True),
        ("Hello World", False),
        ("hello!", False),
        ("user@email.com", False),
        ("", False),
        ("   ", False),
        ("hello\n", False),
    ],
)
def test_is_alphanumeric(text, expected):
    assert is_alphanumeric(text) is expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello world! How are you?", 5),
        ("hello world", 2),
        ("one", 1),
        ("", 0),
        ("   ", 0),
        ("hello-world_again", 3),
        ("camelCaseText", 3),
        ("hello 123 world", 3),
    ],
)
def test_count_words(text, expected):
    assert count_words(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello world", "Hello World"),
        ("HELLO WORLD", "Hello World"),
        ("hello_world", "Hello World"),
        ("hello-world", "Hello World"),
        ("helloWorldFromPython", "Hello World From Python"),
        ("don't stop", "Don't Stop"),
        ("y'all can't", "Y'all Can't"),
        ("'quoted text'", "'Quoted Text'"),
        ("Python 3 Basics", "Python 3 Basics"),
        ("  multiple   spaces  ", "Multiple Spaces"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_to_title_case(text, expected):
    assert to_title_case(text) == expected
