import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from py_simple_package.src.py_simple import plot_pie_chart as public_plot_pie_chart
from py_simple_package.src.py_simple.easy_data_visualization import plot_pie_chart


@pytest.fixture(autouse=True)
def mock_plt_show(monkeypatch):
    """Prevent matplotlib from popping up windows during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")


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


def test_public_import():
    assert public_plot_pie_chart is plot_pie_chart
