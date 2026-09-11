"""Tests for easy_date_formatter module."""

from unittest.mock import patch
import re
import pytest
import datetime as dt
from py_simple_package.src.py_simple.easy_date_formatter import *


from py_simple_package.src.py_simple.easy_date_formatter import (
    get_pretty_date,
    get_past_pretty_date,
    get_future_pretty_date,
    dd_mm_yyyy,
    past_dd_mm_yyyy,
    future_dd_mm_yyyy,
    mm_dd_yyyy,
    past_mm_dd_yyyy,
    future_mm_dd_yyyy,
    slash_dd_mm_yyyy,
    past_slash_dd_mm_yyyy,
    future_slash_dd_mm_yyyy,
    slash_mm_dd_yyyy,
    past_slash_mm_dd_yyyy,
    future_slash_mm_dd_yyyy,
    list_available_formats,
    _FORMATS,
    _format_date,
    _get_past_date,
    _get_future_date,
)


class TestPrettyDates:
    """Tests for human-friendly pretty date formats."""

    def test_get_pretty_date_format(self):
        """Should return 'Weekday, Month Day, Year' format."""
        result = get_pretty_date()
        assert re.match(r"[A-Z][a-z]+, [A-Z][a-z]+ \d{1,2}, \d{4}", result)

    def test_get_past_pretty_date_returns_string(self):
        """Should return a string for valid input."""
        result = get_past_pretty_date(7)
        assert isinstance(result, str)
        assert re.match(r"[A-Z][a-z]+, [A-Z][a-z]+ \d{1,2}, \d{4}", result)

    def test_get_past_pretty_date_zero_days(self):
        """Zero days ago should equal today."""
        assert get_past_pretty_date(0) == get_pretty_date()

    def test_get_past_pretty_date_one_day(self):
        """Yesterday should be one day before today."""
        past = get_past_pretty_date(1)
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        expected = yesterday.strftime("%A, %B %d, %Y")
        assert past == expected

    def test_get_future_pretty_date(self):
        """Future pretty date should exist and differ from today."""
        result = get_future_pretty_date(7)
        assert isinstance(result, str)
        assert result != get_pretty_date()

    def test_get_future_pretty_date_zero_days(self):
        """Zero days from now should equal today."""
        assert get_future_pretty_date(0) == get_pretty_date()

    def test_get_future_pretty_date_one_day(self):
        """Tomorrow should be one day after today."""
        future = get_future_pretty_date(1)
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        expected = tomorrow.strftime("%A, %B %d, %Y")
        assert future == expected


class TestHyphenatedDates:
    """Tests for DD-MM-YYYY and MM-DD-YYYY formats."""

    def test_dd_mm_yyyy_format(self):
        """Should return DD-MM-YYYY pattern."""
        result = dd_mm_yyyy()
        assert re.match(r"\d{2}-\d{2}-\d{4}", result)

    def test_mm_dd_yyyy_format(self):
        """Should return MM-DD-YYYY pattern."""
        result = mm_dd_yyyy()
        assert re.match(r"\d{2}-\d{2}-\d{4}", result)

    def test_dd_mm_yyyy_vs_mm_dd_yyyy_are_different(self):
        """Should generally produce different values (unless day==month)."""
        d = dd_mm_yyyy()
        m = mm_dd_yyyy()
        parts_d = d.split("-")
        parts_m = m.split("-")
        # DD-MM-YYYY first two are day,month; MM-DD-YYYY first two are month,day
        if parts_d[0] != parts_m[0]:  # day may equal month on same numbers
            assert parts_d[0] == parts_m[1]
            assert parts_d[1] == parts_m[0]

    def test_past_dd_mm_yyyy(self):
        """Past date should differ from current and have correct format."""
        result = past_dd_mm_yyyy(30)
        assert re.match(r"\d{2}-\d{2}-\d{4}", result)
        assert result != dd_mm_yyyy()

    def test_future_dd_mm_yyyy(self):
        """Future date should differ from current."""
        result = future_dd_mm_yyyy(30)
        assert re.match(r"\d{2}-\d{2}-\d{4}", result)
        assert result != dd_mm_yyyy()

    def test_past_vs_future_symmetry(self):
        """Past N days ago should differ from future N days from now."""
        assert past_dd_mm_yyyy(7) != future_dd_mm_yyyy(7)


class TestSlashDates:
    """Tests for DD/MM/YYYY and MM/DD/YYYY formats."""

    def test_slash_dd_mm_yyyy_format(self):
        """Should return DD/MM/YYYY pattern."""
        result = slash_dd_mm_yyyy()
        assert re.match(r"\d{2}/\d{2}/\d{4}", result)

    def test_slash_mm_dd_yyyy_format(self):
        """Should return MM/DD/YYYY pattern."""
        result = slash_mm_dd_yyyy()
        assert re.match(r"\d{2}/\d{2}/\d{4}", result)

    def test_past_slash_vs_current(self):
        """Past slash date should differ from current slash date."""
        assert past_slash_dd_mm_yyyy(14) != slash_dd_mm_yyyy()

    def test_future_slash_vs_current(self):
        """Future slash date should differ from current."""
        assert future_slash_dd_mm_yyyy(14) != slash_dd_mm_yyyy()


