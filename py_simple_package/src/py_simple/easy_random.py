"""
easy_random is built to simplify common random choices, numbers, and shuffling.
"""

import random
from collections.abc import Sequence
from datetime import date, time
from typing import Any


def roll_dice(sides: int = 6) -> int:
    """
    Simulates rolling a die with a given number of sides (default is 6).

    Args:
        sides (int): Number of sides on the die. Defaults to 6.

    Returns:
        int: A random integer between 1 and sides inclusive.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import roll_dice

            result = roll_dice(6)  # -> e.g. 4
            ```

        === "The Traditional Way"
            ```python
            import random

            result = random.randint(1, 6)
            ```
    """
    if sides < 1:
        raise ValueError("Dice must have at least 1 side.")
    return random.randint(1, sides)


def flip_coin() -> str:
    """
    Simulates a coin toss, returning 'Heads' or 'Tails'.

    Returns:
        str: 'Heads' or 'Tails'.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import flip_coin

            result = flip_coin()  # -> 'Heads'
            ```

        === "The Traditional Way"
            ```python
            import random

            result = random.choice(["Heads", "Tails"])
            ```
    """
    return random.choice(["Heads", "Tails"])


def pick_random_item(items: Sequence[Any]) -> Any:
    """
    Picks a single random element from a list or tuple.

    Args:
        items (Sequence[Any]): The collection to pick from.

    Returns:
        Any: A randomly chosen element from the sequence.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import pick_random_item

            fruit = pick_random_item(["apple", "banana", "cherry"])  # -> 'banana'
            ```

        === "The Traditional Way"
            ```python
            import random

            fruit = random.choice(["apple", "banana", "cherry"])
            ```
    """
    if not items:
        raise ValueError("Cannot pick an item from an empty sequence.")
    return random.choice(items)


def pick_random_items(items: Sequence[Any], count: int) -> list[Any]:
    """
    Picks several unique positions from a list or tuple without changing it.

    Args:
        items (Sequence[Any]): The collection to pick from.
        count (int): Number of items to pick.

    Returns:
        List[Any]: A new list containing the selected items.

    Raises:
        ValueError: If count is not a whole number from zero through the
            number of available items.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import pick_random_items

            winners = pick_random_items(["Ada", "Lin", "Sam"], 2)
            # -> e.g. ['Lin', 'Ada']
            ```

        === "The Traditional Way"
            ```python
            import random

            winners = random.sample(["Ada", "Lin", "Sam"], k=2)
            ```
    """
    if not isinstance(count, int) or isinstance(count, bool):
        raise ValueError("count must be a whole number.")
    if count < 0 or count > len(items):
        raise ValueError(
            f"count must be between 0 and the number of items ({len(items)})."
        )
    return random.sample(items, k=count)


def shuffle_list(items: Sequence[Any]) -> list[Any]:
    """
    Returns a new list with the items shuffled in random order.

    Args:
        items (Sequence[Any]): The items to shuffle.

    Returns:
        List[Any]: A new shuffled copy of the list.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import shuffle_list

            shuffled = shuffle_list([1, 2, 3, 4, 5])  # -> e.g. [3, 1, 5, 2, 4]
            ```

        === "The Traditional Way"
            ```python
            import random

            my_list = [1, 2, 3, 4, 5]
            shuffled = list(my_list)
            random.shuffle(shuffled)
            ```
    """
    result = list(items)
    random.shuffle(result)
    return result


def generate_simple_password(length: int = 12, include_symbols: bool = True) -> str:
    """
    Generates a random password of the given length.

    Args:
        length (int): Length of the password. Defaults to 12.
        include_symbols (bool): Whether to include symbols. Defaults to True.

    Returns:
        str: A randomly generated password.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import generate_simple_password

            password = generate_simple_password(12)  # -> e.g. 'aB3$x9!qW2#z'
            ```

        === "The Traditional Way"
            ```python
            import random
            import string

            chars = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(chars) for _ in range(12))
            ```
    """
    import string

    if length < 1:
        raise ValueError("Password length must be at least 1.")
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def random_int(start: int, end: int) -> int:
    """
    Generates a random integer between start and end (inclusive).

    Args:
        start (int): The lower bound.
        end (int): The upper bound.

    Returns:
        int: A random integer within [start, end].

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import random_int

            num = random_int(10, 20)  # -> e.g. 17
            ```

        === "The Traditional Way"
            ```python
            import random

            num = random.randint(10, 20)
            ```
    """
    if start > end:
        raise ValueError("start cannot be greater than end.")
    return random.randint(start, end)


