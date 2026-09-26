"""
easy_async is built to simplify asynchronous code execution.
"""

import asyncio


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


async def run_at_the_same_time_no_params(functions: list) -> list:
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
            import asyncio
            from py_simple import run_at_the_same_time_no_params

            def add():
                return 1 + 1

            def sub():
                return 4 - 2

            async def main():
                return await run_at_the_same_time_no_params([add, sub])

            asyncio.run(main())  # -> [("add", 2), ("sub", 2)]
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def add():
                return 1 + 1

            def sub():
                return 4 - 2

            async def main():
                loop = asyncio.get_running_loop()
                functions = [add, sub]
                tasks = [loop.run_in_executor(None, f) for f in functions]
                results = await asyncio.gather(*tasks)
                return list(zip((f.__name__ for f in functions), results))

            asyncio.run(main())
            ```
    """
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, function) for function in functions]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise EasyAsyncError(f"\n\n\nERROR: {result}") from None
    return list(zip((f.__name__ for f in functions), results))


async def run_at_the_same_time_with_params(functions_and_args: list[tuple]) -> list:
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
            import asyncio
            from py_simple import run_at_the_same_time_with_params

            def add(a, b):
                return a + b

            def sub(a, b):
                return a - b

            async def main():
                return await run_at_the_same_time_with_params([
                    (add, 1, 1),
                    (sub, 4, 2),
                ])

            asyncio.run(main())  # -> [("add", 2), ("sub", 2)]
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def add(a, b):
                return a + b

            def sub(a, b):
                return a - b

            async def main():
                loop = asyncio.get_running_loop()
                functions_and_args = [(add, 1, 1), (sub, 4, 2)]
                tasks = [
                    loop.run_in_executor(None, item[0], *item[1:])
                    for item in functions_and_args
                ]
                results = await asyncio.gather(*tasks)
                names = [item[0].__name__ for item in functions_and_args]
                return list(zip(names, results))

            asyncio.run(main())
            ```
    """
    loop = asyncio.get_running_loop()
    tasks = [
        loop.run_in_executor(None, items[0], *items[1:])
        for items in functions_and_args
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise EasyAsyncError(f"\n\n\nERROR: {result}") from None
    names = [items[0].__name__ for items in functions_and_args]
    return list(zip(names, results))


async def run_with_timeout(func, timeout: float, *args) -> tuple:
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
            import asyncio
            from py_simple import run_with_timeout

            def slow_add(a, b):
                return a + b

            async def main():
                return await run_with_timeout(slow_add, 2.0, 3, 5)

            asyncio.run(main())  # -> ("slow_add", 8)
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def slow_add(a, b):
                return a + b

            async def main():
                loop = asyncio.get_running_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, slow_add, 3, 5),
                    timeout=2.0,
                )
                return (slow_add.__name__, result)

            asyncio.run(main())
            ```
    """
    loop = asyncio.get_running_loop()
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(None, func, *args),
            timeout=timeout,
        )
        return (func.__name__, result)
    except Exception as e:
        raise EasyAsyncError(f"\n\n\nERROR: {e}") from None


async def run_concurrent_map(func, items: list) -> list:
    """
    Applies a function to a list of items concurrently and returns the
    results in the original order.

    Raises EasyAsyncError if any function call raises an exception.

    Args:
        func (callable): The function to call on each item.
        items (list): The list of items to pass one by one into the function.

    Returns:
        list: The list of return values in the same order as items.

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_concurrent_map

            def square(n):
                return n * n

            async def main():
                return await run_concurrent_map(square, [1, 2, 3, 4])

            asyncio.run(main())  # -> [1, 4, 9, 16]
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def square(n):
                return n * n

            async def main():
                loop = asyncio.get_running_loop()
                items = [1, 2, 3, 4]
                tasks = [loop.run_in_executor(None, square, item) for item in items]
                return await asyncio.gather(*tasks)

            asyncio.run(main())
            ```
    """
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, func, item) for item in items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise EasyAsyncError(f"\n\n\nERROR: {result}") from None
    return results


async def run_with_retry(func, attempts: int, delay: float, *args) -> tuple:
    """
    Runs a function repeatedly until it succeeds or all attempts are
    exhausted, waiting between attempts.

    Raises EasyAsyncError if every attempt fails.

    Args:
        func (callable): The function to execute.
        attempts (int): Number of attempts to make before giving up.
        delay (float): Time to wait between failed attempts, in seconds.
        *args: Positional arguments to pass to the function.

    Returns:
        tuple: A tuple containing `(func.__name__, result)`.

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_with_retry

            def add(a, b):
                return a + b

            async def main():
                return await run_with_retry(add, 4, 2.0, 2, 3)

            asyncio.run(main())  # -> ("add", 5)
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def add(a, b):
                return a + b

            async def main():
                loop = asyncio.get_running_loop()
                attempts = 4
                for attempt in range(attempts):
                    try:
                        result = await loop.run_in_executor(None, add, 2, 3)
                        return (add.__name__, result)
                    except Exception as e:
                        if attempt == attempts - 1:
                            raise EasyAsyncError(f"\n\n\nERROR: {e}") from None
                        await asyncio.sleep(2.0)

            asyncio.run(main())
            ```
    """
    loop = asyncio.get_running_loop()
    for attempt in range(attempts):
        try:
            result = await loop.run_in_executor(None, func, *args)
            return (func.__name__, result)
        except Exception as e:
            if attempt == attempts - 1:
                raise EasyAsyncError(f"\n\n\nERROR: {e}") from None
            await asyncio.sleep(delay)
