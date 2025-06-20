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
path_utils = importlib.import_module("claude_panel.path_utils")
AIDetector = ai_module.AIDetector


def test_detect_simple_phrase(tmp_path, monkeypatch):
    monkeypatch.setattr(path_utils, "get_project_root", lambda: tmp_path)
    monkeypatch.setattr(ai_module, "project_root", tmp_path)
    detector = AIDetector(None)
    text = "As an AI, I cannot browse the internet. I hope this helps."
    result = detector._detect_ai_patterns(text)
    assert result["detected"]
    assert result["count"] >= 2
