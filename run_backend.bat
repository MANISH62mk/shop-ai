@echo off
title ShopAI Backend (FastAPI)
echo ====================================================
echo Starting SHOPAI FastAPI Backend on http://127.0.0.1:8000
echo ====================================================
cd /d "%~dp0"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
