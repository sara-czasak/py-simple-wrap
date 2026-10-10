"""
easy_logging is meant to simplify logging code blocks and function calls.
Built on top of the logging module, it handles start, success, and error
messages without repeating try/except blocks.

Configure logging in your application before using these helpers, for
example with logging.basicConfig(level=logging.INFO).
"""

import logging
import os
import re
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from inspect import signature
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


@contextmanager
def log_step(message: str) -> Iterator[None]:
    """
    Logs the start, successful completion, or failure of a code block.

    Writes "Starting:" and "Finished:" messages at INFO level. If the
    block raises an Exception, logs "Error during:" at ERROR level with
    the traceback and re-raises the original exception instead of logging
    a successful completion. Uses the root logger and its configuration.

    Args:
        message (str): Description of the operation, such as
            "Calculate total".

    Yields:
        None: Runs the enclosed code block without providing an object
            for an optional `as` target.

    Raises:
        Exception: Re-raises any Exception raised by the enclosed block
            after logging it.

    Example:
        === "The Py_simple Way"
            ```python
            import logging
            from py_simple.easy_logging import log_step

            logging.basicConfig(level=logging.INFO)

            with log_step("Calculate total"):
                total = sum([10, 20, 30])

            print(total)  # -> 60
            ```

        === "The Traditional Way"
            ```python
            import logging

            logging.basicConfig(level=logging.INFO)

            try:
                logging.info("Starting: Calculate total")
                total = sum([10, 20, 30])
            except Exception:
                logging.exception("Error during: Calculate total")
                raise
            else:
                logging.info("Finished: Calculate total")

            print(total)  # -> 60
            ```
    """
    try:
        logging.info(f"Starting: {message}")
        yield
    except Exception:
        logging.exception(f"Error during: {message}")
        raise
    else:
        logging.info(f"Finished: {message}")


