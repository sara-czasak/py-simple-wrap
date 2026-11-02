# Easy Config

GitHub Actions workflow files are easy to start and just as easy to leave
unfinished. `easy_config` creates a commented starter workflow file, so you
can focus on choosing when it runs and what jobs your project needs.

## A small real-world example

Imagine you have started a Python project and want a place to add automated
checks later. From your project root, create a workflow called `checks`:

```python
from pathlib import Path

from py_simple import gh_workflow_config

workflow = Path(".github/workflows/checks.yml")

gh_workflow_config("checks")

print(workflow.exists())
print("name: checks" in workflow.read_text(encoding="utf-8"))
```

Example output:

```text
True
True
```

## What happened?

`gh_workflow_config()` created the `.github/workflows` folder when it was
missing, copied the built-in starter template into `checks.yml`, and replaced
the template's workflow name with `checks`.

`Path()` points to the file that will be created. `exists()` confirms that the
file is there, and `read_text()` lets the example check that the workflow has
the expected name. If `checks.yml` already exists, `gh_workflow_config()`
leaves it unchanged.

## Working from a subfolder

If you run a setup script from a subfolder instead of the project root, pass
`at_root=False`. The helper finds the Git repository root and creates the
workflow there:

```python
from py_simple import gh_workflow_config

gh_workflow_config("checks", at_root=False)
```

## Loading Environment Files

When developing web services or CLI tools, configuration values are often stored
in `.env` files. `load_env_file()` reads key-value pairs from a `.env` file and
loads them directly into `os.environ` so standard calls like `os.getenv()` work
without third-party dependencies:

```python
import os
from py_simple import create_env_file, load_env_file

# Create a sample .env file
create_env_file({"PORT": "8080", "APP_ENV": "development"})

# Load variables into os.environ
load_env_file(".env")

print(os.getenv("PORT"))
print(os.getenv("APP_ENV"))
```

Example output:

```text
8080
development
```

Existing environment variables can be preserved by keeping `override=False` (the
default) or updated by passing `override=True`.

## Why use these helpers?

Without this helper, you would need to create the `.github/workflows` folders,
copy a workflow skeleton, and remember the basic YAML structure yourself.
`gh_workflow_config()` gives you a commented starting point while still
leaving the trigger, permissions, and commands under your control.
