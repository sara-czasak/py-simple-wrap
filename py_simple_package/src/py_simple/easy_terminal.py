"""
easy_terminal is meant to make it easy to get styled output in the terminal.
Built on top of the rich library — no more memorizing markup strings.
"""

from __future__ import annotations


class EasyTerminal:
    """
    Builds styled terminal text by chaining style methods, then prints it.

    Nothing is printed until show() is called, so you can chain as many
    styles as you like first. Every set_* method returns the object itself,
    which is what makes the chaining work.

    Args:
        text (str): The text to print.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import EasyTerminal

            EasyTerminal("Hello World").set_color("red").set_bold().show()
            ```

        === "The Traditional Way"
            ```python
            from rich.console import Console

            console = Console()
            console.print("Hello World", style="bold red")
            ```
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.color = "#ffffff"
        self.bg_color = None
        self.color_scheme = None
        self.weight = None
        self.styles = {}
        self.style_chain = None

    def set_color(self, color: str) -> EasyTerminal:
        """
        Sets the text color and returns the object so you can keep chaining.

        Args:
            color (str): A color name ("red"), a hex code ("#ff0000"),
                or an rgb string ("rgb(255,0,0)").

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_color("#ff0000").show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="#ff0000")
                ```
        """
        self.color = color
        return self

    def set_bg_color(self, color: str) -> EasyTerminal:
        """
        Sets the background color and returns the object for chaining.

        Args:
            color (str): A color name ("blue"), a hex code ("#0000ff"),
                or an rgb string ("rgb(0,0,255)").

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_color("white").set_bg_color("blue").show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="white on blue")
                ```
        """
        self.bg_color = color
        return self

    def set_bold(self) -> EasyTerminal:
        """
        Makes the text bold and returns the object for chaining.

        Replaces any weight set earlier, so calling set_bold() after
        set_light_weight() leaves the text bold, not both.

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_bold().show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="bold")
                ```
        """
        self.weight = "bold"
        self.styles["weight"] = self.weight
        return self

    def set_light_weight(self) -> EasyTerminal:
        """
        Makes the text dim (lighter than normal) and returns the object.

        Terminals only have bold, normal and dim, so this is the lightest
        weight available. It replaces any weight set earlier.

        Returns:
            EasyTerminal: The same object, ready for the next call.

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello").set_light_weight().show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello", style="dim")
                ```
        """
        self.weight = "dim"
        self.styles["weight"] = self.weight
        return self

    def _check_color_scheme(self) -> EasyTerminal:
        """Combines the text and background colors into one rich style."""
        if self.bg_color is not None:
            self.color_scheme = f"{self.color} on {self.bg_color}"
        else:
            self.color_scheme = self.color
        self.styles["color_scheme"] = self.color_scheme
        return self

    def _chain_styles(self) -> EasyTerminal:
        """Joins all chosen styles into a single space-separated string."""
        self._check_color_scheme()
        style_list = list(self.styles.values())
        style_list = [i for i in style_list if i is not None]
        self.style_chain = " ".join(style_list)
        return self

    def show(self) -> None:
        """
        Prints the text to the terminal with all the chosen styles.

        Call this last. Anything you didn't set falls back to the terminal's
        normal look (the text color defaults to white).

        Example:
            === "The Py_simple Way"
                ```python
                from py_simple import EasyTerminal

                EasyTerminal("Hello World").set_color("red").set_bg_color("white").set_bold().show()
                ```

            === "The Traditional Way"
                ```python
                from rich.console import Console

                console = Console()
                console.print("Hello World", style="bold red on white")
                ```
        """
        from rich.console import Console

        self._chain_styles()

        c = Console()
        c.print(self.text, style=self.style_chain)


def print_styled(
    text: str,
    color: str = "#ffffff",
    bg_color: str | None = None,
    bold: bool = False,
    dim: bool = False,
) -> None:
    """
    Prints styled text to the terminal in a single function call.

    Args:
        text (str): The text to print.
        color (str, optional): Text color name ("red"), hex code ("#ff0000"),
            or rgb string ("rgb(255,0,0)"). Defaults to `"#ffffff"`.
        bg_color (str, optional): Background color name ("blue"), hex code
            ("#0000ff"), or rgb string. Defaults to `None`.
        bold (bool, optional): Whether to make the text bold. Defaults to `False`.
            If both `bold` and `dim` are True, `bold` takes precedence.
        dim (bool, optional): Whether to make the text dim (light weight).
            Defaults to `False`. Ignored if `bold` is also True.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import print_styled

            print_styled("Hello World", color="red", bg_color="white", bold=True)
            ```

        === "The Traditional Way"
            ```python
            from rich.console import Console

            console = Console()
            console.print("Hello World", style="bold red on white")
            ```
    """
    terminal = EasyTerminal(str(text)).set_color(color)
    if bg_color is not None:
        terminal.set_bg_color(bg_color)
    if bold:
        terminal.set_bold()
    elif dim:
        terminal.set_light_weight()
    terminal.show()


def print_centered(text: str, width: int | None = None) -> None:
    """
    Prints text centered across the terminal width.

    A one-line way to center a heading or message without working out
    the padding yourself. When no width is given, the current terminal
    width is used.

    Args:
        text (str): The text to print.
        width (int, optional): Width to center within. Defaults to the
            current terminal width.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import print_centered

            print_centered("Hello World")
            ```

        === "The Traditional Way"
            ```python
            from rich.align import Align
            from rich.console import Console

            Console().print(Align.center("Hello World"))
            ```
    """
    import shutil

    from rich.align import Align
    from rich.console import Console

    if width is None:
        width = shutil.get_terminal_size().columns
    Console(width=width).print(Align.center(str(text)))


def print_rule(title: str = "") -> None:
    """
    Print a horizontal divider with an optional centered heading.

    Uses the current console width. Rich fits or shortens the heading
    when the console is narrow; the exact divider depends on the console.

    Args:
        title (str, optional): Heading to show as literal text, without
            interpreting Rich markup. Defaults to an empty string for
            a plain divider. Values are converted to strings, as with
            `print_centered()`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import print_rule

            print_rule("Results")
            ```

        === "The Traditional Way"
            ```python
            from rich.console import Console
            from rich.text import Text

            Console().rule(Text("Results"))
            ```
    """
    from rich.console import Console
    from rich.text import Text

    Console().rule(Text(str(title)))
