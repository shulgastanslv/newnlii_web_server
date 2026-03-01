#!/bin/bash

echo "========================================"
echo "Starting Newnlii Web Server (PRODUCTION)"
echo "========================================"

# Проверка виртуального окружения
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Активация
source .venv/bin/activate

# Установка зависимостей (если требуется)
# pip install -r requirements.txt

echo "Starting Main API Server with uvicorn (production)..."
echo ""

# Запуск uvicorn с 4 воркерами.
# Для работы в фоне добавьте & в конец, либо используйте nohup.
# Здесь запускаем в текущем терминале – удобно для отладки.
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4