# ruff: noqa: E402
import importlib
import sys
import types
from pathlib import Path

import pytest

# Provide dummy modules required by project imports
sys.modules.setdefault("requests", types.ModuleType("requests"))
dotenv_mod = types.ModuleType("dotenv")
dotenv_mod.load_dotenv = lambda *a, **k: None
sys.modules.setdefault("dotenv", dotenv_mod)
sys.modules.setdefault("markdown", types.ModuleType("markdown"))

claude_dir = Path(__file__).resolve().parents[1] / "showup-editor-ui" / "claude_panel"
dummy = types.ModuleType("claude_panel")
dummy.__path__ = [str(claude_dir)]
sys.modules.setdefault("claude_panel", dummy)

mp_module = importlib.import_module("claude_panel.main_panel")
ClaudeAIPanel = mp_module.ClaudeAIPanel


class FakeTree:
    def __init__(self, path):
        self._path = str(path)

    def selection(self):
        return ["item"]

    def item(self, _id, _key=None):
        return (self._path, "file")


class FakeEditor:
    def __init__(self, path):
        self.current_file_path = str(path)


def test_on_file_select_markdown(tmp_path):
    md = tmp_path / "sample.md"
    md.write_text("hi")
    tree = FakeTree(md)
    called = {}
    enrich = types.SimpleNamespace(load_current_lesson=lambda p: called.setdefault("path", p))
    panel = types.SimpleNamespace(file_tree=tree, enrich_lesson=enrich)
    ClaudeAIPanel._on_file_select(panel, object())
    assert called["path"] == str(md)


def test_on_file_select_non_markdown(tmp_path):
    other = tmp_path / "sample.pdf"
    other.write_text("pdf")
    tree = FakeTree(other)
    called = {}
    enrich = types.SimpleNamespace(load_current_lesson=lambda p: called.setdefault("path", p))
    panel = types.SimpleNamespace(file_tree=tree, enrich_lesson=enrich)
    ClaudeAIPanel._on_file_select(panel, object())
    assert called["path"] == str(other)


def test_on_file_select_missing_values():
    tree = types.SimpleNamespace(selection=lambda: [], item=lambda *_: None)
    called = {}
    enrich = types.SimpleNamespace(load_current_lesson=lambda p: called.setdefault("path", p))
    panel = types.SimpleNamespace(file_tree=tree, enrich_lesson=enrich)
    ClaudeAIPanel._on_file_select(panel, object())
    assert called == {}


def test_on_file_select_unreadable(tmp_path):
    md = tmp_path / "bad.md"
    md.write_text("content")
    tree = FakeTree(md)

    def raise_io(path):
        raise IOError("fail")

    enrich = types.SimpleNamespace(load_current_lesson=raise_io)
    panel = types.SimpleNamespace(file_tree=tree, enrich_lesson=enrich)
    ClaudeAIPanel._on_file_select(panel, object())


def test_gui_smoke_select_load_enrich(tmp_path):
    md = tmp_path / "lesson.md"
    md.write_text("content")
    tree = FakeTree(md)
    editor = FakeEditor(md)

    class FakeEnrich:
        def __init__(self):
            self.current_file_path = None
            self.loaded = None
            self.enriched = False
            self.markdown_editor = editor

        def load_current_lesson(self, path):
            self.current_file_path = path
            self.loaded = path

        def _ui_request_load_lesson(self):
            path = self.current_file_path or self.markdown_editor.current_file_path
            if path:
                self.load_current_lesson(path)

        def enrich_content(self):
            self.enriched = True

        def _ui_request_enrich_content(self):
            self.enrich_content()

    enrich = FakeEnrich()
    panel = types.SimpleNamespace(file_tree=tree, enrich_lesson=enrich)

    ClaudeAIPanel._on_file_select(panel, object())
    assert enrich.loaded == str(md)

    enrich._ui_request_load_lesson()
    assert enrich.current_file_path == str(md)

    enrich._ui_request_enrich_content()
    assert enrich.enriched
