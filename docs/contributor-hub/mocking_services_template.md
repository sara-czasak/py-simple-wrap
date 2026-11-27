# Mocking Functions and Services

When writing unit tests for functions that call external libraries, third-party APIs, or system operations, tests should never make real external calls or depend on live credentials. This guide provides copy-paste templates using `unittest.mock.patch` and `pytest.monkeypatch` to substitute predictable test doubles while testing actual package helpers.

## Copy a working example first

Save this as `tests/test_mock_demo.py` while practicing. For your actual contribution, add your test cases to the appropriate file in `tests/`.

```python
from datetime import datetime
from unittest.mock import MagicMock, patch
import os
import pytest
import requests

from py_simple_package.src.py_simple.easy_ai import summarize_text
from py_simple_package.src.py_simple.easy_date_formatter import get_pretty_date
from py_simple_package.src.py_simple.easy_web import (
    SomethingWentWrongError,
    is_page_up,
)


def test_mocking_time_dependency():
    """Example 1: Mocking an external system clock dependency to test get_pretty_date()."""
    with patch("py_simple_package.src.py_simple.easy_date_formatter.datetime") as mock_dt:
        # Freeze the clock to January 1, 2026 (Thursday)
        mock_dt.now.return_value = datetime(2026, 1, 1, 12, 0)

        # Exercise the real helper under test
        result = get_pretty_date()
        assert result == "Thursday, January 01, 2026"
        mock_dt.now.assert_called_once()


def test_mocking_client_dependency():
    """Example 2: Mocking an external AI model client to test summarize_text()."""
    # Create a mock client model
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Antigravity streamlines open-source workflows."
    mock_model.invoke.return_value = mock_response

    # Exercise the real helper with the test double
    summary = summarize_text(mock_model, "Long article about software tooling...")

    assert summary == "Antigravity streamlines open-source workflows."
    mock_model.invoke.assert_called_once()


def test_mocking_network_and_exceptions():
    """Example 3: Mocking network calls and simulating timeouts in easy_web."""
    with patch("requests.get") as mock_get:
        # Simulate a network timeout from requests
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        # The real is_page_up() catches requests exceptions and raises SomethingWentWrongError
        with pytest.raises(SomethingWentWrongError, match="Connection timed out"):
            is_page_up("https://example.com")


def test_mocking_with_pytest_monkeypatch(monkeypatch):
    """Example 4: Using pytest's built-in monkeypatch fixture for environment variables."""
    # Safely set a temporary environment variable
    monkeypatch.setenv("MOCK_API_KEY", "test-secret-key-123")
    assert os.getenv("MOCK_API_KEY") == "test-secret-key-123"

    # Environment is automatically restored when this test finishes
```

From the repository root, run:

```bash
python -m pytest tests/test_mock_demo.py -q
```

This example produces **4 passed** with zero network calls or system changes.

---

## The Golden Rule: "Patch Where It Is Used"

The most common bug when writing mocks is patching where an object was **defined** instead of where it was **imported and used**.

### What does this mean?

Suppose a helper in `easy_date_formatter.py` imports `datetime` directly:

```python
# py_simple_package/src/py_simple/easy_date_formatter.py
from datetime import datetime

def get_pretty_date():
    return _format_date(datetime.now(), "pretty")
```

If your test patches the standard library `datetime.datetime`:

```python
# ❌ INCORRECT: easy_date_formatter already imported datetime into its own namespace!
with patch("datetime.datetime"):
    get_pretty_date()
```

The real `datetime.now()` will still run because `easy_date_formatter` has its own reference to `datetime`.

Instead, patch it where it is used:

```python
# ✅ CORRECT: patch the reference inside easy_date_formatter
with patch("py_simple_package.src.py_simple.easy_date_formatter.datetime") as mock_dt:
    mock_dt.now.return_value = datetime(2026, 1, 1, 12, 0)
    get_pretty_date()
```

### Hypothetical Web Request Example

As another example, imagine a hypothetical module `my_crawler.py` that imports `requests.get` directly:

```python
# hypothetical my_crawler.py
from requests import get

def fetch_content(url: str):
    return get(url).text
```

- ❌ Patching `patch("requests.get")` will **not** intercept calls made by `my_crawler.py` because `fetch_content` holds a direct reference imported into `my_crawler`.
- ✅ Patching `patch("my_crawler.get")` targets the exact namespace where the function is looked up and executed.

*(Note: If a module imports `import requests` and calls `requests.get()`, patching `requests.get` works because `requests` is looked up dynamically on each call.)*

---

## Fill-in-the-Blanks Templates

### 1. Mocking a Function or Dependency with a Custom Return Value

```python
from unittest.mock import patch

def test_<helper>_success():
    with patch("<target_module>.<dependency_to_mock>") as mock_dep:
        mock_dep.return_value = <expected_fake_result>
        
        result = <your_helper_function>(...)
        
        assert result == <expected_output>
        mock_dep.assert_called_once_with(<expected_args>)
```

### 2. Mocking an External Service or SDK Client

```python
from unittest.mock import MagicMock, patch

def test_<helper>_calls_client():
    mock_client = MagicMock()
    mock_client.<method_name>.return_value = <fake_response>
    
    result = <your_helper_function>(mock_client, ...)
    
    assert result == <expected_result>
    mock_client.<method_name>.assert_called_once_with(...)
```

### 3. Mocking an Error or Exception

```python
from unittest.mock import patch
import pytest

def test_<helper>_handles_error():
    with patch("<target_module>.<dependency_to_mock>") as mock_dep:
        mock_dep.side_effect = <ExpectedUnderlyingError>("Failed operation")
        
        with pytest.raises(<ExpectedPackageError>):
            <your_helper_function>(...)
```

---

## Checklist for Clean Mocks

- [ ] **Test real helpers**: Exercise real package helper functions by mocking their external dependencies, rather than calling mock objects directly.
- [ ] **No live network or API calls**: Tests run entirely offline and complete in milliseconds.
- [ ] **Patch where used**: Double check that the patch target string references the module executing the call.
- [ ] **Verify call arguments**: Use `.assert_called_once_with(...)` or inspect `call_args` to ensure your wrapper forwards the right parameters.
- [ ] **Keep tests isolated**: Use context managers (`with patch(...):`) or fixtures (`monkeypatch`) so mocks are cleaned up after the test exits.
