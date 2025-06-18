@echo off
setlocal

echo Admin Assistant Launcher
echo ======================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please install Python 3.6 or higher.
    echo Visit https://www.python.org/downloads/ to download Python.
    pause
    exit /b 1
)

:: Check for .env file and create if not exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul 2>&1
    echo Created .env file. Please edit it to add your Anthropic API key.
    echo.
)

:: Install requirements if needed
echo Checking dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error installing dependencies. Please check your internet connection
    echo and make sure you have the necessary permissions.
    pause
    exit /b 1
)

echo.
echo Starting Admin Assistant GUI...
echo.

:: Run the GUI application
python gui.py

:: If the program exits with an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo The application encountered an error.
    pause
)

endlocal
