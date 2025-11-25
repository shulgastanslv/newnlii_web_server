@echo off
echo ========================================
echo Starting Devsy Web Server (Production)
echo ========================================

REM Проверка виртуального окружения
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    echo Installing dependencies...
    .\venv\Scripts\activate
    pip install -r requirements.txt
) else (
    .\venv\Scripts\activate
)

REM Запуск основного сервера на всех интерфейсах (0.0.0.0) для внешнего доступа
echo Starting Main API Server on 0.0.0.0:8000...
echo Server will be accessible from external networks
echo.
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

