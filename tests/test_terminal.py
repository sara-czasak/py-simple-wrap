import pytest

from py_simple_package.src.py_simple import (
    print_centered as public_print_centered,
    print_styled as public_print_styled,
)
from py_simple_package.src.py_simple.easy_terminal import (
    EasyTerminal,
    print_centered,
    print_rule,
    print_styled,
)


def test_init_default_color():
    terminal = EasyTerminal("Hello")
    assert terminal.color == "#ffffff"


def test_init_defaults():
    terminal = EasyTerminal("Hello")
    assert terminal.bg_color is None
    assert terminal.color_scheme is None
    assert terminal.weight is None
    assert terminal.styles == {}
    assert terminal.style_chain is None


def test_set_color():
    terminal = EasyTerminal("Hello")
    colors = [
        "red",
        "blue",
        "green",
        "yellow",
        "#bee6c9",
        "#99238d",
        "#1c0219",
        "#454138",
    ]
    for color in colors:
        result = terminal.set_color(color)
        assert terminal.color == color
        assert result is terminal


def test_set_bg_color():
    terminal = EasyTerminal("Hello")
    colors = [
        "red",
        "blue",
        "green",
        "yellow",
        "#bee6c9",
        "#99238d",
        "#1c0219",
        "#454138",
    ]
    for color in colors:
        result = terminal.set_bg_color(color)
        assert terminal.bg_color == color
        assert result is terminal


def test_set_bold():
    terminal = EasyTerminal("Hello")
    result = terminal.set_bold()
    assert terminal.weight == "bold"
    assert terminal.styles["weight"] == "bold"
    assert result is terminal


def test_set_light_weight():
    terminal = EasyTerminal("Hello")
    result = terminal.set_light_weight()
    assert terminal.weight == "dim"
    assert terminal.styles["weight"] == "dim"
    assert result is terminal


def test_weight_replaces_previous():
    terminal = EasyTerminal("Hello")
    terminal.set_bold()
    terminal.set_light_weight()
    assert terminal.weight == "dim"
    assert terminal.styles["weight"] == "dim"


def test_check_color_scheme_without_bg():
    terminal = EasyTerminal("Hello")
    terminal.set_color("red")
    terminal._check_color_scheme()
    assert terminal.color_scheme == "red"


def test_check_color_scheme_with_bg():
    terminal = EasyTerminal("Hello")
    terminal.set_color("red")
    terminal.set_bg_color("blue")
    terminal._check_color_scheme()
    assert terminal.color_scheme == "red on blue"


def test_chain_styles_combines_everything():
    terminal = EasyTerminal("Hello")
    terminal.set_color("red")
    terminal.set_bg_color("blue")
    terminal.set_bold()
    terminal._chain_styles()
    assert terminal.style_chain == "bold red on blue"


def test_show_prints_text(capsys):
    terminal = EasyTerminal("Hello World")
    terminal.show()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"


def test_show_with_styles_still_prints_text(capsys):
    terminal = (
        EasyTerminal("Hello World").set_color("red").set_bg_color("blue").set_bold()
    )
    terminal.show()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"


def test_print_styled_prints_text(capsys):
    print_styled("Simple text")
    captured = capsys.readouterr()
    assert captured.out == "Simple text\n"


def test_print_styled_with_styles(capsys):
    print_styled("Styled", color="green", bg_color="yellow", bold=True)
    captured = capsys.readouterr()
    assert captured.out == "Styled\n"


def test_print_styled_with_dim(capsys):
    print_styled("Dimmed text", color="cyan", dim=True)
    captured = capsys.readouterr()
    assert captured.out == "Dimmed text\n"


