@echo off
echo ========================================
echo Starting Devsy Web Server...
echo ========================================


@echo check_venv_status
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
@echo venv_created

@echo activate_venv
.\venv\Scripts\activate
@echo venv_activated

REM

REM Запуск основного сервера в новом окне
echo Starting Main API Server...
start "Devsy Main API" cmd /k "fastapi dev .\app\main.py"

REM Небольшая задержка перед запуском второго сервера
timeout /t 2 /nobreak >nul

REM Переход в директорию chat-api и запуск Chat API
echo Starting Chat API Server...
cd chat-api
start "Devsy Chat API" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8010"
cd ..

echo.
echo ========================================
echo Both servers are starting...
echo Main API: http://localhost:8000
echo Chat API: http://localhost:8010
echo ========================================
echo.
echo Press any key to exit (servers will continue running)...
pause >nul
