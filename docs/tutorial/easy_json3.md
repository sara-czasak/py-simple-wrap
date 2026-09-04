# Get Nested Values

`get_nested` lets you access values inside nested dictionaries and lists using a dot-separated path.

## Example

```python
from py_simple.easy_json import get_nested

data = {
    "users": [
        {"name": "Alice", "role": "admin"},
        {"name": "Bob", "role": "user"}
    ]
}

alice = get_nested(data, "users.0.name")
role = get_nested(data, "users.1.role")
missing = get_nested(data, "users.2.name", "n/a")

print(alice)    # Alice
print(role)     # user
print(missing)  # n/a
