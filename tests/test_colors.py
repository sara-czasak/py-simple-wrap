import pytest

from py_simple_package.src.py_simple.easy_colors import (
    contrast_ratio,
    hex_to_rgb,
    hex_to_rgba,
    hsl_to_rgb,
    is_light_color,
    is_valid_hex,
    random_hex_color,
    rgb_to_hex,
    rgb_to_hsl,
)


@pytest.mark.parametrize(
    "hex_code, expected",
    [
        ("#FFFFFF", True),
        ("#ffffff", True),
        ("FFFFFF", True),
        ("ffffff", True),
        ("#FFF", True),
        ("#fff", True),
        ("FFF", True),
        ("fff", True),
        ("#000000", True),
        ("#123456", True),
        ("#abcDEF", True),
        ("123456", True),
        ("#GGGGGG", False),
        ("#12345", False),
        ("#1234567", False),
        ("xyz", False),
        ("", False),
        (None, False),
        (123456, False),
    ],
)
def test_is_valid_hex(hex_code, expected):
    assert is_valid_hex(hex_code) is expected


@pytest.mark.parametrize(
    "hex_code, expected",
    [
        ("#FFFFFF", (255, 255, 255)),
        ("#ffffff", (255, 255, 255)),
        ("FFFFFF", (255, 255, 255)),
        ("#000000", (0, 0, 0)),
        ("#00ff00", (0, 255, 0)),
        ("#123456", (18, 52, 86)),
        ("#FFF", (255, 255, 255)),
        ("fff", (255, 255, 255)),
        ("#000", (0, 0, 0)),
        ("f0a", (255, 0, 170)),
    ],
)
def test_hex_to_rgb_valid(hex_code, expected):
    assert hex_to_rgb(hex_code) == expected


@pytest.mark.parametrize(
    "invalid_hex",
    [
        "#GGGGGG",
        "#12345",
        "#1234567",
        "invalid",
        "",
        "1234567",
    ],
)
def test_hex_to_rgb_invalid(invalid_hex):
    with pytest.raises(ValueError):
        hex_to_rgb(invalid_hex)


@pytest.mark.parametrize(
    "r, g, b, expected",
    [
        (255, 255, 255, "#FFFFFF"),
        (0, 0, 0, "#000000"),
        (0, 255, 0, "#00FF00"),
        (18, 52, 86, "#123456"),
        (255, 0, 170, "#FF00AA"),
    ],
)
def test_rgb_to_hex_valid(r, g, b, expected):
    assert rgb_to_hex(r, g, b) == expected


@pytest.mark.parametrize(
    "r, g, b",
    [
        (-1, 0, 0),
        (0, 256, 0),
        (0, 0, 300),
        (-255, 0, 0),
    ],
)
def test_rgb_to_hex_out_of_range(r, g, b):
    with pytest.raises(ValueError):
        rgb_to_hex(r, g, b)


@pytest.mark.parametrize(
    "r, g, b",
    [
        ("255", 255, 255),
        (255, 255.0, 255),
        (True, 255, 255),
        (255, None, 255),
    ],
)
def test_rgb_to_hex_invalid_types(r, g, b):
    with pytest.raises(TypeError):
        rgb_to_hex(r, g, b)


@pytest.mark.parametrize(
    "r, g, b, expected",
    [
        (255, 0, 0, (0.0, 100.0, 50.0)),
        (0, 255, 0, (120.0, 100.0, 50.0)),
        (0, 0, 255, (240.0, 100.0, 50.0)),
        (255, 255, 255, (0.0, 0.0, 100.0)),
        (0, 0, 0, (0.0, 0.0, 0.0)),
        (128, 128, 128, (0.0, 0.0, 50.2)),
        (18, 52, 86, (210.0, 65.38, 20.39)),
    ],
)
def test_rgb_to_hsl_valid(r, g, b, expected):
    assert rgb_to_hsl(r, g, b) == expected


@pytest.mark.parametrize(
    "r, g, b",
    [
        (-1, 0, 0),
        (0, 256, 0),
        (0, 0, 300),
        (-255, 0, 0),
    ],
)
def test_rgb_to_hsl_out_of_range(r, g, b):
    with pytest.raises(ValueError):
        rgb_to_hsl(r, g, b)


@pytest.mark.parametrize(
    "r, g, b",
    [
        ("255", 255, 255),
        (255, 255.0, 255),
        (True, 255, 255),
        (255, None, 255),
    ],
)
def test_rgb_to_hsl_invalid_types(r, g, b):
    with pytest.raises(TypeError):
        rgb_to_hsl(r, g, b)


@pytest.mark.parametrize(
    "h, s, lightness, expected",
    [
        (0, 100, 50, (255, 0, 0)),
        (120, 100, 50, (0, 255, 0)),
        (240, 100, 50, (0, 0, 255)),
        (0, 0, 100, (255, 255, 255)),
        (0, 0, 0, (0, 0, 0)),
        (210.0, 65.38, 20.39, (18, 52, 86)),
        (60, 100, 50, (255, 255, 0)),
        (300, 100, 50, (255, 0, 255)),
    ],
)
def test_hsl_to_rgb_valid(h, s, lightness, expected):
    assert hsl_to_rgb(h, s, lightness) == expected


