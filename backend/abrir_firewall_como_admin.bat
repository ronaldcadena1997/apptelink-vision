@echo off
REM Script que ejecuta PowerShell como Administrador para abrir el firewall
REM Este script solicita permisos de administrador automáticamente

echo ========================================
echo ABRIR FIREWALL - EJECUTAR COMO ADMIN
echo ========================================
echo.
echo Este script ejecutara PowerShell como Administrador
echo para crear la regla de firewall.
echo.

REM Obtener la ruta del script PowerShell
set SCRIPT_DIR=%~dp0
set PS_SCRIPT=%SCRIPT_DIR%abrir_firewall_ps1.ps1

REM Verificar que existe el script PowerShell
if not exist "%PS_SCRIPT%" (
    echo [ERROR] No se encontro el script PowerShell: %PS_SCRIPT%
    echo [INFO] Asegurate de que abrir_firewall_ps1.ps1 este en la misma carpeta
    pause
    exit /b 1
)

echo [INFO] Ejecutando PowerShell como Administrador...
echo [INFO] Se te pedira confirmacion de UAC (Control de Cuentas de Usuario)
echo.

REM Ejecutar PowerShell como Administrador
powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%PS_SCRIPT%\"' -Verb RunAs"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Script de PowerShell ejecutado
    echo [INFO] Revisa la ventana de PowerShell que se abrio
) else (
    echo.
    echo [ERROR] No se pudo ejecutar PowerShell como Administrador
    echo [INFO] Intenta ejecutar manualmente:
    echo   1. Abre PowerShell como Administrador
    echo   2. Navega a: %SCRIPT_DIR%
    echo   3. Ejecuta: .\abrir_firewall_ps1.ps1
)

echo.
pause
