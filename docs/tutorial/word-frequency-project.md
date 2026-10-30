# Build a Word Detective with Easy Text and Easy CSV

Combine **Easy Text** and **Easy CSV** to find repeated words in a short
story and save a ranked table you can open in a spreadsheet.

## A small real-world example

You are writing a story about a moon garden and want to spot words you
keep reusing. Install the package with
`python -m pip install py-simple-wrap`, then run this in a practice folder.
It creates or replaces `word-counts.csv` in that folder.

```python
from py_simple import word_frequency, write_csv_from_list

story = "Moon gardens glow. Moon flowers glow, and moon paths sparkle!"
counts = word_frequency(story)

# Put the most frequent words first; sort ties alphabetically.
ranked_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
rows = [{"word": word, "count": count} for word, count in ranked_words]

if rows:
    write_csv_from_list("word-counts.csv", rows)
    for row in rows:
        print(f"{row['word']}: {row['count']}")
    print("Saved word-counts.csv")
else:
    print("No words to count; no CSV was written.")
```

Example output:

```text
moon: 3
glow: 2
and: 1
flowers: 1
gardens: 1
paths: 1
sparkle: 1
Saved word-counts.csv
```

The CSV starts with:

```csv
word,count
moon,3
glow,2
and,1
```

## What happened?

`word_frequency()` removes punctuation, lowercases the text, and counts
words separated by whitespace. That makes `Moon` and `moon` share one
entry, and `glow.` and `glow,` share another.

The sorting key uses a negative count to put larger counts first. Its
second value is the word itself, so equal counts appear alphabetically.
We then turn the pairs into dictionaries with `word` and `count` keys.

`write_csv_from_list()` uses those keys as column headers and writes one
dictionary per row. It opens the output file for writing, so running the
example again replaces the previous report. The `if rows` check avoids
passing an empty list, which the helper rejects. An empty story leaves
any existing report untouched.

## Try it yourself

Replace `story` with your own paragraph, then try an empty string to see
the no-words message. Remember that punctuation is removed rather than
replaced with spaces: `moon-garden` becomes `moongarden`. This is a simple
word counter, so review the results before using them to edit a story.

## Why use these helpers?

You can concentrate on the report: count the words, rank them, and save
the results. The helpers handle the character cleanup and CSV headers,
encoding, and row writing. See [Easy Text](easy_text.md) and
[Easy CSV](easy_csv.md) for more ways to work with the same data.
