"""
easy_csv is built to simplify reading and writing CSV files.
"""

import csv
import os.path
from typing import Any


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
