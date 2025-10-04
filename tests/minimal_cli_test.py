import pytest

from minimal_cli import main, __version__


@pytest.mark.parametrize(
    "flag",
    [
        "--version",
        "-V",
    ],
)
def test_version_string(flag, capsys):
    with pytest.raises(SystemExit) as exc:
        main([flag])
    assert exc.value.code == 0
    out, _ = capsys.readouterr()
    assert out.strip() == __version__


def test_main_without_args():
    assert main() == 0
