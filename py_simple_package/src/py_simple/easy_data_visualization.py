"""
easy_data_visualization aims to simplify data visualization.
without requiring users to memorize every chart type or matplotlib function.
"""

from collections import Counter
from typing import Literal


def plot_data(X: list, Y: list | None = None):
    """
    Infers the type of the given data (quantitative or categorical) and
    automatically plots the most appropriate chart(s) for it, handling
    the chart-type selection, axis setup, and matplotlib boilerplate
    every data visualization needs.

    Args:
        X (list): The primary data series to plot.
        Y (list, optional): A second data series to plot against `X`.
            If omitted, only `X` is visualized on its own. Defaults to
            `None`.

    Returns:
        None: The chart(s) are rendered directly via `plt.show()`.
            One or two subplots are created depending on how many
            chart types are suggested for the given data combination
            (e.g. a categorical `X` alone suggests both a bar chart
            and a pie chart).

    Raises:
        KeyError: If the inferred type combination of `X` and `Y` has
            no matching entry in `CHART_SUGGESTIONS` (e.g. two
            categorical series).
        ValueError: If `X` or `Y` is an empty list (raised internally
            by `_infer_type`).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import plot_data

            plot_data([1, 2, 2, 3, 5, 5, 5, 8])
            ```

        === "The Traditional Way"
            ```python
            import matplotlib.pyplot as plt

            data = [1, 2, 2, 3, 5, 5, 5, 8]
            fig, ax = plt.subplots()
            ax.hist(data)
            ax.set_title("Histogram")
            ax.spines[['top', 'right']].set_visible(False)
            plt.show()
            ```
    """
    import matplotlib.pyplot as plt

    # Figure out whether each series is "quantitative" or "categorical"
    # so we can look up which chart(s) make sense for this combination.
    type_X = _infer_type(X)

    type_Y = _infer_type(Y) if Y is not None else None

    CHART_SUGGESTIONS = {
        ("quantitative", None): ["histogram", "line"],
        ("categorical", None): ["barchart", "pie"],
        ("quantitative", "quantitative"): ["scatter"],
        ("quantitative", "categorical"): ["barchart"],
        ("categorical", "quantitative"): ["barchart"],
    }

    charts = CHART_SUGGESTIONS[(type_X, type_Y)]
    chart_index = 0  # tracks which subplot slot to draw into next

    # One subplot per suggested chart, so a single chart fills the figure
    _fig, axes = plt.subplots(
        1, len(charts), figsize=(5 * len(charts), 5), squeeze=False
    )

    if "histogram" in charts:
        ax = axes.flat[chart_index]
        ax.hist(X)
        ax.set_title("Histogram")
        ax.spines[["top", "right"]].set_visible(False)
        chart_index += 1

    if "line" in charts:
        ax = axes.flat[chart_index]
        ax.plot(X)
        ax.set_title("Line chart")
        ax.spines[["top", "right"]].set_visible(False)
        chart_index += 1

    if "barchart" in charts:
        ax = axes.flat[chart_index]

        if Y is None:
            # Single categorical/quantitative series: bar per index.
            ax.bar(range(len(X)), X)
        else:
            # Two series: put the categorical one on the x-axis and the
            # quantitative one as the bar height, regardless of which
            # argument (X or Y) is which.
            if (type_X, type_Y) == ("categorical", "quantitative"):
                ax.bar(X, Y)
            else:
                ax.bar(Y, X)

        ax.set_title("Bar chart")
        ax.spines[["top", "right"]].set_visible(False)
        chart_index += 1

    if "pie" in charts:
        ax = axes.flat[chart_index]
        counts = Counter(X)
        ax.pie(counts.values(), labels=counts.keys(), autopct="%1.1f%%")
        ax.set_title("Pie chart")
        chart_index += 1

    if "scatter" in charts:
        ax = axes.flat[chart_index]
        ax.scatter(X, Y)
        ax.set_title("Scatter plot")
        chart_index += 1

    # Remove any subplot slots that weren't used (e.g. when only one
    # chart type was suggested for the given data).
    for ax in axes.flat[chart_index:]:
        ax.remove()

    print("Plotting data...")
    plt.show()


