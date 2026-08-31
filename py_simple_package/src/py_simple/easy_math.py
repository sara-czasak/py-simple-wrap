"""Beginner-friendly helpers for common math operations."""

import math


def get_least_common_multiple(a: int, b: int) -> int:
    """
    Returns the least common multiple of two integers.

    The result is always positive, and 0 is returned if either number is 0.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: The least common multiple.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import lcm

            result = lcm(4, 6)  # -> 12
            ```

        === "The Traditional Way"
            ```python
            import math
            from math import gcd

            a, b = 4, 6
            result = abs(a * b) // gcd(a, b)
            ```
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def factorial(n: int) -> int:
    """
    Returns the factorial of a whole number.

    Args:
        n (int): Non-negative integer.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative or not a whole number.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import factorial

            result = factorial(5)  # -> 120
            ```

        === "The Traditional Way"
            ```python
            n = 5
            result = 1
            for number in range(2, n + 1):
                result *= number
            ```
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for whole numbers (0, 1, 2, ...).")

    return math.factorial(n)


def fibonacci(count: int) -> list:
    """
    Returns the first count Fibonacci numbers as a list.

    Args:
        count (int): How many Fibonacci numbers to return.

    Returns:
        list: The first count Fibonacci numbers.

    Raises:
        ValueError: If count is less than 1.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import fibonacci

            result = fibonacci(5)  # -> [0, 1, 1, 2, 3]
            ```

        === "The Traditional Way"
            ```python
            count = 5
            sequence = [0, 1]
            while len(sequence) < count:
                sequence.append(sequence[-1] + sequence[-2])
            result = sequence[:count]
            ```
    """
    if not isinstance(count, int) or count < 1:
        raise ValueError("'count' must be at least 1.")

    sequence = [0, 1]
    while len(sequence) < count:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:count]


def prime_factorization(n: int) -> list:
    """
    Returns the prime factors of a positive integer, including repeats.

    Args:
        n (int): Positive integer to factor.

    Returns:
        list: Prime factors of n.

    Raises:
        ValueError: If n is less than 1.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import prime_factorization

            result = prime_factorization(12)  # -> [2, 2, 3]
            ```

        === "The Traditional Way"
            ```python
            n = 12
            factors = []
            divisor = 2
            while divisor * divisor <= n:
                while n % divisor == 0:
                    factors.append(divisor)
                    n //= divisor
                divisor += 1
            if n > 1:
                factors.append(n)
            ```
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("'n' must be a positive integer.")

    factors = []
    remaining = n
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors.append(divisor)
            remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    return factors


def sum_of_digits(n: int) -> int:
    """
    Returns the sum of the digits of an integer.

    Negative numbers are handled by ignoring the minus sign.

    Args:
        n (int): Integer to add up.

    Returns:
        int: The sum of the digits.

    Raises:
        ValueError: If n is not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sum_of_digits

            result = sum_of_digits(1234)  # -> 10
            ```

        === "The Traditional Way"
            ```python
            n = 1234
            result = sum(int(digit) for digit in str(n))
            ```
    """
    if not isinstance(n, int):
        raise ValueError("'n' must be an integer.")

    return sum(int(digit) for digit in str(abs(n)))


def divisors(n: int) -> list:
    """
    Returns every positive integer that divides n evenly.

    Args:
        n (int): Positive integer to divide.

    Returns:
        list: All divisors of n.

    Raises:
        ValueError: If n is less than 1.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import divisors

            result = divisors(12)  # -> [1, 2, 3, 4, 6, 12]
            ```

        === "The Traditional Way"
            ```python
            n = 12
            result = [number for number in range(1, n + 1) if n % number == 0]
            ```
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("'n' must be a positive integer.")

    small = [number for number in range(1, int(math.sqrt(n)) + 1) if n % number == 0]
    large = [n // number for number in reversed(small) if n // number != number]
    return small + large


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert temperature from Celsius to Fahrenheit.

    Args:
        celsius (float): Temperature in degrees Celsius.

    Returns:
        float: Temperature in degrees Fahrenheit.
    """
    return (celsius * 9 / 5) + 32

