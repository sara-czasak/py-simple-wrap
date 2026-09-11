# Easy Validator

Validating user input is something you'll often need in Python projects. Checking emails, usernames, URLs, ZIP codes, and passwords can require repetitive regular expressions and validation logic.

The `easy_validator` module provides simple helpers for common validation tasks, allowing you to check whether values follow expected formats without writing the underlying validation logic yourself.

## A small real-world example

Imagine you're creating a registration form where users need to provide an email address, username, and password.

```python id="h4x8sd"
from py_simple import is_valid_email, is_valid_username, is_password_secure

email = "hello@example.com"
username = "user_name"
password = "1andkrf!AG5"

print(is_valid_email(email))
print(is_valid_username(username))
print(is_password_secure(password))
```

Example output:

```text id="t2k6pf"
True
True
True
```

## What happened?

`is_valid_email()` checks whether a string follows a valid email format.

`is_valid_username()` checks whether a username contains only letters, numbers, and underscores.

`is_valid_zipcode()` checks whether a value is a valid five-digit US ZIP code.

`is_valid_url()` checks whether a string follows a supported URL format.

`is_password_secure()` checks a password against several security requirements.

For example:

```python id="s7n3qm"
from py_simple import is_valid_url, is_valid_zipcode

print(is_valid_url("https://example.com"))
# True

print(is_valid_zipcode(12345))
# True
```

## The Py_simple Way

```python id="j8v2nc"
from py_simple import (
    is_valid_email,
    is_valid_username,
    is_valid_zipcode,
    is_valid_url,
    is_password_secure,
)

print(is_valid_email("hello@example.com"))
print(is_valid_username("user_name"))
print(is_valid_zipcode(12345))
print(is_valid_url("www.google.com"))
print(is_password_secure("1andkrf!AG5"))
```

## The Traditional Way

Without `py_simple`, you would normally need to write the appropriate regular expressions and validation logic yourself:

```python id="r5k1zp"
import re

email_pattern = r"[a-zA-Z_.%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+"
username_pattern = r"^[a-zA-Z0-9_]+"
zipcode_pattern = r"^[0-9]{5}$"

email_valid = bool(re.fullmatch(email_pattern, "hello@example.com"))

username_valid = bool(re.fullmatch(username_pattern, "user_name"))

zipcode_valid = bool(re.fullmatch(zipcode_pattern, str(12345)))
```

For password validation, you would additionally need to manually count characters, check their types, and make sure characters aren't repeated.

The `easy_validator` helpers package these common validation patterns into simple, reusable functions.

## Validating emails and usernames

`is_valid_email()` checks whether an email follows the expected format:

```python id="c3n7vw"
from py_simple import is_valid_email

print(is_valid_email("hello@example.com"))
# True

print(is_valid_email("not-an-email"))
# False
```

`is_valid_username()` accepts usernames containing letters, numbers, and underscores:

```python id="x9q4mk"
from py_simple import is_valid_username

print(is_valid_username("user_name"))
# True

print(is_valid_username("user-name"))
# False
```

## Validating URLs and ZIP codes

`is_valid_url()` checks common URLs:

```python id="p6d2fz"
from py_simple import is_valid_url

print(is_valid_url("www.google.com"))
# True

print(is_valid_url("https://example.com"))
# True
```

`is_valid_zipcode()` checks for a five-digit US ZIP code:

```python id="m8r5yx"
from py_simple import is_valid_zipcode

print(is_valid_zipcode(12345))
# True

print(is_valid_zipcode(1234))
# False
```

## Checking password security

`is_password_secure()` checks that a password meets several requirements.

A password must have:

* At least 9 characters.
* At least 1 uppercase letter.
* At least 2 lowercase letters.
* At least 2 digits.
* At least 1 special character.
* No consecutive repeated characters.

For example:

```python id="f7c2ka"
from py_simple import is_password_secure

password = "1andkrf!AG5"

print(is_password_secure(password))
```

Output:

```text id="b9w4qt"
True
```

A password that doesn't meet the requirements returns `False`:

```python id="v3m8sx"
print(is_password_secure("password"))
# False
```

## Validating credit card numbers

`is_valid_creditcard()` checks that a credit card number meets some basic requirements (which doesn't necessarily mean that it's a real credit card number).

A valid credit card number is 13 to 19 digits long with optional dashes or spaces for formatting. Additionally, numbers meeting those requirements are checked against the [Luhn algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm), a type of checksum designed to detect errors when relaying or transcribing credit card numbers.

For example:

```python
from py_simple import is_valid_creditcard

# Valid test numbers provided by Stripe
# https://docs.stripe.com/testing?testing-method=card-numbers#cards
visa = "4242-4242-4242-4242"
visa_error = "4242-4242-4242-4241"  # last digit changed!

print(is_valid_creditcard(visa))
print(is_valid_creditcard(visa_error))
```

Output:

```text
True
False
```

## Why use these helpers?

Instead of repeatedly writing regular expressions, character counters, and validation conditions, you can simply use:

```python id="n2x6pk"
is_valid_email(email)
is_valid_username(username)
is_valid_zipcode(zipcode)
is_valid_url(url)
is_password_secure(password)
is_valid_creditcard(card_num)
```

These helpers keep common validation tasks simple, readable, and beginner-friendly while handling the underlying regular expressions and validation logic for you.
