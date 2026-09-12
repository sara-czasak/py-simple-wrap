import pytest

from py_simple_package.src.py_simple.easy_stats import (
    correlation_coefficient,
    data_range,
    interquartile_range,
    median,
    mode,
    percentile,
    standard_deviation,
    variance,
    z_score,
)


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 2, 3], 2),
        ([4, 1, 9, 2], 3.0),
        ([1, 2], 1.5),
        ([1.5, 2.5, 3.5], 2.5),
        ([7], 7),
        ([-1, 0, 5], 0),
    ],
)
def test_median(nums, expected):
    assert median(nums) == expected


def test_median_rejects_empty_list():
    with pytest.raises(ValueError):
        median([])


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([2, 1, 2, 3], 2),
        ([1, 1, 1], 1),
        ([3, 1, 3, 1], 3),
        ([7], 7),
        ([1, 2, 3], 1),
    ],
)
def test_mode(nums, expected):
    assert mode(nums) == expected


def test_mode_rejects_empty_list():
    with pytest.raises(ValueError):
        mode([])


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([4, 1, 8, 2], 7),
        ([1, 2, 3], 2),
        ([-2, 2], 4),
        ([7], 0),
        ([1, 1, 1], 0),
    ],
)
def test_data_range(nums, expected):
    assert data_range(nums) == expected


def test_data_range_rejects_empty_list():
    with pytest.raises(ValueError):
        data_range([])


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 2, 3], 1.0),
        ([1, 1, 1], 0.0),
        ([1, 3, 5], 4.0),
        ([2, 4, 4, 4, 5, 5, 7, 9], 32 / 7),
    ],
)
def test_variance(nums, expected):
    assert variance(nums) == expected


@pytest.mark.parametrize("nums", [[], [1]])
def test_variance_rejects_less_than_two_numbers(nums):
    with pytest.raises(ValueError):
        variance(nums)


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 2, 3], 1.0),
        ([1, 1, 1], 0.0),
        ([1, 3, 5], 2.0),
        ([1, 5, 9], 4.0),
    ],
)
def test_standard_deviation(nums, expected):
    assert standard_deviation(nums) == expected


@pytest.mark.parametrize("nums", [[], [1]])
def test_standard_deviation_rejects_less_than_two_numbers(nums):
    with pytest.raises(ValueError):
        standard_deviation(nums)


@pytest.mark.parametrize(
    "nums, percent, expected",
    [
        ([1, 2, 3, 4], 0, 1),
        ([1, 2, 3, 4], 25, 1),
        ([1, 2, 3, 4], 37.5, 2),
        ([1, 2, 3, 4], 50, 2),
        ([1, 2, 3, 4], 75, 3),
        ([1, 2, 3, 4], 100, 4),
        ([5], 50, 5),
        ([3, 1, 6, 4, 9], 80, 6),
    ],
)
def test_percentile(nums, percent, expected):
    assert percentile(nums, percent) == expected


def test_percentile_rejects_empty_list():
    with pytest.raises(ValueError):
        percentile([], 50)


@pytest.mark.parametrize("percent", [-1, 100.5, 101])
def test_percentile_rejects_invalid_percent(percent):
    with pytest.raises(ValueError):
        percentile([1, 2, 3], percent)


@pytest.mark.parametrize(
    "nums, value, expected",
    [
        ([1, 2, 3, 4, 5], 5, 1.26),
        ([1, 2, 3, 4, 5], 3, 0.0),
        ([10, 12, 14], 10, -1.0),
    ],
)
def test_z_score(nums, value, expected):
    assert z_score(nums, value) == expected


@pytest.mark.parametrize("nums", [[], [1]])
def test_z_score_rejects_too_few_numbers(nums):
    with pytest.raises(ValueError):
        z_score(nums, 1)


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 2, 3, 4], 2),
        ([4, 1, 2, 3], 2),
        ([1, 2, 3, 4, 5, 6, 7, 8], 4),
        ([5, 5, 5, 5], 0),
        ([10], 0),
    ],
)
def test_interquartile_range(nums, expected):
    assert interquartile_range(nums) == expected


