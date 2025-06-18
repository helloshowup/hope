@echo off
echo Starting 5 Whys Analyzer GUI...

:: Change to the project root directory
cd /d "%~dp0.."

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Run the application
python -m showup_tools.five_whys_analyzer.main

:: If you want the window to stay open after execution (for debugging)
:: pause
