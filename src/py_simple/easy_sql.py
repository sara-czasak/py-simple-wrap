"""
Beginner friendly helpers for handling databases.
"""

import re
import sqlite3
import warnings


class ExperimentalWarning(UserWarning):
    """
    Raised when calling a py_simple function that isn't yet covered
    by tests.
    """


class EasySqlError(Exception):
    """
    Custom exception for py_simple SQL helpers.

    Raised when a database operation fails - for example, when the
    connection to the database file cannot be established.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _check_if_valid(to_check: str) -> bool | None:
    """Check that a table/column string is safe to interpolate into SQL."""
    forbidden = [
        "union",
        "union all",
        "select",
        "join",
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "replace",
        "attach",
        "detach",
        "pragma",
        "vacuum",
        "sqlite_master",
        "sqlite_version",
        "sqlite_temp_master",
        "load_extension",
        "randomblob",
        "zeroblob",
        "glob",
        "like",
    ]

    if not isinstance(to_check, str):
        return False

    pieces = [p.strip() for p in to_check.split(",")]
    for i in forbidden:
        if i in to_check.lower():
            return False
    if to_check == "*":
        return True
    return all(re.fullmatch(r"[0-9A-Za-z_]+", p) for p in pieces)


def open_db(db_filepath: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Opens a connection to a SQLite database file.

    Args:
        db_filepath (str): Path to the database file.

    Returns:
        tuple[sqlite3.Connection, sqlite3.Cursor]: The open connection
            and a cursor for executing SQL statements.

    Raises:
        EasySqlError: If the connection cannot be established.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_db

            connection, cursor = open_db('mydb.db')
            ```

        === "The Traditional Way"
            ```python
            import sqlite3

            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            ```
    """
    try:
        conn = sqlite3.connect(db_filepath)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.OperationalError as e:
        raise EasySqlError(f"\n\nERROR: {e}") from None


def run_select(
    connection: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    table_name: str,
    to_select: str,
    close_conn_after: bool = False,
):
    """
    Runs a SELECT query against a table and returns all matching rows.

    **Status:** 🚧 Experimental — not yet covered by tests; behavior may
    change without notice.

    Validates `table_name` and `to_select` first - only letters, numbers,
    and underscores are allowed (or `*` for `to_select`) - to guard
    against SQL injection before building the query string.

    Args:
        connection (sqlite3.Connection): Open connection to the database.
        cursor (sqlite3.Cursor): Cursor for executing SQL statements.
        table_name (str): Name of the table to select from.
        to_select (str): Column name(s) to select, comma-separated, or
            "*" for all columns.
        close_conn_after (bool): If True, closes `connection` after the
            query runs. Defaults to False.

    Returns:
        list[tuple]: All rows returned by the query.

    Raises:
        EasySqlError: If `table_name` or `to_select` contain anything
            other than letters, numbers, underscores, or "*", or if the
            query itself fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_db, run_select

            connection, cursor = open_db('mydb.db')
            rows = run_select(connection, cursor, 'users', 'name, email')
            ```

        === "The Traditional Way"
            ```python
            import sqlite3

            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            rows = cursor.execute("SELECT name, email FROM users").fetchall()
            ```
    """
    warnings.warn(
        "\n\n‼️WARNING‼️\n🚧 Experimental - not yet "
        "covered by tests; behavior "
        "may change without notice.\n\n",
        category=ExperimentalWarning,
        stacklevel=2,
    )

    if _check_if_valid(table_name) and _check_if_valid(to_select):
        try:
            res = cursor.execute(f"SELECT {to_select} FROM {table_name}")
            rows = res.fetchall()
            if close_conn_after:
                connection.close()
            return rows
        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            raise EasySqlError(f"\n\nERROR: {e}") from None
    else:
        raise EasySqlError(
            "\n\nERROR: table_name and to_select can only "
            "contain:"
            "\n\t- Uppercase letters (A-Z)"
            "\n\t- Lowercase letters (a-z)"
            "\n\t- Underscores  (_)."
        ) from None


