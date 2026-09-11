import pytest

from py_simple_package.src.py_simple.easy_numbers import (
    average,
    clamp,
    greatest_common_divisor,
    is_even,
    is_evenly_divisible,
    is_negative,
    is_odd,
    is_positive,
    is_prime,
    percentage_of,
    round_to_nearest,
)

# even


def test_is_even_with_even_number():
    assert is_even(4) is True


def test_is_even_with_odd_number():
    assert is_even(5) is False


def test_is_even_with_zero():
    assert is_even(0) is True


def test_is_even_with_negative_even():
    assert is_even(-8) is True


def test_is_even_with_negative_odd():
    assert is_even(-7) is False


# odd


def test_is_odd_with_odd_number():
    assert is_odd(5) is True


def test_is_odd_with_even_number():
    assert is_odd(4) is False


def test_is_odd_with_zero():
    assert is_odd(0) is False


def test_is_odd_with_negative_odd():
    assert is_odd(-5) is True


def test_is_odd_with_negative_even():
    assert is_odd(-4) is False


# evenly_divisible


def test_is_evenly_divisible_true():
    assert is_evenly_divisible(10, 5) is True


def test_is_evenly_divisible_false():
    assert is_evenly_divisible(10, 3) is False


def test_is_evenly_divisible_by_one():
    assert is_evenly_divisible(99, 1) is True


def test_is_evenly_divisible_equal_numbers():
    assert is_evenly_divisible(8, 8) is True


def test_is_evenly_divisible_negative_number():
    assert is_evenly_divisible(-10, 5) is True


def test_is_evenly_divisible_negative_divisor():
    assert is_evenly_divisible(10, -5) is True


def test_is_evenly_divisible_both_negative():
    assert is_evenly_divisible(-10, -5) is True


# positive


def test_is_positive_positive():
    assert is_positive(8) is True


def test_is_positive_negative():
    assert is_positive(-8) is False


def test_is_positive_zero():
    assert is_positive(0) is False


# negative


def test_is_negative_negative():
    assert is_negative(-8) is True


def test_is_negative_positive():
    assert is_negative(8) is False


def test_is_negative_zero():
    assert is_negative(0) is False


# average


def test_average_integers():
    assert average([2, 4, 6]) == 4.0


def test_average_floats():
    assert average([1.5, 2.5]) == 2.0


def test_average_single_number():
    assert average([5]) == 5.0


def test_average_negative_numbers():
    assert average([-2, -4]) == -3.0


def test_average_rounding():
    assert average([1, 2, 2]) == 1.67


# prime


def test_is_prime_two():
    assert is_prime(2) is True


def test_is_prime_three():
    assert is_prime(3) is True


def test_is_prime_composite():
    assert is_prime(9) is False


def test_is_prime_large_prime():
    assert is_prime(17) is True


def test_is_prime_one():
    assert is_prime(1) is False


def test_is_prime_zero():
    assert is_prime(0) is False


def test_is_prime_even_composite():
    assert is_prime(4) is False


def test_is_prime_large_even():
    assert is_prime(100) is False


def test_is_prime_negative():
    assert is_prime(-7) is False


def test_is_prime_odd_composite_square():
    assert is_prime(25) is False


# percentage


def test_percentage_half():
    assert percentage_of(100, 0.5) == 50.0


def test_percentage_quarter():
    assert percentage_of(80, 0.25) == 20.0


def test_percentage_zero():
    assert percentage_of(100, 0) == 0.0


def test_percentage_decimal():
    assert percentage_of(19, 0.4) == 7.6


# round_to_nearest


def test_round_to_nearest_rounds_up():
    assert round_to_nearest(23, 5) == 25.0


def test_round_to_nearest_rounds_down():
    assert round_to_nearest(21, 5) == 20.0


def test_round_to_nearest_exact_multiple():
    assert round_to_nearest(20, 5) == 20.0


def test_round_to_nearest_decimal_input():
    assert round_to_nearest(7.4, 2) == 8.0


def test_round_to_nearest_negative_number():
    assert round_to_nearest(-23, 5) == -25.0


def test_round_to_nearest_nearest_one():
    assert round_to_nearest(3.2, 1) == 3.0


def test_round_to_nearest_zero_raises_value_error():
    with pytest.raises(ValueError):
        round_to_nearest(10, 0)


# greatest_common_divisor


def test_gcd_coprime_numbers():
    assert greatest_common_divisor(7, 13) == 1


def test_gcd_shared_divisor():
    assert greatest_common_divisor(12, 18) == 6


def test_gcd_one_is_multiple_of_other():
    assert greatest_common_divisor(10, 30) == 10


def test_gcd_negative_numbers():
    assert greatest_common_divisor(-12, 18) == 6


def test_gcd_both_negative():
    assert greatest_common_divisor(-12, -18) == 6


def test_gcd_zero_and_number():
    assert greatest_common_divisor(0, 5) == 5


def test_gcd_both_zero():
    assert greatest_common_divisor(0, 0) == 0


# clamp


def test_clamp_within_range_unchanged():
    assert clamp(5, 0, 10) == 5


def test_clamp_above_maximum():
    assert clamp(15, 0, 10) == 10


def test_clamp_below_minimum():
    assert clamp(-3, 0, 10) == 0


def test_clamp_at_minimum():
    assert clamp(0, 0, 10) == 0


def test_clamp_at_maximum():
    assert clamp(10, 0, 10) == 10


def test_clamp_decimal_values():
    assert clamp(2.5, 1.0, 3.0) == 2.5


def test_clamp_negative_range():
    assert clamp(-5, -10, -1) == -5
