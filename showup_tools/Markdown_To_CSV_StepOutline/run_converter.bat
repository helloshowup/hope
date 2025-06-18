@echo on
setlocal

title Markdown to CSV Converter (Debug Mode)

REM Determine the script directory
set "SCRIPT_DIR=%~dp0"
echo Running from: %SCRIPT_DIR%

REM Ensure Python environment is activated if it exists
if exist "%SCRIPT_DIR%..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%SCRIPT_DIR%..\venv\Scripts\activate.bat"
    echo Virtual environment activated
) else (
    echo Using system Python
)

REM Show Python information
python --version

REM Change to script directory and run the simplified Python script
cd "%SCRIPT_DIR%"
echo Running simplified entry point...
python run.py

REM Pause on any result to see output
echo Application exited with code: %ERRORLEVEL%
pause

endlocal
