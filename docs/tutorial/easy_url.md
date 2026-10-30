# Easy URL

Links show up in bookmarks, club pages, and search results. Pulling out the
site name, checking HTTPS, or adding `?page=2` usually means importing four
names from `urllib.parse`. `easy_url` keeps each of those jobs as one function.

## A small real-world example

Imagine a club page that should only link to secure sites, and the "next
page" button needs a page number on the link.

```python
from py_simple import add_query_param, get_domain, is_https

link = "https://school.example/clubs"
print(get_domain(link))
print(is_https(link))
print(add_query_param(link, "page", "2"))
```

Example output:

```text
school.example
True
https://school.example/clubs?page=2
```

## What happened?

`get_domain()` returns the host name and leaves off the path.

`is_https()` is True only when the link starts with `https`.

`add_query_param()` adds `page=2`. Call it again with the same name and the
old value is replaced instead of duplicated.

## Read every value for a query parameter

Links can use the same query name more than once. `get_query_values()`
keeps those values in order, including blanks:

```python
from py_simple import get_query_values

link = "https://school.example/clubs?tag=python&tag=&tag=art+club#list"
print(get_query_values(link, "tag"))
print(get_query_values(link, "missing"))
```

Example output:

```text
['python', '', 'art club']
[]
```

Pass the decoded, case-sensitive name. Percent escapes are decoded and
`+` becomes a space; a bare `tag` also produces an empty string. The
fragment is ignored, and the input link is not changed. This uses the
module's existing full-link validation rather than checking whether a
link is safe to visit.

## Why use these helpers?

A link without `https://` is rejected with a clear error, so a bare
`school.example` does not quietly become an empty host. The query helper
keeps any parameters that were already on the link.
