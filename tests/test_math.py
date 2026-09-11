import pytest
from py_simple_package.src.py_simple import is_perfect_square as public_is_perfect_square

from py_simple_package.src.py_simple.easy_math import (
    divisors,
    factorial,
    fibonacci,
    get_least_common_multiple,
    is_perfect_square,
    prime_factorization,
    sum_of_digits,
    is_armstrong_number,
    calculate_simple_interest,
    collatz_sequence,
    count_digits,
    distance_between_points,
    is_abundant_number,
    is_harshad_number,
    is_triangular_number,
    midpoint,
    reverse_digits,
    sum_of_squares,
    
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
    "n, expected",
    [
        (0, True),
        (1, True),
        (4, True),
        (49, True),
        (50, False),
        (10**12, True),
        (10**12 - 1, False),
    ],
)
def test_is_perfect_square(n, expected):
    assert is_perfect_square(n) is expected


def test_is_perfect_square_is_available_from_public_api():
    assert public_is_perfect_square is is_perfect_square


@pytest.mark.parametrize("n", [-1, -25, 4.0, "9"])
def test_is_perfect_square_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        is_perfect_square(n)

@pytest.mark.parametrize(
    "n, expected",
    [
        (0, True),       # 0^1 = 0
        (1, True),       # 1^1 = 1
        (153, True),     # 1^3 + 5^3 + 3^3 = 153
        (370, True),     # 3^3 + 7^3 + 0^3 = 370
        (371, True),     # 3^3 + 7^3 + 1^3 = 371
        (407, True),     # 4^3 + 0^3 + 7^3 = 407
        (1634, True),    # 1^4 + 6^4 + 3^4 + 4^4 = 1634
        (10, False),     # 1^2 + 0^2 = 1 != 10
        (154, False),    # Not an Armstrong number
    ],
)
def test_is_armstrong_number(n, expected):
    assert is_armstrong_number(n) is expected

@pytest.mark.parametrize("n", [-1, -153, 15.3, "153"])
def test_is_armstrong_number_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        is_armstrong_number(n)
        
# --- 1. is_triangular_number ---
@pytest.mark.parametrize(
    "n, expected",
    [(0, True), (1, True), (3, True), (6, True), (10, True), (15, True), (5, False), (14, False)],
)
def test_is_triangular_number(n, expected):
    assert is_triangular_number(n) is expected

@pytest.mark.parametrize("n", [-1, -5, 2.5, "10"])
def test_is_triangular_number_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        is_triangular_number(n)


# --- 2. is_harshad_number ---
@pytest.mark.parametrize(
    "n, expected", [(1, True), (18, True), (20, True), (21, True), (19, False), (25, False)]
)
def test_is_harshad_number(n, expected):
    assert is_harshad_number(n) is expected

@pytest.mark.parametrize("n", [0, -1, -18, 18.5, "18"])
def test_is_harshad_number_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        is_harshad_number(n)


# --- 3. count_digits ---
@pytest.mark.parametrize(
    "n, expected", [(0, 1), (5, 1), (42, 2), (12345, 5), (-9, 1), (-1234, 4)]
)
def test_count_digits(n, expected):
    assert count_digits(n) == expected

@pytest.mark.parametrize("n", [12.34, "123", None])
def test_count_digits_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        count_digits(n)


# --- 4. reverse_digits ---
@pytest.mark.parametrize(
    "n, expected", [(0, 0), (5, 5), (123, 321), (120, 21), (-45, -54), (-123, -321)]
)
def test_reverse_digits(n, expected):
    assert reverse_digits(n) == expected

@pytest.mark.parametrize("n", [12.34, "123", None])
def test_reverse_digits_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        reverse_digits(n)


# --- 5. is_abundant_number ---
@pytest.mark.parametrize(
    "n, expected", [(12, True), (18, True), (20, True), (24, True), (1, False), (10, False)]
)
def test_is_abundant_number(n, expected):
    assert is_abundant_number(n) is expected

@pytest.mark.parametrize("n", [0, -1, -12, 12.5, "12"])
def test_is_abundant_number_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        is_abundant_number(n)


# --- 6. distance_between_points ---
@pytest.mark.parametrize(
    "x1, y1, x2, y2, expected",
    [(0, 0, 3, 4, 5.0), (1, 1, 1, 1, 0.0), (-1, -1, 2, 3, 5.0), (0, 0, 0, 5, 5.0)],
)
def test_distance_between_points(x1, y1, x2, y2, expected):
    assert distance_between_points(x1, y1, x2, y2) == expected


# --- 7. midpoint ---
@pytest.mark.parametrize(
    "x1, y1, x2, y2, expected",
    [(0, 0, 4, 6, (2.0, 3.0)), (1, 1, 1, 1, (1.0, 1.0)), (-2, 4, 2, -4, (0.0, 0.0)), (0, 0, 5, 5, (2.5, 2.5))],
)
def test_midpoint(x1, y1, x2, y2, expected):
    assert midpoint(x1, y1, x2, y2) == expected


# --- 8. sum_of_squares ---
@pytest.mark.parametrize(
    "numbers, expected", [([1, 2, 3], 14.0), ([0, 0, 0], 0.0), ([-1, -2], 5.0), ([2.5], 6.25)]
)
def test_sum_of_squares(numbers, expected):
    assert sum_of_squares(numbers) == expected

@pytest.mark.parametrize("numbers", ["123", 123, None])
def test_sum_of_squares_rejects_invalid_input(numbers):
    with pytest.raises(ValueError):
        sum_of_squares(numbers)


# --- 9. calculate_simple_interest ---
@pytest.mark.parametrize(
    "principal, rate, time, expected",
    [(1000, 5, 2, 100.0), (500, 10, 1, 50.0), (0, 5, 2, 0.0), (1000, 0, 2, 0.0)],
)
def test_calculate_simple_interest(principal, rate, time, expected):
    assert calculate_simple_interest(principal, rate, time) == expected

@pytest.mark.parametrize(
    "principal, rate, time", [("1000", 5, 2), (1000, "5", 2), (1000, 5, "2"), (None, 5, 2)]
)
def test_calculate_simple_interest_rejects_invalid_input(principal, rate, time):
    with pytest.raises(ValueError):
        calculate_simple_interest(principal, rate, time)


# --- 10. collatz_sequence ---
@pytest.mark.parametrize(
    "n, expected",
    [
        (1, [1]),
        (2, [2, 1]),
        (3, [3, 10, 5, 16, 8, 4, 2, 1]),
        (6, [6, 3, 10, 5, 16, 8, 4, 2, 1]),
    ],
)
def test_collatz_sequence(n, expected):
    assert collatz_sequence(n) == expected

@pytest.mark.parametrize("n", [0, -1, -6, 6.5, "6"])
def test_collatz_sequence_rejects_invalid_input(n):
    with pytest.raises(ValueError):
        collatz_sequence(n)
