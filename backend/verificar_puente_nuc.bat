@echo off
REM Script para verificar si el puente genérico está corriendo en el NUC

echo ========================================
echo VERIFICAR PUENTE GENERICO EN NUC
echo ========================================
echo.

echo [1/4] Verificando si el puente esta corriendo...
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Puente esta corriendo en puerto 5000
    echo.
    echo   Procesos en puerto 5000:
    netstat -ano | findstr :5000
) else (
    echo   [ERROR] Puente NO esta corriendo
    echo   [INFO] Iniciando puente...
    cd /d "%~dp0"
    start /B pythonw puente_generico_nuc.py > nul 2>&1
    timeout /t 5 /nobreak > nul
    netstat -ano | findstr :5000 > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Puente iniciado
    ) else (
        echo   [ERROR] No se pudo iniciar el puente
        echo   [INFO] Ejecuta manualmente: ejecutar_puente_silencioso.bat
    )
)
echo.

echo [2/4] Verificando respuesta local...
curl -s http://localhost:5000/api/status > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Puente responde localmente
    echo.
    echo   Respuesta:
    curl -s http://localhost:5000/api/status
) else (
    echo   [ERROR] Puente NO responde localmente
)
echo.
echo.

echo [3/4] Verificando Tailscale...
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Tailscale esta corriendo
    for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
    if defined TAILSCALE_IP (
        echo   [OK] IP de Tailscale: %TAILSCALE_IP%
    ) else (
        echo   [ERROR] Tailscale no tiene IP asignada
    )
) else (
    echo   [ERROR] Tailscale NO esta corriendo
)
echo.

echo [4/4] Verificando conectividad desde IP de Tailscale...
if defined TAILSCALE_IP (
    echo   Probando: http://%TAILSCALE_IP%:5000/api/status
    curl -s -o nul -w "%%{http_code}" http://%TAILSCALE_IP%:5000/api/status 2>nul | findstr /R "^200" > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] NUC responde desde IP de Tailscale
    ) else (
        echo   [ERROR] NUC NO responde desde IP de Tailscale
        echo   [INFO] Esto puede ser por:
        echo     - Firewall bloqueando conexiones
        echo     - Puente no escucha en todas las interfaces
    )
) else (
    echo   [ADVERTENCIA] No se pudo obtener IP de Tailscale
)
echo.

echo ========================================
echo RESUMEN
echo ========================================
echo.
if defined TAILSCALE_IP (
    echo IP de Tailscale del NUC: %TAILSCALE_IP%
    echo.
    echo Railway deberia poder conectarse a:
    echo   http://%TAILSCALE_IP%:5000
    echo.
)

echo Si el puente NO esta corriendo:
echo   1. Ejecuta: ejecutar_puente_silencioso.bat
echo   2. O ejecuta manualmente: python puente_generico_nuc.py
echo.
echo Si el puente esta corriendo pero Railway no puede conectarse:
echo   1. Verifica el firewall: abrir_firewall_ps1.ps1
echo   2. Verifica que Railway este online en Tailscale
echo.

pause
