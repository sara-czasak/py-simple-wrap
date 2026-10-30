import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from py_simple_package.src.py_simple import (
    plot_bar_chart as public_plot_bar_chart,
    plot_box_plot as public_plot_box_plot,
    plot_heatmap as public_plot_heatmap,
    plot_histogram as public_plot_histogram,
    plot_line_chart as public_plot_line_chart,
    plot_pie_chart as public_plot_pie_chart,
    plot_scatter_chart as public_plot_scatter_chart,
)
from py_simple_package.src.py_simple.easy_data_visualization import (
    _infer_type,
    plot_bar_chart,
    plot_box_plot,
    plot_data,
    plot_heatmap,
    plot_histogram,
    plot_line_chart,
    plot_pie_chart,
    plot_scatter_chart,
)


# --- Tests for _infer_type ---


def test_infer_type_quantitative_int():
    assert _infer_type([1, 2, 3, 4]) == "quantitative"


def test_infer_type_quantitative_float():
    assert _infer_type([1.5, 2.5, 3.5]) == "quantitative"


def test_infer_type_quantitative_mixed_numbers():
    assert _infer_type([1, 2.5, 3]) == "quantitative"


def test_infer_type_categorical_strings():
    assert _infer_type(["apple", "banana", "cherry"]) == "categorical"


def test_infer_type_categorical_booleans():
    assert _infer_type([True, False, True]) == "categorical"


def test_infer_type_categorical_mixed_types():
    assert _infer_type([1, "two", 3.0]) == "categorical"


def test_infer_type_empty_list_raises_value_error():
    with pytest.raises(ValueError, match="The series cannot be empty."):
        _infer_type([])


# --- Tests for plot_data ---


