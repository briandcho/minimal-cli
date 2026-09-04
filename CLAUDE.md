# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A [Copier](https://copier.readthedocs.io/) template repo (`minimal-cli`) that scaffolds a minimal
Python CLI tool project. This is **not** itself an installable/published package — it's a template
plus the tooling to test that the template renders correctly.

- `copier.yml` — the questions asked at generation time (`project_name`, `description`,
  `author_name`, `author_email`) plus `_subdirectory: template`.
- `template/` — the actual generated payload. Files ending in `.jinja` are Jinja-rendered with the
  copier answers and have the suffix stripped on output (e.g.
  `template/{{ python_module }}.py.jinja` → `my_project.py`); files without `.jinja` are copied
  byte-for-byte (this matters for `template/.github/workflows/*.yml`, which use `${{ github.* }}`
  syntax that would otherwise collide with Jinja).
- Everything else at the repo root (`pyproject.toml`, `tests/`, `.pre-commit-config.yaml`,
  `.github/workflows/ci.yml`) is this repo's own dev tooling — used only to verify the template,
  never shipped to generated projects.

**When editing generated-looking files, always edit the source under `template/`, never a copy in
a generated output directory.** When changing something that should appear in every generated
project (e.g. a new tox env, a new classifier), edit `template/pyproject.toml.jinja`; when
changing something about the CLI module/test itself, edit
`template/{{ python_module }}.py.jinja` / `template/tests/{{ python_module }}_test.py.jinja`.

## Commands

Run via `tox`, which drives both testing and pre-commit for **this repo** (not a generated
project):

```sh
tox -e py            # render the template, assert substitutions, install the generated project
                      # into a throwaway venv, and run its own test suite (tests/minimal_cli_test.py)
tox -e pre-commit    # run pre-commit-stage hooks (ruff, ruff-format, mypy, bandit, etc.) — excludes pip-audit and checkov, see below
tox                  # run both py and pre-commit envs
tox -e update_deps   # regenerate requirements-dev.txt via pip-compile and autoupdate pre-commit hooks
```

Run the generation tests directly (bypassing tox) once deps from `requirements-dev.txt` are installed:

```sh
pytest tests/minimal_cli_test.py
```

Lint/format/type-check individually via pre-commit's underlying tools if needed: `ruff check .`, `ruff format .`, `mypy .`.

Manually generate a project from a local checkout to eyeball the output:

```sh
copier copy . /tmp/my-project
```

## Versioning and releases

- **This repo's own git tags matter**: `copier copy https://github.com/briandcho/minimal-cli
  my-project` (no explicit `--vcs-ref`) makes copier fetch the *latest git tag*, not `main`'s
  HEAD. So the tag has to actually point at a commit containing `copier.yml`/`template/` for the
  command in the README to work — a stale or missing tag silently serves an old/broken template.
- `.github/workflows/release.yml` at the repo root is **manual-only** (`workflow_dispatch`, no
  `push` trigger) — running `python-semantic-release version --no-changelog --no-commit`, which
  tags `vX.Y.Z` from Conventional Commits, pushes the tag, and publishes a GitHub Release, but only
  when someone deliberately runs the workflow. It has no `pypi_token` and never builds/publishes
  anything — this repo isn't a package, tagging is purely so `copier copy` has something current to
  resolve. There's no root `CHANGELOG.md`: it would just duplicate the notes on the GitHub Release
  page this step already publishes, and nothing here consumes it (this repo isn't installed as a
  package). (`tests/minimal_cli_test.py`'s own `generate()` sidesteps tag resolution entirely by
  passing `vcs_ref="HEAD"`, so local test runs always exercise the current checkout regardless of
  tags.)
- If this repo ever opens to real external code contributions, revisit this: `commitizen`'s
  Conventional-Commit enforcement is a local git hook contributors won't have installed, and
  `googleapis/release-please-action` (a PR-based release flow versioned from Conventional-Commit-
  style PR titles, going through normal PR review rather than a one-off manual trigger) would be
  a better fit at that point.
- The workflows shipped inside `template/.github/workflows/` (`ci.yml`, `release.yml`,
  `auto-update-deps.yml`) are a *separate*, unrelated release process — the *generated* project's
  own versioning (`setuptools-scm` git-tag-based versioning, its own `python-semantic-release` run,
  PyPI publish on `v*` tags). See those files directly for that behavior; don't confuse the two.
- Commit messages in this repo must follow Conventional Commits — enforced by a Commitizen
  `commit-msg` hook. Install hooks with
  `pre-commit install --hook-type pre-commit --hook-type pre-push --hook-type commit-msg`.
- `pip-audit` (network-bound dependency vulnerability scan, against `requirements-dev.txt`) and
  `checkov` (IaC scanner, against `.github/workflows/` at the repo root only) are scoped to
  `stages: [pre-push]` in `.pre-commit-config.yaml`, so they're excluded from
  `tox -e pre-commit`/the default commit-time hook run to keep local iteration fast. They still
  run on `git push` (if the `pre-push` hook type is installed) and as standalone steps in CI's
  `security` job (`.github/workflows/ci.yml`).

## Adding functionality

- New copier questions/answers go in `copier.yml`.
- New CLI behavior for the *generated* project extends `create_parser()`/`main()` in
  `template/{{ python_module }}.py.jinja` (mirrors the current single-module scaffold; if it grows
  enough to need a package directory, `template/pyproject.toml.jinja`'s setuptools config would
  need updating too).
- New assertions about what the generated project should look like go in
  `tests/minimal_cli_test.py` at the repo root.
