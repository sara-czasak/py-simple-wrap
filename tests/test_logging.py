import logging
import pytest
from py_simple_package.src.py_simple.easy_logging import setup_file_logger
"""Tests for easy_logging module."""

import logging

import pytest

from py_simple_package.src.py_simple.easy_logging import (
    clear_log_file,
    find_log_lines,
    log_function,
    log_step,
    log_to_file,
    read_recent_log_lines,
    setup_file_logger,
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


def test_setup_file_logger_writes_to_file(tmp_path):
    log_file = tmp_path / "app.log"
    logger = setup_file_logger(str(log_file))
    logger.info("Application started")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "INFO - Application started" in content



'Tests for easy_logging module.'
@pytest.fixture(autouse=True)
def cleanup_logging_handlers():
    """Ensure handlers added during tests are closed and removed."""
    yield
    manager = logging.Logger.manager
    loggers = [logging.root] + [logging.getLogger(name) for name in manager.loggerDict]
    for logger in loggers:
        for handler in list(logger.handlers):
            if isinstance(handler, logging.FileHandler):
                handler.close()
                logger.removeHandler(handler)
def test_setup_file_logger_creates_file_and_logs(tmp_path):
    log_file = tmp_path / 'app.log'
    logger = setup_file_logger(str(log_file))
    logger.info('Application started successfully')
    assert log_file.exists()
    content = log_file.read_text(encoding='utf-8')
    assert 'INFO - Application started successfully' in content
def test_setup_file_logger_respects_level_int(tmp_path):
    log_file = tmp_path / 'app.log'
    logger = setup_file_logger(str(log_file), level=logging.WARNING)
    logger.info('This info message should not appear')
    logger.warning('This warning message should appear')
    content = log_file.read_text(encoding='utf-8')
    assert 'This info message should not appear' not in content
    assert 'WARNING - This warning message should appear' in content
def test_setup_file_logger_respects_level_str(tmp_path):
    log_file = tmp_path / 'debug.log'
    logger = setup_file_logger(str(log_file), level='debug')
    logger.debug('Debug message logged via string level')
    content = log_file.read_text(encoding='utf-8')
    assert 'DEBUG - Debug message logged via string level' in content
def test_setup_file_logger_custom_format(tmp_path):
    log_file = tmp_path / 'custom.log'
    logger = setup_file_logger(str(log_file), format_string='[%(levelname)s] %(message)s')
    logger.info('Custom formatted log line')
    content = log_file.read_text(encoding='utf-8')
    assert content.strip() == '[INFO] Custom formatted log line'
def test_setup_file_logger_creates_parent_directories(tmp_path):
    log_file = tmp_path / 'nested' / 'sub' / 'app.log'
    logger = setup_file_logger(str(log_file))
    logger.info('Nested directory message')
    assert log_file.exists()
    content = log_file.read_text(encoding='utf-8')
    assert 'INFO - Nested directory message' in content
def test_setup_file_logger_custom_name(tmp_path):
    log_file = tmp_path / 'named.log'
    logger = setup_file_logger(str(log_file), name='my_custom_service')
    assert logger.name == 'my_custom_service'
    logger.info('Named service message')
    content = log_file.read_text(encoding='utf-8')
    assert 'INFO - Named service message' in content
def test_setup_file_logger_does_not_duplicate_handlers(tmp_path):
    log_file = tmp_path / 'single_handler.log'
    logger1 = setup_file_logger(str(log_file))
    logger2 = setup_file_logger(str(log_file))
    assert logger1 is logger2
    file_handlers = [h for h in logger1.handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) == 1
    logger1.info('Single line message')
    lines = log_file.read_text(encoding='utf-8').strip().splitlines()
    assert len(lines) == 1
def test_setup_file_logger_updates_level_on_existing_handler(tmp_path):
    log_file = tmp_path / 'level_update.log'
    logger = setup_file_logger(str(log_file), level=logging.WARNING)
    logger.info('Ignored before update')
    setup_file_logger(str(log_file), level=logging.DEBUG)
    logger.info('Captured after update')
    content = log_file.read_text(encoding='utf-8')
    assert 'Ignored before update' not in content
    assert 'INFO - Captured after update' in content
def test_setup_file_logger_imported_from_py_simple():
    from py_simple.easy_logging import setup_file_logger as easy_logging_setup
    from py_simple import setup_file_logger as top_level_setup
    assert callable(easy_logging_setup)
    assert callable(top_level_setup)
    assert easy_logging_setup is top_level_setup