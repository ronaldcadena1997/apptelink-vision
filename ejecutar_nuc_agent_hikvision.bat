@echo off
REM ========================================
REM EJECUTAR NUC AGENT - ESTILO HIKVISION
REM ========================================
REM Este script ejecuta el agente que se conecta al servidor central
REM ========================================

cd /d "%~dp0backend"

echo ========================================
echo NUC AGENT - ESTILO HIKVISION
echo ========================================
echo.

REM Verificar que Python esté instalado
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

REM Verificar que el archivo exista
if not exist "nuc_agent_hikvision.py" (
    echo [ERROR] No se encontro nuc_agent_hikvision.py
    pause
    exit /b 1
)

echo [INFO] Iniciando NUC Agent...
echo [INFO] El agente se conectara al servidor central
echo [INFO] Presiona CTRL+C para detener
echo.
echo ========================================
echo.

REM Ejecutar el agente
python nuc_agent_hikvision.py

pause
