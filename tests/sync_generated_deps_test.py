from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from sync_generated_deps import sync_requirements


def test_sync_requirements_replaces_project_name_and_copies_pre_commit_config(tmp_path):
    throwaway = tmp_path / "throwaway"
    throwaway.mkdir()
    template_dir = tmp_path / "template"
    template_dir.mkdir()

    (throwaway / "requirements.txt").write_text(
        "some-pkg==1.0.0\n    # via my-project (pyproject.toml)\n"
    )
    (throwaway / "requirements-dev.txt").write_text(
        "covdefaults==2.3.0\n    # via my-project (pyproject.toml)\n"
    )
    (throwaway / ".pre-commit-config.yaml").write_text("repos: []\n")

    sync_requirements(throwaway, template_dir, "my-project")

    requirements = (template_dir / "requirements.txt.jinja").read_text()
    assert "my-project" not in requirements
    assert "# via {{ project_name }} (pyproject.toml)" in requirements

    requirements_dev = (template_dir / "requirements-dev.txt.jinja").read_text()
    assert "my-project" not in requirements_dev
    assert "# via {{ project_name }} (pyproject.toml)" in requirements_dev

    assert (template_dir / ".pre-commit-config.yaml").read_text() == "repos: []\n"


def test_sync_requirements_is_a_no_op_when_project_name_does_not_appear(tmp_path):
    throwaway = tmp_path / "throwaway"
    throwaway.mkdir()
    template_dir = tmp_path / "template"
    template_dir.mkdir()

    (throwaway / "requirements.txt").write_text("some-pkg==1.0.0\n")
    (throwaway / "requirements-dev.txt").write_text("covdefaults==2.3.0\n")
    (throwaway / ".pre-commit-config.yaml").write_text("repos: []\n")

    sync_requirements(throwaway, template_dir, "my-project")

    assert (template_dir / "requirements.txt.jinja").read_text() == "some-pkg==1.0.0\n"
    assert (
        template_dir / "requirements-dev.txt.jinja"
    ).read_text() == "covdefaults==2.3.0\n"
