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
