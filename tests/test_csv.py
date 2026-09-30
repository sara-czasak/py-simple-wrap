import pytest

from py_simple_package.src.py_simple import (
    count_csv_rows,
    filter_csv_rows,
    get_csv_columns,
    read_csv_to_list,
    write_csv_from_list,
    sort_csv_by_column,
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


class TestSortCsvByColumn:
    def test_sort_ascending_by_default(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nCarol,42\nAlice,24\nBob,31\n", encoding="utf-8")

        sort_csv_by_column(str(csv_file), column="Age")

        result = read_csv_to_list(str(csv_file), return_dict=True)

        assert result[0]["Age"] == "24"
        assert result[1]["Age"] == "31"
        assert result[2]["Age"] == "42"

    def test_sort_descending(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nCarol,42\nAlice,24\nBob,31\n", encoding="utf-8")
        sort_csv_by_column(str(csv_file), column="Age", reverse=True)

        result = read_csv_to_list(str(csv_file), return_dict=True)

        assert result[0]["Age"] == "42"
        assert result[1]["Age"] == "31"
        assert result[2]["Age"] == "24"

    def test_sort_to_new_output_file(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        new_csv_file = tmp_path / "people_sorted.csv"
        csv_file.write_text("Name,Age\nCarol,42\nAlice,24\nBob,31\n", encoding="utf-8")

        sort_csv_by_column(str(csv_file), column="Age", output_filepath=str(new_csv_file))

        result = read_csv_to_list(str(new_csv_file), return_dict=True)
        original = read_csv_to_list(str(csv_file), return_dict=True)

        assert result[0]["Age"] == "24"
        assert result[1]["Age"] == "31"
        assert result[2]["Age"] == "42"

        assert original[0]["Age"] == "42"
        assert original[1]["Age"] == "24"
        assert original[2]["Age"] == "31"

    def test_sort_invalid_output_path_raises_error(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        invalid_output = tmp_path / "non_existent_folder" / "people_sorted.csv"
        csv_file.write_text("Name,Age\nCarol,42\nAlice,24\nBob,31\n", encoding="utf-8")

        with pytest.raises(FileNotFoundError):
            sort_csv_by_column(str(csv_file), column="Age", output_filepath=str(invalid_output))

    def test_sort_missing_column_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,InvalidColumn\nCarol,42\nAlice,24\nBob,31\n", encoding="utf-8")

        with pytest.raises(ValueError):
            sort_csv_by_column(str(csv_file), column="Age")

    def test_sort_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match=f"File is empty: "):
            sort_csv_by_column(str(empty_file), column="Age")

    def test_sort_by_string_column(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nCarol,42\nAlice,24\nBob,31\n", encoding="utf-8")

        sort_csv_by_column(str(csv_file), column="Name")

        result = read_csv_to_list(str(csv_file), return_dict=True)

        assert result[0]["Name"] == "Alice"
        assert result[1]["Name"] == "Bob"
        assert result[2]["Name"] == "Carol"

    def test_sort_mixed_column_types(self, tmp_path):
        csv_file = tmp_path / "mixed.csv"
        csv_file.write_text("Name,Age\n""Alice,thirty\n""Bob,25\n""Carol,2.5\n""Dan,\n""Eve,eleven\n", encoding="utf-8",)

        sort_csv_by_column(str(csv_file), column="Age")
        
        result = read_csv_to_list(str(csv_file), return_dict=True)

        assert [row["Age"] for row in result] == ["2.5", "25", "", "eleven", "thirty"]

    def test_sort_mixed_column_types_reversed(self, tmp_path):
        csv_file = tmp_path / "mixed.csv"
        csv_file.write_text("Name,Age\n""Alice,thirty\n""Bob,25\n""Carol,2.5\n""Dan,\n""Eve,eleven\n", encoding="utf-8",)

        sort_csv_by_column(str(csv_file), column="Age", reverse=True)
        
        result = read_csv_to_list(str(csv_file), return_dict=True)

        assert [row["Age"] for row in result] == ["thirty", "eleven", "", "25", "2.5"]

    def test_sort_header_only_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "header_only.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        with pytest.raises(ValueError, match="No data rows to sort in file"):
            sort_csv_by_column(str(csv_file), column="Age")