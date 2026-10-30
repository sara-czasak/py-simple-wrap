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
        list: A list of (name, result) tuples, one per function. Exception
            objects returned by callbacks are preserved as values.

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
    for task, result in zip(tasks, results):
        # Exception instances may also be ordinary callback return values.
        if isinstance(result, Exception) and task.exception() is not None:
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
        list: A list of (name, result) tuples, one per function. Exception
            objects returned by callbacks are preserved as values.

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
        loop.run_in_executor(None, items[0], *items[1:]) for items in functions_and_args
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for task, result in zip(tasks, results):
        # Exception instances may also be ordinary callback return values.
        if isinstance(result, Exception) and task.exception() is not None:
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
        list: The list of return values in the same order as items, including
            exception objects returned (rather than raised) by callbacks.

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
    for task, result in zip(tasks, results):
        # Exception instances may also be ordinary callback return values.
        if isinstance(result, Exception) and task.exception() is not None:
            raise EasyAsyncError(f"\n\n\nERROR: {result}") from None
    return results


async def run_concurrent_map_limited(func, items: list, max_concurrency: int) -> list:
    """
    Applies a synchronous function with a limit on concurrent executor jobs.

    Uses at most `max_concurrency` workers, each submitting one item at a
    time to the event loop's executor. Results keep the input order.
    An ordinary callback error does not stop the remaining items: all
    workers are awaited before the first error in input order is raised.

    Cancelling the await propagates `asyncio.CancelledError` and cancels
    the internal workers so they submit no more items. Already running
    Python threads cannot be forcibly stopped and may finish afterward.

    Args:
        func (callable): Ordinary synchronous function called with each
            item. Async callbacks are not supported.
        items (list): Items passed one by one to `func`.
        max_concurrency (int): Positive maximum number of submitted jobs
            at once. Booleans are not accepted. The executor may run fewer.

    Returns:
        list: Callback results in the same order as `items`, or an empty
            list for empty input.

    Raises:
        EasyAsyncError: If the limit is not a positive integer or a
            callback/executor call raises an ordinary exception.

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_concurrent_map_limited

            def square(number):
                return number * number

            async def main():
                return await run_concurrent_map_limited(square, [1, 2, 3, 4], 2)

            print(asyncio.run(main()))  # [1, 4, 9, 16]
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def square(number):
                return number * number

            async def main():
                loop = asyncio.get_running_loop()
                items = [1, 2, 3, 4]
                results = [None] * len(items)
                work = iter(enumerate(items))

                async def worker():
                    for index, item in work:
                        results[index] = await loop.run_in_executor(None, square, item)

                await asyncio.gather(worker(), worker())
                return results

            print(asyncio.run(main()))  # [1, 4, 9, 16]
            ```
    """
    if (
        isinstance(max_concurrency, bool)
        or not isinstance(max_concurrency, int)
        or max_concurrency < 1
    ):
        raise EasyAsyncError("max_concurrency must be a positive integer.")

    loop = asyncio.get_running_loop()
    results = [None] * len(items)
    work = iter(enumerate(items))
    errors = {}

    async def worker():
        for index, item in work:
            try:
                results[index] = await loop.run_in_executor(None, func, item)
            except Exception as error:
                errors[index] = error

    outcomes = await asyncio.gather(
        *(worker() for _ in range(min(max_concurrency, len(items)))),
        return_exceptions=True,
    )
    for outcome in outcomes:
        if isinstance(outcome, BaseException):
            raise outcome
    if errors:
        raise EasyAsyncError(f"\n\n\nERROR: {errors[min(errors)]}") from None
    return results


async def run_after_delay(func, delay: float, *args) -> tuple:
    """
    Waits asynchronously before running a function.

    Raises EasyAsyncError if the function raises an exception after the
    delay finishes.

    Args:
        func (callable): The function to execute.
        delay (float): Number of seconds to wait before running the function.
        *args: Positional arguments to pass to the function.

    Returns:
        tuple: A tuple containing `(func.__name__, result)`.

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_after_delay

            def greet(name):
                return f"Hello, {name}!"

            async def main():
                return await run_after_delay(greet, 1.0, "Sam")

            asyncio.run(main())  # -> ("greet", "Hello, Sam!")
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def greet(name):
                return f"Hello, {name}!"

            async def main():
                await asyncio.sleep(1.0)
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, greet, "Sam")
                return ("greet", result)
            ```
    """
    try:
        await asyncio.sleep(delay)
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, func, *args)
        return (func.__name__, result)
    except Exception as e:
        raise EasyAsyncError(f"\n\n\nERROR: {e}") from None


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


