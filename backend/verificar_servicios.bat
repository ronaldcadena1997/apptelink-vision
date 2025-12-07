@echo off
REM Script para verificar el estado de Tailscale y el puente genérico

echo ========================================
echo Verificacion de Servicios
echo ========================================
echo.

REM Verificar Tailscale
echo [1/2] Verificando Tailscale...
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Tailscale esta corriendo
    for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
    if defined TAILSCALE_IP (
        echo [OK] IP de Tailscale: %TAILSCALE_IP%
    ) else (
        echo [ADVERTENCIA] Tailscale no tiene IP asignada
    )
) else (
    echo [ERROR] Tailscale NO esta corriendo
    echo.
    echo Intentando iniciar Tailscale...
    if exist "C:\Program Files\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files\Tailscale\tailscaled.exe"
        echo [INFO] Comando de inicio enviado
    ) else if exist "C:\Program Files (x86)\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files (x86)\Tailscale\tailscaled.exe"
        echo [INFO] Comando de inicio enviado
    ) else (
        echo [ERROR] No se encontro Tailscale instalado
    )
)
echo.

REM Verificar puente genérico
echo [2/2] Verificando puente generico...
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Puente generico esta corriendo (puerto 5000)
    echo.
    echo Probando conexion...
    curl http://localhost:5000/api/status > nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [OK] El puente responde correctamente
    ) else (
        echo [ADVERTENCIA] El puente no responde
    )
) else (
    echo [ERROR] Puente generico NO esta corriendo
    echo.
    echo Para iniciarlo manualmente:
    echo   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
    echo   python puente_generico_nuc.py
)
echo.

echo ========================================
echo Verificacion completada
echo ========================================
echo.
pause
