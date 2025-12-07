@echo off
REM Script para subir cambios de stream

echo ========================================
echo AGREGAR STREAM AL PUENTE GENERICO
echo ========================================
echo.
echo Cambios:
echo   - Agregar endpoint /api/camaras/<ip>/stream al puente generico del NUC
echo   - Modificar backend de Railway para hacer proxy al stream del NUC
echo.

cd /d "%~dp0"

echo [1/2] Agregando archivos...
git add backend/puente_generico_nuc.py backend/server.py
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados
) else (
    echo   [ERROR] No se pudo agregar archivos
    pause
    exit /b 1
)

echo.
echo [2/2] Haciendo commit y push...
git commit -m "Agregar endpoint de stream MJPEG al puente generico y proxy desde Railway"
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
    echo IMPORTANTE: Despues del redespliegue:
    echo   1. Reinicia el puente generico en el NUC:
    echo      - Detenlo si esta corriendo
    echo      - Ejecuta: ejecutar_puente_silencioso.bat
    echo   2. Espera 2-3 minutos para que Railway se redesplegue
    echo   3. Prueba el stream en el frontend:
    echo      - Presiona "En Vivo" o "Ver en vivo"
    echo      - Deberias ver la transmision en tiempo real
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