class TestUtilityFunctions:
    """Tests for helper/utility functions."""

    def test_list_available_formats(self):
        """Should list all registered format keys."""
        formats = list_available_formats()
        assert isinstance(formats, list)
        assert "pretty" in formats
        assert "dd-mm-yyyy" in formats
        assert "mm/dd/yyyy" in formats
        assert set(formats) == set(_FORMATS.keys())

    def test_negative_days_ago(self):
        """Negative days_ago should effectively be a future date."""
        past = past_dd_mm_yyyy(-7)
        future = future_dd_mm_yyyy(7)
        assert past == future

    def test_negative_days_future(self):
        """Negative days_from_now should effectively be a past date."""
        future = future_dd_mm_yyyy(-7)
        past = past_dd_mm_yyyy(7)
        assert future == past

    @pytest.mark.parametrize("days", [1, 3, 7, 30, 365])
    def test_various_past_periods(self, days):
        """Should produce valid dates for various periods."""
        result = past_dd_mm_yyyy(days)
        assert re.match(r"\d{2}-\d{2}-\d{4}", result)

    @pytest.mark.parametrize("days", [1, 3, 7, 30, 365])
    def test_various_future_periods(self, days):
        """Should produce valid dates for various future periods."""
        result = future_dd_mm_yyyy(days)
        assert re.match(r"\d{2}-\d{2}-\d{4}", result)

    @pytest.mark.parametrize(
        "fmt_key, pattern",
        [
            ("pretty", "%A, %B %d, %Y"),
            ("dd-mm-yyyy", "%d-%m-%Y"),
            ("mm-dd-yyyy", "%m-%d-%Y"),
            ("dd/mm/yyyy", "%d/%m/%Y"),
            ("mm/dd/yyyy", "%m/%d/%Y"),
        ],
    )
    def test_format_date_applies_registered_pattern(self, fmt_key, pattern):
        """Should match the strftime pattern registered for each key."""
        day = dt.datetime(2026, 7, 20, 12, 34, 56)
        assert _format_date(day, fmt_key) == day.strftime(pattern)

    @patch("py_simple_package.src.py_simple.easy_date_formatter.datetime")
    def test_get_past_date_subtracts_days(self, mock_datetime):
        """Should pin exact output against a fixed now."""
        mock_datetime.now.return_value = dt.datetime(2026, 7, 20, 12, 34, 56)
        assert _get_past_date(7) == dt.datetime(2026, 7, 13, 12, 34, 56)

    @patch("py_simple_package.src.py_simple.easy_date_formatter.datetime")
    def test_get_future_date_adds_days(self, mock_datetime):
        """Should pin exact output against a fixed now."""
        mock_datetime.now.return_value = dt.datetime(2026, 7, 20, 12, 34, 56)
        assert _get_future_date(7) == dt.datetime(2026, 7, 27, 12, 34, 56)


