@echo off
echo ========================================
echo Starting Newnlii Web Server...
echo ========================================


@echo check_venv_status
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM
echo Starting Main API Server...
start "Newnlii Main API" cmd /k "fastapi dev .\app\main.py"

REM
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Both servers are starting...
echo Main API: http://localhost:8000
echo ========================================
echo.
echo Press any key to exit (servers will continue running)...
pause > nul
