# Easy Data Visualization

Working with data visualization often means choosing the right chart and writing several lines of plotting code. The `easy_data_visualization` module simplifies this process by automatically identifying whether your data is quantitative or categorical and suggesting an appropriate chart.

## A small real-world example

Imagine you're analyzing a set of values and want to quickly visualize the data without deciding which chart type to use or writing the usual Matplotlib setup yourself.

```python
from py_simple import plot_data

data = [1, 2, 2, 3, 5, 5, 5, 8]

plot_data(data)
```

Example output:

```text
Plotting data...
```

The function automatically creates suitable visualizations, such as a histogram and a line chart, for the quantitative data.

## What happened?

`plot_data()` examines the data and determines whether it is quantitative or categorical before selecting appropriate chart types.

For example, numerical data can be visualized with a histogram and line chart:

```python
plot_data([1, 2, 3, 4, 5])
```

Categorical data can be visualized with a bar chart and pie chart:

```python
plot_data(["Python", "Python", "Java", "C++"])
```

You can also provide two data series. When both are quantitative, `plot_data()` creates a scatter plot:

```python
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 8, 10]

plot_data(x, y)
```

The module uses `_infer_type()` internally to classify each series as either `quantitative` or `categorical`, allowing `plot_data()` to choose the appropriate visualization automatically.

## Dedicated Chart Functions

When you already know the exact visualization you want and want to label axes and titles, `easy_data_visualization` provides dedicated helpers:

```python
from py_simple import (
    plot_bar_chart,
    plot_line_chart,
    plot_pie_chart,
    plot_scatter_chart,
)

# Scatter plot: Explore relationships between two numeric sets
plot_scatter_chart(
    x_values=[1, 2, 3, 4, 5],
    y_values=[10, 20, 25, 30, 50],
    title="Study Hours vs Test Score",
    x_label="Hours Studied",
    y_label="Score (%)",
)
```

## Why use these helpers?

Instead of manually checking your data, choosing a chart, creating Matplotlib figures, and configuring each axis, you can simply write:

```python
plot_data(data)
```

or:

```python
plot_data(x, y)
```

This keeps data visualization simple, readable, and beginner-friendly while letting `easy_data_visualization` handle the chart selection and Matplotlib boilerplate for you.