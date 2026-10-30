# Build a Message Capsule with Easy Base64 and Easy JSON

Write a note to your future self, store it as a shareable code in a JSON
file, then open it in a later run. Combine **Easy Base64** for the text
encoding with **Easy JSON** for saving and loading the capsule.

Base64 is reversible encoding, not encryption or a time lock. Anyone who
has the file can read the message, so use a fun note rather than a secret.

## The build

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save the following as `message_capsule.py`. This project uses the existing
text and JSON helpers and needs no optional extras.

```python
import argparse

from py_simple import (
    EasyBase64Error,
    decode_text,
    encode_text,
    open_json,
    save_json_data,
)
from py_simple.easy_json import EasyJsonError


def main():
    parser = argparse.ArgumentParser(description="Save or open a message capsule")
    parser.add_argument("action", choices=["create", "open"])
    parser.add_argument("file", help="Path to the capsule JSON file")
    parser.add_argument("--message", help="Your note, required when creating")
    args = parser.parse_args()

    if args.action == "create" and args.message is None:
        parser.error("create requires --message")
    if args.action == "open" and args.message is not None:
        parser.error("--message is only used with create")

    try:
        if args.action == "create":
            capsule = {
                "format": "message-capsule-v1",
                "message": encode_text(args.message),
            }
            save_json_data(args.file, capsule)
            print(f"Saved capsule: {args.file}")
        else:
            capsule = open_json(args.file)
            if (
                not isinstance(capsule, dict)
                or capsule.get("format") != "message-capsule-v1"
                or not isinstance(capsule.get("message"), str)
            ):
                parser.exit(1, "This file is not a message capsule.\n")
            print("Your message:", decode_text(capsule["message"]))
    except (EasyBase64Error, EasyJsonError) as error:
        parser.exit(1, f"Could not {args.action} capsule: {str(error).strip()}\n")


if __name__ == "__main__":
    main()
```

## Save it, then come back later

Run these commands in the folder containing your script:

```bash
python message_capsule.py create capsule.json --message "You finished your first Python project!"
python message_capsule.py open capsule.json
```

Output:

```text
Saved capsule: capsule.json
Your message: You finished your first Python project!
```

These are separate program runs: the second command gets the message from
the file, not from a variable left over from the first run. You can close
the terminal and run the `open` command tomorrow, or send the JSON file to
a friend who has the same script.

Unicode works too. Try a new file with `--message "Hello, future me! 🎉"`.

## What happened?

`encode_text()` converts your note to UTF-8 and then Base64. The JSON object
stores that code alongside a small format label, so the script can recognize
its own files.

`save_json_data()` writes the object to the chosen filename. It refuses to
replace an existing file. If you repeat the `create` command with the same
filename, the program reports an error and leaves your original capsule
alone. Pick a new filename for your next note.

`open_json()` loads the saved object. The script checks its format and
message field before calling `decode_text()` to restore the original note.
An invalid JSON file, missing file, or malformed Base64 message produces a
short error and a nonzero exit status.

Python's `argparse` handles the two commands and required arguments. Run
`python message_capsule.py --help` to see them. The two py-simple-wrap
modules handle the encoding and file operations.

## Make it your own

- Write a capsule for each finished project, using a different filename.
- Add a `title` field and show it above the decoded message. Update the
  reader's field checks if you make the title required.
- Add a suggested opening date as a label. It is a reminder, not protection
  against someone opening the file early.

## Why use these helpers?

With the standard library, you would convert between text and bytes,
validate Base64 while decoding, open files with the right encoding, and
serialize or parse JSON. These helpers keep those steps behind named
operations while the project code focuses on creating and opening a note.

See [Easy Base64](easy_base64.md) and [Easy JSON](easy_json.md) for the
individual modules. For a different in-memory game involving a checksum,
try [Message Detective](message-detective-project.md).
