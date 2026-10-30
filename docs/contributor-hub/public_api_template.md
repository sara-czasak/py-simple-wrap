# Public API Export Template

Adding a helper to an `easy_*.py` file makes it available from that module.
To let a beginner use `from py_simple import your_helper`, also add it to
`py_simple_package/src/py_simple/__init__.py`.

## Copy this checklist

Replace `easy_<module>` and `your_helper` with your module and function names:

```text
[ ] Define your_helper in py_simple_package/src/py_simple/easy_<module>.py.
[ ] Write its docstring using the Docstring Template.
[ ] Find the existing import block for .easy_<module> in __init__.py.
[ ] Add your_helper to that block, keeping the existing names.
[ ] Check both import paths in the installed development environment.
[ ] Add behavior tests to the matching tests/test_<module>.py file.
```

The export entry looks like this (the angle brackets are placeholders,
so replace them before using the code):

```python
from .easy_<module> import (
    existing_helper,
    your_helper,
)
```

Edit the existing block instead of adding another copy. For a new module,
add a new block alongside the other module imports.

## A real example

`hash_text` lives in `easy_hash.py`, and the package's `__init__.py` imports
it from `.easy_hash`. After setting up the development environment using
[CONTRIBUTING.md](../how-to/contributing.md), run this from the repository root:

```bash
python -c "from py_simple import hash_text; from py_simple.easy_hash import hash_text as module_helper; print(hash_text is module_helper)"
```

Expected output:

```text
True
```

Use `uv run python` instead of `python` if you set up the project with `uv`.
For your own helper, replace `hash_text` and `easy_hash` in the command.
This checks that the short import exposes the same function as the module
import. It does not replace tests of the function's behavior.

## What happened?

Python runs the package's `__init__.py` when it imports `py_simple`.
The import block gives the package a name pointing to your function,
so users can choose either import style.

If the module import works but the short import fails, check the spelling
and the export block. If both fail, first check that your development
environment has this checkout installed and read the exception for the
module that failed to load.

## Before opening the pull request

- Check that your chosen name is not already exported by another module.
  An import later in `__init__.py` can replace a name imported earlier.
- Export helpers meant for users; leave internal helpers such as
  `_new_hasher` inside their module.
- Follow the [Docstring Template](docstring_template.md) and
  [Module Tests Template](tests_template.md) for the implementation.
- For a new module, also add its tutorial and reference page to `mkdocs.yml`.

Keeping the short import working means readers can copy the package's
examples without needing to learn its internal file layout first.
