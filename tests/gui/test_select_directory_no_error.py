# ruff: noqa: E402
import importlib
import sys
import types
from pathlib import Path

sys.modules.setdefault("requests", types.ModuleType("requests"))
_temp = types.ModuleType("dotenv")
_temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", _temp)
sys.modules.setdefault("markdown", types.ModuleType("markdown"))

claude_dir = Path(__file__).resolve().parents[2] / "showup-editor-ui" / "claude_panel"
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [str(claude_dir)]
sys.modules.setdefault("claude_panel", dummy)

mp_module = importlib.import_module("claude_panel.main_panel")
ClaudeAIPanel = mp_module.ClaudeAIPanel


class FakeTree:
    def __init__(self, path: Path, kind: str):
        self._path = str(path)
        self._kind = kind

    def selection(self):
        return ["item"]

    def item(self, _id, _key=None):
        return (self._path, self._kind)


def test_select_directory_no_error(tmp_path, monkeypatch):
    folder = tmp_path / "dir"
    folder.mkdir()

    tree = FakeTree(folder, "directory")
    events = []

    def fake_showerror(*a, **k):
        events.append("error")

    def fake_load(path):
        events.append("load")

    enrich = types.SimpleNamespace(load_current_lesson=fake_load)
    panel = types.SimpleNamespace(file_tree=tree, enrich_lesson=enrich)

    monkeypatch.setattr(mp_module.messagebox, "showerror", fake_showerror)

    ClaudeAIPanel._on_file_select(panel, object())

    assert events == []
