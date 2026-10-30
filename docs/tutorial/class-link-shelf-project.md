# Build a Class Link Shelf with Easy URL and Easy CSV

Combine **Easy URL** and **Easy CSV** to keep a clean list of class
links. Tracking parameters are removed before the links are saved, so
the file stays readable.

## A small real-world example

A classmate drops two resource links in chat. Each one has a
`utm_source` tag from the messaging app. This example writes a temporary
CSV shelf, so you can run it repeatedly without touching a real file.
The folder is removed when the example ends.

Install the package with `python -m pip install py-simple-wrap`, then run:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from py_simple import get_domain, read_csv_to_list, remove_query_param, write_csv_from_list

raw_links = [
    "https://school.example/science?utm_source=chat&week=3",
    "https://library.example/math?utm_source=chat&week=3",
]

with TemporaryDirectory() as workspace:
    cleaned = []
    for link in raw_links:
        without_tracker = remove_query_param(link, "utm_source")
        cleaned.append(
            {
                "site": get_domain(without_tracker),
                "link": without_tracker,
            }
        )

    shelf = str(Path(workspace) / "class_links.csv")
    write_csv_from_list(shelf, cleaned)

    for row in read_csv_to_list(shelf):
        print(row["site"], row["link"])
```

Example output:

```text
school.example https://school.example/science?week=3
library.example https://library.example/math?week=3
```

## What happened?

`remove_query_param()` drops the `utm_source` tag and leaves `week=3`.
A missing tag would leave the link unchanged.

`get_domain()` pulls the host name, such as `school.example`, so the
shelf can show the site without repeating the whole URL in your head.

`write_csv_from_list()` saves the rows, using the dictionary keys as
headers. `read_csv_to_list()` reads them back as dictionaries with
`site` and `link`.

## Try it yourself

Add a third link, or remove `week` as well. Keep the keys the same so
the CSV columns stay aligned.

## Why use these helpers?

The standard-library version needs `urlparse`, query-pair filtering, and
a CSV writer. These helpers let you focus on the useful sequence: clean
the link, name the site, save the shelf. For more examples, see
[Easy URL](easy_url.md) and [Easy CSV](easy_csv.md).
