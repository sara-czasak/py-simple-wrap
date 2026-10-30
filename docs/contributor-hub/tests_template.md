# Testing Tutorial

Every function in `py-simple-wrap` has tests, and every pull request runs them automatically. This page walks you through writing your first one. You don't need to know anything about testing already — if you can write a Python function, you can write a test.

Modeled on the real tests already in the repo (like `tests/test_strings.py` and `tests/test_json.py`), so what you learn here is exactly what you'll see in the codebase.

## What is a test, really?

A test is a small function that answers one question: **"when I give my function this input, do I get the output I expected?"**

You already do this by hand. You write a function, run it with a few values, look at what prints, and think "yep, that looks right." A test is the same thing, except you write your expectation down once and let the computer check it — every time, in a second, forever. If someone changes the code later and accidentally breaks something, the test notices before anyone else has to.

## Why bother?

- **You find out when something breaks.** Not a week later when someone opens an issue.
- **You can change code without fear.** Run the tests after your change. Green means you didn't break anything.
- **Reviewers trust your pull request more.** A PR with a test says "I checked this works," and it makes the review quicker.

## Setting up

You only need `pytest`. If you followed [CONTRIBUTING.md](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md) to set up the project, you already have it. To check:

````bash
pytest --version
````

If that prints a version number, you're ready. (If it says "command not found", install the project with `pip install -e .[all,test,docs]` or `uv sync --all-extras --dev`, as described in CONTRIBUTING.)

## Your first test

Say you're adding a test for `count_words`, which counts the words in a piece of text. Create a practice file in the `tests/` folder (`test_strings.py` already exists for real, so we'll call ours `test_count_words_demo.py`). The name **must** start with `test_` — that's how pytest knows it's a test file.

````python
# tests/test_count_words_demo.py

from py_simple_package.src.py_simple.easy_strings import count_words


def test_count_words_counts_a_sentence():
    result = count_words("Hello world! How are you?")
    assert result == 5
````

That's the whole test. Let's read it top to bottom:

1. **The import** brings in the function you want to test. Every test file in this repo imports from `py_simple_package.src.py_simple.<module>`.
2. **`def test_...`** — the function name must start with `test_`, or pytest will ignore it. Make the rest of the name say what you're checking.
3. **`result = count_words(...)`** — call your function with an example input.
4. **`assert result == 5`** — this is the actual check. `assert` means "I expect this to be true." If it is, the test passes. If it isn't, the test fails.

## Running it

From the project's main folder, run:

````bash
pytest -v
````

