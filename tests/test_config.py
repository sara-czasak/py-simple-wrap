import git
import pytest

from py_simple_package.src.py_simple.easy_config import (
    EasyConfigError,
    gh_workflow_config,
    create_env_file,
    read_env_file,
    gitignore_config,
    requirements_config,
)
from py_simple import gitignore_config as top_level_gitignore_config


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


def test_read_env_file_reads_key_value_pairs(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8000\nDEBUG=True\n", encoding="utf-8")

    assert read_env_file(str(env_file)) == {
        "PORT": "8000",
        "DEBUG": "True",
    }


def test_read_env_file_ignores_blank_lines_and_comments(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# local config\n\nPORT=8000\nINVALID_LINE\n# ignored\nDEBUG=True\n",
        encoding="utf-8",
    )

    assert read_env_file(str(env_file)) == {
        "PORT": "8000",
        "DEBUG": "True",
    }


def test_read_env_file_strips_key_value_whitespace(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(" PORT = 8000 \n DEBUG = True \n", encoding="utf-8")

    assert read_env_file(str(env_file)) == {
        "PORT": "8000",
        "DEBUG": "True",
    }


def test_read_env_file_keeps_equals_signs_in_values(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("DATABASE_URL=postgres://user:p=a@s/db\n", encoding="utf-8")

    assert read_env_file(str(env_file)) == {
        "DATABASE_URL": "postgres://user:p=a@s/db",
    }


def test_read_env_file_wraps_missing_file_error(tmp_path):
    with pytest.raises(EasyConfigError, match="does_not_exist"):
        read_env_file(str(tmp_path / "does_not_exist.env"))


def test_gitignore_config_creates_file_at_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    gitignore_config()

    gitignore_file = tmp_path / ".gitignore"
    assert gitignore_file.exists()
    content = gitignore_file.read_text(encoding="utf-8")
    assert "__pycache__/" in content
    assert "*.py[cod]" in content
    assert ".venv/" in content
    assert ".env" in content


def test_gitignore_config_does_not_overwrite_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text("custom gitignore\n", encoding="utf-8")

    gitignore_config()

    assert gitignore_file.read_text(encoding="utf-8") == "custom gitignore\n"


def test_gitignore_config_can_target_repository_root(tmp_path, monkeypatch):
    git.Repo.init(tmp_path)
    nested = tmp_path / "nested"
    nested.mkdir()
    monkeypatch.chdir(nested)

    gitignore_config(at_root=False)

    gitignore_file = tmp_path / ".gitignore"
    assert gitignore_file.exists()
    content = gitignore_file.read_text(encoding="utf-8")
    assert "__pycache__/" in content
    assert not (nested / ".gitignore").exists()


def test_gitignore_config_wraps_template_errors(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def missing_template(_package):
        raise FileNotFoundError("template missing")

    monkeypatch.setattr(
        "py_simple_package.src.py_simple.easy_config.files", missing_template
    )

    with pytest.raises(EasyConfigError, match="template missing"):
        gitignore_config()


def test_gitignore_config_wraps_git_errors(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(EasyConfigError):
        gitignore_config(at_root=False)


def test_gitignore_config_wraps_permission_errors(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(EasyConfigError, match="Permission denied"):
        gitignore_config()


def test_gitignore_config_imported_from_py_simple():
    assert callable(top_level_gitignore_config)

def test_requirements_config_creates_file(tmp_path):
    requirements_file = tmp_path / "requirements.txt"

    requirements_config(
        ["numpy", "pandas", "scikit-learn"],
        file_path=str(requirements_file),
    )

    assert requirements_file.exists()
    assert requirements_file.read_text(encoding="utf-8") == (
        "numpy\n"
        "pandas\n"
        "scikit-learn\n"
    )

def test_requirements_config_does_not_overwrite_by_default(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text("old-package\n", encoding="utf-8")

    requirements_config(
        ["numpy", "pandas"],
        file_path=str(requirements_file),
    )

    assert requirements_file.read_text(encoding="utf-8") == "old-package\n"
    
def test_requirements_config_overwrites_when_flag_is_true(tmp_path):
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text("old-package\n", encoding="utf-8")

    requirements_config(
        ["numpy", "pandas"],
        file_path=str(requirements_file),
        overwrite=True,
    )

    assert requirements_file.read_text(encoding="utf-8") == (
        "numpy\n"
        "pandas\n"
    )
    
def test_requirements_config_creates_parent_directories(tmp_path):
    requirements_file = tmp_path / "config" / "requirements.txt"

    requirements_config(
        ["numpy", "pandas"],
        file_path=str(requirements_file),
    )

    assert requirements_file.exists()
    assert requirements_file.read_text(encoding="utf-8") == (
        "numpy\n"
        "pandas\n"
    )
    
def test_requirements_config_wraps_errors(tmp_path, monkeypatch):
    requirements_file = tmp_path / "requirements.txt"

    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(EasyConfigError):
        requirements_config(
            ["numpy"],
            file_path=str(requirements_file),
        )
        
def test_requirements_config_imported_from_py_simple():
    from py_simple import requirements_config as imported_function

    assert callable(imported_function)
