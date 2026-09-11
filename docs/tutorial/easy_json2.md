# Easy JSON

Working with JSON files is something you'll often need in Python projects. Reading, writing, updating, formatting, and inspecting JSON data can require repetitive file-handling and parsing code.

The `easy_json` module provides simple helpers that make these common JSON operations easier to use without writing the underlying logic yourself.

## A small real-world example

Imagine you're creating an application that stores its configuration in a JSON file. You need to create the configuration, update it later, and read its values.

```python
from py_simple import save_json_data, open_json, update_json

save_json_data("config.json", {"name": "Sara", "theme": "dark"})

update_json("config.json", {"theme": "light"})

config = open_json("config.json")

print(config["name"])
print(config["theme"])
```

Example output:

```text
Sara
light
```

## What happened?

`save_json_data()` creates a new JSON file from a dictionary. It refuses to overwrite an existing file, helping prevent accidental data loss.

`open_json()` opens a JSON file and returns its contents as a dictionary.

`update_json()` merges new data into an existing JSON file. Existing keys with the same name are replaced while other data remains untouched.

You can also format JSON, check whether a file is a JSON file, and inspect nested data:

```python
from py_simple import pretty_json, is_json_file, is_nested_json

print(pretty_json(data={"name": "Sara", "settings": {"theme": "dark"}}))

print(is_json_file("config.json"))

print(is_nested_json(data={"name": "Sara", "settings": {"theme": "dark"}}))
```

## The Py_simple Way

```python
from py_simple import save_json_data, open_json, update_json, pretty_json

save_json_data("config.json", {"name": "Sara"})

update_json("config.json", {"age": 25})

data = open_json("config.json")

print(pretty_json(data=data))
```

## The Traditional Way

Without `py_simple`, you would normally have to handle JSON files directly with Python's `json` module:

```python
import json
import os

filepath = "config.json"

if not os.path.exists(filepath):
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump({"name": "Sara"}, json_file, indent=4)

with open(filepath, encoding="utf-8") as json_file:
    data = json.load(json_file)

data.update({"age": 25})

with open(filepath, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4)

print(json.dumps(data, indent=2))
```

## Formatting JSON

`pretty_json()` returns an indented JSON string from either a dictionary or a JSON file.

```python
from py_simple import pretty_json

print(pretty_json(data={"name": "Sara", "settings": {"theme": "dark"}}))
```

Example output:

```text
{
  "name": "Sara",
  "settings": {
    "theme": "dark"
  }
}
```

You can also provide a file instead:

```python
from py_simple import pretty_json

print(pretty_json(filepath="config.json"))
```

Provide exactly one of `data` or `filepath`.

## Working with nested JSON

`is_nested_json()` checks whether a dictionary or JSON file contains nested dictionaries or lists at the top level.

```python
from py_simple import is_nested_json

print(is_nested_json(data={"name": "Sara", "age": 25}))
# False

print(is_nested_json(data={"name": "Sara", "settings": {"theme": "dark"}}))
# True
```

`flatten_json()` can then convert nested JSON into a single-level dictionary:

```python
from py_simple import flatten_json

data = {"user": {"name": "Sara", "age": 25}}

print(flatten_json(data=data))
```

Example output:

```text
{
    'user-name': 'Sara',
    'user-age': 25
}
```

You can choose a different separator:

```python
flatten_json(".", data=data)
```

This produces keys such as:

```text
user.name
user.age
```

## Checking JSON files

`is_json_file()` checks whether a path points to an existing file with a `.json` extension.

```python
from py_simple import is_json_file

if is_json_file("config.json"):
    print("Looks good!")
```

## Error handling

The `easy_json` module provides `EasyJsonError` so JSON-related failures can be handled with one consistent exception.

For example, attempting to open a file that doesn't exist can be handled like this:

```python
from py_simple import open_json, EasyJsonError

try:
    data = open_json("missing.json")
except EasyJsonError as error:
    print(error)
```

The same exception is used for problems such as invalid JSON syntax, file permissions, attempting to overwrite an existing file, or invalid arguments.

## Why use these helpers?

Instead of repeatedly writing JSON file-handling and parsing logic, you can simply use:

```python
data = open_json("config.json")

save_json_data("new.json", {"name": "Sara"})

update_json("config.json", {"age": 25})

pretty = pretty_json(data=data)

nested = is_nested_json(data=data)

flat = flatten_json(data=data)
```

These helpers keep common JSON operations simple, readable, and beginner-friendly while handling the underlying file operations, parsing, formatting, and nested-data processing for you.
