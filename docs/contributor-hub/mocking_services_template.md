# Mocking Functions and Services

When writing unit tests for functions that call external libraries, third-party APIs, or system operations, tests should never make real external calls or depend on live credentials. This guide provides copy-paste templates using `unittest.mock.patch` and `pytest.monkeypatch` to substitute predictable test doubles.

## Copy a working example first

Save this as `tests/test_mock_demo.py` while practicing. For your actual contribution, add your test cases to the appropriate file in `tests/`.

```python
from unittest.mock import MagicMock, patch
import pytest

from py_simple_package.src.py_simple import easy_date_formatter


def test_mocking_function_return_value():
    """Example 1: Mocking a module function to return a fixed value."""
    with patch("py_simple_package.src.py_simple.easy_date_formatter.get_pretty_date") as mock_date:
        mock_date.return_value = "Monday, Jan 1, 2026"
        result = easy_date_formatter.get_pretty_date()
        assert result == "Monday, Jan 1, 2026"
        mock_date.assert_called_once()


def test_mocking_class_instantiation():
    """Example 2: Mocking an external class constructor and its method."""
    with patch("smtplib.SMTP") as mock_smtp_cls:
        # Configure instance returned when SMTP() is instantiated
        mock_instance = MagicMock()
        mock_instance.sendmail.return_value = {}
        mock_smtp_cls.return_value = mock_instance

        # Call the code under test
        import smtplib
        server = smtplib.SMTP("smtp.example.com", 587)
        status = server.sendmail("sender@test.com", ["recv@test.com"], "Hello!")

        assert status == {}
        mock_smtp_cls.assert_called_once_with("smtp.example.com", 587)
        mock_instance.sendmail.assert_called_once()


def test_mocking_exceptions_and_failures():
    """Example 3: Simulating network timeouts or errors."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = TimeoutError("Connection timed out")

        import urllib.request
        with pytest.raises(TimeoutError, match="timed out"):
            urllib.request.urlopen("https://api.example.com")


def test_mocking_with_pytest_monkeypatch(monkeypatch):
    """Example 4: Using pytest's built-in monkeypatch fixture."""
    import os

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

Suppose `py_simple.easy_web` imports `urlopen` like this:

```python
# py_simple_package/src/py_simple/easy_web.py
from urllib.request import urlopen

def fetch_page(url: str):
    return urlopen(url).read()
```

If your test patches `urllib.request.urlopen`:

```python
# ❌ INCORRECT: easy_web already imported urlopen directly into its namespace!
with patch("urllib.request.urlopen"):
    fetch_page("https://example.com")
```

The real `urlopen` will still run because `easy_web` has its own reference to `urlopen`.

Instead, patch it where it is used:

```python
# ✅ CORRECT: patch the reference inside easy_web
with patch("py_simple_package.src.py_simple.easy_web.urlopen"):
    fetch_page("https://example.com")
```

---

## Fill-in-the-Blanks Templates

### 1. Mocking a Function with a Custom Return Value

```python
from unittest.mock import patch

def test_<helper>_success():
    with patch("<target_module>.<function_to_mock>") as mock_func:
        mock_func.return_value = <expected_fake_result>
        
        result = <your_helper_function>(...)
        
        assert result == <expected_output>
        mock_func.assert_called_once_with(<expected_args>)
```

### 2. Mocking an External Service or SDK Client

```python
from unittest.mock import MagicMock, patch

def test_<helper>_calls_client():
    with patch("<target_module>.<ClientClass>") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.<method_name>.return_value = <fake_response>
        mock_client_cls.return_value = mock_client
        
        result = <your_helper_function>(...)
        
        mock_client_cls.assert_called_once()
        mock_client.<method_name>.assert_called_once_with(...)
```

### 3. Mocking an Error or Exception

```python
from unittest.mock import patch
import pytest

def test_<helper>_handles_error():
    with patch("<target_module>.<function_to_mock>") as mock_func:
        mock_func.side_effect = <ExpectedError>("Failed operation")
        
        with pytest.raises(<ExpectedCustomError>):
            <your_helper_function>(...)
```

---

## Checklist for Clean Mocks

- [ ] **No live network or API calls**: Tests run entirely offline and complete in milliseconds.
- [ ] **Patch where used**: Double check that the patch target string references the module executing the call.
- [ ] **Verify call arguments**: Use `.assert_called_once_with(...)` or inspect `call_args` to ensure your wrapper forwards the right parameters.
- [ ] **Keep tests isolated**: Use context managers (`with patch(...):`) or fixtures (`monkeypatch`) so mocks are cleaned up after the test exits.
