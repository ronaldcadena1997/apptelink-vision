@echo off
REM Script para subir mejoras de logging en snapshot

echo ========================================
echo MEJORAR LOGGING DE SNAPSHOT
echo ========================================
echo.
echo Cambio: Agregar logging detallado para diagnosticar problemas de imagen
echo.

cd /d "%~dp0"

echo [1/2] Agregando archivos...
git add backend/server.py backend/DIAGNOSTICO_IMAGEN_NO_CARGA.md
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados
) else (
    echo   [ERROR] No se pudo agregar archivos
    pause
    exit /b 1
)

echo.
echo [2/2] Haciendo commit y push...
git commit -m "Mejorar logging de snapshot para diagnosticar problemas de carga de imagenes"
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
    echo   1. Intenta ver la imagen de la camara en el frontend
    echo   2. Revisa los logs de Railway
    echo   3. Busca los mensajes:
    echo      - "📸 Obteniendo snapshot desde NUC"
    echo      - "✅ Usando proxy SOCKS5" o "⚠️ NO se está usando proxy SOCKS5"
    echo      - "✅ Respuesta recibida: Status ..."
    echo   4. Comparte los logs conmigo para diagnosticar
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)

echo.
pause
