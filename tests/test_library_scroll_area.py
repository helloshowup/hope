import importlib
import sys
import types
from pathlib import Path

import pytest


@pytest.fixture()
def panel(tmp_path, monkeypatch):
    claude_dir = (
        Path(__file__).resolve().parents[1]
        / "showup-editor-ui"
        / "claude_panel"
    )
    dummy = types.ModuleType("claude_panel")
    dummy.__path__ = [str(claude_dir)]
    monkeypatch.setitem(sys.modules, "claude_panel", dummy)

    mp_module = importlib.import_module("claude_panel.main_panel")
    monkeypatch.setattr(
        mp_module.messagebox,
        "showerror",
        lambda *a, **k: None,
    )
    monkeypatch.setattr(
        mp_module.config_manager,
        "get_library_path",
        lambda: str(tmp_path),
    )

    import tkinter as tk

    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tk display required")
    root.geometry("800x800")
    panel = mp_module.ClaudeAIPanel(root, root)
    root.update_idletasks()
    yield panel
    root.destroy()


def test_batch_buttons_visible_after_resize(panel):
    panel.master.geometry("800x600")
    panel.master.update_idletasks()
    assert panel.send_to_batch_btn.winfo_ismapped()
    assert panel.send_to_full_regen_btn.winfo_ismapped()
