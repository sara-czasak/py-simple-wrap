# Build a Sleep Diary with Easy Config, Easy Logging, Easy Numbers, and Easy Flow

Combine **Easy Config**, **Easy Logging**, **Easy Numbers**, and **Easy Flow** to create a simple sleep diary that records your sleep hours, calculates your weekly average, and warns you when you are not getting enough sleep.

## A small real-world example

Imagine you are a student who thinks they are getting enough sleep but wants to check their sleep habits. In this example, you will set a daily sleep goal, record your sleep hours for seven nights, and check whether your weekly average meets your goal.

The example uses a temporary directory, so you can run it multiple times without changing or overwriting files in your project.

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import (
    average,
    create_env_file,
    log_to_file,
    read_env_file,
    read_recent_log_lines,
    run_if,
)

sleep_hours = [7.5, 8, 6.5, 7, 8.5, 6, 7.5]

with TemporaryDirectory() as workspace:
    env_file = str(Path(workspace) / ".env")
    log_file = str(Path(workspace) / "sleep.log")

    # 1. Save your sleep goal in a .env file
    create_env_file({"SLEEP_GOAL": "8"}, file_path=env_file)

    # 2. Log one week of sleep (7 nights)
    for hours in sleep_hours:
        log_to_file(log_file, str(hours))

    # 3. Read the last 7 nights and compute the average
    recent_logs = read_recent_log_lines(log_file, 7)
    average_sleep = average([float(line) for line in recent_logs])

    print("Average sleep:", average_sleep)

    # 4. Read the goal back and warn if the average is below it
    goal = float(read_env_file(env_file)["SLEEP_GOAL"])

    run_if(average_sleep < goal, print, "Warning: You are not getting enough sleep!")
```

Example output:

```text
Average sleep: 7.29
Warning: You are not getting enough sleep!
```

## What happened?

Let's look at each helper function in the order it was called.

**1. `create_env_file()` — Easy Config**

```python
create_env_file({"SLEEP_GOAL": "8"}, file_path=env_file)
```

This creates a `.env` file and stores the daily sleep goal. By specifying `file_path`, we can choose exactly where the file is saved.

**2. `log_to_file()` — Easy Logging**

```python
for hours in sleep_hours:
    log_to_file(log_file, str(hours))
```

This records each night's sleep hours in `sleep.log`. Each call adds one entry to the file. The function does not automatically add a timestamp, so each line contains only the recorded sleep hours.

**3. `read_recent_log_lines()` — Easy Logging**

```python
recent_logs = read_recent_log_lines(log_file, 7)
```

This reads the last seven lines from the log file. It is useful when you only need the most recent entries rather than the entire file.

**4. `average()` — Easy Numbers**

```python
average_sleep = average([float(line) for line in recent_logs])
```

The log entries are strings, so we convert them into floating-point numbers using `float()` before calculating the average. The `average()` helper calculates the mean and rounds the result to two decimal places (7.2857... becomes 7.29).

**5. `read_env_file()` — Easy Config**

```python
goal = float(read_env_file(env_file)["SLEEP_GOAL"])
```

This reads the `.env` file and returns a dictionary of environment variables as strings. We access the value using the `"SLEEP_GOAL"` key and convert it to a number with `float()` so that we can compare it with the weekly average.

**6. `run_if()` — Easy Flow**

```python
run_if(average_sleep < goal, print, "Warning: You are not getting enough sleep!")
```

This executes `print()` only when the condition is `True`. If the condition is `False`, nothing happens and the function returns `None`.

## Try it yourself

What happens if you change `SLEEP_GOAL` from `"8"` to `"7"`?

Since the weekly average is 7.29 hours, the warning should disappear. Try changing the goal or replacing `sleep_hours` with your own sleep data for a more personal sleep diary!

## Why use these helpers?

You could build the same program using only Python's standard library, but you would need to handle several tasks yourself:

- Parse the `.env` file and manage its contents.
- Open log files and manually retrieve the last N lines.
- Calculate and round the average.
- Write conditional logic to decide when to display a warning.

These helpers make each task simpler and let you focus on the actual purpose of your program.

Want to learn more? Check out the individual tutorials:

- [Easy Config](easy_config.md)
- [Easy Logging](easy_logging.md)
- [Easy Numbers](easy_numbers.md)
- [Easy Flow](easy_flow.md)
