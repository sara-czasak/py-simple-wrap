# easy_json Tutorial

## Updating a JSON configuration

Suppose your application stores its settings in a JSON configuration file. You can use `easy_json` to load the configuration, update a value, and display the result.

```python
from easy_json import open_json, update_json, pretty_json

config = open_json("config.json")

update_json(config, "debug", True)

print(pretty_json(config))