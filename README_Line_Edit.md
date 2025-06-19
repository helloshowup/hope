# Line Edit Workflow

This document outlines how Claude's line-by-line edit mode works.

## Tag Grammar

Requests to `edit_markdown_with_claude` must instruct Claude to produce bracketed edit tags:

```
[EDIT:INSERT:X]
content to insert
[/EDIT]
```

```
[EDIT:REPLACE:X-Y]
replacement content
[/EDIT]
```

`X` is the 1-indexed line number after which to insert content or the start of the replacement range. `Y` is the inclusive end line for replacements.

The returned content inside each tag should contain only the new markdown. Do not include line numbers or commentary.

## Failure Behaviour

If no valid edit tags are found in the Claude reply, the API raises a `ValueError`. This prevents silent failures when the model produces unexpected output.

The raw reply is saved to `showup-core/logs/claude/raw/` before regex parsing to aid troubleshooting.
