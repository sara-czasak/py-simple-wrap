# Optional Dependency Guide

`py-simple-wrap` aims to stay lightweight and fast to install. While most helpers use only Python's standard library, some specialized modules (such as `easy_game`, `easy_images`, or `easy_data_visualization`) rely on third-party packages like `pygame` or `matplotlib`.

When an optional package is not installed, importing `py_simple` should never crash. Instead, the module must import the dependency safely, provide clear instructions when an uninstalled feature is accessed, and include unit tests for both scenarios.

## Why handle optional dependencies this way?

If a module uses a bare `import pygame` at the top level, any user who hasn't installed `pygame` will see an immediate `ModuleNotFoundError` the moment they run `import py_simple`, even if they only wanted to use `easy_math` or `easy_strings`.

By catching the import error and checking for `None` inside functions, `py-simple-wrap` stays fully usable as a lightweight toolbox, while still allowing developers to opt into heavier libraries when needed.

## The module pattern

When writing or expanding a module that uses an optional third-party library, follow this standard pattern at the top of your file:

```python
try:
    import my_optional_package
except ImportError:
    my_optional_package = None
```

Then, in each function requiring that package, guard the call before running library-specific code:

```python
def my_helper_function(...):
    """... standard docstring ..."""
    if my_optional_package is None:
        raise EasyModuleNameError(
            "easy_module needs my_optional_package. Install it with: pip install py-simple-wrap[feature]"
        )

    # Proceed with using my_optional_package...
```

## How to test optional dependencies

A common question for new contributors is: *"How do I test the missing dependency error if the library is already installed in my virtual environment?"*

Do **not** uninstall packages during tests! Pytest provides the built-in `monkeypatch` fixture, which lets you temporarily simulate the package being absent.

Copy this pattern into your test file (e.g. `tests/test_my_module.py`):

```python
import pytest

from py_simple import EasyModuleNameError
import py_simple.easy_my_module as easy_my_module


def test_helper_when_dependency_is_missing(monkeypatch):
    # Temporarily simulate the package not being installed
    monkeypatch.setattr(easy_my_module, "my_optional_package", None)

    # Verify that calling the helper raises the expected custom error
    with pytest.raises(
        EasyModuleNameError,
        match="easy_module needs my_optional_package",
    ):
        easy_my_module.my_helper_function(...)
```

When this test finishes, `monkeypatch` automatically restores the original package import for all subsequent tests.

## Rules of thumb

- **Never use bare top-level imports for third-party libraries.** Always wrap the import in `try ... except ImportError: pkg = None`.
- **Raise the module's custom exception**, not `ImportError` or `ModuleNotFoundError`. Modeled on `EasyGameError` in `easy_game.py`: users catch one consistent exception type for all module failures.
- **Provide an actionable install command** in the error message, showing the optional extra (e.g., `pip install py-simple-wrap[game]`).
- **Use `monkeypatch.setattr(module, "package_name", None)` in tests.** This cleanly verifies the error branch without modifying your local environment or affecting other tests.
- **Document optional dependencies** in the module docstring and tutorial, noting whether an extra install tag is needed.

## A real worked example from `easy_game`

Here is how `py_simple.easy_game` implements and tests optional `pygame` support:

**In `py_simple_package/src/py_simple/easy_game.py`:**

```python
try:
    import pygame
except ImportError:
    pygame = None


def basic_game_setup(width: int, height: int, title: str = "My Game") -> tuple:
    """Sets up a pygame window and clock in one call."""
    if pygame is None:
        raise EasyGameError(
            "easy_game needs pygame. Install it with: pip install py-simple-wrap[game]"
        )

    try:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        clock = pygame.time.Clock()
        return screen, clock
    except Exception as e:
        raise EasyGameError(str(e)) from None
```

**In `tests/test_game.py`:**

```python
import pytest

from py_simple.easy_game import EasyGameError
import py_simple.easy_game as easy_game


def test_basic_game_setup_missing_pygame(monkeypatch):
    monkeypatch.setattr(easy_game, "pygame", None)

    with pytest.raises(EasyGameError, match="easy_game needs pygame"):
        easy_game.basic_game_setup(800, 600)
```
