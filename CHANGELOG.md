# CHANGELOG

## v1.0.1 (2026-09-04)

### Fix

* fix(ci): pin trufflehog action to a real release tag

The floating `@v3` tag on trufflesecurity/trufflehog no longer exists
upstream (they only publish precise `vX.Y.Z` tags now), which broke
the security job&#39;s &#34;Set up job&#34; step on push. Pin to v3.97.4 in both
this repo&#39;s own ci.yml and the copy shipped inside template/ for
generated projects.

Co-Authored-By: Claude Sonnet 5 &lt;noreply@anthropic.com&gt;
Claude-Session: https://claude.ai/code/session_01MkpJdUbmXe6dt5zmrUjNWp ([`2b8b67a`](https://github.com/briandcho/minimal-cli/commit/2b8b67a0f0c602529672ce13a0595d6d47971ba2))

## v1.0.0 (2026-09-04)

### Breaking

* feat!: convert repo into a Copier template

Move the CLI scaffold under template/ (Jinja-rendered where it needs
project_name/description/author substitutions, verbatim elsewhere so
GitHub Actions&#39; ${{ }} syntax doesn&#39;t collide with Jinja) and add
copier.yml with _subdirectory: template, so `copier copy
https://github.com/briandcho/minimal-cli my-project` scaffolds a new
CLI project.

The repo root is repurposed into meta-tooling that only tests the
template: pyproject.toml/tox no longer describe an installable
package, and tests/minimal_cli_test.py renders the template end-to-end
(via the copier API, substitution assertions, then an install + pytest
run of the generated project in a throwaway venv) instead of testing
minimal_cli.py directly.

Since `copier copy` resolves the latest git tag by default (not
main&#39;s HEAD), add a root release.yml that runs python-semantic-release
on every push to main to keep a current tag available - separate from
template/release.yml, which governs the *generated* project&#39;s own
PyPI release process.

Co-Authored-By: Claude Sonnet 5 &lt;noreply@anthropic.com&gt;
Claude-Session: https://claude.ai/code/session_01MkpJdUbmXe6dt5zmrUjNWp ([`411f6c4`](https://github.com/briandcho/minimal-cli/commit/411f6c4c2d754735a2d605bbad395749b5a21046))

### Chore

* chore: pip-tools/pre-commit updates ([`e22402a`](https://github.com/briandcho/minimal-cli/commit/e22402a7a6ebf8a0dabf790d5ec196611d47ce17))

### Fix

* fix: install project package in tox py env for version resolution

Removing the __version__ fallback exposed that skipsdist=true prevented
tox from installing the package into any testenv, so importlib.metadata
lookups failed under tox -e py. Drop skipsdist and use usedevelop=true
for an editable install instead.

Also add CLAUDE.md documenting repo commands and architecture.

Co-Authored-By: Claude Sonnet 5 &lt;noreply@anthropic.com&gt;
Claude-Session: https://claude.ai/code/session_01BKGq93JoU3W9wk43yc5z6d ([`cc41647`](https://github.com/briandcho/minimal-cli/commit/cc41647936794140fbc72baa9afec1ca7805dad6))

### Performance

* perf: defer checkov to pre-push to speed up local pre-commit

checkov&#39;s IaC scan was adding noticeable time to every tox -e
pre-commit run. Scope it to the pre-push hook stage alongside
pip-audit, and add it as a standalone CI step so coverage isn&#39;t lost
for workflows that don&#39;t install git hooks locally.

Co-Authored-By: Claude Sonnet 5 &lt;noreply@anthropic.com&gt;
Claude-Session: https://claude.ai/code/session_0168oeQFkLH18jZzZusZgPFY ([`c2a8602`](https://github.com/briandcho/minimal-cli/commit/c2a8602f826d377bb320313d2cb0ed372a86cf6f))

* perf: defer pip-audit to pre-push to speed up local pre-commit

pip-audit&#39;s network-bound scan was adding ~8s to every tox -e pre-commit
run. Scope it to the pre-push hook stage instead, and add it as a
standalone CI step so coverage isn&#39;t lost for workflows that don&#39;t
install git hooks locally.

Co-Authored-By: Claude Sonnet 5 &lt;noreply@anthropic.com&gt;
Claude-Session: https://claude.ai/code/session_0168oeQFkLH18jZzZusZgPFY ([`2fb00e5`](https://github.com/briandcho/minimal-cli/commit/2fb00e53032e69eb8ad1fb2453ef8d574d35cbdf))

### Refactor

* refactor: modernize tox config to native pyproject.toml format

tox 4 supports [tool.tox] natively now, so the legacy_tox_ini escape
hatch (an embedded ini string) is no longer needed. Converted to native
tables/dotted-keys; pyproject-fmt normalized usedevelop=true to the
more idiomatic package=&#34;editable&#34;. Verified tox -av, tox -e py,
tox -e pre-commit, tox c -e update_deps, and a full tox run all behave
identically to the previous ini-based config.

Co-Authored-By: Claude Sonnet 5 &lt;noreply@anthropic.com&gt;
Claude-Session: https://claude.ai/code/session_01BKGq93JoU3W9wk43yc5z6d ([`ce71895`](https://github.com/briandcho/minimal-cli/commit/ce718959845988a419502ddcb1d394728254c8c9))

* refactor: drop uninstalled-package version fallback

Require the package to be installed for __version__ resolution instead of
silently falling back to &#34;0+unknown&#34; when running the file directly from
an uninstalled checkout. ([`7d5cfbb`](https://github.com/briandcho/minimal-cli/commit/7d5cfbb26450fdd02cec6ba09e59a29585df88d4))

## v0.1.0 (2026-01-18)

### Feature

* feat: initial commit ([`a1ef5ff`](https://github.com/briandcho/minimal-cli/commit/a1ef5ff59cf82c94e1bb36225a9c1f79ed4f4b8a))
