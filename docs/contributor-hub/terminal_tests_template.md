# Terminal & CLI Testing Template

Functions that print text, draw styled rules, format tables, or prompt the user for input shouldn't pollute the test runner's console or hang waiting for manual keystrokes. Use pytest's built-in `capsys` fixture to capture standard output (`stdout`) and standard error (`stderr`), and `monkeypatch` to simulate terminal widths or mock user input.

This builds on the [Module Tests Template](tests_template.md), using the same patterns found across `tests/test_terminal.py`.

## Copy this working example

After following the environment setup in [CONTRIBUTING.md](../how-to/contributing.md), create `tests/test_terminal_demo.py` and paste this code:

```python
from py_simple_package.src.py_simple.easy_terminal import (
    EasyTerminal,
    print_centered,
    print_rule,
    print_styled,
    print_table,
)


def test_print_styled_captures_stdout(capsys):
    """Verify that print_styled sends formatted text to stdout."""
    print_styled("Build complete!", color="green", bold=True)

    captured = capsys.readouterr()
    assert "Build complete!" in captured.out
    assert captured.err == ""


def test_easy_terminal_show_prints_expected_content(capsys):
    """Verify EasyTerminal.show() outputs clean text."""
    terminal = EasyTerminal("Deploying service...")
    terminal.show()

    captured = capsys.readouterr()
    assert captured.out == "Deploying service...\n"


def test_print_rule_with_custom_columns(monkeypatch, capsys):
    """Verify print_rule adapts cleanly to simulated terminal width."""
    monkeypatch.setenv("COLUMNS", "40")
    print_rule("System Status")

    captured = capsys.readouterr()
    assert "System Status" in captured.out


def test_print_table_renders_headers_and_rows(capsys):
    """Verify print_table renders column headers and associated values."""
    table_data = {
        "Service": ["API Gateway", "Database"],
        "Status": ["Online", "Healthy"],
    }
    print_table(table_data, style="cyan")

    captured = capsys.readouterr()
    assert "Service" in captured.out
    assert "Status" in captured.out
    assert "API Gateway" in captured.out
    assert "Healthy" in captured.out


def test_mocking_user_prompt_input(monkeypatch, capsys):
    """Simulate user interactive input without pausing test execution."""

    def mock_cli_prompt(message: str) -> bool:
        print(message)
        response = input().strip().lower()
        return response in ("y", "yes")

    # Simulate user typing 'y'
    monkeypatch.setattr("builtins.input", lambda: "y")

    result = mock_cli_prompt("Continue with migration? (y/n)")
    assert result is True

    captured = capsys.readouterr()
    assert "Continue with migration?" in captured.out
```

Run the test from the repository root:

=== "Using uv"
    ```bash
    uv run pytest tests/test_terminal_demo.py
    ```

=== "Using pip"
    ```bash
    pytest tests/test_terminal_demo.py
    ```

When you see green passing tests, delete `tests/test_terminal_demo.py`.

---

## Fill-in-the-blanks test template

Copy this template into your module's test file in `tests/`:

```python
import pytest
from py_simple_package.src.py_simple.<your_module> import <your_cli_function>


def test_<function_name>_standard_output(capsys):
    """Check that <function_name> prints the expected output string."""
    <your_cli_function>("Sample argument")

    captured = capsys.readouterr()
    assert "<expected_snippet>" in captured.out
    assert captured.err == ""


def test_<function_name>_custom_styling_or_width(monkeypatch, capsys):
    """Check output behavior under controlled terminal environment settings."""
    monkeypatch.setenv("COLUMNS", "80")
    <your_cli_function>("Sample title")

    captured = capsys.readouterr()
    assert "<expected_title>" in captured.out


def test_<function_name>_simulated_user_input(monkeypatch, capsys):
    """Check prompts that accept simulated user response without blocking."""
    # Mock built-in input to provide a deterministic string
    monkeypatch.setattr("builtins.input", lambda: "yes")

    result = <your_cli_function>("Confirm action?")

    assert result is True
    captured = capsys.readouterr()
    assert "Confirm action?" in captured.out
```

---

## How it works

### 1. Capturing terminal text with `capsys`

Pytest's built-in fixture `capsys` intercepts anything written to standard output (`sys.stdout`) or standard error (`sys.stderr`):

```python
captured = capsys.readouterr()
captured.out  # String containing standard output
captured.err  # String containing standard error
```

Calling `readouterr()` clears the capture buffer. Any subsequent prints will accumulate fresh in the next `readouterr()` call.

### 2. Mocking terminal environment with `monkeypatch`

CLI helpers often inspect terminal characteristics like column width via `os.environ.get("COLUMNS")` or `shutil.get_terminal_size()`. Use pytest's `monkeypatch` fixture to safely override them for the duration of the test:

```python
monkeypatch.setenv("COLUMNS", "60")
```

After the test finishes, pytest automatically restores the original environment variables.

### 3. Preventing hangs on interactive prompts

Functions that ask the user for confirmation (e.g., `input("Are you sure? ")`) will freeze automated test suites unless mocked. Use `monkeypatch.setattr("builtins.input", ...)` to supply automated answers:

```python
# Provide an affirmative answer
monkeypatch.setattr("builtins.input", lambda: "yes")

# Or provide a sequence of inputs for multi-prompt functions
responses = iter(["name", "25", "confirm"])
monkeypatch.setattr("builtins.input", lambda: next(responses))
```

---

## Checklist before opening a PR

- [ ] Does every terminal function that writes to `stdout` or `stderr` have a test with `capsys`?
- [ ] Did you assert that `captured.err == ""` unless the test specifically checks error logging?
- [ ] Are interactive prompts mocked with `monkeypatch.setattr("builtins.input", ...)` so test runners never hang?
- [ ] Did you test both basic and styled configurations?
- [ ] Do all tests pass locally with `uv run pytest`?
