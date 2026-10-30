# Easy Async

Running multiple tasks at the same time can make programs faster and more efficient. Whether you're processing data, running independent operations, or automating tasks, `easy_async` provides simple helpers that make asynchronous execution easier to understand and use.

## A small real-world example

Imagine you are building a tool that needs to perform several independent calculations. Instead of waiting for each function to finish one by one, you want to run them at the same time.

```python
from py_simple import run_at_the_same_time_no_params


def download_file():
    return "File downloaded"


def update_database():
    return "Database updated"


results = run_at_the_same_time_no_params(
    [
        download_file,
        update_database,
    ]
)

print(results)
```

Example output:

```text
[
    ('download_file', 'File downloaded'),
    ('update_database', 'Database updated')
]
```

## What happened?

`run_at_the_same_time_no_params()` runs multiple functions at the same time when they do not need any arguments.

It uses a thread pool internally to execute each function independently and collects all the results in a simple list.

If your functions need arguments, you can use:

```python
from py_simple import run_at_the_same_time_with_params


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


results = run_at_the_same_time_with_params(
    [
        (add, 2, 3),
        (multiply, 4, 5),
    ]
)

print(results)
```

Example output:

```text
[
    ('add', 5),
    ('multiply', 20)
]
```

`run_at_the_same_time_with_params()` allows every function to receive its own arguments while still running all tasks together.

## Limit concurrent map jobs

Use `run_concurrent_map_limited()` when you want to process a list without
submitting every item at once. It runs ordinary synchronous callbacks in
the event loop's executor and returns results in input order.

```python
import asyncio
from py_simple import run_concurrent_map_limited


def square(number):
    return number * number


async def main():
    return await run_concurrent_map_limited(square, [1, 2, 3, 4], 2)


print(asyncio.run(main()))  # [1, 4, 9, 16]
```

The final argument is the maximum number of submitted jobs at once. It
must be a positive integer, excluding booleans. A limit of one processes
items one at a time; a larger limit still uses only as many workers as
there are items. The executor may run fewer jobs than the chosen limit.
Empty input returns `[]`. Async callbacks are not supported.

An invalid limit or an ordinary callback failure raises `EasyAsyncError`.
If a callback fails, the other items are still attempted and all workers
are awaited; the first error in input order is then reported. Side effects
from successful calls are not rolled back.

Cancelling the await propagates `asyncio.CancelledError` and stops the
internal workers from submitting more items. It cannot forcibly terminate
an already running Python thread; those callbacks may finish later. When
using `asyncio.run()`, its executor shutdown can wait for those threads.

## Return the first completed result

Use `run_first_completed()` to run multiple zero-argument functions concurrently and get the result of whichever finishes first:

```python
import asyncio
import time
from py_simple import run_first_completed


def query_primary():
    return "primary data"


def query_mirror():
    time.sleep(0.05)
    return "mirror data"


async def main():
    return await run_first_completed([query_primary, query_mirror])


print(asyncio.run(main()))  # ("query_primary", "primary data")
```

In this example, `query_primary` returns immediately while `query_mirror` has a short delay, so `query_primary` finishes first.

Once the first function completes, all other pending tasks are cancelled. Note that cancelling an asyncio task cannot forcibly terminate an already running thread in Python's thread pool; those callbacks may complete in the background. If the first completed function raises an exception, an `EasyAsyncError` is raised.

## Why use these helpers?

Instead of manually creating thread pools and handling results every time, you can simply write:

```python
run_at_the_same_time_no_params(
    [
        task_one,
        task_two,
    ]
)
```

or:

```python
run_at_the_same_time_with_params(
    [
        (task_one, value),
        (task_two, value),
    ]
)
```

These helpers keep asynchronous code simple, readable, and beginner-friendly while providing consistent error handling when tasks fail.
