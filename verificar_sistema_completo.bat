@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================
echo VERIFICACION COMPLETA DEL SISTEMA
echo ========================================
echo.

echo [1] Verificando procesos de Python...
tasklist | findstr /I python > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] Hay procesos de Python corriendo
    tasklist | findstr /I python
) else (
    echo    [ADVERTENCIA] No se encontraron procesos de Python
    echo    El NUC Agent probablemente no esta corriendo
)
echo.

echo [2] Verificando dependencias de Python...
echo    - websocket-client...
python -c "import websocket; print('      [OK] websocket-client instalado')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo    [ERROR] websocket-client NO esta instalado
    echo    Ejecuta: pip install websocket-client
)

echo    - socketio...
python -c "import socketio; print('      [OK] socketio instalado')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo    [ERROR] socketio NO esta instalado
    echo    Ejecuta: pip install python-socketio
)

echo    - opencv...
python -c "import cv2; print('      [OK] opencv instalado')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo    [ERROR] opencv NO esta instalado
    echo    Ejecuta: pip install opencv-python-headless
)
echo.

echo [3] Verificando archivos de configuracion...
if exist "backend\config.py" (
    echo    [OK] config.py existe
    python -c "from backend.config import CAMARAS_CONFIGURADAS, NUCs_CONFIG; print(f'      [OK] Camaras configuradas: {len(CAMARAS_CONFIGURADAS)}'); print(f'      [OK] NUCs configurados: {len(NUCs_CONFIG)}')" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo    [ADVERTENCIA] No se pudo importar config.py
    )
) else (
    echo    [ERROR] config.py NO existe
)
echo.

echo [4] Verificando conectividad a la camara...
if exist "backend\config.py" (
    python -c "from backend.config import CAMARAS_CONFIGURADAS; ip = CAMARAS_CONFIGURADAS[0] if CAMARAS_CONFIGURADAS else '192.168.60.65'; print(f'      Probando ping a {ip}...')" 2>nul
    ping -n 1 192.168.60.65 > nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo    [OK] La camara responde al ping (192.168.60.65)
    ) else (
        echo    [ADVERTENCIA] La camara NO responde al ping (192.168.60.65)
        echo    Verifica que la IP sea correcta y que la camara este encendida
    )
) else (
    echo    [ADVERTENCIA] No se puede verificar sin config.py
)
echo.

echo [5] Verificando archivos del NUC Agent...
if exist "backend\nuc_agent_hikvision.py" (
    echo    [OK] nuc_agent_hikvision.py existe
) else (
    echo    [ERROR] nuc_agent_hikvision.py NO existe
)

if exist "ejecutar_nuc_agent_hikvision.bat" (
    echo    [OK] ejecutar_nuc_agent_hikvision.bat existe
) else (
    echo    [ADVERTENCIA] ejecutar_nuc_agent_hikvision.bat NO existe
)
echo.

echo ========================================
echo RESUMEN
echo ========================================
echo.
echo Si el NUC Agent no esta corriendo:
echo   1. Ejecuta: .\ejecutar_nuc_agent_hikvision.bat
echo   2. O configura inicio automatico: .\configurar_nuc_agent_automatico.bat
echo.
echo Si hay errores de dependencias:
echo   1. Ejecuta: .\instalar_dependencias_nuc.bat
echo.
echo Para ver los logs del NUC Agent:
echo   1. Ejecuta: .\ejecutar_nuc_agent_hikvision.bat
echo   2. Observa la ventana para ver mensajes de conexion y snapshots
echo.
echo ========================================
pause
