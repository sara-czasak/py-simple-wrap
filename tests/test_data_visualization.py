import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from py_simple_package.src.py_simple.easy_data_visualization import (
    _infer_type,
    plot_data,
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
