import pytest

from py_simple_package.src.py_simple import (
    extract_hashtag_names as public_extract_hashtag_names,
    extract_hex_colors as public_extract_hex_colors,
    extract_phone_numbers as public_extract_phone_numbers,
)
from py_simple_package.src.py_simple.easy_regex import (
    extract_emails,
    extract_hashtag_names,
    extract_hashtags,
    extract_hex_colors,
    extract_ipv4_addresses,
    extract_mentions,
    extract_number_sequences,
    extract_numbers,
    extract_phone_numbers,
    extract_urls,
    clean_extra_whitespace,
)


# email test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("this is my address, ginny@gmail.com", ["ginny@gmail.com"]),
        ("this has no address right?", []),
        (
            "what about more than one with hello@example.com and support@test.org",
            ["hello@example.com", "support@test.org"],
        ),
        ("a curveball to try test%123@domain.com", ["test%123@domain.com"]),
        ("will.this.work@test.edu", ["will.this.work@test.edu"]),
    ],
)
def test_is_email_extracted(input_text, expected):
    assert extract_emails(input_text) == expected


# url test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        (
            "visit https://www.example.com or www.test.org today",
            ["https://www.example.com", "www.test.org"],
        ),
        ("visit test.edu today", []),
        ("yourself http://127.0.0.1", []),
        ("explore www.test14-maps.com", ["www.test14-maps.com"]),
        ("for longer url: http://test.org/example", ["http://test.org/example"]),
    ],
)
def test_is_url_extracted(input_text, expected):
    assert extract_urls(input_text) == expected


# number sequence test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        (
            "Server 192.168.1.1 logged in at 14:32 on 04-08-2026",
            ["192.168.1.1", "14:32", "04-08-2026"],
        ),
        ("Python 3.14.6", ["3.14.6"]),
        ("call me at 929_759_0263", ["929_759_0263"]),
    ],
)
def test_is_number_sequence_extracted(input_text, expected):
    assert extract_number_sequences(input_text) == expected


# number test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("I have 3 cats and 12 fish", ["3", "12"]),
        ("this is one and this 1 too", ["1"]),
    ],
)
def test_is_number_extracted(input_text, expected):
    assert extract_numbers(input_text) == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Use #fff on #1a2b3c", ["#fff", "#1a2b3c"]),
        ("Alpha colors: #abcd and #12345678", ["#abcd", "#12345678"]),
        ("Case is preserved: #Aa00Ff", ["#Aa00Ff"]),
        ("Ignore #12, #12345, #ggg, and abc#fff", []),
        ("No colors here", []),
    ],
)
def test_hex_colors_are_extracted(input_text, expected):
    assert extract_hex_colors(input_text) == expected


def test_extract_hex_colors_is_available_from_public_api():
    assert public_extract_hex_colors is extract_hex_colors


# hashtag test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Loving #Python and #OpenSource!", ["#Python", "#OpenSource"]),
        ("No tags here", []),
        ("Multiple on one line #code #test #123", ["#code", "#test", "#123"]),
        ("Ignore just a # symbol", []),
        ("Handles #under_scores but stops at #hash-tags", ["#under_scores", "#hash"]),
        ("Case preserved #UPPERCASE", ["#UPPERCASE"]),
    ],
)
def test_hashtags_are_extracted(input_text, expected):
    assert extract_hashtags(input_text) == expected


# mention test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Hey @alice, please review @dev_team's code", ["@alice", "@dev_team"]),
        ("No mentions here", []),
        ("Multiple @user1 @user2 @user3", ["@user1", "@user2", "@user3"]),
        ("Ignores just an @ symbol", []),
        ("Handles @under_scores but stops at @hyphen-users", ["@under_scores", "@hyphen"]),
    ],
)
def test_mentions_are_extracted(input_text, expected):
    assert extract_mentions(input_text) == expected


# IPv4 test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Server 192.168.1.1 connected to 10.0.0.5", ["192.168.1.1", "10.0.0.5"]),
        ("Localhost is 127.0.0.1", ["127.0.0.1"]),
        ("No IPs in this text", []),
    ],
)
def test_ipv4_addresses_are_extracted(input_text, expected):
    assert extract_ipv4_addresses(input_text) == expected


# whitespace test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Hello    world\n\nthis is Python", "Hello world this is Python"),
        ("   leading and trailing   ", "leading and trailing"),
        ("NoExtraSpaces", "NoExtraSpaces"),
        ("Tabs\t\tand\tspaces", "Tabs and spaces"),
    ],
)
def test_extra_whitespace_is_cleaned(input_text, expected):
    assert clean_extra_whitespace(input_text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello #Python and #coding", ["Python", "coding"]),
        ("#hello_world #123 #_", ["hello_world", "123", "_"]),
        ("#Python #Python #python", ["Python", "Python", "python"]),
        ("", []),
        ("No hashtags here", []),
        ("# ## ### #!", []),
        ("word#tag _#tag 1#tag ##tag ###tag", []),
        ("(#one), #two! #three-four", ["one", "two", "three"]),
        ("#one\n#two\t#three", ["one", "two", "three"]),
        ("#caf\u00e9 #\u6771\u4eac", ["caf\u00e9", "\u6771\u4eac"]),
        ("\u00e9#tag", []),
        ("#cafe\u0301", ["cafe"]),
        ("#one#two", ["one"]),
        ("#\U0001f600", []),
    ],
)
def test_extract_hashtag_names(text, expected):
    assert extract_hashtag_names(text) == expected


def test_public_export():
    assert public_extract_hashtag_names is extract_hashtag_names


def test_existing_regex_hashtags_keep_hash_symbols():
    assert extract_hashtags("#Python #coding") == ["#Python", "#coding"]


# phone number test
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
            "In parentheses: ((555) 123-4567) or call ((555) 987-6543).",
            ["(555) 123-4567", "(555) 987-6543"],
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
        (
            "Malformed partials: (555 123-4567, 555-123-4567-999, 999-555-123-4567.",
            [],
        ),
        (
            "Malformed formats: 555-123-45678, (555) 123-4567-89, 555) 123-4567, 555.123.4567.890.",
            [],
        ),
    ],
)
def test_is_phone_number_extracted(input_text, expected):
    assert extract_phone_numbers(input_text) == expected


def test_extract_phone_numbers_is_available_from_public_api():
    assert public_extract_phone_numbers is extract_phone_numbers


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Contact user@mail.example.com.", ["user@mail.example.com"]),
        ("Send to person+tag@dept.example.co.uk or user2@example.org!", ["person+tag@dept.example.co.uk", "user2@example.org"]),
        ("<first.last@eu-west.team2.example.org>", ["first.last@eu-west.team2.example.org"]),
    ],
)
def test_extract_emails_preserves_complete_subdomains(text, expected):
    assert extract_emails(text) == expected
