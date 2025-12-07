@echo off
REM ========================================
REM EJECUTAR API DEL NUC (Puente Genérico)
REM ========================================
REM Script simple que solo ejecuta el puente genérico
REM ========================================

cd /d "%~dp0backend"

echo ========================================
echo EJECUTANDO API DEL NUC
echo ========================================
echo.

REM Verificar que Python esté instalado
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo [INFO] Instala Python 3.11 o superior
    pause
    exit /b 1
)

REM Verificar que el archivo exista
if not exist "puente_generico_nuc.py" (
    echo [ERROR] No se encontro puente_generico_nuc.py
    echo [INFO] Verifica que el archivo exista en el directorio backend
    pause
    exit /b 1
)

echo [INFO] Iniciando puente generico del NUC...
echo [INFO] El API estara disponible en: http://localhost:5000
echo [INFO] Presiona CTRL+C para detener
echo.
echo ========================================
echo.

REM Ejecutar el puente genérico
python puente_generico_nuc.py
