import git
import pytest

from py_simple_package.src.py_simple.easy_config import (
    EasyConfigError,
    gh_workflow_config,
    create_env_file,
)


def test_gh_workflow_config_writes_template_at_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    gh_workflow_config("issues")

    workflow = tmp_path / ".github" / "workflows" / "issues.yml"
    assert workflow.exists()
    content = workflow.read_text(encoding="utf-8")
    assert "name: issues" in content
    assert "[NAME]" not in content


def test_gh_workflow_config_does_not_overwrite_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow = tmp_path / ".github" / "workflows" / "issues.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("custom workflow\n", encoding="utf-8")

    gh_workflow_config("issues")

    assert workflow.read_text(encoding="utf-8") == "custom workflow\n"


def test_gh_workflow_config_can_target_repository_root(tmp_path, monkeypatch):
    git.Repo.init(tmp_path)
    nested = tmp_path / "nested"
    nested.mkdir()
    monkeypatch.chdir(nested)

    gh_workflow_config("release", at_root=False)

    workflow = tmp_path / ".github" / "workflows" / "release.yml"
    assert workflow.exists()
    assert "name: release" in workflow.read_text(encoding="utf-8")


def test_gh_workflow_config_wraps_template_errors(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def missing_template(_package):
        raise FileNotFoundError("template missing")

    monkeypatch.setattr(
        "py_simple_package.src.py_simple.easy_config.files", missing_template
    )

    with pytest.raises(EasyConfigError, match="template missing"):
        gh_workflow_config("broken")

def test_create_env_file_creates_file_with_variables(tmp_path):
    env_file = tmp_path / ".env"
    create_env_file({"PORT": "8000", "DEBUG": "True"}, file_path=str(env_file))

    assert env_file.exists()
    content = env_file.read_text(encoding="utf-8")
    assert content == "PORT=8000\nDEBUG=True\n"


def test_create_env_file_does_not_overwrite_by_default(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("INITIAL=1\n", encoding="utf-8")

    create_env_file({"PORT": "8000"}, file_path=str(env_file))

    assert env_file.read_text(encoding="utf-8") == "INITIAL=1\n"


def test_create_env_file_overwrites_when_flag_is_true(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("INITIAL=1\n", encoding="utf-8")

    create_env_file({"PORT": "8000"}, file_path=str(env_file), overwrite=True)

    assert env_file.read_text(encoding="utf-8") == "PORT=8000\n"


def test_create_env_file_creates_parent_directories(tmp_path):
    nested_env = tmp_path / "sub" / "config" / ".env"
    create_env_file({"API_KEY": "secret"}, file_path=str(nested_env))

    assert nested_env.exists()
    assert nested_env.read_text(encoding="utf-8") == "API_KEY=secret\n"


def test_create_env_file_wraps_errors(tmp_path, monkeypatch):
    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(EasyConfigError, match="Permission denied"):
        create_env_file({"KEY": "VALUE"}, file_path=str(tmp_path / ".env"))
        