# Build an Arcade Leaderboard with Easy SQL and Easy Text

Combine **Easy SQL** and **Easy Text** to store player scores in an in-memory database, format gamer tags and shoutouts, and filter tournament qualifiers.

## A small real-world example

Arcade games and competitive leagues need clean leaderboards to showcase player achievements. This example runs entirely in memory using SQLite's `:memory:` mode, so you can test database queries and text formatting without creating temporary files or leaving databases on disk.

Install the package:

```bash
python -m pip install py-simple-wrap
```

Save this as `arcade_leaderboard.py`:

```python
from py_simple import (
    capitalize_title,
    conditional_run_select,
    open_db,
    pluralize,
    run_insert,
    run_select,
    truncate,
)

# 1. Connect to a temporary in-memory database and set up the table
connection, cursor = open_db(":memory:")
cursor.execute("CREATE TABLE leaderboard (player TEXT, score INTEGER, shoutout TEXT)")

# 2. Raw player submissions with unformatted names and long victory messages
submissions = [
    ("pixel knight", 9800, "GG everyone! Catch me on the next stream."),
    ("shadow ninja", 18200, "Unstoppable combo! New personal record achieved today."),
    ("star voyager", 14500, "GG!"),
    ("speed runner", 7200, "Almost had the gold split!"),
]

# 3. Clean player details and save each score to the database
for raw_name, score, shout in submissions:
    player_name = capitalize_title(raw_name)
    shoutout = truncate(shout, 24)
    run_insert(
        connection,
        cursor,
        [player_name, score, shoutout],
        "leaderboard",
        ["player", "score", "shoutout"],
    )

# 4. Retrieve all scores and display the full arcade rankings
print("--- Arcade Leaderboard ---")
all_records = run_select(connection, cursor, "leaderboard", "player, score, shoutout")
for player, score, shout in sorted(all_records, key=lambda row: row[1], reverse=True):
    print(f'{player} - {score:,} pts | "{shout}"')

# 5. Query players who scored at least 10,000 points to qualify for the tournament
qualifiers = conditional_run_select(
    connection, cursor, "leaderboard", "player, score, shoutout", "score >= ?", (10000,)
)
count = len(qualifiers)
print(f"\nTournament qualifiers: {count} {pluralize('player', count)}")
for player, score, _ in sorted(qualifiers, key=lambda row: row[1], reverse=True):
    print(f"  Qualified: {player} ({score:,} pts)")
```

Run the script from your terminal:

```bash
python arcade_leaderboard.py
```

Example output:

```text
--- Arcade Leaderboard ---
Shadow Ninja - 18,200 pts | "Unstoppable combo! New p…"
Star Voyager - 14,500 pts | "GG!"
Pixel Knight - 9,800 pts | "GG everyone! Catch me on…"
Speed Runner - 7,200 pts | "Almost had the gold spli…"

Tournament qualifiers: 2 players
  Qualified: Shadow Ninja (18,200 pts)
  Qualified: Star Voyager (14,500 pts)
```

## What happened?

`open_db()` establishes a connection to a lightweight SQLite database and returns both the connection and execution cursor. Passing `":memory:"` builds the database inside RAM, leaving zero residual files when the script ends.

`capitalize_title()` converts lowercase player handles (such as `"pixel knight"`) into proper title case (`"Pixel Knight"`).

`truncate()` caps long victory messages to 24 characters and appends an ellipsis (`…`) so descriptions display cleanly within leaderboard columns.

`run_insert()` safely commits each cleaned record into the `leaderboard` table using parameterized inputs that defend against SQL injection.

`run_select()` queries all rows from the specified table and columns, returning the stored leaderboard records as a list of tuples.

`conditional_run_select()` filters the table with a parameterized SQL `WHERE` clause (`score >= ?`), cleanly returning only the players who achieved 10,000 points or more.

`pluralize()` checks the count of qualified players and selects the grammatically correct word (`"player"` for 1, `"players"` for any other count).

## Try it yourself

- **Change the score threshold:** Adjust the condition parameter in `conditional_run_select()` from `10000` to `15000` to see only top grandmasters qualify (`1 player`).
- **Update a player score:** Use `run_update(connection, cursor, "leaderboard", {"score": 20000}, "player = ?", ("Pixel Knight",))` to simulate a player beating their previous high score.
- **Wipe the board:** Call `delete_all_from_table(connection, cursor, "leaderboard")` to reset the arcade cabinet between seasons.

## Why use these helpers?

Without `py-simple-wrap`, managing databases and text formatting in standard Python requires writing substantial boilerplate:
- Writing manual `sqlite3` setup code, creating cursors, and remembering to call `connection.commit()` after every query.
- Manually writing parameterized SQL queries with string concatenation while carefully checking for injection vulnerabilities.
- Writing custom text truncation loops with slices and conditional checks (`len(s) > limit`) and conditional pluralization logic (`"player" if count == 1 else "players"`).

Combining `easy_sql` and `easy_text` replaces database plumbing and string handling with intuitive, readable single-line helpers.

For more examples and detailed function references, see [Easy SQL](easy_sql.md) and [Easy Text](easy_text.md).
