import sys
import types
from pathlib import Path

import pytest

# Provide dummy modules required by project imports
temp = types.ModuleType("dotenv")
temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", temp)
sys.modules.setdefault("requests", types.ModuleType("requests"))


def process_file(path: Path, edit_func):
    original = path.read_text()
    new_content = edit_func(markdown_text=original)
    if new_content.strip() == original.strip():
        raise RuntimeError("No edits applied \u2013 file left unchanged")
    path.write_text(new_content)


def test_no_overwrite_when_unchanged(tmp_path):
    file_path = tmp_path / "doc.md"
    file_path.write_text("hello")

    def same_edit(**kwargs):
        return kwargs["markdown_text"]

    with pytest.raises(RuntimeError):
        process_file(file_path, same_edit)

    assert file_path.read_text() == "hello"
    assert not (tmp_path / "doc.md.bak").exists()
