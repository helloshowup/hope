import os
import time
from typing import List

_cache_enabled = True
_cache_instance = None

class SimpleCache:
    def __init__(self, cache_dir: str = "cache") -> None:
        self.cache_dir = os.path.abspath(cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)

    def _iter_files(self):
        for root, _, files in os.walk(self.cache_dir):
            for name in files:
                yield os.path.join(root, name)

    def get_cache_items(self) -> List[str]:
        return [os.path.relpath(f, self.cache_dir) for f in self._iter_files()]

    def get_cache_size(self) -> float:
        total = sum(os.path.getsize(f) for f in self._iter_files())
        return total / (1024 * 1024)

    def clear_cache(self, max_age_days: int = 0) -> int:
        count = 0
        now = time.time()
        for path in list(self._iter_files()):
            age_days = (now - os.path.getmtime(path)) / 86400
            if max_age_days == 0 or age_days >= max_age_days:
                os.remove(path)
                count += 1
        return count

    def delete_cache_item(self, relative_path: str) -> bool:
        path = os.path.join(self.cache_dir, relative_path)
        if os.path.isfile(path):
            os.remove(path)
            return True
        return False


def get_cache_instance() -> SimpleCache:
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = SimpleCache()
    return _cache_instance


def set_local_cache_enabled(enabled: bool) -> None:
    global _cache_enabled
    _cache_enabled = enabled
