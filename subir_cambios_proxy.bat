@echo off
REM Script para subir los cambios del proxy SOCKS5

echo ========================================
echo SUBIR CAMBIOS DE PROXY SOCKS5
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Agregando archivos...
git add backend/server.py backend/start_with_tailscale.sh backend/requirements.txt
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados
) else (
    echo   [ERROR] No se pudo agregar archivos
    pause
    exit /b 1
)

echo.
echo [2/2] Haciendo commit y push...
git commit -m "Configurar proxy SOCKS5 para Tailscale userspace-networking"
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
    echo Despues de que Railway se redesplegue:
    echo   1. Espera 2-3 minutos para que se complete el despliegue
    echo   2. Prueba: https://apptelink-vision-production.up.railway.app/api/test/nuc
    echo   3. Revisa los logs de Railway para ver si el proxy se configuro
    echo   4. Si funciona, prueba el frontend para ver las imagenes
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
