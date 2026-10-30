
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

DATA_FILE = "books.json"


# ---------- Easy JSON: save and load data ----------

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


# ---------- Add and view books ----------

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

    print(f"\n'{title}' added to your reading shelf!")


def view_books(data):
    """Display saved books and their statuses."""
    if not data["books"]:
        print("\nYour reading shelf is empty. Add your first book!")
        return

    print("\n========== MY READING SHELF ==========")

    for number, book in enumerate(data["books"], start=1):
        print(f"\n{number}. {book['title']}")

        if book.get("author"):
            print(f"   Author: {book['author']}")

        print(f"   Started: {book['start_date']}")
        print(f"   Status: {book['status']}")

        if book.get("finish_date"):
            print(f"   Finished: {book['finish_date']}")


# ---------- Mark a book as completed ----------

def finish_book(data):
    """Record when a book is finished."""
    unfinished = [
        book for book in data["books"]
        if book["status"] == "reading"
    ]

    if not unfinished:
        print("\nYou have no books in progress.")
        return

    print("\n========== BOOKS IN PROGRESS ==========")

    for number, book in enumerate(unfinished, start=1):
        print(f"{number}. {book['title']}")

    try:
        choice = int(input("Enter the number of the completed book: "))

        if not 1 <= choice <= len(unfinished):
            print("Please select a number from the list.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    book = unfinished[choice - 1]
    book["finish_date"] = date.today().isoformat()
    book["status"] = "completed"

    save_data(data)
    print(f"\nCongratulations! You finished '{book['title']}'!")


# ---------- Set monthly reading goal ----------

def set_monthly_goal(data):
    """Set a target for books completed each month."""
    try:
        goal = int(input("How many books do you want to finish per month? "))

        if goal < 1:
            print("Your goal must be at least one book.")
            return

    except ValueError:
        print("Please enter a whole number.")
        return

    data["monthly_goal"] = goal
    save_data(data)

    print(f"Your monthly goal is now {goal} books.")


# ---------- Calculate monthly totals ----------

def get_monthly_totals(data):
    """Count books in the month they were finished."""
    totals = {}

    for book in data["books"]:
        finish_date = book.get("finish_date")

        if finish_date:
            month = finish_date[:7]  # YYYY-MM
            totals[month] = totals.get(month, 0) + 1

    return totals


def get_month_labels(start_month, end_month):
    """Create chronological month labels, including months with zero books."""
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


# ---------- Reading summary, statistics and charts ----------

def reading_summary(data):
    """Show monthly progress, statistics and labeled charts."""
    totals = get_monthly_totals(data)
    today = date.today()
    current_month = today.strftime("%Y-%m")
    goal = data["monthly_goal"]
    completed_this_month = totals.get(current_month, 0)

    print("\n========== READING SUMMARY ==========")
    print("Today's date:", get_pretty_date())
    print("Current month:", current_month)
    print(f"Monthly goal: {goal} books")
    print(f"Completed this month: {completed_this_month}/{goal}")

    progress = min(completed_this_month / goal * 100, 100)
    print(f"Goal progress: {progress:.0f}%")

    if completed_this_month >= goal:
        print("You reached your monthly reading goal!")
    else:
        remaining = goal - completed_this_month
        print(f"{remaining} more book(s) to reach your goal.")

    if not totals:
        print("\nFinish your first book to start your monthly history.")
        return

    # Include zero-completion months between the first finish and this month.
    first_month = min(totals)
    months = get_month_labels(first_month, current_month)
    counts = [totals.get(month, 0) for month in months]

    print("\n========== MONTHLY READING HISTORY ==========")

    for month, count in zip(months, counts):
        book_word = "book" if count == 1 else "books"
        print(f"{month}: {count} {book_word}")

    # Easy Stats
    print("\n========== READING STATISTICS ==========")
    print("Median books per month:", median(counts))
    print("Highest monthly total:", max(counts))
    print("Lowest monthly total:", min(counts))
    print("Monthly total range:", data_range(counts))

    if len(counts) >= 2:
        print(
            "Standard deviation:",
            round(standard_deviation(counts), 2),
        )
    else:
        print("Standard deviation requires at least two months.")

    # Easy Data Visualization: labeled month names on the x-axis.
    display_months = [
        date(int(month[:4]), int(month[5:7]), 1).strftime("%b %Y")
        for month in months
    ]

    print("\nOpening monthly bar chart...")
    plot_bar_chart(
        display_months,
        counts,
        title="Books Completed per Month",
        x_label="Month",
        y_label="Books Completed",
    )

    print("\nOpening monthly trend line chart...")
    plot_line_chart(
        display_months,
        counts,
        title="Monthly Reading Trend",
        x_label="Month",
        y_label="Books Completed",
    )


# ---------- Main menu ----------

def main():
    """Run BookQuest."""
    data = load_data()

    while True:
        print("\n========== BOOKQUEST ==========")
        print("1. Add a book")
        print("2. View my reading shelf")
        print("3. Mark a book as completed")
        print("4. Set monthly reading goal")
        print("5. View monthly summary and statistics")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_book(data)
        elif choice == "2":
            view_books(data)
        elif choice == "3":
            finish_book(data)
        elif choice == "4":
            set_monthly_goal(data)
        elif choice == "5":
            reading_summary(data)
        elif choice == "6":
            print("Happy reading! See you next time.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
