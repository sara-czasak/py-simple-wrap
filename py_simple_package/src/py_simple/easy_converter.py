"""
easy_converter is built to simplify different types of conversions
"""

from datetime import timedelta


def seconds_to_hh_mm_ss(seconds: int) -> str:
    """
    Returns seconds in HH:MM:SS format.

    Args:
        seconds (int): Number of seconds to convert.

    Returns:
        str: Time formatted as HH:MM:SS.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import seconds_to_hh_mm_ss

            time_string = seconds_to_hh_mm_ss(3665)  # -> "01:01:05"
            ```

        === "The Traditional Way"
            ```python
            seconds = 3665
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            time_string = f"{hours:02}:{minutes:02}:{secs:02}"
            ```
    """
    return str(timedelta(seconds=seconds))


def hh_mm_ss_to_seconds(hours: int = 0, minutes: int = 0, seconds: int = 0) -> int:
    """
    Returns hours, minutes and seconds converted to seconds.

    Args:
        hours (int): Number of hours to convert. Defaults to 0.
        minutes (int): Number of minutes to convert. Defaults to 0.
        seconds (int): Number of seconds to convert. Defaults to 0.

    Returns:
        int: The total number of seconds.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import hh_mm_ss_to_seconds

            total = hh_mm_ss_to_seconds(1, 1, 1)  # -> 3661
            ```

        === "The Traditional Way"
            ```python
            hours, minutes, seconds = 1, 1, 1
            total = (hours * 3600) + (minutes * 60) + seconds
            ```
    """
    total_seconds = seconds
    total_seconds += hours * 3600
    total_seconds += minutes * 60
    return total_seconds


def km_to_mile(km: float) -> float:
    """
    Converts kilometers to miles. Returns miles as a float.

    Args:
        km (float): Kilometers.

    Returns:
        float: The equivalent distance in miles.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import km_to_mile

            miles = km_to_mile(100)  # -> 62.13
            ```

        === "The Traditional Way"
            ```python
            km = 100
            miles = round(km * 0.621371, 2)
            ```
    """
    return float(f"{km * 0.621371:.2f}")


def miles_to_km(miles: float) -> float:
    """
    Converts miles to kilometers. Returns kilometers as a float.

    Args:
        miles (float): Miles.

    Returns:
        float: The equivalent distance in kilometers.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import miles_to_km

            km = miles_to_km(100)  # -> 160.93
            ```

        === "The Traditional Way"
            ```python
            miles = 100
            km = round(miles * 1.60934, 2)
            ```
    """
    return float(f"{miles * 1.60934:.2f}")


def fluid_oz_to_ml(oz: float, standard="us") -> float | None:
    """
    Converts fluid ounces to milliliters. Returns milliliters as a float.

    Args:
        oz (float): Fluid ounces.
        standard (str): Measurement standard, 'us' or 'uk'. Defaults to 'us'.

    Returns:
        float | None: The equivalent volume in milliliters, or None if
            standard isn't 'us' or 'uk'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import fluid_oz_to_ml

            ml_us = fluid_oz_to_ml(1, standard='us')  # -> 29.6
            ml_uk = fluid_oz_to_ml(1, standard='uk')  # -> 28.4
            ```

        === "The Traditional Way"
            ```python
            oz = 1
            ml_us = round(oz * 29.6, 2)
            ml_uk = round(oz * 28.4, 2)
            ```
    """
    match standard:
        case "uk":
            return float(f"{oz * 28.4:.2f}")
        case "us":
            return float(f"{oz * 29.6:.2f}")
    return None


def ml_to_fluid_oz(milliliters: float, standard="us") -> float | None:
    """
    Converts milliliters to fluid ounces. Returns fluid ounces as a float.

    Args:
        milliliters (float): Milliliters.
        standard (str): Measurement standard, 'us' or 'uk'. Defaults to 'us'.

    Returns:
        float | None: The equivalent volume in fluid ounces, or None if
            standard isn't 'us' or 'uk'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import ml_to_fluid_oz

            oz_us = ml_to_fluid_oz(1, standard='us')  # -> 0.03
            oz_uk = ml_to_fluid_oz(1, standard='uk')  # -> 0.04
            ```

        === "The Traditional Way"
            ```python
            milliliters = 1
            oz_us = round(milliliters * 0.034, 2)
            oz_uk = round(milliliters * 0.035, 2)
            ```
    """
    match standard:
        case "uk":
            return float(f"{milliliters * 0.035:.2f}")
        case "us":
            return float(f"{milliliters * 0.034:.2f}")
    return None


def celsius_to_fahrenheit(temp_celsius: float) -> float:
    """
    Converts temperature in Celsius to temperature in Fahrenheit.
    Returns degrees Fahrenheit as float.

    Args:
        temp_celsius (float): Temperature in Celsius.

    Returns:
        float: The equivalent temperature in Fahrenheit.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import celsius_to_fahrenheit

            temp_f = celsius_to_fahrenheit(25)  # -> 77.0
            ```

        === "The Traditional Way"
            ```python
            celsius = 25
            fahrenheit = (celsius * 9 / 5) + 32
            ```
    """
    return float(f"{((temp_celsius * 9 / 5) + 32):.2f}")


