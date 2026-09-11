"""
easy_async is built to simplify asynchronous code execution.
"""

from concurrent.futures import ThreadPoolExecutor


class EasyAsyncError(Exception):
    """
    Raised when a py_simple async function fails to complete.

    Wraps the underlying error (an exception raised inside one of the
    functions being run, a thread pool failure, etc.) so py_simple
    functions can fail with one consistent, easy-to-read exception
    instead of a random builtin one.

    Args:
        message (str): Human-readable description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def run_at_the_same_time_no_params(functions: list) -> list:
    """
    Runs multiple zero-argument functions at the same time and returns
    their results.

    Raises EasyAsyncError if any function raises an exception while
    running.

    Args:
        functions (list): Functions to run, each taking no arguments.

    Returns:
        list: A list of (name, result) tuples, one per function.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_at_the_same_time

            def add():
                return 1 + 1

            def sub():
                return 4 - 2

            run_at_the_same_time([add, sub])  # -> [("add", 2), ("sub", 2)]
            ```

        === "The Traditional Way"
            ```python
            from concurrent.futures import ThreadPoolExecutor

            def add():
                return 1 + 1

            def sub():
                return 4 - 2

            functions = [add, sub]
            results = []
            with ThreadPoolExecutor() as executor:
                tickets = [
                    (f.__name__, executor.submit(f)) for f in functions
                ]
                for name, ticket in tickets:
                    results.append((name, ticket.result()))
            ```
    """
    tickets = []
    results = []
    try:
        with ThreadPoolExecutor() as executor:
            for function in functions:
                ticket = executor.submit(function)
                tickets.append((function.__name__, ticket))
            for ticket in tickets:
                results.append((ticket[0], ticket[1].result()))
        return results
    except Exception as e:
        raise EasyAsyncError(f"\n\n\nERROR: {e}") from None


def run_at_the_same_time_with_params(functions_and_args: list[tuple]) -> list:
    """
    Runs multiple functions at the same time, each with its own
    arguments, and returns their results.

    Raises EasyAsyncError if any function raises an exception while
    running.

    Args:
        functions_and_args (list[tuple]): Functions to run, each given
            as a tuple where the first item is the function and the
            remaining items are the positional arguments to call it
            with, e.g. (func, arg1, arg2).

    Returns:
        list: A list of (name, result) tuples, one per function.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_at_the_same_time_with_params

            def add(a, b):
                return a + b

            def sub(a, b):
                return a - b

            run_at_the_same_time_with_params([
                (add, 1, 1),
                (sub, 4, 2),
            ])  # -> [("add", 2), ("sub", 2)]
            ```

        === "The Traditional Way"
            ```python
            from concurrent.futures import ThreadPoolExecutor

            def add(a, b):
                return a + b

            def sub(a, b):
                return a - b

            functions_and_args = [(add, 1, 1), (sub, 4, 2)]
            results = []
            with ThreadPoolExecutor() as executor:
                tickets = [
                    (item[0].__name__, executor.submit(item[0], *item[1:]))
                    for item in functions_and_args
                ]
                for name, ticket in tickets:
                    results.append((name, ticket.result()))
            ```
    """
    tickets = []
    results = []
    try:
        with ThreadPoolExecutor() as executor:
            for items in functions_and_args:
                args = items[1:]
                ticket = executor.submit(items[0], *args)
                tickets.append((items[0].__name__, ticket))
            for ticket in tickets:
                results.append((ticket[0], ticket[1].result()))
        return results
    except Exception as e:
        raise EasyAsyncError(f"\n\n\nERROR: {e}") from None


def run_with_timeout(func, timeout: float, *args) -> tuple:
    """
    Runs a function asynchronously with a timeout limit.

    Raises EasyAsyncError if the function times out or raises an exception.

    Args:
        func (callable): The function to execute.
        timeout (float): Maximum time to wait in seconds.
        *args: Positional arguments to pass to the function.

    Returns:
        tuple: A tuple containing `(func.__name__, result)`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_with_timeout

            def slow_add(a, b):
                return a + b

            run_with_timeout(slow_add, 2.0, 3, 5)  # -> ("slow_add", 8)
            ```

        === "The Traditional Way"
            ```python
            from concurrent.futures import ThreadPoolExecutor

            def slow_add(a, b):
                return a + b

            with ThreadPoolExecutor() as executor:
                future = executor.submit(slow_add, 3, 5)
                result = future.result(timeout=2.0)
            ```
    """
    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(func, *args)
            result = future.result(timeout=timeout)
            return (func.__name__, result)
    except Exception as e:
        raise EasyAsyncError(f"\n\n\nERROR: {e}") from None
