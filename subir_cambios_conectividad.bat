@echo off
REM Script para subir los cambios de conectividad

echo ========================================
echo SUBIR CAMBIOS DE CONECTIVIDAD
echo ========================================
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
git commit -m "Agregar endpoint de prueba de conectividad y mejor logging"
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
    echo   1. Prueba: https://apptelink-vision-production.up.railway.app/api/test/nuc
    echo   2. Revisa los logs de Railway
    echo   3. Comparte la respuesta del endpoint
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
