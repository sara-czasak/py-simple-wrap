"""Tests for easy_logging module."""

import io
import logging
from uuid import uuid4

import pytest

from py_simple_package.src.py_simple import (
    count_log_levels as public_count_log_levels,
    setup_file_logger as public_setup_file_logger,
)
from py_simple_package.src.py_simple.easy_logging import (
    clear_log_file,
    count_log_levels,
    filter_log_lines,
    find_log_lines,
    log_function,
    log_step,
    log_to_file,
    read_recent_log_lines,
    setup_file_logger,
    temporary_log_level,
)


@pytest.fixture
def level_logger():
    """Register an isolated logger and remove only its own state afterward."""
    logger = logging.getLogger(f"temporary-level-test-{uuid4().hex}")
    logger.setLevel(logging.WARNING)
    logger.propagate = False
    handler = logging.StreamHandler(io.StringIO())
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)
    try:
        yield logger
    finally:
        logger.removeHandler(handler)
        handler.close()
        logging.Logger.manager.loggerDict.pop(logger.name)


def test_temporary_log_level_top_level_public_import(level_logger):
    from py_simple import temporary_log_level as public_temporary_log_level
    from py_simple.easy_logging import temporary_log_level as module_temporary_log_level

    assert public_temporary_log_level is module_temporary_log_level
    stream = level_logger.handlers[0].stream
    level_logger.debug("hidden before public context")
    with public_temporary_log_level(level_logger, "debug"):
        assert level_logger.level == logging.DEBUG
        level_logger.debug("visible through public import")
    assert level_logger.level == logging.WARNING
    level_logger.debug("hidden after public context")
    assert stream.getvalue() == "DEBUG: visible through public import\n"


@pytest.mark.parametrize(
    "level,expected",
    [
        (logging.DEBUG, logging.DEBUG),
        (logging.INFO, logging.INFO),
        (logging.NOTSET, logging.NOTSET),
        (15, 15),
        (-1, -1),
        (True, True),
        ("debug", logging.DEBUG),
        ("InFo", logging.INFO),
        ("WARN", logging.WARNING),
        ("fatal", logging.CRITICAL),
        ("NOTSET", logging.NOTSET),
    ],
)
def test_temporary_log_level_restores_explicit_level(level_logger, level, expected):
    with temporary_log_level(level_logger, level) as value:
        assert value is None
        assert level_logger.level == expected
    assert level_logger.level == logging.WARNING


def test_temporary_log_level_changes_actual_records_and_restores_cache(level_logger):
    stream = level_logger.handlers[0].stream
    level_logger.debug("hidden before")
    with temporary_log_level(level_logger, logging.DEBUG):
        level_logger.debug("visible inside")
        level_logger.info("also visible")
    level_logger.debug("hidden after")
    level_logger.warning("visible after")
    assert stream.getvalue().splitlines() == [
        "DEBUG: visible inside",
        "INFO: also visible",
        "WARNING: visible after",
    ]


def test_temporary_log_level_restores_notset_inheritance(level_logger):
    parent = logging.Logger("temporary-parent", logging.ERROR)
    level_logger.parent = parent
    level_logger.setLevel(logging.NOTSET)
    assert level_logger.getEffectiveLevel() == logging.ERROR
    with temporary_log_level(level_logger, "debug"):
        assert level_logger.getEffectiveLevel() == logging.DEBUG
        parent.setLevel(logging.CRITICAL)
    assert level_logger.level == logging.NOTSET
    assert level_logger.getEffectiveLevel() == logging.CRITICAL


@pytest.mark.parametrize("error_type", [ValueError, KeyboardInterrupt, SystemExit])
def test_temporary_log_level_restores_and_preserves_exception(level_logger, error_type):
    error = error_type("original failure")
    origin = None
    with pytest.raises(error_type) as caught:
        with temporary_log_level(level_logger, "debug"):
            try:
                raise error
            except BaseException as raised:
                origin = raised.__traceback__
                raise
    assert caught.value is error
    traceback = caught.value.__traceback__
    frames = []
    while traceback is not None:
        frames.append(traceback)
        traceback = traceback.tb_next
    assert origin in frames
    assert level_logger.level == logging.WARNING


def test_temporary_log_level_nested_success_and_failure(level_logger):
    with temporary_log_level(level_logger, "info"):
        with temporary_log_level(level_logger, logging.DEBUG):
            assert level_logger.level == logging.DEBUG
        assert level_logger.level == logging.INFO
        with pytest.raises(RuntimeError, match="inner"):
            with temporary_log_level(level_logger, logging.ERROR):
                raise RuntimeError("inner")
        assert level_logger.level == logging.INFO
    assert level_logger.level == logging.WARNING


