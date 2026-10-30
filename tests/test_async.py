import asyncio
import gc
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from py_simple_package.src.py_simple.easy_async import (
    EasyAsyncError,
    run_at_the_same_time_no_params,
    run_at_the_same_time_with_params,
    run_with_timeout,
    run_concurrent_map,
    run_concurrent_map_limited,
    run_after_delay,
    run_with_retry,
    run_periodically,
    run_first_completed,
    run_with_default,
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


@pytest.mark.parametrize("limit", [1, 2, 10])
def test_limited_map_bounds_running_and_submitted_work(limit, monkeypatch):
    """Blocked callbacks reveal both active work and executor queue growth."""

    async def scenario():
        loop = asyncio.get_running_loop()
        loop.set_default_executor(ThreadPoolExecutor(max_workers=8))
        started = asyncio.Event()
        release = threading.Event()
        lock = threading.Lock()
        items = list(range(5))
        target = min(limit, len(items))
        active = 0
        peak = 0
        seen = []
        submitted = []
        original_submit = loop.run_in_executor

        def tracked_submit(executor, func, *args):
            future = original_submit(executor, func, *args)
            submitted.append(future)
            assert sum(not future.done() for future in submitted) <= limit
            return future

        monkeypatch.setattr(loop, "run_in_executor", tracked_submit)

        def double(item):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
                seen.append(item)
                if active == target:
                    loop.call_soon_threadsafe(started.set)
            try:
                assert release.wait(5), "test failed to release callbacks"
                return item * 2
            finally:
                with lock:
                    active -= 1

        task = asyncio.create_task(run_concurrent_map_limited(double, items, limit))
        try:
            await asyncio.wait_for(started.wait(), 5)
            await asyncio.sleep(0)
            assert not task.done()
            assert active == target
            assert len(submitted) == target
        finally:
            release.set()

        assert await asyncio.wait_for(task, 5) == [0, 2, 4, 6, 8]
        assert peak == target
        assert active == 0
        assert sorted(seen) == items
        assert len(submitted) == len(items)

    asyncio.run(scenario())


def test_limited_map_keeps_input_order_with_out_of_order_completion(monkeypatch):
    """Each callback is released separately to control completion order."""

    async def scenario():
        loop = asyncio.get_running_loop()
        loop.set_default_executor(ThreadPoolExecutor(max_workers=3))
        gates = [threading.Event() for _ in range(3)]
        started = asyncio.Queue()
        finished = asyncio.Queue()
        original_submit = loop.run_in_executor

        def tracked_submit(executor, func, item):
            future = original_submit(executor, func, item)
            future.add_done_callback(lambda _: finished.put_nowait(item))
            return future

        monkeypatch.setattr(loop, "run_in_executor", tracked_submit)

        def label(item):
            loop.call_soon_threadsafe(started.put_nowait, item)
            assert gates[item].wait(5), "test failed to release callback"
            return f"item {item}"

        task = asyncio.create_task(run_concurrent_map_limited(label, [0, 1, 2], 3))
        try:
            observed = [await asyncio.wait_for(started.get(), 5) for _ in range(3)]
            assert sorted(observed) == [0, 1, 2]
            for item in [2, 0, 1]:
                gates[item].set()
                assert await asyncio.wait_for(finished.get(), 5) == item
            assert await asyncio.wait_for(task, 5) == ["item 0", "item 1", "item 2"]
        finally:
            for gate in gates:
                gate.set()

    asyncio.run(scenario())


def test_limited_map_empty_input_submits_nothing(monkeypatch):
    async def scenario():
        def unexpected_submit(*args):
            pytest.fail("empty input submitted executor work")

        monkeypatch.setattr(
            asyncio.get_running_loop(), "run_in_executor", unexpected_submit
        )
        assert await run_concurrent_map_limited(lambda item: item, [], 2) == []

    asyncio.run(scenario())


@pytest.mark.parametrize("limit", [0, -1, True, False, 1.0, 1.5, "2", None, [], {}])
def test_limited_map_rejects_invalid_limit_before_work(limit):
    def unexpected_callback(item):
        pytest.fail("invalid limit called callback")

    with pytest.raises(
        EasyAsyncError, match="max_concurrency must be a positive integer"
    ):
        asyncio.run(run_concurrent_map_limited(unexpected_callback, [1], limit))


def test_limited_map_waits_for_all_items_and_reports_first_input_error():
    """An error finishing first must not replace an earlier input's error."""

    async def scenario():
        loop = asyncio.get_running_loop()
        loop.set_default_executor(ThreadPoolExecutor(max_workers=2))
        second_failed = threading.Event()
        seen = []
        contexts = []
        loop.set_exception_handler(lambda _, context: contexts.append(context))

        def work(item):
            seen.append(item)
            if item == 0:
                assert second_failed.wait(5)
                raise ValueError("first input failed")
            if item == 1:
                second_failed.set()
                raise RuntimeError("second input failed")
            return item * 2

        with pytest.raises(EasyAsyncError, match="first input failed") as exc_info:
            await asyncio.wait_for(run_concurrent_map_limited(work, [0, 1, 2, 3], 2), 5)

        assert exc_info.value.__cause__ is None
        assert sorted(seen) == [0, 1, 2, 3]
        assert asyncio.all_tasks() == {asyncio.current_task()}
        gc.collect()
        await asyncio.sleep(0)
        assert contexts == []

    asyncio.run(scenario())


def test_limited_map_preserves_none_and_exception_return_values():
    error_value = ValueError("returned rather than raised")
    items = [None, error_value, {"value": 3}]
    results = asyncio.run(run_concurrent_map_limited(lambda item: item, items, 2))
    assert all(actual is expected for actual, expected in zip(results, items))


def test_limited_map_wraps_executor_submission_failure(monkeypatch):
    async def scenario():
        submitted = []

        def broken_submit(executor, func, item):
            submitted.append(item)
            raise RuntimeError("executor unavailable")

        monkeypatch.setattr(
            asyncio.get_running_loop(), "run_in_executor", broken_submit
        )
        with pytest.raises(EasyAsyncError, match="executor unavailable"):
            await run_concurrent_map_limited(str, [1, 2, 3], 2)
        assert submitted == [1, 2, 3]

    asyncio.run(scenario())


def test_limited_map_cancellation_stops_submission_and_observes_late_failure():
    """Cancellation finishes wrappers while real worker threads may continue."""

    async def scenario():
        loop = asyncio.get_running_loop()
        loop.set_default_executor(ThreadPoolExecutor(max_workers=2))
        started = asyncio.Event()
        finished = asyncio.Event()
        release = threading.Event()
        lock = threading.Lock()
        contexts = []
        seen = []
        active = 0
        completed = 0
        loop.set_exception_handler(lambda _, context: contexts.append(context))

        def work(item):
            nonlocal active, completed
            with lock:
                seen.append(item)
                active += 1
                if active == 2:
                    loop.call_soon_threadsafe(started.set)
            try:
                assert release.wait(5), "test failed to release callbacks"
                if item == 0:
                    raise ValueError("late thread failure")
                return item
            finally:
                with lock:
                    active -= 1
                    completed += 1
                    if completed == 2:
                        loop.call_soon_threadsafe(finished.set)

        task = asyncio.create_task(run_concurrent_map_limited(work, list(range(10)), 2))
        try:
            await asyncio.wait_for(started.wait(), 5)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert task.cancelled()
            assert active == 2
            assert sorted(seen) == [0, 1]
            assert asyncio.all_tasks() == {asyncio.current_task()}
        finally:
            release.set()

        await asyncio.wait_for(finished.wait(), 5)
        await asyncio.sleep(0)
        gc.collect()
        await asyncio.sleep(0)
        assert sorted(seen) == [0, 1]
        assert active == 0
        assert contexts == []

    asyncio.run(scenario())


def test_limited_map_propagates_callback_cancelled_error():
    def cancelled(item):
        raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(run_concurrent_map_limited(cancelled, [1], 1))


def test_limited_map_public_imports():
    from py_simple import run_concurrent_map_limited as public_map
    from py_simple.easy_async import run_concurrent_map_limited as module_map

    assert public_map is module_map
    assert asyncio.run(public_map(abs, [-2, 1, -3], 2)) == [2, 1, 3]


def test_run_after_delay_success(monkeypatch):
    async def instant_sleep(delay):
        assert delay == 0.5

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def add(a, b):
        return a + b

    result = asyncio.run(run_after_delay(add, 0.5, 2, 3))

    assert result == ("add", 5)


def test_run_after_delay_wraps_function_error(monkeypatch):
    async def instant_sleep(delay):
        assert delay == 0.1

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def fail():
        raise ValueError("broken")

    with pytest.raises(EasyAsyncError, match="broken"):
        asyncio.run(run_after_delay(fail, 0.1))


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


def test_run_periodically_success(monkeypatch):
    slept = []

    async def fake_sleep(delay):
        slept.append(delay)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    def add():
        return 2 + 2

    result = asyncio.run(run_periodically(add, 0.5, 3))

    assert result == [4, 4, 4]
    assert slept == [0.5, 0.5, 0.5]


def test_run_periodically_passes_args_every_run(monkeypatch):
    async def instant_sleep(delay):
        pass

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def add(a, b):
        return a + b

    result = asyncio.run(run_periodically(add, 0.1, 2, 3, 4))

    assert result == [7, 7]


def test_run_periodically_single_run(monkeypatch):
    async def instant_sleep(delay):
        pass

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def greet():
        return "hi"

    result = asyncio.run(run_periodically(greet, 0.1, 1))

    assert result == ["hi"]


def test_run_periodically_error(monkeypatch):
    async def instant_sleep(delay):
        pass

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)

    def fail():
        raise ValueError("Something went wrong")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_periodically(fail, 0.1, 3))


