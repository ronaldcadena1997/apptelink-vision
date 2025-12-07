@echo off
echo ========================================
echo Eliminar Inicio Automatico del Puente
echo ========================================
echo.

set SCRIPT_NAME=PuenteGenericoNUC

echo Eliminando tarea programada...
schtasks /Delete /TN "%SCRIPT_NAME%" /F > nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] Tarea programada eliminada
) else (
    echo [INFO] No se encontro tarea programada
)

echo.
echo Eliminando de carpeta de inicio...
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
del "%STARTUP_FOLDER%\ejecutar_puente_inicio.bat" > nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] Script eliminado de carpeta de inicio
) else (
    echo [INFO] No se encontro en carpeta de inicio
)

echo.
echo ========================================
echo Proceso completado
echo ========================================
echo.
pause
