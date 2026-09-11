"""Tests for easy_file_manager module."""

import os
import tempfile

import pytest

from py_simple_package.src.py_simple.easy_file_manager import (
    VALID_EXTENSIONS,
    EasyFileManagerError,
    add_a_line,
    copy_file,
    is_file_there,
    list_files,
    make_blank_file,
    read_file_to_list,
    remove_file,
    rename_file,
)


@pytest.fixture
def tmp_workdir():
    """Change to a temp directory for file operations, then clean up."""
    original_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            yield tmpdir
        finally:
            os.chdir(original_cwd)


class TestMakeBlankFile:
    """Tests for make_blank_file function."""

    def test_creates_file(self, tmp_workdir):
        """Should create a blank file."""
        make_blank_file("test_file", "txt")
        assert is_file_there("test_file.txt")

    def test_does_not_overwrite(self, tmp_workdir):
        """Should raise EasyFileManagerError instead of overwriting."""
        make_blank_file("test_file", "txt")
        with pytest.raises(EasyFileManagerError):
            make_blank_file("test_file", "txt")

    def test_invalid_extension_raises(self, tmp_workdir):
        """Should raise InvalidExtension for unsupported extension."""
        with pytest.raises(EasyFileManagerError):
            make_blank_file("test", "exe")

    @pytest.mark.parametrize("ext", VALID_EXTENSIONS)
    def test_all_valid_extensions(self, tmp_workdir, ext):
        """Should create files for each valid extension."""
        make_blank_file(f"file_{ext}", ext)
        assert is_file_there(f"file_{ext}.{ext}")


class TestAddALine:
    """Tests for add_a_line function."""

    def test_append_to_existing_file(self, tmp_workdir):
        """Should append a line to an existing file."""
        make_blank_file("test", "txt")
        add_a_line("test.txt", "hello world")
        lines = read_file_to_list("test.txt")
        assert "hello world" in lines

    def test_creates_file_if_not_exists(self, tmp_workdir):
        """Should create file if it doesn't exist and add line."""
        add_a_line("new_file.txt", "first line")
        assert is_file_there("new_file.txt")
        lines = read_file_to_list("new_file.txt")
        assert lines == ["first line"]

    def test_multiple_lines(self, tmp_workdir):
        """Should append multiple lines sequentially."""
        for i in range(3):
            add_a_line("multi.txt", f"line {i}")
        lines = read_file_to_list("multi.txt")
        assert lines == ["line 0", "line 1", "line 2"]

    def test_invalid_extension_raises(self, tmp_workdir):
        """Should raise for unsupported extension."""
        with pytest.raises(EasyFileManagerError):
            add_a_line("test.exe", "hello")


class TestReadFileToList:
    """Tests for read_file_to_list function."""

    def test_read_empty_file(self, tmp_workdir):
        """Should return empty list for blank file."""
        make_blank_file("empty", "txt")
        assert read_file_to_list("empty.txt") == []

    def test_read_non_existent_file(self, tmp_workdir):
        """Should raise EasyFileManagerError for missing file."""
        with pytest.raises(EasyFileManagerError):
            read_file_to_list("nonexistent.txt")

    def test_strips_whitespace(self, tmp_workdir):
        """Should strip whitespace from lines."""
        with open("test.txt", "w") as f:
            f.write("  spaced line  \n")
            f.write("\tindented\n")
        lines = read_file_to_list("test.txt")
        assert lines == ["spaced line", "indented"]

    def test_invalid_extension_raises(self, tmp_workdir):
        """Should raise for unsupported extension."""
        with pytest.raises(EasyFileManagerError):
            read_file_to_list("test.jpg")


class TestRemoveFile:
    """Tests for remove_file function."""

    def test_removes_existing_file(self, tmp_workdir):
        """Should delete an existing file."""
        make_blank_file("delete_me", "txt")
        assert is_file_there("delete_me.txt")
        remove_file("delete_me.txt")
        assert not is_file_there("delete_me.txt")

    def test_remove_nonexistent(self, tmp_workdir):
        """Should raise for non-existent file."""
        with pytest.raises(EasyFileManagerError):
            remove_file("ghost.txt")

    def test_invalid_extension_raises(self, tmp_workdir):
        """Should raise for unsupported extension."""
        with pytest.raises(EasyFileManagerError):
            remove_file("test.dll")


