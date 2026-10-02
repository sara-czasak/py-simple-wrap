import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from py_simple_package.src.py_simple import plot_heatmap as public_plot_heatmap
from py_simple_package.src.py_simple.easy_data_visualization import plot_heatmap


@pytest.fixture(autouse=True)
def close_plots(monkeypatch):
    """Prevent matplotlib from displaying windows during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")


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
