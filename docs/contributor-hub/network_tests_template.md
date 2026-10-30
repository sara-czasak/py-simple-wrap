# Network Test Template

A test for a web helper should not depend on a website being online. Use
Python's built-in `unittest.mock` to replace the request with a response you
control. You can check successful responses and failures without an internet
connection, API key, or extra mocking library.

This builds on the [Module Tests Template](tests_template.md), using the same
patterns as the project's `tests/test_web.py`.

## Copy this working example

After following the environment setup in
[CONTRIBUTING.md](../how-to/contributing.md), copy this into
`tests/test_web_mock_demo.py`:

```python
from unittest.mock import MagicMock, patch

import pytest
import requests

from py_simple_package.src.py_simple.easy_web import (
    SomethingWentWrongError,
    get_page_content,
)


def test_get_page_content_with_fake_html():
    response = MagicMock()
    response.ok = True
    response.text = "<html><body><h1>Hello</h1></body></html>"

    with patch("requests.get", return_value=response) as mock_get:
        result = get_page_content("https://example.com")

    assert "<h1>" in result
    assert "Hello" in result
    mock_get.assert_called_once_with("https://example.com", timeout=10)


def test_get_page_content_with_unsuccessful_response():
    response = MagicMock()
    response.ok = False

    with patch("requests.get", return_value=response) as mock_get:
        result = get_page_content("https://example.com")

    assert result is None
    mock_get.assert_called_once_with("https://example.com", timeout=10)


def test_get_page_content_with_timeout():
    with patch(
        "requests.get", side_effect=requests.Timeout("example timeout")
    ) as mock_get:
        with pytest.raises(SomethingWentWrongError, match="example timeout"):
            get_page_content("https://example.com")

    mock_get.assert_called_once_with("https://example.com", timeout=10)
```

Run the practice file from the repository root:

=== "Using uv"
    ```bash
    uv run pytest tests/test_web_mock_demo.py
    ```

=== "Using pip"
    ```bash
    python -m pytest tests/test_web_mock_demo.py
    ```

You should see **3 passed**. These cases are already covered in the real web
tests, so remove the practice file when you're done. For a contribution, add
your new cases to the matching module test file instead of submitting the
same tests again.

## Fill in the parts for your helper

Use the example as a starting point, then change these parts:

| Part | Replace it with |
| --- | --- |
| `easy_web`, `get_page_content`, `SomethingWentWrongError` | Your module, helper, and the error it actually promises to raise. |
| `"requests.get"` | The request name your helper looks up; see the next section. |
| `response.ok` and `response.text` | The response attributes your helper reads. For example, some web helpers read `response.content` as bytes. |
| The fake HTML and expected result | A small made-up response and the result your helper should return. |
| `requests.Timeout(...)` | An error from the dependency that your helper should handle. |
| `assert_called_once_with(...)` | Your helper's expected request arguments, including its actual timeout. |

Keep a normal response, an unsuccessful response if your helper handles one,
and a request failure. The expected results come from your helper's behavior:
`get_page_content` returns `None` when `response.ok` is false, but another
helper may raise an error instead.

## Why this works

`MagicMock` gives us a small stand-in for a response. Set the attributes the
helper uses explicitly: an unset mock attribute is another mock, which can
accidentally act like a successful response.

`return_value=response` makes the replaced request return our fake response.
`side_effect=requests.Timeout(...)` makes it raise an exception instead.
Neither makes a real HTTP request inside the `with patch(...)` block.

The `assert` checks the helper's result. `assert_called_once_with` also checks
that it made exactly one request with the expected arguments. Checking only
that a mock was called would miss a helper returning the wrong result.

### Patch the name the helper uses

Read the helper's import and request call before choosing the patch target.
The current `get_page_content` imports `requests` inside the function, then
calls `requests.get(...)`, so `patch("requests.get", ...)` replaces that call.

If a module instead uses `from requests import get`, it holds its own `get`
name. Patch that name in the module under test; replacing `requests.get`
afterward would not replace the reference it already imported. Use the same
module import path as your test, so you patch the module you're actually
calling.

Keep the helper call inside the `with` block. `patch` restores the original
request when the block ends, even if the test fails, so the replacement does
not leak into later tests.

## Before opening the pull request

- Use made-up HTML, URLs, and error messages. Never include real credentials
  or a response copied from a private account.
- Check both the returned result or raised error and the expected request.
  Do not change the expectation just to make a failing test pass.
- Keep requests replaced in every test case, including error cases. Running
  tests should not require a live website or paid service.
- Run your module tests and the full suite described in
  [CONTRIBUTING.md](../how-to/contributing.md), plus the
  [repository's hooks](pre_commit_template.md).

These tests check how the helper handles the responses you provide. They do
not prove that a live website is available or that its response format has
stayed the same.