@pytest.mark.parametrize(
    "level,error_type",
    [
        (None, TypeError),
        (1.5, TypeError),
        ([], TypeError),
        ({}, TypeError),
        (object(), TypeError),
        ("unknown", ValueError),
        ("10", ValueError),
        ("", ValueError),
    ],
)
def test_temporary_log_level_invalid_level_does_not_enter(
    level_logger, level, error_type
):
    entered = False
    with pytest.raises(error_type):
        with temporary_log_level(level_logger, level):
            entered = True
    assert not entered
    assert level_logger.level == logging.WARNING


@pytest.mark.parametrize(
    "logger",
    [None, "example", object(), logging.LoggerAdapter(logging.Logger("adapter"), {})],
)
def test_temporary_log_level_rejects_invalid_logger(logger):
    with pytest.raises(TypeError, match="logger must be a logging.Logger"):
        with temporary_log_level(logger, "debug"):
            pytest.fail("Invalid logger must not enter the block")


def test_temporary_log_level_leaves_other_state_and_handler_threshold(level_logger):
    handler = level_logger.handlers[0]
    handler.setLevel(logging.ERROR)
    logger_filter, handler_filter = logging.Filter(), logging.Filter()
    level_logger.addFilter(logger_filter)
    handler.addFilter(handler_filter)
    other = logging.Logger("unrelated", logging.CRITICAL)
    root_state = (logging.root.level, list(logging.root.handlers))
    disabled = logging.root.manager.disable
    original_state = (
        list(level_logger.handlers),
        list(level_logger.filters),
        level_logger.propagate,
        level_logger.disabled,
        handler.level,
        list(handler.filters),
        handler.formatter,
    )
    with temporary_log_level(level_logger, "debug"):
        level_logger.debug("still blocked by handler")
        level_logger.error("visible error")
        assert other.level == logging.CRITICAL
    assert handler.stream.getvalue() == "ERROR: visible error\n"
    assert original_state == (
        list(level_logger.handlers),
        list(level_logger.filters),
        level_logger.propagate,
        level_logger.disabled,
        handler.level,
        list(handler.filters),
        handler.formatter,
    )
    assert root_state == (logging.root.level, list(logging.root.handlers))
    assert logging.root.manager.disable == disabled


def test_temporary_log_level_does_not_enable_disabled_logger(level_logger):
    level_logger.disabled = True
    with temporary_log_level(level_logger, "debug"):
        level_logger.error("disabled")
    assert level_logger.disabled
    assert level_logger.handlers[0].stream.getvalue() == ""


def test_temporary_log_level_preserves_filtering_and_shared_visibility(level_logger):
    handler = level_logger.handlers[0]

    class MessageFilter(logging.Filter):
        def __init__(self, blocked):
            super().__init__()
            self.blocked = blocked

        def filter(self, record):
            return record.getMessage() != self.blocked

    level_logger.addFilter(MessageFilter("logger-blocked"))
    handler.addFilter(MessageFilter("handler-blocked"))
    shared = logging.getLogger(level_logger.name)
    with temporary_log_level(level_logger, "debug"):
        assert shared.level == logging.DEBUG
        shared.debug("logger-blocked")
        shared.debug("handler-blocked")
        shared.debug("visible")
    assert shared.level == logging.WARNING
    assert handler.stream.getvalue() == "DEBUG: visible\n"


def test_temporary_log_level_restores_entry_value_after_block_changes(level_logger):
    with temporary_log_level(level_logger, "info"):
        level_logger.setLevel(logging.CRITICAL)
    assert level_logger.level == logging.WARNING


def test_temporary_log_level_registered_name(level_logger, monkeypatch):
    monkeypatch.setitem(logging._nameToLevel, "NOTICE", 25)
    with temporary_log_level(level_logger, "notice"):
        assert level_logger.level == 25
    assert level_logger.level == logging.WARNING


def test_temporary_log_level_public_module_import(level_logger):
    from py_simple.easy_logging import temporary_log_level as public_context

    with public_context(level_logger, "debug"):
        assert level_logger.level == logging.DEBUG
    assert level_logger.level == logging.WARNING


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


def test_setup_file_logger_writes_to_file(tmp_path):
    log_file = tmp_path / "app.log"
    logger = setup_file_logger(str(log_file))
    logger.info("Application started")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "INFO - Application started" in content


def test_setup_file_logger_public_import():
    assert public_setup_file_logger is setup_file_logger


@pytest.fixture(autouse=True)
def cleanup_logging_handlers():
    """Ensure only handlers added during tests are closed and removed."""
    manager = logging.Logger.manager
    pre_existing_handlers = {
        name: set(logging.getLogger(name).handlers) for name in list(manager.loggerDict)
    }
    pre_existing_root_handlers = set(logging.root.handlers)

    yield

    for handler in list(logging.root.handlers):
        if handler not in pre_existing_root_handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
            logging.root.removeHandler(handler)

    for name in list(manager.loggerDict):
        logger = logging.getLogger(name)
        known_handlers = pre_existing_handlers.get(name, set())
        for handler in list(logger.handlers):
            if handler not in known_handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
                logger.removeHandler(handler)


