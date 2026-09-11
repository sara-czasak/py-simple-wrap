"""
easy_file_manager is meant to simplify working with files.
"""

import os
import shutil

VALID_EXTENSIONS = ["txt", "md", "log", "csv"]


class EasyFileManagerError(Exception):
    """
    Raised when a file operation cannot be completed.
    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _is_valid_extension(extension):
    """Check if extension is valid"""
    return extension in VALID_EXTENSIONS


def _get_extension(filename: str) -> str:
    """Extract the lowercased extension from a filename."""
    return filename.split(".")[-1].lower()


def is_file_there(filename: str) -> bool:
    """
    Check if file exists in current working directory.

    Args:
        filename (str): Name of the file to be checked.

    Returns:
        bool: True if file exists, False otherwise.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_file_there

            exists = is_file_there("new_file.txt")
            ```

        === "The Traditional Way"
            ```python
            import os

            exists = os.path.isfile("new_file.txt")
            ```
    """
    return os.path.isfile(filename)


def make_blank_file(filename: str, file_extension: str):
    """
    Creates a blank file in current working directory.
        Raises EasyFileManagerError if the file already exists.

    Args:
        filename (str): The name of the file to be created.
        file_extension (str): The extension without '.'.
            Allowed: ['txt', 'csv', 'md', 'log']

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import make_blank_file

            make_blank_file("new_file", "txt")
            ```

        === "The Traditional Way"
            ```python
            import os

            filename = "new_file.txt"
            if not os.path.isfile(filename):
                with open(filename, "w", encoding="utf-8"):
                    pass
            ```
    """
    if _is_valid_extension(file_extension.lower()):
        file = f"{filename}.{file_extension.lower()}"
        if is_file_there(file):
            raise EasyFileManagerError(
                f"\n\n\nERROR: File {file} already exists in current working directory."
            )
        with open(file, "w", encoding="utf-8"):
            pass
    else:
        raise EasyFileManagerError(
            f"\n\n\n'ERROR: '{file_extension} is not a valid extension.\n"
            f"Please enter a valid extension and try again.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )


def add_a_line(filename: str, line: str):
    """
    Add line to existing file. If file does not exist, create it.

    Args:
        filename (str): File to write to.
        line (str): Line to write.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import add_a_line

            add_a_line("new_file.txt", "hello world!")
            ```

        === "The Traditional Way"
            ```python
            with open("new_file.txt", "a", encoding="utf-8") as f:
                f.write("hello world!" + "\\n")
            ```
    """
    ext = _get_extension(filename)
    if _is_valid_extension(ext):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    else:
        raise EasyFileManagerError(
            f"\n\n\n'{ext}' is not a valid extension.\n"
            f"Please enter a valid extension and try again.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )


def read_file_to_list(filename: str) -> list:
    """
    Reads lines of existing file to list.

    Args:
        filename (str): File to read from.

    Returns:
        list: List of lines.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import read_file_to_list

            lines = read_file_to_list("new_file.txt")
            ```

        === "The Traditional Way"
            ```python
            try:
                with open("new_file.txt", "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f.readlines()]
            except FileNotFoundError:
                lines = []
            ```
    """
    ext = _get_extension(filename)
    if _is_valid_extension(ext):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return [line.strip() for line in f]
        except FileNotFoundError as e:
            raise EasyFileManagerError(f"\n\n\nERROR: {e}") from None
    else:
        raise EasyFileManagerError(
            f"\n\n\nERROR: '{ext}' is not a valid extension.\n"
            f"Please enter a valid extension and try again.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )


def remove_file(filename: str):
    """
    Removes file from current working directory.

    Args:
        filename (str): File to delete.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import remove_file

            remove_file("new_file.txt")
            ```

        === "The Traditional Way"
            ```python
            import os

            filename = "new_file.txt"
            if os.path.isfile(filename):
                os.remove(filename)
            ```
    """
    ext = _get_extension(filename)
    if _is_valid_extension(ext):
        if is_file_there(filename):
            os.remove(filename)
        else:
            raise EasyFileManagerError(f"\n\n\nERROR: File {filename} does not exist!")
    else:
        raise EasyFileManagerError(
            f"\n\n\nERROR: '{ext}' is not a valid extension.\n"
            f"Please enter a valid extension and try again.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )


def rename_file(old_name: str, new_name: str):
    """
    Rename file in the current working directory.

    Args:
        old_name (str): Current filename.
        new_name (str): New filename.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import rename_file

            rename_file("old_name.txt", "new_name.txt")
            ```

        === "The Traditional Way"
            ```python
            import os

            old_name, new_name = "old_name.txt", "new_name.txt"
            if os.path.isfile(old_name) and not os.path.isfile(new_name):
                os.rename(old_name, new_name)
            ```
    """
    ext_old = _get_extension(old_name)
    ext_new = _get_extension(new_name)
    if _is_valid_extension(ext_old) and _is_valid_extension(ext_new):
        if is_file_there(old_name):
            if not is_file_there(new_name):
                os.rename(old_name, new_name)
            else:
                raise EasyFileManagerError(
                    f"\n\n\nERROR: File '{new_name}'"
                    f" already exists in current "
                    f"working directory."
                )
        else:
            raise EasyFileManagerError(
                f"\n\n\nERROR: File {old_name} does "
                f"not exist in current working "
                f"directory."
            )
    else:
        raise EasyFileManagerError(
            f"\n\n\nERROR: '{ext_old}' or '{ext_new}' is not a valid "
            f"extension.\n"
            f"Please enter a valid extension and try again.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )


def list_files(extension: str | None = None) -> list:
    """
    List files in the current working directory that have valid extensions.
    Optionally filter by a specific extension.

    Args:
        extension (str, optional): Filter by extension (e.g., 'txt').
            If None, all valid extension files are listed.

    Returns:
        list: Sorted list of filenames matching the filter.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import list_files

            all_valid = list_files()
            txt_only = list_files("txt")
            ```

        === "The Traditional Way"
            ```python
            import os

            valid_extensions = ["txt", "md", "log", "csv"]
            matches = [
                f for f in os.listdir(".")
                if os.path.isfile(f) and f.split(".")[-1].lower()
                in valid_extensions
            ]
            matches.sort()
            ```
    """
    if extension is not None and not _is_valid_extension(extension.lower()):
        raise EasyFileManagerError(
            f"\n\n\nERROR:'{extension}' is not a valid extension.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )

    matches = []
    for fname in os.listdir("."):
        if os.path.isfile(fname):
            ext = _get_extension(fname)
            if _is_valid_extension(ext):
                if extension is None or ext == extension.lower():
                    matches.append(fname)
    return sorted(matches)


def copy_file(source: str, destination: str):
    """
    Copy a file to a new location or name.

    Args:
        source (str): File to copy.
        destination (str): Destination path or filename.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import copy_file

            copy_file("notes.txt", "notes_backup.txt")
            ```

        === "The Traditional Way"
            ```python
            import os
            import shutil

            source, destination = "notes.txt", "notes_backup.txt"
            if os.path.isfile(source) and not os.path.isfile(destination):
                shutil.copy2(source, destination)
            ```
    """
    ext_src = _get_extension(source)
    ext_dst = _get_extension(destination)
    if not _is_valid_extension(ext_src):
        raise EasyFileManagerError(
            f"\n\n\nERROR: '{ext_src}' is not a valid extension.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )
    if not _is_valid_extension(ext_dst):
        raise EasyFileManagerError(
            f"\n\n\nERROR: '{ext_dst}' is not a valid extension.\n"
            f"\nVALID EXTENSIONS: {VALID_EXTENSIONS}"
        )
    if not is_file_there(source):
        raise EasyFileManagerError(f"\n\n\nERROR: File '{source}' does not exist.")
    if is_file_there(destination):
        raise EasyFileManagerError(
            f"\n\n\nERROR: File '{destination}' already exists — not overwriting."
        )
    shutil.copy2(source, destination)