`-v` means "verbose", which shows each test by name. (The project already turns this on for you in `pyproject.toml`, but it doesn't hurt to know what it does.)

Example output:

````text
tests/test_count_words_demo.py::test_count_words_counts_a_sentence PASSED [100%]

============================== 1 passed in 0.02s ===============================
````

`PASSED` and `1 passed` are what you want to see. Congratulations, that's a working test.

## What a failing test looks like

Failing tests are not bad news. They're the whole point — they're the test doing its job. Let's break ours on purpose by changing `5` to `6`:

````python
assert result == 6
````

Run `pytest` again:

````text
=================================== FAILURES ===================================
______________________ test_count_words_counts_a_sentence __________________

    def test_count_words_counts_a_sentence():
        result = count_words("Hello world! How are you?")
>       assert result == 6
E       assert 5 == 6

tests/test_count_words_demo.py:6: AssertionError
=========================== short test summary info ============================
FAILED tests/test_count_words_demo.py::test_count_words_counts_a_sentence - a...
============================== 1 failed in 0.03s ===============================
````

How to read this:

- The **`>`** arrow points at the exact line that failed.
- The **`E`** lines say why: `assert 5 == 6` means "the function gave back `5`, but you said it should be `6`."
- The last line tells you which test failed, so you know where to look.

When a test fails, there are two possibilities: either the function has a bug, or your expectation was wrong. Figuring out which one is part of the job — and here, the function was right (it *is* five words) and the test was wrong. Change it back to `5` and it goes green again.

## Testing lots of inputs at once

A function should work for more than one input, including weird ones (empty text, only spaces). Writing a separate test for each gets repetitive, so pytest has `parametrize`: one test, many examples.

````python
import pytest

from py_simple_package.src.py_simple.easy_strings import remove_extra_spaces


@pytest.mark.parametrize(
    "text, expected",
    [
        ("  hello   world  ", "hello world"),
        ("hello world", "hello world"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_remove_extra_spaces(text, expected):
    assert remove_extra_spaces(text) == expected
````

Read the list as a little table: each row is one example, with the input first and the answer you expect second. pytest runs the test once per row and reports each one separately, so if row three fails you'll know exactly which input caused it.

To add a new case later, you just add one more row. This is the pattern used all over `tests/test_strings.py`.

## Testing that a function raises an error

Sometimes the *correct* behaviour is an error. In this project, functions raise a clear custom error (see the [Custom Exception Template](error_template.md)) instead of letting a confusing one leak through. You test that with `pytest.raises`:

````python
import pytest

from py_simple_package.src.py_simple.easy_json import EasyJsonError, open_json


def test_open_json_missing_file_raises(tmp_path):
    missing_file = tmp_path / "nope.json"

    with pytest.raises(EasyJsonError):
        open_json(str(missing_file))
````

Two new things here:

- **`with pytest.raises(EasyJsonError):`** means "the code inside this block *must* raise `EasyJsonError`." If it does, the test passes. If it raises nothing, or a different error, the test fails.
- **`tmp_path`** is a built-in pytest helper that gives your test its own temporary folder. Anything you create there is deleted afterwards, so your tests never leave junk files behind or touch real ones. Just add `tmp_path` as a parameter and pytest fills it in for you. Use it any time your test needs a file.

## The template

Copy this block into a `tests/test_<module>.py` file and fill in the placeholders:

`````markdown
````python
import pytest

from py_simple_package.src.py_simple.easy_<module> import <function_name>


def test_<function_name>_<what_you_are_checking>():
    result = <function_name>(<example input>)
    assert result == <expected output>


@pytest.mark.parametrize(
    "<input_name>, expected",
    [
        (<normal example>, <expected>),
        (<edge case, e.g. empty>, <expected>),
    ],
)
def test_<function_name>_many_inputs(<input_name>, expected):
    assert <function_name>(<input_name>) == expected


def test_<function_name>_raises_on_bad_input():
    with pytest.raises(<ModuleError>):
        <function_name>(<bad input>)
````
`````

Delete the parts you don't need. A function that never raises doesn't need the third test.

## What should I test?

You don't have to test everything. For each function, aim for:

- **One normal example** — the thing the function is meant to do.
- **One or two edge cases** — empty text, an empty list, zero, a single item. Edge cases are where bugs hide.
- **One error case** — only if the function is supposed to raise something.

That's usually three to five tests per function, and it's plenty.

## Rules of thumb

- **Test names describe the behaviour.** `test_count_words_counts_a_sentence` tells the reader what broke without opening the file. `test_1` doesn't.
- **One idea per test.** If a test fails, you want to know immediately which thing went wrong.
- **Run the test before you trust it.** Make sure it can actually fail. If you've never seen it fail, you don't know it's checking anything.
- **Use `tmp_path` for files.** Never read or write real files from a test.
- **Don't hit the internet or paid APIs in tests.** Tests must run anywhere, quickly, and for free. Look at `tests/test_web.py` and `tests/test_ai.py` to see how the project fakes those calls.
- **Put the file in the right place.** Tests go in `tests/`, named `test_<module>.py`, one file per module.

## Running just your tests

Once the project has lots of tests, you don't want to wait for all of them while you work. Run one file:

````bash
pytest tests/test_strings.py
````

Or only the tests whose name contains a word:

````bash
pytest tests/test_strings.py -k count_words
````

Example output:

````text
tests/test_strings.py::test_count_words[hello 123 world-3] PASSED        [100%]

======================= 8 passed, 53 deselected in 0.04s =======================
````

Before you open your pull request, run plain `pytest` once with no extras, so you know the whole suite is still green. GitHub will run it again on Python 3.11 through 3.14 when you push.

## Still stuck?

That's okay. Open a draft pull request with your test file as it is — even a failing one — and say what you're stuck on. Someone will help you get it green. See [CONTRIBUTING.md](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md) for how to reach out.