"""
easy_flow is built to simplify work flows
"""

import runpy
import time


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
                runpy.run_path("script.py")
            except Exception as e:
                print(f"Couldn't run the file: {e}")
            ```
    """
    print(f"RUNNING: {filename}")
    try:
        runpy.run_path(filename)
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
                runpy.run_path("script.py")
            except Exception as e:
                print(f"Couldn't run the file: {e}")
            ```
    """
    print(f"RUNNING: {filename}")
    try:
        runpy.run_path(filename)
        return True, None
    except Exception as e:
        return False, str(e)


def time_function_call(function, args: list | None = None) -> float:
    """
    Runs a function once and returns how long it took to run, in
    seconds.

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

            start = time.time()
            try:
                add(2, 3)
            except Exception as e:
                print(f"Couldn't time the function: {e}")
            duration = time.time() - start
            ```
    """
    try:
        start = time.time()
        if args is None:
            function()
        else:
            function(*args)
        return time.time() - start
    except Exception as e:
        raise EasyFlowError(f"\n\n\nERROR: {e}") from None


def time_it(func):
    """
    Decorator that measures how long a function takes to run,
    prints the elapsed time, and returns the original result.

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

            start = time.time()
            result = add(2, 3)
            elapsed = time.time() - start
            print(f"add took {elapsed:.2f}s")
            ```
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
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