def conditional_run_select(
    connection: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    table_name: str,
    to_select: str,
    condition: str,
    params: tuple = (),
    close_conn_after: bool = False,
):
    """
    Runs a SELECT query with a WHERE condition and returns matching rows.

    **Status:** 🚧 Experimental - not yet covered by tests; behavior may
    change without notice.

    Validates `table_name` and `to_select` first - only letters, numbers,
    and underscores are allowed - to guard against SQL injection
    before building the query string.

    Args:
        connection (sqlite3.Connection): Open connection to the database.
        cursor (sqlite3.Cursor): Cursor for executing SQL statements.
        table_name (str): Name of the table to select from.
        to_select (str): Column name(s) to select, comma-separated, or
            "*" for all columns.
        condition (str): SQL condition with `?` placeholders for values
            used in the WHERE clause.
        params (tuple): Values to substitute into the `?` placeholders
            in `condition`, in order. Defaults to an empty tuple.
        close_conn_after (bool): If True, closes `connection` after the
            query runs. Defaults to False.

    Returns:
        list[tuple]: All rows matching the condition.

    Raises:
        EasySqlError: If `table_name` or `to_select` contain anything
            other than letters, numbers, underscores, or "*", or if the
            query itself fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_db, conditional_run_select

            connection, cursor = open_db('mydb.db')
            rows = conditional_run_select(connection, cursor, 'users',
                                           'name, email', "age > ?", (18,))
            ```

        === "The Traditional Way"
            ```python
            import sqlite3

            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT name, email FROM users WHERE age > ?",
                (18,)).fetchall()
            ```
    """
    warnings.warn(
        "\n\n‼️WARNING‼️\n🚧 Experimental - not yet "
        "covered by tests; behavior "
        "may change without notice.\n\n",
        category=ExperimentalWarning,
        stacklevel=2,
    )

    if _check_if_valid(table_name) and _check_if_valid(to_select):
        try:
            res = cursor.execute(
                f"SELECT {to_select} FROM {table_name} WHERE {condition}", params
            )
            rows = res.fetchall()
            if close_conn_after:
                connection.close()
            return rows
        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            raise EasySqlError(f"\n\nERROR: {e}") from None
    else:
        raise EasySqlError(
            "\n\nERROR: table_name and to_select can only "
            "contain:"
            "\n\t- Uppercase letters (A-Z)"
            "\n\t- Lowercase letters (a-z)"
            "\n\t- Underscores  (_)."
        ) from None


def run_insert(
    connection: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    to_insert: list,
    table_name: str,
    columns: list,
    close_conn_after: bool = False,
):
    """
    Inserts a single row into a table.

    **Status:** 🚧 Experimental - not yet covered by tests; behavior may
    change without notice.

    Validates `table_name` and `columns` first - only letters, numbers,
    and underscores are allowed - to guard against SQL injection before
    building the query string. Values in `to_insert` are passed as
    parameters, not interpolated into the query.

    Args:
        connection (sqlite3.Connection): Open connection to the database.
        cursor (sqlite3.Cursor): Cursor for executing SQL statements.
        to_insert (list): Values to insert, in the same order as `columns`.
        table_name (str): Name of the table to insert into.
        columns (list): Column names the values in `to_insert` map to.
        close_conn_after (bool): If True, closes `connection` after the
            insert runs. Defaults to False.

    Raises:
        EasySqlError: If `table_name` or `columns` contain anything
            other than letters, numbers, or underscores, or if the
            insert itself fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_db, run_insert

            connection, cursor = open_db('mydb.db')
            run_insert(connection, cursor, ['Ada', 'ada@example.com'],
                       'users', ['name', 'email'])
            ```

        === "The Traditional Way"
            ```python
            import sqlite3

            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                           ['Ada', 'ada@example.com'])
            conn.commit()
            ```
    """
    warnings.warn(
        "\n\n‼️WARNING‼️\n🚧 Experimental - not yet "
        "covered by tests; behavior "
        "may change without notice.\n\n",
        category=ExperimentalWarning,
        stacklevel=2,
    )

    columns_str = ", ".join(columns)
    if _check_if_valid(columns_str) and _check_if_valid(table_name):
        try:
            cursor.execute(
                f"INSERT INTO {table_name} ({columns_str}) "
                f"VALUES ({(len(to_insert) * '?, ').strip(', ')})",
                to_insert,
            )
            connection.commit()
            if close_conn_after:
                connection.close()
        except (
            sqlite3.OperationalError,
            sqlite3.ProgrammingError,
            sqlite3.DatabaseError,
        ) as e:
            raise EasySqlError(f"\n\nERROR: {e}") from None
    else:
        raise EasySqlError(
            "\n\nERROR: table_name, columns and to_insert "
            "can only contain:"
            "\n\t- Uppercase letters (A-Z)"
            "\n\t- Lowercase letters (a-z)"
            "\n\t- Underscores  (_)."
        ) from None


