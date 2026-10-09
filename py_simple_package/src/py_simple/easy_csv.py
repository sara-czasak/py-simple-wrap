"""
easy_csv is built to simplify reading and writing CSV files.
"""

import csv
import os.path
from typing import Any
import tempfile


def read_csv_to_list(
    filepath: str,
    return_dict: bool = True,
    delimiter: str = ",",
) -> list[dict[str, Any]] | list[list[Any]]:
    """
    Read a CSV file and return its contents
    Args:
        filepath (str): The path to the CSV file.
        return_dict (bool): If True, return list of dicts (keys are headers).
        delimiter (str): Field delimiter (default is comma).

    Returns:
        list: Rows as dicts (if return_dict=True) or lists.

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        ValueError: If the file is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import read_csv_to_list

            data = read_csv_to_list(filepath="people.csv")
            print(data[0])  # {'Name': 'Alice', 'Age': '24'}

            rows = read_csv_to_list(filepath="people.csv", return_dict=False)
            print(rows[0])  # ['Alice','24']
            ```

        === "The Traditional Way"
            ```python
            import csv

            with open("people.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
            headers = rows[0]
            data = [dict(zip(headers, row)) for row in rows[1:]]
            print(data[0])  # {'Name': 'Alice', 'Age': '24'}

            with open("people.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
            print(rows[1])  # ['Alice', '24']  # 0 is a header row
            ```
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        raise ValueError(f"File is empty: {filepath}")

    if not return_dict:
        return rows

    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:]]


def write_csv_from_list(
    filepath: str,
    data: list[dict[str, Any]] | list[list[Any]],
    headers: list[str] | None = None,
    delimiter: str = ",",
) -> None:
    """
    Write data to a CSV file.

    Args:
        filepath (str): Output path.
        data (list): List of dicts or list of lists.
        headers (list): Column names. Required if data is list of lists
                        and you want headers. If data is dict, keys are used.
        delimiter (str): Field delimiter (default is comma).

    Raises:
        ValueError: If data is empty or invalid.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import write_csv_from_list

            people = [
                {"Name": "Alice", "Age": "24"},
                {"Name": "Bob", "Age": "31"},
            ]
            write_csv_from_list(filepath="people.csv", data=people)
            ```

        === "The Traditional Way"
            ```python
            import csv

            people = [
                {"Name": "Alice", "Age": "24"},
                {"Name": "Bob", "Age": "31"},
            ]
            headers = list(people[0].keys())
            with open("people.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(people)
            ```
    """
    if not data:
        raise ValueError("Data cannot be empty")

    is_dict = isinstance(data[0], dict)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        if is_dict:
            if headers is None:
                headers = list(data[0].keys())
            writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
        else:
            writer = csv.writer(f, delimiter=delimiter)
            if headers:
                writer.writerow(headers)
            writer.writerows(data)


def get_csv_columns(
    filepath: str,
    delimiter: str = ",",
) -> list[str]:
    """
    Retrieve a CSV column names (headers) from a CSV file.

    Args:
        filepath (str): Path to the CSV file.
        delimiter (str): Field delimiter (default is comma).

    Returns:
        list: Column names.

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        ValueError: If the file is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_csv_columns

            columns = get_csv_columns(filepath="people.csv")
            print(columns)  # ['Name', 'Age']
            ```

        === "The Traditional Way"
            ```python
            import csv

            with open("people.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                columns = next(reader)
            print(columns)  # ['Name', 'Age']
            ```
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError(f"File is empty: {filepath}")
    return headers


def count_csv_rows(
    filepath: str,
    include_header: bool = False,
    delimiter: str = ",",
) -> int:
    """
    Count rows in a CSV file.

    Args:
        filepath (str): Path to the CSV file.
        include_header (bool): If True, include the header row in the count.
        delimiter (str): Field delimiter (default is comma).

    Returns:
        int: Number of rows in the CSV file.

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        ValueError: If the file is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import count_csv_rows

            row_count = count_csv_rows(filepath="people.csv")
            print(row_count)  # 3
            ```

        === "The Traditional Way"
            ```python
            import csv

            with open("people.csv", "r", newline="", encoding="utf-8") as f:
                row_count = sum(1 for _ in csv.reader(f)) - 1
            print(row_count)  # 3
            ```
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        row_count = sum(1 for _ in csv.reader(f, delimiter=delimiter))

    if row_count == 0:
        raise ValueError(f"File is empty: {filepath}")

    if include_header:
        return row_count

    return max(row_count - 1, 0)


def filter_csv_rows(
    filepath: str,
    column: str,
    value: str,
    return_dict: bool = True,
    delimiter: str = ",",
) -> list[dict[str, Any]] | list[list[Any]]:
    """
    Filter rows where a specific column equals the given value.

    Args:
        filepath (str): Path to the CSV file.
        column (str): Column name to filter on.
        value (str): Value to match.
        return_dict (bool): Whether to return dicts or lists (see read_csv_to_list).
        delimiter (str): Field delimiter (default is comma).

    Returns:
        list: Filtered rows (dicts or lists).

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        ValueError: If the column is not found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import filter_csv_rows

            data = filter_csv_rows(filepath="people.csv", column="Name", value="Alice")
            print(data)  # [{'Name': 'Alice', 'Age': '24'}]
            ```

        === "The Traditional Way"
            ```python
            import csv

            with open("people.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = [row for row in reader if row["Name"] == "Alice"]
            print(data)  # [{'Name': 'Alice', 'Age': '24'}]
            ```
    """
    if not (
        all_rows := read_csv_to_list(filepath, return_dict=True, delimiter=delimiter)
    ):
        return []

    if column not in all_rows[0]:
        raise ValueError(f"Column not found: {column}")

    filtered = [row for row in all_rows if row.get(column) == value]

    if return_dict:
        return filtered

    headers = list(all_rows[0].keys())
    return [[row[h] for h in headers] for row in filtered]

def append_row_to_csv(
    filepath: str,
    row: dict[str, Any] | list[Any],
    delimiter: str = ",",
) -> None:
    """
    Append a single row (as a dictionary or list) to an existing CSV file.

    Args:
        filepath (str): Path to the CSV file.
        row (dict or list): The row data to append.
        delimiter (str): Field delimiter (default is comma).

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        ValueError: If the file is empty.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    headers = get_csv_columns(filepath, delimiter=delimiter)
    if not headers:
        raise ValueError(f"File is empty: {filepath}")

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        if isinstance(row, dict):
            writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
            writer.writerow(row)
        else:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(row)


def read_csv_column(
    filepath: str | None = None,
    column: str | None = None,
    delimiter: str = ",",
    *,
    file_path: str | None = None,
    column_name: str | None = None,
) -> list[str]:
    """
    Read all values from a specific column in a CSV file.

    Args:
        filepath (str): Path to the CSV file. Also accepts file_path as alias.
        column (str): Column name to extract. Also accepts column_name as alias.
        delimiter (str): Field delimiter (default is comma).
        file_path (str, optional): Keyword alias for filepath.
        column_name (str, optional): Keyword alias for column.

    Returns:
        list: Values from the specified column.

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        ValueError: If the file is empty or if the column is not found.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import read_csv_column

            names = read_csv_column(filepath="people.csv", column="Name")
            print(names)  # ['Alice', 'Bob', 'Carol']
            ```

        === "The Traditional Way"
            ```python
            import csv

            with open("people.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                names = [row["Name"] for row in reader]
            print(names)  # ['Alice', 'Bob', 'Carol']
            ```
    """
    path = filepath if filepath is not None else file_path
    col = column if column is not None else column_name

    if path is None:
        raise TypeError("read_csv_column() missing required argument: 'filepath' or 'file_path'")
    if col is None:
        raise TypeError("read_csv_column() missing required argument: 'column' or 'column_name'")

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        
        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError(f"File is empty: {path}")

        if col not in headers:
            raise ValueError(f"Column not found: {col}")

        col_index = headers.index(col)
        return [row[col_index] if len(row) > col_index else "" for row in reader]

 
def delete_csv_rows(
    filepath: str,
    column: str,
    value: str,
    delimiter: str = ",",
) -> None:
    """
    Deletes rows from a CSV file where a column matches the given value.

    Args:
        filepath (str): The path to the CSV file.
        column (str): The column to check for the given value.
        value (str): The value used to find rows to delete.
        delimiter (str): The field delimiter. Defaults to a comma.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the file is empty, the column does not exist,
            or no row matches the given value.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import delete_csv_rows

            delete_csv_rows(
                filepath="people.csv",
                column="Name",
                value="Alice"
            )
            ```

        === "The Traditional Way"
            ```python
            import csv
            import os
            import tempfile

            with open("people.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            rows = [row for row in rows if row["Name"] != "Alice"]

            with open("people.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            ```
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        if reader.fieldnames is None:
            raise ValueError(f"File is empty: {filepath}")

        if column not in reader.fieldnames:
            raise ValueError(f"Column not found: {column}")

        found = False
        with tempfile.NamedTemporaryFile(
            "w",
            newline="",
            encoding="utf-8",
            delete=False,
            dir=os.path.dirname(os.path.abspath(filepath)),
        ) as temp_file:
            temp_filepath = temp_file.name
            writer = csv.DictWriter(
                temp_file, fieldnames=reader.fieldnames, delimiter=delimiter
            )
            writer.writeheader()

            for row in reader:
                if row[column] == value:
                    found = True
                else:
                    writer.writerow(row)

    if not found:
        os.remove(temp_filepath)
        raise ValueError(f"No rows found with {column}={value} in {filepath}")

    os.replace(temp_filepath, filepath)
