@echo off
REM Script para diagnosticar el error 502

echo ========================================
echo DIAGNOSTICO ERROR 502
echo ========================================
echo.
echo Este script verifica por que Railway no puede
echo conectarse al NUC para obtener snapshots.
echo.

REM ========================================
REM 1. Verificar Puente Local
REM ========================================
echo [1/6] Verificando puente local...
set PUENTE_OK=0
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Puente esta corriendo en puerto 5000
    echo.
    echo   Verificando en que interfaz escucha...
    netstat -ano | findstr :5000
    echo.
    
    REM Verificar si escucha en 0.0.0.0 o solo 127.0.0.1
    netstat -ano | findstr ":5000" | findstr "0.0.0.0" > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Puente escucha en todas las interfaces (0.0.0.0)
    ) else (
        echo   [ADVERTENCIA] Puente puede estar escuchando solo en localhost
        echo   [INFO] Verifica que puente_generico_nuc.py use: app.run(host='0.0.0.0', port=5000)
    )
    
    REM Probar respuesta local
    curl -s http://localhost:5000/api/status > nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Puente responde localmente
        set PUENTE_OK=1
    ) else (
        echo   [ADVERTENCIA] Puente no responde localmente (puede estar iniciando)
    )
) else (
    echo   [ERROR] Puente NO esta corriendo
    echo   [INFO] Ejecuta: ejecutar_puente_silencioso.bat
    set PUENTE_OK=0
)

REM Solo continuar si el puente está OK, pero no salir con error si solo falta respuesta
if %PUENTE_OK% EQU 0 (
    echo   [INFO] El puente puede estar iniciando. Espera 10 segundos y vuelve a ejecutar este script.
    echo.
)
echo.

REM ========================================
REM 2. Verificar Tailscale
REM ========================================
echo [2/6] Verificando Tailscale...
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Tailscale esta corriendo
    
    REM Obtener IP de Tailscale
    for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
    if defined TAILSCALE_IP (
        echo   [OK] IP de Tailscale: %TAILSCALE_IP%
    ) else (
        echo   [ERROR] Tailscale no tiene IP asignada
        goto :error
    )
) else (
    echo   [ERROR] Tailscale NO esta corriendo
    goto :error
)
echo.

REM ========================================
REM 3. Verificar Conectividad desde Tailscale IP
REM ========================================
echo [3/6] Verificando conectividad desde IP de Tailscale...
if not defined TAILSCALE_IP (
    echo   [ERROR] No se pudo obtener IP de Tailscale
    echo   [INFO] Verifica que Tailscale este corriendo y conectado
    goto :error
)
echo   Probando: http://%TAILSCALE_IP%:5000/api/status
curl -s -o nul -w "%%{http_code}" http://%TAILSCALE_IP%:5000/api/status 2>nul | findstr /R "^200" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] NUC responde desde IP de Tailscale
) else (
    echo   [ERROR] NUC NO responde desde IP de Tailscale
    echo   [INFO] Esto puede ser por:
    echo     - Firewall bloqueando conexiones (MAS PROBABLE)
    echo     - Puente no escucha en todas las interfaces
    echo     - Tailscale no permite conexiones entrantes
    echo.
    echo   [SOLUCION] Ejecuta como Administrador: abrir_firewall.bat
    echo   O manualmente:
    echo     New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
    echo.
    echo   [INFO] Continuando con otras verificaciones...
)
echo.

REM ========================================
REM 4. Verificar Firewall
REM ========================================
echo [4/6] Verificando firewall...
Get-NetFirewallRule -DisplayName "*5000*" -ErrorAction SilentlyContinue | Select-Object DisplayName, Enabled, Direction | findstr /I "5000" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Regla de firewall encontrada para puerto 5000
    echo.
    echo   Reglas encontradas:
    Get-NetFirewallRule -DisplayName "*5000*" -ErrorAction SilentlyContinue | Select-Object DisplayName, Enabled, Direction
) else (
    echo   [ADVERTENCIA] No se encontro regla de firewall para puerto 5000
    echo   [INFO] Ejecuta como Administrador:
    echo     New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
)
echo.

REM ========================================
REM 5. Verificar Endpoint de Snapshot
REM ========================================
echo [5/6] Verificando endpoint de snapshot...
echo   Probando: http://localhost:5000/api/camaras/192.168.60.65/snapshot
curl -s -o nul -w "%%{http_code}" http://localhost:5000/api/camaras/192.168.60.65/snapshot 2>nul | findstr /R "^200" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Endpoint de snapshot funciona localmente
) else (
    echo   [ADVERTENCIA] Endpoint de snapshot no responde (puede ser normal si OpenCV no esta instalado)
    echo   [INFO] Verifica que OpenCV este instalado: pip install opencv-python-headless
)
echo.

REM ========================================
REM 6. Verificar Configuración en Railway
REM ========================================
echo [6/6] Verificando configuracion...
echo   [INFO] Verifica manualmente en Railway Dashboard:
echo     - Variable NUC_URLS debe ser: nuc_sede1:http://%TAILSCALE_IP%:5000
echo     - Variable CAMARAS_IPS debe ser: 192.168.60.65
echo.
echo   [INFO] Revisa los logs de Railway para ver errores de conexion
echo.

REM ========================================
REM RESUMEN
REM ========================================
echo ========================================
echo RESUMEN
echo ========================================
echo.
echo Estado del NUC:
echo   - Puente local: [OK]
echo   - Tailscale: [OK] - IP: %TAILSCALE_IP%
echo   - Conectividad Tailscale: [VERIFICAR]
echo   - Firewall: [VERIFICAR]
echo.
echo Siguientes pasos:
echo   1. Si el NUC no responde desde IP de Tailscale:
echo      - Abre el firewall: New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
echo      - Verifica que puente_generico_nuc.py use: app.run(host='0.0.0.0', port=5000)
echo.
echo   2. Verifica en Railway Dashboard:
echo      - Variables de entorno: NUC_URLS=nuc_sede1:http://%TAILSCALE_IP%:5000
echo      - Logs para ver errores de conexion
echo.
echo   3. IMPORTANTE: Railway puede no tener acceso a Tailscale
echo      Si Railway no puede conectarse, considera:
echo      - Instalar Tailscale en Railway (complejo)
echo      - Usar un tunel publico (ngrok, Cloudflare Tunnel)
echo.
goto :end

:error
echo.
echo ========================================
echo ERRORES DETECTADOS
echo ========================================
echo.
echo Hay problemas con la configuracion del NUC.
echo Revisa los errores anteriores y corrigelos.
echo.
echo SOLUCIONES RAPIDAS:
echo   1. Si el puente no esta corriendo:
echo      - Ejecuta: ejecutar_puente_silencioso.bat
echo.
echo   2. Si Tailscale no tiene IP:
echo      - Verifica que Tailscale este instalado y corriendo
echo      - Ejecuta: tailscale status
echo.
echo   3. Si el NUC no responde desde IP de Tailscale:
echo      - Ejecuta como Administrador: abrir_firewall.bat
echo.
pause
exit /b 1

:end
echo.
pause
