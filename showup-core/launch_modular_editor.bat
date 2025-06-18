@echo off
setlocal
REM Ensure working directory is the script's folder
cd /d "%~dp0"

REM Activate the Python virtual environment from showup-core
if exist "..\showup-core\venv\Scripts\activate" (
    call "..\showup-core\venv\Scripts\activate"
) else (
    echo ERROR: venv not found at ..\showup-core\venv\Scripts\activate
    pause
    exit /b 1
)

REM Get the parent directory of this script's directory
set "PROJECT_ROOT=%~dp0"
REM Remove trailing backslash if present
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
REM Remove the last path segment to get the parent
for %%I in ("%PROJECT_ROOT%") do set "PROJECT_ROOT=%%~dpI"
REM Remove trailing backslash again if present
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

REM Set PYTHONPATH so showup_editor_ui is importable
set "PYTHONPATH=%PROJECT_ROOT%"

REM Set Python executable path
FOR /F "tokens=*" %%i IN ('python -c "import sys; print(sys.executable)" 2^>nul') DO SET PYTHON=%%i
if "%PYTHON%"=="" (
    set "PYTHON=python"
)

%PYTHON% %PROJECT_ROOT%\scripts\import_sanity_check.py
if %ERRORLEVEL% NEQ 0 (
    echo Import sanity check failed.
    exit /b %ERRORLEVEL%
)

REM Diagnostics: log working directory, PYTHONPATH, and Python executable
(echo Current directory: %CD% & echo PYTHONPATH: %PYTHONPATH% & echo Python path: %PYTHON%) > "launch.log"
if exist "%PYTHON%" (
    echo Found Python at: %PYTHON% >> "launch.log"
) else (
    echo Python not found in PATH, using system default >> "launch.log"
)

REM Start the modular editor UI (updated package path)
%PYTHON% -m showup_editor_ui.claude_panel.main >> "launch.log" 2>&1

REM Check if the process launched successfully
if %ERRORLEVEL% EQU 0 (
    echo Launch successful
) else (
    echo Launch failed. Check launch.log for details.
)

pause