# Custom Exception Template

`py-simple-wrap` wraps risky operations (network calls, file I/O, JSON parsing, external libraries) so beginners get one clear, readable error instead of a random builtin traceback. This page is the template for adding a new custom exception when a module needs one.

Modeled on the real exceptions already in the codebase — `SomethingWentWrongError` in `easy_web.py`, `EasyJsonError` in `easy_json.py`, `EasyFlowError`, `EasyAsyncError`, `EasyGameError`, `EasyGeneratorError`, `ImageProcessingError`, and `InvalidExtension` in `easy_file_manager.py` — all follow the same shape.

## Why bother with a custom exception at all?

If `easy_web.get_page_content()` just let `requests`' own exceptions bubble up, a beginner would see something like `requests.exceptions.ConnectionError` or `requests.exceptions.Timeout` — different exception types depending on *how* the network failed, none of which say anything about *py-simple-wrap*. A custom exception gives one predictable name per module (`SomethingWentWrongError`) that always means "this py_simple function couldn't do its job," with a plain-English message explaining why. Beginners can write one `except` clause instead of memorizing every exception type a third-party library might throw.

## The template

Copy this whole block and fill in the placeholders:

````python
class ModuleNameError(Exception):
    """
    Raised when <the specific situation this covers>.

    <A sentence or two on what this covers and, importantly, what it
    does NOT cover — e.g. "this is only for real failures; a function
    that can succeed with an empty result returns None/[] instead of
    raising.">

    Args:
        message (str): Description of what went wrong, usually
            including the original error message.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
````

And where you raise it, wrap the risky call:

````python
def do_the_risky_thing(...):
    """... normal docstring ..."""
    try:
        return _actually_risky_stdlib_or_third_party_call(...)
    except Exception as e:
        raise ModuleNameError(f"Couldn't do the thing: {e}") from None
````

## Rules of thumb

- **Name it `<Module>Error`.** `SomethingWentWrongError`, `EasyJsonError`, `EasyFlowError` all follow this. (`InvalidExtension` in `easy_file_manager.py` is the one exception to the pattern in this codebase — new exceptions should still follow `<Module>Error` rather than add another one-off name.)
- **Always subclass `Exception` directly**, not a more specific builtin like `ValueError` or `IOError`. Every custom exception in this codebase does this — it keeps the public API surface to one predictable exception type per module, rather than making users guess which builtin subclass a given failure maps to.
- **Store the message and call `super().__init__()`** exactly like the template — this is what makes `str(the_exception)` and `print(the_exception)` show the readable message, and keeps the exception compatible with normal Python exception handling.
- **Use `raise ModuleError(...) from None`** when wrapping another exception. The `from None` suppresses Python's "During handling of the above exception, another exception occurred" chained traceback — a beginner doesn't need to see `requests`' internal stack trace, they need to see *your* message. Compare `easy_web.py`'s `get_page_content` for a real example.
- **Only raise for real failures.** If a function can reasonably return "nothing found" (an empty list, `None`), do that instead of raising — this is called out explicitly in `SomethingWentWrongError`'s own docstring. Custom exceptions are for "the operation could not complete," not "the operation completed and found nothing."
- **Document what it does and doesn't cover** in the exception's own docstring, not just in the function that raises it — someone catching `EasyJsonError` should be able to read its docstring alone and know what triggers it.

## A minimal worked example

```python
class EasyColorsError(Exception):
    """
    Raised when a color value can't be parsed or converted.

    Covers malformed hex codes, out-of-range RGB values, and any other
    input that isn't a valid color py_simple can work with.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def hex_to_rgb(hex_code: str) -> tuple:
    """... docstring ..."""
    try:
        hex_code = hex_code.lstrip("#")
        return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
    except (ValueError, IndexError) as e:
        raise EasyColorsError(f"'{hex_code}' isn't a valid hex color: {e}") from None
```

And how a user of the package would catch it today:

```python
from py_simple import hex_to_rgb
from py_simple.easy_colors import EasyColorsError

try:
    rgb = hex_to_rgb("not-a-color")
except EasyColorsError as e:
    print(f"Oops: {e}")
```

## A known gap worth knowing about

None of the eight existing custom exceptions (`SomethingWentWrongError`, `EasyJsonError`, `EasyFlowError`, `EasyAsyncError`, `EasyGameError`, `EasyGeneratorError`, `ImageProcessingError`, `InvalidExtension`) are currently exported from `py_simple/__init__.py` — only functions are. That means today, catching any of them requires importing from the submodule directly (`from py_simple.easy_web import SomethingWentWrongError`), not the flatter `from py_simple import ...` style every function in this package uses. This is inconsistent with the project's whole "simple, flat imports" philosophy, but it's the current reality, not a documentation error — worth raising with the maintainer as its own fix rather than quietly working around it here.
