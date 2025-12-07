@echo off
REM Script para subir corrección del estado de cámara

echo ========================================
echo CORREGIR ESTADO DE CAMARA
echo ========================================
echo.
echo Cambio: Usar endpoint correcto para verificar acceso a camara
echo   - Antes: /proxy/{ip}:554/stream (no existe)
echo   - Ahora: /api/camaras/{ip}/snapshot (existe)
echo.

cd /d "%~dp0"

echo [1/2] Agregando archivos...
git add backend/server.py
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados
) else (
    echo   [ERROR] No se pudo agregar archivos
    pause
    exit /b 1
)

echo.
echo [2/2] Haciendo commit y push...
git commit -m "Corregir verificacion de estado de camara: usar endpoint /api/camaras/{ip}/snapshot"
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
    echo   1. Prueba el frontend nuevamente
    echo   2. Haz clic en "DETECTAR CAMARAS EN LA RED"
    echo   3. La camara deberia mostrar "Activa" en lugar de "SIN ACCESO"
    echo   4. Si funciona, las imagenes deberian cargarse correctamente
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
