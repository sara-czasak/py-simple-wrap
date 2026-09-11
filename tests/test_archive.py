import zipfile

import pytest

from py_simple_package.src.py_simple.easy_archive import (
    EasyArchiveError,
    add_to_zip,
    is_zip_file,
    list_zip_contents,
    unzip_file,
    zip_files,
    zip_folder,
)


def make_folder_with_files(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "a.txt").write_text("hello", encoding="utf-8")
    sub = project / "sub"
    sub.mkdir()
    (sub / "b.txt").write_text("world", encoding="utf-8")
    return project


def test_zip_folder_creates_zip_with_relative_paths(tmp_path):
    project = make_folder_with_files(tmp_path)
    zip_name = str(tmp_path / "project.zip")

    result = zip_folder(str(project), zip_name)

    assert result == zip_name
    assert zipfile.is_zipfile(zip_name)
    with zipfile.ZipFile(zip_name) as zf:
        names = set(zf.namelist())
    assert names == {"a.txt", "sub/b.txt"}


def test_zip_folder_default_name(tmp_path, monkeypatch):
    project = make_folder_with_files(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = zip_folder(str(project))

    assert result == "project.zip"
    assert zipfile.is_zipfile("project.zip")


def test_zip_folder_dot_default_name_uses_cwd_folder(tmp_path, monkeypatch):
    project = make_folder_with_files(tmp_path)
    monkeypatch.chdir(project)

    result = zip_folder(".")

    assert result == "project.zip"
    assert zipfile.is_zipfile("project.zip")
    with zipfile.ZipFile("project.zip") as zf:
        names = set(zf.namelist())
    assert "a.txt" in names
    assert "sub/b.txt" in names


def test_zip_folder_missing_folder_raises(tmp_path):
    with pytest.raises(EasyArchiveError):
        zip_folder(str(tmp_path / "does_not_exist"), str(tmp_path / "out.zip"))


def test_zip_folder_rejects_non_zip_extension(tmp_path):
    project = make_folder_with_files(tmp_path)
    with pytest.raises(EasyArchiveError):
        zip_folder(str(project), str(tmp_path / "project.tar"))


def test_zip_files_missing_file_raises(tmp_path):
    file1 = tmp_path / "one.txt"
    file1.write_text("1", encoding="utf-8")
    missing = tmp_path / "missing.txt"
    zip_name = str(tmp_path / "out.zip")

    with pytest.raises(EasyArchiveError):
        zip_files([str(file1), str(missing)], zip_name)


def test_zip_files_all_missing_raises(tmp_path):
    with pytest.raises(EasyArchiveError):
        zip_files([str(tmp_path / "ghost.txt")], str(tmp_path / "out.zip"))


def test_zip_files_empty_input_raises(tmp_path):
    with pytest.raises(EasyArchiveError, match="No valid files to zip"):
        zip_files([], str(tmp_path / "out.zip"))


def test_zip_files_rejects_non_zip_extension(tmp_path):
    file1 = tmp_path / "one.txt"
    file1.write_text("1", encoding="utf-8")
    with pytest.raises(EasyArchiveError):
        zip_files([str(file1)], str(tmp_path / "out.rar"))


def test_unzip_file_round_trip(tmp_path):
    project = make_folder_with_files(tmp_path)
    zip_name = str(tmp_path / "project.zip")
    zip_folder(str(project), zip_name)

    destination = str(tmp_path / "restored")
    result = unzip_file(zip_name, destination)

    assert result == destination
    assert (tmp_path / "restored" / "a.txt").read_text(encoding="utf-8") == "hello"
    assert (tmp_path / "restored" / "sub" / "b.txt").read_text(
        encoding="utf-8"
    ) == "world"


def test_unzip_file_extracts_into_existing_destination(tmp_path):
    project = make_folder_with_files(tmp_path)
    zip_name = str(tmp_path / "project.zip")
    zip_folder(str(project), zip_name)
    destination = tmp_path / "restored"
    destination.mkdir()

    result = unzip_file(zip_name, str(destination))

    assert result == str(destination)
    assert (destination / "a.txt").read_text(encoding="utf-8") == "hello"
    assert (destination / "sub" / "b.txt").read_text(encoding="utf-8") == "world"


def test_unzip_file_missing_zip_raises(tmp_path):
    with pytest.raises(EasyArchiveError):
        unzip_file(str(tmp_path / "nope.zip"), str(tmp_path / "out"))


def test_unzip_file_invalid_zip_raises(tmp_path):
    fake_zip = tmp_path / "fake.zip"
    fake_zip.write_text("not actually a zip", encoding="utf-8")

    with pytest.raises(EasyArchiveError):
        unzip_file(str(fake_zip), str(tmp_path / "out"))


def test_list_zip_contents(tmp_path):
    project = make_folder_with_files(tmp_path)
    zip_name = str(tmp_path / "project.zip")
    zip_folder(str(project), zip_name)

    contents = list_zip_contents(zip_name)

    assert set(contents) == {"a.txt", "sub/b.txt"}


def test_list_zip_contents_missing_zip_raises(tmp_path):
    with pytest.raises(EasyArchiveError):
        list_zip_contents(str(tmp_path / "nope.zip"))


def test_list_zip_contents_invalid_zip_raises(tmp_path):
    fake_zip = tmp_path / "fake.zip"
    fake_zip.write_text("nope", encoding="utf-8")
    with pytest.raises(EasyArchiveError):
        list_zip_contents(str(fake_zip))


def test_add_to_zip_appends_file(tmp_path):
    file1 = tmp_path / "one.txt"
    file1.write_text("1", encoding="utf-8")
    zip_name = str(tmp_path / "out.zip")
    zip_files([str(file1)], zip_name)

    extra = tmp_path / "extra.txt"
    extra.write_text("extra", encoding="utf-8")

    result = add_to_zip(zip_name, str(extra))

    assert result is True
    with zipfile.ZipFile(zip_name) as zf:
        assert set(zf.namelist()) == {"one.txt", "extra.txt"}


def test_add_to_zip_missing_zip_raises(tmp_path):
    extra = tmp_path / "extra.txt"
    extra.write_text("extra", encoding="utf-8")
    with pytest.raises(EasyArchiveError):
        add_to_zip(str(tmp_path / "nope.zip"), str(extra))


def test_add_to_zip_missing_file_raises(tmp_path):
    file1 = tmp_path / "one.txt"
    file1.write_text("1", encoding="utf-8")
    zip_name = str(tmp_path / "out.zip")
    zip_files([str(file1)], zip_name)

    with pytest.raises(EasyArchiveError):
        add_to_zip(zip_name, str(tmp_path / "ghost.txt"))


def test_add_to_zip_invalid_zip_raises_without_corrupting(tmp_path):
    fake_zip = tmp_path / "fake.zip"
    fake_zip.write_text("plain text, not a zip", encoding="utf-8")
    extra = tmp_path / "extra.txt"
    extra.write_text("extra", encoding="utf-8")

    with pytest.raises(EasyArchiveError):
        add_to_zip(str(fake_zip), str(extra))

    assert fake_zip.read_text(encoding="utf-8") == "plain text, not a zip"


def test_is_zip_file_true_for_valid_zip(tmp_path):
    file1 = tmp_path / "one.txt"
    file1.write_text("1", encoding="utf-8")
    zip_name = str(tmp_path / "out.zip")
    zip_files([str(file1)], zip_name)

    assert is_zip_file(zip_name) is True


def test_is_zip_file_false_for_missing_path(tmp_path):
    assert is_zip_file(str(tmp_path / "nope.zip")) is False


def test_is_zip_file_false_for_non_zip_file(tmp_path):
    text_file = tmp_path / "notes.txt"
    text_file.write_text("plain text", encoding="utf-8")
    assert is_zip_file(str(text_file)) is False


def test_zip_folder_does_not_include_itself_when_output_is_inside_folder(tmp_path):
    project = make_folder_with_files(tmp_path)
    zip_name = str(project / "backup.zip")

    zip_folder(str(project), zip_name)

    with zipfile.ZipFile(zip_name) as zf:
        names = zf.namelist()
    assert "backup.zip" not in names
    assert set(names) == {"a.txt", "sub/b.txt"}


def test_zip_folder_empty_folder_creates_empty_archive(tmp_path):
    folder = tmp_path / "empty"
    folder.mkdir()
    zip_name = str(tmp_path / "empty.zip")

    result = zip_folder(str(folder), zip_name)

    assert result == zip_name
    with zipfile.ZipFile(zip_name) as zf:
        assert zf.namelist() == []


def test_unzip_file_destination_is_existing_file_raises(tmp_path):
    file1 = tmp_path / "one.txt"
    file1.write_text("1", encoding="utf-8")
    zip_name = str(tmp_path / "out.zip")
    zip_files([str(file1)], zip_name)

    blocked_destination = tmp_path / "blocked"
    blocked_destination.write_text("i am a file, not a folder", encoding="utf-8")

    with pytest.raises(EasyArchiveError):
        unzip_file(zip_name, str(blocked_destination))


def test_zip_files_disambiguates_colliding_basenames(tmp_path, capsys):
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()
    (dir1 / "report.txt").write_text("from dir1", encoding="utf-8")
    (dir2 / "report.txt").write_text("from dir2", encoding="utf-8")
    zip_name = str(tmp_path / "collide.zip")

    zip_files([str(dir1 / "report.txt"), str(dir2 / "report.txt")], zip_name)

    with zipfile.ZipFile(zip_name) as zf:
        names = zf.namelist()

    assert len(names) == 2
    assert len(set(names)) == 2

    destination = str(tmp_path / "extracted")
    unzip_file(zip_name, destination)
    extracted_texts = {
        p.read_text(encoding="utf-8") for p in (tmp_path / "extracted").iterdir()
    }
    assert extracted_texts == {"from dir1", "from dir2"}

    captured = capsys.readouterr()
    assert "already added from another folder" in captured.out


def test_zip_files_numbers_collisions_with_the_same_parent_name(tmp_path):
    files = []
    for index in range(3):
        folder = tmp_path / f"root{index}" / "shared"
        folder.mkdir(parents=True)
        path = folder / "report.txt"
        path.write_text(str(index), encoding="utf-8")
        files.append(str(path))
    zip_name = str(tmp_path / "collide.zip")

    zip_files(files, zip_name)

    with zipfile.ZipFile(zip_name) as zf:
        assert set(zf.namelist()) == {
            "report.txt",
            "report_shared.txt",
            "report_shared_2.txt",
        }
