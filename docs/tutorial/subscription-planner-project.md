# Build a Subscription Budget Planner with Easy Money and Easy Date Formatter

Combine **Easy Money** and **Easy Date Formatter** to calculate discounted subscription costs, apply sales tax, and predict upcoming payment due dates.

## A small real-world example

When managing recurring memberships, software subscriptions, or club dues, keeping track of exact costs after taxes alongside upcoming renewal deadlines can get messy. This example calculates monthly costs after applying a discount and sales tax, and projects future renewal dates into clear, human-readable strings without modifying any external files.

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from decimal import Decimal

from py_simple import (
    add_tax,
    calculate_discount,
    format_money,
    future_dd_mm_yyyy,
    get_future_pretty_date,
)

subscriptions = [
    {"service": "Music Streaming", "monthly_fee": 12.0, "renewal_days": 5},
    {"service": "Cloud Backup", "monthly_fee": 8.0, "renewal_days": 14},
    {"service": "Dev Tools Pro", "monthly_fee": 25.0, "renewal_days": 30},
]

print("--- Upcoming Subscription Renewals ---")

total_monthly = Decimal("0.00")
for sub in subscriptions:
    discounted = calculate_discount(sub["monthly_fee"], 15.0)
    final_cost = add_tax(discounted, 8.0)
    total_monthly += final_cost

    due_date = future_dd_mm_yyyy(sub["renewal_days"])
    formatted_amount = format_money(final_cost)
    name = sub["service"]
    print(f"{name}: {formatted_amount} (due {due_date})")

print(f"\nTotal Monthly Budget: {format_money(total_monthly)}")
print(f"Earliest renewal: {get_future_pretty_date(5)}")
```

Example output:

```text
--- Upcoming Subscription Renewals ---
Music Streaming: $11.02 (due 09-11-2026)
Cloud Backup: $7.34 (due 18-11-2026)
Dev Tools Pro: $22.95 (due 04-12-2026)

Total Monthly Budget: $41.31
Earliest renewal: Monday, November 09, 2026
```

*(Note: The exact calendar dates and weekdays follow the day on which you run the script.)*

## What happened?

`calculate_discount(fee, 15.0)` reduces each monthly fee by 15% and returns an exact `Decimal` value, avoiding standard floating-point precision issues.

`add_tax(discounted, 8.0)` computes the final amount payable after applying an 8% sales tax rate to the discounted price.

`future_dd_mm_yyyy(days)` calculates the target calendar date a specific number of days into the future and returns it in `DD-MM-YYYY` format.

`format_money(amount)` converts the numeric amount into standard currency notation with a dollar symbol and two decimal places.

`get_future_pretty_date(days)` returns a friendly, written date (such as `Monday, November 09, 2026`) that is easy to present directly to users or reminder notifications.

## Try it yourself

Try calculating an annual subscription plan by using `calculate_discount(annual_fee, 25.0)` for a 25% annual discount, or use `future_slash_mm_dd_yyyy(days)` to format due dates using slashes (`MM/DD/YYYY`).

## Why use these helpers?

Doing financial math with standard Python `float` types introduces subtle binary rounding errors that can cause balances to be off by fractions of a cent. Meanwhile, calculating future calendar dates typically requires importing `datetime`, constructing `timedelta` objects, and remembering `strftime` formatting directive codes. With **Easy Money** and **Easy Date Formatter**, exact currency arithmetic and readable dates take only a single function call each.

For more details on each module, see the [Easy Money Tutorial](easy_money.md) and the [Easy Date Formatter Tutorial](easy_date_formatter.md).