def log_function(
    message_template: str,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Creates a decorator that logs each call to a synchronous function and method.

    Formats the message using the function's argument names and values,
    including default values for omitted arguments. Excludes `self` and
    `cls` from the formatting context. Uses log_step to log the start,
    successful completion, or exception with a traceback through the
    root logger. Preserves the function's metadata and return value.

    Argument binding and message formatting happen before logging starts;
    errors in those steps propagate without being logged by this helper.
    For async functions or generators, this decorator only logs creation
    of the coroutine or generator, not its later execution.

    Args:
        message_template (str): Message with named str.format_map fields
            matching function parameters, such as "Add {a} and {b}".
            Format specifications such as "{price:.2f}" are supported.

    Returns:
        Callable[[Callable[P, R]], Callable[P, R]]: Decorator that wraps a
            function with logging while preserving its parameters and
            return type.

    Raises:
        KeyError: A message field is missing from the formatting context.
        ValueError: The message template or a format specification is
            invalid.
        TypeError: The supplied arguments cannot be bound to the wrapped
            function's signature.
        Exception: Re-raises any Exception from the wrapped function
            after logging it.

    Example:
        === "The Py_simple Way"
            ```python
            import logging
            from py_simple.easy_logging import log_function

            logging.basicConfig(level=logging.INFO)

            @log_function("Add {a} and {b}")
            def add(a: int, b: int = 10) -> int:
                return a + b

            print(add(5))  # -> 15; logs "Add 5 and 10"
            ```

        === "The Traditional Way"
            ```python
            import logging

            logging.basicConfig(level=logging.INFO)

            def add(a: int, b: int = 10) -> int:
                message = f"Add {a} and {b}"
                try:
                    logging.info(f"Starting: {message}")
                    result = a + b
                except Exception:
                    logging.exception(f"Error during: {message}")
                    raise
                else:
                    logging.info(f"Finished: {message}")
                    return result

            print(add(5))  # -> 15; logs "Add 5 and 10"
            ```
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        func_signature = signature(func)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound_args = func_signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            log_context = {
                name: value
                for name, value in bound_args.arguments.items()
                if name not in {"self", "cls"}
            }
            message = message_template.format_map(log_context)

            with log_step(message):
                return func(*args, **kwargs)

        return wrapper

    return decorator

def clear_log_file(file_path: str) -> bool:
    """
    Empties a log file, leaving it in place but with no contents.
    Args:
        file_path (str): Path to the log file to clear.
    Returns:
        bool: True if the file was cleared successfully, False if the
            file could not be found (e.g., False when the path doesn't exist).
    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import clear_log_file
            clear_log_file("app.log")
            ```
        === "The Traditional Way"
            ```python
            import os
            if os.path.exists("app.log"):
                open("app.log", "w").close()
            ```
    """
    if not os.path.exists(file_path):
        return False

    with open(file_path, "w"):
        pass

    return True


def read_recent_log_lines(file_path: str, line_count: int = 10) -> list[str]:
    """
    Reads the most recent lines from a log file.

    Args:
        file_path (str): Path to the log file to read.
        line_count (int, optional): Number of recent lines to return.
            Defaults to `10`.

    Returns:
        list[str]: The last `line_count` lines without trailing newline
            characters. Returns an empty list if the file does not exist
            or if `line_count` is less than `1`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import read_recent_log_lines

            recent_lines = read_recent_log_lines("app.log", line_count=5)
            ```

        === "The Traditional Way"
            ```python
            import os

            if os.path.exists("app.log"):
                with open("app.log") as log_file:
                    recent_lines = [line.rstrip("\\n") for line in log_file.readlines()[-5:]]
            else:
                recent_lines = []
            ```
    """
    if line_count < 1 or not os.path.exists(file_path):
        return []

    with open(file_path) as log_file:
        return [line.rstrip("\n") for line in log_file.readlines()[-line_count:]]


def log_to_file(file_path: str, message: str) -> bool:
    """
    Appends a message to a log file.

    Creates the file if it does not exist and writes the message as one
    line. Returns True after the message is written successfully.

    Args:
        file_path (str): Path to the log file to write to.
        message (str): Message to append to the log file.

    Returns:
        bool: True when the message is written successfully.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import log_to_file

            log_to_file("app.log", "Started import job")
            ```

        === "The Traditional Way"
            ```python
            with open("app.log", "a") as log_file:
                log_file.write("Started import job\\n")
            ```
    """
    with open(file_path, "a") as log_file:
        log_file.write(f"{message}\n")

    return True


def find_log_lines(file_path: str, search_text: str) -> list[str]:
    """
    Returns log file lines that contain the supplied search text.

    Searches case sensitively and removes trailing newline characters from
    returned lines. Returns an empty list when the file does not exist or
    when no lines contain the search text.

    Args:
        file_path (str): Path to the log file to search.
        search_text (str): Text to look for in each log line.

    Returns:
        list[str]: Matching log lines without trailing newline characters.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple.easy_logging import find_log_lines

            errors = find_log_lines("app.log", "ERROR")
            ```

        === "The Traditional Way"
            ```python
            import os

            if os.path.exists("app.log"):
                with open("app.log") as log_file:
                    errors = [
                        line.rstrip("\\n")
                        for line in log_file
                        if "ERROR" in line
                    ]
            else:
                errors = []
            ```
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path) as log_file:
        return [
            line.rstrip("\n") for line in log_file if search_text in line
        ]


def count_log_levels(file_path: str) -> dict[str, int]:
    """
    Counts how many lines in a log file mention each standard level.

    Looks for DEBUG, INFO, WARNING, ERROR, and CRITICAL as whole words,
    so a line is counted once for each level name it contains. A missing
    file returns zeros for every level.

    Args:
        file_path (str): Path to the log file to scan.

    Returns:
        dict[str, int]: Counts keyed by level name, always including
            DEBUG, INFO, WARNING, ERROR, and CRITICAL.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_log_levels

            totals = count_log_levels("app.log")
            print(totals["ERROR"])
            ```

        === "The Traditional Way"
            ```python
            import os
            import re

            levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            totals = {level: 0 for level in levels}
            if os.path.exists("app.log"):
                with open("app.log") as log_file:
                    for line in log_file:
                        for level in levels:
                            if re.search(rf"\\b{level}\\b", line):
                                totals[level] += 1
            ```
    """
    levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    totals = {level: 0 for level in levels}
    if not os.path.exists(file_path):
        return totals

    patterns = {level: re.compile(rf"\b{level}\b") for level in levels}
    with open(file_path) as log_file:
        for line in log_file:
            for level, pattern in patterns.items():
                if pattern.search(line):
                    totals[level] += 1
    return totals
