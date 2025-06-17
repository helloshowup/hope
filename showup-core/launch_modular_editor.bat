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
set "PARENTDIR=%~dp0"
REM Remove trailing backslash if present
if "%PARENTDIR:~-1%"=="\" set "PARENTDIR=%PARENTDIR:~0,-1%"
REM Remove the last path segment to get the parent
for %%I in ("%PARENTDIR%") do set "PARENTDIR=%%~dpI"
REM Remove trailing backslash again if present
if "%PARENTDIR:~-1%"=="\" set "PARENTDIR=%PARENTDIR:~0,-1%"

REM Set PYTHONPATH so showup_editor_ui is importable
set "PYTHONPATH=%PARENTDIR%"

REM Set Python executable path
FOR /F "tokens=*" %%i IN ('python -c "import sys; print(sys.executable)" 2^>nul') DO SET PYTHONEXE=%%i
if "%PYTHONEXE%"=="" (
    set "PYTHONEXE=python"
)

REM Diagnostics: log working directory, PYTHONPATH, and Python executable
(echo Current directory: %CD% & echo PYTHONPATH: %PYTHONPATH% & echo Python path: %PYTHONEXE%) > "launch.log"
if exist "%PYTHONEXE%" (
    echo Found Python at: %PYTHONEXE% >> "launch.log"
) else (
    echo Python not found in PATH, using system default >> "launch.log"
)

REM Start the modular editor UI (updated package path)
python -m showup_editor_ui.claude_panel.main >> "launch.log" 2>&1

REM Check if the process launched successfully
if %ERRORLEVEL% EQU 0 (
    echo Launch successful
) else (
    echo Launch failed. Check launch.log for details.
)

pause