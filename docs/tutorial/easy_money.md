# Easy Money

Prices show up in club sales, bake sales, and split lunches. Formatting them
by hand is where extra pennies and missing zeros sneak in. `easy_money` rounds
to cents and prints a currency symbol for you.

## A small real-world example

Imagine three friends sharing a $48 pizza, and the shop adds 8.5% tax first.

```python
from py_simple import add_tax, format_money, split_bill

with_tax = add_tax(48, 8.5)
each = split_bill(with_tax, 3)

print(format_money(with_tax))
print(format_money(each))
```

Example output:

```text
$52.08
$17.36
```

## What happened?

`add_tax()` takes the price and a percent, then returns the total rounded to
cents.

`remove_tax()` finds the original pre-tax price from a tax-inclusive total.

`calculate_tip()` calculates the tip amount to add based on a percentage.

`split_bill()` divides that total by the number of people and rounds each
share to cents.

`format_money()` prints the result with a dollar sign and two decimal places.
Pass another symbol, such as `"€"`, when you need one.

## Calculating tips and discounts

Use `calculate_tip()` to find the tip on a bill:

```python
from py_simple import calculate_tip, format_money

tip = calculate_tip(50, 18)
print(format_money(tip))  # $9.00
```

Use `calculate_discount()` to find the price after subtracting a discount:

```python
from py_simple import calculate_discount, format_money

sale_price = calculate_discount(100, 15)
print(format_money(sale_price))  # $85.00
```

Use `remove_tax()` to reverse a tax rate and find the original pre-tax price:

```python
from py_simple import format_money, remove_tax

pre_tax = remove_tax(10.85, 8.5)
print(format_money(pre_tax))  # $10.00
```

## Keep every cent when splitting a bill

Use `split_bill_exact()` when you need all the shares to add up to the full
bill, even when it cannot be divided evenly:

```python
from py_simple import split_bill_exact

shares = split_bill_exact("10.00", 3)
print(shares)  # [Decimal('3.34'), Decimal('3.33'), Decimal('3.33')]
print(sum(shares))  # 10.00
```

It returns one `Decimal` per person, each with two decimal places. The total
is rounded once to cents using `ROUND_HALF_UP`, then leftover cents go to
the first shares. For example, `"0.015"` shared by two people becomes
`[Decimal('0.01'), Decimal('0.01')]`. Refunds follow the same allocation:
`split_bill_exact(-10, 3)` gives `-3.34`, `-3.33`, `-3.33`. Zero shares are
`Decimal('0.00')`, including when a negative amount rounds to zero.

The amount may be an integer, float, numeric string or `Decimal`. Floats are
converted through their string representation; strings or `Decimal` values
are useful when entering exact amounts. Non-finite amounts and invalid inputs
raise `EasyMoneyError`. The number of people must be a positive integer,
excluding booleans. Amounts must be representable to cents in the current
Decimal context; precision or rounding-trap failures also raise `EasyMoneyError`.

`split_bill()` keeps its existing behavior: it returns one rounded share,
so `split_bill(10, 3)` is still `Decimal('3.33')`.

## Growing savings with compound interest

Use `calculate_compound_interest()` to find what savings grow to when
interest is added to the balance each period:

```python
from py_simple import calculate_compound_interest, format_money

balance = calculate_compound_interest(1000, 5, 2)
print(format_money(balance))  # $1102.50
```

Pass `12` as the fourth argument for monthly compounding instead of the
default yearly compounding. The rate is a percent per year, and the result
is rounded to cents.

## Why use these helpers?

Float math can print `17.359999999` when you only wanted `$17.36`. These
helpers use decimal rounding, so the number you show someone is the number
you calculated.
