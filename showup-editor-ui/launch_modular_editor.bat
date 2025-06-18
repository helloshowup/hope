@echo off

REM Determine project root relative to this script
set "PROJECT_ROOT=%~dp0.."

REM Construct PYTHONPATH using the project root
set "PYTHONPATH=%PROJECT_ROOT%;%PROJECT_ROOT%\showup-core;%PROJECT_ROOT%\showup_tools"

REM Prefer virtual environment Python if available
if exist "%PROJECT_ROOT%\showup-core\venv\Scripts\python.exe" (
    set "PYTHON=%PROJECT_ROOT%\showup-core\venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

%PYTHON% %PROJECT_ROOT%\scripts\import_sanity_check.py
if %ERRORLEVEL% NEQ 0 (
    echo Import sanity check failed.
    exit /b %ERRORLEVEL%
)

REM Change to the script's directory
cd /d "%~dp0"

echo Starting editor... > launch.log
echo Using Python: %PYTHON% >> launch.log
echo PYTHONPATH: %PYTHONPATH% >> launch.log

REM Launch the module and log output
%PYTHON% -m claude_panel.main >> launch.log 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ^> Launch failed. Check launch.log for details.
) else (
    echo.
    echo ^> Launch successful!
)

echo.
echo Press any key to close this window...
pause >nul