def test_run_periodically_invalid_interval():
    def add():
        return 2 + 2

    with pytest.raises(EasyAsyncError, match="interval"):
        asyncio.run(run_periodically(add, 0, 3))

    with pytest.raises(EasyAsyncError, match="interval"):
        asyncio.run(run_periodically(add, -1.0, 3))


def test_run_periodically_invalid_times():
    def add():
        return 2 + 2

    with pytest.raises(EasyAsyncError, match="times"):
        asyncio.run(run_periodically(add, 0.5, 0))

    with pytest.raises(EasyAsyncError, match="times"):
        asyncio.run(run_periodically(add, 0.5, -2))


def test_run_first_completed_fastest_wins():
    def slow_func():
        time.sleep(0.3)
        return "slow"

    def fast_func():
        return "fast"

    name, result = asyncio.run(run_first_completed([slow_func, fast_func]))
    assert name == "fast_func"
    assert result == "fast"


def test_run_first_completed_single_func():
    def only_func():
        return 42

    name, result = asyncio.run(run_first_completed([only_func]))
    assert name == "only_func"
    assert result == 42


def test_run_first_completed_first_raises_error():
    def slow_func():
        time.sleep(0.3)
        return "slow"

    def fast_error():
        raise ValueError("instant failure")

    with pytest.raises(EasyAsyncError):
        asyncio.run(run_first_completed([slow_func, fast_error]))


