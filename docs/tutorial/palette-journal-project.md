# Building a Palette Journal with Easy Colors and Easy File Manager

Combine **Easy Colors** and **Easy File Manager** to collect random colors
in a text file you can open later.

## What we are building

A small journal that picks a color, says whether it is light or dark, and
appends that note to `palette.txt`. Run it once for each new swatch.

```python
from py_simple import add_a_line, hex_to_rgb, is_light_color, random_hex_color

color = random_hex_color()
kind = "light" if is_light_color(color) else "dark"
red, green, blue = hex_to_rgb(color)

add_a_line(
    "palette.txt",
    f"{color} is {kind} (rgb {red}, {green}, {blue})",
)
```

Example line appended to `palette.txt`:

```text
#A1B2C3 is light (rgb 161, 178, 195)
```

The hex value changes every run. The shape of the line stays the same.

## What happened?

1. `random_hex_color()` returns a color such as `#A1B2C3`.
2. `is_light_color()` decides whether text on that color should be dark or
   light, which is handy when you paint a button.
3. `hex_to_rgb()` turns the same color into red, green, and blue numbers.
4. `add_a_line()` creates `palette.txt` if it is missing and adds one line.
   The next run adds another line under the first.

## Why use these helpers?

A random hex color, a lightness check, and an RGB conversion are three
separate recipes if you write them yourself. Appending a line also means
opening a file in append mode and adding a newline. These helpers keep the
journal script focused on the color you want to remember.
