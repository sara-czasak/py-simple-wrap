"""Tests for easy_logging module."""

import logging

import pytest

from py_simple_package.src.py_simple import count_log_levels as public_count_log_levels
from py_simple_package.src.py_simple.easy_logging import (
    clear_log_file,
    count_log_levels,
    find_log_lines,
    log_function,
    log_step,
    log_to_file,
    read_recent_log_lines,
)


def test_log_step_logs_start_and_finish(caplog):
    with caplog.at_level(logging.INFO), log_step("Calculate total"):
        assert caplog.messages == ["Starting: Calculate total"]
        total = sum([10, 20, 30])

    assert total == 60
    assert [(record.levelno, record.message) for record in caplog.records] == [
        (logging.INFO, "Starting: Calculate total"),
        (logging.INFO, "Finished: Calculate total"),
    ]


def test_log_step_logs_error_and_reraises(caplog):
    error = ValueError("Operation failed")

    with caplog.at_level(logging.INFO), pytest.raises(ValueError) as exc_info:
        with log_step("Calculate total"):
            raise error

    assert exc_info.value is error
    assert caplog.messages == [
        "Starting: Calculate total",
        "Error during: Calculate total",
    ]
    record = caplog.records[-1]
    assert record.levelno == logging.ERROR
    assert record.exc_info[1] is error
    assert record.exc_info[2] is not None


@pytest.mark.parametrize(
    "args, kwargs, expected, message",
    [
        ((2, 3), {}, 5, "Add 2 and 3"),
        ((2,), {"b": 4}, 6, "Add 2 and 4"),
        ((2,), {}, 12, "Add 2 and 10"),
    ],
)
def test_log_function_formats_arguments_and_returns_result(
    caplog, args, kwargs, expected, message
):
    @log_function("Add {a} and {b}")
    def add(a, b=10):
        return a + b

    with caplog.at_level(logging.INFO):
        result = add(*args, **kwargs)

    assert result == expected
    assert caplog.messages == [f"Starting: {message}", f"Finished: {message}"]


def test_log_function_logs_error_and_reraises(caplog):
    error = ValueError("Invalid value")

    @log_function("Process {value}")
    def process(value):
        raise error

    with caplog.at_level(logging.INFO), pytest.raises(ValueError) as exc_info:
        process(5)

    assert exc_info.value is error
    assert caplog.messages == ["Starting: Process 5", "Error during: Process 5"]
    record = caplog.records[-1]
    assert record.levelno == logging.ERROR
    assert record.exc_info[1] is error
    assert record.exc_info[2] is not None


def test_log_function_preserves_metadata():
    @log_function("Add {a} and {b}")
    def add(a, b):
        """Returns the sum of two numbers."""
        return a + b

    assert add.__name__ == "add"
    assert add.__doc__ == "Returns the sum of two numbers."


def test_log_function_missing_message_field_does_not_run_function(caplog):
    calls = []

    @log_function("Process {missing}")
    def process(value):
        calls.append(value)

    with caplog.at_level(logging.INFO), pytest.raises(KeyError, match="missing"):
        process(5)

    assert calls == []
    assert caplog.messages == []


def test_clear_log_file_empties_existing_file(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line one\nline two\n")

    result = clear_log_file(str(log_file))

    assert result is True
    assert log_file.read_text() == ""


def test_clear_log_file_returns_false_when_missing(tmp_path):
    missing_file = tmp_path / "does_not_exist.log"

    result = clear_log_file(str(missing_file))

    assert result is False


def test_read_recent_log_lines_returns_last_lines(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line one\nline two\nline three\n")

    assert read_recent_log_lines(str(log_file), line_count=2) == [
        "line two",
        "line three",
    ]


def test_read_recent_log_lines_returns_all_lines_when_count_is_large(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line one\nline two\n")

    assert read_recent_log_lines(str(log_file), line_count=10) == [
        "line one",
        "line two",
    ]


def test_read_recent_log_lines_returns_empty_list_when_missing(tmp_path):
    missing_file = tmp_path / "missing.log"

    assert read_recent_log_lines(str(missing_file)) == []


def test_read_recent_log_lines_returns_empty_list_for_invalid_count(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line one\n")

    assert read_recent_log_lines(str(log_file), line_count=0) == []


def test_log_to_file_creates_file_and_writes_message(tmp_path):
    log_file = tmp_path / "app.log"

    result = log_to_file(str(log_file), "Started import job")

    assert result is True
    assert log_file.read_text() == "Started import job\n"


def test_log_to_file_appends_to_existing_file(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("First line\n")

    log_to_file(str(log_file), "Second line")

    assert log_file.read_text() == "First line\nSecond line\n"


def test_find_log_lines_returns_matching_lines_without_newlines(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("INFO: Started\nERROR: Connection failed\nERROR: Retry\n")

    assert find_log_lines(str(log_file), "ERROR") == [
        "ERROR: Connection failed",
        "ERROR: Retry",
    ]


def test_find_log_lines_returns_empty_list_when_nothing_matches(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("INFO: Started\nWARNING: Slow response\n")

    assert find_log_lines(str(log_file), "ERROR") == []


def test_find_log_lines_returns_empty_list_when_file_is_missing(tmp_path):
    missing_file = tmp_path / "missing.log"

    assert find_log_lines(str(missing_file), "ERROR") == []


def test_count_log_levels_counts_each_standard_level(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text(
        "DEBUG startup\n"
        "INFO ready\n"
        "INFO still ready\n"
        "WARNING slow\n"
        "ERROR failed\n"
        "CRITICAL down\n"
    )

    assert count_log_levels(str(log_file)) == {
        "DEBUG": 1,
        "INFO": 2,
        "WARNING": 1,
        "ERROR": 1,
        "CRITICAL": 1,
    }


def test_count_log_levels_ignores_level_names_inside_words(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("INFORMATION loaded\nDEBUGGING helper\n")

    assert count_log_levels(str(log_file)) == {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
    }


def test_count_log_levels_missing_file_returns_zeros(tmp_path):
    missing_file = tmp_path / "missing.log"
    assert count_log_levels(str(missing_file)) == {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
    }


def test_count_log_levels_public_import():
    assert public_count_log_levels is count_log_levels
