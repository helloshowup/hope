@echo off
REM Run the legacy podcast generator

REM Determine the project root relative to this script
set "PROJECT_ROOT=%~dp0.."

REM Prefer the virtual environment Python if available
if exist "%PROJECT_ROOT%\showup-core\venv\Scripts\python.exe" (
    set "PYTHON=%PROJECT_ROOT%\showup-core\venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

REM Construct PYTHONPATH
set "PYTHONPATH=%PROJECT_ROOT%;%PROJECT_ROOT%\showup-core;%PROJECT_ROOT%\showup_tools"

REM Launch the podcast generator (fitness voiceover tool as placeholder)
"%PYTHON%" "%PROJECT_ROOT%\showup_tools\fitness_podcaster\fitness_instructor_voiceover.py" %*

if errorlevel 1 (
    echo Podcast generator exited with errors.
    pause
)
