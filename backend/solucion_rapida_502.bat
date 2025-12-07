@echo off
REM Solución rápida para el error 502
REM Verifica y corrige los problemas más comunes

echo ========================================
echo SOLUCION RAPIDA ERROR 502
echo ========================================
echo.

REM ========================================
REM 1. Verificar y abrir firewall
REM ========================================
echo [1/3] Verificando firewall...
powershell -Command "Get-NetFirewallRule -DisplayName 'Puente Genérico NUC' -ErrorAction SilentlyContinue" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   [INFO] Regla de firewall no existe.
    echo   [INFO] Ejecutando script de PowerShell para crear regla...
    echo   [INFO] Se te pedira confirmacion de UAC (Control de Cuentas de Usuario)
    echo.
    powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0abrir_firewall_ps1.ps1\"' -Verb RunAs" > nul 2>&1
    timeout /t 3 /nobreak > nul
    echo   [INFO] Revisa la ventana de PowerShell que se abrio
    echo   [INFO] Si la regla se creo correctamente, presiona cualquier tecla para continuar...
    pause > nul
    echo.
    REM Verificar nuevamente
    powershell -Command "Get-NetFirewallRule -DisplayName 'Puente Genérico NUC' -ErrorAction SilentlyContinue" > nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Regla de firewall creada
    ) else (
        echo   [ADVERTENCIA] No se pudo verificar la regla de firewall
        echo   [INFO] Ejecuta manualmente: abrir_firewall_como_admin.bat
    )
) else (
    echo   [OK] Regla de firewall ya existe
    powershell -Command "Enable-NetFirewallRule -DisplayName 'Puente Genérico NUC'" > nul 2>&1
)
echo.

REM ========================================
REM 2. Verificar puente
REM ========================================
echo [2/3] Verificando puente...
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Puente esta corriendo
) else (
    echo   [ADVERTENCIA] Puente NO esta corriendo
    echo   [INFO] Iniciando puente...
    cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend"
    start /B pythonw puente_generico_nuc.py > nul 2>&1
    timeout /t 5 /nobreak > nul
    netstat -ano | findstr :5000 > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Puente iniciado correctamente
    ) else (
        echo   [ERROR] No se pudo iniciar el puente
        echo   [INFO] Ejecuta manualmente: ejecutar_puente_silencioso.bat
    )
)
echo.

REM ========================================
REM 3. Verificar conectividad desde Tailscale
REM ========================================
echo [3/3] Verificando conectividad...
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
if defined TAILSCALE_IP (
    echo   IP de Tailscale: %TAILSCALE_IP%
    echo   Probando: http://%TAILSCALE_IP%:5000/api/status
    curl -s -o nul -w "%%{http_code}" http://%TAILSCALE_IP%:5000/api/status 2>nul | findstr /R "^200" > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] NUC responde desde IP de Tailscale
        echo.
        echo ========================================
        echo TODO CORRECTO
        echo ========================================
        echo.
        echo El NUC esta configurado correctamente.
        echo Railway deberia poder conectarse ahora.
        echo.
        echo Si aun ves error 502, verifica en Railway:
        echo   - Variable NUC_URLS: nuc_sede1:http://%TAILSCALE_IP%:5000
        echo   - Logs de Railway para ver errores de conexion
    ) else (
        echo   [ADVERTENCIA] NUC no responde desde IP de Tailscale
        echo   [INFO] Esto puede ser normal si Tailscale no permite conexiones externas
        echo   [INFO] Verifica los logs de Railway para ver el error exacto
    )
) else (
    echo   [ADVERTENCIA] No se pudo obtener IP de Tailscale
    echo   [INFO] Verifica que Tailscale este corriendo: tailscale status
)
echo.

pause
