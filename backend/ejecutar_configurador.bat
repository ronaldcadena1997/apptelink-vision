@echo off
chcp 65001 >nul
title Configurador SIM7600
cd /d "%~dp0"
echo ========================================
echo   Configurador Automático SIM7600
echo ========================================
echo.
python detectar_y_configurar_sim7600.py
pause
