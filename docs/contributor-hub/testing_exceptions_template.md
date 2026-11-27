# Testing Exceptions and Error Handling

Every helper in `py-simple-wrap` is designed to fail gracefully. Instead of letting internal Python tracebacks bubble up to beginners, our modules validate inputs and raise clean, predictable custom exceptions (such as `EasyMoneyError`, `EasyConfigError`, or `EasyArchiveError`).

When you add or update a function, you also need to test that it fails correctly when given invalid arguments. This guide walks you through testing error conditions using `pytest.raises`.

## Copy a working example first

Follow the setup instructions in [CONTRIBUTING.md](../how-to/contributing.md), then save this practice file as `tests/test_exception_demo.py`:

```python
"""Practice test demonstrating exception testing with pytest."""

import pytest

from py_simple_package.src.py_simple.easy_money import (
    EasyMoneyError,
    calculate_discount,
    format_money,
    split_bill,
)


def test_raises_custom_exception():
    """Verify that an invalid input type raises the module's custom exception."""
    with pytest.raises(EasyMoneyError):
        format_money(True)


def test_raises_with_matching_message():
    """Verify that the error message clearly explains the problem."""
    with pytest.raises(EasyMoneyError, match=r"amount must be a number"):
        format_money(True)


def test_inspect_exception_details():
    """Capture exc_info to inspect the exception object and message."""
    with pytest.raises(EasyMoneyError) as exc_info:
        split_bill(100, 0)

    assert "people must be an integer of at least 1" in str(exc_info.value)


@pytest.mark.parametrize("invalid_rate", [-10, 105, 999])
def test_raises_for_multiple_invalid_inputs(invalid_rate):
    """Test boundary checks across multiple invalid inputs."""
    with pytest.raises(EasyMoneyError, match=r"discount rate must be between 0 and 100"):
        calculate_discount(50, invalid_rate)
```

Run the tests with:

```bash
pytest tests/test_exception_demo.py
```

All 6 test cases will pass green. Once you see it work, you can delete `tests/test_exception_demo.py`.

---

## 4 Patterns You Will Use

### 1. Basic Type Check (`pytest.raises`)

Use this when you want to ensure a helper rejects invalid types or missing parameters by raising the right exception:

```python
def test_rejects_non_numeric_input():
    with pytest.raises(EasyMoneyError):
        format_money(True)
```

If the function does *not* raise `EasyMoneyError`, pytest fails the test with `DID NOT RAISE EasyMoneyError`.

### 2. Matching the Error Message (`match=...`)

Checking only the exception type can hide bugs if the function fails for an unexpected reason. Use the `match` parameter to assert that the error text contains the expected keywords:

```python
def test_error_message_is_helpful():
    # The match argument takes a regex or substring pattern
    with pytest.raises(EasyMoneyError, match=r"amount must be a number"):
        format_money(True)
```

If the function raises `EasyMoneyError` with a different message, pytest reports a clear mismatch explaining what regex was expected versus what was received.

### 3. Inspecting the Exception (`as exc_info`)

When an error message is long, multi-line, or contains dynamic details (like file paths or calculated values), bind the exception context with `as exc_info`:

```python
def test_error_details_are_accurate():
    with pytest.raises(EasyMoneyError) as exc_info:
        split_bill(100, 0)

    # exc_info.value is the actual exception instance
    error_message = str(exc_info.value)
    assert "people must be an integer of at least 1" in error_message
```

> **Note**: Place your assertions *after* the `with` block finishes, because `exc_info.value` is only populated once the block exits.

### 4. Testing Multiple Edge Cases (`@pytest.mark.parametrize`)

If a function has boundary conditions (e.g., values must be between 0 and 100, or lists cannot be empty), test several invalid values using parametrization:

```python
@pytest.mark.parametrize("invalid_rate", [-10, -0.01, 100.5, 999])
def test_discount_rate_out_of_bounds(invalid_rate):
    with pytest.raises(EasyMoneyError, match=r"discount rate must be between 0 and 100"):
        calculate_discount(50, invalid_rate)
```

---

## Common Pitfalls to Avoid

- **Do not catch `Exception` or `BaseException`:** Always test against the specific custom exception class defined in the module (e.g., `EasyJsonError`, `EasyArchiveError`, `EasyMoneyError`). Catching generic `Exception` passes even if the function crashes with a `NameError` or `AttributeError`.
- **Keep the `with` block small:** Put only the single line that is supposed to fail inside the `with pytest.raises(...)` block. Setup code belongs before the block so failures in setup don't get swallowed.
- **Remember the `r` prefix for regex:** In `match=r"..."`, special characters like parentheses `(` or brackets `[` are regex symbols. Escape them if needed (e.g., `match=r"invalid option \(foo\)"`).

---

## Where do error tests go?

Add your exception tests to the module's test file under `tests/test_<module_name>.py`. You can either group them into an existing `Test...` class or add a dedicated `test_<function>_errors()` function.