def plot_heatmap(
    data: list[list[int | float]],
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
) -> None:
    """
    Displays a heatmap for a two-dimensional numeric data series.

    A heatmap represents values in a grid using color intensity, making it
    useful for quickly spotting patterns, differences, and high or low values
    across a two-dimensional dataset.

    Args:
        data (list[list[int | float]]): A rectangular two-dimensional list
            containing numeric values.
        title (str, optional): Text shown above the heatmap. Defaults to
            `None` (no title).
        x_label (str, optional): Text shown under the x-axis. Defaults to
            `None` (no label).
        y_label (str, optional): Text shown beside the y-axis. Defaults to
            `None` (no label).

    Returns:
        None: The heatmap is rendered directly via `plt.show()`.

    Raises:
        ValueError: If `data` is empty, is not two-dimensional, is not
            rectangular, or contains non-numeric values.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import plot_heatmap

            plot_heatmap(
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                title="Example Heatmap",
                x_label="Columns",
                y_label="Rows",
            )
            ```

        === "The Traditional Way"
            ```python
            import matplotlib.pyplot as plt

            data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            fig, ax = plt.subplots()
            image = ax.imshow(data)
            fig.colorbar(image, ax=ax)
            ax.set_title("Example Heatmap")
            ax.set_xlabel("Columns")
            ax.set_ylabel("Rows")
            plt.show()
            ```
    """
    import matplotlib.pyplot as plt

    if not data:
        raise ValueError("The data cannot be empty.")

    if not all(isinstance(row, list) for row in data):
        raise ValueError("The data must be two-dimensional.")

    if any(not row for row in data):
        raise ValueError("The data must contain non-empty rows.")

    row_length = len(data[0])
    if any(len(row) != row_length for row in data):
        raise ValueError("The data must be rectangular.")

    if not all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for row in data
        for value in row
    ):
        raise ValueError("All values must be numbers.")

    fig, ax = plt.subplots()
    image = ax.imshow(data)
    fig.colorbar(image, ax=ax)

    if title:
        ax.set_title(title)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)

    ax.spines[["top", "right"]].set_visible(False)
    plt.show()


def plot_box_plot(data: list[float]) -> None:
    """
    Displays a box-and-whisker plot for a numeric data series.

    A box plot shows the middle half of the data, the median, and possible
    outliers, making it useful for quickly understanding the distribution of
    a list of numbers.

    Args:
        data (list[float]): The numeric values to visualize.

    Returns:
        None: The box plot is rendered directly via `plt.show()`.

    Raises:
        ValueError: If `data` is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import plot_box_plot

            plot_box_plot([12, 14, 15, 15, 16, 18, 30])
            ```

        === "The Traditional Way"
            ```python
            import matplotlib.pyplot as plt

            data = [12, 14, 15, 15, 16, 18, 30]
            fig, ax = plt.subplots()
            ax.boxplot(data)
            ax.set_title("Box plot")
            plt.show()
            ```
    """
    import matplotlib.pyplot as plt

    if not data:
        raise ValueError("The data series cannot be empty.")

    _, ax = plt.subplots()
    ax.boxplot(data)
    ax.set_title("Box plot")
    ax.set_ylabel("Values")
    ax.spines[["top", "right"]].set_visible(False)
    plt.show()


def _infer_type(series) -> Literal["quantitative", "categorical"]:
    """
    Inspects a list of values and classifies it as either
    "quantitative" (all numeric, excluding booleans) or "categorical"
    (anything else, including booleans), so `plot_data` can decide
    which chart types are appropriate.

    Args:
        series (list): The data series to classify.

    Returns:
        Literal["quantitative", "categorical"]: `"quantitative"` if
            every value in `series` is an `int` or `float` (and not a
            `bool`); `"categorical"` otherwise — this includes lists
            containing booleans, strings, or mixed types.

    Raises:
        ValueError: If `series` is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import _infer_type

            kind = _infer_type([1, 2, 3])  # -> "quantitative"
            kind = _infer_type(["a", "b"])  # -> "categorical"
            ```

        === "The Traditional Way"
            ```python
            series = [1, 2, 3]
            if not series:
                raise ValueError("The series cannot be empty.")

            is_quantitative = all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in series
            )
            kind = "quantitative" if is_quantitative else "categorical"
            ```
    """
    if not series:
        raise ValueError("The series cannot be empty.")

    is_quantitative = all(
        isinstance(x, (int, float)) and not isinstance(x, bool) for x in series
    )
    return "quantitative" if is_quantitative else "categorical"


