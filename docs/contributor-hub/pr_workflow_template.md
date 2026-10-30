# Pull Request Workflow Guide

Contributing to open source can feel intimidating the first time. This guide breaks down the full lifecycle of a pull request for `py-simple-wrap`—from creating your feature branch to passing all automated checks and getting your PR merged.

## Copy this checklist

```text
[ ] Sync your local main branch with upstream/main.
[ ] Create a descriptive branch (e.g. feat/..., fix/..., docs/..., test/...).
[ ] Make your changes following the Contributor Hub templates.
[ ] Run the test suite: pytest tests/test_<module>.py
[ ] Check code formatting: ruff check . && ruff format --check .
[ ] Commit your changes with a clear message (Conventional Commits style).
[ ] Push your branch to your GitHub fork: git push -u origin your-branch-name
[ ] Open your pull request on GitHub and link the matching issue (e.g. Closes #123).
[ ] Watch the CI checks and respond to review comments if requested.
```

## Branch naming conventions

Branch names in `py-simple-wrap` reflect the type of contribution:

| Prefix | When to use it | Example |
|---|---|---|
| `feat/` | Adding a new function or helper capability | `feat/easy-bytes-percent-free` |
| `fix/` | Fixing a bug or unexpected behavior | `fix/url-duplicate-query-params` |
| `docs/` | Writing tutorials, guides, or documentation | `docs/study-habit-tracker-tutorial` |
| `test/` | Adding or improving unit tests | `test/easy-date-formatter-coverage` |

Create your branch starting from an up-to-date `upstream/main`:

```bash
git fetch upstream
git checkout -b feat/your-feature-name upstream/main
```

## Running local checks before committing

Catching issues on your machine is much faster than waiting for GitHub Actions:

```bash
# 1. Run unit tests for your module
pytest tests/test_<module>.py

# 2. Check linting and formatting
ruff check .
ruff format --check .
```

If `ruff format` reports formatting differences, format your files automatically:

```bash
ruff format .
```

## Writing commit messages

Use clear, imperative commit messages. If your pull request resolves an issue, mention the issue number:

```bash
git add py_simple_package/src/py_simple/easy_<module>.py tests/test_<module>.py
git commit -m "feat(easy_<module>): add helper_name function and tests (#123)"
```

## Opening the Pull Request

Push your branch to your fork on GitHub:

```bash
git push -u origin your-branch-name
```

Then visit the repository on GitHub or use the GitHub CLI:

```bash
gh pr create --base main --title "feat(easy_<module>): add helper_name function (#123)"
```

### Pull Request Description Template

Copy this into your PR description:

```markdown
### Summary
Brief description of what this PR does and why.

### Changes
- Implemented `helper_name()` in `py_simple_package/src/py_simple/easy_<module>.py`.
- Re-exported `helper_name` in `py_simple_package/src/py_simple/__init__.py`.
- Added unit tests in `tests/test_<module>.py`.
- Updated documentation in `docs/tutorial/easy_<module>.md`.

Closes #<issue_number>
```

## What happens after opening?

1. **Automated CI Checks**: GitHub Actions runs the test suite on Ubuntu across supported Python versions (3.11 through 3.14), along with Pylint and CodeQL static analysis.
2. **Review & Feedback**: The maintainer or reviewers will review your code. If any changes are requested, simply make the edits on your local branch, commit, and push. GitHub automatically updates the pull request.
3. **Merge**: Once approved and checks pass, your PR will be merged into `main` and your name will be added to the contributors list!
