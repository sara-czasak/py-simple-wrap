# Understanding the Codebase Layout

New to `py-simple-wrap`? The list of folders can look intimidating, but the layout is consistent and small once you know what each piece is for. This page is a map: where the real code lives, where tests and docs go, and how it all wires together.

## The layout in one glance

```
py-simple-wrap/
├── py_simple_package/src/py_simple/   # the importable package — this is where modules live
│   ├── __init__.py                    # re-exports every public function
│   └── easy_<name>.py                 # one module per feature: easy_config.py, easy_url.py, ...
├── tests/
│   └── test_<name>.py                 # tests mirror the modules (test_config.py for easy_config.py)
├── docs/
│   ├── tutorial/                      # one "how do I use it" page per module + project tutorials
│   ├── reference/                     # auto-generated API pages (rebuilt from docstrings)
│   └── contributor-hub/               # the guides you're reading now
├── mkdocs.yml                         # builds and orders the docs site (the nav lives here)
├── pyproject.toml                     # package metadata, dependencies, tool config
└── scripts/                           # maintainer automation — usually not needed for PRs
```

## Where the actual Python code lives

Everything importable lives in **`py_simple_package/src/py_simple/`**. You'll see both a directory *and* a file named `py_simple` in the repo root — the directory is the source of truth; the file is a thin shim so imports work during development. Don't add code there.

Each feature is one `easy_<name>.py` file:

- `easy_config.py` — writing and reading config files
- `easy_url.py`, `easy_json.py`, `easy_money.py`, ... one per topic

A module typically contains a module docstring, a few clearly named functions, and often one custom exception (see the [Custom Exception Template](error_template.md)).

## How a function becomes importable

Functions are defined in their module, then re-exported from `py_simple/__init__.py`. That is why both of these work:

```python
from py_simple import read_env_file               # flat, the style this project prefers
from py_simple.easy_config import read_env_file   # direct module import
```

If you add a function and want the flat `from py_simple import ...` style, it must be added to `__init__.py` too — see the [Public API Export Template](public_api_template.md) for where and how.

## Where tests go

Tests live in **`tests/`** and mirror the modules: `easy_config.py` → `tests/test_config.py`. Test file names drop the `easy_` prefix.

Run them from the repo root with:

```bash
pytest tests/test_config.py
```

See the [Module Tests Template](tests_template.md) for the expected structure, and the [Keeping Tests Isolated](test_isolation_template.md) guide for `tmp_path` / `monkeypatch` patterns.

## Where docs go

- **Tutorials** (how-to-use pages) → `docs/tutorial/`
- **Auto-generated API reference** → `docs/reference/` (regenerated from docstrings; not hand-edited)
- **Contributor guides** → `docs/contributor-hub/`

Every page is listed in `mkdocs.yml` under its nav section. Add new pages there or they won't appear on the built site.

## Checklist when you add a file

- [ ] Put source code in `py_simple_package/src/py_simple/easy_<name>.py`
- [ ] Add matching tests in `tests/test_<name>.py`
- [ ] Add a tutorial page in `docs/tutorial/` if it's a new module
- [ ] Register any new docs page in `mkdocs.yml`
- [ ] Run the relevant tests before opening a PR
