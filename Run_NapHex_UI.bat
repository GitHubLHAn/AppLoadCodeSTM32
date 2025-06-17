@echo off
REM Activate the virtual environment named myenv and run NapHex_UI.py

REM Change directory to the folder containing this script (optional, if needed)
cd /d "%~dp0"

REM Activate venv (Windows)
call myenv\Scripts\activate.bat

REM Run the Python GUI
python NapHex_Terminal.py

REM Pause so the window stays open if there is an error
pause