def get_data_range(data: list[int | float]) -> tuple[int | float, int | float]:
    """
    Calculates the minimum and maximum values of a numeric data series,
    providing a quick summary range for data inspection before plotting.

    Args:
        data (list): A list of quantitative (int or float) values.

    Returns:
        tuple: A tuple containing the minimum and maximum values (min, max).

    Raises:
        ValueError: If `data` is empty or contains non-numeric values.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple.easy_data_visualization import get_data_range

            min_val, max_val = get_data_range([5, 2, 9, 1, 7])
            ```

        === "The Traditional Way"
            ```python
            data = [5, 2, 9, 1, 7]
            if not data:
                raise ValueError("Data series cannot be empty.")
            min_val = min(data)
            max_val = max(data)
            ```
    """
    if not data:
        raise ValueError("The data series cannot be empty.")

    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in data):
        raise ValueError("All elements in the data series must be numbers.")

    return (min(data), max(data))


def plot_bar_chart(
    labels: list[str],
    values: list[int | float],
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
) -> None:
    """
    Displays a bar chart with an optional title and axis labels.

    Unlike `plot_data`, which picks a chart type for you, this function
    always draws a bar chart and lets you name the chart and its axes, so
    the result is ready to share or screenshot.

    Args:
        labels (list[str]): The name of each bar (shown on the x-axis).
        values (list[int | float]): The height of each bar.
        title (str, optional): Text shown above the chart. Defaults to
            `None` (no title).
        x_label (str, optional): Text shown under the x-axis. Defaults to
            `None` (no label).
        y_label (str, optional): Text shown beside the y-axis. Defaults to
            `None` (no label).

    Returns:
        None: The bar chart is rendered directly via `plt.show()`.

    Raises:
        ValueError: If `labels` or `values` is empty, if they have
            different lengths, or if any value is not a number.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import plot_bar_chart

            plot_bar_chart(
                ["Mon", "Tue", "Wed"],
                [3.5, 2.0, 4.5],
                title="My Screen Time",
                x_label="Day",
                y_label="Hours",
            )
            ```

        === "The Traditional Way"
            ```python
            import matplotlib.pyplot as plt

            labels = ["Mon", "Tue", "Wed"]
            values = [3.5, 2.0, 4.5]
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            ax.set_title("My Screen Time")
            ax.set_xlabel("Day")
            ax.set_ylabel("Hours")
            ax.spines[["top", "right"]].set_visible(False)
            plt.show()
            ```
    """
    import matplotlib.pyplot as plt

    if not labels or not values:
        raise ValueError("Labels and values cannot be empty.")

    if len(labels) != len(values):
        raise ValueError("Labels and values must have the same length.")

    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
        raise ValueError("All values must be numbers.")

    _, ax = plt.subplots()
    ax.bar([str(label) for label in labels], values)

    if title:
        ax.set_title(title)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)

    ax.spines[["top", "right"]].set_visible(False)
    plt.show()


def plot_pie_chart(
    labels: list[str],
    values: list[int | float],
    title: str | None = None,
) -> None:
    """
    Displays a pie chart that shows how a whole splits into parts.

    Each value becomes one slice. Labels name the slices, and an
    optional title sits above the chart.

    Args:
        labels (list[str]): The name of each slice.
        values (list[int | float]): The size of each slice. Values must
            be numbers and cannot be negative.
        title (str, optional): Text shown above the chart. Defaults to
            `None` (no title).

    Returns:
        None: The pie chart is rendered directly via `plt.show()`.

    Raises:
        ValueError: If `labels` or `values` is empty, if they have
            different lengths, if any value is not a number, or if any
            value is negative.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import plot_pie_chart

            plot_pie_chart(
                ["Walk", "Bus", "Bike"],
                [12, 7, 5],
                title="How we get to school",
            )
            ```

        === "The Traditional Way"
            ```python
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            ax.pie([12, 7, 5], labels=["Walk", "Bus", "Bike"])
            ax.set_title("How we get to school")
            plt.show()
            ```
    """
    import matplotlib.pyplot as plt

    if not labels or not values:
        raise ValueError("Labels and values cannot be empty.")

    if len(labels) != len(values):
        raise ValueError("Labels and values must have the same length.")

    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
        raise ValueError("All values must be numbers.")

    if any(v < 0 for v in values):
        raise ValueError("Pie chart values cannot be negative.")

    _, ax = plt.subplots()
    ax.pie(values, labels=[str(label) for label in labels])
    if title:
        ax.set_title(title)
    plt.show()