def test_mm_dd_yyyy():
    # ARRANGE
    expected_output = dt.datetime.now().strftime("%m-%d-%Y")

    # ACT
    result = mm_dd_yyyy()

    # ASSERT
    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_dd_mm_yyyy():
    # ARRANGE
    expected_output = datetime.now().strftime("%d-%m-%Y")

    # ACT
    result = dd_mm_yyyy()

    # ASSERT
    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_pretty_date():
    expected_output = datetime.now().strftime("%A, %B %d, %Y")

    result = get_pretty_date()

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_slash_dd_mm_yyyy():
    expected_output = dt.datetime.now().strftime("%d/%m/%Y")

    result = slash_dd_mm_yyyy()

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_slash_mm_dd_yyyy():
    expected_output = dt.datetime.now().strftime("%m/%d/%Y")

    result = slash_mm_dd_yyyy()

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_past_pretty_date():
    expected_output = [
        (datetime.now() - timedelta(days=1)).strftime("%A, %B %d, %Y"),
        (datetime.now() - timedelta(days=4)).strftime("%A, %B %d, %Y"),
        (datetime.now() - timedelta(days=9)).strftime("%A, %B %d, %Y"),
        (datetime.now() - timedelta(days=30)).strftime("%A, %B %d, %Y"),
    ]

    result = [
        get_past_pretty_date(1),
        get_past_pretty_date(4),
        get_past_pretty_date(9),
        get_past_pretty_date(30),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_past_dd_mm_yyyy():
    expected_output = [
        (dt.datetime.now() - timedelta(1)).strftime("%d-%m-%Y"),
        (dt.datetime.now() - timedelta(25)).strftime("%d-%m-%Y"),
        (dt.datetime.now() - timedelta(13)).strftime("%d-%m-%Y"),
        (dt.datetime.now() - timedelta(53)).strftime("%d-%m-%Y"),
    ]

    result = [
        past_dd_mm_yyyy(1),
        past_dd_mm_yyyy(25),
        past_dd_mm_yyyy(13),
        past_dd_mm_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_past_mm_dd_yyyy():
    expected_output = [
        (dt.datetime.now() - timedelta(1)).strftime("%m-%d-%Y"),
        (dt.datetime.now() - timedelta(25)).strftime("%m-%d-%Y"),
        (dt.datetime.now() - timedelta(13)).strftime("%m-%d-%Y"),
        (dt.datetime.now() - timedelta(53)).strftime("%m-%d-%Y"),
    ]

    result = [
        past_mm_dd_yyyy(1),
        past_mm_dd_yyyy(25),
        past_mm_dd_yyyy(13),
        past_mm_dd_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_past_slash_dd_mm_yyyy():
    expected_output = [
        (dt.datetime.now() - timedelta(1)).strftime("%d/%m/%Y"),
        (dt.datetime.now() - timedelta(25)).strftime("%d/%m/%Y"),
        (dt.datetime.now() - timedelta(13)).strftime("%d/%m/%Y"),
        (dt.datetime.now() - timedelta(53)).strftime("%d/%m/%Y"),
    ]

    result = [
        past_slash_dd_mm_yyyy(1),
        past_slash_dd_mm_yyyy(25),
        past_slash_dd_mm_yyyy(13),
        past_slash_dd_mm_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_past_slash_mm_dd_yyyy():
    expected_output = [
        (dt.datetime.now() - timedelta(1)).strftime("%m/%d/%Y"),
        (dt.datetime.now() - timedelta(25)).strftime("%m/%d/%Y"),
        (dt.datetime.now() - timedelta(13)).strftime("%m/%d/%Y"),
        (dt.datetime.now() - timedelta(53)).strftime("%m/%d/%Y"),
    ]

    result = [
        past_slash_mm_dd_yyyy(1),
        past_slash_mm_dd_yyyy(25),
        past_slash_mm_dd_yyyy(13),
        past_slash_mm_dd_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_future_pretty_date():
    expected_output = [
        (datetime.now() + timedelta(1)).strftime("%A, %B %d, %Y"),
        (datetime.now() + timedelta(4)).strftime("%A, %B %d, %Y"),
        (datetime.now() + timedelta(9)).strftime("%A, %B %d, %Y"),
        (datetime.now() + timedelta(30)).strftime("%A, %B %d, %Y"),
    ]

    result = [
        get_future_pretty_date(1),
        get_future_pretty_date(4),
        get_future_pretty_date(9),
        get_future_pretty_date(30),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_future_dd_mm_yyyy():
    expected_output = [
        (dt.datetime.now() + timedelta(1)).strftime("%d-%m-%Y"),
        (dt.datetime.now() + timedelta(25)).strftime("%d-%m-%Y"),
        (dt.datetime.now() + timedelta(13)).strftime("%d-%m-%Y"),
        (dt.datetime.now() + timedelta(53)).strftime("%d-%m-%Y"),
    ]

    result = [
        future_dd_mm_yyyy(1),
        future_dd_mm_yyyy(25),
        future_dd_mm_yyyy(13),
        future_dd_mm_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_future_mm_dd_yyyy():
    expected_output = [
        (dt.datetime.now() + timedelta(1)).strftime("%m-%d-%Y"),
        (dt.datetime.now() + timedelta(25)).strftime("%m-%d-%Y"),
        (dt.datetime.now() + timedelta(13)).strftime("%m-%d-%Y"),
        (dt.datetime.now() + timedelta(53)).strftime("%m-%d-%Y"),
    ]

    result = [
        future_mm_dd_yyyy(1),
        future_mm_dd_yyyy(25),
        future_mm_dd_yyyy(13),
        future_mm_dd_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_future_slash_dd_mm_yyyy():
    expected_output = [
        (dt.datetime.now() + timedelta(1)).strftime("%d/%m/%Y"),
        (dt.datetime.now() + timedelta(25)).strftime("%d/%m/%Y"),
        (dt.datetime.now() + timedelta(13)).strftime("%d/%m/%Y"),
        (dt.datetime.now() + timedelta(53)).strftime("%d/%m/%Y"),
    ]

    result = [
        future_slash_dd_mm_yyyy(1),
        future_slash_dd_mm_yyyy(25),
        future_slash_dd_mm_yyyy(13),
        future_slash_dd_mm_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"


def test_future_slash_mm_dd_yyyy():
    expected_output = [
        (dt.datetime.now() + timedelta(1)).strftime("%m/%d/%Y"),
        (dt.datetime.now() + timedelta(25)).strftime("%m/%d/%Y"),
        (dt.datetime.now() + timedelta(13)).strftime("%m/%d/%Y"),
        (dt.datetime.now() + timedelta(53)).strftime("%m/%d/%Y"),
    ]

    result = [
        future_slash_mm_dd_yyyy(1),
        future_slash_mm_dd_yyyy(25),
        future_slash_mm_dd_yyyy(13),
        future_slash_mm_dd_yyyy(53),
    ]

    assert result == expected_output, f"Expected {expected_output} but got {result}"

    assert result == expected_output, f"Expected {expected_output} but got {result}"
    assert result == expected_output, f"Expected {expected_output} but got {result}"

    assert result == expected_output, f"Expected {expected_output} but got {result}"

    assert result == expected_output, f"Expected {expected_output} but got {result}"
