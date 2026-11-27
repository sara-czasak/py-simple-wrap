# Parametrized Tests Guide

A test should verify your helper against normal inputs, edge cases (zero, empty values, boundaries), and invalid inputs that trigger error handling. Instead of writing separate test functions for every single input—or grouping multiple assertions into one function where the first failure stops the rest—use pytest's `@pytest.mark.parametrize`.

## Copy a working example first

Save this as `tests/test_parametrize_demo.py` while practicing. For a real contribution, add your cases to the matching module's test file in `tests/` instead.

```python
import pytest

from py_simple_package.src.py_simple.easy_money import (
    EasyMoneyError,
    format_money,
)


@pytest.mark.parametrize(
    ("amount", "symbol", "expected"),
    [
        (12.5, "$", "$12.50"),
        ("3", "€", "€3.00"),
        (0, "$", "$0.00"),
        ("100.999", "£", "£101.00"),
    ],
)
def test_format_money_valid_cases(amount, symbol, expected):
    """Normal values and boundary rounding produce formatted currency strings."""
    assert format_money(amount, symbol=symbol) == expected


@pytest.mark.parametrize(
    "bad_amount",
    [
        "not_a_number",
        True,
        None,
        [10],
    ],
)
def test_format_money_rejects_invalid_types(bad_amount):
    """Non-numeric and boolean values raise an EasyMoneyError."""
    with pytest.raises(EasyMoneyError):
        format_money(bad_amount)


@pytest.mark.parametrize(
    ("amount", "expected_ending"),
    [
        (10, ".00"),
        (10.5, ".50"),
        (10.55, ".55"),
    ],
    ids=["integer", "one-decimal", "two-decimals"],
)
def test_format_money_decimal_precision(amount, expected_ending):
    """Custom IDs help identify which precision variant failed."""
    result = format_money(amount)
    assert result.endswith(expected_ending)
```

From the repository root, run:

=== "Using uv"
    ```bash
    uv run pytest tests/test_parametrize_demo.py -v
    ```

=== "Using pip"
    ```bash
    python -m pytest tests/test_parametrize_demo.py -v
    ```

You should see **11 passed**. Pytest treats each row in the parameter list as its own independent test run. Remove the practice file afterward.

## Fill in the parts for your helper

| Part | Replace it with |
| --- | --- |
| `easy_money` and `format_money` | The module and helper function you are testing. |
| `("amount", "symbol", "expected")` | The argument names passed to your test function. Match the tuple order with each row below. |
| `[ (12.5, "$", "$12.50"), ... ]` | The test table: rows of tuples containing input arguments and the expected return value. |
| `"bad_amount"` | Single parameter name (as a string) when testing only one variable across multiple values. |
| `EasyMoneyError` | The specific exception class your helper raises on invalid input (see [Custom Exception Template](error_template.md)). |
| `ids=[...]` | Optional readable labels for each row, making failure logs easy to pinpoint without checking raw values. |

## Why parametrize instead of loops or multiple asserts?

### 1. Isolated failure reporting
When you place multiple `assert` statements in a single test function:

```python
# Avoid this pattern:
def test_format_money_multiple():
    assert format_money(12.5) == "$12.50"
    assert format_money(0) == "$0.00"      # If this fails...
    assert format_money("3") == "$3.00"    # ...this never runs!
```

If the second assertion fails, execution stops immediately. You will not know whether the third case passed or failed until you fix the second one.

With `@pytest.mark.parametrize`, pytest executes every case independently. If one case fails, all other cases continue running and are reported separately.

### 2. Testing error conditions
Testing invalid inputs requires verifying that the expected exception is raised. A parametrized error test checks every invalid variation:

```python
@pytest.mark.parametrize("invalid_input", ["", None, -5, "abc"])
def test_helper_raises_on_invalid_input(invalid_input):
    with pytest.raises(EasyModuleError):
        my_helper(invalid_input)
```

If you also need to verify specific error messages, you can pass the expected message regex to `match`:

```python
@pytest.mark.parametrize(
    ("bad_input", "error_message"),
    [
        (-1, "must be positive"),
        ("abc", "must be numeric"),
    ],
)
def test_helper_error_messages(bad_input, error_message):
    with pytest.raises(EasyModuleError, match=error_message):
        my_helper(bad_input)
```

### 3. Clear case names with `ids`
By default, pytest names each test variant using its parameter values, e.g.:

```text
tests/test_parametrize_demo.py::test_format_money_valid_cases[12.5-$-12.50] PASSED
```

When parameter values are large strings, complex objects, or floats, auto-generated names can get noisy or hard to read in terminal logs. Pass `ids=[...]` to give each row a concise label:

```python
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  leading and trailing  ", "leading and trailing"),
        ("multiple   spaces   between", "multiple spaces between"),
        ("", ""),
    ],
    ids=["padding", "internal-spaces", "empty-string"],
)
def test_clean_spaces(text, expected):
    assert clean_spaces(text) == expected
```

If the empty string test fails, the output clearly reads:

```text
FAILED tests/...::test_clean_spaces[empty-string] - AssertionError
```

## What should you parametrize?

A thorough parametrized test suite typically covers three categories:

- **Happy paths:** Typical inputs representing everyday usage.
- **Edge cases:** Empty strings `""`, zero `0`, negative numbers `-1`, boundaries (minimum and maximum allowed values), single-element collections `[1]`, or whitespace-only inputs `"   "`.
- **Invalid inputs:** Types or values that violate constraints (e.g., `None`, wrong types, out-of-range numbers).

## Rules of thumb

- **Keep test rows independent:** Each row in a parameter table must be completely independent. Never rely on one row running before another or sharing mutable state.
- **Group similar assertions:** Use one parametrized test for happy path returns, and a separate parametrized test for exceptions. Don't mix return checks and exception checks in the same table unless using `pytest.raises` context conditionally.
- **Tuple formatting:** You can specify parameter names as a comma-separated string `"arg1, arg2"` or a tuple of strings `("arg1", "arg2")`. Both are supported; pick one style and keep it consistent within the test file.
- **Keep data synthetic:** Use simple, hardcoded test data rather than reading from disk or external sources.
- **Run before pushing:** Verify with `pytest tests/test_<module>.py -v` to ensure every test case passes cleanly.

## Before opening your PR

- Place your tests in the appropriate module file under `tests/` (e.g. `tests/test_money.py`).
- Run the full test suite locally: `python -m pytest tests/` or `uv run pytest`.
- Check formatting and style with `pre-commit run --all-files` (see the [Pre-commit Guide](pre_commit_template.md)).
- Follow the [Pull Request Workflow Guide](pr_workflow_template.md) to commit and open your PR.
