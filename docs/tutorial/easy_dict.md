# Easy Dict

Working with dictionaries is something you'll do in almost every Python project. Whether you're combining data, searching for values, sorting keys, or accessing nested information, `easy_dict` provides beginner-friendly helpers that make common dictionary operations simple and easy to read.

## A small real-world example

Imagine you're working with user information stored in several dictionaries. You want to combine the data, rename a key, and access information stored inside a nested dictionary.

```python
from py_simple import merge_dicts, rename_key, get_nested_value

user = {"name": "Ana", "age": 25}
extra_data = {"country": "Spain"}

user = merge_dicts(user, extra_data)
user = rename_key(user, "name", "username")

print(user)
```

Example output:

```text
{'age': 25, 'country': 'Spain', 'username': 'Ana'}
```

You can also retrieve values from nested dictionaries without manually checking every level:

```python
from py_simple import get_nested_value

data = {"user": {"profile": {"name": "Ana"}}}

name = get_nested_value(data, "user.profile.name")

print(name)
```

Example output:

```text
Ana
```

## What happened?

`merge_dicts()` combines two dictionaries into one. If both dictionaries contain the same key, the value from the second dictionary is kept.

`rename_key()` creates a copy of a dictionary with one key renamed without modifying the original dictionary.

`get_nested_value()` retrieves a value from a nested dictionary using a simple dot-separated path such as `"user.profile.name"`.

The module also provides helpers for other common dictionary operations, such as converting two lists into a dictionary, inverting keys and values, sorting by keys or values, finding keys with a specific value, counting values, and finding the most common value.

For example:

```python
from py_simple import sort_dict_by_value, find_keys, most_common_value

data = {"a": 2, "b": 1, "c": 2}

print(sort_dict_by_value(data))
print(find_keys(2, data))
print(most_common_value(data))
```

Example output:

```text
{'b': 1, 'a': 2, 'c': 2}
['a', 'c']
2
```

## Why use these helpers?

Instead of repeatedly writing dictionary comprehensions, loops, `.update()`, `.pop()`, and nested dictionary checks, you can simply write:

```python
user = merge_dicts(user, extra_data)
user = rename_key(user, "name", "username")

name = get_nested_value(data, "user.profile.name")
```

These helpers keep dictionary operations simple, readable, and beginner-friendly while providing useful tools for manipulating, searching, sorting, and analyzing dictionaries.