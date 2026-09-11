import pytest

from py_simple_package.src.py_simple.easy_stats import (
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
