# Writing the Two-Panel Examples

Every function and tutorial in `py-simple-wrap` shows what you're building side by side: the **Py_simple Way** (the short call this package exists for) next to the **Traditional Way** (the verbose standard-library version). This page is the template for writing those two panels — the exact syntax, when both are needed, and the rules that keep them useful.

## The template

Inside a module (`easy_*.py`), an example lives under `Example:` and uses two tabs:

````markdown
    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import <function>

            result = <function>(<args>)
            ```

        === "The Traditional Way"
            ```python
            # the equivalent, using only the Python standard library
            ...
            ```
````

In a tutorial page (`docs/tutorial/*.md`), the same tabs are written without indentation:

````markdown
=== "The Py_simple Way"
    ```python
    from py_simple import <function>
    ```

=== "The Traditional Way"
    ```python
    # verbose standard-library equivalent
    ```
````

## Rules of thumb

- **Lead with the Py_simple Way.** It's the whole point of the project.
- **The Traditional Way must be real and equivalent** — same input, same output, and written with only the standard library (or other third-party packages, never `py_simple`).
- **Keep both short.** Enough to show the contrast, not a full program.
- **Write a matching output comment** (`# -> "..."`) when the result is short, so readers can check it at a glance.
- **Never leave the Traditional panel blank.** If there's no clean one-liner equivalent, show the honest manual steps a beginner would otherwise have to write.

## Why bother?

The two panels answer the first question every reader asks: "what would I actually have to write without this?" Seeing the short version next to the long one makes why the package exists obvious, and it gives maintainers a quick check that a function does something real rather than just wrapping itself.

## A worked example

````markdown
    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import read_env_file

            config = read_env_file(".env")
            ```

        === "The Traditional Way"
            ```python
            config = {}
            with open(".env", encoding="utf-8") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        config[key] = value
            ```
````
