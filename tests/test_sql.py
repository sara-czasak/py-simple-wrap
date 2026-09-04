import sqlite3

import pytest

from py_simple.easy_sql import (
    EasySqlError,
    conditional_run_select,
    delete_all_from_table,
    open_db,
    run_delete,
    run_insert,
    run_select,
    run_update,
)


def test_open_db_success():
    """Test if the database opens successfully."""
    # SQLite has a cool trick: using ":memory:" creates a temporary
    # database in your computer's RAM that deletes itself when finished!
    conn, cursor = open_db(":memory:")

    # Assert (check) that the function gave us back the right types of objects
    assert isinstance(conn, sqlite3.Connection)
    assert isinstance(cursor, sqlite3.Cursor)

    # Close the connection safely
    conn.close()


def test_open_db_error():
    """Test if EasySqlError is raised when given a bad path."""
    # We give it a completely impossible file path to force it to fail
    invalid_path = "/this/directory/does/not/exist/test.db"

    # Assert that calling the function with a bad path raises Sara's custom error
    with pytest.raises(EasySqlError):
        open_db(invalid_path)


class TestRunSelect:
    """Tests for run_select function."""

    def setup_method(self):
        """Create a fresh in-memory database with test data before each test."""
        self.conn, self.cursor = open_db(":memory:")
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER)"
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Alice", "alice@example.com", 30),
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Bob", "bob@example.com", 25),
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Charlie", "charlie@example.com", 35),
        )
        self.conn.commit()

    def teardown_method(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_run_select_all_columns(self):
        """Test selecting all columns with *."""
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 3
        assert rows[0][1] == "Alice"
        assert rows[1][1] == "Bob"
        assert rows[2][1] == "Charlie"

    def test_run_select_specific_columns(self):
        """Test selecting specific columns."""
        rows = run_select(self.conn, self.cursor, "users", "name, email")
        assert len(rows) == 3
        assert rows[0] == ("Alice", "alice@example.com")
        assert rows[1] == ("Bob", "bob@example.com")
        assert rows[2] == ("Charlie", "charlie@example.com")

    def test_run_select_single_column(self):
        """Test selecting a single column."""
        rows = run_select(self.conn, self.cursor, "users", "name")
        assert len(rows) == 3
        assert rows[0] == ("Alice",)
        assert rows[1] == ("Bob",)
        assert rows[2] == ("Charlie",)

    def test_run_select_close_conn_after(self):
        """Test that connection closes when close_conn_after=True."""
        rows = run_select(self.conn, self.cursor, "users", "*", close_conn_after=True)
        assert len(rows) == 3
        # Connection should be closed, next operation should fail
        with pytest.raises(sqlite3.ProgrammingError):
            self.cursor.execute("SELECT * FROM users")

    def test_run_select_invalid_table_name(self):
        """Test that invalid table name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            run_select(self.conn, self.cursor, "users; DROP TABLE users;--", "*")

    def test_run_select_invalid_column_name(self):
        """Test that invalid column name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            run_select(self.conn, self.cursor, "users", "name; DROP TABLE users;--")

    def test_run_select_sql_injection_table(self):
        """Test SQL injection attempt via table name."""
        malicious_table = "users; DROP TABLE users;--"
        with pytest.raises(EasySqlError):
            run_select(self.conn, self.cursor, malicious_table, "*")
        # Verify table still exists
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 3

    def test_run_select_sql_injection_column(self):
        """Test SQL injection attempt via column name."""
        malicious_column = "name, email; DROP TABLE users;--"
        with pytest.raises(EasySqlError):
            run_select(self.conn, self.cursor, "users", malicious_column)
        # Verify table still exists
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 3

    def test_run_select_union_injection(self):
        """Test UNION-based SQL injection attempt."""
        with pytest.raises(EasySqlError):
            run_select(
                self.conn, self.cursor, "users UNION SELECT * FROM sqlite_master", "*"
            )
        with pytest.raises(EasySqlError):
            run_select(
                self.conn,
                self.cursor,
                "users",
                "name UNION SELECT sql FROM sqlite_master",
            )


class TestConditionalRunSelect:
    """Tests for conditional_run_select function."""

    def setup_method(self):
        """Create a fresh in-memory database with test data before each test."""
        self.conn, self.cursor = open_db(":memory:")
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER)"
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Alice", "alice@example.com", 30),
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Bob", "bob@example.com", 25),
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Charlie", "charlie@example.com", 35),
        )
        self.conn.commit()

    def teardown_method(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_conditional_run_select_basic(self):
        """Test basic conditional select with parameter."""
        rows = conditional_run_select(
            self.conn, self.cursor, "users", "name, age", "age > ?", (28,)
        )
        assert len(rows) == 2
        assert rows[0][0] == "Alice"
        assert rows[1][0] == "Charlie"

    def test_conditional_run_select_multiple_params(self):
        """Test conditional select with multiple parameters."""
        rows = conditional_run_select(
            self.conn, self.cursor, "users", "name", "age > ? AND age < ?", (25, 35)
        )
        assert len(rows) == 1
        assert rows[0][0] == "Alice"

    def test_conditional_run_select_no_results(self):
        """Test conditional select with no matching rows."""
        rows = conditional_run_select(
            self.conn, self.cursor, "users", "name", "age > ?", (100,)
        )
        assert len(rows) == 0

    def test_conditional_run_select_close_conn_after(self):
        """Test that connection closes when close_conn_after=True."""
        rows = conditional_run_select(
            self.conn,
            self.cursor,
            "users",
            "name",
            "age > ?",
            (20,),
            close_conn_after=True,
        )
        assert len(rows) == 3
        with pytest.raises(sqlite3.ProgrammingError):
            self.cursor.execute("SELECT * FROM users")

    def test_conditional_run_select_invalid_table(self):
        """Test that invalid table name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            conditional_run_select(
                self.conn,
                self.cursor,
                "users; DROP TABLE users;--",
                "name",
                "age > ?",
                (18,),
            )

    def test_conditional_run_select_invalid_column(self):
        """Test that invalid column name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            conditional_run_select(
                self.conn,
                self.cursor,
                "users",
                "name; DROP TABLE users;--",
                "age > ?",
                (18,),
            )

    def test_conditional_run_select_sql_injection_condition(self):
        """Test SQL injection attempt via condition parameter (should use params)."""
        # This should work safely because we use parameterized queries
        rows = conditional_run_select(
            self.conn,
            self.cursor,
            "users",
            "name",
            "name = ?",
            ("Alice'; DROP TABLE users;--",),
        )
        # Should not find any user with that name, but table should still exist
        assert len(rows) == 0
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 3

    def test_conditional_run_select_union_injection(self):
        """Test UNION-based SQL injection attempt via table/column."""
        with pytest.raises(EasySqlError):
            conditional_run_select(
                self.conn,
                self.cursor,
                "users UNION SELECT * FROM sqlite_master",
                "name",
                "age > ?",
                (18,),
            )


class TestRunInsert:
    """Tests for run_insert function."""

    def setup_method(self):
        """Create a fresh in-memory database before each test."""
        self.conn, self.cursor = open_db(":memory:")
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER)"
        )
        self.conn.commit()

    def teardown_method(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_run_insert_single_row(self):
        """Test inserting a single row."""
        run_insert(
            self.conn,
            self.cursor,
            ["Alice", "alice@example.com", 30],
            "users",
            ["name", "email", "age"],
        )
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 1
        assert rows[0][1] == "Alice"
        assert rows[0][2] == "alice@example.com"
        assert rows[0][3] == 30

    def test_run_insert_multiple_rows(self):
        """Test inserting multiple rows sequentially."""
        run_insert(
            self.conn,
            self.cursor,
            ["Alice", "alice@example.com", 30],
            "users",
            ["name", "email", "age"],
        )
        run_insert(
            self.conn,
            self.cursor,
            ["Bob", "bob@example.com", 25],
            "users",
            ["name", "email", "age"],
        )
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 2

    def test_run_insert_close_conn_after(self):
        """Test that connection closes when close_conn_after=True."""
        run_insert(
            self.conn,
            self.cursor,
            ["Alice", "alice@example.com", 30],
            "users",
            ["name", "email", "age"],
            close_conn_after=True,
        )
        with pytest.raises(sqlite3.ProgrammingError):
            self.cursor.execute("SELECT * FROM users")

    def test_run_insert_invalid_table_name(self):
        """Test that invalid table name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            run_insert(
                self.conn,
                self.cursor,
                ["Alice", "alice@example.com"],
                "users; DROP TABLE users;--",
                ["name", "email"],
            )

    def test_run_insert_invalid_column_name(self):
        """Test that invalid column name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            run_insert(
                self.conn,
                self.cursor,
                ["Alice", "alice@example.com"],
                "users",
                ["name; DROP TABLE users;--", "email"],
            )

    def test_run_insert_sql_injection_values(self):
        """Test that values are safely parameterized (not interpolated)."""
        # This should be safely inserted as a literal string, not executed as SQL
        malicious_name = "Alice'; DROP TABLE users;--"
        run_insert(
            self.conn,
            self.cursor,
            [malicious_name, "alice@example.com", 30],
            "users",
            ["name", "email", "age"],
        )
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 1
        assert rows[0][1] == malicious_name  # Stored as literal string
        # Table should still exist
        rows2 = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows2) == 1

    def test_run_insert_union_injection_table(self):
        """Test UNION-based SQL injection attempt via table name."""
        with pytest.raises(EasySqlError):
            run_insert(
                self.conn,
                self.cursor,
                ["Alice", "alice@example.com"],
                "users UNION SELECT * FROM sqlite_master",
                ["name", "email"],
            )


