import git
import pytest

from py_simple_package.src.py_simple.easy_config import (
    EasyConfigError,
    gh_workflow_config,
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
