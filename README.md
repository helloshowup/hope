# hope
The cleaned version of Showup4

## Installation

Install the core and tools packages in editable mode:

```bash
pip install -e ./showup-core
pip install -e ./showup-tools
```

RAG features rely on both packages being installed locally. When launching the UI,
ensure that your `PYTHONPATH` includes the project root along with `showup-core`
and `showup-tools`. The vector database backing RAG queries only works on the
local machine.
Before launching the GUI, build the vector index for your handbook:
```bash
python scripts/index_handbook.py --file path/to/handbook.pdf
```
Run the import sanity check to verify that these packages resolve correctly:
```bash
python scripts/import_sanity_check.py
```

A compatibility module named `showup_editor_ui` exposes the existing `claude_panel` package for older imports. Ensure the project root is on `PYTHONPATH` when launching the UI so this shim resolves correctly.

## Optional Testing

You can run the included unit tests locally with [pytest](https://docs.pytest.org/en/stable/):

```bash
pytest
```

When Claude omits line-edit tags, the tool automatically falls back to diff-edit mode.
