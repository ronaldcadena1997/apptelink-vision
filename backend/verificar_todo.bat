@echo off
REM Script para verificar todo el flujo: NUC -> Railway -> Frontend

echo ========================================
echo VERIFICACION COMPLETA DEL SISTEMA
echo ========================================
echo.

REM ========================================
REM 1. Verificar NUC Local
REM ========================================
echo [1/5] Verificando NUC Local...
echo.

REM Verificar Tailscale
echo   - Verificando Tailscale...
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo     [OK] Tailscale esta corriendo
    for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
    if defined TAILSCALE_IP (
        echo     [OK] IP de Tailscale: %TAILSCALE_IP%
    ) else (
        echo     [ERROR] Tailscale no tiene IP asignada
        goto :error
    )
) else (
    echo     [ERROR] Tailscale NO esta corriendo
    goto :error
)

REM Verificar puente genérico
echo   - Verificando puente generico...
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    echo     [OK] Puente generico esta corriendo (puerto 5000)
    
    REM Probar respuesta
    curl -s http://localhost:5000/api/status > nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo     [OK] El puente responde correctamente
    ) else (
        echo     [ERROR] El puente no responde
        goto :error
    )
) else (
    echo     [ERROR] Puente generico NO esta corriendo
    goto :error
)

echo.
echo [OK] NUC Local: TODO CORRECTO
echo.

REM ========================================
REM 2. Verificar conexión desde NUC a Railway
REM ========================================
echo [2/5] Verificando Backend en Railway...
echo.

REM Intentar obtener la URL de Railway desde config.py o variable de entorno
set RAILWAY_URL=https://apptelink-vision-production.up.railway.app

echo   - Probando conexion a Railway: %RAILWAY_URL%
curl -s -o nul -w "%%{http_code}" %RAILWAY_URL%/api/status 2>nul | findstr /R "^200" > nul
if %ERRORLEVEL% EQU 0 (
    echo     [OK] Railway backend esta respondiendo
) else (
    echo     [ADVERTENCIA] No se pudo conectar a Railway (puede ser normal si no esta desplegado)
    echo     [INFO] Verifica manualmente: curl %RAILWAY_URL%/api/status
)

echo.

REM ========================================
REM 3. Verificar que Railway puede conectarse al NUC
REM ========================================
echo [3/5] Verificando conexion Railway -> NUC...
echo.
echo   [INFO] Esta verificacion debe hacerse desde Railway
echo   [INFO] Revisa los logs de Railway para ver si puede conectarse a:
echo   [INFO]   http://%TAILSCALE_IP%:5000/api/status
echo.

REM ========================================
REM 4. Verificar Frontend
REM ========================================
echo [4/5] Verificando Frontend...
echo.

set FRONTEND_URL=https://impartial-wisdom-production-3c22.up.railway.app
echo   - URL del Frontend: %FRONTEND_URL%
echo   [INFO] Abre esta URL en tu navegador para verificar
echo.

REM ========================================
REM 5. Verificar configuración
REM ========================================
echo [5/5] Verificando configuracion...
echo.

if exist "config.py" (
    echo   [OK] Archivo config.py existe
    findstr /C:"100.92.50.72" config.py > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] IP de Tailscale configurada en config.py
    ) else (
        echo   [ADVERTENCIA] IP de Tailscale no encontrada en config.py
    )
    
    findstr /C:"192.168.60" config.py > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Red local configurada en config.py
    ) else (
        echo   [ADVERTENCIA] Red local no encontrada en config.py
    )
) else (
    echo   [ERROR] Archivo config.py no existe
)

echo.

REM ========================================
REM RESUMEN
REM ========================================
echo ========================================
echo RESUMEN
echo ========================================
echo.
echo NUC Local:
echo   - Tailscale IP: %TAILSCALE_IP%
echo   - Puerto: 5000
echo   - Estado: [OK]
echo.
echo Railway Backend:
echo   - URL: %RAILWAY_URL%
echo   - Verifica manualmente: curl %RAILWAY_URL%/api/status
echo.
echo Railway Frontend:
echo   - URL: %FRONTEND_URL%
echo   - Abre en navegador para verificar
echo.
echo ========================================
echo SIGUIENTES PASOS
echo ========================================
echo.
echo 1. Verifica que Railway tenga configurado:
echo    NUC_URLS=nuc_sede1:http://%TAILSCALE_IP%:5000
echo.
echo 2. Abre el frontend en tu navegador:
echo    %FRONTEND_URL%
echo.
echo 3. Revisa la consola del navegador (F12) para ver errores
echo.
echo 4. Si hay problemas, revisa los logs de Railway
echo.
goto :end

:error
echo.
echo ========================================
echo ERROR DETECTADO
echo ========================================
echo.
echo Hay un problema con la configuracion del NUC.
echo Revisa los errores anteriores y corrigelos.
echo.
pause
exit /b 1

:end
echo.
pause
