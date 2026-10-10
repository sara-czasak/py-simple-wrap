import builtins

import pytest

from py_simple.easy_csv import iter_csv_rows


def test_dict_rows_and_unicode(tmp_path):
    path = tmp_path / "people.csv"
    path.write_text('Name,Note\nŽan,"hello, world"\nAlice,"two\nlines"\n', encoding="utf-8")
    assert list(iter_csv_rows(str(path))) == [
        {"Name": "Žan", "Note": "hello, world"},
        {"Name": "Alice", "Note": "two\nlines"},
    ]


def test_list_rows_include_header_and_custom_delimiter(tmp_path):
    path = tmp_path / "people.csv"
    path.write_text("Name;Age\nAlice;24\n", encoding="utf-8")
    assert list(iter_csv_rows(str(path), return_dict=False, delimiter=";")) == [
        ["Name", "Age"], ["Alice", "24"]
    ]


def test_header_only_has_no_dict_rows(tmp_path):
    path = tmp_path / "header.csv"
    path.write_text("Name,Age\n", encoding="utf-8")
    assert list(iter_csv_rows(str(path))) == []


def test_empty_file_is_an_error(tmp_path):
    path = tmp_path / "empty.csv"
    path.touch()
    with pytest.raises(ValueError, match="File is empty"):
        list(iter_csv_rows(str(path)))


def test_missing_file_is_an_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(iter_csv_rows(str(tmp_path / "missing.csv")))


@pytest.mark.parametrize("finish", ["exhaust", "close"])
def test_file_is_opened_lazily_and_closed(tmp_path, monkeypatch, finish):
    path = tmp_path / "people.csv"
    path.write_text("Name\nAlice\nBob\n", encoding="utf-8")
    handles = []
    original_open = builtins.open

    def tracked_open(*args, **kwargs):
        handle = original_open(*args, **kwargs)
        handles.append(handle)
        return handle

    monkeypatch.setattr(builtins, "open", tracked_open)
    rows = iter_csv_rows(str(path))
    assert handles == []
    assert next(rows) == {"Name": "Alice"}
    assert not handles[0].closed
    if finish == "exhaust":
        assert list(rows) == [{"Name": "Bob"}]
    else:
        rows.close()
    assert handles[0].closed
