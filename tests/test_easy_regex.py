import pytest

from py_simple import extract_phone_numbers as public_extract_phone_numbers
from py_simple.easy_regex import extract_phone_numbers


@pytest.mark.parametrize(
    "input_text, expected",
    [
        (
            "Call us at 555-123-4567 or (555) 987-6543 today.",
            ["555-123-4567", "(555) 987-6543"],
        ),
        (
            "Contact +1-555-234-5678 or +1 (555) 345-6789 for help.",
            ["+1-555-234-5678", "+1 (555) 345-6789"],
        ),
        (
            "Dot format: 555.456.7890, space format: 555 456 7890.",
            ["555.456.7890", "555 456 7890"],
        ),
        (
            "Plain ten digits: 5551234567.",
            ["5551234567"],
        ),
        (
            "In parentheses: (555-123-4567) or call ((555) 123-4567).",
            ["555-123-4567", "(555) 123-4567"],
        ),
        (
            "Country code without symbol: 1-555-123-4567 and 1 (555) 123-4567.",
            ["1-555-123-4567", "1 (555) 123-4567"],
        ),
        (
            "No phone numbers in this sentence.",
            [],
        ),
        (
            "",
            [],
        ),
        (
            "Invalid: 12345, 123-45-6789, 123456789012, abc555-123-4567, 555-123-4567xyz.",
            [],
        ),
    ],
)
def test_extract_phone_numbers(input_text, expected):
    assert extract_phone_numbers(input_text) == expected


def test_extract_phone_numbers_exported():
    assert public_extract_phone_numbers is extract_phone_numbers
