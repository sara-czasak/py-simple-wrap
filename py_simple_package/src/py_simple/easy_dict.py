"""Beginner-friendly helpers for common dictionary operations."""


def merge_dicts(dict_a: dict, dict_b: dict) -> dict:
    """
    Combines two dictionaries into one.

    If both dictionaries have the same key, the value from dict_b is kept.

    Args:
        dict_a (dict): First dictionary.
        dict_b (dict): Second dictionary.

    Returns:
        dict: Combined dictionary.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import merge_dicts

            result = merge_dicts({"a": 1}, {"b": 2})  # -> {"a": 1, "b": 2}
            ```

        === "The Traditional Way"
            ```python
            import copy

            dict_a, dict_b = {"a": 1}, {"b": 2}
            result = dict(copy.deepcopy(dict_a))
            result.update(copy.deepcopy(dict_b))
            ```
    """
    import copy

    result = dict(copy.deepcopy(dict_a))
    result.update(copy.deepcopy(dict_b))
    return result


def lists_to_dict(keys: list, values: list) -> dict:
    """
    Combines two lists into a dictionary, pairing them by position.

    Args:
        keys (list): List of keys.
        values (list): List of values.

    Returns:
        dict: Dictionary with keys matched to values.

    Raises:
        ValueError: If keys and values have different lengths.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import lists_to_dict

            result = lists_to_dict(["name", "age"], ["Ana", 25])
            # -> {"name": "Ana", "age": 25}
            ```

        === "The Traditional Way"
            ```python
            keys, values = ["name", "age"], ["Ana", 25]
            result = dict(zip(keys, values))
            ```
    """
    if len(keys) != len(values):
        raise ValueError("'keys' and 'values' must have the same length.")

    return {key: value for key, value in zip(keys, values)}


def invert_dict(dictionary: dict) -> dict:
    """
    Returns a new dictionary with keys and values swapped.

    Args:
        dictionary (dict): Dictionary to invert.

    Returns:
        dict: Inverted dictionary.

    Raises:
        ValueError: If a value appears more than once and can't be a key.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import invert_dict

            result = invert_dict({"a": 1, "b": 2})  # -> {1: "a", 2: "b"}
            ```

        === "The Traditional Way"
            ```python
            dictionary = {"a": 1, "b": 2}
            result = {value: key for key, value in dictionary.items()}
            ```
    """
    inverted = {}
    for key, value in dictionary.items():
        if value in inverted:
            raise ValueError(f"Cannot invert: value {value!r} appears more than once.")
        inverted[value] = key
    return inverted


def get_nested_value(dictionary: dict, path: str, default: object = None) -> object:
    """
    Returns a value from a nested dictionary using a dot-separated path.

    Args:
        dictionary (dict): Dictionary to search in.
        path (str): Dot-separated keys, e.g. "user.name".
        default (object): Value to return if the path is missing.

    Returns:
        object: The value found, or default.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_nested_value

            data = {"user": {"name": "Ana"}}
            result = get_nested_value(data, "user.name")  # -> "Ana"
            ```

        === "The Traditional Way"
            ```python
            data = {"user": {"name": "Ana"}}
            result = data.get("user", {}).get("name", None)
            ```
    """
    current = dictionary
    for part in path.split("."):
        if not part or not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def sort_dict_by_key(dictionary: dict, reverse: bool = False) -> dict:
    """
    Returns a new dictionary with keys sorted alphabetically.

    Args:
        dictionary (dict): Dictionary to sort.
        reverse (bool): Sort in descending order if True.

    Returns:
        dict: Dictionary sorted by key.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sort_dict_by_key

            result = sort_dict_by_key({"b": 2, "a": 1})  # -> {"a": 1, "b": 2}
            ```

        === "The Traditional Way"
            ```python
            dictionary = {"b": 2, "a": 1}
            result = {key: dictionary[key] for key in sorted(dictionary)}
            ```
    """
    return dict(sorted(dictionary.items(), reverse=reverse))


