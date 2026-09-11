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


def is_perfect_square(n: int) -> bool:
    """
    Returns whether a non-negative integer is a perfect square.

    A perfect square is an integer that can be written as another
    integer multiplied by itself, such as 0, 1, 4, 9, or 16.

    Args:
        n (int): Non-negative integer to check.

    Returns:
        bool: True if n is a perfect square, otherwise False.

    Raises:
        ValueError: If n is negative or not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_perfect_square

            result = is_perfect_square(49)  # -> True
            ```

        === "The Traditional Way"
            ```python
            import math

            n = 49
            root = math.isqrt(n)
            result = root * root == n
            ```
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("'n' must be a non-negative integer.")

    root = math.isqrt(n)
    return root * root == n


def is_armstrong_number(n: int) -> bool:
    """
    Returns whether a non-negative integer is an Armstrong number.

    An Armstrong number (or narcissistic number) is a number that is equal 
    to the sum of its own digits each raised to the power of the number of digits.
    For example, 153 is an Armstrong number because 1^3 + 5^3 + 3^3 = 153.

    Args:
        n (int): Non-negative integer to check.

    Returns:
        bool: True if n is an Armstrong number, otherwise False.

    Raises:
        ValueError: If n is negative or not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_armstrong_number

            result = is_armstrong_number(153)  # -> True
            ```

        === "The Traditional Way"
            ```python
            n = 153
            num_str = str(n)
            num_digits = len(num_str)
            result = sum(int(digit) ** num_digits for digit in num_str) == n
            ```
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("'n' must be a non-negative integer.")
    
    num_str = str(n)
    num_digits = len(num_str)
    return sum(int(digit) ** num_digits for digit in num_str) == n

def is_triangular_number(n: int) -> bool:
    """
    Returns whether a non-negative integer is a triangular number.

    A triangular number counts objects arranged in an equilateral triangle.
    For example, 6 is triangular because it can be arranged as 1 + 2 + 3.

    Args:
        n (int): Non-negative integer to check.

    Returns:
        bool: True if n is a triangular number, otherwise False.

    Raises:
        ValueError: If n is negative or not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_triangular_number

            result = is_triangular_number(10)  # -> True
            ```

        === "The Traditional Way"
            ```python
            n = 10
            k = int((2 * n) ** 0.5)
            result = k * (k + 1) // 2 == n
            ```
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("'n' must be a non-negative integer.")
    
    k = int((2 * n) ** 0.5)
    return k * (k + 1) // 2 == n


