# SpendSmart: Build a Personal Expense Analyzer with Easy CSV and Easy Stats

Keeping track of daily expenses can help you understand your spending habits. SpendSmart combines **Easy CSV** and **Easy Stats** to save expense records in a CSV file and calculate useful statistics with simple Python functions.

## What we are building

Imagine you want to record expenses such as food, transport, and shopping. Instead of calculating everything manually, you can store your expenses in a CSV file and let Python find the median expense and the difference between your highest and lowest expenses.

```python
from py_simple import (
    write_csv_from_list,
    read_csv_to_list,
    median,
    data_range,
)

# 1. Create some sample expense records
sample_expenses = [
    {"Category": "Food", "Amount": "250"},
    {"Category": "Transport", "Amount": "100"},
    {"Category": "Shopping", "Amount": "500"},
    {"Category": "Food", "Amount": "150"},
    {"Category": "Transport", "Amount": "200"},
]

# 2. Save the expenses to a CSV file
write_csv_from_list("expenses.csv", sample_expenses)

# 3. Read the saved expense records
expenses = read_csv_to_list("expenses.csv")

# 4. Convert the amounts from text to numbers
amounts = [float(expense["Amount"]) for expense in expenses]

# 5. Calculate useful spending statistics
middle_expense = median(amounts)
expense_range = data_range(amounts)

print("Expenses:", expenses)
print("Median expense:", middle_expense)
print("Expense range:", expense_range)
```

Example output:

```text
pygame-ce 2.5.8 (SDL 2.32.10, Python 3.13.7)
Expenses: [{'Category': 'Food', 'Amount': '250'}, {'Category': 'Transport', 'Amount': '100'}, {'Category': 'Shopping', 'Amount': '500'}, {'Category': 'Food', 'Amount': '150'}, {'Category': 'Transport', 'Amount': '200'}]
Median expense: 200.0
Expense range: 400.0
```

The pygame startup message may differ depending on your environment. The expense records and statistics above are from the tested example.

## What happened?

1. `write_csv_from_list()` saves the expense records in `expenses.csv`, making them available for later use.
2. `read_csv_to_list()` reads the saved CSV file and returns the records as a list of dictionaries.
3. `float()` converts each expense amount from text into a number so Python can perform calculations.
4. `median()` finds the middle amount when the expenses are arranged in order. For our sample values (100, 150, 200, 250, and 500), the median is 200.
5. `data_range()` calculates the difference between the largest and smallest amounts. Here, 500 - 100 = 400.

## Why use these helpers?

Without these helpers, you would need to work directly with Python's CSV reader and writer, handle file operations, and implement statistical calculations yourself. Easy CSV and Easy Stats provide straightforward functions for these common tasks, allowing beginners to focus on building useful projects rather than writing repetitive code.