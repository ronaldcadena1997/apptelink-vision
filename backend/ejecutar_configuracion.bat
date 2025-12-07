@echo off
chcp 65001 >nul
title Configurar SIM7600
cd /d "%~dp0"
echo ========================================
echo   Ejecutar Configuración SIM7600
echo ========================================
echo.
python configurar_sim7600.py
pause