def is_harshad_number(n: int) -> bool:
    """
    Returns whether a positive integer is a Harshad (or Niven) number.

    A Harshad number is an integer that is divisible by the sum of its digits.
    For example, 18 is a Harshad number because 1 + 8 = 9, and 18 % 9 == 0.

    Args:
        n (int): Positive integer to check.

    Returns:
        bool: True if n is a Harshad number, otherwise False.

    Raises:
        ValueError: If n is less than 1 or not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_harshad_number

            result = is_harshad_number(18)  # -> True
            ```

        === "The Traditional Way"
            ```python
            n = 18
            result = n % sum(int(d) for d in str(n)) == 0
            ```
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("'n' must be a positive integer.")
    
    digit_sum = sum(int(d) for d in str(n))
    return n % digit_sum == 0


def count_digits(n: int) -> int:
    """
    Returns the total number of digits in an integer.

    The negative sign is ignored when counting digits.

    Args:
        n (int): Integer to count digits for.

    Returns:
        int: The number of digits.

    Raises:
        ValueError: If n is not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_digits

            result = count_digits(-1234)  # -> 4
            ```

        === "The Traditional Way"
            ```python
            n = -1234
            result = len(str(abs(n)))
            ```
    """
    if not isinstance(n, int):
        raise ValueError("'n' must be an integer.")
    
    return len(str(abs(n)))


def reverse_digits(n: int) -> int:
    """
    Returns an integer with its digits reversed, preserving the sign.

    Args:
        n (int): Integer to reverse.

    Returns:
        int: The reversed integer.

    Raises:
        ValueError: If n is not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import reverse_digits

            result = reverse_digits(-123)  # -> -321
            ```

        === "The Traditional Way"
            ```python
            n = -123
            result = int(str(n)[::-1]) * (-1 if n < 0 else 1)
            ```
    """
    if not isinstance(n, int):
        raise ValueError("'n' must be an integer.")
    
    sign = -1 if n < 0 else 1
    return int(str(abs(n))[::-1]) * sign


def is_abundant_number(n: int) -> bool:
    """
    Returns whether a positive integer is an abundant number.

    An abundant number is one where the sum of its proper divisors 
    (excluding the number itself) is greater than the number.
    For example, 12 is abundant because 1 + 2 + 3 + 4 + 6 = 16 > 12.

    Args:
        n (int): Positive integer to check.

    Returns:
        bool: True if n is an abundant number, otherwise False.

    Raises:
        ValueError: If n is less than 1 or not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_abundant_number

            result = is_abundant_number(12)  # -> True
            ```

        === "The Traditional Way"
            ```python
            n = 12
            proper_divisors = [i for i in range(1, n) if n % i == 0]
            result = sum(proper_divisors) > n
            ```
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("'n' must be a positive integer.")
    
    proper_divisors_sum = sum(i for i in range(1, n // 2 + 1) if n % i == 0)
    return proper_divisors_sum > n


def distance_between_points(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Returns the Euclidean distance between two 2D points.

    Args:
        x1 (float): X coordinate of the first point.
        y1 (float): Y coordinate of the first point.
        x2 (float): X coordinate of the second point.
        y2 (float): Y coordinate of the second point.

    Returns:
        float: The distance between the two points.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import distance_between_points

            result = distance_between_points(0, 0, 3, 4)  # -> 5.0
            ```

        === "The Traditional Way"
            ```python
            import math

            result = math.sqrt((3 - 0)**2 + (4 - 0)**2)
            ```
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
    """
    Returns the exact midpoint between two 2D coordinates.

    Args:
        x1 (float): X coordinate of the first point.
        y1 (float): Y coordinate of the first point.
        x2 (float): X coordinate of the second point.
        y2 (float): Y coordinate of the second point.

    Returns:
        tuple[float, float]: The (x, y) coordinates of the midpoint.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import midpoint

            result = midpoint(0, 0, 4, 6)  # -> (2.0, 3.0)
            ```

        === "The Traditional Way"
            ```python
            result = ((0 + 4) / 2, (0 + 6) / 2)
            ```
    """
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def sum_of_squares(numbers: list[float]) -> float:
    """
    Returns the sum of the squared values in a list of numbers.

    Args:
        numbers (list[float]): A list of numeric values.

    Returns:
        float: The sum of the squares.

    Raises:
        ValueError: If the input is not a list.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sum_of_squares

            result = sum_of_squares([1, 2, 3])  # -> 14.0
            ```

        === "The Traditional Way"
            ```python
            numbers = [1, 2, 3]
            result = sum(x**2 for x in numbers)
            ```
    """
    if not isinstance(numbers, list):
        raise ValueError("'numbers' must be a list.")
    
    return sum(x**2 for x in numbers)


def calculate_simple_interest(principal: float, rate: float, time: float) -> float:
    """
    Returns the simple interest earned on a principal amount.

    Args:
        principal (float): The initial amount of money.
        rate (float): The annual interest rate (as a percentage, e.g., 5 for 5%).
        time (float): The time the money is invested or borrowed for, in years.

    Returns:
        float: The calculated simple interest amount.

    Raises:
        ValueError: If any argument is not a number (int or float).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import calculate_simple_interest

            result = calculate_simple_interest(1000, 5, 2)  # -> 100.0
            ```

        === "The Traditional Way"
            ```python
            principal, rate, time = 1000, 5, 2
            result = (principal * rate * time) / 100
            ```
    """
    if not all(isinstance(x, (int, float)) for x in (principal, rate, time)):
        raise ValueError("principal, rate, and time must be numbers.")
    
    return (principal * rate * time) / 100


def collatz_sequence(n: int) -> list[int]:
    """
    Returns the Collatz conjecture sequence for a given positive integer.

    The sequence starts with n. If n is even, the next number is n / 2.
    If n is odd, the next number is 3 * n + 1. This repeats until n reaches 1.

    Args:
        n (int): Positive integer to start the sequence.

    Returns:
        list[int]: The Collatz sequence ending in 1.

    Raises:
        ValueError: If n is less than 1 or not an integer.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import collatz_sequence

            result = collatz_sequence(6)  # -> [6, 3, 10, 5, 16, 8, 4, 2, 1]
            ```

        === "The Traditional Way"
            ```python
            n = 6
            sequence = [n]
            while n != 1:
                n = n // 2 if n % 2 == 0 else 3 * n + 1
                sequence.append(n)
            ```
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("'n' must be a positive integer.")
    
    sequence = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        sequence.append(n)
    return sequence