import pytest

from py_simple_package.src.py_simple import (
    extract_hex_colors as public_extract_hex_colors,
)
from py_simple_package.src.py_simple.easy_regex import (
    extract_emails,
    extract_hex_colors,
    extract_number_sequences,
    extract_numbers,
    extract_urls,
    extract_hashtags,
    extract_mentions,
    extract_ipv4_addresses,
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

# email test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("this is my address, ginny@gmail.com", ["ginny@gmail.com"]),
        ("this has no address right?",[]),
        ("what about more than one with hello@example.com and support@test.org",['hello@example.com','support@test.org']),
        ("a curveball to try test%123@domain.com",['test%123@domain.com']),
        ("will.this.work@test.edu",['will.this.work@test.edu'])
    ]

)

def test_is_email_extracted(input_text,expected):
    assert extract_emails(input_text) == expected

# url test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("visit https://www.example.com or www.test.org today", ['https://www.example.com','www.test.org']),
        ("visit test.edu today", []),
        ("yourself http://127.0.0.1", []),
        ("explore www.test14-maps.com", ['www.test14-maps.com']),
        ("for longer url: http://test.org/example", ['http://test.org/example'])
    ]
)

def test_is_url_extracted(input_text, expected):
    assert extract_urls(input_text) == expected

# number sequence test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Server 192.168.1.1 logged in at 14:32 on 04-08-2026", ['192.168.1.1', '14:32', '04-08-2026']),
        ("Python 3.14.6", ['3.14.6']),
        ("call me at 929_759_0263", ['929_759_0263']),

    ]
)

def test_is_number_sequence_extracted(input_text, expected):
    assert extract_number_sequences(input_text) == expected

# number test
@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("I have 3 cats and 12 fish", ['3','12']),
        ("this is one and this 1 too", ['1']),

    ]
)

def test_is_number_extracted(input_text,expected):
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