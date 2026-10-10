# Building a Homework Log with Easy Date Formatter and Easy Logging

Combine **Easy Date Formatter** and **Easy Logging** to keep a plain-text
log of finished homework, dated in a way you can read later.

## What we are building

Each time a task is done, the script writes one line with today's date and
a short note. The file is `homework.log`.

```python
from py_simple import get_pretty_date, log_to_file

today = get_pretty_date()
log_to_file("homework.log", f"{today} | math worksheet finished")
```

Example line in `homework.log`:

```text
Friday, October 10, 2026 | math worksheet finished
```

The weekday and date follow the day you run the script.

## What happened?

1. `get_pretty_date()` returns today as words, such as
   `Friday, October 10, 2026`, so you do not have to remember a
   `strftime` pattern.
2. `log_to_file()` creates `homework.log` if needed and appends the message
   as one line. Call it again with a different subject and the new line
   sits under the first.

## Why use these helpers?

The usual version imports `datetime`, picks a format string, then opens the
log in append mode. Here the date is already readable and the log write is
one call, which is enough for a homework list you check at the end of the
week.
