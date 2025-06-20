import concurrent.futures

from claude_panel.enrich_lesson import _perform_handbook_indexing_subprocess


def test_handbook_indexing_subprocess_returns_progress():
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            _perform_handbook_indexing_subprocess,
            "stub text",
            "stub_id",
        )
        ok, steps = future.result(timeout=60)
    assert ok and isinstance(steps, list)
