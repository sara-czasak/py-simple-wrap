"""
easy_flow is built to simplify work flows
"""

import runpy
import time
from functools import wraps


class EasyFlowError(Exception):
    """
    Raised when a Python file can't be run.

    Wraps the underlying error (missing file, bad permissions, an
    exception raised inside the file being run, etc.) so py_simple
    functions can fail with one consistent, easy-to-read exception
    instead of a random builtin one.

    Args:
        message (str): Human-readable description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def run_py_file(filename: str):
    """
    Runs a Python file as if it were called directly from the command
    line (i.e. as `__main__`), using the current process.

    Args:
        filename (str): Path to the `.py` file to run.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_py_file

            run_py_file("script.py")
            ```

        === "The Traditional Way"
            ```python
            import runpy

            print("RUNNING: script.py")
            try:
                runpy.run_path("script.py", run_name="__main__")
            except Exception as e:
                print(f"Couldn't run the file: {e}")
            ```
    """
    print(f"RUNNING: {filename}")
    try:
        runpy.run_path(filename, run_name="__main__")
    except Exception as e:
        raise EasyFlowError(f"\n\n\nERROR: {e}") from None


def run_py_file_safe(filename: str):
    """
    Runs a Python file as if it were called directly from the command
    line (i.e. as `__main__`), returning a success flag instead of
    raising an exception if something goes wrong.

    Args:
        filename (str): Path to the `.py` file to run.

    Returns:
        tuple: `(True, None)` if the file ran successfully, or
            `(False, error_message)` if it failed, where
            `error_message` (str) describes what went wrong.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_py_file_safe

            success, error = run_py_file_safe("script.py")
            if not success:
                print(f"Couldn't run the file: {error}")
            ```

        === "The Traditional Way"
            ```python
            import runpy

            print("RUNNING: script.py")
            try:
                runpy.run_path("script.py", run_name="__main__")
            except Exception as e:
                print(f"Couldn't run the file: {e}")
            ```
    """
    print(f"RUNNING: {filename}")
    try:
        runpy.run_path(filename, run_name="__main__")
        return True, None
    except Exception as e:
        return False, str(e)


def time_function_call(function, args: list | None = None) -> float:
    """
    Runs a function once and returns how long it took to run, in
    seconds, using a monotonic performance counter.

    Raises EasyFlowError if the function raises an exception while
    running.

    Args:
        function: The function to run and time.
        args (list, optional): Positional arguments to pass to the
            function. Leave as None to call it with no arguments.

    Returns:
        float: Number of seconds the function took to run.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import time_function_call

            def add(a, b):
                return a + b

            time_function_call(add, [2, 3])  # -> 0.000002
            ```

        === "The Traditional Way"
            ```python
            import time

            def add(a, b):
                return a + b

            start = time.perf_counter()
            try:
                add(2, 3)
            except Exception as e:
                print(f"Couldn't time the function: {e}")
            duration = time.perf_counter() - start
            ```
    """
    try:
        start = time.perf_counter()
        if args is None:
            function()
        else:
            function(*args)
        return time.perf_counter() - start
    except Exception as e:
        raise EasyFlowError(f"\n\n\nERROR: {e}") from None


def time_it(func):
    """
    Decorator that measures how long a function takes to run,
    prints the elapsed time, and returns the original result.
    Uses a monotonic performance counter so clock adjustments do not
    change the measured duration.
    Preserves the original function's name, docstring, and inspectable
    signature, so documentation and introspection still describe `func`.

    Args:
        func (callable): The function to decorate.

    Returns:
        callable: A wrapped version of `func` that behaves the same
            but prints its runtime each time it's called.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import time_it

            @time_it
            def add(a, b):
                return a + b

            add(2, 3)  # prints: add took 0.00s
            ```

        === "The Traditional Way"
            ```python
            import time

            def add(a, b):
                return a + b

            start = time.perf_counter()
            result = add(2, 3)
            elapsed = time.perf_counter() - start
            print(f"add took {elapsed:.2f}s")
            ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.2f}s")
        return result

    return wrapper


def retry(func, attempts=3, delay=1):
    """
    Calls a function, automatically retrying it if it raises an exception
    up to a specified number of attempts, with a pause between tries.

    Args:
        func (callable): The function to execute.
        attempts (int, optional): Maximum number of times to try running
            the function. Defaults to 3.
        delay (int or float, optional): Time to wait in seconds between
            failed attempts. Defaults to 1.

    Returns:
        Any: The return value of `func` if it succeeds.

    Raises:
        Exception: The last exception raised by `func` if all attempts fail.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import retry

            def flaky_api():
                # Might fail sometimes
                pass

            result = retry(flaky_api, attempts=5, delay=2)
            ```

        === "The Traditional Way"
            ```python
            import time

            def flaky_api():
                pass

            attempts = 5
            delay = 2
            for i in range(attempts):
                try:
                    result = flaky_api()
                    break
                except Exception as e:
                    if i == attempts - 1:
                        raise e
                    time.sleep(delay)
            ```
    """
    # loop from 1 up to attempts (max 3)
    for i in range(attempts):
        try:
            result = func()
            return result
        except Exception:
            if i == attempts - 1:
                raise
            time.sleep(delay)
    return None


def run_py_string(code_string: str) -> None:
    """
    Executes a string of Python code in the current global scope,
    saving you from writing temporary file creation boilerplate.

    Args:
        code_string (str): Valid Python code as a string to execute.

    Returns:
        None

    Raises:
        EasyFlowError: If executing the code string raises an exception.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_py_string

            run_py_string("print('Hello from string!')")
            ```

        === "The Traditional Way"
            ```python
            try:
                exec("print('Hello from string!')")
            except Exception as e:
                print(f"Execution failed: {e}")
            ```
    """
    try:
        exec(code_string)
    except Exception as e:
        raise EasyFlowError(f"\n\n\nERROR: {e}") from None


def run_with_fallback(func, default_value, *args, **kwargs):
    """
    Executes a function and returns its result, or returns a default
    fallback value if an exception is raised.

    Args:
        func (callable): The function to execute.
        default_value (Any): The value to return if the function fails.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Any: The function's return value or the default fallback value.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_with_fallback

            result = run_with_fallback(int, 0, "not_a_number")
            print(result)  # -> 0
            ```

        === "The Traditional Way"
            ```python
            try:
                result = int("not_a_number")
            except Exception:
                result = 0
            print(result)  # -> 0
            ```
    """
    try:
        return func(*args, **kwargs)
    except Exception:
        return default_value


def run_with_delay(delay: float | int, func, *args, **kwargs):
    """
    Waits for a specified number of seconds before executing a function
    and returning its result.

    Args:
        delay (int or float): Time to wait in seconds before running the function.
        func (callable): The function to execute.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Any: The return value of `func`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_with_delay

            result = run_with_delay(1, print, "Hello after 1 second!")
            ```

        === "The Traditional Way"
            ```python
            import time

            time.sleep(1)
            result = print("Hello after 1 second!")
            ```
    """
    time.sleep(delay)
    return func(*args, **kwargs)


def run_if(condition: bool, func, *args, default_value=None, **kwargs):
    """
    Runs a function only when a condition is true.

    Args:
        condition (bool): Whether to run the function.
        func (callable): The function to execute when condition is True.
        *args: Positional arguments to pass to the function.
        default_value (Any, optional): Value to return when condition is
            False. Defaults to None.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Any: The function's return value when condition is True, or the
            default value when condition is False.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import run_if

            result = run_if(True, max, 3, 8)  # -> 8
            skipped = run_if(False, max, 3, 8, default_value=0)  # -> 0
            ```

        === "The Traditional Way"
            ```python
            if should_run:
                result = max(3, 8)
            else:
                result = 0
            ```
    """
    if condition:
        return func(*args, **kwargs)

    return default_value


def wait_until(condition, timeout: float | int = 5, interval: float | int = 0.1) -> bool:
    """
    Waits until a condition function returns True, or until a timeout
    is reached.

    Args:
        condition (callable): A function that returns True when the
            waiting should stop.
        timeout (int or float, optional): Maximum number of seconds to
            wait. Defaults to `5`.
        interval (int or float, optional): Seconds to wait between
            checks. Defaults to `0.1`.

    Returns:
        bool: True if the condition became true before the timeout,
            otherwise False.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import wait_until

            ready = wait_until(lambda: file_exists("report.csv"), timeout=10)
            ```

        === "The Traditional Way"
            ```python
            import time

            start = time.time()
            ready = False
            while time.time() - start < 10:
                if file_exists("report.csv"):
                    ready = True
                    break
                time.sleep(0.1)
            ```
    """
    start = time.time()

    while time.time() - start < timeout:
        if condition():
            return True
        time.sleep(interval)

    return bool(condition())
