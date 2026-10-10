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

`split_bill()` divides that total by the number of people and rounds each
share to cents.

`format_money()` prints the result with a dollar sign and two decimal places.
Pass another symbol, such as `"€"`, when you need one.

## Why use these helpers?

Float math can print `17.359999999` when you only wanted `$17.36`. These
helpers use decimal rounding, so the number you show someone is the number
you calculated.
