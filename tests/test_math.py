import pytest

from py_simple_package.src.py_simple.easy_math import (
    celsius_to_fahrenheit,
    divisors,
    factorial,
    fibonacci,
    get_least_common_multiple,
    prime_factorization,
    sum_of_digits,
)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 6, 12),
        (3, 7, 21),
        (12, 18, 36),
        (6, 8, 24),
        (0, 5, 0),
        (5, 0, 0),
        (21, 6, 42),
        (-4, -6, 12),
        (-4, 6, 12),
    ],
)
def test_get_least_common_multiple(a, b, expected):
    assert get_least_common_multiple(a, b) == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ],
)
def test_factorial(n, expected):
    assert factorial(n) == expected


@pytest.mark.parametrize("n", [-1, -5, 2.5])
def test_factorial_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        factorial(n)


@pytest.mark.parametrize(
    "count, expected",
    [
        (1, [0]),
        (2, [0, 1]),
        (5, [0, 1, 1, 2, 3]),
        (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
    ],
)
def test_fibonacci(count, expected):
    assert fibonacci(count) == expected


@pytest.mark.parametrize("count", [0, -3, 1.5])
def test_fibonacci_rejects_invalid_count(count):
    with pytest.raises(ValueError):
        fibonacci(count)


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, []),
        (2, [2]),
        (7, [7]),
        (12, [2, 2, 3]),
        (100, [2, 2, 5, 5]),
        (360, [2, 2, 2, 3, 3, 5]),
    ],
)
def test_prime_factorization(n, expected):
    assert prime_factorization(n) == expected


@pytest.mark.parametrize("n", [0, -1])
def test_prime_factorization_rejects_less_than_one(n):
    with pytest.raises(ValueError):
        prime_factorization(n)


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (5, 5),
        (1234, 10),
        (100, 1),
        (-123, 6),
    ],
)
def test_sum_of_digits(n, expected):
    assert sum_of_digits(n) == expected


@pytest.mark.parametrize("n", [1.5, "12"])
def test_sum_of_digits_rejects_non_integer(n):
    with pytest.raises(ValueError):
        sum_of_digits(n)


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, [1]),
        (7, [1, 7]),
        (12, [1, 2, 3, 4, 6, 12]),
        (16, [1, 2, 4, 8, 16]),
        (25, [1, 5, 25]),
    ],
)
def test_divisors(n, expected):
    assert divisors(n) == expected


@pytest.mark.parametrize("n", [0, -2])
def test_divisors_rejects_less_than_one(n):
    with pytest.raises(ValueError):
        divisors(n)


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0.0, 32.0),
        (100.0, 212.0),
        (-40.0, -40.0),
        (25.0, 77.0),
        (37.0, 98.6),
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)

