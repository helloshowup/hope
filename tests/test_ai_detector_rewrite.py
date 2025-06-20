import importlib
import types
import sys
from pathlib import Path

sys.modules.setdefault("requests", types.ModuleType("requests"))
_temp = types.ModuleType("dotenv")
_temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", _temp)

claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [str(claude_dir)]
sys.modules.setdefault("claude_panel", dummy)

ai_module = importlib.import_module("claude_panel.ai_detector")
AIDetector = ai_module.AIDetector


def test_rewrite_calls_claude(monkeypatch, tmp_path):
    file_path = tmp_path / "text.md"
    file_path.write_text("Hello")

    called = {}
    def fake_rewrite(**k):
        called["args"] = k
        return {"edited_content": "NEW"}
    monkeypatch.setattr(ai_module, "rewrite_ai_content", fake_rewrite)
    monkeypatch.setattr(ai_module, "CLAUDE_MODELS", {"CONTENT_EDIT": "model"})
    monkeypatch.setattr(ai_module, "ui", types.SimpleNamespace(toast=lambda *a, **k: None))

    backup_created = []
    def fake_backup(path):
        backup_created.append(path)
        return str(tmp_path / "backup.bak")
    monkeypatch.setattr("showup_core.file_utils.create_timestamped_backup", fake_backup)

    detector = AIDetector(None)
    result = {"detected": True, "content": "Hello", "patterns": []}
    detector._rewrite_content(str(file_path), result)

    assert "args" in called
    assert called["args"]["original_content"] == "Hello"
    assert backup_created
    assert file_path.read_text() == "NEW"
