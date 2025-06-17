@echo on
setlocal EnableDelayedExpansion

title Markdown to CSV Converter

REM Determine the script directory
set "SCRIPT_DIR=%~dp0"
echo Script directory: %SCRIPT_DIR%

REM Check if Python is installed
python --version
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in the PATH.
    echo Please install Python 3.7 or newer and try again.
    pause
    exit /b 1
)

REM Ensure Python environment is activated
if exist "%SCRIPT_DIR%..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%SCRIPT_DIR%..\venv\Scripts\activate.bat"
    echo Virtual environment activated
) else (
    echo Using system Python
)

REM Make sure we're using the correct Python interpreter
echo Python executable path:
python -c "import sys; print(sys.executable)"

REM Print Python path for debugging
echo Python path:
python -c "import sys; print(sys.path)"

REM Skip anthropic check as it might be causing issues
REM echo Checking for anthropic module...
REM python -c "import anthropic; print('Anthropic module found, version:', anthropic.__version__)" 2>nul
REM if %ERRORLEVEL% NEQ 0 (
REM    echo Warning: The 'anthropic' module is not installed.
REM    echo AI features will not be available.
REM )

REM Check if tkinter is available
echo Checking for tkinter...
python -c "import tkinter; print('Tkinter version:', tkinter.TkVersion)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Warning: tkinter is not available. The GUI may not work properly.
)

REM Run the application in GUI mode with direct Python invocation
echo Starting Markdown to CSV Converter...
cd "%SCRIPT_DIR%"
python main.py

REM Pause on error
if %ERRORLEVEL% NEQ 0 (
    echo Error occurred. Press any key to exit...
    pause > nul
)

endlocal
