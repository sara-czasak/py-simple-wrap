# Easy Math

Performing common mathematical operations is something you'll often need in Python projects. Calculating factorials, Fibonacci sequences, prime factors, divisors, and least common multiples can require repetitive mathematical logic.

The `easy_math` module provides simple helpers for these common operations without requiring you to write the underlying algorithms yourself.

## A small real-world example

Imagine you're creating a program that needs to analyze a number. You want to find its divisors, prime factors, and the sum of its digits.

```python id="p7k2mz"
from py_simple import divisors, prime_factorization, sum_of_digits

number = 12

print(divisors(number))
print(prime_factorization(number))
print(sum_of_digits(number))
```

Example output:

```text id="q8s4nd"
[1, 2, 3, 4, 6, 12]
[2, 2, 3]
3
```

## What happened?

`divisors()` returns every positive integer that divides a number evenly.

`prime_factorization()` breaks a positive integer into its prime factors, including repeated factors.

`sum_of_digits()` adds all the digits of an integer together.

The module also provides helpers for factorials, Fibonacci sequences, and least common multiples:

```python id="v5j9kx"
from py_simple import factorial, fibonacci, get_least_common_multiple

print(factorial(5))
# 120

print(fibonacci(6))
# [0, 1, 1, 2, 3, 5]

print(get_least_common_multiple(4, 6))
# 12
```

## The Py_simple Way

```python id="n3x7qa"
from py_simple import (
    get_least_common_multiple,
    factorial,
    fibonacci,
    prime_factorization,
    sum_of_digits,
    divisors,
)

print(get_least_common_multiple(4, 6))
print(factorial(5))
print(fibonacci(5))
print(prime_factorization(12))
print(sum_of_digits(1234))
print(divisors(12))
```

## The Traditional Way

Without `py_simple`, you would normally have to implement these operations yourself or combine Python's built-in functionality with your own algorithms.

For example, calculating a factorial manually:

```python id="c4m8pw"
n = 5
result = 1

for number in range(2, n + 1):
    result *= number

print(result)
```

Generating Fibonacci numbers:

```python id="x2q6vs"
count = 5
sequence = [0, 1]

while len(sequence) < count:
    sequence.append(sequence[-1] + sequence[-2])

print(sequence[:count])
```

Finding prime factors:

```python id="j9r3kf"
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

print(factors)
```

The `easy_math` helpers package these common mathematical patterns into reusable functions.

## Working with numbers

`factorial()` calculates the factorial of a non-negative integer:

```python id="r5v2hb"
from py_simple import factorial

print(factorial(5))
```

Output:

```text id="z1m7pd"
120
```

`fibonacci()` returns the number of Fibonacci values you request:

```python id="m8q4sx"
from py_simple import fibonacci

print(fibonacci(7))
```

Output:

```text id="e3k9wf"
[0, 1, 1, 2, 3, 5, 8]
```

`get_least_common_multiple()` finds the smallest positive number that is divisible by both inputs:

```python id="u6p3nx"
from py_simple import get_least_common_multiple

print(get_least_common_multiple(4, 6))
```

Output:

```text id="a7v2kc"
12
```

If either number is `0`, the result is `0`.

## Prime factors and divisors

`prime_factorization()` returns the prime factors of a positive integer:

```python id="h4q8zm"
from py_simple import prime_factorization

print(prime_factorization(60))
```

Output:

```text id="w2n5jr"
[2, 2, 3, 5]
```

`divisors()` returns every positive divisor:

```python id="k7s3fd"
from py_simple import divisors

print(divisors(12))
```

Output:

```text id="m9x1vc"
[1, 2, 3, 4, 6, 12]
```

## Working with digits

`sum_of_digits()` adds all digits in an integer together.

```python id="q5b8ln"
from py_simple import sum_of_digits

print(sum_of_digits(1234))
```

Output:

```text id="t3r6kp"
10
```

Negative numbers are supported as well. The minus sign is ignored:

```python id="y8c2vf"
print(sum_of_digits(-1234))
```

Output:

```text id="d4m7qs"
10
```

## Error handling

The math helpers validate their inputs and raise `ValueError` when an operation receives an invalid value.

For example, factorials cannot be calculated for negative numbers:

```python id="p2x9zk"
from py_simple import factorial

try:
    print(factorial(-5))
except ValueError as error:
    print(error)
```

Similar validation is performed for operations that require positive integers or specific input types.

## Why use these helpers?

Instead of repeatedly implementing mathematical algorithms yourself, you can simply use:

```python id="r7n4bc"
get_least_common_multiple(4, 6)
factorial(5)
fibonacci(10)
prime_factorization(60)
sum_of_digits(1234)
divisors(12)
```

These helpers keep common mathematical operations simple, readable, and beginner-friendly while handling the underlying algorithms and calculations for you.
