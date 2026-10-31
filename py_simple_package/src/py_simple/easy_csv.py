"""
easy_csv is built to simplify reading and writing CSV files.
"""

import csv
import io
import os.path
from decimal import Decimal, InvalidOperation
from collections.abc import Generator
from typing import Any
import tempfile


def merge_csv_files(
    filepaths: list[str], output_filepath: str, delimiter: str = ","
) -> None:
    """
    Combines CSV files with matching headers into one file in input order.

    Reads UTF-8 files one record at a time and writes the header only once.
    Header names and their order must match exactly. Header-only files are
    accepted; empty files or files with a blank first record are rejected.
    Data records are copied without changing their field count or values.

    Writes to a temporary file beside the output, then replaces the output
    only after all inputs succeed. Inputs and any existing output are left
    unchanged on failure. The output must not refer to an input, including
    through a symbolic or hard link. An unrelated output symlink is replaced
    itself, leaving its target unchanged. File metadata is not copied.

    Args:
        filepaths (list[str]): Non-empty list of input paths, in merge order.
        output_filepath (str): Destination path; its parent must exist.
        delimiter (str): Field delimiter for all files (default is comma).

    Raises:
        ValueError: If there are no inputs, an input has no header, headers
            differ, or the output refers to an input.
        OSError: If a file cannot be read, written or replaced.
        UnicodeError: If an input cannot be decoded as UTF-8.
        csv.Error: If CSV parsing fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import merge_csv_files

            merge_csv_files(["january.csv", "february.csv"], "combined.csv")
            ```

        === "The Traditional Way"
            ```python
            import csv
            import os
            import tempfile

            inputs = ["january.csv", "february.csv"]
            output = "combined.csv"
            if not inputs:
                raise ValueError("At least one input is required")
            for path in inputs:
                if os.path.realpath(path) == os.path.realpath(output) or (
                    os.path.exists(output) and os.path.samefile(path, output)
                ):
                    raise ValueError("Output must not be an input")

            temporary_path = None
            try:
                with tempfile.NamedTemporaryFile(
                    "w", newline="", encoding="utf-8", delete=False,
                    dir=os.path.dirname(os.path.abspath(output))
                ) as temporary:
                    temporary_path = temporary.name
                    writer = csv.writer(temporary)
                    header = None
                    for path in inputs:
                        with open(path, newline="", encoding="utf-8") as source:
                            reader = csv.reader(source, strict=True)
                            current = next(reader, None)
                            if not current:
                                raise ValueError(f"File has no header: {path}")
                            if header is None:
                                header = current
                                writer.writerow(header)
                            elif current != header:
                                raise ValueError(f"Headers do not match: {path}")
                            writer.writerows(reader)
                os.replace(temporary_path, output)
            finally:
                if temporary_path is not None and os.path.exists(temporary_path):
                    os.remove(temporary_path)
            ```
    """
    if not filepaths:
        raise ValueError("At least one input CSV file is required")

    for filepath in filepaths:
        if os.path.realpath(filepath) == os.path.realpath(output_filepath) or (
            os.path.exists(output_filepath)
            and os.path.samefile(filepath, output_filepath)
        ):
            raise ValueError(f"Output must not refer to an input file: {filepath}")

    temp_filepath = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            newline="",
            encoding="utf-8",
            delete=False,
            dir=os.path.dirname(os.path.abspath(output_filepath)),
        ) as temp_file:
            temp_filepath = temp_file.name
            writer = csv.writer(temp_file, delimiter=delimiter)
            headers = None
            for filepath in filepaths:
                with open(filepath, newline="", encoding="utf-8") as source:
                    reader = csv.reader(source, delimiter=delimiter, strict=True)
                    current = next(reader, None)
                    if not current:
                        raise ValueError(f"File has no header: {filepath}")
                    if headers is None:
                        headers = current
                        writer.writerow(headers)
                    elif current != headers:
                        raise ValueError(
                            f"Headers do not match in {filepath}: "
                            f"expected {headers!r}, got {current!r}"
                        )
                    writer.writerows(reader)
        os.replace(temp_filepath, output_filepath)
    finally:
        if temp_filepath is not None and os.path.exists(temp_filepath):
            os.remove(temp_filepath)