def fahrenheit_to_celsius(temp_fahrenheit: float) -> float:
    """
    Converts temperature in Fahrenheit to temperature in Celsius.
    Returns degrees Celsius as float.

    Args:
        temp_fahrenheit (float): Temperature in Fahrenheit.

    Returns:
        float: The equivalent temperature in Celsius.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import fahrenheit_to_celsius

            temp_c = fahrenheit_to_celsius(104)  # -> 40.0
            ```

        === "The Traditional Way"
            ```python
            fahrenheit = 104
            celsius = (fahrenheit - 32) * 5 / 9
            ```
    """
    return float(f"{((temp_fahrenheit - 32) * 5 / 9):.2f}")


def kg_to_lb(kg: float) -> float:
    """
    Converts kilograms to pounds. Returns pounds as float.

    Args:
        kg (float): Kilograms.

    Returns:
        float: The equivalent weight in pounds.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import kg_to_lb

            weight_lb = kg_to_lb(5)  # -> 11.02
            ```

        === "The Traditional Way"
            ```python
            kg = 5
            lb = round(kg * 2.20462, 2)
            ```
    """
    return float(f"{kg * 2.20462:.2f}")


def lb_to_kg(lb: float) -> float:
    """
    Converts pounds to kilograms. Returns kilograms as float.

    Args:
        lb (float): Pounds.

    Returns:
        float: The equivalent weight in kilograms.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import lb_to_kg

            weight_kg = lb_to_kg(110.23)  # -> 50.0
            ```

        === "The Traditional Way"
            ```python
            lb = 110.23
            kg = round(lb * 0.453592, 2)
            ```
    """
    return float(f"{(lb * 0.453592):.2f}")


def meters_to_feet(meters: float) -> float:
    """
    Converts meters to feet. Returns feet as float.

    Args:
        meters (float): Meters to be converted to feet.

    Returns:
        float: The equivalent length in feet.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import meters_to_feet

            feet = meters_to_feet(100)  # -> 328.08
            ```

        === "The Traditional Way"
            ```python
            meters = 100
            feet = round(meters * 3.28084, 2)
            ```
    """
    return float(f"{(meters * 3.28084):.2f}")


def feet_to_meters(feet: float) -> float:
    """
    Converts feet to meters. Returns meters as float.

    Args:
        feet (float): Feet to be converted to meters.

    Returns:
        float: The equivalent length in meters.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import feet_to_meters

            meters = feet_to_meters(328.08)  # -> 100.0
            ```

        === "The Traditional Way"
            ```python
            feet = 328.08
            meters = round(feet * 0.3048, 2)
            ```
    """
    return float(f"{(feet * 0.3048):.2f}")


def cm_to_inches(cm: float) -> float:
    """
    Converts centimeters to inches. Returns inches as float.

    Args:
        cm (float): Centimeters to be converted to inches.

    Returns:
        float: The equivalent length in inches.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import cm_to_inches

            inches = cm_to_inches(100)  # -> 39.37
            ```

        === "The Traditional Way"
            ```python
            cm = 100
            inches = round(cm / 2.54, 2)
            ```
    """
    return float(f"{(cm / 2.54):.2f}")


def inches_to_cm(inches: float) -> float:
    """
    Converts inches to centimeters. Returns centimeters as float.

    Args:
        inches (float): Inches to be converted to centimeters.

    Returns:
        float: The equivalent length in centimeters.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import inches_to_cm

            cm = inches_to_cm(39.37)  # -> 100.0
            ```

        === "The Traditional Way"
            ```python
            inches = 39.37
            cm = round(inches * 2.54, 2)
            ```
    """
    return float(f"{(inches * 2.54):.2f}")


def sq_meters_to_sq_feet(sq_meters: float) -> float:
    """
    Converts square meters to square feet. Returns square feet as float.

    Args:
        sq_meters (float): Square meters to be converted to square feet.

    Returns:
        float: The equivalent area in square feet.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sq_meters_to_sq_feet

            sq_feet = sq_meters_to_sq_feet(10)  # -> 107.64
            ```

        === "The Traditional Way"
            ```python
            sq_meters = 10
            sq_feet = round(sq_meters * 10.7639, 2)
            ```
    """
    return float(f"{(sq_meters * 10.7639):.2f}")


def sq_feet_to_sq_meters(sq_feet: float) -> float:
    """
    Converts square feet to square meters. Returns square meters as float.

    Args:
        sq_feet (float): Square feet to be converted to square meters.

    Returns:
        float: The equivalent area in square meters.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sq_feet_to_sq_meters

            sq_meters = sq_feet_to_sq_meters(107.64)  # -> 10.0
            ```

        === "The Traditional Way"
            ```python
            sq_feet = 107.64
            sq_meters = round(sq_feet * 0.092903, 2)
            ```
    """
    return float(f"{(sq_feet * 0.092903):.2f}")


def mph_to_kph(mph):
    """
    Converts mph speed to kph speed. Returns kph speed as float.

    Args:
        mph (float): Speed in mph to be converted to kph.

    Returns:
        float: The equivalent speed in kph.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import mph_to_kph

            kph = mph_to_kph(0.621371)  # -> 1.0
            ```

        === "The Traditional Way"
            ```python
            mph = 0.621371
            kph = round(mph * 1.60934, 2)
            ```
    """
    return float(f"{(mph * 1.60934):.2f}")


def kph_to_mph(kph):
    """
    Converts kph speed to mph speed. Returns mph speed as float.

    Args:
        kph (float): Speed in kph to be converted to mph.

    Returns:
        float: The equivalent speed in mph.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import kph_to_mph

            mph = kph_to_mph(1.60934)  # -> 1.0
            ```

        === "The Traditional Way"
            ```python
            kph = 1.60934
            mph = round(kph * 0.621371, 2)
            ```
    """
    return float(f"{(kph * 0.621371):.2f}")
