# Build a Password Strength Game with Easy Generator, Easy Validator, and Easy Text

Combine **Easy Generator**, **Easy Validator**, and **Easy Text** to build a small terminal game that challenges players to create secure passwords and awards points for strength and character variety.

## What we are building

The player gets three attempts to create a password. Each attempt earns points for length, letter variety, digits, special characters, and passing the complete security check. Reaching 6/6 means the game is passed; using all three attempts without reaching 6/6 means the game is failed. The game explains the result and offers a generated example when the player needs inspiration. The example only evaluates passwords in memory and never saves a player's password after the check.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `password_game.py`:

```python
from py_simple import count_letters, generate_password, is_password_secure


def score_password(password: str) -> tuple[int, list[str]]:
    """Return a strength score and feedback for a password."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("use at least 8 characters")

    if count_letters(password) >= 4:
        score += 1
    else:
        feedback.append("include at least 4 letters")

    if any(character.isupper() for character in password) and any(
        character.islower() for character in password
    ):
        score += 1
    else:
        feedback.append("mix uppercase and lowercase letters")

    if sum(character.isdigit() for character in password) >= 2:
        score += 1
    else:
        feedback.append("include at least 2 digits")

    if any(not character.isalnum() for character in password):
        score += 1
    else:
        feedback.append("include a special character")

    if is_password_secure(password):
        score += 1
    else:
        feedback.append("avoid repeated characters and satisfy every security rule")

    return score, feedback


def play_password_game() -> None:
    """Run a short password-strength challenge in the terminal."""
    print("=== Password Strength Challenge ===")
    print("Create a password with at least 8 characters, uppercase and lowercase letters,")
    print("two digits, a special character, and no repeated characters.")
    print("You have three attempts.\n")

    for attempt in range(1, 4):
        password = input(f"Attempt {attempt}/3 — enter a password: ")

        score, feedback = score_password(password)
        print(f"Strength score: {score}/6")

        if score == 6:
            print("\nCongratulations! Your password scored 6/6.")
            print("You have passed this game.")
            return

        print("Suggestions: " + "; ".join(feedback) + ".")

        if attempt < 3:
            example = generate_password(
                pass_length=12,
                uppercase_chars=2,
                digit_chars=2,
                special_chars=2,
            )
            print(f"Hint: try a pattern like {example} (do not reuse this example).\n")

    print("\nGame failed: Sorry you failed to get a 6/6 score in three attempts.")
    print("Try again with a longer, less predictable password.")


if __name__ == "__main__":
    play_password_game()
```

Run the game from your terminal:

```bash
python password_game.py
```

Example session:

```text
=== Password Strength Challenge ===
Create a password with at least 8 characters, uppercase and lowercase letters,
two digits, a special character, and no repeated characters.
You have three attempts.

Attempt 1/3 — enter a password: sunshine
Strength score: 2/6
Suggestions: mix uppercase and lowercase letters; include at least 2 digits; include a special character; avoid repeated characters and satisfy every security rule.
Hint: try a pattern like aQ7!mZ2@rT5k (do not reuse this example).

Attempt 2/3 — enter a password: River!27Map
Strength score: 6/6

Congratulations! Your password scored 6/6.
You have passed this game.
```

## What happened?

1. `count_letters(password)` contributes a point when the password contains enough letters to provide meaningful variety.
2. The character checks contribute points for mixed case, digits, and special characters. The game can explain missing criteria instead of showing only `True` or `False`.
3. `is_password_secure(password)` contributes the final point when the password passes the module's complete rules: at least 8 characters, one special character, one uppercase letter, at least two lowercase letters, at least two digits, and no repeating characters.
4. A score of `6/6` immediately ends the game with a passed result; after three lower scores, the game ends with a failed result.
5. The `for` loop gives the player three attempts without requiring separate counters or repeated input code.
6. `generate_password()` creates a randomized example with the requested length and character counts. It also shuffles the characters and avoids identical adjacent characters.
7. The example is shown only as a hint. A generated password should not be copied directly into a real account, and this tutorial does not store passwords in a file or database.

## Try it yourself

- Change the number of attempts from `3` to `5`.
- Make the generated hint longer by changing `pass_length=12` to `pass_length=16`.
- Add a high-score table that stores only scores and dates, never passwords.
- Replace the generated hint with a reminder to use a unique passphrase instead of copying a random example.
- Add a second round where the player must create a different secure password.

## Why use these helpers?

Without `py-simple-wrap`, the game would need to manually count letters, detect uppercase and lowercase letters, count digits and punctuation, check the minimum length, and track repeated characters. It would also need separate logic to build character pools, choose random characters, shuffle them, and avoid adjacent duplicates.

Combining `easy_generator`, `easy_validator`, and `easy_text` keeps the game focused on its rules and feedback. `generate_password()` handles random password construction, `count_letters()` simplifies one of the scoring checks, and `is_password_secure()` provides the final complete-security check.

For more examples and detailed function references, see [Easy Generator](easy_generator.md), [Easy Text](easy_text.md), and [Easy Validator](easy_validator.md).
