import importlib
import types
import sys
from pathlib import Path

sys.modules.setdefault("requests", types.ModuleType("requests"))
temp = types.ModuleType("dotenv")
temp.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", temp)

claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [str(claude_dir)]
sys.modules.setdefault("claude_panel", dummy)

bp_module = importlib.import_module("claude_panel.batch_processor")
BatchProcessor = bp_module.BatchProcessor


def _dummy_parent():
    import types

    parent = types.SimpleNamespace()
    parent.update_idletasks = lambda: None
    parent.after = lambda *a, **k: None
    return parent


def test_header_auto_prepended(tmp_path, monkeypatch):
    fake_file = tmp_path / "foo.md"
    fake_file.write_text("# T\nB")
    captured = {}
    monkeypatch.setattr(
        "claude_api.edit_markdown_with_claude",
        lambda markdown_text, instructions, context: captured.setdefault(
            "ins", instructions
        )
        or markdown_text,
    )
    monkeypatch.setattr(
        bp_module,
        "edit_markdown_with_claude",
        lambda markdown_text, instructions, context: captured.setdefault(
            "ins", instructions
        )
        or markdown_text,
    )
    bp = BatchProcessor(None, _dummy_parent())
    bp.processing_batch = True
    bp.progress_var = types.SimpleNamespace(set=lambda *a, **k: None)
    bp.status_var = types.SimpleNamespace(set=lambda *a, **k: None)
    bp.process_btn = types.SimpleNamespace(config=lambda *a, **k: None)
    bp.cancel_btn = types.SimpleNamespace(config=lambda *a, **k: None)
    bp.status_label = types.SimpleNamespace(config=lambda *a, **k: None)
    bp._process_files([str(fake_file)], "Fix typos only.", "")
    header = importlib.import_module(
        "showup_core.claude_api_consts"
    ).LINE_EDIT_HEADER.strip()
    assert captured["ins"].lstrip().startswith(header)
