from __future__ import annotations

from pathlib import Path

from showup_editor_ui.claude_panel import user_config


def get_persona_library_root() -> Path:
    """Return the configured persona library root directory.

    Returns:
        Path: Path to persona library directory.

    Raises:
        ValueError: If no persona library path is configured.
    """
    path_str = user_config.get_setting("persona_library_root", None)
    if not path_str:
        raise ValueError("Persona library root not configured")
    return Path(path_str)

