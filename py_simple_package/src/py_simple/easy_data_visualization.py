"""
easy_data_visualization aims to simplify data visualization.
without requiring users to memorize every chart type or matplotlib function.
"""

from collections import Counter
from typing import Literal

import matplotlib.pyplot as plt


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

    _fig, axes = plt.subplots(1, 2, figsize=(10, 5))

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
