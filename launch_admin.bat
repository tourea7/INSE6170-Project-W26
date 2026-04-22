@echo off
if not "%1"=="am_admin" (
    powershell -Command "Start-Process -FilePath '%0' -ArgumentList 'am_admin' -Verb RunAs"
    exit
)
cd /d "%~dp0"
python main.py
pause