def iter_csv_rows(
    filepath: str,
    return_dict: bool = True,
    delimiter: str = ",",
) -> Generator[dict[str, str] | list[str], None, None]:
    """
    Returns CSV rows one at a time without loading the whole file into memory.

    Args:
        filepath (str): Path to a UTF-8 CSV file.
        return_dict (bool): Use the first row as dictionary keys (default True).
            If False, yield lists including the header, like read_csv_to_list.
        delimiter (str): Field separator (default comma).

    Returns:
        Iterator: Rows such as {'Name': 'Alice', 'Age': '24'}.

    Raises:
        FileNotFoundError: When iteration begins and the file does not exist.
        ValueError: When iteration begins and the file is empty.

    The file opens on the first iteration and closes on exhaustion. If you
    stop early, call the iterator's close() method to release it immediately.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple.easy_csv import iter_csv_rows

            for person in iter_csv_rows("people.csv"):
                print(person["Name"])
            ```

        === "The Traditional Way"
            ```python
            import csv

            with open("people.csv", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    person = dict(zip(headers, row))
                    print(person["Name"])
            ```
    """
    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=delimiter)
        try:
            first = next(reader)
        except StopIteration:
            raise ValueError(f"File is empty: {filepath}") from None
        if return_dict:
            for row in reader:
                yield dict(zip(first, row))
        else:
            yield first
            yield from reader


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


def sort_csv_by_column(
    filepath: str,
    column: str,
    reverse: bool = False,
    output_filepath: str | None = None,
    delimiter: str = ",",
) -> None:
    """
    Sort a CSV file based on a specific column.

    Args:
        filepath (str): Path to the CSV file.
        column (str): Column name to sort by. For mixed data, values are
            sorted numerically first, followed by non-numeric strings
            and empty cells. Numeric comparisons preserve decimal precision;
            NaN values are treated as non-numeric strings.
        reverse (bool): If True, sorts in descending order.
            For mixed data, this reverses the grouping.
        output_filepath (str | None): Output path. If None, overwrites
            the source file.
        delimiter (str): Field delimiter (default is comma).

    Raises:
        ValueError: If the file is empty, contains no data rows,
            or the column is not found.
    """
    data = read_csv_to_list(filepath, return_dict=True, delimiter=delimiter)

    if not data:
        raise ValueError(f"No data rows to sort in file: {filepath}")

    if column not in data[0]:
        raise ValueError(f"Column not found: {column}")

    def sort_key(row: dict[str, Any]) -> Any:
        val = row.get(column, "") or ""
        try:
            number = Decimal(val)
        except InvalidOperation:
            return (1, Decimal(0), val)
        if number.is_nan():
            return (1, Decimal(0), val)
        return (0, number, "")

    sorted_data = sorted(data, key=sort_key, reverse=reverse)

    save_path = output_filepath if output_filepath else filepath
    write_csv_from_list(save_path, data=sorted_data, delimiter=delimiter)


def append_row_to_csv(
    filepath: str,
    row: dict[str, Any] | list[Any],
    delimiter: str = ",",
) -> None:
    """
    Append a single row (as a dictionary or list) to an existing CSV file.

    Adds a record separator first if the existing file has no final newline.
    Existing contents are preserved. CSV serialization errors are raised
    before changing the file.

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

    # Validate and serialize before changing the existing file.
    buffer = io.StringIO(newline="")
    if isinstance(row, dict):
        writer = csv.DictWriter(buffer, fieldnames=headers, delimiter=delimiter)
    else:
        writer = csv.writer(buffer, delimiter=delimiter)
    writer.writerow(row)

    with open(filepath, "rb") as source:
        source.seek(-1, os.SEEK_END)
        needs_newline = source.read(1) not in (b"\n", b"\r")

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        if needs_newline:
            f.write("\r\n")
        f.write(buffer.getvalue())


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

            with open("people.csv", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                names = [row["Name"] for row in reader]
            print(names)  # ['Alice', 'Bob', 'Carol']
            ```
    """
    path = filepath if filepath is not None else file_path
    col = column if column is not None else column_name

    if path is None:
        raise TypeError(
            "read_csv_column() missing required argument: 'filepath' or 'file_path'"
        )
    if col is None:
        raise TypeError(
            "read_csv_column() missing required argument: 'column' or 'column_name'"
        )

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


def drop_empty_csv_rows(filepath: str, delimiter: str = ",") -> int:
    """
    Remove rows whose cells are all blank and rewrite the CSV in place.

    The header row is always kept. A cell that contains only spaces
    counts as blank.

    Args:
        filepath (str): Path to the CSV file.
        delimiter (str): Field delimiter (default is comma).

    Returns:
        int: How many data rows were removed.

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        ValueError: If the file is empty.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import drop_empty_csv_rows

            removed = drop_empty_csv_rows("people.csv")
            print(removed)  # 2
            ```

        === "The Traditional Way"
            ```python
            import csv

            with open("people.csv", newline="", encoding="utf-8") as f:
                rows = list(csv.reader(f))
            header, data = rows[0], rows[1:]
            kept = [row for row in data if any(cell.strip() for cell in row)]
            with open("people.csv", "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows([header, *kept])
            ```
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter=delimiter))

    if not rows:
        raise ValueError(f"File is empty: {filepath}")

    header, data_rows = rows[0], rows[1:]
    kept = [row for row in data_rows if any(cell.strip() for cell in row)]
    removed = len(data_rows) - len(kept)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(header)
        writer.writerows(kept)

    return removed


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
