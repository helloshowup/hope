# Core Logic Migration Summary

**Date:** 2025-05-22

## Overview
This document summarizes the atomic migration of the core application logic into a dedicated repository folder, as per project reorganization rules.

## Actions Performed

6. **Renamed `core/` to `showup_core/`**
   - Ensured absolute imports (from showup_core import ...) and relative imports (from .file_utils import ...) both work.
   - Updated Python packaging to match standard conventions.

1. **Created `showup-core/` Repository Folder**
   - Established a new folder to house all core logic modules.

2. **Moved `core/` Directory**
   - Ensured the entire `core/` directory is now located at `showup-core/core/`.
   - Verified that only one authoritative copy exists (no duplication).
   - Removed `batch_processor - Copy.py` to enforce single-source rule.

3. **Generated Minimal `requirements.txt`**
   - Included only core-level dependencies required by the modules:
     - `requests`
     - `python-dotenv`

4. **Added Python-standard `.gitignore`**
   - Included a comprehensive `.gitignore` to exclude Python build, cache, and environment files.

5. **Initialized Git and Committed**
   - Initialized a new git repository in `showup-core/`.
   - Made the initial commit with the message: `Initial commit: migrated core modules.`

## Compliance
- All operations were performed atomically (no partial moves, no duplication).
- All steps followed the project’s reorganization and validation rules.
- The migration preserves the integrity and workflow of the core logic.

---

For further details or validation steps, see commit history or request additional reports.
