"""Beginner-friendly helpers for hex and RGB color handling."""

import random
import re

LUMINANCE_WEIGHTS: tuple[float, float, float] = (0.2126, 0.7152, 0.0722)
LUMINANCE_LIGHT_THRESHOLD: float = 0.179
SRGB_LINEAR_THRESHOLD: float = 0.03928
SRGB_LINEAR_DIVISOR: float = 12.92
SRGB_GAMMA_OFFSET: float = 0.055
SRGB_GAMMA_DIVISOR: float = 1.055
SRGB_GAMMA_EXPONENT: float = 2.4


def is_valid_hex(hex_code: str) -> bool:
    """
    Checks whether a string is a valid hex color code.

    Supports 3-digit and 6-digit hex color formats, with or without
    a leading '#' prefix.

    Args:
        hex_code (str): Color string to check.

    Returns:
        bool: True if hex_code is a valid hex color, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_valid_hex

            is_valid_hex("#FFFFFF")  # -> True
            is_valid_hex("fff")  # -> True
            is_valid_hex("invalid")  # -> False
            ```

        === "The Traditional Way"
            ```python
            import re

            hex_code = "#FFFFFF"
            cleaned = hex_code.lstrip("#")
            is_valid = len(cleaned) in (3, 6) and all(
                c in "0123456789abcdefABCDEF" for c in cleaned
            )
            ```
    """
    if not isinstance(hex_code, str):
        return False

    cleaned = hex_code.lstrip("#")
    if len(cleaned) not in (3, 6):
        return False

    return bool(re.fullmatch(r"[0-9a-fA-F]+", cleaned))


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    """
    Converts a hex color code string to an (R, G, B) integer tuple.

    Supports 3-digit and 6-digit hex color codes with or without '#'.

    Args:
        hex_code (str): Hex color string to convert (e.g., "#FFFFFF" or "fff").

    Returns:
        tuple[int, int, int]: RGB values as (r, g, b) integers in range 0-255.

    Raises:
        ValueError: If hex_code is not a valid hex color.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hex_to_rgb

            hex_to_rgb("#FFFFFF")  # -> (255, 255, 255)
            hex_to_rgb("00ff00")  # -> (0, 255, 0)
            ```

        === "The Traditional Way"
            ```python
            hex_code = "#FFFFFF".lstrip("#")
            if len(hex_code) == 3:
                hex_code = "".join(c * 2 for c in hex_code)
            r, g, b = tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
            ```
    """
    if not is_valid_hex(hex_code):
        raise ValueError(f"Invalid hex color code: '{hex_code}'")

    cleaned = hex_code.lstrip("#")
    if len(cleaned) == 3:
        cleaned = "".join(character * 2 for character in cleaned)

    r = int(cleaned[0:2], 16)
    g = int(cleaned[2:4], 16)
    b = int(cleaned[4:6], 16)

    return r, g, b


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Converts (R, G, B) color values to a hex color string.

    Args:
        r (int): Red channel value (0 to 255).
        g (int): Green channel value (0 to 255).
        b (int): Blue channel value (0 to 255).

    Returns:
        str: Uppercase hex color string (e.g., "#FFFFFF").

    Raises:
        ValueError: If any channel is outside the 0-255 range.
        TypeError: If any channel is not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import rgb_to_hex

            rgb_to_hex(255, 255, 255)  # -> "#FFFFFF"
            rgb_to_hex(0, 128, 64)  # -> "#008040"
            ```

        === "The Traditional Way"
            ```python
            r, g, b = 255, 255, 255
            hex_code = f"#{r:02X}{g:02X}{b:02X}"
            ```
    """
    for name, val in [("r", r), ("g", g), ("b", b)]:
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(f"Color channel '{name}' must be an integer.")
        if not (0 <= val <= 255):
            raise ValueError(
                f"Color channel '{name}' must be between 0 and 255, got {val}."
            )

    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    """
    Converts (R, G, B) color values to an (H, S, L) tuple.

    Hue is measured in degrees (0-360), while Saturation and Lightness
    are measured as percentages (0-100).

    Args:
        r (int): Red channel value (0 to 255).
        g (int): Green channel value (0 to 255).
        b (int): Blue channel value (0 to 255).

    Returns:
        tuple[float, float, float]: HSL values as (h, s, l), where h is in
        the 0-360 range and s/l are percentages in the 0-100 range.

    Raises:
        ValueError: If any channel is outside the 0-255 range.
        TypeError: If any channel is not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import rgb_to_hsl

            rgb_to_hsl(255, 0, 0)  # -> (0.0, 100.0, 50.0)
            rgb_to_hsl(18, 52, 86)  # -> (210.0, 65.38, 20.39)
            ```

        === "The Traditional Way"
            ```python
            r, g, b = 18, 52, 86
            r, g, b = r / 255, g / 255, b / 255
            color_max, color_min = max(r, g, b), min(r, g, b)
            delta = color_max - color_min
            lightness = (color_max + color_min) / 2
            if delta == 0:
                hue = saturation = 0
            else:
                saturation = delta / (1 - abs(2 * lightness - 1))
                if color_max == r:
                    hue = (60 * ((g - b) / delta)) % 360
                elif color_max == g:
                    hue = 60 * ((b - r) / delta) + 120
                else:
                    hue = 60 * ((r - g) / delta) + 240
            ```
    """
    for name, val in [("r", r), ("g", g), ("b", b)]:
        if not isinstance(val, int) or isinstance(val, bool):
            raise TypeError(f"Color channel '{name}' must be an integer.")
        if not (0 <= val <= 255):
            raise ValueError(
                f"Color channel '{name}' must be between 0 and 255, got {val}."
            )

    red, green, blue = r / 255, g / 255, b / 255
    color_max = max(red, green, blue)
    color_min = min(red, green, blue)
    delta = color_max - color_min

    lightness = (color_max + color_min) / 2

    if delta == 0:
        hue = 0.0
        saturation = 0.0
    else:
        saturation = delta / (1 - abs(2 * lightness - 1))
        if color_max == red:
            hue = (60 * ((green - blue) / delta)) % 360
        elif color_max == green:
            hue = 60 * ((blue - red) / delta) + 120
        else:
            hue = 60 * ((red - green) / delta) + 240

    return round(hue % 360, 2), round(saturation * 100, 2), round(lightness * 100, 2)


def hsl_to_rgb(h: float, s: float, lightness: float) -> tuple[int, int, int]:
    """
    Converts an (H, S, L) color to an (R, G, B) integer tuple.

    Hue is measured in degrees (0-360), while Saturation and Lightness
    are measured as percentages (0-100).

    Args:
        h (float): Hue in degrees (0 to 360).
        s (float): Saturation as a percentage (0 to 100).
        lightness (float): Lightness as a percentage (0 to 100).

    Returns:
        tuple[int, int, int]: RGB values as (r, g, b) integers in range 0-255.

    Raises:
        ValueError: If hue is outside the 0-360 range or saturation/lightness
            are outside the 0-100 range.
        TypeError: If any value is not an int or float.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hsl_to_rgb

            hsl_to_rgb(120, 100, 50)  # -> (0, 255, 0)
            hsl_to_rgb(0, 0, 100)  # -> (255, 255, 255)
            ```

        === "The Traditional Way"
            ```python
            h, s, lightness = 120, 100, 50
            s, lightness = s / 100, lightness / 100
            chroma = (1 - abs(2 * lightness - 1)) * s
            secondary = chroma * (1 - abs((h / 60) % 2 - 1))
            match = lightness - chroma / 2
            if h < 60:
                red, green, blue = chroma, secondary, 0
            elif h < 120:
                red, green, blue = secondary, chroma, 0
            elif h < 180:
                red, green, blue = 0, chroma, secondary
            elif h < 240:
                red, green, blue = 0, secondary, chroma
            elif h < 300:
                red, green, blue = secondary, 0, chroma
            else:
                red, green, blue = chroma, 0, secondary
            r = round((red + match) * 255)
            g = round((green + match) * 255)
            b = round((blue + match) * 255)
            ```
    """
    for name, val, color_min, color_max in [
        ("h", h, 0, 360),
        ("s", s, 0, 100),
        ("lightness", lightness, 0, 100),
    ]:
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError(f"Color value '{name}' must be an int or a float.")
        if not (color_min <= val <= color_max):
            raise ValueError(
                f"Color value '{name}' must be between {color_min} and "
                f"{color_max}, got {val}."
            )

    saturation, lightness = s / 100, lightness / 100
    chroma = (1 - abs(2 * lightness - 1)) * saturation
    secondary = chroma * (1 - abs((h / 60) % 2 - 1))
    match = lightness - chroma / 2

    if h < 60:
        red, green, blue = chroma, secondary, 0
    elif h < 120:
        red, green, blue = secondary, chroma, 0
    elif h < 180:
        red, green, blue = 0, chroma, secondary
    elif h < 240:
        red, green, blue = 0, secondary, chroma
    elif h < 300:
        red, green, blue = secondary, 0, chroma
    else:
        red, green, blue = chroma, 0, secondary

    return (
        round((red + match) * 255),
        round((green + match) * 255),
        round((blue + match) * 255),
    )


def random_hex_color() -> str:
    """
    Returns a random valid hex color string in uppercase #RRGGBB format.

    Returns:
        str: Uppercase hex color string (e.g., "#FFFFFF").

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import random_hex_color

            color = random_hex_color()  # -> e.g. "#A1B2C3"
            ```

        === "The Traditional Way"
            ```python
            import random

            color = f"#{random.randint(0, 0xFFFFFF):06X}"
            ```
    """
    return f"#{random.randint(0, 0xFFFFFF):06X}"


def is_light_color(hex_code: str, threshold: float = LUMINANCE_LIGHT_THRESHOLD) -> bool:
    """
    Takes a hex color and returns whether it's "light" based on perceived luminance.
    Uses the sRGB relative luminance formula (ITU-R BT.709 weights).
    Threshold ~0.179 is commonly used for WCAG contrast calculations.

    Args:
        hex_code (str): Hex color string to convert (e.g., "#FFFFFF" or "fff").
        threshold (float): Luminance threshold for "light" classification
            (default 0.179).

    Returns:
        bool: True if it's "light" based on perceived luminance.

    Raises:
        ValueError: If hex_code is not a valid hex color.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_light_color

            is_light_color("#FFFFFF")  # -> True
            is_light_color("#000000")  # -> False
            ```

        === "The Traditional Way"
            ```python
            hex_code = "#FFFFFF".lstrip("#")
            if len(hex_code) == 3:
                hex_code = "".join(c * 2 for c in hex_code)
            r, g, b = (int(hex_code[i:i + 2], 16) / 255 for i in (0, 2, 4))

            def linearize(c):
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

            luminance = sum(w * linearize(v)
                            for w, v in zip((0.2126, 0.7152, 0.0722), (r, g, b)))
            is_light = luminance > 0.179  # -> True
            ```
    """

    def linearize(c: float) -> float:
        if c <= SRGB_LINEAR_THRESHOLD:
            return c / SRGB_LINEAR_DIVISOR
        return ((c + SRGB_GAMMA_OFFSET) / SRGB_GAMMA_DIVISOR) ** SRGB_GAMMA_EXPONENT

    r, g, b = hex_to_rgb(hex_code)

    r_srgb = r / 255.0
    g_srgb = g / 255.0
    b_srgb = b / 255.0

    r_lin = linearize(r_srgb)
    g_lin = linearize(g_srgb)
    b_lin = linearize(b_srgb)

    r_weight, g_weight, b_weight = LUMINANCE_WEIGHTS
    luminance = r_weight * r_lin + g_weight * g_lin + b_weight * b_lin

    return luminance > threshold


def _relative_luminance(hex_code: str) -> float:
    """
    Calculates WCAG relative luminance for a hex color.

    Uses sRGB linearization and ITU-R BT.709 luminance weights.

    Args:
        hex_code (str): Hex color string to convert (e.g., "#FFFFFF" or "fff").

    Returns:
        float: Relative luminance value in range 0.0 to 1.0.

    Raises:
        ValueError: If hex_code is not a valid hex color.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple.easy_colors import _relative_luminance

            _relative_luminance("#FFFFFF")  # -> 1.0
            _relative_luminance("#000000")  # -> 0.0
            ```

        === "The Traditional Way"
            ```python
            hex_code = "#FFFFFF".lstrip("#")
            if len(hex_code) == 3:
                hex_code = "".join(c * 2 for c in hex_code)

            r, g, b = (int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

            def adjust(channel):
                c = channel / 255.0
                return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

            luminance = (
                0.2126 * adjust(r) +
                0.7152 * adjust(g) +
                0.0722 * adjust(b)
            )
            ```
    """
    r, g, b = hex_to_rgb(hex_code)

    def adjust(channel: int) -> float:
        c = channel / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r_lin, g_lin, b_lin = adjust(r), adjust(g), adjust(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def hex_to_rgba(hex_code: str, alpha: float) -> tuple[int, int, int, float]:
    """
    Converts a hex color and alpha value into an (R, G, B, A) tuple.

    Args:
        hex_code (str): Hex color string to convert (e.g., "#FFFFFF" or "fff").
        alpha (float): Alpha channel value in range 0.0 to 1.0.

    Returns:
        tuple[int, int, int, float]: RGBA values as (r, g, b, alpha).

    Raises:
        ValueError: If hex_code is not a valid hex color.
        ValueError: If alpha is outside the 0.0-1.0 range.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hex_to_rgba

            hex_to_rgba("#FF0000", 0.5)  # -> (255, 0, 0, 0.5)
            hex_to_rgba("00ff00", 1.0)  # -> (0, 255, 0, 1.0)
            ```

        === "The Traditional Way"
            ```python
            hex_code = "#FF0000".lstrip("#")
            if len(hex_code) == 3:
                hex_code = "".join(c * 2 for c in hex_code)

            r = int(hex_code[0:2], 16)
            g = int(hex_code[2:4], 16)
            b = int(hex_code[4:6], 16)
            alpha = 0.5
            rgba = (r, g, b, alpha)
            ```
    """
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("Alpha must be between 0.0 and 1.0")

    r, g, b = hex_to_rgb(hex_code)
    return (r, g, b, alpha)


def contrast_ratio(hex1: str, hex2: str) -> float:
    """
    Calculates WCAG contrast ratio between two hex colors.

    Args:
        hex1 (str): First hex color string (e.g., "#000000").
        hex2 (str): Second hex color string (e.g., "#FFFFFF").

    Returns:
        float: Contrast ratio between the two colors.

    Raises:
        ValueError: If either hex color is not valid.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import contrast_ratio

            contrast_ratio("#000000", "#FFFFFF")  # -> 21.0
            contrast_ratio("#777777", "#FFFFFF")  # -> 4.48
            ```

        === "The Traditional Way"
            ```python
            def contrast(l1, l2):
                lighter = max(l1, l2)
                darker = min(l1, l2)
                return (lighter + 0.05) / (darker + 0.05)

            l_black = 0.0
            l_white = 1.0
            ratio = contrast(l_black, l_white)  # -> 21.0
            ```
    """
    lum1 = _relative_luminance(hex1)
    lum2 = _relative_luminance(hex2)

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)
