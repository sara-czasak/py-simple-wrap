# BookQuest: Build a Monthly Reading Tracker

In this tutorial, you'll build BookQuest, a simple Python application that helps you maintain a reading list, set a monthly reading goal, and review your reading progress over time.

You'll combine several `py_simple` modules:

- **Easy JSON** to save your books and monthly goal.
- **Easy Date Formatter** to display today's date.
- **Easy Stats** to analyze your monthly reading activity.
- **Easy Data Visualization** to visualize books completed per month.

## What you'll build

BookQuest lets you add books, record their start and finish dates, set a monthly target, and view a summary of your reading habits.

A book counts as completed in the month its finish date is recorded. A book still in progress is not counted as completed.

## Step 1: Import the helpers

Create a Python file named `bookquest.py` and import the required helpers:

```python
from datetime import date

from py_simple import (
    save_json_data,
    open_json,
    update_json,
    is_json_file,
    get_pretty_date,
    plot_bar_chart,
    plot_line_chart,
    median,
    standard_deviation,
    data_range,
)
```

Python's built-in `date` class records the start and finish dates. The `py_simple` helpers handle JSON storage, readable dates, statistics, and chart creation.

## Step 2: Store your reading data

We need to remember the reading list and monthly goal between program runs.

```python
DATA_FILE = "books.json"


def load_data():
    """Load the reading tracker or create a new one."""
    if is_json_file(DATA_FILE):
        data = open_json(DATA_FILE)
        data.setdefault("monthly_goal", 4)
        data.setdefault("books", [])
        return data

    data = {
        "monthly_goal": 4,
        "books": [],
    }
    save_json_data(DATA_FILE, data)
    return data


def save_data(data):
    """Save the latest reading tracker data."""
    if is_json_file(DATA_FILE):
        update_json(DATA_FILE, data)
    else:
        save_json_data(DATA_FILE, data)
```

`load_data()` opens the existing JSON file or creates a new reading tracker. `save_data()` persists changes to the file.

## Step 3: Add a book

Each book has a title, an optional author, a start date, a finish date, and a status.

```python
def add_book(data):
    """Add a book to the reading shelf."""
    title = input("Enter book title: ").strip()

    if not title:
        print("Book title cannot be empty.")
        return

    author = input("Enter author (optional): ").strip()

    book = {
        "title": title,
        "author": author,
        "start_date": date.today().isoformat(),
        "finish_date": None,
        "status": "reading",
    }

    data["books"].append(book)
    save_data(data)
    print(f"'{title}' added to your reading shelf!")
```

The start date is recorded when the book is added. Its finish date remains `None` until you complete it.

## Step 4: Complete a book

When you finish reading, record the finish date and update the status. In the full application, select a book from the list of books currently in progress first.

```python
book["finish_date"] = date.today().isoformat()
book["status"] = "completed"
save_data(data)
```

The finish date is stored in ISO format (`YYYY-MM-DD`), which makes it easy to group completed books by month.

## Step 5: Set a monthly goal

BookQuest starts with a goal of four books per month. You can change the goal and save it:

```python
try:
    goal = int(input("Enter your monthly book target: "))

    if goal >= 1:
        data["monthly_goal"] = goal
        save_data(data)
    else:
        print("Your goal must be at least one book.")

except ValueError:
    print("Please enter a whole number.")
```

The goal must be a positive whole number. Invalid input is handled without crashing the application.

## Step 6: Count books completed each month

We can use the first seven characters of a finish date, such as `2026-10`, as a month key.

```python
def get_monthly_totals(data):
    """Count books in the month they were finished."""
    totals = {}

    for book in data["books"]:
        finish_date = book.get("finish_date")

        if finish_date:
            month = finish_date[:7]
            totals[month] = totals.get(month, 0) + 1

    return totals
```

This function returns a dictionary containing the number of completed books per month. Books without a finish date are excluded.

For example, if two books were completed in October 2026 and one in September 2026, the result would be:

```python
{
    "2026-10": 2,
    "2026-09": 1,
}
```

