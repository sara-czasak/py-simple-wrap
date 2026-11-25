# Build a Community Post Digest with Easy Regex and Easy Lists

Combine **Easy Regex** and **Easy Lists** to extract links, hashtags, and mentions from social posts and summarize trending topics.

## A small real-world example

Community moderators, developer advocates, and social media managers often need to parse message streams or announcement channels to see which topics are trending and which links or contributors are frequently highlighted. This example extracts URLs, hashtags, and usernames from a list of community messages, identifies the top trending tag, and detects frequently mentioned members entirely in memory without writing files to disk.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `community_digest.py`:

```python
from py_simple.easy_regex import (
    extract_hashtags,
    extract_mentions,
    extract_urls,
)
from py_simple.easy_lists import (
    find_duplicates,
    flatten_list,
    most_common_item,
    unique_items,
)

posts = [
    "Excited to launch our new open source tool! Check it out: https://py-simple.dev #python #opensource @sara",
    "Great tutorial by @alex on building CLI tools with #python! cc @sara",
    "Join our weekend hackathon! Details at https://hackathon.org #coding #python #hackathon @dev_team",
    "Loving the new release of py-simple-wrap! #python #opensource @alex",
]

# 1. Extract hashtags, mentions, and URLs across all posts
all_tags = flatten_list([extract_hashtags(p) for p in posts])
all_mentions = flatten_list([extract_mentions(p) for p in posts])
all_urls = flatten_list([extract_urls(p) for p in posts])

# 2. Analyze trending topics and member activity
unique_tags = unique_items(all_tags)
top_tag = most_common_item(all_tags)
active_members = unique_items(all_mentions)
frequent_mentions = find_duplicates(all_mentions)

print("--- Community Post Digest ---")
print(f"Total posts analyzed: {len(posts)}")
print(f"Shared links ({len(all_urls)}): {all_urls}")
print(f"Unique hashtags ({len(unique_tags)}): {unique_tags}")
print(f"Trending topic: {top_tag}")
print(f"Tagged members: {active_members}")
print(f"Frequently mentioned: {frequent_mentions}")
```

Run the script from your terminal:

```bash
python community_digest.py
```

Example output:

```text
--- Community Post Digest ---
Total posts analyzed: 4
Shared links (2): ['https://py-simple.dev', 'https://hackathon.org']
Unique hashtags (4): ['#python', '#opensource', '#coding', '#hackathon']
Trending topic: #python
Tagged members: ['@sara', '@alex', '@dev_team']
Frequently mentioned: ['@sara', '@alex']
```

## What happened?

`extract_hashtags()` from `Easy Regex` scans message text and pulls out hashtag tokens (including their `#` prefix) without requiring custom regular expression boundaries.

`extract_mentions()` locates user handle mentions prefixed with `@` across each post.

`extract_urls()` extracts full web links embedded in message bodies for easy URL cataloging.

`flatten_list()` merges lists of extracted tokens across multiple messages into a single unified list.

`unique_items()` removes duplicate tags and handles while preserving the order in which they were first encountered.

`most_common_item()` identifies the most frequently used hashtag to highlight the primary trending topic.

`find_duplicates()` isolates usernames mentioned more than once to recognize repeated community contributors.

## Try it yourself

- **Extract email contacts:** Call `extract_emails()` from `Easy Regex` on message text to detect support or reach-out email addresses.
- **Capture phone numbers:** Use `extract_phone_numbers()` to extract contact numbers from event or help-desk announcements.
- **Clean irregular whitespace:** Call `clean_extra_whitespace()` on user-submitted messages before parsing to normalize tabs and spacing.

## Why use these helpers?

Without `py-simple-wrap`, achieving this with Python's standard library requires extensive boilerplate and custom regular expressions:
- Compiling multiple regular expressions (`re.findall(r'#(\w+)', ...)`, `re.findall(r'@\w+', ...)`, and complex URL regex patterns) while handling edge cases and trailing punctuation.
- Writing nested list comprehension loops (`[item for sublist in nested for item in sublist]`) to flatten extracted results.
- Maintaining dictionary counting loops or importing `collections.Counter` and calling `.most_common(1)` just to identify the most frequent tag.
- Looping with custom tracking sets to extract duplicate items while preserving appearance order.

Combining `easy_regex` and `easy_lists` replaces regex compilation and list accumulation boilerplate with clean, single-line functions.

For more examples and detailed function references, see [Easy Regex](easy_regex.md) and [Easy Lists](easy_lists.md).
