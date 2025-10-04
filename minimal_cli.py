from __future__ import annotations

from collections.abc import Sequence
import argparse
from importlib.metadata import PackageNotFoundError, version as resolve_package_version


try:
    __version__ = resolve_package_version("minimal-cli")
except PackageNotFoundError:
    __version__ = "0+unknown"


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
