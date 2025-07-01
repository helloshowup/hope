import importlib
import json
import sys
import types
from pathlib import Path

sys.modules.setdefault("requests", types.ModuleType("requests"))
_temp = types.ModuleType("dotenv")
_temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", _temp)
sys.modules.setdefault("markdown", types.ModuleType("markdown"))

claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [str(claude_dir)]
sys.modules.setdefault("claude_panel", dummy)

mp_module = importlib.import_module("claude_panel.main_panel")
uc_module = importlib.import_module("claude_panel.user_config")


class DummyVar:
    def __init__(self, value=""):
        self._value = value

    def get(self):
        return self._value

    def set(self, val):
        self._value = val

    def trace(self, *a, **k):
        pass


def test_save_persona_path(monkeypatch, tmp_path):
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(uc_module, "CONFIG_PATH", cfg_path)
    monkeypatch.setattr(mp_module, "user_config", uc_module, raising=False)

    persona_dir = tmp_path / "personas"
    persona_dir.mkdir()

    panel = types.SimpleNamespace(
        persona_path_var=DummyVar(str(persona_dir)),
        update_status=lambda *a, **k: None,
    )

    assert mp_module.ClaudeAIPanel._save_persona_path(panel)
    data = json.loads(cfg_path.read_text())
    assert data["persona_library_root"] == str(persona_dir)


def test_prepopulate_from_config(monkeypatch, tmp_path):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"persona_library_root": "foo"}))
    monkeypatch.setattr(uc_module, "CONFIG_PATH", cfg_path)
    monkeypatch.setattr(mp_module, "user_config", uc_module, raising=False)

    created = {}

    class DummyStringVar(DummyVar):
        def __init__(self, value=""):
            super().__init__(value)
            created["value"] = value

    monkeypatch.setattr(mp_module.tk, "StringVar", DummyStringVar)
    monkeypatch.setattr(mp_module.ttk, "Frame", lambda *a, **k: types.SimpleNamespace(pack=lambda *a, **k: None))
    monkeypatch.setattr(mp_module.ttk, "LabelFrame", lambda *a, **k: types.SimpleNamespace(pack=lambda *a, **k: None))
    monkeypatch.setattr(mp_module.ttk, "Label", lambda *a, **k: types.SimpleNamespace(pack=lambda *a, **k: None))
    monkeypatch.setattr(mp_module.ttk, "Entry", lambda *a, **k: types.SimpleNamespace(pack=lambda *a, **k: None))
    monkeypatch.setattr(mp_module.ttk, "Button", lambda *a, **k: types.SimpleNamespace(pack=lambda *a, **k: None))
    monkeypatch.setattr(mp_module.ttk, "Treeview", lambda *a, **k: types.SimpleNamespace(
        configure=lambda *a, **k: None,
        heading=lambda *a, **k: None,
        column=lambda *a, **k: None,
        bind=lambda *a, **k: None,
        pack=lambda *a, **k: None,
        yview=lambda *a, **k: None,
        xview=lambda *a, **k: None,
    ))
    monkeypatch.setattr(mp_module.ttk, "Scrollbar", lambda *a, **k: types.SimpleNamespace(pack=lambda *a, **k: None, set=lambda *a, **k: None))
    monkeypatch.setattr(mp_module.ClaudeAIPanel, "_browse_library_path", lambda *a, **k: True)
    monkeypatch.setattr(mp_module.ClaudeAIPanel, "_save_library_path", lambda *a, **k: True)
    monkeypatch.setattr(mp_module.ClaudeAIPanel, "_browse_prompt_path", lambda *a, **k: True)
    monkeypatch.setattr(mp_module.ClaudeAIPanel, "_save_prompt_path", lambda *a, **k: True)
    monkeypatch.setattr(mp_module.ClaudeAIPanel, "_browse_persona_path", lambda *a, **k: True)
    monkeypatch.setattr(mp_module.ClaudeAIPanel, "_save_persona_path", lambda *a, **k: True)
    monkeypatch.setattr(mp_module.ClaudeAIPanel, "_populate_library", lambda *a, **k: None)

    panel = mp_module.ClaudeAIPanel.__new__(mp_module.ClaudeAIPanel)
    panel.library_frame = object()
    mp_module.ClaudeAIPanel._setup_library_panel(panel)
    assert panel.persona_path_var.get() == "foo"
