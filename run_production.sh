#!/bin/bash
echo "========================================"
echo "Starting Devsy Web Server (Production)"
echo "========================================"

# Проверка виртуального окружения
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Installing dependencies..."
    .venv/bin/pip install -r requirements.txt
else
    # Убедимся, что зависимости установлены
    .venv/bin/pip install -r requirements.txt --quiet
fi

echo "Starting Main API Server on 0.0.0.0:8000..."
echo "Server will be accessible from external networks"
echo ""
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

