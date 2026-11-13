# Easy Base64

Sometimes a program needs to tuck a short message into a form field or a
chat that only allows plain text. Base64 does that, but the
standard library asks you to juggle bytes and encodings. `easy_base64` keeps
the job to one readable call.

## A small real-world example

Imagine a classroom quiz that hides the answer key inside a shareable code.
You encode the answer before you send it, then decode it when you are ready
to check.

```python
from py_simple import decode_text, encode_text, is_base64

answer = "The capital of France is Paris"
code = encode_text(answer)

print(code)
print(is_base64(code))
print(decode_text(code))
```

Example output:

```text
VGhlIGNhcGl0YWwgb2YgRnJhbmNlIGlzIFBhcmlz
True
The capital of France is Paris
```

## What happened?

`encode_text()` turns the answer into a Base64 string you can paste anywhere
plain text is allowed.

`is_base64()` checks that a string really is Base64 before you try to read it.

`decode_text()` turns a valid code back into the original sentence.

## Working with files

To encode an entire file (such as an image or an icon) into Base64 without opening and reading bytes yourself, use `encode_file()`:

```python
from py_simple import encode_file

image_data = encode_file("icon.png")
```

To decode a Base64 string and save it directly to a file (such as restoring an image or document from an API response), use `decode_to_file()`:

```python
from py_simple import decode_to_file

decode_to_file(image_data, "restored_icon.png")
```

## URL-safe Base64

When embedding Base64 strings into URLs, tokens, or filenames, standard characters like `+` and `/` can cause issues. Use `encode_urlsafe_text()` and `decode_urlsafe_text()` to use `-` and `_` instead:

```python
from py_simple import decode_urlsafe_text, encode_urlsafe_text

safe_code = encode_urlsafe_text("hello?world")
print(safe_code)

original = decode_urlsafe_text(safe_code)
print(original)
```

## Working with bytes

Text functions are for words and sentences. If you already have **bytes**
(the raw contents of an image or another file), use `encode_bytes()` instead:

```python
from py_simple import encode_bytes, decode_to_bytes

raw_data = b"hello"
code = encode_bytes(raw_data)
print(code)  # aGVsbG8=

restored_data = decode_to_bytes(code)
print(restored_data)  # b'hello'
```

`decode_to_bytes()` gives you bytes back. Use `decode_text()` when you want a
sentence back, or `decode_to_file()` when you want to save the result to disk.

## Why use these helpers?

The usual version needs `encode`, `decode`, and a `validate=True` flag that
is easy to forget:

```python
import base64

code = base64.b64encode(answer.encode("utf-8")).decode("ascii")
original = base64.b64decode(code, validate=True).decode("utf-8")
```

`easy_base64` keeps that detail inside named functions, so the quiz code
reads like the task you are actually doing.