def test_setup_file_logger_respects_level_int(tmp_path):
    log_file = tmp_path / "app.log"
    logger = setup_file_logger(str(log_file), level=logging.WARNING)

    logger.info("This info message should not appear")
    logger.warning("This warning message should appear")

    content = log_file.read_text(encoding="utf-8")
    assert "This info message should not appear" not in content
    assert "WARNING - This warning message should appear" in content


def test_setup_file_logger_respects_level_str(tmp_path):
    log_file = tmp_path / "debug.log"
    logger = setup_file_logger(str(log_file), level="debug")

    logger.debug("Debug message logged via string level")

    content = log_file.read_text(encoding="utf-8")
    assert "DEBUG - Debug message logged via string level" in content


def test_setup_file_logger_custom_format(tmp_path):
    log_file = tmp_path / "custom.log"
    logger = setup_file_logger(
        str(log_file),
        format_string="[%(levelname)s] %(message)s",
    )

    logger.info("Custom formatted log line")

    content = log_file.read_text(encoding="utf-8")
    assert content.strip() == "[INFO] Custom formatted log line"


def test_setup_file_logger_creates_parent_directories(tmp_path):
    log_file = tmp_path / "nested" / "sub" / "app.log"
    logger = setup_file_logger(str(log_file))

    logger.info("Nested directory message")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "INFO - Nested directory message" in content


def test_setup_file_logger_custom_name(tmp_path):
    log_file = tmp_path / "named.log"
    logger = setup_file_logger(str(log_file), name="my_custom_service")

    assert logger.name == "my_custom_service"
    logger.info("Named service message")

    content = log_file.read_text(encoding="utf-8")
    assert "INFO - Named service message" in content


def test_setup_file_logger_does_not_duplicate_handlers(tmp_path):
    log_file = tmp_path / "single_handler.log"
    logger1 = setup_file_logger(str(log_file))
    logger2 = setup_file_logger(str(log_file))

    assert logger1 is logger2

    file_handlers = [h for h in logger1.handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) == 1

    logger1.info("Single line message")
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1


def test_setup_file_logger_updates_level_on_existing_handler(tmp_path):
    log_file = tmp_path / "level_update.log"
    logger = setup_file_logger(str(log_file), level=logging.WARNING)

    logger.info("Ignored before update")

    # Reconfigure with DEBUG
    setup_file_logger(str(log_file), level=logging.DEBUG)
    logger.info("Captured after update")

    content = log_file.read_text(encoding="utf-8")
    assert "Ignored before update" not in content
    assert "INFO - Captured after update" in content


def test_filter_log_lines_return_matching_level(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text(
        "2026-10-24 10:00:01,123 - INFO - Application started\n"
        "2026-10-24 10:00:02,234 - ERROR - Connection failed\n"
        "2026-10-24 10:00:03,345 - WARNING - ERROR appears in this message\n"
        "2026-10-24 10:00:04,456 - ERROR - Retry failed\n"
    )

    assert filter_log_lines(str(log_file), "ERROR") == [
        "2026-10-24 10:00:02,234 - ERROR - Connection failed",
        "2026-10-24 10:00:04,456 - ERROR - Retry failed",
    ]
    assert len(filter_log_lines(str(log_file), "WARNING")) == 1


def test_filter_log_lines_accepts_lowercase_level(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("2026-10-24 10:00:01,123 - ERROR - Connection failed\n")

    assert len(filter_log_lines(str(log_file), "error")) == 1


def test_filter_log_lines_returns_empty_list_for_empty_file(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("")

    assert filter_log_lines(str(log_file), "ERROR") == []


def test_filter_log_lines_raises_for_missing_file(tmp_path):
    log_file = tmp_path / "missing.log"

    with pytest.raises(FileNotFoundError):
        filter_log_lines(str(log_file), "ERROR")


def test_filter_log_lines_raises_for_invalid_level(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("2026-10-24 10:00:01,123 - INFO - Started\n")

    with pytest.raises(ValueError):
        filter_log_lines(str(log_file), "TRACE")

        
@pytest.mark.parametrize("new_format", ["[%(levelname)s] %(message)s", "%(message)s"])
def test_setup_file_logger_updates_existing_handler_format(tmp_path, new_format):
    log_file = tmp_path / "reconfigured.log"
    logger = setup_file_logger(str(log_file), format_string="old: %(message)s")
    logger.info("before")
    original_handlers = list(logger.handlers)

    configured = setup_file_logger(str(log_file), format_string=new_format)
    configured.info("after")

    assert configured is logger
    assert logger.handlers == original_handlers
    expected = "[INFO] after" if new_format.startswith("[") else "after"
    assert log_file.read_text(encoding="utf-8").splitlines() == [
        "old: before",
        expected,
    ]
