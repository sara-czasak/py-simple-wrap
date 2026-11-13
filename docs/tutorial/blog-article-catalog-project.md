# Build a Blog Article Catalog with Easy Generator and Easy Dict

Combine **Easy Generator** and **Easy Dict** to publish article metadata, generate clean URL slugs, organize posts by category, and analyze topic distribution.

## A small real-world example

Bloggers, editorial teams, and content management systems need structured ways to convert article headlines into URL-friendly slugs, standardize post metadata dictionaries, and monitor topic coverage across published content. This example builds an in-memory article registry that maps article slugs to categories, merges default publication status flags, and ranks the most popular topics without writing files to disk.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `blog_catalog.py`:

```python
from py_simple import (
    count_values,
    find_keys,
    generate_slug,
    lists_to_dict,
    merge_dicts,
    most_common_value,
    rename_key,
    sort_dict_by_value,
)

# 1. Generate clean URL slugs from raw article headlines
articles = [
    "10 Tips for Modern Python 3.13!",
    "Async vs Multiprocessing: A Guide!",
    "Building Fast CLI Tools in Python",
    "Understanding Python Metaclasses",
    "Testing Web APIs with Pytest",
    "Deploying Microservices with Docker",
]

slugs = [generate_slug(title) for title in articles]

# 2. Pair column headers with article data to build a structured post
headers = ["title", "author", "category", "reads"]
row_data = ["10 Tips for Modern Python 3.13!", "Alex Rivers", "Tutorials", 1420]
post = lists_to_dict(headers, row_data)

# 3. Rename abbreviated key and attach default publication metadata
post = rename_key(post, "reads", "view_count")
defaults = {"status": "published", "featured": False}
complete_post = merge_dicts(defaults, post)

# 4. Map article slugs to topic categories
catalog = {
    slugs[0]: "Tutorials",
    slugs[1]: "Guides",
    slugs[2]: "Tutorials",
    slugs[3]: "Deep Dive",
    slugs[4]: "Tutorials",
    slugs[5]: "Guides",
}

# 5. Analyze publication topic distribution
category_counts = count_values(catalog)
top_category = most_common_value(catalog)
top_articles = find_keys(top_category, catalog)
ranked_topics = sort_dict_by_value(category_counts, reverse=True)

print("--- Published Article Metadata ---")
print(f"Generated slug: {slugs[0]}")
print(f"Complete post record: {complete_post}")
print()
print("--- Catalog Topic Summary ---")
print(f"Topic counts: {category_counts}")
print(f"Top category: {top_category}")
print(f"Articles in top category: {top_articles}")
print(f"Ranked topics: {ranked_topics}")
```

Run the script from your terminal:

```bash
python blog_catalog.py
```

Example output:

```text
--- Published Article Metadata ---
Generated slug: 10-tips-for-modern-python-3-13
Complete post record: {'status': 'published', 'featured': False, 'title': '10 Tips for Modern Python 3.13!', 'author': 'Alex Rivers', 'category': 'Tutorials', 'view_count': 1420}

--- Catalog Topic Summary ---
Topic counts: {'Tutorials': 3, 'Guides': 2, 'Deep Dive': 1}
Top category: Tutorials
Articles in top category: ['10-tips-for-modern-python-3-13', 'building-fast-cli-tools-in-python', 'testing-web-apis-with-pytest']
Ranked topics: {'Tutorials': 3, 'Guides': 2, 'Deep Dive': 1}
```

## What happened?

`generate_slug()` transforms human-readable headlines with punctuation and mixed casing into clean, lowercase, hyphenated URL slugs suitable for web routing.

`lists_to_dict()` pairs a sequence of field names with corresponding article values by position, assembling a dictionary record in a single call.

`rename_key()` returns a copy of the dictionary with a specified key updated (in this case, normalizing the abbreviated `"reads"` key into `"view_count"`).

`merge_dicts()` combines the default publication dictionary with the article record so every post automatically carries baseline flags like `"status"` and `"featured"`.

`count_values()` scans every value in the catalog dictionary and counts how many times each topic category appears across all registered articles.

`most_common_value()` inspects the catalog dictionary to find the category assigned to the highest number of posts without requiring custom frequency comparisons.

`find_keys()` retrieves a list of all dictionary keys (article slugs) that match a given target value, extracting all posts filed under the top category.

`sort_dict_by_value()` orders the category summary dictionary by post frequency in descending order (`reverse=True`) to produce a ranked popularity leaderboard.

## Try it yourself

- **Add reading time:** Add `"read_time"` to `headers` and a value like `"6 min"` to `row_data` to track estimated reading duration in each post record.
- **Filter another category:** Call `find_keys("Guides", catalog)` to inspect every article filed under the secondary topic.
- **Alphabetical article index:** Use `sort_dict_by_key(catalog)` from `Easy Dict` to print an alphabetical listing of all catalog slugs.

## Why use these helpers?

Without `py-simple-wrap`, achieving this with Python's standard library requires importing multiple modules and writing manual boilerplate:
- Importing `unicodedata` and `re` to normalize Unicode characters, lowercase text, strip punctuation, and collapse consecutive hyphens into a valid URL slug.
- Manually zipping lists (`dict(zip(headers, row_data))`) and writing `.copy()` and `.pop()` statements to rename dictionary keys without mutating in place.
- Merging dictionaries with dictionary unpacking `{**defaults, **post}` and looping over values with `collections.Counter` to count frequencies, extract the mode with `max()`, and list matching keys.
- Writing custom lambda functions (`sorted(counts.items(), key=lambda item: item[1], reverse=True)`) just to sort dictionaries by their values.

Combining `easy_generator` and `easy_dict` replaces regular expression parsing, manual key renaming, and dictionary sorting boilerplate with intuitive, expressive functions.

For more examples and detailed function references, see [Easy Generator](easy_generator.md) and [Easy Dict](easy_dict.md).
