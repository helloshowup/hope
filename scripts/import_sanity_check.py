#!/usr/bin/env python
"""Verify key package imports from the project root."""

from __future__ import annotations

import importlib
import sys
from typing import List, Optional

MODULES = [
    "showup_core",
    "showup_tools.simplified_app.rag_system.textbook_vector_db",
    "showup_editor_ui",
]


def main(argv: Optional[List[str]] = None) -> int:
    """Attempt to import core modules to validate PYTHONPATH."""
    for module in MODULES:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError as exc:
            sys.exit(f"Failed to import '{module}': {exc}")

    print("\N{White Heavy Check Mark} All modules imported successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
