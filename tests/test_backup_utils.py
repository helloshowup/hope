import types
import datetime
from pathlib import Path

import sys

# Provide dummy modules for imports
sys.modules.setdefault("requests", types.ModuleType("requests"))
_temp = types.ModuleType("dotenv")
_temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", _temp)

import importlib

claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [str(claude_dir)]
sys.modules.setdefault("claude_panel", dummy)
sys.modules.setdefault("markdown", types.ModuleType("markdown"))

import showup_core.file_utils as file_utils


class FrozenDatetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2024, 1, 1, 0, 0, 0)


def test_backup_increment(tmp_path, monkeypatch):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("data")

    path_utils = importlib.import_module("claude_panel.path_utils")
    monkeypatch.setattr(path_utils, "get_project_root", lambda: tmp_path)

    monkeypatch.setattr(file_utils.datetime, "datetime", FrozenDatetime)

    first = file_utils.create_timestamped_backup(str(test_file))
    second = file_utils.create_timestamped_backup(str(test_file))

    first_path = Path(first)
    second_path = Path(second)

    assert first_path.name == "sample.txt.bak.20240101_000000"
    assert second_path.name == "sample.txt.bak.20240101_000000_1"
    assert first_path.exists()
    assert second_path.exists()
