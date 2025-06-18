import importlib
import sys

claude_panel = importlib.import_module("claude_panel")
sys.modules[__name__ + ".claude_panel"] = claude_panel