class TestRunDelete:
    """Tests for run_delete function."""

    def setup_method(self):
        """Create a fresh in-memory database with test data before each test."""
        self.conn, self.cursor = open_db(":memory:")
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER)"
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Alice", "alice@example.com", 30),
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Bob", "bob@example.com", 25),
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Charlie", "charlie@example.com", 35),
        )
        self.conn.commit()

    def teardown_method(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_run_delete_single_row(self):
        """Test deleting a single row."""
        run_delete(self.conn, self.cursor, "users", "name = ?", ("Alice",))
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 2
        assert rows[0][1] == "Bob"
        assert rows[1][1] == "Charlie"

    def test_run_delete_multiple_rows(self):
        """Test deleting multiple rows matching condition."""
        run_delete(self.conn, self.cursor, "users", "age > ?", (28,))
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 1
        assert rows[0][1] == "Bob"

    def test_run_delete_no_match(self):
        """Test deleting with condition that matches no rows."""
        run_delete(self.conn, self.cursor, "users", "name = ?", ("NonExistent",))
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 3

    def test_run_delete_close_conn_after(self):
        """Test that connection closes when close_conn_after=True."""
        run_delete(
            self.conn,
            self.cursor,
            "users",
            "name = ?",
            ("Alice",),
            close_conn_after=True,
        )
        with pytest.raises(sqlite3.ProgrammingError):
            self.cursor.execute("SELECT * FROM users")

    def test_run_delete_invalid_table_name(self):
        """Test that invalid table name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            run_delete(
                self.conn,
                self.cursor,
                "users; DROP TABLE users;--",
                "name = ?",
                ("Alice",),
            )

    def test_run_delete_sql_injection_condition_params(self):
        """Test that condition values are safely parameterized."""
        malicious_value = "Alice'; DROP TABLE users;--"
        run_delete(self.conn, self.cursor, "users", "name = ?", (malicious_value,))
        # Should not delete anything (no user with that literal name)
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 3

    def test_run_delete_union_injection_table(self):
        """Test UNION-based SQL injection attempt via table name."""
        with pytest.raises(EasySqlError):
            run_delete(
                self.conn,
                self.cursor,
                "users UNION SELECT * FROM sqlite_master",
                "name = ?",
                ("Alice",),
            )


class TestDeleteAllFromTable:
    """Tests for delete_all_from_table function."""

    def setup_method(self):
        """Create a fresh in-memory database with test data before each test."""
        self.conn, self.cursor = open_db(":memory:")
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER)"
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Alice", "alice@example.com", 30),
        )
        self.cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Bob", "bob@example.com", 25),
        )
        self.conn.commit()

    def teardown_method(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_delete_all_from_table(self):
        """Test deleting all rows from a table."""
        delete_all_from_table(self.conn, self.cursor, "users")
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 0

    def test_delete_all_from_table_close_conn_after(self):
        """Test that connection closes when close_conn_after=True."""
        delete_all_from_table(self.conn, self.cursor, "users", close_conn_after=True)
        with pytest.raises(sqlite3.ProgrammingError):
            self.cursor.execute("SELECT * FROM users")

    def test_delete_all_from_table_invalid_table(self):
        """Test that invalid table name raises EasySqlError."""
        with pytest.raises(EasySqlError):
            delete_all_from_table(self.conn, self.cursor, "users; DROP TABLE users;--")

    def test_delete_all_from_table_sql_injection(self):
        """Test SQL injection attempt via table name."""
        with pytest.raises(EasySqlError):
            delete_all_from_table(self.conn, self.cursor, "users; DROP TABLE users;--")
        # Verify table still exists with data
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 2

    def test_delete_all_from_table_union_injection(self):
        """Test UNION-based SQL injection attempt."""
        with pytest.raises(EasySqlError):
            delete_all_from_table(
                self.conn, self.cursor, "users UNION SELECT * FROM sqlite_master"
            )


class TestCheckIfValid:
    """Tests for the internal _check_if_valid helper function."""

    def test_valid_table_name(self):
        from py_simple.easy_sql import _check_if_valid

        assert _check_if_valid("users") is True
        assert _check_if_valid("Users") is True
        assert _check_if_valid("USERS") is True
        assert _check_if_valid("user_data") is True
        assert _check_if_valid("user123") is True
        assert _check_if_valid("_users") is True
        assert _check_if_valid("users_") is True

    def test_valid_column_names(self):
        from py_simple.easy_sql import _check_if_valid

        assert _check_if_valid("name") is True
        assert _check_if_valid("name, email") is True
        assert _check_if_valid("name,email,age") is True
        assert _check_if_valid("name, email, age") is True
        assert _check_if_valid("*") is True

    def test_invalid_sql_keywords(self):
        from py_simple.easy_sql import _check_if_valid

        assert _check_if_valid("SELECT") is False
        assert _check_if_valid("select") is False
        assert _check_if_valid("UNION") is False
        assert _check_if_valid("union") is False
        assert _check_if_valid("DROP") is False
        assert _check_if_valid("drop") is False
        assert _check_if_valid("INSERT") is False
        assert _check_if_valid("DELETE") is False
        assert _check_if_valid("UPDATE") is False
        assert _check_if_valid("ALTER") is False
        assert _check_if_valid("CREATE") is False
        assert _check_if_valid("TRUNCATE") is False

    def test_invalid_special_characters(self):
        from py_simple.easy_sql import _check_if_valid

        assert _check_if_valid("user; DROP TABLE users") is False
        assert _check_if_valid("users--") is False
        assert _check_if_valid("users/*") is False
        assert _check_if_valid("user's") is False
        assert _check_if_valid('user"') is False
        assert _check_if_valid("user@name") is False
        assert _check_if_valid("user-name") is False
        assert _check_if_valid("user.name") is False

    def test_invalid_union_variants(self):
        from py_simple.easy_sql import _check_if_valid

        assert _check_if_valid("users UNION SELECT * FROM sqlite_master") is False
        assert _check_if_valid("users union all select * from sqlite_master") is False
        assert _check_if_valid("users; union select * from sqlite_master") is False

    def test_non_string_input(self):
        from py_simple.easy_sql import _check_if_valid

        assert _check_if_valid(123) is False
        assert _check_if_valid(None) is False
        assert _check_if_valid(["name"]) is False


class TestRunUpdate:
    """Tests for run_update function."""

    def setup_method(self):
        """Create a fresh in-memory database with test data before each test."""
        self.conn, self.cursor = open_db(":memory:")
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        )
        self.cursor.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Ada", 25), ("Grace", 40)],
        )
        self.conn.commit()

    def teardown_method(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_run_update_changes_matching_row(self):
        """Test that run_update only changes the row matching the condition."""
        run_update(self.conn, self.cursor, "users", {"age": 30}, "name = ?", ("Ada",))

        self.cursor.execute("SELECT age FROM users WHERE name = ?", ("Ada",))
        assert self.cursor.fetchone()[0] == 30

        # Grace's row should be untouched
        self.cursor.execute("SELECT age FROM users WHERE name = ?", ("Grace",))
        assert self.cursor.fetchone()[0] == 40

    def test_run_update_multiple_columns(self):
        """Test that run_update can set more than one column at once."""
        run_update(
            self.conn,
            self.cursor,
            "users",
            {"name": "Ada Lovelace", "age": 36},
            "name = ?",
            ("Ada",),
        )

        self.cursor.execute("SELECT name, age FROM users WHERE age = 36")
        row = self.cursor.fetchone()
        assert row == ("Ada Lovelace", 36)

    def test_run_update_invalid_table_name_raises(self):
        """Test that an unsafe table_name raises EasySqlError instead of running."""
        with pytest.raises(EasySqlError):
            run_update(
                self.conn,
                self.cursor,
                "users; DROP TABLE users;",
                {"age": 99},
                "name = ?",
                ("Ada",),
            )

    def test_run_update_invalid_column_name_raises(self):
        """Test that an unsafe column name in updates raises EasySqlError."""
        with pytest.raises(EasySqlError):
            run_update(
                self.conn,
                self.cursor,
                "users",
                {"age; DROP TABLE users;": 99},
                "name = ?",
                ("Ada",),
            )

    def test_run_update_bad_condition_raises(self):
        """Test that a condition referencing a non-existent column surfaces as EasySqlError."""
        with pytest.raises(EasySqlError):
            run_update(
                self.conn,
                self.cursor,
                "users",
                {"age": 99},
                "not_a_real_column = ?",
                ("Ada",),
            )

    def test_run_update_closes_connection_when_requested(self):
        """Test that close_conn_after=True closes the connection after updating."""
        run_update(
            self.conn,
            self.cursor,
            "users",
            {"age": 50},
            "name = ?",
            ("Ada",),
            close_conn_after=True,
        )

        with pytest.raises(sqlite3.ProgrammingError):
            self.conn.execute("SELECT 1")


class TestIntegration:
    """Integration tests combining multiple operations."""

    def setup_method(self):
        """Create a fresh in-memory database before each test."""
        self.conn, self.cursor = open_db(":memory:")
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER)"
        )
        self.conn.commit()

    def teardown_method(self):
        """Close the connection after each test."""
        self.conn.close()

    def test_full_crud_workflow(self):
        """Test a full Create-Read-Update-Delete workflow."""
        # Create
        run_insert(
            self.conn,
            self.cursor,
            ["Alice", "alice@example.com", 30],
            "users",
            ["name", "email", "age"],
        )
        run_insert(
            self.conn,
            self.cursor,
            ["Bob", "bob@example.com", 25],
            "users",
            ["name", "email", "age"],
        )

        # Read
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 2

        # Read with condition
        rows = conditional_run_select(
            self.conn, self.cursor, "users", "name, age", "age > ?", (28,)
        )
        assert len(rows) == 1
        assert rows[0][0] == "Alice"

        # Update
        run_update(
            self.conn,
            self.cursor,
            "users",
            {"age": 31},
            "name = ?",
            ("Alice",),
        )
        rows = conditional_run_select(
            self.conn, self.cursor, "users", "name, age", "age > ?", (28,)
        )
        assert rows[0][1] == 31

        # Delete
        run_delete(self.conn, self.cursor, "users", "name = ?", ("Alice",))
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 1
        assert rows[0][1] == "Bob"

        # Delete all
        delete_all_from_table(self.conn, self.cursor, "users")
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 0

    def test_sql_injection_resilience_full_workflow(self):
        """Test that SQL injection attempts fail at every step."""
        # Try to inject via table name in insert
        with pytest.raises(EasySqlError):
            run_insert(
                self.conn,
                self.cursor,
                ["test", "test@test.com"],
                "users; DROP TABLE users;--",
                ["name", "email"],
            )

        # Normal insert should still work
        run_insert(
            self.conn,
            self.cursor,
            ["Alice", "alice@example.com"],
            "users",
            ["name", "email"],
        )

        # Try to inject via table name in select
        with pytest.raises(EasySqlError):
            run_select(self.conn, self.cursor, "users; DROP TABLE users;--", "*")

        # Normal select should still work
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 1

        # Try to inject via condition in conditional select
        rows = conditional_run_select(
            self.conn,
            self.cursor,
            "users",
            "name",
            "name = ?",
            ("Alice'; DROP TABLE users;--",),
        )
        assert len(rows) == 0  # No match, but table intact

        # Try to inject via table name in delete
        with pytest.raises(EasySqlError):
            run_delete(
                self.conn,
                self.cursor,
                "users; DROP TABLE users;--",
                "name = ?",
                ("Alice",),
            )

        # Normal delete should still work
        run_delete(self.conn, self.cursor, "users", "name = ?", ("Alice",))
        rows = run_select(self.conn, self.cursor, "users", "*")
        assert len(rows) == 0

        # Table should still exist (just empty)
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        assert len(rows) == 0