async def run_periodically(func, interval: float, times: int, *args) -> list:
    """
    Runs the same function repeatedly on a fixed schedule and returns
    the results in order.

    Waits `interval` seconds before each run (including the first),
    runs `func` in a thread pool so it never blocks the event loop, and
    collects one result per run. Raises EasyAsyncError if any run raises
    an exception while running.

    Args:
        func (callable): The function to run, each time with the same
            positional arguments.
        interval (float): Seconds to wait before each run, including
            the first one. Must be greater than 0.
        times (int): How many times to run the function. Must be at
            least 1.
        *args: Positional arguments to pass to func on every run.

    Returns:
        list: One result per run, in the order the runs finished,
            e.g. [4, 4, 4] for a function that returns 2 + 2.

    Raises:
        EasyAsyncError: If a run raises an exception, or if interval or
            times are out of range.

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_periodically

            def add():
                return 2 + 2

            async def main():
                return await run_periodically(add, 1.0, 3)

            asyncio.run(main())  # -> [4, 4, 4]
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def add():
                return 2 + 2

            async def main():
                loop = asyncio.get_running_loop()
                results = []
                for _ in range(3):
                    await asyncio.sleep(1.0)
                    results.append(await loop.run_in_executor(None, add))
                return results

            asyncio.run(main())  # -> [4, 4, 4]
            ```
    """
    if not isinstance(interval, (int, float)) or interval <= 0:
        raise EasyAsyncError(
            f"interval must be a number greater than 0, got {interval!r}"
        )
    if not isinstance(times, int) or times < 1:
        raise EasyAsyncError(f"times must be an integer of at least 1, got {times!r}")

    loop = asyncio.get_running_loop()
    results = []
    for _ in range(times):
        await asyncio.sleep(interval)
        try:
            results.append(await loop.run_in_executor(None, func, *args))
        except Exception as e:
            raise EasyAsyncError(f"\n\n\nERROR: {e}") from None
    return results


async def run_first_completed(functions: list) -> tuple:
    """
    Runs multiple zero-argument functions concurrently and returns the
    result of whichever finishes first.

    Pending tasks are cancelled once the first function completes.
    Note that cancelling an asyncio task does not forcibly terminate
    an already running thread in the thread pool.
    Raises EasyAsyncError if `functions` is empty, contains non-callable
    items, or if the first completed function raises an exception.

    Args:
        functions (list): Functions to run concurrently, each taking no
            arguments. Must be a non-empty list.

    Returns:
        tuple: A tuple containing `(func_name, result)` of the first
            function to finish.

    Raises:
        EasyAsyncError: If `functions` is not a list, is empty, contains
            non-callable elements, or if the first completed function
            raises an exception.

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_first_completed

            def fetch_fast():
                return "quick response"

            def fetch_slow():
                return "slow response"

            async def main():
                return await run_first_completed([fetch_fast, fetch_slow])

            asyncio.run(main())  # -> ("fetch_fast", "quick response")
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def fetch_fast():
                return "quick response"

            def fetch_slow():
                return "slow response"

            async def main():
                loop = asyncio.get_running_loop()
                tasks = [
                    asyncio.ensure_future(loop.run_in_executor(None, f))
                    for f in [fetch_fast, fetch_slow]
                ]
                task_to_fn = {
                    t: f for t, f in zip(tasks, [fetch_fast, fetch_slow])
                }
                try:
                    done, pending = await asyncio.wait(
                        tasks, return_when=asyncio.FIRST_COMPLETED
                    )
                finally:
                    for t in tasks:
                        if not t.done():
                            t.cancel()
                first = next(iter(done))
                return (task_to_fn[first].__name__, first.result())

            asyncio.run(main())
            ```
    """
    if not isinstance(functions, list) or len(functions) == 0:
        raise EasyAsyncError("functions must be a non-empty list of callables")
    for f in functions:
        if not callable(f):
            raise EasyAsyncError(
                f"All items in functions must be callable, got {type(f).__name__}"
            )

    loop = asyncio.get_running_loop()
    task_to_func = {}
    completed_order = []
    for f in functions:
        task = asyncio.ensure_future(loop.run_in_executor(None, f))
        task.add_done_callback(completed_order.append)
        task_to_func[task] = f

    try:
        done, _ = await asyncio.wait(
            task_to_func.keys(), return_when=asyncio.FIRST_COMPLETED
        )
    finally:
        for task in task_to_func:
            if not task.done():
                task.cancel()

    first_task = completed_order[0] if completed_order else next(iter(done))
    func = task_to_func[first_task]
    func_name = getattr(func, "__name__", None)
    if func_name is None:
        func_name = repr(func)
    try:
        result = first_task.result()
        return (func_name, result)
    except Exception as e:
        raise EasyAsyncError(f"\n\n\nERROR: {e}") from None


async def run_with_default(func, fallback, *args) -> tuple:
    """
    Runs a function asynchronously, returning a fallback value if it fails.

    When the function succeeds you get its result; when it raises, you
    get the fallback instead of an exception. Useful for optional work
    where a default is fine, such as reading an optional config file
    or fetching a best-effort value. This is the async counterpart of
    the synchronous `run_with_fallback` in easy_flow: it runs the
    function in an executor and returns a `(name, result)` tuple like
    the other helpers in this module.

    Args:
        func (callable): The function to execute.
        fallback: The value to return if the function raises.
        *args: Positional arguments to pass to the function.

    Returns:
        tuple: A tuple containing `(name, result)` on success
            or `(name, fallback)` on failure, where `name` is
            `func.__name__` when present and `repr(func)` otherwise
            (same approach as `run_first_completed`).

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_with_default

            def read_config():
                raise FileNotFoundError("no config file")

            async def main():
                return await run_with_default(read_config, {"theme": "light"})

            asyncio.run(main())  # -> ("read_config", {"theme": "light"})
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def read_config():
                raise FileNotFoundError("no config file")

            async def main():
                loop = asyncio.get_running_loop()
                try:
                    result = await loop.run_in_executor(None, read_config)
                    return (read_config.__name__, result)
                except Exception:
                    return (read_config.__name__, {"theme": "light"})

            asyncio.run(main())
            ```
    """
    func_name = getattr(func, "__name__", None)
    if func_name is None:
        func_name = repr(func)
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(None, func, *args)
        return (func_name, result)
    except Exception:
        return (func_name, fallback)
