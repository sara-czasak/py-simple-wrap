import builtins
import csv
import os

import pytest

from py_simple_package.src.py_simple.easy_csv import iter_csv_rows
from py_simple_package.src.py_simple import easy_csv

from py_simple_package.src.py_simple import (
    append_row_to_csv,
    count_csv_rows,
    drop_empty_csv_rows,
    filter_csv_rows,
    get_csv_columns,
    read_csv_column,
    read_csv_to_list,
    write_csv_from_list,
    sort_csv_by_column,
    delete_csv_rows,
    merge_csv_files,
)


def write_people_csv(path):
    path.write_text(
        "Name,Age\nAlice,24\nBob,31\nCarol,42\n",
        encoding="utf-8",
    )


def _symlink_or_skip(link, target):
    """Skip only when Windows denies the privilege to create symbolic links."""
    try:
        link.symlink_to(target)
    except OSError as error:
        if getattr(error, "winerror", None) == 1314:
            pytest.skip("Creating symbolic links requires a Windows privilege")
        raise


class TestIterCsvRows:
    @pytest.mark.parametrize("newline", ["\n", "\r\n"], ids=["lf", "crlf"])
    def test_dict_rows_and_unicode(self, tmp_path, newline):
        path = tmp_path / "people.csv"
        # Write exact bytes so Windows does not translate the fixture's newlines.
        content = f'Name,Note{newline}Žan,"hello, world"{newline}Alice,"two{newline}lines"{newline}'
        path.write_bytes(content.encode("utf-8"))
        assert list(iter_csv_rows(str(path))) == [
            {"Name": "Žan", "Note": "hello, world"},
            {"Name": "Alice", "Note": f"two{newline}lines"},
        ]

    def test_list_rows_include_header_and_custom_delimiter(self, tmp_path):
        path = tmp_path / "people.csv"
        path.write_text("Name;Age\nAlice;24\n", encoding="utf-8")
        assert list(iter_csv_rows(str(path), return_dict=False, delimiter=";")) == [
            ["Name", "Age"], ["Alice", "24"]
        ]

    def test_header_only_has_no_dict_rows(self, tmp_path):
        path = tmp_path / "header.csv"
        path.write_text("Name,Age\n", encoding="utf-8")
        assert list(iter_csv_rows(str(path))) == []

    def test_empty_file_is_an_error(self, tmp_path):
        path = tmp_path / "empty.csv"
        path.touch()
        with pytest.raises(ValueError, match="File is empty"):
            list(iter_csv_rows(str(path)))

    def test_missing_file_is_an_error(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            list(iter_csv_rows(str(tmp_path / "missing.csv")))

    @pytest.mark.parametrize("finish", ["exhaust", "close"])
    def test_file_is_opened_lazily_and_closed(self, tmp_path, monkeypatch, finish):
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


class TestMergeCsvFiles:
    def test_order_single_header_and_existing_helpers(self, tmp_path):
        first, second, output = [tmp_path / name for name in ("a", "b", "out")]
        write_people_csv(first)
        second.write_text("Name,Age\nDana,19\nEve,20\n", encoding="utf-8")
        originals = [path.read_bytes() for path in (first, second)]
        output.write_text("old output", encoding="utf-8")

        assert merge_csv_files([str(second), str(first)], str(output)) is None

        assert get_csv_columns(str(output)) == ["Name", "Age"]
        assert count_csv_rows(str(output)) == 5
        assert read_csv_column(str(output), "Name") == [
            "Dana",
            "Eve",
            "Alice",
            "Bob",
            "Carol",
        ]
        assert [path.read_bytes() for path in (first, second)] == originals
        assert set(tmp_path.iterdir()) == {first, second, output}

    @pytest.mark.parametrize("delimiter", [",", ";", "\t"])
    def test_csv_values_and_record_shapes_are_preserved(self, tmp_path, delimiter):
        first, second, output = [tmp_path / name for name in ("a", "b", "out")]
        rows = [
            ["Name", "Note"],
            ['Zoë, "林"', "line one\r\nline two"],
            ["", ""],
            [],
            ["short"],
            ["extra", "", "third"],
            [" spaced ", f"contains{delimiter}delimiter"],
        ]
        for path, records in ((first, rows[:3]), (second, [rows[0], *rows[3:]])):
            with path.open("w", newline="", encoding="utf-8") as file:
                csv.writer(file, delimiter=delimiter).writerows(records)

        merge_csv_files([first, second], output, delimiter=delimiter)

        with output.open(newline="", encoding="utf-8") as file:
            assert list(csv.reader(file, delimiter=delimiter)) == rows

    def test_header_only_inputs_and_repeated_input(self, tmp_path):
        empty, data, output = [tmp_path / name for name in ("header", "data", "out")]
        empty.write_text("Name,Age\n", encoding="utf-8")
        data.write_text("Name,Age\nAlice,24\n", encoding="utf-8")

        merge_csv_files([empty, data, empty, data], output)
        assert read_csv_to_list(str(output), return_dict=False) == [
            ["Name", "Age"],
            ["Alice", "24"],
            ["Alice", "24"],
        ]
        merge_csv_files([empty, empty], output)
        assert read_csv_to_list(str(output), return_dict=False) == [["Name", "Age"]]

    @pytest.mark.parametrize("existing_output", [False, True])
    @pytest.mark.parametrize(
        "later_content,exception,message",
        [
            (b"", ValueError, "File has no header"),
            (b"\nName,Age\n", ValueError, "File has no header"),
            (b"Age,Name\n24,Alice\n", ValueError, "Headers do not match"),
            (b"Name,Years\nAlice,24\n", ValueError, "Headers do not match"),
            (b"Name,Age\n\xff\n", UnicodeError, None),
            (b'Name,Age\n"unterminated,24\n', csv.Error, None),
            (None, FileNotFoundError, None),
        ],
    )
    def test_later_failure_preserves_inputs_and_output(
        self, tmp_path, existing_output, later_content, exception, message
    ):
        first, later, output = [tmp_path / name for name in ("first", "later", "out")]
        write_people_csv(first)
        if later_content is not None:
            later.write_bytes(later_content)
        if existing_output:
            output.write_bytes(b"original output\r\n")
        before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}

        with pytest.raises(exception, match=message):
            merge_csv_files([first, later], output)

        assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before

    def test_no_inputs_does_not_touch_output(self, tmp_path):
        output = tmp_path / "out"
        output.write_bytes(b"original")
        with pytest.raises(ValueError, match="At least one input"):
            merge_csv_files([], output)
        assert output.read_bytes() == b"original"
        assert list(tmp_path.iterdir()) == [output]

    @pytest.mark.parametrize("alias", ["same", "relative", "symlink", "hardlink"])
    def test_output_alias_rejected_even_for_later_input(
        self, tmp_path, monkeypatch, alias
    ):
        first, second = tmp_path / "first.csv", tmp_path / "second.csv"
        write_people_csv(first)
        write_people_csv(second)
        output = tmp_path / "alias.csv"
        if alias == "same":
            output = second
        elif alias == "relative":
            monkeypatch.chdir(tmp_path)
            output = "./second.csv"
        elif alias == "symlink":
            _symlink_or_skip(output, second)
        else:
            os.link(second, output)
        before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}

        with pytest.raises(ValueError, match="Output must not refer to an input"):
            merge_csv_files([first, second], output)

        assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before

    def test_output_symlink_to_unrelated_file_is_replaced(self, tmp_path):
        source, target, output = [
            tmp_path / name for name in ("source", "target", "out")
        ]
        write_people_csv(source)
        target.write_bytes(b"leave alone")
        _symlink_or_skip(output, target)

        merge_csv_files([source], output)

        assert not output.is_symlink()
        assert target.read_bytes() == b"leave alone"
        assert read_csv_to_list(str(output)) == read_csv_to_list(str(source))

    def test_missing_output_parent_preserves_source(self, tmp_path):
        source = tmp_path / "source"
        write_people_csv(source)
        before = source.read_bytes()
        with pytest.raises(FileNotFoundError):
            merge_csv_files([source], tmp_path / "missing" / "out")
        assert source.read_bytes() == before
        assert list(tmp_path.iterdir()) == [source]

    @pytest.mark.parametrize("failure", ["write", "replace"])
    def test_output_failure_cleans_temp_and_preserves_files(
        self, tmp_path, monkeypatch, failure
    ):
        source, output = tmp_path / "source", tmp_path / "out"
        write_people_csv(source)
        output.write_bytes(b"original")
        before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}

        def fail(*args, **kwargs):
            raise OSError("simulated output failure")

        if failure == "replace":
            monkeypatch.setattr(easy_csv.os, "replace", fail)
        else:
            real_writer = csv.writer

            def failing_writer(*args, **kwargs):
                class FailingWriter:
                    writerow = real_writer(*args, **kwargs).writerow
                    writerows = staticmethod(fail)

                return FailingWriter()

            monkeypatch.setattr(easy_csv.csv, "writer", failing_writer)

        with pytest.raises(OSError, match="simulated output failure"):
            merge_csv_files([source], output)

        assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before

    def test_streams_records_without_reading_ahead(self, tmp_path, monkeypatch):
        source, output = tmp_path / "source", tmp_path / "out"
        source.write_text("n\n" + "1\n" * 1000, encoding="utf-8")
        real_reader, real_writer = csv.reader, csv.writer
        progress = {"read": 0, "written": 0}

        def guarded_reader(*args, **kwargs):
            for row in real_reader(*args, **kwargs):
                assert progress["read"] == progress["written"]
                progress["read"] += 1
                yield row

        def tracking_writer(*args, **kwargs):
            writer = real_writer(*args, **kwargs)

            class Writer:
                def writerow(self, row):
                    writer.writerow(row)
                    progress["written"] += 1

                def writerows(self, rows):
                    for row in rows:
                        self.writerow(row)

            return Writer()

        monkeypatch.setattr(easy_csv.csv, "reader", guarded_reader)
        monkeypatch.setattr(easy_csv.csv, "writer", tracking_writer)
        merge_csv_files([source], output)
        assert progress == {"read": 1001, "written": 1001}
        with output.open(newline="", encoding="utf-8") as file:
            assert list(real_reader(file)) == [["n"], *([["1"]] * 1000)]

    def test_public_imports(self):
        from py_simple import merge_csv_files as public_merge
        from py_simple.easy_csv import merge_csv_files as module_merge

        assert public_merge is module_merge
        assert module_merge.__name__ == merge_csv_files.__name__


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

        with pytest.raises(ValueError, match="File is empty"):
            read_csv_to_list(str(empty_file))

    def test_read_missing_file_error_message_includes_path(self, tmp_path):
        missing_file = tmp_path / "missing.csv"
        with pytest.raises(FileNotFoundError, match="File not found"):
            read_csv_to_list(str(missing_file))

    def test_read_header_only_returns_empty_list_of_dicts(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        assert read_csv_to_list(str(csv_file)) == []

    def test_read_header_only_as_lists_returns_header_row(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        assert read_csv_to_list(str(csv_file), return_dict=False) == [["Name", "Age"]]

    def test_read_short_row_drops_missing_keys(self, tmp_path):
        csv_file = tmp_path / "jagged.csv"
        csv_file.write_text("Name,Age\nAlice\n", encoding="utf-8")

        assert read_csv_to_list(str(csv_file)) == [{"Name": "Alice"}]

    def test_read_quoted_field_with_delimiter(self, tmp_path):
        csv_file = tmp_path / "quoted.csv"
        csv_file.write_text('Name,City\n"Smith, Jr.",Paris\n', encoding="utf-8")

        assert read_csv_to_list(str(csv_file)) == [
            {"Name": "Smith, Jr.", "City": "Paris"}
        ]


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
        with pytest.raises(ValueError, match="Data cannot be empty"):
            write_csv_from_list(str(csv_file), data=[])

        assert not csv_file.exists()

    def test_write_dicts_with_explicit_headers_controls_column_order(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        data = [{"Name": "Alice", "Age": "24"}]

        write_csv_from_list(str(csv_file), data=data, headers=["Age", "Name"])

        assert csv_file.read_text(encoding="utf-8") == "Age,Name\n24,Alice\n"

    def test_write_dicts_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        data = [{"Name": "Alice", "Age": "24"}]

        write_csv_from_list(str(csv_file), data=data, delimiter=";")

        assert csv_file.read_text(encoding="utf-8") == "Name;Age\nAlice;24\n"

    def test_write_lists_with_empty_headers_writes_no_header(self, tmp_path):
        csv_file = tmp_path / "out.csv"

        write_csv_from_list(str(csv_file), data=[["Alice", "24"]], headers=[])

        assert csv_file.read_text(encoding="utf-8") == "Alice,24\n"

    def test_write_overwrites_existing_file(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        csv_file.write_text("old,content\n", encoding="utf-8")

        write_csv_from_list(str(csv_file), data=[["new"]])

        assert csv_file.read_text(encoding="utf-8") == "new\n"

    def test_write_then_read_round_trip(self, tmp_path):
        csv_file = tmp_path / "out.csv"
        data = [{"Name": "Smith, Jr.", "Age": "50"}]

        write_csv_from_list(str(csv_file), data=data)

        assert read_csv_to_list(str(csv_file)) == data


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

        with pytest.raises(ValueError, match="File is empty"):
            get_csv_columns(str(empty_file))

    def test_get_columns_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a;b;c\n1;2;3\n", encoding="utf-8")

        assert get_csv_columns(str(csv_file), delimiter=";") == ["a", "b", "c"]

    def test_get_columns_header_only_file(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        assert get_csv_columns(str(csv_file)) == ["Name", "Age"]


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

        with pytest.raises(ValueError, match="File is empty"):
            count_csv_rows(str(empty_file))

    def test_count_header_only_including_header_returns_one(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        assert count_csv_rows(str(csv_file), include_header=True) == 1

    def test_count_ignores_newlines_inside_quoted_fields(self, tmp_path):
        csv_file = tmp_path / "quoted.csv"
        csv_file.write_text('Name,Note\nAlice,"line one\nline two"\n', encoding="utf-8")

        assert count_csv_rows(str(csv_file)) == 1


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

        with pytest.raises(ValueError, match="Column not found: City"):
            filter_csv_rows(str(csv_file), column="City", value="Nowhere")

    def test_filter_multiple_matches_preserve_order(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nAlice,30\nBob,31\nCarol,30\n", encoding="utf-8")

        result = filter_csv_rows(str(csv_file), column="Age", value="30")
        assert result == [
            {"Name": "Alice", "Age": "30"},
            {"Name": "Carol", "Age": "30"},
        ]

    def test_filter_lists_no_match_returns_empty_list(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = filter_csv_rows(
            str(csv_file), column="Name", value="Zed", return_dict=False
        )
        assert result == []

    def test_filter_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a;b\n1;2\n3;4\n", encoding="utf-8")

        result = filter_csv_rows(str(csv_file), column="a", value="3", delimiter=";")
        assert result == [{"a": "3", "b": "4"}]

    def test_filter_header_only_skips_column_check(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        assert filter_csv_rows(str(csv_file), column="City", value="x") == []

    def test_filter_missing_file_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            filter_csv_rows(str(tmp_path / "missing.csv"), column="Name", value="x")

    def test_filter_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="File is empty"):
            filter_csv_rows(str(empty_file), column="Name", value="x")


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

        sort_csv_by_column(
            str(csv_file), column="Age", output_filepath=str(new_csv_file)
        )

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
            sort_csv_by_column(
                str(csv_file), column="Age", output_filepath=str(invalid_output)
            )

    def test_sort_missing_column_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text(
            "Name,InvalidColumn\nCarol,42\nAlice,24\nBob,31\n", encoding="utf-8"
        )

        with pytest.raises(ValueError):
            sort_csv_by_column(str(csv_file), column="Age")

    def test_sort_empty_file_raises_value_error(self, tmp_path):
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="File is empty: "):
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
        csv_file.write_text(
            "Name,Age\n"
            "Alice,thirty\n"
            "Bob,25\n"
            "Carol,2.5\n"
            "Dan,\n"
            "Eve,eleven\n",
            encoding="utf-8",
        )

        sort_csv_by_column(str(csv_file), column="Age")

        result = read_csv_to_list(str(csv_file), return_dict=True)

        assert [row["Age"] for row in result] == ["2.5", "25", "", "eleven", "thirty"]

    def test_sort_mixed_column_types_reversed(self, tmp_path):
        csv_file = tmp_path / "mixed.csv"
        csv_file.write_text(
            "Name,Age\n"
            "Alice,thirty\n"
            "Bob,25\n"
            "Carol,2.5\n"
            "Dan,\n"
            "Eve,eleven\n",
            encoding="utf-8",
        )

        sort_csv_by_column(str(csv_file), column="Age", reverse=True)

        result = read_csv_to_list(str(csv_file), return_dict=True)

        assert [row["Age"] for row in result] == ["thirty", "eleven", "", "25", "2.5"]

    def test_sort_header_only_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "header_only.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        with pytest.raises(ValueError, match="No data rows to sort in file"):
            sort_csv_by_column(str(csv_file), column="Age")

    def test_sort_missing_file_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            sort_csv_by_column(str(tmp_path / "missing.csv"), column="Age")

    def test_sort_missing_column_message(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        with pytest.raises(ValueError, match="Column not found: City"):
            sort_csv_by_column(str(csv_file), column="City")

    def test_sort_numeric_values_not_lexicographic(self, tmp_path):
        csv_file = tmp_path / "nums.csv"
        csv_file.write_text("n\n10\n9\n-1\n100\n", encoding="utf-8")

        sort_csv_by_column(str(csv_file), column="n")

        assert read_csv_column(str(csv_file), "n") == ["-1", "9", "10", "100"]

    def test_sort_is_stable_for_equal_keys(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nAlice,30\nBob,20\nCarol,30\n", encoding="utf-8")

        sort_csv_by_column(str(csv_file), column="Age")

        assert read_csv_column(str(csv_file), "Name") == ["Bob", "Alice", "Carol"]

    def test_sort_short_row_treated_as_empty(self, tmp_path):
        csv_file = tmp_path / "jagged.csv"
        csv_file.write_text("Name,Age\nCarol,\nAlice\nBob,5\n", encoding="utf-8")

        sort_csv_by_column(str(csv_file), column="Age")

        assert read_csv_to_list(str(csv_file)) == [
            {"Name": "Bob", "Age": "5"},
            {"Name": "Carol", "Age": ""},
            {"Name": "Alice", "Age": ""},
        ]

    def test_sort_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("k;v\nb;2\na;1\n", encoding="utf-8")

        sort_csv_by_column(str(csv_file), column="v", delimiter=";")

        assert csv_file.read_text(encoding="utf-8") == "k;v\na;1\nb;2\n"


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

        with pytest.raises(ValueError, match="File is empty"):
            append_row_to_csv(str(empty_file), {"Name": "Charlie", "Age": "29"})

    def test_append_newline_only_file_raises_value_error(self, tmp_path):
        newline_file = tmp_path / "newline_only.csv"
        newline_file.write_text("\n", encoding="utf-8")

        with pytest.raises(ValueError, match="File is empty"):
            append_row_to_csv(str(newline_file), {"Name": "Charlie", "Age": "29"})

    def test_append_dict_custom_delimiter(self, tmp_path):
        tsv_file = tmp_path / "people.tsv"
        tsv_file.write_text("Name\tAge\nAlice\t24\n", encoding="utf-8")

        append_row_to_csv(str(tsv_file), {"Name": "David", "Age": "35"}, delimiter="\t")
        rows = read_csv_to_list(str(tsv_file), delimiter="\t")
        assert rows[-1] == {"Name": "David", "Age": "35"}

    def test_append_list_custom_delimiter(self, tmp_path):
        tsv_file = tmp_path / "people.tsv"
        tsv_file.write_text("Name\tAge\nAlice\t24\n", encoding="utf-8")

        append_row_to_csv(str(tsv_file), ["David", "35"], delimiter="\t")
        rows = read_csv_to_list(str(tsv_file), return_dict=False, delimiter="\t")
        assert rows[-1] == ["David", "35"]

    def test_append_blank_header_line_raises_value_error(self, tmp_path):
        blank_header = tmp_path / "blank.csv"
        blank_header.write_text("\n", encoding="utf-8")

        with pytest.raises(ValueError, match="File is empty"):
            append_row_to_csv(str(blank_header), ["Charlie", "29"])

        assert blank_header.read_text(encoding="utf-8") == "\n"

    def test_append_dict_row_follows_header_order(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        append_row_to_csv(str(csv_file), {"Age": "29", "Name": "Charlie"})

        assert csv_file.read_text(encoding="utf-8").endswith("Charlie,29\n")

    def test_append_dict_row_missing_key_writes_blank(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        append_row_to_csv(str(csv_file), {"Name": "Charlie"})

        assert read_csv_to_list(str(csv_file))[-1] == {"Name": "Charlie", "Age": ""}

    def test_append_dict_row_unknown_key_raises_value_error(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        with pytest.raises(ValueError):
            append_row_to_csv(str(csv_file), {"Name": "Charlie", "City": "Paris"})

    def test_append_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a;b\n1;2\n", encoding="utf-8")

        append_row_to_csv(str(csv_file), {"a": "3", "b": "4"}, delimiter=";")
        append_row_to_csv(str(csv_file), ["5", "6"], delimiter=";")

        assert csv_file.read_text(encoding="utf-8") == "a;b\n1;2\n3;4\n5;6\n"


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
        from py_simple_package.src.py_simple.easy_csv import (
            read_csv_column as easy_csv_read_column,
        )

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

    def test_read_csv_column_mixed_alias_kwargs(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        assert read_csv_column(str(csv_file), column_name="Name") == [
            "Alice",
            "Bob",
            "Carol",
        ]
        assert read_csv_column(file_path=str(csv_file), column="Age") == [
            "24",
            "31",
            "42",
        ]

    def test_read_csv_column_primary_args_take_precedence_over_aliases(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        result = read_csv_column(
            str(csv_file),
            "Name",
            file_path=str(tmp_path / "missing.csv"),
            column_name="Age",
        )
        assert result == ["Alice", "Bob", "Carol"]

    def test_read_csv_column_missing_path_message(self):
        with pytest.raises(TypeError, match="'filepath' or 'file_path'"):
            read_csv_column(column="Name")

    def test_read_csv_column_missing_column_message(self, tmp_path):
        with pytest.raises(TypeError, match="'column' or 'column_name'"):
            read_csv_column(file_path=str(tmp_path / "people.csv"))


class TestDeleteCsvRows:
    def test_delete_matching_row(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        delete_csv_rows(str(csv_file), column="Name", value="Bob")

        rows = read_csv_to_list(str(csv_file), return_dict=True)
        assert rows == [
            {"Name": "Alice", "Age": "24"},
            {"Name": "Carol", "Age": "42"},
        ]

    def test_delete_multiple_matching_rows(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text(
            "Name,Age\nAlice,24\nBob,31\nCarol,42\nBob,35\n",
            encoding="utf-8",
        )

        delete_csv_rows(str(csv_file), column="Name", value="Bob")

        rows = read_csv_to_list(str(csv_file), return_dict=True)
        assert rows == [
            {"Name": "Alice", "Age": "24"},
            {"Name": "Carol", "Age": "42"},
        ]

    def test_delete_no_matching_row(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        with pytest.raises(ValueError, match="No rows found"):
            delete_csv_rows(
                str(csv_file),
                column="Name",
                value="David",
            )

    def test_delete_missing_column(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)

        with pytest.raises(ValueError, match="Column not found"):
            delete_csv_rows(
                str(csv_file),
                column="Country",
                value="India",
            )

    def test_delete_missing_file(self, tmp_path):
        csv_file = tmp_path / "missing.csv"

        with pytest.raises(FileNotFoundError):
            delete_csv_rows(
                str(csv_file),
                column="Name",
                value="Bob",
            )

    def test_delete_empty_file(self, tmp_path):
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="File is empty"):
            delete_csv_rows(
                str(csv_file),
                column="Name",
                value="Bob",
            )

    def test_delete_no_match_leaves_file_and_no_temp_files(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        write_people_csv(csv_file)
        original = csv_file.read_text(encoding="utf-8")

        with pytest.raises(ValueError, match="No rows found with Name=David"):
            delete_csv_rows(str(csv_file), column="Name", value="David")

        assert csv_file.read_text(encoding="utf-8") == original
        assert list(tmp_path.iterdir()) == [csv_file]

    def test_delete_all_rows_keeps_header(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nBob,31\nBob,35\n", encoding="utf-8")

        delete_csv_rows(str(csv_file), column="Name", value="Bob")

        assert csv_file.read_text(encoding="utf-8") == "Name,Age\n"
        assert list(tmp_path.iterdir()) == [csv_file]

    def test_delete_header_only_file_raises_no_rows_found(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        with pytest.raises(ValueError, match="No rows found"):
            delete_csv_rows(str(csv_file), column="Name", value="Bob")

    def test_delete_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a;b\n1;2\n3;4\n", encoding="utf-8")

        delete_csv_rows(str(csv_file), column="a", value="1", delimiter=";")

        assert csv_file.read_text(encoding="utf-8") == "a;b\n3;4\n"


class TestDropEmptyCsvRows:
    def test_removes_blank_rows_and_keeps_header(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text(
            "Name,Age\nAlice,24\n,\nBob,31\n  ,  \n",
            encoding="utf-8",
        )

        removed = drop_empty_csv_rows(str(csv_file))

        assert removed == 2
        assert read_csv_to_list(str(csv_file)) == [
            {"Name": "Alice", "Age": "24"},
            {"Name": "Bob", "Age": "31"},
        ]

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
        with pytest.raises(ValueError, match="File is empty"):
            drop_empty_csv_rows(str(empty_file))

    def test_header_only_file_removes_nothing(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\n", encoding="utf-8")

        assert drop_empty_csv_rows(str(csv_file)) == 0
        assert csv_file.read_text(encoding="utf-8") == "Name,Age\n"

    def test_removes_zero_cell_blank_lines(self, tmp_path):
        csv_file = tmp_path / "people.csv"
        csv_file.write_text("Name,Age\nAlice,24\n\nBob,31\n", encoding="utf-8")

        assert drop_empty_csv_rows(str(csv_file)) == 1
        assert csv_file.read_text(encoding="utf-8") == "Name,Age\nAlice,24\nBob,31\n"

    def test_custom_delimiter(self, tmp_path):
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a;b\n1;2\n;\n", encoding="utf-8")

        assert drop_empty_csv_rows(str(csv_file), delimiter=";") == 1
        assert csv_file.read_text(encoding="utf-8") == "a;b\n1;2\n"
