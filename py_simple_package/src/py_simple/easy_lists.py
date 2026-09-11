"""Beginner-friendly helpers for common list operations."""


def unique_items(items: list) -> list:
    """
    Returns a new list with duplicates removed, keeping the original order.

    Args:
        items (list): List that may contain duplicates.

    Returns:
        list: List with duplicates removed, order preserved.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import unique_items

            result = unique_items([1, 2, 2, 3])  # -> [1, 2, 3]
            ```

        === "The Traditional Way"
            ```python
            items = [1, 2, 2, 3]
            result = []
            for item in items:
                if item not in result:
                    result.append(item)
            ```
    """
    return list(dict.fromkeys(items))


def find_duplicates(items: list) -> list:
    """
    Returns a list of items that appear more than once.

    Args:
        items (list): List to check for duplicates.

    Returns:
        list: Duplicated items, in the order they first appear.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import find_duplicates

            result = find_duplicates([1, 2, 2, 3, 3, 3])  # -> [2, 3]
            ```

        === "The Traditional Way"
            ```python
            items = [1, 2, 2, 3, 3, 3]
            result = list({item for item in items if items.count(item) > 1})
            ```
    """
    seen = set()
    duplicates = []
    for item in items:
        if item in seen:
            if item not in duplicates:
                duplicates.append(item)
        else:
            seen.add(item)
    return duplicates


def chunk_list(items: list, size: int) -> list:
    """
    Splits a list into smaller lists of the given size.

    Args:
        items (list): List to split.
        size (int): Maximum size of each chunk.

    Returns:
        list: List of chunks.

    Raises:
        ValueError: If size is less than 1.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import chunk_list

            result = chunk_list([1, 2, 3, 4, 5], 2)  # -> [[1, 2], [3, 4], [5]]
            ```

        === "The Traditional Way"
            ```python
            items, size = [1, 2, 3, 4, 5], 2
            result = [items[i:i + size] for i in range(0, len(items), size)]
            ```
    """
    if size < 1:
        raise ValueError("'size' must be at least 1.")

    return [items[i : i + size] for i in range(0, len(items), size)]


def flatten_list(items: list) -> list:
    """
    Flattens a list with nested lists into a single-level list.

    Args:
        items (list): List that may contain nested lists.

    Returns:
        list: Flattened list, one level deep.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import flatten_list

            result = flatten_list([[1, 2], [3]])  # -> [1, 2, 3]
            ```

        === "The Traditional Way"
            ```python
            items = [[1, 2], [3]]
            result = [item for sublist in items for item in sublist]
            ```
    """
    flattened = []
    for item in items:
        if isinstance(item, list):
            flattened.extend(item)
        else:
            flattened.append(item)
    return flattened


def most_common_item(items: list) -> object:
    """
    Returns the item that appears most often in a list.

    Args:
        items (list): List to examine.

    Returns:
        object: The most frequent item.

    Raises:
        ValueError: If the list is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import most_common_item

            result = most_common_item([1, 1, 2])  # -> 1
            ```

        === "The Traditional Way"
            ```python
            from collections import Counter

            items = [1, 1, 2]
            result = Counter(items).most_common(1)[0][0]
            ```
    """
    if not items:
        raise ValueError("Cannot find the most common item of an empty list.")

    return max(set(items), key=items.count)


def rotate_list(items: list, steps: int) -> list:
    """
    Rotates a list to the right by the given number of steps.

    Negative steps rotate to the left.

    Args:
        items (list): List to rotate.
        steps (int): Number of positions to rotate.

    Returns:
        list: Rotated list.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import rotate_list

            result = rotate_list([1, 2, 3], 1)  # -> [3, 1, 2]
            ```

        === "The Traditional Way"
            ```python
            items, steps = [1, 2, 3], 1
            steps = steps % len(items)
            result = items[-steps:] + items[:-steps]
            ```
    """
    if not items:
        return []

    steps = steps % len(items)
    return items[-steps:] + items[:-steps]


def merge_lists(list_a: list, list_b: list) -> list:
    """
    Combines two lists into one.

    Args:
        list_a (list): First list.
        list_b (list): Second list.

    Returns:
        list: Combined list, list_b items after list_a items.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import merge_lists

            result = merge_lists([1, 2], [3, 4])  # -> [1, 2, 3, 4]
            ```

        === "The Traditional Way"
            ```python
            list_a, list_b = [1, 2], [3, 4]
            result = list_a + list_b
            ```
    """
    return list_a + list_b


def alternate_lists(list_a: list, list_b: list) -> list:
    """
    Combines two lists by taking turns, one item at a time.

    Args:
        list_a (list): First list.
        list_b (list): Second list.

    Returns:
        list: Alternating list, remaining items appended at the end.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import alternate_lists

            result = alternate_lists([1, 2], [3, 4])  # -> [1, 3, 2, 4]
            ```

        === "The Traditional Way"
            ```python
            list_a, list_b = [1, 2], [3, 4]
            result = [item for pair in zip(list_a, list_b) for item in pair]
            ```
    """
    alternated = []
    for first, second in zip(list_a, list_b):
        alternated.append(first)
        alternated.append(second)
    alternated.extend(list_a[len(list_b) :])
    alternated.extend(list_b[len(list_a) :])
    return alternated


def sum_all(items: list) -> int:
    """
    Adds up every number in a list, including numbers inside nested lists.

    Args:
        items (list): List of numbers, possibly with nested lists.

    Returns:
        int: Total of all numbers.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sum_all

            result = sum_all([1, [2, 3], 4])  # -> 10
            ```

        === "The Traditional Way"
            ```python
            items = [1, [2, 3], 4]
            result = sum(item for sublist in items
                         for item in (sublist if isinstance(sublist, list)
                                      else [sublist]))
            ```
    """
    return sum(flatten_list(items))


def sort_numbers(items: list) -> list:
    """
    Returns a new list of numbers sorted from smallest to largest.

    Args:
        items (list): List of numbers.

    Returns:
        list: Sorted list of numbers.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sort_numbers

            result = sort_numbers([3, 1, 2])  # -> [1, 2, 3]
            ```

        === "The Traditional Way"
            ```python
            items = [3, 1, 2]
            result = sorted(items)
            ```
    """
    return sorted(items)


def sort_words(items: list) -> list:
    """
    Returns a new list of words sorted alphabetically, ignoring case.

    Args:
        items (list): List of words.

    Returns:
        list: Sorted list of words.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import sort_words

            result = sort_words(["banana", "Apple", "cherry"])
            # -> ["Apple", "banana", "cherry"]
            ```

        === "The Traditional Way"
            ```python
            items = ["banana", "Apple", "cherry"]
            result = sorted(items, key=str.lower)
            ```
    """
    return sorted(items, key=str.lower)