def run_delete(
    connection: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    table_name: str,
    condition: str,
    params: tuple = (),
    close_conn_after: bool = False,
):
    """
    Deletes rows from a table matching a condition.

    **Status:** 🚧 Experimental - not yet covered by tests; behavior may
    change without notice.

    Validates `table_name` first - only letters, numbers, and
    underscores are allowed -to guard against SQL injection before
    building the query string.

    Args:
        connection (sqlite3.Connection): Open connection to the database.
        cursor (sqlite3.Cursor): Cursor for executing SQL statements.
        table_name (str): Name of the table to delete from.
        condition (str): SQL condition with `?` placeholders for values
            used in the WHERE clause.
        params (tuple): Values to substitute into the `?` placeholders
            in `condition`, in order. Defaults to an empty tuple.
        close_conn_after (bool): If True, closes `connection` after the
            delete runs. Defaults to False.

    Raises:
        EasySqlError: If `table_name` contains anything other than
            letters, numbers, or underscores, or if the delete itself
            fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_db, run_delete

            connection, cursor = open_db('mydb.db')
            run_delete(connection, cursor, 'users', "name = ?", ('Ada',))
            ```

        === "The Traditional Way"
            ```python
            import sqlite3

            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE name = ?", ('Ada',))
            ```
    """
    warnings.warn(
        "\n\n‼️WARNING‼️\n🚧 Experimental - not yet "
        "covered by tests; behavior "
        "may change without notice.\n\n",
        category=ExperimentalWarning,
        stacklevel=2,
    )

    if _check_if_valid(table_name):
        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE {condition}", params)
            if close_conn_after:
                connection.close()
        except (
            sqlite3.OperationalError,
            sqlite3.ProgrammingError,
            sqlite3.DatabaseError,
        ) as e:
            raise EasySqlError(f"\n\nERROR: {e}") from None
    else:
        raise EasySqlError(
            "\n\nERROR: table_name "
            "can only contain:"
            "\n\t- Uppercase letters (A-Z)"
            "\n\t- Lowercase letters (a-z)"
            "\n\t- Underscores  (_)."
        ) from None