def test_interquartile_range_rejects_empty_list():
    with pytest.raises(ValueError):
        interquartile_range([])


@pytest.mark.parametrize(
    "x, y, expected",
    [
        ([1, 2, 3], [2, 4, 6], 1.0),
        ([1, 2, 3], [6, 4, 2], -1.0),
        ([-1, 0, 1], [1, 0, 1], 0.0),
        ([1, 2, 3, 4, 5], [60, 65, 75, 70, 80], 0.9),
        ([1, 2, 3], [1, 3, 2], 0.5),
        ([1, 2, 3], [3, 1, 2], -0.5),
        ([1.5, 2.5, 3.5], [-4, -2, 0], 1.0),
        ([2, 4], [7, 3], -1.0),
        ([1, 1, 2, 2], [2, 2, 4, 4], 1.0),
    ],
)
def test_correlation_coefficient(x, y, expected):
    result = correlation_coefficient(x, y)
    assert isinstance(result, float)
    assert result == pytest.approx(expected)


def test_correlation_coefficient_does_not_round():
    # Centered sums: xy = 3, xx = 2, yy = 14/3, so r = sqrt(27/28).
    assert correlation_coefficient([1, 2, 3], [1, 2, 4]) == pytest.approx(
        (27 / 28) ** 0.5
    )


@pytest.mark.parametrize("scale", [1e-200, 1e200])
def test_correlation_coefficient_handles_different_scales(scale):
    assert correlation_coefficient(
        [scale, 2 * scale, 3 * scale], [-3 * scale, -scale, -2 * scale]
    ) == pytest.approx(0.5)


def test_correlation_coefficient_preserves_pairs_and_input_lists():
    x, y = [3, 1, 2], [2, 1, 3]
    original_x, original_y = x.copy(), y.copy()
    assert correlation_coefficient(x, y) == pytest.approx(0.5)
    assert correlation_coefficient(y, x) == pytest.approx(0.5)
    assert x == original_x
    assert y == original_y


@pytest.mark.parametrize("x, y", [([], [1, 2]), ([1, 2], []), ([1, 2], [1, 2, 3])])
def test_correlation_coefficient_rejects_different_lengths(x, y):
    with pytest.raises(ValueError, match="same number of values"):
        correlation_coefficient(x, y)


@pytest.mark.parametrize("x, y", [([], []), ([1], [2])])
def test_correlation_coefficient_rejects_too_few_pairs(x, y):
    with pytest.raises(ValueError, match="at least two pairs"):
        correlation_coefficient(x, y)


@pytest.mark.parametrize(
    "x, y, name",
    [([1, 1], [1, 2], "x"), ([1, 2], [3, 3], "y"), ([0, 0], [0, 0], "x")],
)
def test_correlation_coefficient_rejects_constant_lists(x, y, name):
    with pytest.raises(ValueError, match=f"'{name}'.*two different values"):
        correlation_coefficient(x, y)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
@pytest.mark.parametrize("name", ["x", "y"])
def test_correlation_coefficient_rejects_nonfinite_values(value, name):
    inputs = {"x": [1, 2, 3], "y": [4, 5, 6]}
    inputs[name][1] = value
    with pytest.raises(ValueError, match=f"'{name}'.*NaN or infinite"):
        correlation_coefficient(**inputs)


@pytest.mark.parametrize("value", ["2", None, 2j])
@pytest.mark.parametrize("name", ["x", "y"])
def test_correlation_coefficient_rejects_nonnumeric_values(value, name):
    inputs = {"x": [1, 2, 3], "y": [4, 5, 6]}
    inputs[name][1] = value
    with pytest.raises(TypeError, match=f"'{name}'.*only numbers"):
        correlation_coefficient(**inputs)


def test_correlation_coefficient_is_exported_from_package():
    from py_simple_package.src.py_simple import correlation_coefficient as exported

    assert exported is correlation_coefficient
