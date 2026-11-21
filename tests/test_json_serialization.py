import json

import pytest

from py_simple_package.src.py_simple.easy_json import (
    EasyJsonError,
    save_json_data,
    update_json,
)


@pytest.fixture(params=["set", "object", "cycle"])
def invalid_data(request):
    if request.param == "cycle":
        data = {}
        data["cycle"] = data
        return data
    return {"valid": 1, "invalid": {1, 2} if request.param == "set" else object()}


def test_update_json_preserves_original_on_serialization_error(tmp_path, invalid_data):
    path = tmp_path / "config.json"
    original = b'{"keep": "original", "version": 1}\n'
    path.write_bytes(original)

    with pytest.raises(EasyJsonError):
        update_json(str(path), invalid_data)

    assert path.read_bytes() == original


def test_save_json_does_not_create_file_on_serialization_error(tmp_path, invalid_data):
    path = tmp_path / "config.json"

    with pytest.raises(EasyJsonError):
        save_json_data(str(path), invalid_data)

    assert not path.exists()
    save_json_data(str(path), {"retry": True})
    assert json.loads(path.read_text(encoding="utf-8")) == {"retry": True}


@pytest.mark.parametrize("operation", [save_json_data, update_json])
def test_json_serialization_preserves_output_format(tmp_path, operation):
    path = tmp_path / "config.json"
    if operation is update_json:
        path.write_text("{}", encoding="utf-8")
    data = {"name": "Žan", "nested": [True, None, 1.25]}

    operation(str(path), data)

    assert path.read_text(encoding="utf-8") == json.dumps(data, indent=4)