def delete_all_from_table(
    connection: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    table_name: str,
    close_conn_after: bool = False,
):
    """
    Deletes all rows from a table, leaving the table itself intact.

    **Status:** 🚧 Experimental - not yet covered by tests; behavior may
    change without notice.

    Validates `table_name` first - only letters, numbers, and
    underscores are allowed - to guard against SQL injection before
    building the query string.

    Args:
        connection (sqlite3.Connection): Open connection to the database.
        cursor (sqlite3.Cursor): Cursor for executing SQL statements.
        table_name (str): Name of the table to empty.
        close_conn_after (bool): If True, closes `connection` after the
            delete runs. Defaults to False.

    Raises:
        EasySqlError: If `table_name` contains anything other than
            letters, numbers, or underscores, or if the delete itself
            fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_db, delete_all_from_table

            connection, cursor = open_db('mydb.db')
            delete_all_from_table(connection, cursor, 'users')
            ```

        === "The Traditional Way"
            ```python
            import sqlite3

            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            ```
    """
    warnings.warn(
        "\n\n‼️WARNING‼️\n🚧 Experimental - not yet "
        "covered by tests; behavior "
        "may change without notice.\n\n",
        category=ExperimentalWarning,
        stacklevel=2,
    )

    if _check_if_valid(table_name):
        try:
            cursor.execute(f"DELETE FROM {table_name}")
            if close_conn_after:
                connection.close()
        except (
            sqlite3.OperationalError,
            sqlite3.ProgrammingError,
            sqlite3.DatabaseError,
        ) as e:
            raise EasySqlError(f"\n\nERROR: {e}") from None
    else:
        raise EasySqlError(
            "\n\nERROR: table_name "
            "can only contain:"
            "\n\t- Uppercase letters (A-Z)"
            "\n\t- Lowercase letters (a-z)"
            "\n\t- Underscores  (_)."
        ) from None


def run_update(
    connection: sqlite3.Connection,
    cursor: sqlite3.Cursor,
    table_name: str,
    updates: dict,
    condition: str,
    params: tuple = (),
    close_conn_after: bool = False,
):
    """
    Updates rows in a table matching a condition.

    **Status:** 🚧 Experimental - not yet covered by tests; behavior may
    change without notice.

    Validates `table_name` and the keys of `updates` first - only
    letters, numbers, and underscores are allowed - to guard against
    SQL injection before building the query string. Values in `updates`
    and `params` are passed as parameters, not interpolated into the
    query.

    Args:
        connection (sqlite3.Connection): Open connection to the database.
        cursor (sqlite3.Cursor): Cursor for executing SQL statements.
        table_name (str): Name of the table to update.
        updates (dict): Column names mapped to their new values, e.g.
            {"age": 30, "city": "Boston"}.
        condition (str): SQL condition with `?` placeholders for values
            used in the WHERE clause.
        params (tuple): Values to substitute into the `?` placeholders
            in `condition`, in order. Defaults to an empty tuple.
        close_conn_after (bool): If True, closes `connection` after the
            update runs. Defaults to False.

    Raises:
        EasySqlError: If `table_name` or any key in `updates` contains
            anything other than letters, numbers, or underscores, or if
            the update itself fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import open_db, run_update

            connection, cursor = open_db('mydb.db')
            run_update(connection, cursor, 'users',
                       {"age": 30, "city": "Boston"}, "name = ?", ('Ada',))
            ```

        === "The Traditional Way"
            ```python
            import sqlite3

            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET age = ?, city = ? WHERE name = ?",
                (30, "Boston", 'Ada'))
            conn.commit()
            ```
    """
    warnings.warn(
        "\n\n‼️WARNING‼️\n🚧 Experimental - not yet "
        "covered by tests; behavior "
        "may change without notice.\n\n",
        category=ExperimentalWarning,
        stacklevel=2,
    )

    columns_str = ", ".join(updates.keys())
    if _check_if_valid(columns_str) and _check_if_valid(table_name):
        try:
            set_clause = ", ".join(f"{col} = ?" for col in updates)
            cursor.execute(
                f"UPDATE {table_name} SET {set_clause} WHERE {condition}",
                (*updates.values(), *params),
            )
            connection.commit()
            if close_conn_after:
                connection.close()
        except (
            sqlite3.OperationalError,
            sqlite3.ProgrammingError,
            sqlite3.DatabaseError,
        ) as e:
            raise EasySqlError(f"\n\nERROR: {e}") from None
    else:
        raise EasySqlError(
            "\n\nERROR: table_name and updates keys can "
            "only contain:"
            "\n\t- Uppercase letters (A-Z)"
            "\n\t- Lowercase letters (a-z)"
            "\n\t- Underscores  (_)."
        ) from None
