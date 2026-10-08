@echo off
title ShopAI Frontend (Port 8080)
echo ====================================================
echo Starting SHOPAI React Frontend on:
echo - Localhost: http://localhost:8080
echo - Network:   http://192.168.0.105:8080
echo ====================================================
cd /d "%~dp0frontend"
npm run dev -- --host 0.0.0.0 --port 8080
pause
