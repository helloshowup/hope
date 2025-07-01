import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".showup_editor" / "config.json"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def get_setting(key: str, default: str | None = None):
    config = load_config()
    return config.get(key, default)


def set_setting(key: str, value) -> None:
    config = load_config()
    config[key] = value
    save_config(config)
