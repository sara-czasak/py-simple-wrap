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

## Check a website's HTTP status code

When visiting a website or working with URLs, it is useful to know whether the requested page is accessible and how the server responds.

Web servers return HTTP status codes to indicate the result of a request. For example:

- `200 OK` – The request was successful.
- `301 Moved Permanently` – The resource has moved to another URL.
- `404 Not Found` – The requested page could not be found.
- `500 Internal Server Error` – Something went wrong on the server.

`get_url_status_code()` makes it easy to retrieve the HTTP status code and response message for a URL without writing the request-handling code yourself.

### Basic usage

```python
from py_simple import get_url_status_code

result = get_url_status_code("https://example.com")

print(result)
```

Example output:

```python
{
    "status_code": 200,
    "message": "OK"
}
```

### Check a page that does not exist

```python
result = get_url_status_code(
    "https://example.com/non-existent-page"
)

print(result)
```

Example output:

```python
{
    "status_code": 404,
    "message": "Not Found"
}
```

A `404` is a valid HTTP response. It means the server responded, but the requested resource could not be found.

### Set a custom timeout

The function uses a default timeout of 5 seconds. You can provide a different timeout if needed.

```python
result = get_url_status_code(
    "https://example.com",
    timeout=10
)

print(result)
```

Here, the request waits for up to 10 seconds.

### Handle connection errors

If the URL uses an unsupported scheme, the connection times out, or the request fails, the function returns a dictionary with `None` as the status code and a descriptive message.

For example, an unsupported FTP URL:

```python
result = get_url_status_code("ftp://example.com/file.txt")

print(result)
```

Example output:

```python
{
    "status_code": None,
    "message": "Unsupported URL scheme. Only HTTP and HTTPS are supported."
}
```

Other possible error messages include:

| Situation | Message |
|---|---|
| Connection timeout | `Connection timed out.` |
| Connection failure | `Connection failed.` |
| Other request error | `Unable to complete the request.` |

### Understanding the return value

The function always returns a dictionary containing:

| Key | Description |
|---|---|
| `status_code` | HTTP status code returned by the server, or `None` if no response was received. |
| `message` | HTTP response reason or an error message. |

You can use the returned status code in conditional statements:

```python
result = get_url_status_code("https://example.com")

if result["status_code"] == 200:
    print("Website is responding successfully.")
elif result["status_code"] is None:
    print("Request failed:", result["message"])
else:
    print("HTTP response:", result["status_code"])
```

**Note:** Only HTTP and HTTPS URLs are supported. The function sends a GET request and follows redirects by default. HTTP error responses such as 404 and 500 are returned normally; they are not treated as connection failures.

## Why use these helpers?

A link without `https://` is rejected with a clear error, so a bare
`school.example` does not quietly become an empty host. The query helper
keeps any parameters that were already on the link.