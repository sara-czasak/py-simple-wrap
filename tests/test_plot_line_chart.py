import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from py_simple_package.src.py_simple import plot_line_chart as public_plot_line_chart
from py_simple_package.src.py_simple.easy_data_visualization import plot_line_chart


@pytest.fixture(autouse=True)
def mock_plt_show(monkeypatch):
    """Prevent matplotlib from popping up windows during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")


def test_plot_line_chart_draws_one_line():
    plot_line_chart(["Mon", "Tue", "Wed"], [3.5, 2.0, 4.5])
    ax = plt.gca()
    assert len(ax.lines) == 1


def test_plot_line_chart_points_match_values():
    plot_line_chart(["A", "B", "C"], [1, 5, 3])
    line = plt.gca().lines[0]
    assert list(line.get_ydata()) == [1, 5, 3]


def test_plot_line_chart_sets_title_and_axis_labels():
    plot_line_chart(
        ["Mon", "Tue"],
        [3.5, 2.0],
        title="My Screen Time",
        x_label="Day",
        y_label="Hours",
    )
    ax = plt.gca()
    assert ax.get_title() == "My Screen Time"
    assert ax.get_xlabel() == "Day"
    assert ax.get_ylabel() == "Hours"


def test_plot_line_chart_without_title_or_labels_leaves_them_blank():
    plot_line_chart(["A", "B"], [1, 2])
    ax = plt.gca()
    assert ax.get_title() == ""
    assert ax.get_xlabel() == ""
    assert ax.get_ylabel() == ""


def test_plot_line_chart_uses_labels_on_x_axis():
    plot_line_chart(["Mon", "Tue", "Wed"], [1, 2, 3])
    fig = plt.gcf()
    fig.canvas.draw()
    tick_text = [t.get_text() for t in plt.gca().get_xticklabels()]
    assert tick_text == ["Mon", "Tue", "Wed"]


def test_plot_line_chart_accepts_numeric_labels():
    plot_line_chart([2024, 2025, 2026], [10, 20, 30])
    assert len(plt.gca().lines) == 1


def test_plot_line_chart_empty_labels_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_line_chart([], [1, 2])


def test_plot_line_chart_empty_values_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_line_chart(["A", "B"], [])


def test_plot_line_chart_mismatched_lengths_raises_value_error():
    with pytest.raises(ValueError, match="same length"):
        plot_line_chart(["A", "B", "C"], [1, 2])


def test_plot_line_chart_non_numeric_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_line_chart(["A", "B"], [1, "two"])


def test_plot_line_chart_boolean_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_line_chart(["A", "B"], [1, True])


def test_plot_line_chart_is_available_from_public_api():
    assert public_plot_line_chart is plot_line_chart