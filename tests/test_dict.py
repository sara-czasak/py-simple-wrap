import pytest

from py_simple_package.src.py_simple.easy_dict import (
    count_values,
    find_keys,
    get_nested_value,
    invert_dict,
    lists_to_dict,
    merge_dicts,
    most_common_value,
    rename_key,
    sort_dict_by_key,
    sort_dict_by_value,
)


@pytest.mark.parametrize(
    "dict_a, dict_b, expected",
    [
        ({"a": 1}, {"b": 2}, {"a": 1, "b": 2}),
        ({"a": 1}, {"a": 2}, {"a": 2}),
        ({}, {"a": 1}, {"a": 1}),
        ({}, {}, {}),
        ({"a": 1, "b": 2}, {"b": 3, "c": 4}, {"a": 1, "b": 3, "c": 4}),
    ],
)
def test_merge_dicts(dict_a, dict_b, expected):
    assert merge_dicts(dict_a, dict_b) == expected


@pytest.mark.parametrize(
    "dict_a, dict_b, expected",
    [
        ({"a": [1, 2]}, {"b": [3, 4]}, {"a": [1, 2], "b": [3, 4]}),
        ({"a": []}, {"a": [1, 2]}, {"a": [1, 2]}),
        (
            {"a": [3, 4], "b": [6]},
            {"b": [3], "c": [8, 9]},
            {"a": [3, 4], "b": [3], "c": [8, 9]},
        ),
    ],
)
def test_merge_dicts_deepcopy(dict_a, dict_b, expected):
    result = merge_dicts(dict_a, dict_b)

    for lst in result.values():
        lst.append(1)

    assert merge_dicts(dict_a, dict_b) != result


@pytest.mark.parametrize(
    "keys, values, expected",
    [
        (["a", "b"], [1, 2], {"a": 1, "b": 2}),
        (["name", "age"], ["Ana", 25], {"name": "Ana", "age": 25}),
        ([], [], {}),
    ],
)
def test_lists_to_dict(keys, values, expected):
    assert lists_to_dict(keys, values) == expected


def test_lists_to_dict_rejects_length_mismatch():
    with pytest.raises(ValueError):
        lists_to_dict(["a", "b"], [1])


@pytest.mark.parametrize(
    "dictionary, expected",
    [
        ({"a": 1, "b": 2}, {1: "a", 2: "b"}),
        ({}, {}),
        ({1: "x"}, {"x": 1}),
    ],
)
def test_invert_dict(dictionary, expected):
    assert invert_dict(dictionary) == expected


def test_invert_dict_rejects_duplicate_values():
    with pytest.raises(ValueError):
        invert_dict({"a": 1, "b": 1})


@pytest.mark.parametrize(
    "dictionary, path, default, expected",
    [
        ({"user": {"name": "Ana"}}, "user.name", None, "Ana"),
        ({"a": {"b": {"c": 1}}}, "a.b.c", None, 1),
        ({"a": 1}, "a", None, 1),
        ({"a": {"b": 1}}, "a.c", "missing", "missing"),
        ({"a": 1}, "a.b.c", None, None),
        ({}, "a.b", 0, 0),
        ({"a": 1}, "", None, None),
        ({"a": 1}, "a..b", None, None),
    ],
)
def test_get_nested_value(dictionary, path, default, expected):
    assert get_nested_value(dictionary, path, default) == expected


@pytest.mark.parametrize(
    "dictionary, reverse, expected",
    [
        ({"b": 2, "a": 1}, False, {"a": 1, "b": 2}),
        ({"b": 2, "a": 1}, True, {"b": 2, "a": 1}),
        ({}, False, {}),
        ({"a": 1}, False, {"a": 1}),
    ],
)
def test_sort_dict_by_key(dictionary, reverse, expected):
    assert sort_dict_by_key(dictionary, reverse=reverse) == expected


@pytest.mark.parametrize(
    "dictionary, reverse, expected",
    [
        ({"a": 2, "b": 1}, False, {"b": 1, "a": 2}),
        ({"a": 2, "b": 1}, True, {"a": 2, "b": 1}),
        ({}, False, {}),
        ({"a": 1}, False, {"a": 1}),
    ],
)
def test_sort_dict_by_value(dictionary, reverse, expected):
    assert sort_dict_by_value(dictionary, reverse=reverse) == expected


@pytest.mark.parametrize(
    "dictionary, old_key, new_key, expected",
    [
        ({"name": "Ana"}, "name", "username", {"username": "Ana"}),
        ({"a": 1, "b": 2}, "a", "c", {"c": 1, "b": 2}),
        ({"a": 1}, "a", "b", {"b": 1}),
    ],
)
def test_rename_key(dictionary, old_key, new_key, expected):
    assert rename_key(dictionary, old_key, new_key) == expected


def test_rename_key_rejects_missing_old_key():
    with pytest.raises(KeyError):
        rename_key({"a": 1}, "b", "c")


def test_rename_key_rejects_existing_new_key():
    with pytest.raises(ValueError):
        rename_key({"a": 1, "b": 2}, "a", "b")


@pytest.mark.parametrize(
    "needle, dictionary, expected",
    [
        (1, {"a": 1, "b": 2, "c": 1}, ["a", "c"]),
        (1, {"a": 1, "b": 2}, ["a"]),
        (3, {"a": 1, "b": 2}, []),
        (None, {}, []),
    ],
)
def test_find_keys(needle, dictionary, expected):
    assert find_keys(needle, dictionary) == expected


@pytest.mark.parametrize(
    "dictionary, expected",
    [
        ({"a": 1, "b": 2, "c": 1}, {1: 2, 2: 1}),
        ({"a": "x", "b": "x"}, {"x": 2}),
        ({}, {}),
        ({"a": 1}, {1: 1}),
    ],
)
def test_count_values(dictionary, expected):
    assert count_values(dictionary) == expected


@pytest.mark.parametrize(
    "dictionary, expected",
    [
        ({"a": 1, "b": 2, "c": 1}, 1),
        ({"a": "x", "b": "x"}, "x"),
        ({"a": 7}, 7),
    ],
)
def test_most_common_value(dictionary, expected):
    assert most_common_value(dictionary) == expected


def test_most_common_value_rejects_empty_dictionary():
    with pytest.raises(ValueError):
        most_common_value({})
