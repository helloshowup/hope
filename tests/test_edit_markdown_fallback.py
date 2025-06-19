import importlib
import logging
import sys
import types
from pathlib import Path

sys.modules.setdefault("requests", types.ModuleType("requests"))
temp = types.ModuleType("dotenv")
temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", temp)
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [
    str(Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel")
]
sys.modules.setdefault("claude_panel", dummy)

claude_api = importlib.import_module("claude_api")


class DummyResponse:
    ok = True

    def json(self):
        return {"content": [{"type": "text", "text": "No tags here"}]}


def test_diff_edit_fallback(monkeypatch, caplog):
    monkeypatch.setattr("requests.post", lambda *a, **k: DummyResponse(), raising=False)
    stub = {"edited_content": "fallback"}
    monkeypatch.setattr(
        claude_api.module, "generate_with_claude_diff_edit", lambda **k: stub
    )
    monkeypatch.setattr(
        claude_api.module, "get_claude_api", lambda: types.SimpleNamespace(api_key="x")
    )

    caplog.set_level(logging.WARNING)
    result = claude_api.edit_markdown_with_claude("hi", "fix")

    assert result == "fallback"
    assert any("falling back to diff-edit mode" in r.message for r in caplog.records)
