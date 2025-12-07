@echo off
chcp 65001 >nul
title Detector SIM7600
cd /d "%~dp0"
echo ========================================
echo   Detector y Configurador SIM7600
echo ========================================
echo.
python listar_puertos.py
pause
