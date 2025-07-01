import importlib
import sys
import types
from pathlib import Path

import pytest


def _setup_claude_panel(monkeypatch) -> None:
    claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
    dummy = types.ModuleType("claude_panel")
    dummy.__path__ = [str(claude_dir)]
    sys.modules["claude_panel"] = dummy
    # ensure reload for subsequent imports
    if "showup_editor.config" in sys.modules:
        del sys.modules["showup_editor.config"]


def test_get_persona_library_root(monkeypatch, tmp_path):
    _setup_claude_panel(monkeypatch)
    uc_module = importlib.import_module("claude_panel.user_config")
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(uc_module, "CONFIG_PATH", cfg_path)
    persona_dir = tmp_path / "personas"
    uc_module.save_config({"persona_library_root": str(persona_dir)})

    cfg_module = importlib.import_module("showup_editor.config")
    assert cfg_module.get_persona_library_root() == persona_dir


def test_missing_persona_library_root(monkeypatch, tmp_path):
    _setup_claude_panel(monkeypatch)
    uc_module = importlib.import_module("claude_panel.user_config")
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(uc_module, "CONFIG_PATH", cfg_path)
    uc_module.save_config({})

    cfg_module = importlib.import_module("showup_editor.config")
    with pytest.raises(ValueError):
        cfg_module.get_persona_library_root()

