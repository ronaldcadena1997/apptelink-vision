@echo off
REM Script para subir TODOS los cambios (CORS + Tailscale fix)

echo ========================================
echo SUBIR TODOS LOS CAMBIOS
echo ========================================
echo.
echo Incluye:
echo   - Correccion de CORS
echo   - Correccion de script Tailscale (remover flag invalido)
echo.

cd /d "%~dp0"

echo [1/2] Agregando archivos...
git add backend/server.py backend/start_with_tailscale.sh
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados
) else (
    echo   [ERROR] No se pudo agregar archivos
    pause
    exit /b 1
)

echo.
echo [2/2] Haciendo commit y push...
git commit -m "Corregir CORS y script Tailscale (remover flag invalido --socks5-server de tailscale up)"
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Commit realizado
) else (
    echo   [ADVERTENCIA] No hay cambios nuevos o commit fallo
)

git push
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Push realizado exitosamente
    echo.
    echo ========================================
    echo SIGUIENTE PASO
    echo ========================================
    echo.
    echo Despues de que Railway se redesplegue (2-3 minutos):
    echo   1. Revisa los logs de Railway:
    echo      - NO debe mostrar: "flag provided but not defined: -socks5-server"
    echo      - Debe mostrar: "Tailscale conectado. IP: ..."
    echo   2. Prueba el frontend:
    echo      - El error de CORS deberia desaparecer
    echo      - El frontend deberia poder conectarse al backend
    echo   3. Si funciona, prueba las imagenes de las camaras
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
