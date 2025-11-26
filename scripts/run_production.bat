@echo off
echo ========================================
echo Starting Devsy Web Server (Production)
echo ========================================

REM
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    echo Installing dependencies...
    .\venv\Scripts\activate
    pip install -r requirements.txt
) else (
    .\venv\Scripts\activate
)

REM
echo Starting Main API Server on 127.0.0.1:8000...
echo Server will be accessible from external networks
echo.
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
