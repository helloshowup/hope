#!/usr/bin/env python
"""Index a handbook for local RAG queries."""

from __future__ import annotations

import argparse
from typing import List, Optional

from showup_tools.simplified_app.rag_system.ingest_textbook import (
    index_textbook,
)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Index a PDF or Markdown handbook for the RAG system."
    )
    parser.add_argument(
        "--file",
        "-f",
        required=True,
        help="Path to the handbook file (PDF or Markdown).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild the index even if it already exists.",
    )

    args = parser.parse_args(argv)

    success = index_textbook(args.file, force_rebuild=args.force)
    if success:
        print(
            f"\N{White Heavy Check Mark} Successfully indexed handbook: "
            f"{args.file}"
        )
        return 0

    print(f"\N{Cross Mark} Failed to index handbook: {args.file}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
