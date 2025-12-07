@echo off
setlocal enabledelayedexpansion

echo ============================================
echo DIAGNOSTICO DE CONEXION NUC - RAILWAY
echo ============================================
echo.

echo [1/5] Verificando API local del NUC...
echo.
curl -s http://localhost:5000/api/status >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo [OK] API local funcionando
    curl http://localhost:5000/api/status
) else (
    echo [ERROR] API local NO responde
)
echo.
echo.

echo [2/5] Verificando Tailscale en NUC...
echo.
tailscale status >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo [OK] Tailscale esta corriendo
    tailscale status
) else (
    echo [ERROR] Tailscale NO esta corriendo
)
echo.
echo.

echo [3/5] Obteniendo IP de Tailscale del NUC...
echo.
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
if defined TAILSCALE_IP (
    echo IP de Tailscale: !TAILSCALE_IP!
) else (
    echo [ERROR] No se pudo obtener IP de Tailscale
    set TAILSCALE_IP=
)
echo.

echo [4/5] Verificando que el API responda desde la IP de Tailscale...
echo.
if defined TAILSCALE_IP (
    curl -s http://!TAILSCALE_IP!:5000/api/status >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [OK] API accesible desde Tailscale
        curl http://!TAILSCALE_IP!:5000/api/status
    ) else (
        echo [ERROR] API NO accesible desde Tailscale
    )
) else (
    echo [ERROR] No se puede verificar - IP de Tailscale no disponible
)
echo.
echo.

echo [5/5] Verificando procesos Python...
echo.
tasklist | findstr /i python
if !ERRORLEVEL! EQU 0 (
    echo [OK] Procesos Python encontrados
) else (
    echo [ERROR] No se encontraron procesos Python
)
echo.
echo.

echo ============================================
echo DIAGNOSTICO COMPLETADO
echo ============================================
pause
