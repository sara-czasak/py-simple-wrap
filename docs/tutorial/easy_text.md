# Easy Text

Text appears everywhere in Python programs: user messages, passwords, titles, tags, and reports. The `easy_text` module provides beginner-friendly helpers for cleaning, formatting, analyzing, and transforming text without repeating the same string logic each time.

## A small real-world example

Imagine you're preparing a social media post for a report. You want to clean the title, count its letters and digits, find its hashtags, and count the words that appear most often.

```python
from py_simple import (
    remove_punctuation,
    count_letters,
    count_digits,
    extract_hashtags,
    word_frequency,
)

post = "Python 101: #coding makes text work! #coding"

clean_post = remove_punctuation(post)
letters = count_letters(post)
digits = count_digits(post)
hashtags = extract_hashtags(post)
frequencies = word_frequency(post)

print(clean_post)
# Python 101 coding makes text work coding

print(letters)
# 31

print(digits)
# 3

print(hashtags)
# ['coding', 'coding']

print(frequencies)
# {'python': 1, '101': 1, 'coding': 2, 'makes': 1, 'text': 1, 'work': 1}
```

## What happened?

`remove_punctuation()` removes punctuation while keeping letters, numbers, and spaces.

`count_letters()` counts alphabetic characters, and `count_digits()` counts numeric characters.

`extract_hashtags()` returns hashtag words without their `#` symbols.

`word_frequency()` ignores punctuation, converts words to lowercase, and returns a dictionary with the number of times each word appears.

## Formatting and transforming text

### Truncating text

Use `truncate()` when you need to limit text to a maximum length. If the text is too long, an ellipsis is added.

```python
from py_simple import truncate

print(truncate("A very long message", 10))
# A very lon…

print(truncate("Short", 10))
# Short
```

The traditional version uses slicing and a length check:

```python
text = "A very long message"
length = 10
result = text[:length] + "…" if len(text) > length else text
```

### Reversing words and creating titles

`reverse_words()` reverses the order of words while keeping the words themselves unchanged. `capitalize_title()` capitalizes the first letter of every word.

```python
from py_simple import capitalize_title, reverse_words

title = "the great gatsby"

print(capitalize_title(title))
# The Great Gatsby

print(reverse_words(title))
# gatsby great the
```

The traditional versions use Python's built-in string methods:

```python
title = "the great gatsby"
capitalized = title.title()
reversed_words = " ".join(title.split()[::-1])
```

## Counting and protecting text

### Counting letters and digits

`count_letters()` and `count_digits()` are useful when checking or summarizing input. Spaces and punctuation are not counted.

```python
from py_simple import count_digits, count_letters

text = "Order 123!"
print(count_letters(text))  # 5
print(count_digits(text))  # 3
```

### Masking sensitive text

Use `mask_part()` to hide part of a card number, account number, or other value. The first four characters remain visible by default.

```python
from py_simple import mask_part

print(mask_part("1234567890"))
# 1234 ******

print(mask_part("1234567890", 2))
# 12 ********
```

The traditional version keeps the visible part and replaces the rest with asterisks:

```python
text, visible = "1234567890", 4
result = text[:visible] + " " + "*" * len(text[visible:])
```

## Words, hashtags, and frequencies

### Pluralizing a word

`pluralize()` returns the original word for a count of `1` and adds a plural ending for other counts. Words ending in `s` receive `es`.

```python
from py_simple import pluralize

print(f"{pluralize('cat', 1)}")
# cat

print(f"{pluralize('cat', 3)}")
# cats

print(f"{pluralize('bus', 2)}")
# buses
```

### Extracting hashtags

`extract_hashtags()` finds hashtags made from word characters and returns them without the `#` symbol.

```python
from py_simple import extract_hashtags

hashtags = extract_hashtags("Learning #Python with #py_simple!")
print(hashtags)
# ['Python', 'py_simple']
```

The traditional version uses a regular expression:

```python
import re

text = "Learning #Python with #py_simple!"
hashtags = re.findall(r"#(\w+)", text)
```

### Counting word frequency

`word_frequency()` is useful for simple text analysis. It removes punctuation, treats uppercase and lowercase words as the same, and counts each word.

```python
from py_simple import word_frequency

print(word_frequency("Hello, hello! Welcome."))
# {'hello': 2, 'welcome': 1}
```

## Why use these helpers?

Instead of repeatedly writing slicing expressions, character checks, regular expressions, and word-counting loops, you can use clear, reusable functions:

```python
summary = {
    "title": capitalize_title("my text report"),
    "tags": extract_hashtags("#python #text"),
    "words": word_frequency("Text text tools"),
}
```

These helpers keep common text operations simple, readable, and beginner-friendly.
