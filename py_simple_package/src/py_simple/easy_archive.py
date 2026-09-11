"""
easy_archive is meant to simplify zipping and unzipping files and folders.
"""

import os
import zipfile


class EasyArchiveError(Exception):
    """
    Raised when an archive operation cannot be completed.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _ensure_zip_extension(zip_name: str) -> str:
    """Raise EasyArchiveError unless zip_name ends in '.zip'."""
    if not zip_name.lower().endswith(".zip"):
        raise EasyArchiveError(
            f"\n'{zip_name}' does not end in '.zip'.\n"
            f"easy_archive only works with .zip files."
        )
    return zip_name


def zip_folder(folder_path: str, zip_name: str | None = None) -> str:
    """
    Zips an entire folder (including subfolders) into a single .zip file.

    Args:
        folder_path (str): Path to the folder to zip.
        zip_name (str, optional): Name/path for the resulting zip file.
            Defaults to the folder's own name with '.zip' appended.

    Returns:
        str: Path to the created zip file.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import zip_folder

            zip_folder("my_project")  # -> 'my_project.zip'
            ```

        === "The Traditional Way"
            ```python
            import os
            import zipfile

            folder_path = "my_project"
            zip_name = "my_project.zip"
            with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, folder_path)
                        zf.write(full_path, arcname)
            ```
    """
    if not os.path.isdir(folder_path):
        raise EasyArchiveError(
            f"\n\n\nERROR: Folder '{folder_path}' does not exist."
        ) from None

    if zip_name is None:
        folder_name = os.path.basename(os.path.abspath(folder_path)) or "folder"
        zip_name = folder_name + ".zip"
    _ensure_zip_extension(zip_name)

    zip_abspath = os.path.abspath(zip_name)

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                if os.path.abspath(full_path) == zip_abspath:
                    continue
                arcname = os.path.relpath(full_path, folder_path)
                zf.write(full_path, arcname)

    return zip_name


def zip_files(file_paths: list, zip_name: str) -> str:
    """
    Zips a list of individual files into a single .zip archive.
    If two files share the same filename (e.g. from different
    folders), the later one is automatically renamed inside the
    archive instead of silently overwriting the first.

    Args:
        file_paths (list): Paths of the files to include.
        zip_name (str): Name/path for the resulting zip file.
            Must end in '.zip'.

    Returns:
        str: Path to the created zip file.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import zip_files

            zip_files(["notes.txt", "todo.md"], "backup.zip")
            ```

        === "The Traditional Way"
            ```python
            import os
            import zipfile

            file_paths = ["notes.txt", "todo.md"]
            with zipfile.ZipFile("backup.zip", "w", zipfile.ZIP_DEFLATED) as zf:
                for path in file_paths:
                    if os.path.isfile(path):
                        zf.write(path, os.path.basename(path))
            ```
    """
    _ensure_zip_extension(zip_name)

    existing = [p for p in file_paths if os.path.isfile(p)]
    missing = [p for p in file_paths if not os.path.isfile(p)]
    if missing:
        raise EasyArchiveError(f"\n\n\nERROR: File '{missing[0]}' does not exist.")

    if not existing:
        raise EasyArchiveError("\n\n\nERROR: No valid files to zip.") from None

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        used_names = set()
        for path in existing:
            arcname = os.path.basename(path)
            if arcname in used_names:
                stem, ext = os.path.splitext(arcname)
                parent = (
                    os.path.basename(os.path.dirname(os.path.abspath(path))) or "file"
                )
                candidate = f"{stem}_{parent}{ext}"
                counter = 2
                while candidate in used_names:
                    candidate = f"{stem}_{parent}_{counter}{ext}"
                    counter += 1
                print(
                    f"'{arcname}' already added from another folder — "
                    f"'{path}' will be stored as '{candidate}' instead."
                )
                arcname = candidate
            used_names.add(arcname)
            zf.write(path, arcname)

    return zip_name


def unzip_file(zip_path: str, destination: str = ".") -> str:
    """
    Extracts every file in a .zip archive into a destination folder.
    The destination folder is created automatically if it doesn't exist.

    Args:
        zip_path (str): Path to the .zip file to extract.
        destination (str): Folder to extract into. Defaults to the
            current working directory.

    Returns:
        str: The destination folder path.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import unzip_file

            unzip_file("backup.zip", "restored")
            ```

        === "The Traditional Way"
            ```python
            import os
            import zipfile

            zip_path, destination = "backup.zip", "restored"
            os.makedirs(destination, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(destination)
            ```
    """
    if not os.path.isfile(zip_path):
        raise EasyArchiveError(
            f"\n\n\nERROR: Zip file '{zip_path}' does not exist."
        ) from None

    if not zipfile.is_zipfile(zip_path):
        raise EasyArchiveError(
            f"\n\n\nERROR: '{zip_path}' is not a valid zip file."
        ) from None

    if os.path.isfile(destination):
        raise EasyArchiveError(
            f"\n\n\nERROR: '{destination}' already exists as a file, not a folder."
        ) from None

    os.makedirs(destination, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(destination)

    return destination


def list_zip_contents(zip_path: str) -> list:
    """
    Lists the files inside a .zip archive without extracting them.

    Args:
        zip_path (str): Path to the .zip file to inspect.

    Returns:
        list: Filenames stored in the archive.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import list_zip_contents

            contents = list_zip_contents("backup.zip")
            ```

        === "The Traditional Way"
            ```python
            import zipfile

            with zipfile.ZipFile("backup.zip", "r") as zf:
                contents = zf.namelist()
            ```
    """
    if not os.path.isfile(zip_path):
        raise EasyArchiveError(
            f"\n\n\nERROR: Zip file '{zip_path}' does not exist."
        ) from None

    if not zipfile.is_zipfile(zip_path):
        raise EasyArchiveError(
            f"\n\n\nERROR: '{zip_path}' is not a valid zip file."
        ) from None

    with zipfile.ZipFile(zip_path, "r") as zf:
        return zf.namelist()


def add_to_zip(zip_path: str, file_to_add: str) -> bool:
    """
    Adds a single file to an existing .zip archive.

    Args:
        zip_path (str): Path to the existing .zip file.
        file_to_add (str): Path of the file to add to the archive.

    Returns:
        bool: True if the file was added.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import add_to_zip

            add_to_zip("backup.zip", "extra_notes.txt")
            ```

        === "The Traditional Way"
            ```python
            import zipfile

            with zipfile.ZipFile("backup.zip", "a", zipfile.ZIP_DEFLATED) as zf:
                zf.write("extra_notes.txt")
            ```
    """
    if not os.path.isfile(zip_path):
        raise EasyArchiveError(
            f"\n\n\nERROR: Zip file '{zip_path}' does not exist."
        ) from None

    if not zipfile.is_zipfile(zip_path):
        raise EasyArchiveError(
            f"\n\n\nERROR: '{zip_path}' is not a valid zip file."
        ) from None

    if not os.path.isfile(file_to_add):
        raise EasyArchiveError(
            f"\n\n\nERROR: File '{file_to_add}' does not exist."
        ) from None

    with zipfile.ZipFile(zip_path, "a", zipfile.ZIP_DEFLATED) as zf:
        zf.write(file_to_add, os.path.basename(file_to_add))

    return True


def is_zip_file(path: str) -> bool:
    """
    Checks whether a given path is a valid zip archive.

    Args:
        path (str): Path to check.

    Returns:
        bool: True if path exists and is a valid zip file, False
            otherwise (including when the path doesn't exist).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import is_zip_file

            is_zip_file("backup.zip")  # -> True
            ```

        === "The Traditional Way"
            ```python
            import zipfile

            zipfile.is_zipfile("backup.zip")
            ```
    """
    return zipfile.is_zipfile(path)
