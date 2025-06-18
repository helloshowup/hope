@echo off
setlocal

title Installing Dependencies for Markdown to CSV Converter

REM Determine the script directory
set "SCRIPT_DIR=%~dp0"
echo Installing dependencies from %SCRIPT_DIR%requirements.txt

REM Ensure Python environment is activated
if exist "%SCRIPT_DIR%..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%SCRIPT_DIR%..\venv\Scripts\activate.bat"
) else (
    echo No virtual environment found. Using system Python.
)

REM Install the required packages
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r "%SCRIPT_DIR%requirements.txt"

if %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies. Please check error messages above.
    pause
    exit /b 1
) else (
    echo Dependencies installed successfully!
    echo You can now run the application using launch_md_to_csv_converter.bat
    pause
    exit /b 0
)