class TestRenameFile:
    """Tests for rename_file function."""

    def test_rename_existing_file(self, tmp_workdir):
        """Should rename an existing file."""
        make_blank_file("original", "txt")
        rename_file("original.txt", "renamed.txt")
        assert not is_file_there("original.txt")
        assert is_file_there("renamed.txt")

    def test_rename_to_existing_name(self, tmp_workdir):
        """Should raise if new name already exists."""
        make_blank_file("file_a", "txt")
        make_blank_file("file_b", "txt")
        with pytest.raises(EasyFileManagerError):
            rename_file("file_a.txt", "file_b.txt")

    def test_rename_nonexistent(self, tmp_workdir):
        """Should raise if source file doesn't exist."""
        with pytest.raises(EasyFileManagerError):
            rename_file("nope.txt", "yep.txt")

    def test_invalid_extension_raises(self, tmp_workdir):
        """Should raise for unsupported extension."""
        with pytest.raises(EasyFileManagerError):
            rename_file("test.txt", "test.bin")


class TestListFiles:
    """Tests for list_files function."""

    def test_lists_valid_files(self, tmp_workdir):
        """Should list all valid extension files."""
        make_blank_file("a", "txt")
        make_blank_file("b", "csv")
        files = list_files()
        assert "a.txt" in files
        assert "b.csv" in files

    def test_filter_by_extension(self, tmp_workdir):
        """Should filter by extension when specified."""
        make_blank_file("doc", "txt")
        make_blank_file("data", "csv")
        txt_files = list_files("txt")
        assert "doc.txt" in txt_files
        assert "data.csv" not in txt_files

    def test_skip_hidden_and_invalid(self, tmp_workdir):
        """Should not list files with invalid extensions."""
        make_blank_file("good", "txt")
        # Create a file with an invalid extension
        with open("bad.jpg", "w") as f:
            f.write("")
        files = list_files()
        assert "good.txt" in files
        assert "bad.jpg" not in files

    def test_invalid_extension_filter_raises(self, tmp_workdir):
        """Should raise InvalidExtension for invalid filter."""
        with pytest.raises(EasyFileManagerError):
            list_files("xyz")


class TestCopyFile:
    """Tests for copy_file function."""

    def test_copy_file(self, tmp_workdir):
        """Should copy a file to a new name."""
        make_blank_file("source", "txt")
        add_a_line("source.txt", "copied content")
        copy_file("source.txt", "dest.txt")
        assert is_file_there("dest.txt")
        assert read_file_to_list("dest.txt") == ["copied content"]

    def test_copy_nonexistent_source(self, tmp_workdir):
        """Should raise if source doesn't exist."""
        with pytest.raises(EasyFileManagerError):
            copy_file("ghost.txt", "dest.txt")

    def test_copy_to_existing_destination(self, tmp_workdir):
        """Should raise if destination already exists."""
        make_blank_file("src", "txt")
        make_blank_file("dst", "txt")
        with pytest.raises(EasyFileManagerError):
            copy_file("src.txt", "dst.txt")

    def test_invalid_source_extension_raises(self, tmp_workdir):
        """Should raise if source has invalid extension."""
        with pytest.raises(EasyFileManagerError):
            copy_file("test.exe", "test.txt")

    def test_invalid_dest_extension_raises(self, tmp_workdir):
        """Should raise if destination has invalid extension."""
        with pytest.raises(EasyFileManagerError):
            copy_file("test.txt", "test.exe")


class TestIsFileThere:
    """Tests for is_file_there function."""

    def test_existing_file(self, tmp_workdir):
        """Should return True for existing file."""
        make_blank_file("present", "txt")
        assert is_file_there("present.txt")

    def test_missing_file(self, tmp_workdir):
        """Should return False for missing file."""
        assert not is_file_there("nonexistent.txt")

    def test_directory_not_file(self, tmp_workdir):
        """Should return False for directories."""
        os.mkdir("mydir")
        assert not is_file_there("mydir")
