import pytest

from py_simple_package.src.py_simple.easy_validator import (
    is_valid_email,
    is_valid_username,
    is_valid_zipcode,
    is_valid_url,
    is_password_secure,
    is_valid_creditcard,
    is_valid_phone_number,
    is_valid_json,
    is_valid_ipv4)

class TestEasyValidator:

    @pytest.mark.parametrize(
    "email,expected",
    [
        ("mymail@gmail.com", True),
        ("email.com", False),
        ("", False),
        ("user@test.co", True),
        ("@gmail.com", False),
    ],
    )

    def test_email_validation(self, email, expected):
        assert is_valid_email(email) is expected

    @pytest.mark.parametrize(
        "username,expected",
        [
            ("user_name", True),
            ("user.name", False),
            ("user123", True),
            ("", False),
            ("user-name", False),
        ],
    )

    def test_username_validation(self, username, expected):
        assert is_valid_username(username) is expected

    @pytest.mark.parametrize(
            "zipcode,expected",
            [
                (12345, True),
                (1248721, False),
                (1234, False),
                (99999, True),
                ("01234", True),
            ],
        )

    def test_zipcode_validation(self, zipcode, expected):
        assert is_valid_zipcode(zipcode) is expected

    @pytest.mark.parametrize(
        "url, expected",
        [
            ("www.google.com", True),
            ("something.com", False),
            ("http://google.com", True),
            ("https://google.com", True),
            ("", False),
        ],
    )

    def test_url_validation(self, url, expected):
        assert is_valid_url(url) is expected

    @pytest.mark.parametrize(
        "password, expected",
        [
            ("1andkrf!AG5", True),
            ("111mskagowd", False),
            ("Ab1!cd", False),
            ("abcd12!ef", False),
            ("Abcdef!g1", False),
            ("Abcd12!!Ef", False),
            ("AAbcdef1!2", False),
            ("Abbcdef1!2", False),
            ("Abcdef11!2", False),
            (" 1andkrf!AG5", True),
            ("Abcde12!", False),
            ("", False),
        ],
    )

    def test_password_validation(self, password, expected):
        assert is_password_secure(password) is expected

    # Valid test numbers provided by Stripe
    # https://docs.stripe.com/testing?testing-method=card-numbers#cards
    @pytest.mark.parametrize(
        "card_num, expected",
        [
            ("4242-4242-4242-4242", True), # visa
            ("5555-5555-5555-4444", True), # mastercard
            ("3782 8224 6310 005", True),  # american_express
            ("6011 1111 1111 1117", True), # discover
            ("4242-4242-4242-0242", False), # visa (one digit changed)
            ("5555-5555-6555-4444", False), # mastercard (one digit changed)
            ("3782 8224 6310 004", False),  # amex (one digit changed)
            ("6011 1111 1011 1117", False), # discover (one digit changed)
            ("012345678901", False),        # too short
            ("01234567890123456789", False), # too long
            ("ab12 cd34 ef56 gh78", False), # non-numeric
            ("5200_8282_8282_8210", False), # invalid separator
        ]
    )

    def test_creditcard_validation(self, card_num, expected):
        assert is_valid_creditcard(card_num) is expected

    @pytest.mark.parametrize(
        "phone_number, expected",
        [
            ("1234567890", True),
            ("123-456-7890", True),
            ("(123) 456-7890", True),
            ("123.456.7890", True),
            ("123 456 7890", True),
            ("+1 123-456-7890", True),
            ("+11234567890", True),
            ("12345", False),
            ("123-456-78901", False),
            ("abc-456-7890", False),
            ("", False),
            ("123-45-6789", False),
            ("+1234567890", False),
        ],
    )

    def test_phone_number_validation(self, phone_number, expected):
        assert is_valid_phone_number(phone_number) is expected
    @pytest.mark.parametrize(
        "json_string, expected",
        [
            ('{"key": "value"}', True),
            ('[1, 2, 3]', True),
            ('"just a string"', True),
            ('123', True),
            ('{key: "value"}', False),
            ('{"key": "value",}', False),
            ('', False),
            ("{'key': 'value'}", False),
        ],
    )

    def test_json_validation(self, json_string, expected):
        assert is_valid_json(json_string) is expected

    @pytest.mark.parametrize(
        "ip, expected",
        [
            ("192.168.1.1", True),
            ("0.0.0.0", True),
            ("255.255.255.255", True),
            ("256.1.1.1", False),
            ("192.168.1", False),
            ("192.168.1.1.1", False),
            ("192.168.01.1", False),
            ("", False),
            ("abc.def.ghi.jkl", False),
        ],
    )

    def test_ipv4_validation(self, ip, expected):
        assert is_valid_ipv4(ip) is expected
