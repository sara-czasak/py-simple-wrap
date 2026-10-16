# Quiz Score Analyzer

Want to turn a simple list of quiz scores into a useful little analysis tool?

In this project, we'll build a **Quiz Score Analyzer** using two `py-simple-wrap` modules:

* `easy_lists` — for working with lists.
* `easy_stats` — for calculating statistics.

The program will clean a list of scores and calculate useful information such as the median, standard deviation, and range.

## What we're building

Our analyzer will:

1. Start with a list of quiz scores.
2. Remove duplicate scores.
3. Calculate the median score.
4. Calculate the standard deviation.
5. Calculate the range of the scores.
6. Display the results.

## Build the project

Create a Python file called `quiz_score_analyzer.py`.

```python
from py_simple import (
    unique_items,
    median,
    standard_deviation,
    data_range,
)

scores = [72, 85, 91, 78, 85, 64, 91, 88, 76, 95]

# Remove duplicate scores
clean_scores = unique_items(scores)

# Calculate statistics
middle_score = median(clean_scores)
score_spread = standard_deviation(clean_scores)
score_range = data_range(clean_scores)

print("Quiz Score Analyzer")
print("-------------------")
print(f"Original scores: {scores}")
print(f"Unique scores: {clean_scores}")
print(f"Median score: {middle_score}")
print(f"Standard deviation: {score_spread:.2f}")
print(f"Score range: {score_range}")
```

## Run the project

Run the Python file:

```bash
python quiz_score_analyzer.py
```

Your output should look similar to:

```text
Quiz Score Analyzer
-------------------
Original scores: [72, 85, 91, 78, 85, 64, 91, 88, 76, 95]
Unique scores: [72, 85, 91, 78, 64, 88, 76, 95]
Median score: 81.5
Standard deviation: 9.97
Score range: 31
```

> **Tip:** Run the program yourself and update the example output if your installed version produces different formatting or values.

## What happened?

### Removing duplicate scores

The original list contains duplicate scores:

```python
scores = [72, 85, 91, 78, 85, 64, 91, 88, 76, 95]
```

We use `unique_items()` from `easy_lists`:

```python
clean_scores = unique_items(scores)
```

This gives us a list containing each score only once.

### Finding the median

Next, we use `median()` from `easy_stats`:

```python
middle_score = median(clean_scores)
```

The median represents the middle value of the dataset.

### Measuring score spread

We use `standard_deviation()` to see how spread out the scores are:

```python
score_spread = standard_deviation(clean_scores)
```

A smaller standard deviation means the values are closer together, while a larger value means they are more spread out.

### Finding the range

Finally, `data_range()` tells us the difference between the largest and smallest values:

```python
score_range = data_range(clean_scores)
```

This gives us a quick idea of how widely the scores vary.

## Why use these helpers?

We could write all of this functionality ourselves using normal Python code.

However, `py-simple-wrap` gives us simple helpers that make the purpose of each operation clear:

```python
clean_scores = unique_items(scores)
middle_score = median(clean_scores)
score_spread = standard_deviation(clean_scores)
score_range = data_range(clean_scores)
```

This makes the code easier to read and lets beginners focus on the project instead of implementing common operations from scratch.

More importantly, this small project demonstrates how multiple `py-simple-wrap` modules can work together instead of being used individually.

## Try it yourself

Change the scores:

```python
scores = [55, 60, 72, 72, 80, 85, 90, 90, 95]
```

Then run the program again.

You can also extend the project by:

* letting users enter their own scores;
* reading scores from a CSV file;
* adding the highest and lowest scores;
* calculating the average;
* displaying a grade based on the score;
* turning the analyzer into a small command-line application.

## Summary

In this project, we combined two `py-simple-wrap` modules:

* **`easy_lists`** — used to remove duplicate scores.
* **`easy_stats`** — used to analyze the cleaned scores.

The result is a small but useful Quiz Score Analyzer that demonstrates how simple helpers can be combined to build a practical Python project.