def test_run_first_completed_empty_list():
    with pytest.raises(EasyAsyncError, match="non-empty list"):
        asyncio.run(run_first_completed([]))


def test_run_first_completed_invalid_type():
    with pytest.raises(EasyAsyncError, match="non-empty list"):
        asyncio.run(run_first_completed("not a list"))


def test_run_first_completed_non_callable():
    def valid_func():
        return 1

    with pytest.raises(EasyAsyncError, match="must be callable"):
        asyncio.run(run_first_completed([valid_func, "not callable"]))


def test_run_first_completed_public_import():
    from py_simple import run_first_completed as public_runner
    from py_simple.easy_async import run_first_completed as module_runner

    assert public_runner is module_runner


def test_run_first_completed_callable_object():
    class CallableObj:
        def __call__(self):
            return "from_object"

        def __repr__(self):
            return "CallableObj()"

    name, result = asyncio.run(run_first_completed([CallableObj()]))
    assert name == "CallableObj()"
    assert result == "from_object"


def test_run_first_completed_bad_repr_with_name():
    class BadReprCallable:
        __name__ = "custom_func"

        def __call__(self):
            return 99

        def __repr__(self):
            raise RuntimeError("broken repr")

    name, result = asyncio.run(run_first_completed([BadReprCallable()]))
    assert name == "custom_func"
    assert result == 99



def test_run_first_completed_outer_cancellation():
    async def scenario():
        def slow_one():
            time.sleep(0.5)
            return "slow1"

        def slow_two():
            time.sleep(0.5)
            return "slow2"

        task = asyncio.create_task(run_first_completed([slow_one, slow_two]))
        await asyncio.sleep(0.01)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(scenario())


def test_run_with_default_returns_result_on_success():
    def add(a, b):
        return a + b

    assert asyncio.run(run_with_default(add, 0, 2, 3)) == ("add", 5)


def test_run_with_default_returns_fallback_on_failure():
    def failing():
        raise ValueError("Something went wrong")

    assert asyncio.run(run_with_default(failing, "default")) == (
        "failing",
        "default",
    )


def test_run_with_default_passes_args_and_keeps_name():
    def greet(name):
        raise RuntimeError("no greeting available")

    assert asyncio.run(run_with_default(greet, "hello", "world")) == (
        "greet",
        "hello",
    )


def test_run_with_default_uses_repr_for_callables_without_name():
    from functools import partial

    def add(a, b):
        return a + b

    adder = partial(add, 2)
    assert asyncio.run(run_with_default(adder, 0, 3)) == (repr(adder), 5)


def test_run_with_default_fallback_uses_repr_for_callables_without_name():
    from functools import partial

    def failing(a):
        raise ValueError("boom")

    failer = partial(failing, 1)
    assert asyncio.run(run_with_default(failer, "default")) == (
        repr(failer),
        "default",
    )


@pytest.mark.parametrize("runner", ["no_params", "with_params", "map"])
@pytest.mark.parametrize("raises_later", [False, True])
def test_concurrent_helpers_distinguish_returned_and_raised_exceptions(runner, raises_later):
    returned_error = ValueError("returned as data")

    def return_error(*args):
        return returned_error

    def second_result(*args):
        if raises_later:
            raise RuntimeError("actually raised")
        return "ok"

    def mapped(index):
        return return_error() if index == 0 else second_result()

    async def run():
        if runner == "no_params":
            return await run_at_the_same_time_no_params([return_error, second_result])
        if runner == "with_params":
            return await run_at_the_same_time_with_params([(return_error, 1), (second_result, 2)])
        return await run_concurrent_map(mapped, [0, 1])

    if raises_later:
        with pytest.raises(EasyAsyncError, match="actually raised"):
            asyncio.run(run())
    else:
        results = asyncio.run(run())
        values = results if runner == "map" else [value for _, value in results]
        assert values[0] is returned_error
        assert values[1] == "ok"
