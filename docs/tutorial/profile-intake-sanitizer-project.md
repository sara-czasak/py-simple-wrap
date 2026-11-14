# Build a Profile Intake Sanitizer with Easy Strings and Easy Validator

Combine **Easy Strings** and **Easy Validator** to sanitize messy applicant text, generate formatted identifiers and slugs, and validate profile credentials.

## A small real-world example

User signup portals, job applications, and community directories frequently receive inputs with messy padding, irregular casing, or invalid contact formats. This example sanitizes user profile inputs, generates clean snake_case and kebab-case identifiers, and validates contact emails, URLs, phone numbers, and security criteria entirely in memory without writing files to disk.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `profile_sanitizer.py`:

```python
from py_simple import (
    count_words,
    is_alphanumeric,
    is_password_secure,
    is_valid_email,
    is_valid_phone_number,
    is_valid_url,
    is_valid_username,
    remove_extra_spaces,
    to_kebab_case,
    to_snake_case,
)

applicant = {
    "display_name": "   Elena   Vasquez   ",
    "handle": "elena_dev99",
    "project_title": "Cloud Backup Daemon",
    "email": "elena.vasquez@example.org",
    "phone": "+1-555-019-2834",
    "portfolio": "https://elena-dev.io/projects",
    "password": "River!27Map",
    "bio": "Full-stack developer building robust backend APIs, distributed workflows, and open-source command line tools.",
}

# 1. Clean whitespace and derive standard identifiers
clean_name = remove_extra_spaces(applicant["display_name"])
user_tag = to_snake_case(clean_name)
repo_slug = to_kebab_case(applicant["project_title"])
bio_words = count_words(applicant["bio"])

# 2. Run intake validation checks
checks = {
    "username": is_valid_username(applicant["handle"]),
    "email": is_valid_email(applicant["email"]),
    "phone": is_valid_phone_number(applicant["phone"]),
    "portfolio": is_valid_url(applicant["portfolio"]),
    "password": is_password_secure(applicant["password"]),
    "handle_chars": is_alphanumeric(applicant["handle"].replace("_", "")),
    "bio_length": bio_words >= 10,
}

print("--- Applicant Profile Audit ---")
print(f"Clean name: {clean_name}")
print(f"User identifier: {user_tag}")
print(f"Project slug: {repo_slug}")
print(f"Bio word count: {bio_words}")
print()
print("--- Intake Validation Checks ---")
for field, passed in checks.items():
    print(f"{field}: {passed}")
print(f"Application accepted: {all(checks.values())}")
```

Run the script from your terminal:

```bash
python profile_sanitizer.py
```

Example output:

```text
--- Applicant Profile Audit ---
Clean name: Elena Vasquez
User identifier: elena_vasquez
Project slug: cloud-backup-daemon
Bio word count: 15

--- Intake Validation Checks ---
username: True
email: True
phone: True
portfolio: True
password: True
handle_chars: True
bio_length: True
Application accepted: True
```

## What happened?

`remove_extra_spaces()` strips leading and trailing whitespace while collapsing duplicate interior spaces into single gaps.

`to_snake_case()` converts human-readable text into lowercase snake_case format (`"elena_vasquez"`), ideal for database primary keys or internal user tags.

`to_kebab_case()` transforms titles into hyphenated kebab-case (`"cloud-backup-daemon"`), suitable for repository names and web URLs.

`count_words()` counts the number of words in freeform text without manual whitespace tokenization, verifying that the candidate bio meets minimum length requirements.

`is_valid_username()` verifies that the public handle follows standard alphanumeric naming rules without illegal characters.

`is_valid_email()` validates that the email address adheres to standard mailbox format conventions.

`is_valid_phone_number()` verifies that the contact phone string follows standard numeric and country-code structures.

`is_valid_url()` confirms that the portfolio web address contains a valid protocol scheme and domain target.

`is_password_secure()` checks the password against core security criteria: minimum length, uppercase and lowercase letters, numbers, symbols, and no adjacent duplicate characters.

`is_alphanumeric()` validates that a string contains only letters and numbers without unexpected special punctuation.

## Try it yourself

- **Test invalid contact formats:** Change `phone` to `"123-abc"` or `email` to `"missing-at.com"` to see the corresponding validation flag switch to `False`.
- **Enforce password duplicate rules:** Change `password` to `"River!27Maap"` to observe `is_password_secure()` catch and reject adjacent duplicate characters (`"aa"`).
- **Require longer bios:** Increase the bio length check threshold from `10` words to `20` words to enforce more descriptive candidate summaries.

## Why use these helpers?

Without `py-simple-wrap`, achieving this with Python's standard library requires extensive boilerplate and custom regular expressions:
- Writing regular expressions or split-and-join logic to collapse duplicate spaces and transform text between snake_case and kebab-case.
- Compiling complex regular expressions for RFC email formats, phone numbers, and URL schemes.
- Iterating across strings with character class lookups and state tracking just to verify password security rules.

Combining `easy_strings` and `easy_validator` replaces fragile custom regex parsing and string manipulation with concise, well-tested validation and formatting helpers.

For more examples and detailed function references, see [Easy Strings](easy_strings.md) and [Easy Validator](easy_validator.md).
