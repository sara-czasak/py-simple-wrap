# Code Coverage Guide

Every pull request in `py-simple-wrap` automatically runs test coverage checks in GitHub Actions, and the project maintains a **94%+ overall test coverage target**. If a pull request adds new lines of code without tests for them, Codecov flags the pull request. This guide shows how to measure coverage locally, read the `Missing` lines report, and write tests to cover missing branches before pushing.

## Copy this workflow

Start in the repository's main folder with your virtual environment activated.
Install `pytest-cov` using your environment tool:

=== "Using uv"
    ```bash
    uv pip install pytest-cov
    ```

=== "Using pip"
    ```bash
    python -m pip install pytest-cov
    ```

Run coverage on only the module you modified (substitute `easy_<module>` with your module name, e.g. `easy_bytes`):

```bash
pytest --cov=py_simple_package/src/py_simple/easy_<module> --cov-report=term-missing tests/test_<module>.py
```

Example output:

```text
---------- coverage: platform win32, python 3.13.4 -----------
Name                                                Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------
py_simple_package/src/py_simple/easy_bytes.py         120      4    97%   45-46, 112, 185
---------------------------------------------------------------------------------
TOTAL                                                 120      4    97%
```

`Cover` shows your current test coverage percentage, and `Missing` lists the exact lines that your tests did not execute.

## How to read the results

Look at the columns in the summary table:

- **`Stmts` (Statements):** Total executable statements in your Python file (excluding comments and blank lines).
- **`Miss` (Missed):** Number of statements that never executed during your test suite.
- **`Cover`:** The percentage of executed lines: `(Stmts - Miss) / Stmts`.
- **`Missing`:** The exact line numbers in your file that were not reached during any test.

In the example above, `Missing: 45-46, 112, 185` tells you:
- Lines `45` and `46` were skipped (typically an `if` condition error guard).
- Line `112` was never called (often an edge-case branch).
- Line `185` was not hit (such as an `except` block).

Open `py_simple_package/src/py_simple/easy_<module>.py`, scroll to those line numbers, and see which branch needs a test.

## Covering missing lines

Uncovered lines in `py-simple-wrap` usually fall into one of three common patterns:

### 1. Input validation guards
Functions in this library guard against bad input types before running:

```python
if not isinstance(text, str):
    raise EasyTextError("Input text must be a string.")
```

If you only test valid inputs, the `raise` line stays red.
**The fix:** Add a test that passes invalid inputs (such as integers, `None`, or lists) and asserts the exception:

```python
@pytest.mark.parametrize("invalid_input", [123, None, ["a", "b"]])
def test_my_function_rejects_non_string(invalid_input):
    with pytest.raises(EasyTextError):
        my_function(invalid_input)
```

### 2. Edge case branches
Functions often contain early returns for empty collections or boundary values:

```python
if not items:
    return []
```

**The fix:** Add a test case passing an empty list `[]` or empty string `""` to verify that the early return works as intended.

### 3. Exception wrappers
When wrapping third-party or standard library operations in custom errors:

```python
try:
    return json.loads(content)
except json.JSONDecodeError as error:
    raise EasyJsonError(f"Could not parse JSON: {error}") from None
```

**The fix:** Pass malformed data (like `"{bad: json"`) so that the error handler executes.

## Visualizing missing lines in your browser

If line numbers in the terminal are hard to navigate, generate a color-coded HTML report:

```bash
pytest --cov=py_simple_package/src/py_simple/easy_<module> --cov-report=html tests/test_<module>.py
```

This creates an `htmlcov/` folder. Open `htmlcov/index.html` in your browser:

=== "Windows"
    ```bash
    start htmlcov/index.html
    ```

=== "macOS"
    ```bash
    open htmlcov/index.html
    ```

=== "Linux"
    ```bash
    xdg-open htmlcov/index.html
    ```

Click on your module name to inspect the source file:
- **Green lines** were executed by your tests.
- **Red lines** were never executed.

Write a test for each red line until the whole file is green.

## Rules of thumb

- **Target only your module during development.** Running `--cov=py_simple_package` across the whole repository takes significantly longer. Using `--cov=py_simple_package/src/py_simple/easy_<module>` gives you feedback in seconds.
- **Never commit `htmlcov/` or `.coverage`.** These are local generated artifacts. The project's `.gitignore` already ignores them, but keep `git status` clean by not force-adding them.
- **Run the check before opening a PR.** If your local coverage shows 100% (or above 94%) on the files you modified, Codecov's patch check on GitHub will pass automatically.
