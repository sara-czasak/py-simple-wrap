"""
easy_numbers is built to simplify different types of number operations.
"""


def is_even(number: int) -> bool:
    """
    Returns true if the number is even and false if it is odd.

    Args:
        number (int): Number to check.

    Returns:
        bool: True if even, False if odd.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_even

            result = is_even(90)  # -> True
            ```

        === "The Traditional Way"
            ```python
            number = 90
            result = number % 2 == 0
            ```
    """
    return number % 2 == 0


def is_odd(number: int) -> bool:
    """
    Returns true if the number is odd and false if it is even.

    Args:
        number (int): Number to check.

    Returns:
        bool: True if odd, False if even.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_odd

            result = is_odd(67)  # -> True
            ```

        === "The Traditional Way"
            ```python
            number = 67
            result = number % 2 == 1
            ```
    """
    return number % 2 == 1


def is_evenly_divisible(number: int, divisor: int) -> bool:
    """
    Returns true if the number can be evenly divided by divisor.

    Args:
        number (int): Number to check.
        divisor (int): Number to divide by.

    Returns:
        bool: True if number divides evenly by divisor, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_evenly_divisible

            result = is_evenly_divisible(90, 9)  # -> True
            ```

        === "The Traditional Way"
            ```python
            number, divisor = 90, 9
            result = number % divisor == 0
            ```
    """
    return number % divisor == 0


def is_positive(number: int) -> bool:
    """
    Returns true if the number is positive and false if it is negative.

    Args:
        number (int): Number to check.

    Returns:
        bool: True if positive, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_positive

            result = is_positive(90)  # -> True
            ```

        === "The Traditional Way"
            ```python
            number = 90
            result = number > 0
            ```
    """
    return number > 0


def is_negative(number: int) -> bool:
    """
    Returns true if the number is negative and false if it is positive.

    Args:
        number (int): Number to check.

    Returns:
        bool: True if negative, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_negative

            result = is_negative(-10)  # -> True
            ```

        === "The Traditional Way"
            ```python
            number = -10
            result = number < 0
            ```
    """
    return number < 0


def average(nums: list[float]) -> float:
    """
    Returns the average of a list of numbers.

    Args:
        nums (list[float]): List of numbers to average.

    Returns:
        float: The average, rounded to 2 decimal places.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import average

            result = average([1.5, 2, 3])  # -> 2.17
            ```

        === "The Traditional Way"
            ```python
            nums = [1.5, 2, 3]
            result = round(sum(nums) / len(nums), 2)
            ```
    """
    return float(f"{(sum(nums) / len(nums)):.2f}")


def is_prime(number: int) -> bool:
    """
    Returns true if the number is prime and false if it is not.

    Args:
        number (int): Number to check.

    Returns:
        bool: True if prime, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_prime

            result = is_prime(2)  # -> True
            ```

        === "The Traditional Way"
            ```python
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(n ** 0.5) + 1):
                    if n % i == 0:
                        return False
                return True

            result = is_prime(2)
            ```
    """
    if number > 0:
        limit = int((number**0.5) + 1)
    else:
        return False
    if number < 2:
        return False
    elif number == 2:
        return True
    elif is_even(number):
        return False
    else:
        for i in range(3, limit, 2):
            if is_evenly_divisible(number, i):
                return False
    return True


def percentage_of(number: int, percentage: float) -> float:
    """
    Returns percentage of number as a float.

    Args:
        number (int): Number to get percentage of.
        percentage (float): Percentage to get, between 0 and 1
            (e.g. 0.5, 0.75).

    Returns:
        float: The calculated percentage, rounded to 2 decimal places.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import percentage_of

            result = percentage_of(100, 0.5)  # -> 50.0
            ```

        === "The Traditional Way"
            ```python
            number, percentage = 100, 0.5
            result = round(number * percentage, 2)
            ```
    """
    return float(f"{(number * percentage):.2f}")


def round_to_nearest(number: float, nearest: int) -> float:
    """
    Returns a number rounded to the nearest multiple.

    Args:
        number (float): Number to round.
        nearest (int): Multiple to round to.

    Returns:
        float: Rounded number.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import round_to_nearest

            result = round_to_nearest(23, 5)  # -> 25.0
            ```

        === "The Traditional Way"
            ```python
            number, nearest = 23, 5
            result = round(number / nearest) * nearest
            ```
    """
    if nearest == 0:
        raise ValueError("'nearest' must not be zero.")

    return round(number / nearest) * nearest


def greatest_common_divisor(a: int, b: int) -> int:
    """
    Returns the greatest common divisor (GCD) of two numbers.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: Greatest common divisor.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import greatest_common_divisor

            result = greatest_common_divisor(12, 18)  # -> 6
            ```

        === "The Traditional Way"
            ```python
            import math

            a, b = 12, 18
            result = math.gcd(a, b)
            ```
    """
    while b != 0:
        a, b = b, a % b

    return abs(a)


def clamp(number: float, minimum: float, maximum: float) -> float:
    """
    Keeps a number within a minimum and maximum range.

    Args:
        number (float): Number to clamp.
        minimum (float): Minimum allowed value.
        maximum (float): Maximum allowed value.

    Returns:
        float: Clamped number.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import clamp

            result = clamp(15, 0, 10)  # -> 10
            ```

        === "The Traditional Way"
            ```python
            number, minimum, maximum = 15, 0, 10
            result = max(minimum, min(number, maximum))
            ```
    """
    return max(minimum, min(number, maximum))
