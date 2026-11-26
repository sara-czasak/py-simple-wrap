# Build an SQLite to CSV Data Exporter & Report Generator with Easy SQL and Easy CSV

Combine **Easy SQL** and **Easy CSV** to query database records, generate structured CSV inventory reports, and filter tabular output.

## A small real-world example

Developers, data analysts, and store administrators frequently need to export database tables into CSV spreadsheets for stakeholders or downstream processing. Writing manual database query scripts requires managing cursor iterations, file streams, delimiter encodings, and headers. This project sets up an SQLite inventory database, logs stock entries, queries records into a clean list, exports them directly to a formatted CSV spreadsheet, and filters specific product categories in memory.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `inventory_exporter.py`:

```python
from py_simple.easy_csv import (
    count_csv_rows,
    filter_csv_rows,
    read_csv_to_list,
    write_csv_from_list,
)
from py_simple.easy_sql import (
    open_db,
    run_insert,
    run_select,
)

# 1. Connect to SQLite database and define the inventory schema
connection, cursor = open_db(":memory:")

cursor.execute(
    """
    CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        category TEXT,
        quantity INTEGER,
        unit_price REAL
    )
"""
)

# 2. Insert sample inventory items into the database
run_insert(
    connection,
    cursor,
    ["Ergonomic Keyboard", "Peripherals", 45, 89.99],
    "inventory",
    ["item_name", "category", "quantity", "unit_price"],
)
run_insert(
    connection,
    cursor,
    ["USB-C Docking Station", "Peripherals", 18, 129.50],
    "inventory",
    ["item_name", "category", "quantity", "unit_price"],
)
run_insert(
    connection,
    cursor,
    ["27-inch 4K Monitor", "Displays", 12, 349.00],
    "inventory",
    ["item_name", "category", "quantity", "unit_price"],
)
run_insert(
    connection,
    cursor,
    ["Noise-Cancelling Headset", "Audio", 30, 75.00],
    "inventory",
    ["item_name", "category", "quantity", "unit_price"],
)

# 3. Retrieve all inventory records from the database
rows = run_select(connection, cursor, "inventory", "*")

# 4. Export database query results directly to a CSV file
output_csv = "inventory_report.csv"
headers = ["ID", "Item Name", "Category", "Quantity", "Unit Price"]
table_data = [list(r) for r in rows]

write_csv_from_list(output_csv, table_data, headers=headers)

# 5. Inspect and verify the generated CSV report
total_rows = count_csv_rows(output_csv)
records = read_csv_to_list(output_csv, return_dict=True)

print("--- Inventory Database Export ---")
print(f"Exported {total_rows} records to {output_csv}\n")

# 6. Filter and display specific categories using CSV helpers
peripherals = filter_csv_rows(output_csv, "Category", "Peripherals")

print("--- Peripherals Category ---")
for item in peripherals:
    print(
        f"• {item['Item Name']} | Qty: {item['Quantity']} | Price: ${float(item['Unit Price']):.2f}"
    )
```

Run the script from your terminal:

```bash
python inventory_exporter.py
```

Example output:

```text
--- Inventory Database Export ---
Exported 4 records to inventory_report.csv

--- Peripherals Category ---
• Ergonomic Keyboard | Qty: 45 | Price: $89.99
• USB-C Docking Station | Qty: 18 | Price: $129.50
```

## What happened?

`open_db()` connects to an SQLite database and returns the connection and cursor objects without boilerplate `sqlite3.connect()` and manual error handling.

`run_insert()` safely parameterizes and inserts individual rows into the database while guarding table and column identifiers against SQL injection.

`run_select()` retrieves all matching records from the target database table with built-in execution checks.

`write_csv_from_list()` takes tabular rows and column headers, creating a standard UTF-8 encoded CSV file on disk in a single step without manual `csv.writer` or `open()` calls.

`count_csv_rows()` inspects the generated CSV file and counts the total data rows without loading the entire dataset into memory.

`read_csv_to_list()` reads the CSV file back into memory, automatically mapping headers to row values when `return_dict=True` is specified.

`filter_csv_rows()` reads the CSV file and isolates only the rows matching a target column and value.

## Try it yourself

- **Sort items by price:** Call `sort_csv_by_column()` to sort the generated inventory CSV by price or quantity before sharing.
- **Append real-time restocks:** Use `append_row_to_csv()` to add new incoming shipments directly to the exported CSV without rewriting existing records.
- **Inspect columns dynamically:** Call `get_csv_columns()` to verify header names before running automated category filters.
- **Clean blank rows:** Use `drop_empty_csv_rows()` to strip out empty lines before archiving reports.

## Why use these helpers?

Without `py-simple-wrap`, this workflow requires repetitive standard library boilerplate and risks resource leaks:
- Manually allocating, closing, and handling connection exceptions across `sqlite3` cursors.
- Opening file streams (`open("report.csv", "w", newline="", encoding="utf-8")`), instantiating `csv.writer` or `csv.DictWriter`, and manually writing header rows.
- Writing custom loops and dictionary comprehensions to filter or map CSV rows back to dictionary objects.
- Handling edge cases with Windows carriage returns (`\r\n`) and missing column values.

Combining `easy_sql` and `easy_csv` turns complex database querying and file serialization into readable, single-line Python helpers.

For more examples and detailed function references, see [Easy SQL](easy_sql.md) and [Easy CSV](easy_csv.md).
