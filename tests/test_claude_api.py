import re
import pytest

import sys
import types
sys.modules.setdefault("requests", types.ModuleType("requests"))
temp=types.ModuleType("dotenv");temp.load_dotenv=lambda *a, **k: None;sys.modules.setdefault("dotenv", temp)


# Helper replicating internal parsing logic from edit_markdown_with_claude

def _parse_edits(api_response: str):
    insert_pattern = r"\[EDIT\s*:\s*INSERT\s*:\s*(\d+)\s*\]([\s\S]*?)\[/\s*EDIT\s*\]"
    replace_pattern = r"\[EDIT\s*:\s*REPLACE\s*:\s*(\d+)\s*-\s*(\d+)\s*\]([\s\S]*?)\[/\s*EDIT\s*\]"
    edits = []
    for match in re.finditer(insert_pattern, api_response, re.IGNORECASE):
        edits.append({
            "type": "insert",
            "line_num": int(match.group(1)),
            "content": match.group(2).strip(),
        })
    for match in re.finditer(replace_pattern, api_response, re.IGNORECASE):
        edits.append({
            "type": "replace",
            "start_line": int(match.group(1)),
            "end_line": int(match.group(2)),
            "content": match.group(3).strip(),
        })
    if not edits:
        raise ValueError("Claude returned no edit tags or they did not parse")
    return edits


def test_parse_with_whitespace():
    reply = "[EDIT : INSERT : 1 ] New line [/EDIT]"
    edits = _parse_edits(reply)
    assert edits == [{"type": "insert", "line_num": 1, "content": "New line"}]


def test_fail_fast_on_full_doc():
    reply = "This is a full document with no edit tags."
    with pytest.raises(ValueError):
        _parse_edits(reply)