def test_print_styled_delegates_to_easy_terminal(monkeypatch):
    calls = []

    class DummyTerminal:
        def __init__(self, text):
            calls.append(("init", text))

        def set_color(self, color):
            calls.append(("set_color", color))
            return self

        def set_bg_color(self, bg_color):
            calls.append(("set_bg_color", bg_color))
            return self

        def set_bold(self):
            calls.append(("set_bold",))
            return self

        def set_light_weight(self):
            calls.append(("set_light_weight",))
            return self

        def show(self):
            calls.append(("show",))

    monkeypatch.setattr(
        "py_simple_package.src.py_simple.easy_terminal.EasyTerminal",
        DummyTerminal,
    )

    print_styled("Test message", color="red", bg_color="blue", bold=True)
    assert calls == [
        ("init", "Test message"),
        ("set_color", "red"),
        ("set_bg_color", "blue"),
        ("set_bold",),
        ("show",),
    ]

    calls.clear()
    print_styled("Test 2", color="green", dim=True)
    assert calls == [
        ("init", "Test 2"),
        ("set_color", "green"),
        ("set_light_weight",),
        ("show",),
    ]

    calls.clear()
    print_styled("Both weights", bold=True, dim=True)
    assert calls == [
        ("init", "Both weights"),
        ("set_color", "#ffffff"),
        ("set_bold",),
        ("show",),
    ]
    assert ("set_light_weight",) not in calls


def test_print_styled_both_bold_and_dim_output(capsys):
    print_styled("Both bold and dim", bold=True, dim=True)
    captured = capsys.readouterr()
    assert captured.out == "Both bold and dim\n"


def test_print_styled_public_import():
    assert public_print_styled is print_styled


def test_print_centered_with_explicit_width(capsys):
    print_centered("Hi", width=10)
    assert capsys.readouterr().out == "    Hi    \n"


def test_print_centered_uses_terminal_width(monkeypatch, capsys):
    import os
    import shutil

    monkeypatch.setattr(
        shutil,
        "get_terminal_size",
        lambda *args, fallback=None, **kwargs: os.terminal_size((10, 24)),
    )
    print_centered("Hi")
    assert capsys.readouterr().out == "    Hi    \n"


def test_print_centered_long_text_does_not_crash(capsys):
    print_centered("toolongtext", width=5)
    out = capsys.readouterr().out.replace("\n", "").replace(" ", "")
    assert out == "toolongtext"


def test_print_centered_public_import():
    assert public_print_centered is print_centered


def test_print_rule_default_heading(monkeypatch, capsys):
    monkeypatch.setenv("COLUMNS", "20")
    assert print_rule() is None
    captured = capsys.readouterr()
    assert captured.out == "─" * 20 + "\n"
    assert captured.err == ""


@pytest.mark.parametrize(
    "title,expected",
    [
        ("", "─" * 20 + "\n"),
        ("Hi", "──────── Hi ────────\n"),
        ("雪", "──────── 雪 ────────\n"),
        ("café", "─────── café ───────\n"),
        ("[red]", "────── [red] ───────\n"),
        (42, "──────── 42 ────────\n"),
    ],
)
def test_print_rule_heading_output(title, expected, monkeypatch, capsys):
    monkeypatch.setenv("COLUMNS", "20")
    assert print_rule(title) is None
    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""


@pytest.mark.parametrize("width", [1, 3, 8, 20])
@pytest.mark.parametrize(
    "title", ["", "A very long heading", "雪と月", "[bold]literal[/bold]"]
)
def test_print_rule_fits_narrow_console(width, title, monkeypatch, capsys):
    from rich.cells import cell_len

    monkeypatch.setenv("COLUMNS", str(width))
    print_rule(title)
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert len(lines) == 1
    assert 0 < cell_len(lines[0]) <= width
    assert "\x1b[" not in captured.out
    assert captured.err == ""


def test_print_rule_output_is_late_bound_to_stdout(monkeypatch, capsys):
    monkeypatch.setenv("COLUMNS", "20")
    print_rule("First")
    first = capsys.readouterr()
    print_rule("Second")
    second = capsys.readouterr()
    assert "First" in first.out and "Second" not in first.out
    assert "Second" in second.out and "First" not in second.out


def test_print_rule_public_imports(monkeypatch, capsys):
    from py_simple import print_rule as public_print
    from py_simple.easy_terminal import print_rule as module_print

    monkeypatch.setenv("COLUMNS", "20")
    assert public_print is module_print
    public_print(title="Hi")
    assert capsys.readouterr().out == "──────── Hi ────────\n"
