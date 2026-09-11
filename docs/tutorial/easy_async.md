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