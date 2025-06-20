import importlib
import json
import sys
import types
from pathlib import Path

import pytest


def _load_config_manager(monkeypatch, tmp_path: Path):
    claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
    dummy = types.ModuleType("claude_panel")
    dummy.__path__ = [str(claude_dir)]
    sys.modules["claude_panel"] = dummy

    path_utils = importlib.import_module("claude_panel.path_utils")
    monkeypatch.setattr(path_utils, "get_project_root", lambda: tmp_path)

    if "claude_panel.config_manager" in sys.modules:
        del sys.modules["claude_panel.config_manager"]
    cfg_module = importlib.import_module("claude_panel.config_manager")
    return cfg_module.ConfigManager()


def test_load_single_settings(monkeypatch, tmp_path):
    data = {"foo": "bar"}
    (tmp_path / "settings.json").write_text(json.dumps(data))
    (tmp_path / "showup-editor-ui").mkdir()
    cm = _load_config_manager(monkeypatch, tmp_path)
    assert cm.load_settings() == data


def test_duplicate_settings_error(monkeypatch, tmp_path):
    (tmp_path / "settings.json").write_text("{}")
    dup_dir = tmp_path / "showup-editor-ui"
    dup_dir.mkdir()
    (dup_dir / "settings.json").write_text("{}")
    cm = _load_config_manager(monkeypatch, tmp_path)
    with pytest.raises(ValueError):
        cm.load_settings()