def random_bool() -> bool:
    """
    Returns a random boolean value (`True` or `False`) with equal probability.

    Returns:
        bool: Either `True` or `False`.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import random_bool

            if random_bool():
                print("Lucky!")
            ```

        === "The Traditional Way"
            ```python
            import random

            if random.choice([True, False]):
                print("Lucky!")
            ```
    """
    return random.choice([True, False])


def random_float(start: float = 0.0, end: float = 1.0, decimals: int | None = None) -> float:
    """
    Generates a random float between start and end.

    Args:
        start (float): The lower bound. Defaults to 0.0.
        end (float): The upper bound. Defaults to 1.0.
        decimals (int | None): Number of decimal places to round to. Defaults to None (no rounding).

    Returns:
        float: A random floating-point number within [start, end].

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import random_float

            num = random_float(1.5, 9.5, decimals=2)  # -> e.g. 4.82
            ```

        === "The Traditional Way"
            ```python
            import random

            num = round(random.uniform(1.5, 9.5), 2)
            ```
    """
    if start > end:
        raise ValueError("start cannot be greater than end.")
    if decimals is not None and decimals < 0:
        raise ValueError("decimals cannot be negative.")
    val = random.uniform(start, end)
    return round(val, decimals) if decimals is not None else val


def random_color() -> str:
    """
    Generates a random hex color string (e.g. "#3FA7B2").

    Returns:
        str: A random hex color in the format "#RRGGBB".

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import random_color

            color = random_color()  # -> e.g. "#3FA7B2"
            ```

        === "The Traditional Way"
            ```python
            import random

            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            ```
    """

    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def random_date(start: date, end: date) -> date:
    """
    Generates a random date between start and end (inclusive).

    Args:
        start (date): The lower bound.
        end (date): The upper bound.

    Returns:
        date: A random date within [start, end], e.g.
            `date(2026, 7, 14)`.

    Example:
        === "The Py_simple Way"
            ```python
            from datetime import date
            from py_simple import random_date

            day = random_date(date(2026, 1, 1), date(2026, 12, 31))
            ```

        === "The Traditional Way"
            ```python
            import random
            from datetime import date

            ordinal = random.randint(date(2026, 1, 1).toordinal(),
                                     date(2026, 12, 31).toordinal())
            day = date.fromordinal(ordinal)
            ```
    """
    if start > end:
        raise ValueError("start cannot be greater than end.")
    ordinal = random.randint(start.toordinal(), end.toordinal())
    return date.fromordinal(ordinal)


def random_choice_weighted(
    items: Sequence[Any], weights: Sequence[float]
) -> Any:
    """
    Picks one random item using the given weights.

    Args:
        items (Sequence[Any]): The collection to choose from.
        weights (Sequence[float]): The relative probability of each item.

    Returns:
        Any: A randomly chosen element from the sequence.

    Raises:
        ValueError: If items and weights have different lengths or
            if the sequence is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import random_choice_weighted

            fruit = random_choice_weighted(
                ["apple", "banana", "cherry"],
                [0.7, 0.2, 0.1],
            )
            ```

        === "The Traditional Way"
            ```python
            import random

            fruit = random.choices(
                ["apple", "banana", "cherry"],
                weights=[0.7, 0.2, 0.1],
                k=1,
            )[0]
            ```
    """
    if not items:
        raise ValueError("Cannot choose from an empty sequence.")
    if len(items) != len(weights):
        raise ValueError("items and weights must have the same length.")

    return random.choices(items, weights=weights, k=1)[0]
