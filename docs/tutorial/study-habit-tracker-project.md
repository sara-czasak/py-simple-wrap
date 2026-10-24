# Building a Study Habit Tracker with Easy Date Formatter, Easy Stats, and Easy Data Visualization

Combine **Easy Date Formatter**, **Easy Stats**, and **Easy Data Visualization** to track daily study sessions, analyze study consistency, and visualize your progress across the week.

## What we are building

Whether you are preparing for exams or building a daily coding habit, seeing your study patterns helps you stay consistent. In this project, we track daily study sessions, calculate your weekly average and variability with `easy_stats`, format report timestamps with `easy_date_formatter`, and render a clean progress line chart with `easy_data_visualization`.

Create `study_tracker.py`:

```python
from py_simple import (
    data_range,
    get_pretty_date,
    mean,
    median,
    plot_line_chart,
)

# 1. Study time recorded across the week (in minutes)
study_sessions = [
    {"day": "Mon", "minutes": 45},
    {"day": "Tue", "minutes": 60},
    {"day": "Wed", "minutes": 30},
    {"day": "Thu", "minutes": 90},
    {"day": "Fri", "minutes": 50},
    {"day": "Sat", "minutes": 120},
    {"day": "Sun", "minutes": 75},
]

days = [entry["day"] for entry in study_sessions]
minutes = [entry["minutes"] for entry in study_sessions]

# 2. Analyze the week's study stats
avg_minutes = mean(minutes)
median_minutes = median(minutes)
spread = data_range(minutes)
total_hours = sum(minutes) / 60

# 3. Print the weekly summary with a formatted date
report_date = get_pretty_date()
print(f"=== Study Habit Report ({report_date}) ===")
print(f"Total time studied: {total_hours:.1f} hours ({sum(minutes)} mins)")
print(f"Daily average:      {avg_minutes:.1f} mins/day")
print(f"Median session:     {median_minutes:.1f} mins")
print(f"Session spread:     {spread:.1f} mins (difference between shortest and longest)")

# 4. Plot the study trend over the week
plot_line_chart(
    labels=days,
    values=minutes,
    title="Weekly Study Trend",
    x_label="Day of Week",
    y_label="Minutes Studied",
)
```

Run the script to see your formatted habit summary in the terminal (note that the exact date in the header will depend on the day you run the script) and a clean line chart showing your daily progress:

```text
=== Study Habit Report (Saturday, October 24, 2026) ===
Total time studied: 7.8 hours (470 mins)
Daily average:      67.1 mins/day
Median session:     60.0 mins
Session spread:     90.0 mins (difference between shortest and longest)
```

## What happened?

1. `get_pretty_date()` generates a human-friendly date string including the weekday (such as "Saturday, October 24, 2026") for your report without needing complex `strftime` directives (the exact date and weekday will reflect when the script runs).
2. `mean(minutes)` computes your average daily study time, while `median(minutes)` gives the middle session length, showing your true typical study effort even when a weekend study marathon spikes the average.
3. `data_range(minutes)` calculates the difference between your highest (120 mins) and lowest (30 mins) days to show habit variance.
4. `plot_line_chart(days, minutes, ...)` draws a clean line chart with marked data points and labels the axes without raw Matplotlib boilerplate.

## Why use these helpers?

Building this analysis from scratch in Python usually requires:
- Importing `datetime` and looking up formatting codes (`%B %d, %Y`) just to print the current date cleanly.
- Importing the `statistics` module or writing manual loops for sums, means, medians, and ranges.
- Writing several lines of `matplotlib.pyplot` code to initialize subplots, draw plots, configure titles, remove unnecessary frame borders, and call `plt.show()`.

By combining `easy_date_formatter`, `easy_stats`, and `easy_data_visualization`, you get a complete personal analytics tool in under 30 readable lines of code.
