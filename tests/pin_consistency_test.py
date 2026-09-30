"""Drift safety net for version pins that neither Dependabot nor pip-compile can reach.

Dependabot's github-actions ecosystem only ever scans the literal `.github/workflows/` path, so
it can't see `template/.github/workflows/*.yml` (copier payload, not a real GitHub-executed
workflow location in this repo). And a handful of tool versions are pinned as literal strings
inside `run:` steps (not `uses:` refs, not requirements files), invisible to any automated
updater. These tests don't pin exact versions themselves -- they just assert that wherever the
same tool is pinned in more than one place, those places agree, so a bump in one spot that's
missed in its counterpart fails CI instead of silently drifting.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ROOT_CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"
TEMPLATE_CI = REPO_ROOT / "template" / ".github" / "workflows" / "ci.yml"
ROOT_RELEASE = REPO_ROOT / ".github" / "workflows" / "release.yml"
TEMPLATE_RELEASE = REPO_ROOT / "template" / ".github" / "workflows" / "release.yml"
ROOT_PRE_COMMIT = REPO_ROOT / ".pre-commit-config.yaml"
TEMPLATE_PRE_COMMIT = REPO_ROOT / "template" / ".pre-commit-config.yaml"

# Actions used by both this repo's own workflows and their template counterparts, and expected
# to be pinned to the same version in both places.
SHARED_ACTIONS = [
    "actions/checkout",
    "actions/setup-python",
    "actions/cache",
    "trufflesecurity/trufflehog",
]


def extract_action_versions(text: str) -> dict[str, set[str]]:
    versions: dict[str, set[str]] = {}
    for owner_repo, ref in re.findall(r"uses:\s*([\w.-]+/[\w.-]+)@(\S+)", text):
        versions.setdefault(owner_repo, set()).add(ref)
    return versions


def test_shared_action_pins_match_between_root_and_template_ci():
    root_versions = extract_action_versions(ROOT_CI.read_text())
    template_versions = extract_action_versions(TEMPLATE_CI.read_text())

    for action in SHARED_ACTIONS:
        assert action in root_versions, f"{action} not found in {ROOT_CI}"
        assert action in template_versions, f"{action} not found in {TEMPLATE_CI}"
        assert root_versions[action] == template_versions[action], (
            f"{action} pinned to {root_versions[action]} in {ROOT_CI} but "
            f"{template_versions[action]} in {TEMPLATE_CI}"
        )


def test_shared_action_pins_match_between_root_and_template_release():
    root_versions = extract_action_versions(ROOT_RELEASE.read_text())
    template_versions = extract_action_versions(TEMPLATE_RELEASE.read_text())

    for action in ("actions/checkout", "actions/setup-python"):
        assert root_versions[action] == template_versions[action], (
            f"{action} pinned to {root_versions[action]} in {ROOT_RELEASE} but "
            f"{template_versions[action]} in {TEMPLATE_RELEASE}"
        )


def test_python_semantic_release_version_matches_root_and_template_release():
    root_match = re.search(
        r"pip install python-semantic-release==([\d.]+)", ROOT_RELEASE.read_text()
    )
    template_match = re.search(
        r"python-semantic-release/python-semantic-release@v([\d.]+)",
        TEMPLATE_RELEASE.read_text(),
    )
    assert root_match, f"python-semantic-release pip pin not found in {ROOT_RELEASE}"
    assert template_match, (
        f"python-semantic-release action pin not found in {TEMPLATE_RELEASE}"
    )
    assert root_match.group(1) == template_match.group(1), (
        f"python-semantic-release=={root_match.group(1)} in {ROOT_RELEASE} but "
        f"@v{template_match.group(1)} in {TEMPLATE_RELEASE}"
    )


def test_checkov_version_matches_pre_commit_and_inline_pip_install():
    for pre_commit_path, ci_path in (
        (ROOT_PRE_COMMIT, ROOT_CI),
        (TEMPLATE_PRE_COMMIT, TEMPLATE_CI),
    ):
        pre_commit_match = re.search(
            r"repo: https://github.com/bridgecrewio/checkov\s*\n\s*rev:\s*([\d.]+)",
            pre_commit_path.read_text(),
        )
        ci_match = re.search(r"checkov==([\d.]+)", ci_path.read_text())
        assert pre_commit_match, f"checkov rev not found in {pre_commit_path}"
        assert ci_match, f"checkov==<version> not found in {ci_path}"
        assert pre_commit_match.group(1) == ci_match.group(1), (
            f"checkov {pre_commit_match.group(1)} in {pre_commit_path} but "
            f"{ci_match.group(1)} in {ci_path}"
        )


def test_python_version_literals_consistent_across_root_and_template_workflows():
    single_version_re = re.compile(r"python-version:\s*'([\d.]+)'")
    matrix_re = re.compile(r"python-version:\s*\[(\"[\d., \"]+)\]")

    root_ci_versions = set(single_version_re.findall(ROOT_CI.read_text()))
    template_ci_versions = set(single_version_re.findall(TEMPLATE_CI.read_text()))
    assert root_ci_versions == template_ci_versions == {"3.11"}

    root_matrix = matrix_re.search(ROOT_CI.read_text())
    template_matrix = matrix_re.search(TEMPLATE_CI.read_text())
    assert root_matrix and template_matrix
    assert root_matrix.group(1) == template_matrix.group(1)

    root_release_version = single_version_re.findall(ROOT_RELEASE.read_text())
    template_release_version = single_version_re.findall(TEMPLATE_RELEASE.read_text())
    assert root_release_version == template_release_version == ["3.12"]


def test_template_requirements_source_uses_project_name_placeholder():
    for name in ("requirements.txt.jinja", "requirements-dev.txt.jinja"):
        content = (REPO_ROOT / "template" / name).read_text()
        assert "my-project" not in content
