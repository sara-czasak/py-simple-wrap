---
name: 🖋️ Add a new function to {{MODULE_NAME}}
about: A module has fewer than 10 functions and could use another one
title: 🖋️ Add a new function to {{MODULE_NAME}}
labels: good first issue, help wanted, good-first-issue
---
`{{MODULE_NAME}}` currently has fewer than 10 functions — there's room for one more!

> I'm looking for a contributor to add a **new function** to the **[{{MODULE_NAME}} module](https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/{{MODULE_NAME}}.py)**.
>
> **Tasks**:
> - [ ] Pick a function that fits the theme of `{{MODULE_NAME}}` and isn't already covered.
> - [ ] Add it to [`{{MODULE_NAME}}.py`](https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/{{MODULE_NAME}}.py), with a docstring following the [docstring guide](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/docstring_template/).
> - [ ] Check if a test file for the module exists, if there is no test for the module then add a matching test in [`tests/`](https://github.com/sara-czasak/py-simple-wrap/tree/main/tests). Test file names should be `test_` + the name of the module without `easy` (eg. `test_random.py`, `test_csv.py`). If the test file for a module already exists, add your tests there.
>
> **A few guidelines to keep things consistent**:
> - **Keep it beginner-friendly.** The whole point of py-simple-wrap is that someone new to Python can use it without fighting boilerplate.
> - **API style:** a separate, clearly named function (e.g. `miles_to_km()`, not a generic `convert()` dispatcher).
> - **Import style:** it should work as `from py_simple.{{MODULE_NAME}} import your_function`.
>
> **Note**: Not sure what function to add? Open a PR anyway or start a discussion here — happy to talk it through.
>
> **Links:**
> - Module: [`{{MODULE_NAME}}.py`](https://github.com/sara-czasak/py-simple-wrap/blob/main/py_simple_package/src/py_simple/{{MODULE_NAME}}.py)
> - Where tests go: [`tests/`](https://github.com/sara-czasak/py-simple-wrap/tree/main/tests)
> - Contributing guide: [`CONTRIBUTING.md`](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md)
> - Tutorials for contributors: [`docs/contributor-hub`](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/)
