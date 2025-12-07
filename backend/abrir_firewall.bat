@echo off
REM Script para abrir el puerto 5000 en el firewall de Windows
REM DEBE ejecutarse como Administrador

echo ========================================
echo ABRIR PUERTO 5000 EN FIREWALL
echo ========================================
echo.
echo Este script crea una regla de firewall para permitir
echo conexiones entrantes en el puerto 5000.
echo.

REM Verificar si ya existe la regla
Get-NetFirewallRule -DisplayName "Puente Genérico NUC" -ErrorAction SilentlyContinue > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] La regla de firewall ya existe
    echo [INFO] Verificando si esta habilitada...
    Get-NetFirewallRule -DisplayName "Puente Genérico NUC" | Select-Object DisplayName, Enabled, Direction
    echo.
    echo [INFO] Si esta deshabilitada, se habilitara automaticamente
    Enable-NetFirewallRule -DisplayName "Puente Genérico NUC"
    echo [OK] Regla habilitada
) else (
    echo [INFO] Creando nueva regla de firewall...
    New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Regla de firewall creada exitosamente
    ) else (
        echo [ERROR] No se pudo crear la regla de firewall
        echo [INFO] Asegurate de ejecutar este script como Administrador
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo VERIFICACION
echo ========================================
echo.
echo Reglas de firewall para puerto 5000:
Get-NetFirewallRule -DisplayName "*5000*" -ErrorAction SilentlyContinue | Select-Object DisplayName, Enabled, Direction, Action
echo.

REM Obtener IP de Tailscale para mostrar
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
if defined TAILSCALE_IP (
    echo IP de Tailscale: %TAILSCALE_IP%
    echo.
    echo Ahora prueba desde Railway o desde otra maquina:
    echo   curl http://%TAILSCALE_IP%:5000/api/status
    echo.
)

echo ========================================
echo COMPLETADO
echo ========================================
echo.
pause
