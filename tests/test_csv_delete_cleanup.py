import pytest

from py_simple_package.src.py_simple import easy_csv


def test_delete_rows_cleans_up_after_serialization_error(tmp_path):
    path = tmp_path / "people.csv"
    original = b"Name,Age\nBob,31\nAlice,24,extra\n"
    path.write_bytes(original)

    with pytest.raises(ValueError, match="fields not in fieldnames"):
        easy_csv.delete_csv_rows(str(path), "Name", "Bob")

    assert path.read_bytes() == original
    assert list(tmp_path.iterdir()) == [path]


def test_delete_rows_cleans_up_after_replace_error(tmp_path, monkeypatch):
    path = tmp_path / "people.csv"
    original = b"Name,Age\nBob,31\nAlice,24\n"
    path.write_bytes(original)

    def fail_replace(source, destination):
        raise PermissionError("replacement denied")

    monkeypatch.setattr(easy_csv.os, "replace", fail_replace)
    with pytest.raises(PermissionError, match="replacement denied"):
        easy_csv.delete_csv_rows(str(path), "Name", "Bob")

    assert path.read_bytes() == original
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.parametrize("value", ["Bob", "missing"])
def test_delete_rows_leaves_no_temporary_file(tmp_path, value):
    path = tmp_path / "people.csv"
    original = b"Name,Age\nBob,31\nAlice,24\n"
    path.write_bytes(original)

    if value == "missing":
        with pytest.raises(ValueError, match="No rows found"):
            easy_csv.delete_csv_rows(str(path), "Name", value)
        assert path.read_bytes() == original
    else:
        easy_csv.delete_csv_rows(str(path), "Name", value)
        assert easy_csv.read_csv_to_list(str(path)) == [{"Name": "Alice", "Age": "24"}]
    assert list(tmp_path.iterdir()) == [path]
