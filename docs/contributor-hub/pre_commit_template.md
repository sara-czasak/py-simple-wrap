# Pre-commit Guide

Pre-commit runs small checks before a commit, so you can catch formatting
problems before someone reviews your pull request. This project already has
a `.pre-commit-config.yaml`; use it rather than creating another one.

## Copy this workflow

Start in the repository's main folder, after setting up the development
environment in [CONTRIBUTING.md](../how-to/contributing.md).
Activate `.venv` first: use `source .venv/bin/activate` on macOS/Linux,
or `.venv\Scripts\activate` in Windows Command Prompt.
Install the pre-commit tool using the same setup method you chose there:

=== "Using uv"
    ```bash
    uv pip install pre-commit
    ```

=== "Using pip"
    ```bash
    python -m pip install pre-commit
    ```

Replace `path/to/your_file.py` below with a file you changed. List more paths
after it if your change touches several files, including documentation.

```bash
pre-commit install
git add -- path/to/your_file.py
pre-commit run --files path/to/your_file.py
git diff -- path/to/your_file.py
```

`pre-commit install` connects this checkout to Git's commit hook. Do it once
per checkout; installing the tool alone does not install the Git hook.
The first run may download the hook tools. Later runs reuse their cached
environments, using the versions pinned in `.pre-commit-config.yaml`.

`git add` stages your chosen files, including new ones. The manual run lets
you see the checks before committing; once the hook is installed, a normal
`git commit` also checks the staged files.

## If a check changes your file

Seeing **Failed** can mean a hook fixed something for you. For example,
`end-of-file-fixer` can add a missing newline, and `ruff-format` can reformat
Python code. Read the output to see which files changed.

Review those edits with `git diff`, then stage the corrected file and run
the checks again:

```bash
git diff -- path/to/your_file.py
git add -- path/to/your_file.py
pre-commit run --files path/to/your_file.py
git diff --cached -- path/to/your_file.py
```

Repeat if another hook makes an edit. A passing run does not stage files
for you; `git diff --cached` shows the version you are about to commit.

If the hook **did not** fix the problem, follow its message, edit the file,
and use the same review, stage and rerun steps. For example, `check-yaml`
reports invalid YAML but cannot decide how your configuration should read.
A syntax error needs a correction, not repeated runs of the unchanged file.

## What this repository checks

These hook IDs come from the repository's `.pre-commit-config.yaml`:

| Hook | What to expect |
| --- | --- |
| `trailing-whitespace` | Removes spaces at the ends of lines. |
| `end-of-file-fixer` | Fixes a missing final newline or extra blank lines at the end. |
| `check-yaml` | Checks YAML syntax; fix reported errors yourself. |
| `check-added-large-files` | Reports added files that exceed its size limit. Check whether the file belongs in the contribution. |
| `ruff` | Checks Python code and applies the fixes it can. This repository's `--exit-non-zero-on-fix` setting asks you to rerun after a fix. |
| `ruff-format` | Formats Python code. Review and stage any edits it makes. |

**Skipped (no files to check)** is normal when a hook has no matching file
type. A documentation-only change, for example, has no Python input for
Ruff. This does not mean Python linting was run and passed.

Keep the existing hook versions and settings. If a download or environment
setup fails, read that error and check your setup before retrying; changing
the project's pins is a separate change, not a fix for your file.

## Checking more than your changed files

To check all tracked files, you can run:

```bash
pre-commit run --all-files
```

This can report or rewrite files outside your change. Inspect `git diff`
afterward and discuss unrelated cleanup with the maintainer rather than
including it automatically in your pull request. It does not include new
untracked files, so remember to stage files you intend to contribute.

## Before opening the pull request

- Inspect your diff, including the staged version, and keep the change focused.
- Rerun the applicable hooks after your last edit.
- Run the tests required by [CONTRIBUTING.md](../how-to/contributing.md).
  The hooks do not run `pytest` or the CI Pylint check for you.
- For documentation changes, also run `mkdocs build` and inspect the pages.
  A successful hook run alone does not verify examples, behavior or rendering.

For the full command reference, see the [pre-commit documentation](https://pre-commit.com/).
