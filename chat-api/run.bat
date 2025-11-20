@echo off
echo Starting Chat API Server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010

