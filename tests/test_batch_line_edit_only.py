# ruff: noqa: E402
import sys
import types
from unittest import mock


# Provide dummy modules required by project imports
_temp = types.ModuleType("dotenv")
_temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", _temp)
sys.modules.setdefault("requests", types.ModuleType("requests"))

import importlib
from pathlib import Path

claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [str(claude_dir)]
sys.modules.setdefault("claude_panel", dummy)

bp_module = importlib.import_module("claude_panel.batch_processor")
const_module = importlib.import_module("claude_panel.constants")

BatchProcessor = bp_module.BatchProcessor
LINE_EDIT_PROMPT_HDR = const_module.LINE_EDIT_PROMPT_HDR


def test_line_edit_path(monkeypatch, tmp_path):
    fake_file = tmp_path / "sample.md"
    fake_file.write_text("# Title\nBody\n")
    called = {"edit": [], "regen": []}

    def fake_edit(**kwargs):
        called["edit"].append(kwargs["instructions"])
        return kwargs["markdown_text"]

    def fake_regen(**kwargs):
        called["regen"].append(kwargs["instructions"])
        return kwargs["markdown_text"]

    monkeypatch.setattr("claude_api.edit_markdown_with_claude", fake_edit)
    monkeypatch.setattr("claude_api.regenerate_markdown_with_claude", fake_regen)
    monkeypatch.setattr("claude_api.generate_with_claude_haiku", lambda *a, **k: "ctx")
    monkeypatch.setattr(bp_module, "edit_markdown_with_claude", fake_edit)
    monkeypatch.setattr(bp_module, "generate_with_claude_haiku", lambda *a, **k: "ctx")
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)

    parent = mock.Mock()
    parent.update_idletasks = lambda: None
    parent.after = lambda *a, **k: None
    bp = BatchProcessor(None, parent)
    bp.progress_var = mock.Mock(set=lambda *a, **k: None)
    bp.status_var = mock.Mock(set=lambda *a, **k: None)
    bp.process_btn = mock.Mock(config=lambda *a, **k: None)
    bp.cancel_btn = mock.Mock(config=lambda *a, **k: None)
    bp.status_label = mock.Mock(config=lambda *a, **k: None)
    bp.processing_batch = True
    bp._process_files([str(fake_file)], f"{LINE_EDIT_PROMPT_HDR}\n\nfix typos", "")

    assert len(called["edit"]) == 1
    assert len(called["regen"]) == 0
    assert "[EDIT:" in called["edit"][0].upper()
