@echo off
title ShopAI Dual Launcher
cd /d "%~dp0"
echo ====================================================
echo Starting SHOPAI Full Stack Application...
echo ====================================================
start "ShopAI Backend (Port 8000)" cmd /k "cd /d "%~dp0" && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
start "ShopAI Frontend (Port 8080)" cmd /k "cd /d "%~dp0frontend" && npm run dev -- --host 0.0.0.0 --port 8080"
echo.
echo Both servers have been launched in separate terminal windows!
echo - Localhost Frontend: http://localhost:8080
echo - Network Frontend:   http://192.168.0.105:8080
echo - Backend URL:        http://127.0.0.1:8000
echo - Swagger Docs:       http://127.0.0.1:8000/docs
echo ====================================================
timeout /t 3 /nobreak >nul
start http://localhost:8080
