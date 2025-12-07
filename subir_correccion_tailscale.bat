@echo off
REM Script para subir la corrección del script de Tailscale

echo ========================================
echo SUBIR CORRECCION DE TAILSCALE
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Agregando archivo corregido...
git add backend/start_with_tailscale.sh
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivo agregado
) else (
    echo   [ERROR] No se pudo agregar el archivo
    pause
    exit /b 1
)

echo.
echo [2/2] Haciendo commit y push...
git commit -m "Corregir Tailscale para usar userspace-networking en Railway"
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
    echo COMPLETADO
    echo ========================================
    echo.
    echo Railway se redesplegara automaticamente.
    echo Espera 2-3 minutos y revisa los logs.
    echo.
    echo Ahora deberias ver:
    echo   - Tailscale iniciando correctamente
    echo   - Tailscale conectado. IP: 100.xx.xx.xx
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
