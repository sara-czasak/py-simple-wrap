# Easy Base64

Sometimes a program needs to tuck a short message into a form field, a
filename, or a chat that only allows plain text. Base64 does that, but the
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