## Step 7: Generate consecutive month labels

If no books were completed in a particular month, that month should still appear in the reading history with a count of zero.

```python
def get_month_labels(start_month, end_month):
    """Create consecutive month labels, including months with zero books."""
    labels = []
    year, month = map(int, start_month.split("-"))
    end_year, end_month_number = map(int, end_month.split("-"))

    while (year, month) <= (end_year, end_month_number):
        labels.append(f"{year}-{month:02d}")

        month += 1
        if month > 12:
            month = 1
            year += 1

    return labels
```

For example:

```python
months = get_month_labels("2026-08", "2026-11")
print(months)
```

Output:

```text
['2026-08', '2026-09', '2026-10', '2026-11']
```

This helper also handles year boundaries, such as December to January.

## Step 8: Display reading statistics

Easy Stats provides helpers for summarizing the monthly totals.

First, calculate the monthly totals, generate the month labels, and create a corresponding count for each month:

```python
totals = get_monthly_totals(data)

if totals:
    first_month = min(totals)
    current_month = date.today().strftime("%Y-%m")

    months = get_month_labels(first_month, current_month)
    counts = [totals.get(month, 0) for month in months]

    print("Median monthly total:", median(counts))
    print("Highest monthly total:", max(counts))
    print("Lowest monthly total:", min(counts))
    print("Monthly total range:", data_range(counts))

    if len(counts) >= 2:
        print("Standard deviation:", standard_deviation(counts))
    else:
        print("Standard deviation requires at least two months.")
else:
    print("Finish your first book to start your monthly history.")
```

Here:

- `months` contains consecutive month labels.
- `counts` contains the number of books completed in each month, including months with zero completions.
- `median()` returns the middle value of the monthly totals.
- `data_range()` returns the difference between the highest and lowest totals.
- `standard_deviation()` measures how spread out the totals are.

The `if totals:` condition ensures that the statistics are calculated only when at least one book has been completed.

## Step 9: Display a friendly date

Use Easy Date Formatter to show today's date in a readable format:

```python
print("Reading summary for", get_pretty_date())
```

The start and finish dates remain in ISO format so they can be grouped by month.

## Step 10: Visualize monthly reading activity

Once the monthly totals have been calculated, use `plot_bar_chart()` and `plot_line_chart()` from `py_simple` to visualize the results.

The variables `months` and `counts` were defined in Step 8. The following examples assume that at least one book has been completed and that those variables are available.

First, convert the month labels into a more readable format:

```python
display_months = [
    date(int(month[:4]), int(month[5:7]), 1).strftime("%b %Y")
    for month in months
]
```

For example, `"2026-10"` becomes `"Oct 2026"`.

### Create a bar chart

Use `plot_bar_chart()` to compare the number of books completed each month:

```python
plot_bar_chart(
    display_months,
    counts,
    title="Books Completed per Month",
    x_label="Month",
    y_label="Books Completed",
)
```

The bars make it easy to compare reading activity across months.

### Create a line chart

Use `plot_line_chart()` to visualize changes in your reading activity over time:

```python
plot_line_chart(
    display_months,
    counts,
    title="Monthly Reading Trend",
    x_label="Month",
    y_label="Books Completed",
)
```

The line chart helps you observe increases, decreases, and months with no completed books.

Both functions use the same month labels and counts, but display the information in different ways.

## Test your project

1. Add two books.
2. View your reading shelf.
3. Mark one book as completed.
4. Change your monthly goal.
5. Open the reading summary.
6. Check the monthly totals and charts.
7. Exit and run the application again.
8. Confirm that the books and goal are still saved.

## What happened?

You combined JSON storage, date formatting, statistics, and visualization to create a small reading tracker. Each helper handles a common task, leaving the application code to focus on managing books and displaying progress.

## Why use these helpers?

Without `py_simple`, you would need to write more of the file handling, date formatting, statistical calculations, and plotting setup yourself. These helpers make the project easier to read and provide a practical example of multiple modules working together.
