# Testing Async Helpers

An async helper returns a coroutine. Your test must run that coroutine before it
can check the result. The tests in `tests/test_async.py` use ordinary pytest tests
with `asyncio.run()`, so you do not need a separate pytest asyncio plugin.

## Start with this working example

Copy this into `tests/test_async_demo.py`. It checks the result and the requested
delay without waiting half a second each time you run the test.

```python
import asyncio

import pytest

from py_simple.easy_async import EasyAsyncError, run_after_delay


def test_delayed_callback_result(monkeypatch):
    delays = []

    async def fake_sleep(delay):
        delays.append(delay)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    def add(left, right):
        return left + right

    result = asyncio.run(run_after_delay(add, 0.5, 2, 3))

    assert result == ("add", 5)
    assert delays == [0.5]


def test_delayed_callback_error(monkeypatch):
    async def fake_sleep(delay):
        pass

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    def fail():
        raise ValueError("demo failure")

    with pytest.raises(EasyAsyncError, match="demo failure"):
        asyncio.run(run_after_delay(fail, 0.5))
```

From the repository root, after setting up the project as described in
[Contributing](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md):

```bash
python -m pytest tests/test_async_demo.py -q
```

Both tests should pass. For the existing async suite, run:

```bash
python -m pytest tests/test_async.py -q
```

## Fill in your helper's details

| Part of the example | Replace it with |
| --- | --- |
| `run_after_delay` | The async helper you changed |
| `add` and its arguments | A small callback with a predictable result |
| `("add", 5)` | Your helper's documented return value |
| `EasyAsyncError` | The exception your helper promises to raise |
| `asyncio.sleep` | The wait used by your helper, only if replacing it fits the behavior under test |

Keep callbacks synchronous when the helper expects a regular function. Making
`add` an `async def` would return another coroutine rather than the integer this
helper expects.

## Why the fake is also async

The helper uses `await asyncio.sleep(...)`. A regular function that returns
`None` cannot be awaited, so the replacement must be an `async def` too.
`monkeypatch` restores the real sleep when each test ends.

The fake sleep is useful for checking results, requested delays, and errors.
It does **not** prove a timeout or concurrent scheduling works: it does not wait
or yield control. For those cases, use events or queues to coordinate tasks,
with a bounded `asyncio.wait_for(...)` to prevent a test hanging. Avoid assertions
such as “this finished in less than 0.1 seconds”; a busy CI runner can be slower.

## Common mistakes

- **“Coroutine was never awaited”:** wrap the helper call in `asyncio.run(...)`
  before checking its result or expected exception.
- **“asyncio.run() cannot be called from a running event loop”:** keep the pytest
  test a normal `def`. For a larger scenario, put the awaits in an inner
  `async def scenario()` and call `asyncio.run(scenario())` once from the test.
- **Pending tasks after the test:** await tasks you start, and use `try/finally`
  to cancel and await them when a scenario exits early.

For examples of events, queues, ordering, and cancellation, read
[`tests/test_async.py`](https://github.com/sara-czasak/py-simple-wrap/blob/main/tests/test_async.py).
For general fixture cleanup, see [Keeping Tests Isolated](test_isolation_template.md).
