<!-- .github/copilot-instructions.md
This file is intended to help AI coding agents be productive in this repository.
When something is unclear, prefer small, reversible changes and open a draft PR with a clear description.
-->

# Copilot / AI agent guidance for Minimal CLI

Purpose: quick, targeted guidance so an AI can make useful edits in this small Python CLI project.

Key facts (discoverable):
- This repo contains a minimal Python CLI scaffold: `minimal_cli.py`, test file `minimal_cli_test.py`, `pyproject.toml`, and dependency stubs `requirements.in` / `requirements-dev.in`.
- At the moment these files are empty; implementers should open and modify them directly.

Big-picture architecture and intent
- Single-module CLI: the executable surface is expected to live in `minimal_cli.py` (export functions and/or a `main()` entrypoint).
- Tests live beside the module in `minimal_cli_test.py` and follow a pytest-style naming convention (filename ends with `_test.py`).
- Packaging/build metadata should be in `pyproject.toml` if/when the project is packaged.

Developer workflows (how to run, build, test)
- Run tests: prefer pytest. Example: run `pytest -q` from the repository root.
- Install dependencies: this repo exposes `requirements.in` and `requirements-dev.in`. Common workflows:
  - If there is a generated `requirements.txt` use `python -m pip install -r requirements.txt`.
  - Otherwise, use `pip install -r requirements-dev.in` for editable/dev installs, or run `pip-compile` if the project uses pip-tools.
- If `pyproject.toml` defines a build backend (PEP 517), use the configured tooling (for example `python -m build`) — inspect `pyproject.toml` before changing packaging.

Project-specific conventions and patterns
- Small, focused changes: given this is a minimal scaffold, avoid adding large frameworks or heavy dependencies without justification.
- CLI structure: implement a `def main(argv: Sequence[str] | None = None) -> int:` function that returns an exit code (0 on success). Expose pure helper functions for logic so tests can import them directly from `minimal_cli.py`.
- Tests: keep tests small and deterministic. Example pattern the tests will expect:
  - `from minimal_cli import some_function, main`
  - call helper functions directly and assert outputs; call `main(['--help'])` where useful.

Integration points and external dependencies
- No external services are present in the repository. If you add network calls, make them injectable (pass a session/client into functions) so tests can monkeypatch or use pytest fixtures.

What to change and how to structure commits
- When implementing features, prefer small commits that add:
  1. A failing test in `minimal_cli_test.py` that demonstrates intended behavior.
  2. Minimal implementation in `minimal_cli.py` to make the test pass.
  3. Update `pyproject.toml` only if packaging/entry points are required (add `[project.scripts]` or `[tool.poetry.scripts]` as the last step).
- Keep README.md and LICENSE unchanged unless you are updating usage docs to match implemented behavior.

Examples from this repo
- Implement CLI behavior in `minimal_cli.py` and make tests in `minimal_cli_test.py` import functions from that module.
- If you add an entry point, update `pyproject.toml` rather than creating a stand-alone script.

Assumptions and clarifications the agent should surface in PRs
- Several files are empty — the guidance above assumes the intended layout described here. If the maintainer has a different intention (packaging style, dependency management), ask in the PR description.

When in doubt
- Leave comments in code explaining non-obvious choices and open a draft PR with a short summary of what you changed and why. Tag the maintainer for review.

End of file
