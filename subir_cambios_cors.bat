@echo off
REM Script para subir los cambios de CORS

echo ========================================
echo SUBIR CAMBIOS DE CORS
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
git commit -m "Corregir configuración CORS con múltiples métodos (Flask-CORS + after_request + OPTIONS handler)"
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
    echo   2. Prueba el frontend nuevamente
    echo   3. El error de CORS deberia desaparecer
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
