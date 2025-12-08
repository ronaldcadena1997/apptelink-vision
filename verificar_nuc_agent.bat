@echo off
cd /d "%~dp0"

echo ========================================
echo VERIFICACIÓN DEL NUC AGENT
echo ========================================
echo.

echo [1] Verificando procesos de Python...
tasklist | findstr python
if %ERRORLEVEL% EQU 0 (
    echo [OK] Hay procesos de Python corriendo
) else (
    echo [ADVERTENCIA] No se encontraron procesos de Python
    echo    El NUC Agent probablemente no está corriendo
)
echo.

echo [2] Verificando dependencias...
python -c "import websocket; print('✅ websocket-client OK')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] websocket-client no está instalado
    echo    Ejecuta: pip install websocket-client
)

python -c "import socketio; print('✅ socketio OK')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] socketio no está instalado
    echo    Ejecuta: pip install python-socketio
)

python -c "import cv2; print('✅ opencv OK')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] opencv no está instalado
    echo    Ejecuta: pip install opencv-python-headless
)
echo.

echo [3] Verificando configuración...
if exist "backend\config.py" (
    echo [OK] config.py existe
    python -c "from backend.config import CAMARAS_CONFIGURADAS, NUCs_CONFIG; print(f'✅ Cámaras configuradas: {len(CAMARAS_CONFIGURADAS)}'); print(f'✅ NUCs configurados: {len(NUCs_CONFIG)}')" 2>nul
) else (
    echo [ERROR] config.py no existe
)
echo.

echo [4] Verificando conectividad a la cámara...
if exist "backend\config.py" (
    python -c "from backend.config import CAMARAS_CONFIGURADAS; import subprocess; ip = CAMARAS_CONFIGURADAS[0] if CAMARAS_CONFIGURADAS else '192.168.60.65'; subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)" 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo [OK] La cámara responde al ping
    ) else (
        echo [ADVERTENCIA] La cámara no responde al ping
    )
)
echo.

echo ========================================
echo RESUMEN
echo ========================================
echo.
echo Si el NUC Agent no está corriendo:
echo   1. Ejecuta: .\ejecutar_nuc_agent_hikvision.bat
echo   2. O configura inicio automático: .\configurar_nuc_agent_automatico.bat
echo.
echo Si hay errores de dependencias:
echo   1. Ejecuta: .\instalar_dependencias_nuc.bat
echo.
pause
