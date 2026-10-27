# Type Hints Template

Type hints tell Python users, code editors (like VS Code and PyCharm), and documentation tools what type of data your helper expects and returns.

Adding clean type hints means beginners get autocomplete, helpful hover tooltips, and early error warnings in their editor.

## Copy this checklist

Replace `<module>` and `your_helper` with your module and function names:

```text
[ ] Add type hints to every parameter in your function header.
[ ] Add a return type hint (use `-> None` if the function does not return a value).
[ ] Use modern built-in generics like `list[str]` and `dict[str, Any]` rather than importing uppercase `List` or `Dict`.
[ ] Use `| None` for optional parameters with default values (such as `options: list[str] | None = None`).
[ ] Use union `|` when multiple types are accepted (such as `file_path: str | Path`).
[ ] Check that the types documented in your Google-style docstring match your type annotations.
```

## Function template

Copy this template into your module and adjust the types to match what your function needs:

```python
from pathlib import Path
from typing import Any, Callable


def your_helper(
    text: str,
    count: int = 1,
    tags: list[str] | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Short summary of what your helper does.

    Args:
        text (str): The input text to process.
        count (int, optional): Number of times to process. Defaults to 1.
        tags (list[str] | None, optional): Optional list of tag labels. Defaults to None.
        output_path (str | Path | None, optional): Destination file path. Defaults to None.

    Returns:
        dict[str, Any]: Dictionary containing the results.
    """
    ...
```

## Quick reference: common types in py-simple-wrap

This project uses Python 3.10+ modern type hints. You do not need to import `List`, `Dict`, `Tuple`, `Set`, or `Optional` from `typing`.

| Data type | Type hint | Example usage |
|---|---|---|
| Text string | `str` | `title: str` |
| Whole number | `int` | `limit: int = 10` |
| Decimal number | `float` | `threshold: float = 0.5` |
| True or False | `bool` | `overwrite: bool = False` |
| List of items | `list[str]` or `list[int]` | `items: list[str]` |
| Dictionary | `dict[str, Any]` | `payload: dict[str, Any]` |
| File path | `str | Path` | `source: str | Path` |
| Optional parameter | `str | None` | `encoding: str | None = None` |
| Either of two types | `int | float` | `value: int | float` |
| Callback function | `Callable[[str], bool]` | `validator: Callable[[str], bool]` |
| No return value | `None` | `def save_file(...) -> None:` |

## A real example

Here is how `verify_file_hash` in `py_simple.easy_hash` types its parameters and return value:

```python
from pathlib import Path


def verify_file_hash(
    file_path: str | Path,
    expected_checksum: str,
    algorithm: str = "sha256",
) -> bool:
    """Check whether a file matches an expected hash checksum."""
    ...
```

Notice how:
- `file_path: str | Path` accepts either a string path (`"data/notes.txt"`) or a `pathlib.Path` object.
- `expected_checksum: str` explicitly expects a hexadecimal checksum string.
- `algorithm: str = "sha256"` specifies a default string argument.
- `-> bool` clearly documents that the function returns `True` if the hash matches, and `False` otherwise.

## Why this matters

1. **Editor Autocomplete:** When a beginner types `result = your_helper("test")`, their editor inspects the type annotations and shows available methods on `result`.
2. **Clear Documentation:** The project documentation builds with `mkdocs` and `griffe`. If parameters lack annotations, the documentation generator emits warnings.
3. **Catching Bugs Early:** Type checkers like `mypy` flag mismatched arguments before running the code.

## Before opening the pull request

- Run automated tests for your module using `pytest tests/test_<module>.py` to verify behavior.
- Run `mkdocs build` to confirm the documentation renders without syntax errors.
- Keep helper signatures simple and easy to understand for beginners.
