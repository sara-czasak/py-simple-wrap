"""
easy_converter is built to simplify different types of conversions
"""

from datetime import timedelta


def seconds_to_hh_mm_ss(seconds: int) -> str:
    """
    Returns seconds in HH:MM:SS format.

    Arguments:
        seconds (int) -- number of seconds to convert

    Example:
        seconds_to_hh_mm_ss(90)
        (00:01:30)
    """
    return str(timedelta(seconds=seconds))


def hh_mm_ss_to_seconds(hours: int = 0, minutes: int = 0, seconds: int = 0) \
        -> int:
    """
        Returns hours, minutes and seconds converted to seconds.

        Arguments:
            hours (int) -- number of hours to convert. Defaults to 0.
            minutes (int) -- number of minutes to convert. Defaults to 0.
            seconds (int) -- number of seconds to convert. Defaults to 0.

        Example:
            hh_mm_ss_to_seconds(1, 1, 1)
            (3661)
        """
    total_seconds = seconds
    total_seconds += hours * 3600
    total_seconds += minutes * 60
    return total_seconds


def km_to_mile(km: float) -> float:
    """
    Converts kilometers to miles. Returns miles as a float.

    Arguments:
        km (float) -- kilometers

    Example:
        km_to_mile(100)
        (62.13)
    """
    return float(f"{km * 0.621371:.2f}")


def miles_to_km(miles: float) -> float:
    """
        Converts miles to kilometers. Returns kilometers as a float.

        Arguments:
            miles (float) -- miles

        Example:
            miles_to_km(100)
            (160.93)
    """
    return float(f"{miles * 1.60934:.2f}")


def fluid_oz_to_ml(oz: float, standard = 'us') -> float | None:
    """
    Converts fluid ounces to milliliters. Returns milliliters as a float.

    :param:
        oz (float) -- fluid ounces
        standard -- us or uk

    Example:
        standard = 'us'
        fluid_oz_to_ml(1)
        (29.6)
        standard = 'uk'
        fluid_oz_to_ml(1)
        (28.4)

    """
    match standard:
        case "uk":
            return float(f"{oz * 28.4:.2f}")
        case "us":
            return float(f"{oz * 29.6:.2f}")
    return None


def ml_to_fluid_oz(milliliters: float, standard = 'us') -> float | None:
    """
        Converts milliliters to fluid ounces. Returns fluid ounces as a
        float.

        :param:
            milliliters (float) -- milliliters
            standard -- us or uk

        Example:
            standard = 'us'
            ml_to_fluid_oz(1)
            (0.03)
            standard = 'uk'
            ml_to_fluid_oz(1)
            (0.04)

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

        :param:
            temp_celsius (float) -- temperature in Celsius

        Example:
            celsius_to_fahrenheit(40)
            (104.0)

        """
    return float(f"{((temp_celsius * 9 / 5) + 32):.2f}")


def fahrenheit_to_celsius(temp_fahrenheit: float) -> float:
    """
        Converts temperature in Fahrenheit to temperature in Celsius.
        Returns degrees Celsius as float.

        :param:
            temp_fahrenheit (float) -- temperature in Fahrenheit

        Example:
            fahrenheit_to_celsius(104)
            (40.0)
        """
    return float(f"{((temp_fahrenheit - 32) * 5 / 9):.2f}")


def kg_to_lb(kg: float) -> float:
    """
        Converts kilograms to pounds.
        Returns pounds as float.

        :param:
            kg (float) -- kilograms

        Example:
            kg_to_lb(50)
            (110.23)
        """
    return float(f"{kg * 2.20462:.2f}")


def lb_to_kg(lb: float) -> float:
    """
        Converts pounds to kilograms.
        Returns kilograms as float.

        :param:
            lb (float) -- pounds

        Example:
            lb_to_kg(110.23)
            (50.0)
        """
    return float(f"{(lb * 0.453592):.2f}")


def meters_to_feet(meters: float) -> float:
    """
        Converts meters to feet.
        Returns feet as float.

        Arguments:
            meters (float) -- meters to be converted to feet.

        Example:
            meters_to_feet(100)
            (328.08)
        """
    return float(f"{(meters * 3.28084):.2f}")


def feet_to_meters(feet: float) -> float:
    """
        Converts feet to meters.
        Returns meters as float.

        Arguments:
            feet (float) -- feet to be converted to meters.

        Example:
            feet_to_meters(328.08)
            (100.0)
        """
    return float(f"{(feet * 0.3048):.2f}")


def cm_to_inches(cm: float) -> float:
    """
        Converts centimeters to inches.
        Returns inches as float.

        Arguments:
            cm (float) -- centimeters to be converted to inches.

        Example:
            cm_to_inches(100)
            (39.37)
        """
    return float(f"{(cm / 2.54):.2f}")


def inches_to_cm(inches: float) -> float:
    """
        Converts centimeters to inches.
        Returns inches as float.

        Arguments:
            inches (float) -- inches to be converted to centimeters.

        Example:
            inches_to_cm(39.37)
            (100.0)
        """
    return float(f"{(inches * 2.54):.2f}")


def sq_meters_to_sq_feet(sq_meters: float) -> float:
    """
        Converts square meters to square feet.
        Returns square feet as float.

        Arguments:
            sq_meters (float) -- square meters to be converted to
            square feet.

        Example:
            sq_meters_to_sq_feet(10)
            (107.64)
        """
    return float(f"{(sq_meters * 10.7639):.2f}")


def sq_feet_to_sq_meters(sq_feet: float) -> float:
    """
        Converts square feet to square meters.
        Returns square meters as float.

        Arguments:
            sq_feet (float) -- square feet to be converted to
            square meters.

        Example:
            sq_feet_to_sq_meters(107.64)
            (10.0)
        """
    return float(f"{(sq_feet * 0.092903):.2f}")
def mph_to_kph(mph):
    """
        Converts mph speed to kph speed.
        Returns kph speed as float.

        Arguments:
            mph (float) -- mph speed to be converted to
            kph speed.

        Example:
            mph_to_kph(0.621371)
            (1.0)
        """
    return float(f"{(mph * 1.60934):.2f}")


def kph_to_mph(kph):
    """
        Converts kph speed to mph speed.
        Returns mph speed as float.

        Arguments:
            kph (float) -- kph speed to be converted to
            kph speed.

        Example:
            kph_to_mph(1.60934)
            (1.0)
        """
    return float(f"{(kph * 0.621371):.2f}")
