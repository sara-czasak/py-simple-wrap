"""
easy_logging is meant to simplify logging code blocks and function calls.
Built on top of the logging module, it handles start, success, and error
messages without repeating try/except blocks.

Configure logging in your application before using these helpers, for
example with logging.basicConfig(level=logging.INFO).
"""

import logging
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
