@echo off
REM Script para verificar si OpenCV está instalado y funciona

echo ========================================
echo VERIFICACION DE OPENCV
echo ========================================
echo.

echo [1/3] Verificando si OpenCV esta instalado...
python -c "import cv2; print('OpenCV version:', cv2.__version__)" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] OpenCV esta instalado
) else (
    echo   [ERROR] OpenCV NO esta instalado
    echo   [INFO] Instalando OpenCV...
    pip install opencv-python-headless
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] OpenCV instalado correctamente
    ) else (
        echo   [ERROR] No se pudo instalar OpenCV
        echo   [INFO] Intenta manualmente: pip install opencv-python-headless
        pause
        exit /b 1
    )
)
echo.

echo [2/3] Verificando que el puente esta corriendo...
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Puente esta corriendo
) else (
    echo   [ERROR] Puente NO esta corriendo
    echo   [INFO] Ejecuta: ejecutar_puente_silencioso.bat
    pause
    exit /b 1
)
echo.

echo [3/3] Probando endpoint de snapshot localmente...
echo   Probando: http://localhost:5000/api/camaras/192.168.60.65/snapshot
curl -s http://localhost:5000/api/camaras/192.168.60.65/snapshot > test_snapshot.json 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Endpoint responde
    echo   [INFO] Revisando respuesta...
    findstr /C:"success" test_snapshot.json > nul
    if %ERRORLEVEL% EQU 0 (
        findstr /C:"true" test_snapshot.json > nul
        if %ERRORLEVEL% EQU 0 (
            echo   [OK] Snapshot obtenido exitosamente
        ) else (
            echo   [ERROR] Snapshot fallo - Revisa test_snapshot.json para ver el error
            type test_snapshot.json
        )
    ) else (
        echo   [ERROR] Respuesta inesperada - Revisa test_snapshot.json
        type test_snapshot.json
    )
) else (
    echo   [ERROR] No se pudo conectar al endpoint
)
echo.

echo ========================================
echo RESUMEN
echo ========================================
echo.
echo Si OpenCV esta instalado y el snapshot funciona localmente,
echo pero aun ves "sin_acceso" en el frontend, el problema es
echo que Railway no puede conectarse al NUC para obtener snapshots.
echo.
echo Siguiente paso: Verifica los logs de Railway para ver el error exacto.
echo.

del test_snapshot.json 2>nul
pause