@pytest.mark.parametrize(
    "h, s, lightness",
    [
        (-1, 0, 0),
        (361, 0, 0),
        (0, -1, 0),
        (0, 101, 0),
        (0, 0, -1),
        (0, 0, 101),
    ],
)
def test_hsl_to_rgb_out_of_range(h, s, lightness):
    with pytest.raises(ValueError):
        hsl_to_rgb(h, s, lightness)


@pytest.mark.parametrize(
    "h, s, lightness",
    [
        ("120", 100, 50),
        (120, "100", 50),
        (120, 100, "50"),
        (True, 100, 50),
        (120, None, 50),
        (120, 100, [50]),
    ],
)
def test_hsl_to_rgb_invalid_types(h, s, lightness):
    with pytest.raises(TypeError):
        hsl_to_rgb(h, s, lightness)


@pytest.mark.parametrize(
    "r, g, b",
    [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 255),
        (0, 0, 0),
        (18, 52, 86),
        (64, 128, 255),
        (123, 45, 67),
        (255, 128, 0),
    ],
)
def test_rgb_hsl_round_trip(r, g, b):
    result = hsl_to_rgb(*rgb_to_hsl(r, g, b))
    assert all(abs(result[i] - channel) <= 1 for i, channel in enumerate((r, g, b)))


def test_random_hex_color():
    assert is_valid_hex(random_hex_color())


@pytest.mark.parametrize(
    "hex_code, expected",
    [
        ("#FFFFFF", True),
        ("#ffffff", True),
        ("FFFFFF", True),
        ("ffffff", True),
        ("#FFF", True),
        ("#fff", True),
        ("FFF", True),
        ("fff", True),
        ("#F0F0F0", True),
        ("#E0E0E0", True),
        ("#FFEEEE", True),
        ("#EEFFEE", True),
        ("#EEEEFF", True),
        ("#000000", False),
        ("#121212", False),
        ("#1A1A1A", False),
        ("#333333", False),
        ("#000080", False),
        ("#006400", False),
        ("#8B0000", False),
        ("#808080", True),
        ("#7F7F7F", True),
        ("#858585", True),
    ],
)
def test_is_light_color(hex_code, expected):
    assert is_light_color(hex_code) == expected


@pytest.mark.parametrize(
    "hex_code, threshold, expected",
    [
        ("#808080", 0.15, True),
        ("#808080", 0.20, True),
        ("#808080", 0.179, True),
        ("#FFFFFF", 0.5, True),
        ("#FFFFFF", 0.9, True),
        ("#000000", 0.01, False),
        ("#000000", 0.0, False),
        ("#333333", 0.05, False),
        ("#333333", 0.10, False),
    ],
)
def test_is_light_color_with_threshold(hex_code, threshold, expected):
    assert is_light_color(hex_code, threshold=threshold) == expected


def test_is_light_color_invalid_hex():
    with pytest.raises((ValueError, IndexError)):
        is_light_color("#GGGGGG")

    with pytest.raises((ValueError, IndexError)):
        is_light_color("#12345")

    with pytest.raises((ValueError, IndexError)):
        is_light_color("#1234567")


def test_is_light_color_edge_cases():
    assert is_light_color("#FFF") == is_light_color("#FFFFFF")
    assert is_light_color("#000") == is_light_color("#000000")
    assert is_light_color("#ABC") == is_light_color("#AABBCC")

    assert is_light_color("#AbCdEf") == is_light_color("#ABCDEF")

    assert is_light_color("#FF0000")
    assert is_light_color("#00FF00")
    assert not is_light_color("#0000FF")


@pytest.mark.parametrize(
    "hex_code, alpha, expected",
    [
        ("#FF0000", 0.5, (255, 0, 0, 0.5)),
        ("00ff00", 1.0, (0, 255, 0, 1.0)),
        ("#000", 0.0, (0, 0, 0, 0.0)),
        ("#4287F5", 0.8, (66, 135, 245, 0.8)),
    ],
)
def test_hex_to_rgba_valid(hex_code, alpha, expected):
    assert hex_to_rgba(hex_code, alpha) == expected


@pytest.mark.parametrize("alpha", [-0.1, 1.1])
def test_hex_to_rgba_invalid_alpha(alpha):
    with pytest.raises(ValueError):
        hex_to_rgba("#FF0000", alpha)


@pytest.mark.parametrize(
    "hex1, hex2, expected",
    [
        ("#000000", "#FFFFFF", 21.0),
        ("#FFFFFF", "#000000", 21.0),
        ("#000000", "#000000", 1.0),
        ("#777777", "#FFFFFF", 4.478089453577214),
    ],
)
def test_contrast_ratio(hex1, hex2, expected):
    assert contrast_ratio(hex1, hex2) == pytest.approx(expected)
