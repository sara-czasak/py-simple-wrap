"""Tests for easy_logging module."""

import logging

import pytest

from py_simple_package.src.py_simple.easy_logging import log_function, log_step


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
