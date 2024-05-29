@echo off
echo Carisk Combine Started

SETLOCAL
set FILE_PATH=%~dp0
set SCRIPT_PATH=%FILE_PATH%main.py
set VENV_PATH=%FILE_PATH%.venv

call "%VENV_PATH%\Scripts\activate.bat"
python -u "%SCRIPT_PATH%"
ENDLOCAL

Echo Process Completed
pause