@echo off

REM Absolute path to Python executable
set PYTHON="C:\Users\User\Documents\showup-v4\showup-core\venv\Scripts\python.exe"

REM Set the PYTHONPATH to include both parent directory and showup-core
set PYTHONPATH="C:\Users\User\Documents\showup-v4";"C:\Users\User\Documents\showup-v4\showup-core";"C:\Users\User\Documents\showup-v4\showup-tools"

REM Change to the script's directory
cd /d "%~dp0"

echo Starting editor... > launch.log
echo Using Python: %PYTHON% >> launch.log
echo PYTHONPATH: %PYTHONPATH% >> launch.log

REM Launch the module
%PYTHON% -m claude_panel.main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ^> Launch failed. Check the error message above.
) else (
    echo.
    echo ^> Launch successful!
)

echo.
echo Press any key to close this window...
pause >nul

