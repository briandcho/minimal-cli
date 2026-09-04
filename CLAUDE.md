# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal Python CLI tool scaffold (`minimal-cli`), currently just an argument parser exposing `--version`/`-V`. The whole implementation is `minimal_cli.py`; everything else in the repo is packaging/tooling config.

## Commands

Run via `tox`, which drives both testing and pre-commit:

```sh
tox -e py            # run tests with coverage (pytest + coverage report)
tox -e pre-commit    # run all pre-commit hooks (ruff, ruff-format, mypy, bandit, etc.)
tox                  # run both py and pre-commit envs
tox -e update_deps   # regenerate requirements*.txt via pip-compile and autoupdate pre-commit hooks
```

Run a single test directly (bypassing tox) once deps from `requirements-dev.txt` are installed:

```sh
pytest tests/minimal_cli_test.py -k test_version_string
```

Lint/format/type-check individually via pre-commit's underlying tools if needed: `ruff check .`, `ruff format .`, `mypy .`.

## Versioning and releases

- Package version comes from `setuptools-scm` (git tags), not a hardcoded string — `__version__` in `minimal_cli.py` resolves via `importlib.metadata.version("minimal-cli")`, which requires the package to be installed in the running environment; it raises `PackageNotFoundError` if run from an uninstalled checkout (e.g. `python minimal_cli.py` without `pip install -e .` first).
- CI (`.github/workflows/ci.yml`) runs security scans, tests across Python 3.10–3.14, then builds. Pushing a `v*` tag triggers `publish` to PyPI via trusted `TWINE_PASSWORD`/`twine upload`.
- Commit messages must follow Conventional Commits — enforced by a Commitizen `commit-msg` hook. Install hooks with `pre-commit install --hook-type pre-commit --hook-type commit-msg`.

## Adding functionality

New CLI behavior extends `create_parser()`/`main()` in `minimal_cli.py`. Since this is a single-module package (see `pyproject.toml` `scripts.minimal-cli = "minimal_cli:main"`), keep new code in that module unless it grows enough to justify splitting into a package directory (would require updating `pyproject.toml`'s setuptools config accordingly).
