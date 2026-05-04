@echo off
setlocal enabledelayedexpansion

title FB PRO AUTOMATOR | Cyber Edition
color 0b

echo =======================================================
echo          FB PRO AUTOMATOR - CYBER EDITION
echo =======================================================
echo.

:: Hardcoded Python Path
set "PYTHON_EXE=C:\Python314\python.exe"

echo [INFO] Environment: Python 3.14
echo [INFO] Project Path: %~dp0
echo.

if not exist "!PYTHON_EXE!" (
    echo [ERROR] Python not found at !PYTHON_EXE!
    echo.
    echo Searching for Python in other common locations...
    for /f "delims=" %%i in ('where python 2^>nul') do set "PYTHON_EXE=%%i"
)

echo [INFO] Using Python: !PYTHON_EXE!
echo.

echo [INFO] Launching Cyber Engine...
echo [INFO] Server starting at http://localhost:8000
echo.

:: Run the server
"!PYTHON_EXE!" server.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The server has stopped unexpectedly.
    echo.
    pause
)

pause
