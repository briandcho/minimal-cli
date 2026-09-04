from __future__ import annotations

import argparse
from collections.abc import Sequence
from importlib.metadata import version as resolve_package_version

__version__ = resolve_package_version("minimal-cli")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", action="version", version=__version__)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = create_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
