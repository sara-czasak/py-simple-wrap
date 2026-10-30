# Build a Website Health Monitor

Combine **Easy Web**, **Easy CSV**, and **Easy Terminal** to build a command-line
application that monitors health of websites and saves a report.

You will read website addresses from a CSV file, check the health of each address, pretty-print the results, and also save a report to another CSV file.
You should be comfortable with Python loops, dictionaries, and functions
before starting.

## Set up the project

Use Python 3.11 or later and install the package with its web and terminal extras:

```bash
python -m pip install "py-simple-wrap[web,terminal]"
```

Create a folder containing two files:

```text
website-monitor/
    websites.csv
    monitor.py
```

Add these addresses to `websites.csv`:

```csv
url
https://www.google.com
https://github.com
https://offline.invalid
https://www.python.org
https://youtube.com
```

The first row is the column name, `url`. Be sure to include `https://` or `http://` in
each address. The `offline.invalid` address is deliberately invalid so you
can see how the monitor handles a failed request.

## Build the monitor

Copy and paste the example below into `monitor.py`:

```python
from pathlib import Path

from py_simple import (
    EasyTerminal,
    get_page_title,
    get_csv_columns,
    is_page_up,
    read_csv_to_list,
    write_csv_from_list,
)
from py_simple.easy_web import SomethingWentWrongError


def check_website(url: str) -> dict[str, str]:
    """Check a URL and return its status, title, and any error details."""
    result = {"url": url, "status": "OFFLINE", "title": "", "error": ""}

    try:
        online = is_page_up(url)
    except SomethingWentWrongError as error:
        result["error"] = str(error).strip()
        return result

    if not online:
        result["error"] = "The response did not have HTTP status 200."
        return result

    result["status"] = "ONLINE"

    try:
        result["title"] = get_page_title(url) or ""
    except SomethingWentWrongError as error:
        result["error"] = f"Title unavailable: {str(error).strip()}"

    return result


def main() -> None:
    """Read website addresses, display their health, and save a CSV report."""
    folder = Path(__file__).resolve().parent
    input_file = folder / "websites.csv"
    report_file = folder / "website_health.csv"

    print("─" * 60)
    EasyTerminal("WEBSITE HEALTH MONITOR").set_bold().show()
    print("─" * 60)
    # 1. Read list of websites from websites.csv.
    try:
        columns = get_csv_columns(str(input_file))
        websites = read_csv_to_list(str(input_file))
    except (OSError, ValueError) as error:
        EasyTerminal(f"Cannot read websites.csv: {error}").set_color("red").show()
        return

    if "url" not in columns:
        print("websites.csv must have a column named url.")
        return

    urls = [row.get("url", "").strip() for row in websites]
    urls = [url for url in urls if url]

    if not urls:
        print("No websites to check. Add addresses below the url header.")
        return

    print(f"\nChecking {len(urls)} websites...\n")
    results = []
    # 2. For each website address check its online status.
    for url in urls:
        result = check_website(url)
        results.append(result)

        online = result["status"] == "ONLINE"
        symbol = "✓" if online else "✗"
        color = "green" if online else "red"
        message = f"[{symbol}] {url:<36} {result['status']}"
        EasyTerminal(message).set_color(color).show()

    # 3. Compute statistics and display results in terminal.
    total = len(results)
    online_count = sum(result["status"] == "ONLINE" for result in results)
    offline_count = total - online_count
    availability = online_count / total * 100

    print()
    print(" SUMMARY ".center(60, "─"))
    print(f"Total Websites: {total}")
    print(f"Online:         {online_count}")
    print(f"Offline:        {offline_count}")
    print(f"Availability:   {availability:.0f}%")
    print()

    # 4. Save results to a csv file.
    write_csv_from_list(str(report_file), results)
    print(f"Report saved: {report_file.name}")

### Entry point of script ###
if __name__ == "__main__":
    main()
```

## Run it

Open a terminal in your project folder and run:

```bash
python monitor.py
```

Example output (results will depend on your connection and the websites):

```text
────────────────────────────────────────────────────────────
WEBSITE HEALTH MONITOR
────────────────────────────────────────────────────────────

Checking 5 websites...

[✓] https://www.google.com               ONLINE
[✓] https://github.com                   ONLINE
[✗] https://offline.invalid              OFFLINE
[✓] https://www.python.org               ONLINE
[✓] https://youtube.com                  ONLINE

───────────────────────── SUMMARY ──────────────────────────
Total Websites: 5
Online:         4
Offline:        1
Availability:   80%

Report saved: website_health.csv
```

## What happened?

### Reading the website list

`read_csv_to_list()` uses the first CSV row as column names and returns a list
of dictionaries. Each website becomes a row such as
`{"url": "https://github.com"}`.

`get_csv_columns()` reads the actual header so an empty first data row does not
hide a valid `url` column. The script checks that header, strips surrounding whitespace from
addresses, and skips empty addresses. If there are no addresses, it stops
before calculating a percentage or trying to write an empty report.

### Checking each website

`is_page_up()` returns `True` when the final HTTP response has status `200`.

HTTP errors, connection problems, and timeouts raise `SomethingWentWrongError`.
The `try`/`except` inside `check_website()` records the error and lets the loop
continue to the next website. Other responses that return `False` also count
as offline in this example.

Here, **OFFLINE means the check did not pass**. It does not prove the website
is unavailable to everyone: a website might block automated requests, or your
connection might have a problem. The report's `error` column gives more detail.

After a successful health check, `get_page_title()` makes another request to
retrieve the HTML title. Wrapping it in its own `try`/`except` keeps a title retrieval failure
from changing an `ONLINE` result to `OFFLINE`. For example, a page might
respond successfully but have no title element.

### Styling the terminal output

`EasyTerminal()` holds the text you want to display. `set_color()` selects its
color, `set_bold()` emphasizes the heading, and `show()` prints it.
`print()` repeats the `─` character to separate the heading and summary from the
results.

### Calculating the summary and saving the report

The script counts the `ONLINE` results and subtracts that number from the
total to get the offline count. Availability is calculated as:

```text
online websites / total websites × 100
```

Four passing checks out of five give `80%`. This is the percentage of websites
that passed **this run** and not a measurement of uptime over a period of time.

`write_csv_from_list()` writes the result dictionaries to `website_health.csv`,
using their keys as the header: `url,status,title,error`. Each checked address
has one report row, including failed checks. The final save message on the terminal appears only after the file is written;
a file-writing failure raises an error instead.

## Challenge to try yourself
- Add a timestamp column to show when each check ran.
- Run checks every 30 seconds using `time.sleep()`. Keep an accumulated history
  to measure availability over time.
- Highlight title retrieval errors in yellow while keeping the health status
  green when the initial check passed.

## Helpers in this project
These are the helpers used in this project:

| Module | Helpers |
| --- | --- |
| Easy Web | `is_page_up()`, `get_page_title()` |
| Easy CSV | `get_csv_columns()`, `read_csv_to_list()`, `write_csv_from_list()` |
| Easy Terminal | `EasyTerminal`, `set_color()`, `set_bold()`, `show()` |

## Why use these helpers?

The helpers help you handle HTTP requests, CSV parsing and
writing, and terminal styling in the simple and easy way. This health monitor connects those pieces into a
workflow: read, check, display, summarize, and save.

For more examples, see [Easy Web](easy_web.md), [Easy CSV](easy_csv.md),
and [Easy Terminal](easy_terminal.md).
