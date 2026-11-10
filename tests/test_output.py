"""Output-file error handling for the git2md CLI."""

import sys
from unittest import mock

import pytest

import git2md


def test_output_to_missing_directory_exits_nonzero(tmp_path):
    src = tmp_path / "hello.py"
    src.write_text("x = 1\n", encoding="utf-8")
    missing = tmp_path / "no-such-dir" / "out.md"

    with mock.patch.object(
        sys, "argv", ["git2md", str(src), "-o", str(missing)]
    ):
        with pytest.raises(SystemExit) as exc_info:
            git2md.main()

    assert exc_info.value.code == 1
    assert not missing.exists()


def test_output_to_valid_file_succeeds(tmp_path):
    src = tmp_path / "hello.py"
    src.write_text("x = 1\n", encoding="utf-8")
    out = tmp_path / "out.md"

    with mock.patch.object(sys, "argv", ["git2md", str(src), "-o", str(out)]):
        git2md.main()

    assert out.exists()
    assert "hello.py" in out.read_text(encoding="utf-8")
