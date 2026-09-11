import pytest

from py_simple_package.src.py_simple import (
    pick_random_items as public_pick_random_items,
)
from py_simple_package.src.py_simple.easy_random import (
    flip_coin,
    pick_random_item,
    pick_random_items,
    random_int,
    roll_dice,
    shuffle_list,
)


def test_roll_dice():
    for _ in range(50):
        res = roll_dice(6)
        assert 1 <= res <= 6

    with pytest.raises(ValueError):
        roll_dice(0)


def test_flip_coin():
    outcomes = {flip_coin() for _ in range(50)}
    assert outcomes.issubset({"Heads", "Tails"})


def test_pick_random_item():
    items = ["apple", "banana", "cherry"]
    for _ in range(20):
        assert pick_random_item(items) in items

    with pytest.raises(ValueError):
        pick_random_item([])


def test_pick_random_items(monkeypatch):
    items = ["Ada", "Lin", "Sam"]
    received = {}

    def fake_sample(population, k):
        received.update(population=population, count=k)
        return list(population)[:k]

    monkeypatch.setattr("py_simple.easy_random.random.sample", fake_sample)

    assert pick_random_items(items, 2) == ["Ada", "Lin"]
    assert received == {"population": items, "count": 2}
    assert items == ["Ada", "Lin", "Sam"]
    assert pick_random_items(items, 0) == []


@pytest.mark.parametrize("count", [-1, 4, 1.5, True])
def test_pick_random_items_rejects_invalid_count(count):
    with pytest.raises(ValueError, match="count must be"):
        pick_random_items(["Ada", "Lin", "Sam"], count)


def test_pick_random_items_is_available_from_public_api():
    assert public_pick_random_items is pick_random_items


def test_shuffle_list():
    original = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    shuffled = shuffle_list(original)
    assert len(shuffled) == len(original)
    assert set(shuffled) == set(original)
    assert original == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    assert shuffle_list([]) == []


def test_random_int():
    for _ in range(50):
        val = random_int(5, 15)
        assert 5 <= val <= 15

    with pytest.raises(ValueError):
        random_int(10, 5)
