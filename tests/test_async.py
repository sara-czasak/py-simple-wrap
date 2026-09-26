import asyncio

import pytest

from py_simple_package.src.py_simple.easy_async import (
    EasyAsyncError,
    run_at_the_same_time_no_params,
    run_at_the_same_time_with_params,
    run_with_timeout,
    run_concurrent_map,
    run_with_retry,
)


def test_run_at_the_same_time_no_params_error():
    def failing_function():
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_at_the_same_time_no_params([failing_function]))


def test_run_at_the_same_time_no_params():
    def add():
        return 2 + 2

    def multiply():
        return 3 * 3

    result = asyncio.run(run_at_the_same_time_no_params([add, multiply]))

    assert result == [
        ("add", 4),
        ("multiply", 9),
    ]


def test_run_at_the_same_time_with_params():
    def add(a, b):
        return a + b

    def subtract(a, b):
        return a - b

    result = asyncio.run(
        run_at_the_same_time_with_params(
            [
                (add, 5, 3),
                (subtract, 5, 3),
            ]
        )
    )

    assert result == [
        ("add", 8),
        ("subtract", 2),
    ]


def test_run_at_the_same_time_with_params_error():
    def failing_function(value):
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_at_the_same_time_with_params([(failing_function, 10)]))


def test_run_with_timeout_success():
    """It should execute the function with arguments and return its name and result."""

    def sample_func(x):
        return x * 2

    name, result = asyncio.run(run_with_timeout(sample_func, 2.0, 5))
    assert name == "sample_func"
    assert result == 10


def test_run_with_timeout_failure():
    """It should raise EasyAsyncError if execution times out or fails."""
    import time

    def slow_func():
        time.sleep(0.4)
        return True

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_with_timeout(slow_func, 0.1))


def test_run_concurrent_map_success():
    def double(x):
        return x * 2

    inputs = [1, 2, 3, 4, 5]
    results = asyncio.run(run_concurrent_map(double, inputs))
    assert results == [2, 4, 6, 8, 10]


def test_run_concurrent_map_error():
    def divide_hundred_by(x):
        return 100 // x

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_concurrent_map(divide_hundred_by, [10, 5, 0, 2]))


def test_run_with_retry_success():
    def num(n1, n2):
        return n1 + n2

    result = asyncio.run(run_with_retry(num, 4, 2.0, 2, 3))
    assert result == ("num", 5)


def test_run_with_retry_fail():
    def num():
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_with_retry(num, 3, 0.01))
