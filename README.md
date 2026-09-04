# Minimal CLI

This is a minimal Python CLI tool scaffold.

## Installation

Install from PyPI:

```sh
pip install minimal-cli
```

## Usage

Run the CLI and display the version:

```sh
minimal-cli --version
# or
minimal-cli -V
```

## Development

### Install pre-commit hooks (including commit message checks)

This repo enforces Conventional Commits via a `commit-msg` hook (Commitizen). Most checks run on every commit; `pip-audit` (a network-bound dependency vulnerability scan) and `checkov` (an IaC scanner) are deferred to `pre-push` so they don't slow down every commit.

Install hooks locally:

```sh
pre-commit install --hook-type pre-commit --hook-type pre-push --hook-type commit-msg
# optional: run all hooks (including pip-audit) against the repo once
pre-commit run --all-files --hook-stage pre-push
```

If you see a commit rejected, format your message using Conventional Commits, for example:

```text
feat: add new subcommand
fix(cli): handle empty args
chore(deps): weekly dependency updates
```

You can also use Commitizen to guide you:

```sh
cz commit
# or without installing: pipx run commitizen commit
```

### Use tox for development

This project uses `tox` to run tests and checks consistently across environments.

- Run tests and coverage:

```sh
tox -e py
```

- Run all pre-commit hooks (format, lint, type-check, security, etc.):

```sh
tox -e pre-commit
```

- Update pinned dependencies and pre-commit hooks:

```sh
tox -e update_deps
```
