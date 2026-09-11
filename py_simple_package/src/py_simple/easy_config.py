"""
easy_config aims to simplify creating configuration files.
"""

import os
from importlib.resources import files

import git


class EasyConfigError(Exception):
    """
    Raised when a config file could not be written.
    This wraps the underlying error (missing template, permission
    denied, no git repository found) so callers only have to catch one
    exception type instead of several.
    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def gh_workflow_config(filename: str, at_root: bool = True) -> None:
    """
    Creates a starter GitHub Actions workflow file from a template.
    The workflow is written to '.github/workflows/<filename>.yml', with
    the placeholder '[NAME]' in the template replaced by filename. Any
    missing folders are created. If the file already exists it is left
    alone.
    Args:
        filename (str): Name for the workflow, without the '.yml'
            extension (e.g. 'issues' -> '.github/workflows/issues.yml').
        at_root (bool, optional): When True, the path is relative to the
            current working directory. When False, the git repository
            root is looked up and the workflow is placed there.
            Defaults to True.
    Returns:
        None
    Raises:
        EasyConfigError: If the template cannot be read or the workflow
            file cannot be written.
    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import gh_workflow_config

            gh_workflow_config("issues")
            ```

        === "The Traditional Way"
            ```python
            import os

            os.makedirs(".github/workflows", exist_ok=True)
            with open(".github/workflows/issues.yml", "w",
                      encoding="utf-8") as f:
                f.write(
                    "name: issues\n"
                    "\n"
                    "on:\n"
                    "\n"
                    "jobs:\n"
                    "  build:\n"
                    "    runs-on: ubuntu-latest\n"
                    "\n"
                    "    steps:\n"
                    "      - uses: actions/checkout@v7\n"
                    "      - name:\n"
                    "        run:\n"
                )
            ```
    """
    if at_root:
        workflow_path = f".github/workflows/{filename}.yml"
    else:
        git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
        workflow_path = f"{git_root}/.github/workflows/{filename}.yml"
    try:
        if not os.path.exists(workflow_path):
            template_path = (
                files("py_simple") / "config_templates" / "workflow-template.yml"
            )
            with template_path.open(encoding="utf-8") as f:
                template = f.readlines()
            os.makedirs(os.path.dirname(workflow_path), exist_ok=True)
            with open(workflow_path, "w", encoding="utf-8") as f:
                for line in template:
                    if "[NAME]" in line:
                        f.write(line.replace("[NAME]", filename))
                    else:
                        f.write(line)
    except Exception as e:
        raise EasyConfigError(f"\n\n\nERROR: {e}") from None
