import pytest

from py_simple_package.src.py_simple.easy_lists import (
    alternate_lists,
    chunk_list,
    find_duplicates,
    flatten_list,
    merge_lists,
    most_common_item,
    rotate_list,
    sort_numbers,
    sort_words,
    sum_all,
    unique_items,
)


@pytest.mark.parametrize(
    "items, expected",
    [
        ([1, 2, 2, 3], [1, 2, 3]),
        (["a", "b", "a", "c"], ["a", "b", "c"]),
        ([1, 1, 1], [1]),
        ([], []),
    ],
)
def test_unique_items(items, expected):
    assert unique_items(items) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([1, 2, 2, 3, 3, 3], [2, 3]),
        ([1, 2, 3], []),
        (["a", "b", "a"], ["a"]),
        ([], []),
    ],
)
def test_find_duplicates(items, expected):
    assert find_duplicates(items) == expected


@pytest.mark.parametrize(
    "items, size, expected",
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3], 5, [[1, 2, 3]]),
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([], 3, []),
    ],
)
def test_chunk_list(items, size, expected):
    assert chunk_list(items, size) == expected


@pytest.mark.parametrize("size", [0, -1, -5])
def test_chunk_list_rejects_invalid_size(size):
    with pytest.raises(ValueError):
        chunk_list([1, 2, 3], size)


@pytest.mark.parametrize(
    "items, expected",
    [
        ([[1, 2], [3]], [1, 2, 3]),
        ([1, [2, 3], 4], [1, 2, 3, 4]),
        ([[], [1]], [1]),
        ([], []),
    ],
)
def test_flatten_list(items, expected):
    assert flatten_list(items) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([1, 1, 2], 1),
        (["a", "b", "b"], "b"),
        ([7], 7),
    ],
)
def test_most_common_item(items, expected):
    assert most_common_item(items) == expected


def test_most_common_item_rejects_empty_list():
    with pytest.raises(ValueError):
        most_common_item([])


@pytest.mark.parametrize(
    "items, steps, expected",
    [
        ([1, 2, 3], 1, [3, 1, 2]),
        ([1, 2, 3], -1, [2, 3, 1]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([1, 2, 3, 4], 2, [3, 4, 1, 2]),
        ([1, 2, 3], 4, [3, 1, 2]),
        ([], 1, []),
    ],
)
def test_rotate_list(items, steps, expected):
    assert rotate_list(items, steps) == expected


@pytest.mark.parametrize(
    "list_a, list_b, expected",
    [
        ([1, 2], [3, 4], [1, 2, 3, 4]),
        (["a"], ["b", "c"], ["a", "b", "c"]),
        ([], [1], [1]),
        ([], [], []),
    ],
)
def test_merge_lists(list_a, list_b, expected):
    assert merge_lists(list_a, list_b) == expected


@pytest.mark.parametrize(
    "list_a, list_b, expected",
    [
        ([1, 2], [3, 4], [1, 3, 2, 4]),
        ([1, 2, 3], [4], [1, 4, 2, 3]),
        (["a"], ["x", "y"], ["a", "x", "y"]),
        ([], [1, 2], [1, 2]),
        ([], [], []),
    ],
)
def test_alternate_lists(list_a, list_b, expected):
    assert alternate_lists(list_a, list_b) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([1, 2, 3], 6),
        ([1, [2, 3], 4], 10),
        ([1.5, 2.5], 4.0),
        ([], 0),
    ],
)
def test_sum_all(items, expected):
    assert sum_all(items) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([3, 1, 2], [1, 2, 3]),
        ([3.5, 1.2], [1.2, 3.5]),
        ([-1, 5, -3], [-3, -1, 5]),
        ([], []),
    ],
)
def test_sort_numbers(items, expected):
    assert sort_numbers(items) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        (["banana", "Apple", "cherry"], ["Apple", "banana", "cherry"]),
        (["Zebra", "apple", "mango"], ["apple", "mango", "Zebra"]),
        (["a", "a"], ["a", "a"]),
        ([], []),
    ],
)
def test_sort_words(items, expected):
    assert sort_words(items) == expected


@pytest.mark.parametrize(
    "items,expected",
    [
        ([1, 2, 2, 1], [1, 2]),
        (["first", "second", "third", "third", "second", "first"], ["first", "second", "third"]),
        ([0, 1, 2, 2, 1, 1, 3], [1, 2]),
    ],
)
def test_find_duplicates_keeps_first_occurrence_order(items, expected):
    original = items.copy()
    assert find_duplicates(items) == expected
    assert items == original