@pytest.fixture(autouse=True)
def mock_plt_show(monkeypatch):
    """Prevent matplotlib from popping up windows during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")


def test_plot_data_quantitative_single_series(capsys):
    plot_data([1, 2, 3, 4, 5])
    captured = capsys.readouterr()
    assert "Plotting data..." in captured.out


def test_plot_data_categorical_single_series(capsys):
    plot_data(["cat", "dog", "cat", "bird"])
    captured = capsys.readouterr()
    assert "Plotting data..." in captured.out


def test_plot_data_quantitative_quantitative(capsys):
    plot_data([1, 2, 3], [10, 20, 30])
    captured = capsys.readouterr()
    assert "Plotting data..." in captured.out


def test_plot_data_quantitative_categorical(capsys):
    plot_data([10, 20, 30], ["A", "B", "C"])
    captured = capsys.readouterr()
    assert "Plotting data..." in captured.out


def test_plot_data_categorical_quantitative(capsys):
    plot_data(["A", "B", "C"], [10, 20, 30])
    captured = capsys.readouterr()
    assert "Plotting data..." in captured.out


def test_plot_data_invalid_type_combination_raises_key_error():
    with pytest.raises(KeyError):
        plot_data(["A", "B"], ["X", "Y"])


def test_plot_data_empty_series_raises_value_error():
    with pytest.raises(ValueError, match="The series cannot be empty."):
        plot_data([])


# --- Tests for plot_box_plot ---


def test_plot_box_plot_creates_box_plot():
    plot_box_plot([12, 14, 15, 15, 16, 18, 30])

    ax = plt.gca()
    assert ax.get_title() == "Box plot"
    assert ax.get_ylabel() == "Values"
    assert len(ax.lines) > 0


def test_plot_box_plot_empty_series_raises_value_error():
    with pytest.raises(ValueError,
                       match="The data series cannot be empty."):
        plot_box_plot([])


def test_plot_box_plot_is_available_from_public_api():
    assert public_plot_box_plot is plot_box_plot


import pytest
from py_simple.easy_data_visualization import get_data_range


def test_get_data_range_success():
    assert get_data_range([10, 5, 20, 2]) == (2, 20)
    assert get_data_range([3.5, 1.1, 7.8]) == (1.1, 7.8)


def test_get_data_range_empty_error():
    with pytest.raises(ValueError):
        get_data_range([])


def test_get_data_range_invalid_type_error():
    with pytest.raises(ValueError):
        get_data_range([1, 2, "three"])


# --- Tests for plot_data figure layout ---


@pytest.mark.parametrize(
    "X, Y, expected_charts",
    [
        ([1, 2, 3, 4, 5], None, 2),
        (["cat", "dog", "cat"], None, 2),
        ([1, 2, 3], [10, 20, 30], 1),
        ([10, 20, 30], ["A", "B", "C"], 1),
        (["A", "B", "C"], [10, 20, 30], 1),
    ],
)
def test_plot_data_creates_one_subplot_per_chart(X, Y, expected_charts):
    plot_data(X, Y)
    fig = plt.gcf()
    assert len(fig.axes) == expected_charts
    plt.close(fig)


def test_plot_data_single_chart_fills_figure_width():
    plot_data(["Mon", "Tue", "Wed"], [3.5, 2.0, 4.5])
    fig = plt.gcf()
    assert fig.get_size_inches()[0] == 5
    assert fig.axes[0].get_position().width > 0.5
    plt.close(fig)


def test_plot_data_removes_unused_subplot_slots(monkeypatch):
    original_subplots = plt.subplots

    def subplots_with_extra_axis(*args, **kwargs):
        return original_subplots(1, 2, squeeze=False)

    monkeypatch.setattr(plt, "subplots", subplots_with_extra_axis)

    plot_data([1, 2, 3], [4, 5, 6])

    fig = plt.gcf()
    assert len(fig.axes) == 1
    assert fig.axes[0].get_title() == "Scatter plot"
    plt.close(fig)


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


# --- Tests for plot_heatmap ---


def test_plot_heatmap_draws_the_data():
    data = [[1, 2, 3], [4, 5, 6]]

    plot_heatmap(data)

    image = plt.gcf().axes[0].images[0]
    assert image.get_array().tolist() == data


def test_plot_heatmap_sets_title_and_axis_labels():
    plot_heatmap(
        [[1, 2], [3, 4]],
        title="Example Heatmap",
        x_label="Columns",
        y_label="Rows",
    )

    ax = plt.gcf().axes[0]
    assert ax.get_title() == "Example Heatmap"
    assert ax.get_xlabel() == "Columns"
    assert ax.get_ylabel() == "Rows"


def test_plot_heatmap_without_optional_labels_leaves_them_blank():
    plot_heatmap([[1, 2], [3, 4]])

    ax = plt.gcf().axes[0]
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


def test_plot_heatmap_adds_a_colorbar():
    plot_heatmap([[1, 2], [3, 4]])

    assert len(plt.gcf().axes) == 2


def test_plot_heatmap_accepts_integer_and_float_values():
    data = [[1, 2.5], [3, 4.5]]

    plot_heatmap(data)

    image = plt.gcf().axes[0].images[0]
    assert image.get_array().tolist() == data


def test_plot_heatmap_rejects_a_one_dimensional_list():
    with pytest.raises(ValueError, match="two-dimensional"):
        plot_heatmap([1, 2, 3])


def test_plot_heatmap_empty_data_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_heatmap([])


def test_plot_heatmap_empty_row_raises_value_error():
    with pytest.raises(ValueError, match="non-empty rows"):
        plot_heatmap([[1, 2], []])


def test_plot_heatmap_ragged_data_raises_value_error():
    with pytest.raises(ValueError, match="rectangular"):
        plot_heatmap([[1, 2], [3]])


def test_plot_heatmap_non_numeric_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_heatmap([[1, 2], [3, "four"]])


def test_plot_heatmap_boolean_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_heatmap([[1, 2], [3, True]])


def test_plot_heatmap_is_available_from_public_api():
    assert public_plot_heatmap is plot_heatmap


def test_plot_pie_chart_draws_one_slice_per_value():
    plot_pie_chart(["Walk", "Bus", "Bike"], [12, 7, 5])
    wedges = plt.gca().patches
    assert len(wedges) == 3


def test_plot_pie_chart_sets_title():
    plot_pie_chart(["A", "B"], [1, 3], title="Split")
    assert plt.gca().get_title() == "Split"


def test_plot_pie_chart_without_title_leaves_it_blank():
    plot_pie_chart(["A", "B"], [1, 1])
    assert plt.gca().get_title() == ""


def test_plot_pie_chart_empty_labels_raises():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_pie_chart([], [1])


def test_plot_pie_chart_empty_values_raises():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_pie_chart(["A"], [])


def test_plot_pie_chart_mismatched_lengths_raises():
    with pytest.raises(ValueError, match="same length"):
        plot_pie_chart(["A", "B"], [1])


def test_plot_pie_chart_rejects_non_numbers():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_pie_chart(["A", "B"], [1, "two"])


def test_plot_pie_chart_rejects_booleans():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_pie_chart(["A"], [True])


def test_plot_pie_chart_rejects_negative_values():
    with pytest.raises(ValueError, match="negative"):
        plot_pie_chart(["A", "B"], [1, -2])


def test_plot_pie_chart_is_available_from_public_api():
    assert public_plot_pie_chart is plot_pie_chart


def test_plot_bar_chart_draws_one_bar_per_value():
    plot_bar_chart(["Mon", "Tue", "Wed"], [3.5, 2.0, 4.5])
    ax = plt.gca()
    assert len(ax.patches) == 3


def test_plot_bar_chart_bar_heights_match_values():
    plot_bar_chart(["A", "B", "C"], [1, 5, 3])
    heights = [bar.get_height() for bar in plt.gca().patches]
    assert heights == [1, 5, 3]


def test_plot_bar_chart_sets_title_and_axis_labels():
    plot_bar_chart(
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


def test_plot_bar_chart_without_title_or_labels_leaves_them_blank():
    plot_bar_chart(["A", "B"], [1, 2])
    ax = plt.gca()
    assert ax.get_title() == ""
    assert ax.get_xlabel() == ""
    assert ax.get_ylabel() == ""


def test_plot_bar_chart_uses_labels_on_x_axis():
    plot_bar_chart(["Mon", "Tue", "Wed"], [1, 2, 3])
    fig = plt.gcf()
    fig.canvas.draw()
    tick_text = [t.get_text() for t in plt.gca().get_xticklabels()]
    assert tick_text == ["Mon", "Tue", "Wed"]


def test_plot_bar_chart_accepts_numeric_labels():
    plot_bar_chart([2024, 2025, 2026], [10, 20, 30])
    assert len(plt.gca().patches) == 3


def test_plot_bar_chart_empty_labels_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_bar_chart([], [1, 2])


def test_plot_bar_chart_empty_values_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_bar_chart(["A", "B"], [])


def test_plot_bar_chart_mismatched_lengths_raises_value_error():
    with pytest.raises(ValueError, match="same length"):
        plot_bar_chart(["A", "B", "C"], [1, 2])


def test_plot_bar_chart_non_numeric_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_bar_chart(["A", "B"], [1, "two"])


def test_plot_bar_chart_boolean_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_bar_chart(["A", "B"], [1, True])


def test_plot_bar_chart_is_available_from_public_api():
    assert public_plot_bar_chart is plot_bar_chart


def test_plot_scatter_chart_draws_points():
    plot_scatter_chart([1, 2, 3], [10, 20, 30])
    ax = plt.gca()
    assert len(ax.collections) == 1
    offsets = ax.collections[0].get_offsets()
    assert len(offsets) == 3


def test_plot_scatter_chart_sets_title_and_axis_labels():
    plot_scatter_chart(
        [1, 2],
        [10, 20],
        title="Hours vs Scores",
        x_label="Hours",
        y_label="Scores",
    )
    ax = plt.gca()
    assert ax.get_title() == "Hours vs Scores"
    assert ax.get_xlabel() == "Hours"
    assert ax.get_ylabel() == "Scores"


def test_plot_scatter_chart_without_title_or_labels_leaves_them_blank():
    plot_scatter_chart([1, 2], [3, 4])
    ax = plt.gca()
    assert ax.get_title() == ""
    assert ax.get_xlabel() == ""
    assert ax.get_ylabel() == ""


def test_plot_scatter_chart_accepts_floats_and_integers():
    plot_scatter_chart([1.5, 2, 3.75], [10.2, 20, 35.5])
    assert len(plt.gca().collections) == 1


def test_plot_scatter_chart_empty_x_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_scatter_chart([], [1, 2])


def test_plot_scatter_chart_empty_y_raises_value_error():
    with pytest.raises(ValueError, match="cannot be empty"):
        plot_scatter_chart([1, 2], [])


def test_plot_scatter_chart_mismatched_lengths_raises_value_error():
    with pytest.raises(ValueError, match="same length"):
        plot_scatter_chart([1, 2, 3], [10, 20])


def test_plot_scatter_chart_non_numeric_x_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_scatter_chart(["one", 2], [10, 20])


def test_plot_scatter_chart_non_numeric_y_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_scatter_chart([1, 2], [10, "twenty"])


def test_plot_scatter_chart_boolean_value_raises_value_error():
    with pytest.raises(ValueError, match="must be numbers"):
        plot_scatter_chart([1, True], [10, 20])


def test_plot_scatter_chart_is_available_from_public_api():
    assert public_plot_scatter_chart is plot_scatter_chart


# --- Tests for plot_histogram ---


def test_plot_histogram_creates_bars():
    plot_histogram([65, 72, 78, 80, 82, 85, 88, 90, 92], bins=3)

    ax = plt.gca()
    assert len(ax.patches) == 3


def test_plot_histogram_uses_labels_and_title():
    plot_histogram(
        [65, 72, 78, 80, 82],
        title="Test Scores",
        x_label="Score",
        y_label="Students",
    )

    ax = plt.gca()
    assert ax.get_title() == "Test Scores"
    assert ax.get_xlabel() == "Score"
    assert ax.get_ylabel() == "Students"


def test_plot_histogram_empty_series_raises_value_error():
    with pytest.raises(ValueError, match="The data series cannot be empty."):
        plot_histogram([])


def test_plot_histogram_bad_bins_raises_value_error():
    with pytest.raises(ValueError, match="bins must be a positive integer"):
        plot_histogram([1, 2, 3], bins=0)
    with pytest.raises(ValueError, match="bins must be a positive integer"):
        plot_histogram([1, 2, 3], bins="three")


def test_plot_histogram_is_available_from_public_api():
    assert public_plot_histogram is plot_histogram
