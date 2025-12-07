@echo off
REM Script para subir captura automática de snapshot

echo ========================================
echo CAPTURA AUTOMATICA DE SNAPSHOT
echo ========================================
echo.
echo Cambio: Capturar snapshot automaticamente cuando:
echo   - Se detecta una camara activa
echo   - Se selecciona una camara activa
echo.

cd /d "%~dp0"

echo [1/2] Agregando archivos...
git add src/screens/CamaraScreen.js
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados
) else (
    echo   [ERROR] No se pudo agregar archivos
    pause
    exit /b 1
)

echo.
echo [2/2] Haciendo commit y push...
git commit -m "Agregar captura automatica de snapshot cuando se detecta o selecciona camara activa"
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
    echo Despues de que el frontend se redesplegue:
    echo   1. La imagen se capturara automaticamente cuando:
    echo      - Detectes camaras y la primera este activa
    echo      - Selecciones una camara activa
    echo   2. Ya no necesitaras presionar "Capturar" manualmente
    echo   3. La imagen deberia aparecer automaticamente
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
