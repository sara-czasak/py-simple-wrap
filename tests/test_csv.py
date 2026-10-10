import pytest

from py_simple_package.src.py_simple import (
    append_row_to_csv,
    count_csv_rows,
    drop_empty_csv_rows,
    filter_csv_rows,
    get_csv_columns,
    read_csv_column,
    read_csv_to_list,
    write_csv_from_list,
)


def write_people_csv(path):
    path.write_text(
        "Name,Age\nAlice,24\nBob,31\nCarol,42\n",
        encoding="utf-8",
    )


class TestReadCsvToList:
    def test_read_dicts(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = read_csv_to_list(str(csv_file))
        assert result == [
            {"Name": "Alice", "Age": "24"},
            {"Name": "Bob", "Age": "31"},
            {"Name": "Carol", "Age": "42"},
        ]

    def test_read_lists(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = read_csv_to_list(str(csv_file), return_dict=False)
        assert result == [
            ["Name", "Age"],
            ["Alice", "24"],
            ["Bob", "31"],
            ["Carol", "42"],
        ]

    def test_read_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a;b\n1;2\n", encoding="utf-8")

        result = read_csv_to_list(str(csv_file), delimiter=";")
        assert result == [{"a": "1", "b": "2"}]

    def test_read_missing_file_raises_file_not_found(self, tmp_path):
        missing_file = tmp_path / "missing.csv"
        with pytest.raises(FileNotFoundError):
            read_csv_to_list(str(missing_file))

    def test_read_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            read_csv_to_list(str(empty_file))


class TestWriteCsvFromList:
    def test_write_dicts(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        data = [
            {"Name": "Alice", "Age": "24"},
            {"Name": "Bob", "Age": "31"},
        ]

        write_csv_from_list(str(csv_file), data=data)

        assert csv_file.read_text(encoding="utf-8") == ("Name,Age\nAlice,24\nBob,31\n")

    def test_write_lists_with_headers(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        data = [["Alice", "24"], ["Bob", "31"]]

        write_csv_from_list(str(csv_file), data=data, headers=["Name", "Age"])

        assert csv_file.read_text(encoding="utf-8") == ("Name,Age\nAlice,24\nBob,31\n")

    def test_write_lists_without_headers(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        data = [["Alice", "24"], ["Bob", "31"]]

        write_csv_from_list(str(csv_file), data=data)

        assert csv_file.read_text(encoding="utf-8") == ("Alice,24\nBob,31\n")

    def test_write_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        data = [["Alice", "24"]]

        write_csv_from_list(str(csv_file), data=data, delimiter=";")

        assert csv_file.read_text(encoding="utf-8") == "Alice;24\n"

    def test_write_empty_data_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        with pytest.raises(ValueError):
            write_csv_from_list(str(csv_file), data=[])


class TestGetCsvColumns:
    def test_get_columns(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = get_csv_columns(str(csv_file))
        assert result == ["Name", "Age"]

    def test_get_columns_missing_file_raises_file_not_found(self, tmp_path):
        missing_file = tmp_path / "missing.csv"
        with pytest.raises(FileNotFoundError):
            get_csv_columns(str(missing_file))

    def test_get_columns_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            get_csv_columns(str(empty_file))


class TestCountCsvRows:
    def test_count_data_rows_by_default(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = count_csv_rows(str(csv_file))

        assert result == 3

    def test_count_rows_including_header(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = count_csv_rows(str(csv_file), include_header=True)

        assert result == 4

    def test_count_header_only_file_returns_zero_by_default(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        result = count_csv_rows(str(csv_file))

        assert result == 0

    def test_count_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a;b\n1;2\n3;4\n", encoding="utf-8")

        result = count_csv_rows(str(csv_file), delimiter=";")

        assert result == 2

    def test_count_missing_file_raises_file_not_found(self, tmp_path):
        missing_file = tmp_path / "missing.csv"
        with pytest.raises(FileNotFoundError):
            count_csv_rows(str(missing_file))

    def test_count_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            count_csv_rows(str(empty_file))


class TestFilterCsvRows:
    def test_filter_dicts(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = filter_csv_rows(str(csv_file), column="Name", value="Bob")
        assert result == [{"Name": "Bob", "Age": "31"}]

    def test_filter_lists(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = filter_csv_rows(
            str(csv_file), column="Age", value="42", return_dict=False
        )
        assert result == [["Carol", "42"]]

    def test_filter_no_match(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = filter_csv_rows(str(csv_file), column="Name", value="Zed")
        assert result == []

    def test_filter_header_only_file_returns_empty_list(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        result = filter_csv_rows(str(csv_file), column="Name", value="Alice")
        assert result == []

    def test_filter_missing_column_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        with pytest.raises(ValueError):
            filter_csv_rows(str(csv_file), column="City", value="Nowhere")


class TestAppendRowToCsv:
    def test_append_dict_row(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        append_row_to_csv(str(csv_file), {"Name": "Charlie", "Age": "29"})

        rows = read_csv_to_list(str(csv_file), return_dict=True)
        assert len(rows) == 4
        assert rows[3] == {"Name": "Charlie", "Age": "29"}

    def test_append_list_row(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        append_row_to_csv(str(csv_file), ["Charlie", "29"])

        rows = read_csv_to_list(str(csv_file), return_dict=False)
        assert rows[-1] == ["Charlie", "29"]

    def test_append_missing_file_raises_file_not_found(self, tmp_path):
        missing_file = tmp_path / "missing.csv"
        with pytest.raises(FileNotFoundError):
            append_row_to_csv(str(missing_file), {"Name": "Charlie", "Age": "29"})

    def test_append_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            append_row_to_csv(str(empty_file), {"Name": "Charlie", "Age": "29"})


class TestReadCsvColumn:
    def test_read_csv_column_values(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = read_csv_column(str(csv_file), "Name")
        assert result == ["Alice", "Bob", "Carol"]

    def test_read_csv_column_numeric_strings(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = read_csv_column(str(csv_file), "Age")
        assert result == ["24", "31", "42"]

    def test_read_csv_column_filepath_kwargs(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = read_csv_column(filepath=str(csv_file), column="Name")
        assert result == ["Alice", "Bob", "Carol"]

    def test_read_csv_column_file_path_kwargs(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = read_csv_column(file_path=str(csv_file), column_name="Age")
        assert result == ["24", "31", "42"]

    def test_read_csv_column_direct_module_import(self, tmp_path):
        from py_simple_package.src.py_simple.easy_csv import read_csv_column as easy_csv_read_column
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = easy_csv_read_column(str(csv_file), "Name")
        assert result == ["Alice", "Bob", "Carol"]

    def test_read_csv_column_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("item;qty\napple;5\nbanana;10\n", encoding="utf-8")

        result = read_csv_column(str(csv_file), "item", delimiter=";")
        assert result == ["apple", "banana"]

    def test_read_csv_column_header_only_file_returns_empty_list(self, tmp_path):
        csv_file = tmp_path / "empty_data.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        result = read_csv_column(str(csv_file), "Name")
        assert result == []

    def test_read_csv_column_missing_file_raises_file_not_found(self, tmp_path):
        missing_file = tmp_path / "missing.csv"
        with pytest.raises(FileNotFoundError):
            read_csv_column(str(missing_file), "Name")

    def test_read_csv_column_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            read_csv_column(str(empty_file), "Name")

    def test_read_csv_column_missing_column_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        with pytest.raises(ValueError, match="Column not found"):
            read_csv_column(str(csv_file), "Nonexistent")

    def test_read_csv_column_missing_required_args_raises_type_error(self):
        with pytest.raises(TypeError):
            read_csv_column()

        with pytest.raises(TypeError):
            read_csv_column(filepath="people.csv")

    def test_read_csv_column_row_with_missing_field(self, tmp_path):
        csv_file = tmp_path / "jagged.csv"
        csv_file.write_text("Name,Age,Role\nAlice,24,Engineer\nBob\n", encoding="utf-8")

        result = read_csv_column(str(csv_file), "Role")
        assert result == ["Engineer", ""]


class TestDropEmptyCsvRows:
    def test_removes_blank_rows_and_keeps_header(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text(
            "Name,Age\nAlice,24\n,\nBob,31\n  ,  \n",
            encoding="utf-8",
        )

        removed = drop_empty_csv_rows(str(csv_file))

        assert removed == 2
        assert csv_file.read_text(encoding="utf-8") == "Name,Age\nAlice,24\nBob,31\n"

    def test_keeps_rows_that_have_one_value(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nAlice,\n,31\n", encoding="utf-8")

        assert drop_empty_csv_rows(str(csv_file)) == 0
        rows = read_csv_to_list(str(csv_file))
        assert rows == [
            {"Name": "Alice", "Age": ""},
            {"Name": "", "Age": "31"},
        ]

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            drop_empty_csv_rows(str(tmp_path / "missing.csv"))

    def test_empty_file_raises(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")
        with pytest.raises(ValueError):
            drop_empty_csv_rows(str(empty_file))