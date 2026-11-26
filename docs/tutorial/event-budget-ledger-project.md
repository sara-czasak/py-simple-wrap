# Build an Event Budget & Expense Ledger with Easy SQL and Easy Money

Combine **Easy SQL** and **Easy Money** to record expenses in an SQLite database, calculate taxes and discounts, and split costs evenly among attendees.

## A small real-world example

Organizing a meetup, hackathon, or team outing involves tracking shared expenses across multiple categories—such as catering, venue hire, and participant badges. Manually tracking receipts in spreadsheets often leads to floating-point currency rounding errors and messy calculations. This project creates an in-memory SQLite database ledger, applies sales tax and discounts to line items, stores clean expense records, tallies category totals, and computes the exact per-person share for all attendees.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `event_ledger.py`:

```python
from py_simple.easy_money import (
    add_tax,
    calculate_discount,
    format_money,
    split_bill,
)
from py_simple.easy_sql import (
    conditional_run_select,
    open_db,
    run_insert,
    run_select,
)

# 1. Connect to SQLite database and set up the schema
connection, cursor = open_db(":memory:")

cursor.execute(
    """
    CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        category TEXT,
        amount REAL
    )
"""
)

# 2. Prepare expense line items with taxes and discounts applied
raw_catering = 450.00
final_catering = float(add_tax(raw_catering, 8.5))  # 8.5% sales tax applied

raw_venue = 800.00
final_venue = float(
    calculate_discount(raw_venue, 15.0)
)  # 15.0% early-bird discount applied

raw_supplies = 120.00
final_supplies = float(add_tax(raw_supplies, 8.5))  # 8.5% sales tax applied

# 3. Insert records into the expenses table
run_insert(
    connection,
    cursor,
    ["Catering & Refreshments", "Food", final_catering],
    "expenses",
    ["item", "category", "amount"],
)
run_insert(
    connection,
    cursor,
    ["Main Hall Reservation", "Venue", final_venue],
    "expenses",
    ["item", "category", "amount"],
)
run_insert(
    connection,
    cursor,
    ["Badges & Signage", "Supplies", final_supplies],
    "expenses",
    ["item", "category", "amount"],
)

# 4. Fetch and display all expense records
records = run_select(connection, cursor, "expenses", "*")

print("--- Event Expense Ledger ---")
for record_id, item, category, amount in records:
    print(f"[{category.upper()}] {item}: {format_money(amount)}")

# 5. Filter expenses by category using conditional select
food_records = conditional_run_select(
    connection, cursor, "expenses", "*", "category = ?", ("Food",)
)
food_total = sum(r[3] for r in food_records)

# 6. Tally overall totals and split cost among attendees
total_cost = sum(r[3] for r in records)
attendee_count = 24
per_person_share = split_bill(total_cost, attendee_count)

print("----------------------------")
print(f"Food Subtotal: {format_money(food_total)}")
print(f"Total Event Cost: {format_money(total_cost)}")
print(f"Cost per attendee ({attendee_count} people): {format_money(per_person_share)}")
```

Run the script from your terminal:

```bash
python event_ledger.py
```

Example output:

```text
--- Event Expense Ledger ---
[FOOD] Catering & Refreshments: $488.25
[VENUE] Main Hall Reservation: $680.00
[SUPPLIES] Badges & Signage: $130.20
----------------------------
Food Subtotal: $488.25
Total Event Cost: $1298.45
Cost per attendee (24 people): $54.10
```

## What happened?

`open_db()` establishes a verified connection and returns both the SQLite connection and cursor objects without boilerplate `sqlite3.connect()` exception handling.

`add_tax()` calculates the additional tax on a transaction and returns the total sum as a precise `Decimal`.

`calculate_discount()` deducts the percentage discount from an amount and returns the discounted total.

`run_insert()` safely parameterizes and inserts a new row into the SQLite table while validating table and column identifiers against SQL injection.

`run_select()` retrieves all matching records from the table with built-in query execution and error guarding.

`conditional_run_select()` runs parameterized queries with `WHERE` clauses to easily isolate category-specific expenses.

`format_money()` formats numbers into clean currency strings with standard decimal separators and currency symbols.

`split_bill()` evenly divides a total amount across a given group count with proper banker's rounding.

## Try it yourself

- **Track vendor tips:** Call `calculate_tip()` from `Easy Money` to compute gratuity for catering staff before inserting into the ledger.
- **Distribute remainder pennies:** Use `split_bill_exact()` to generate an exact list of amounts where the sum precisely matches the total down to the cent.
- **Remove tax from gross invoices:** Use `remove_tax()` to determine the net price of an item when tax was already bundled into the sticker price.
- **Remove cancelled items:** Call `run_delete()` from `Easy SQL` to safely delete an expense row by ID if an activity gets cancelled.

## Why use these helpers?

Without `py-simple-wrap`, building this workflow requires substantial boilerplate and risks subtle financial rounding bugs:
- Managing raw `sqlite3.connect()`, manual cursor allocations, and repetitive `cursor.execute("INSERT ...")` string constructions.
- Manually sanitizing table names and column parameters to prevent accidental SQL injection vulnerabilities.
- Writing custom formatting logic (`f"${val:.2f}"`) that fails on floating-point precision issues like `0.1 + 0.2 != 0.3`.
- Implementing custom rounding logic when dividing bills across groups where fractions of a cent cannot be lost.

Combining `easy_sql` and `easy_money` gives you reliable database persistence and accurate financial calculations in clean, readable Python code.

For more examples and detailed function references, see [Easy SQL](easy_sql.md) and [Easy Money](easy_money.md).