def sort_dict_by_value(dictionary: dict, reverse: bool = False) -> dict:
    """
    Returns a new dictionary with values sorted from smallest to largest.

    Args:
        dictionary (dict): Dictionary to sort.
        reverse (bool): Sort in descending order if True.

    Returns:
        dict: Dictionary sorted by value.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sort_dict_by_value

            result = sort_dict_by_value({"a": 2, "b": 1})  # -> {"b": 1, "a": 2}
            ```

        === "The Traditional Way"
            ```python
            dictionary = {"a": 2, "b": 1}
            result = dict(sorted(dictionary.items(), key=lambda item: item[1]))
            ```
    """
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=reverse))


def rename_key(dictionary: dict, old_key: str, new_key: str) -> dict:
    """
    Returns a copy of the dictionary with one key renamed.

    Args:
        dictionary (dict): Dictionary to copy.
        old_key (str): Key to rename.
        new_key (str): New name for the key.

    Returns:
        dict: Copy with the key renamed.

    Raises:
        KeyError: If old_key is not in the dictionary.
        ValueError: If new_key already exists in the dictionary.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import rename_key

            result = rename_key({"name": "Ana"}, "name", "username")
            # -> {"username": "Ana"}
            ```

        === "The Traditional Way"
            ```python
            dictionary = {"name": "Ana"}
            result = dictionary.copy()
            result["username"] = result.pop("name")
            ```
    """
    if old_key not in dictionary:
        raise KeyError(f"'{old_key}' does not exist in the dictionary.")
    if new_key in dictionary:
        raise ValueError(f"Cannot rename: '{new_key}' already exists.")

    renamed = dict(dictionary)
    renamed[new_key] = renamed.pop(old_key)
    return renamed


def find_keys(needle: object, dictionary: dict) -> list:
    """
    Returns every key whose value matches the given needle.

    Args:
        needle (object): Value to look for.
        dictionary (dict): Dictionary to search in.

    Returns:
        list: Keys with a matching value.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import find_keys

            result = find_keys(1, {"a": 1, "b": 2, "c": 1})  # -> ["a", "c"]
            ```

        === "The Traditional Way"
            ```python
            needle, dictionary = 1, {"a": 1, "b": 2, "c": 1}
            result = [key for key, value in dictionary.items() if value == needle]
            ```
    """
    return [key for key, value in dictionary.items() if value == needle]


def count_values(dictionary: dict) -> dict:
    """
    Counts how many times each value appears in the dictionary.

    Args:
        dictionary (dict): Dictionary to examine.

    Returns:
        dict: Values mapped to how often they appear.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_values

            result = count_values({"a": 1, "b": 2, "c": 1})
            # -> {1: 2, 2: 1}
            ```

        === "The Traditional Way"
            ```python
            dictionary = {"a": 1, "b": 2, "c": 1}
            result = {}
            for value in dictionary.values():
                result[value] = result.get(value, 0) + 1
            ```
    """
    counts = {}
    for value in dictionary.values():
        counts[value] = counts.get(value, 0) + 1
    return counts


def most_common_value(dictionary: dict) -> object:
    """
    Returns the value that appears most often in the dictionary.

    Args:
        dictionary (dict): Dictionary to examine.

    Returns:
        object: The most frequent value.

    Raises:
        ValueError: If the dictionary is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import most_common_value

            result = most_common_value({"a": 1, "b": 2, "c": 1})  # -> 1
            ```

        === "The Traditional Way"
            ```python
            dictionary = {"a": 1, "b": 2, "c": 1}
            values = []
            freq = []

            for item in dictionary.values():
                if item not in values:
                    values.append(item)
                    freq.append(1)
                else:
                    indx = values.index(item)
                    freq[indx] += 1
            result = values[max(enumerate(freq), key=lambda x: x[1])[0]]
            ```
    """
    # cannot use count_values for unhashable types (such as list)

    if not dictionary:
        raise ValueError("Cannot find the most common value of an empty dictionary.")

    values = []
    freq = []

    for item in dictionary.values():
        if item not in values:
            values.append(item)
            freq.append(1)
        else:
            indx = values.index(item)
            freq[indx] += 1

    return values[max(enumerate(freq), key=lambda x: x[1])[0]]
