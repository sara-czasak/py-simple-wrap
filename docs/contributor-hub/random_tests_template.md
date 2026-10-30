# Testing Random Helpers

A random result should not make a test pass only sometimes. Use a controlled
random choice when you need an exact answer, and test properties when any
valid answer is acceptable.

## Copy a working example first

Save this as `tests/test_random_demo.py` while practicing. For a real
contribution, add your cases to the existing `tests/test_random.py` instead.

```python
import pytest

from py_simple_package.src.py_simple import easy_random


@pytest.mark.parametrize("chosen", [1, 6])
def test_roll_dice_includes_both_endpoints(monkeypatch, chosen):
    def fake_randint(start, end):
        assert (start, end) == (1, 6)
        return chosen

    monkeypatch.setattr(easy_random.random, "randint", fake_randint)
    assert easy_random.roll_dice(6) == chosen


@pytest.mark.parametrize("sides", [0, -1])
def test_roll_dice_rejects_invalid_sides_before_drawing(monkeypatch, sides):
    def unexpected_draw(*args):
        pytest.fail("Invalid sides should be rejected before drawing a number")

    monkeypatch.setattr(easy_random.random, "randint", unexpected_draw)
    with pytest.raises(ValueError, match="at least 1 side"):
        easy_random.roll_dice(sides)


def test_shuffle_preserves_items_and_input():
    original = ["moon", "star", "moon"]
    result = easy_random.shuffle_list(original)

    assert sorted(result) == sorted(original)
    assert original == ["moon", "star", "moon"]
    assert result is not original
```

From the repository root, run:

```bash
python -m pytest tests/test_random_demo.py -q
```

This example produces **5 passed**. The first four cases have controlled
outcomes. The shuffle test accepts every valid ordering, including the
original ordering.

## Adapt the example to your helper

1. Replace `easy_random.roll_dice` with the function you are testing.
2. Find the random call inside that function. Here it is
   `random.randint(1, sides)`, so the fake takes `start` and `end`.
3. Replace the expected arguments and chosen results with your own cases.
   Include boundaries such as the smallest and largest allowed result.
4. If bad input should fail before a random call, keep the failing fake in
   the error test. It catches an accidental draw even if the function raises
   the expected error later.

Patch the name where the helper looks it up. This module uses
`import random`, so `easy_random.random.randint` is the right target.
A module using `from random import randint` would instead need its own
`randint` attribute patched.

`monkeypatch` restores the original attribute after each test, including
when the test fails. Avoid assigning a fake directly and forgetting to
restore it. Here the patched `random` module is shared, so keep each test
focused and avoid calling unrelated random helpers while the fake is active.

## Check what must stay true

The shuffle example does not choose a fixed ordering. It checks three
promises: the same items are present, the original list is unchanged, and
the result is a new list. Sorting also preserves duplicate counts; a set
comparison would miss a lost duplicate.

Do not assert that a shuffled list always changes order, that two rolls
must differ, or that ten flips must contain both coin faces. Those can fail
with perfectly valid randomness. Repeating the test until it passes hides
the problem.

A fixed seed is useful for reproducing a local experiment, but hard-coded
sequences can depend on Python's random helper implementation and earlier
calls. For a wrapper's exact behavior, the controlled fake is more direct.
These tests check the helper's contract; they do not measure statistical
fairness or cryptographic security.

## Before opening your PR

Run your module's tests and the repository's pinned hooks, as shown in the
[Pre-commit Guide](pre_commit_template.md). For more on parametrized inputs
and errors, see the [Testing Tutorial](tests_template.md). For fake HTTP
responses, use the separate [Network Test Template](network_tests_template.md).
