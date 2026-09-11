"""Tests for the easy_converter module."""

import pytest

from py_simple_package.src.py_simple.easy_converter import (
    celsius_to_fahrenheit,
    cm_to_inches,
    fahrenheit_to_celsius,
    feet_to_meters,
    fluid_oz_to_ml,
    hh_mm_ss_to_seconds,
    inches_to_cm,
    kg_to_lb,
    km_to_mile,
    kph_to_mph,
    lb_to_kg,
    meters_to_feet,
    miles_to_km,
    ml_to_fluid_oz,
    mph_to_kph,
    seconds_to_hh_mm_ss,
    sq_feet_to_sq_meters,
    sq_meters_to_sq_feet,
)


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "0:00:00"),
        (90, "0:01:30"),
        (3661, "1:01:01"),
        (-1, "-1 day, 23:59:59"),
    ],
)
def test_seconds_to_hh_mm_ss(seconds, expected):
    """Seconds should be rendered using timedelta's stable text format."""
    assert seconds_to_hh_mm_ss(seconds) == expected


@pytest.mark.parametrize(
    ("hours", "minutes", "seconds", "expected"),
    [
        (0, 0, 0, 0),
        (1, 1, 1, 3661),
        (0, 90, 0, 5400),
        (-1, 30, 0, -1800),
    ],
)
def test_hh_mm_ss_to_seconds(hours, minutes, seconds, expected):
    """Hours, minutes, and seconds should combine arithmetically."""
    assert hh_mm_ss_to_seconds(hours, minutes, seconds) == expected


def test_hh_mm_ss_to_seconds_uses_zero_defaults():
    """All omitted components should default to zero."""
    assert hh_mm_ss_to_seconds() == 0


@pytest.mark.parametrize(
    ("converter", "value", "expected"),
    [
        (km_to_mile, 100, 62.14),
        (km_to_mile, 0, 0.0),
        (miles_to_km, 100, 160.93),
        (miles_to_km, 0, 0.0),
        (kg_to_lb, 50, 110.23),
        (kg_to_lb, 0, 0.0),
        (lb_to_kg, 110.23, 50.0),
        (lb_to_kg, 0, 0.0),
        (meters_to_feet, 100, 328.08),
        (meters_to_feet, 0, 0.0),
        (feet_to_meters, 328.08, 100.0),
        (feet_to_meters, 0, 0.0),
        (cm_to_inches, 100, 39.37),
        (cm_to_inches, 0, 0.0),
        (inches_to_cm, 39.37, 100.0),
        (inches_to_cm, 0, 0.0),
        (sq_meters_to_sq_feet, 10, 107.64),
        (sq_meters_to_sq_feet, 0, 0.0),
        (sq_feet_to_sq_meters, 107.64, 10.0),
        (sq_feet_to_sq_meters, 0, 0.0),
    ],
)
def test_distance_weight_and_area_conversions(converter, value, expected):
    """Scalar conversion helpers should apply their documented factors."""
    assert converter(value) == expected


@pytest.mark.parametrize(
    ("converter", "value", "expected"),
    [
        (km_to_mile, -10, -6.21),
        (miles_to_km, -10, -16.09),
        (kg_to_lb, -5, -11.02),
        (lb_to_kg, -5, -2.27),
        (meters_to_feet, -2, -6.56),
        (feet_to_meters, -2, -0.61),
        (cm_to_inches, -2.54, -1.0),
        (inches_to_cm, -1, -2.54),
        (sq_meters_to_sq_feet, -1, -10.76),
        (sq_feet_to_sq_meters, -1, -0.09),
    ],
)
def test_scalar_conversions_preserve_negative_sign(converter, value, expected):
    """The helpers should preserve the sign of negative numeric inputs."""
    assert converter(value) == expected


@pytest.mark.parametrize(
    ("standard", "expected"),
    [
        ("us", 29.6),
        ("uk", 28.4),
    ],
)
def test_fluid_oz_to_ml_supported_standards(standard, expected):
    """US and UK fluid-ounce standards should use distinct factors."""
    assert fluid_oz_to_ml(1, standard) == expected


def test_fluid_oz_to_ml_defaults_to_us_standard():
    """The default fluid-ounce standard should be US."""
    assert fluid_oz_to_ml(1) == 29.6


@pytest.mark.parametrize(
    ("standard", "expected"),
    [
        ("us", 3.4),
        ("uk", 3.5),
    ],
)
def test_ml_to_fluid_oz_supported_standards(standard, expected):
    """US and UK milliliter conversions should use distinct factors."""
    assert ml_to_fluid_oz(100, standard) == expected


def test_ml_to_fluid_oz_defaults_to_us_standard():
    """The default milliliter conversion standard should be US."""
    assert ml_to_fluid_oz(100) == 3.4


@pytest.mark.parametrize("standard", ["", "US", "imperial", None])
def test_fluid_converters_return_none_for_unknown_standard(standard):
    """Unknown standards should follow the documented None fallback."""
    assert fluid_oz_to_ml(1, standard) is None
    assert ml_to_fluid_oz(1, standard) is None


@pytest.mark.parametrize(
    ("celsius", "fahrenheit"),
    [
        (-40, -40.0),
        (0, 32.0),
        (37, 98.6),
        (100, 212.0),
    ],
)
def test_celsius_to_fahrenheit(celsius, fahrenheit):
    """Known Celsius reference points should convert correctly."""
    assert celsius_to_fahrenheit(celsius) == fahrenheit


@pytest.mark.parametrize(
    ("fahrenheit", "celsius"),
    [
        (-40, -40.0),
        (32, 0.0),
        (98.6, 37.0),
        (212, 100.0),
    ],
)
def test_fahrenheit_to_celsius(fahrenheit, celsius):
    """Known Fahrenheit reference points should convert correctly."""
    assert fahrenheit_to_celsius(fahrenheit) == celsius


@pytest.mark.parametrize(
    ("mph", "expected"),
    [
        (0, 0.0),
        (1, 1.61),
        (60, 96.56),
        (-10, -16.09),
    ],
)
def test_mph_to_kph(mph, expected):
    """Miles per hour should convert to kilometres per hour."""
    assert mph_to_kph(mph) == expected


@pytest.mark.parametrize(
    ("kph", "expected"),
    [
        (0, 0.0),
        (1.60934, 1.0),
        (96.56, 60.0),
        (-10, -6.21),
    ],
)
def test_kph_to_mph(kph, expected):
    """Kilometres per hour should convert to miles per hour."""
    assert kph_to_mph(kph) == expected


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (86400, "1 day, 0:00:00"),
        (60, "0:01:00"),
        (1, "0:00:01"),
        (3600, "1:00:00"),
    ],
)
def test_seconds_to_hh_mm_ss_large_values(seconds, expected):
    """Larger second counts should format correctly."""
    assert seconds_to_hh_mm_ss(seconds) == expected


def test_hh_mm_ss_to_seconds_symmetry():
    """Converting to seconds and back should produce the original value
    for small non-negative inputs."""
    assert hh_mm_ss_to_seconds(2, 30, 15) == 9015
    assert seconds_to_hh_mm_ss(9015) == "2:30:15"
