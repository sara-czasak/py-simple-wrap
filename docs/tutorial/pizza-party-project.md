# Building a Pizza Party Bill Splitter with Easy Money and Easy CSV

Combine **Easy Money** and **Easy CSV** to calculate discounts, tax, and split costs among friends, then save an itemized summary to a spreadsheet.

## What we are building

When ordering food for a group, calculating each person's share after coupons and tax usually requires multiple calculations. This example calculates the total, divides it evenly among four friends, and writes a clean summary to a CSV file that can be read back and shared.

```python
from py_simple import (
    add_tax,
    calculate_discount,
    format_money,
    read_csv_to_list,
    split_bill,
    write_csv_from_list,
)

items = [
    {"item": "Pizza Party Pack", "price": 60.0},
    {"item": "Garlic Bread", "price": 12.0},
    {"item": "Soda Pitcher", "price": 8.0},
]

subtotal = sum(item["price"] for item in items)
discounted = calculate_discount(subtotal, 10.0)
with_tax = add_tax(discounted, 8.0)
per_person = split_bill(with_tax, 4)

summary_rows = [
    {"description": "Subtotal", "amount": format_money(subtotal)},
    {"description": "After 10% coupon", "amount": format_money(discounted)},
    {"description": "Total with 8% tax", "amount": format_money(with_tax)},
    {"description": "Per person (4 friends)", "amount": format_money(per_person)},
]

write_csv_from_list("pizza_party.csv", summary_rows)
saved = read_csv_to_list("pizza_party.csv")
for row in saved:
    print(f"{row['description']}: {row['amount']}")
```

Example output:

```text
Subtotal: $80.00
After 10% coupon: $72.00
Total with 8% tax: $77.76
Per person (4 friends): $19.44
```

## What happened?

1. `calculate_discount(subtotal, 10.0)` applies a 10% discount to the initial sum and returns the discounted total.
2. `add_tax(discounted, 8.0)` computes the total after applying an 8% sales tax rate.
3. `split_bill(with_tax, 4)` divides the bill evenly among 4 people.
4. `format_money()` converts numbers and decimals into formatted currency strings with two decimal places.
5. `write_csv_from_list()` saves the rows to `pizza_party.csv`, using dictionary keys as header columns.
6. `read_csv_to_list()` reads the saved spreadsheet back into a list of row dictionaries so values can be displayed.

## Why use these helpers?

Calculating currency with floating-point math often introduces rounding errors. `easy_money` handles exact decimal values under the hood and formats them cleanly. Paired with `easy_csv`, you can save and load tabular records without writing boilerplate file-opening and CSV writer code.
