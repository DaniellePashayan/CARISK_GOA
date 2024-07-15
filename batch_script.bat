@echo off
echo Carisk Combine Started

SETLOCAL
set FILE_PATH="C:\Users\pa_dpashayan\Desktop\PyProjects\CARISK_GOA"
cd %FILE_PATH%
set VENV_PATH=%FILE_PATH\%.venv
call "%VENV_PATH%\Scripts\activate.bat"
set SCRIPT_PATH=%FILE_PATH\%main.py

python -u "%SCRIPT_PATH%"
ENDLOCAL

Echo Process Completed