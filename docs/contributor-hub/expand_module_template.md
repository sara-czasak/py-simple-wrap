# Adding a Function to an Existing Module

Most `good first issue` tickets in this project ask you to add **one
named helper** to a module that already exists. This page is the
copy-paste path for that work. If you are creating a brand-new
`easy_*.py` file instead, use the [Adding a New Module Guide](new_module_template.md).

## Copy this checklist

Replace `easy_<module>` and `your_helper` before you start:

```text
[ ] Add your_helper to py_simple_package/src/py_simple/easy_<module>.py.
[ ] Give it a docstring using the Docstring Template, including both example tabs.
[ ] Raise the module's existing error type, with `from None` on wrapped failures.
[ ] Export your_helper in the existing `.easy_<module>` block in __init__.py.
[ ] Add tests to the existing tests/test_<module>.py file. Do not create a new test file.
[ ] If the module already has a tutorial, add a short section there.
```

## The files you usually touch

```text
py_simple_package/src/py_simple/easy_<module>.py
py_simple_package/src/py_simple/__init__.py
tests/test_<module>.py
docs/tutorial/easy_<module>.md   # only if that tutorial already exists
```

Leave `MODULES.md`, the README badge table, `mkdocs.yml` reference pages,
and `module-book/data/modules.js` alone unless the issue is for a **new
module**. Those files already describe the module you are extending.

## The helper itself

Keep the name specific (`miles_to_km()`, not `process()`). Follow the
helpers already in that file for arguments, return values, and error
messages.

Copy this raise pattern when you wrap a failure:

```python
try:
    return Path(filepath).read_bytes()
except OSError as error:
    raise EasyModuleError(f"\n\nERROR: {error}") from None
```

`from None` hides the original traceback so a beginner sees one clear
error. Use the exception class the module already defines, such as
`EasyHashError` or `EasyCsvError`.

Fill in the docstring from the [Docstring Template](docstring_template.md).
Public helpers need Args, Returns or Raises when they apply, and an
Example block with both **The Py_simple Way** and **The Traditional Way**
tabs.

## Tests go in the file that already exists

If `tests/test_<module>.py` is already there, add your cases at the
bottom of **that** file. Creating `tests/test_your_helper.py` makes
review harder, because the module's tests then live in two places.

Include:

- a success case
- the invalid inputs the helper rejects
- a check that `from py_simple import your_helper` is the same function
  as `from py_simple.easy_<module> import your_helper`

The last check is in the [Public API Export Template](public_api_template.md).
The [Module Tests Template](tests_template.md) shows how to write the
behavior tests.

## A real example

`hash_file()` already hashes one path. A follow-up helper that hashes a
list of paths belongs in the same `easy_hash.py` file, next to
`hash_file` in `__init__.py`, and in `tests/test_hash.py`.

After you export your helper, this should print `True` (swap in your
names):

```bash
python -c "from py_simple import hash_file; from py_simple.easy_hash import hash_file as module_helper; print(hash_file is module_helper)"
```

Use `uv run python` if you set up the project with `uv`.

## Before you open the pull request

- Run `pytest tests/test_<module>.py` from the repository root.
- Keep the pull request to this one helper. A second function belongs
  on its own issue.
- If `main` moved while you worked, rebase and keep **both** the merged
  code and your addition.

The [Pull Request Workflow Guide](pr_workflow_template.md) covers branch
names, commits, and review replies.
