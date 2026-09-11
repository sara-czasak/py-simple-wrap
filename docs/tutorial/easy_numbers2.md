# Easy Numbers

Working with numbers is something you'll often need in Python projects. Checking whether numbers are even, odd, positive, negative, or prime, as well as calculating averages, percentages, and common divisors, can require repetitive code.

The `easy_numbers` module provides simple helpers for common number operations, making them easier to use without writing the underlying logic yourself.

## A small real-world example

Imagine you're processing a collection of numbers and need to check their properties and calculate some basic statistics.

```python
from py_simple import is_even, is_prime, average, percentage_of

number = 90
numbers = [10, 20, 30, 40]

print(is_even(number))
print(is_prime(number))
print(average(numbers))
print(percentage_of(number, 0.5))
```

Example output:

```text
True
False
25.0
45.0
```

## What happened?

`is_even()` checks whether a number is even.

`is_odd()` checks whether a number is odd.

`is_evenly_divisible()` checks whether a number can be divided evenly by another number.

`is_positive()` and `is_negative()` check the sign of a number.

You can also calculate averages, percentages, rounding values, greatest common divisors, and check whether a number is prime.

```python
from py_simple import is_odd, is_evenly_divisible, is_positive, is_negative, is_prime

print(is_odd(67))
# True

print(is_evenly_divisible(90, 9))
# True

print(is_positive(90))
# True

print(is_negative(-10))
# True

print(is_prime(97))
# True
```

## The Py_simple Way

```python
from py_simple import (
    is_even,
    is_odd,
    is_evenly_divisible,
    is_positive,
    is_negative,
    average,
    is_prime,
    percentage_of,
    round_to_nearest,
    greatest_common_divisor,
    clamp,
)

print(is_even(90))
print(is_odd(67))
print(is_evenly_divisible(90, 9))
print(is_positive(90))
print(is_negative(-10))
print(average([1.5, 2, 3]))
print(is_prime(97))
print(percentage_of(100, 0.5))
print(round_to_nearest(23, 5))
print(greatest_common_divisor(12, 18))
print(clamp(15, 0, 10))
```

## The Traditional Way

Without `py_simple`, many of these operations require writing the comparisons or mathematical logic yourself:

```python
import math

number = 90

# Even
even = number % 2 == 0

# Odd
odd = number % 2 == 1

# Evenly divisible
divisible = number % 9 == 0

# Positive
positive = number > 0

# Negative
negative = number < 0

# Average
numbers = [1.5, 2, 3]
average = round(sum(numbers) / len(numbers), 2)

# Percentage
percentage = round(100 * 0.5, 2)

# Greatest common divisor
gcd = math.gcd(12, 18)

# Clamp
clamped = max(0, min(15, 10))
```

For operations such as checking whether a number is prime, you would also need to implement the algorithm yourself.

The `easy_numbers` helpers package these common patterns into simple, reusable functions.

## Checking numbers

The module provides several helpers for checking the properties of a number:

```python
from py_simple import is_even, is_odd, is_positive, is_negative

print(is_even(10))
# True

print(is_odd(7))
# True

print(is_positive(10))
# True

print(is_negative(-10))
# True
```

`is_evenly_divisible()` can check whether one number divides evenly into another:

```python
from py_simple import is_evenly_divisible

print(is_evenly_divisible(90, 9))
# True

print(is_evenly_divisible(10, 3))
# False
```

## Averages and percentages

`average()` calculates the average of a list of numbers and rounds the result to two decimal places:

```python
from py_simple import average

print(average([1.5, 2, 3]))
```

Output:

```text
2.17
```

`percentage_of()` calculates a percentage using a value between `0` and `1`:

```python
from py_simple import percentage_of

print(percentage_of(200, 0.25))
```

Output:

```text
50.0
```

For example, `0.5` represents 50%, while `0.25` represents 25%.

## Prime numbers

`is_prime()` checks whether a number is prime:

```python
from py_simple import is_prime

print(is_prime(2))
# True

print(is_prime(15))
# False

print(is_prime(97))
# True
```

A prime number is a number greater than 1 that can only be divided evenly by 1 and itself.

## Rounding and ranges

`round_to_nearest()` rounds a number to the nearest multiple you provide:

```python
from py_simple import round_to_nearest

print(round_to_nearest(23, 5))
```

Output:

```text
25
```

`clamp()` keeps a number inside a specified minimum and maximum range:

```python
from py_simple import clamp

print(clamp(15, 0, 10))
# 10

print(clamp(-5, 0, 10))
# 0

print(clamp(5, 0, 10))
# 5
```

This can be useful when you need to make sure a value never goes outside an allowed range.

## Greatest common divisor

`greatest_common_divisor()` calculates the GCD of two numbers:

```python
from py_simple import greatest_common_divisor

print(greatest_common_divisor(12, 18))
```

Output:

```text
6
```

The GCD is the largest positive integer that divides both numbers without leaving a remainder.

## Error handling

Some helpers validate their inputs and raise `ValueError` when they receive an invalid value.

For example, `round_to_nearest()` cannot use zero as the nearest multiple:

```python
from py_simple import round_to_nearest

try:
    print(round_to_nearest(23, 0))
except ValueError as error:
    print(error)
```

Output:

```text
'nearest' must not be zero.
```

Other functions perform similar validation when an operation requires a specific type or range of values.

## Why use these helpers?

Instead of repeatedly writing mathematical comparisons and calculations, you can simply use:

```python
is_even(number)
is_odd(number)
is_evenly_divisible(number, divisor)
is_positive(number)
is_negative(number)
average(numbers)
is_prime(number)
percentage_of(number, percentage)
round_to_nearest(number, nearest)
greatest_common_divisor(a, b)
clamp(number, minimum, maximum)
```

These helpers keep common number operations simple, readable, and beginner-friendly while handling the underlying comparisons, calculations, and algorithms for you.
