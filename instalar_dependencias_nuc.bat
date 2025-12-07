@echo off
REM ========================================
REM INSTALAR DEPENDENCIAS PARA NUC AGENT
REM ========================================

cd /d "%~dp0backend"

echo ========================================
echo INSTALANDO DEPENDENCIAS NUC AGENT
echo ========================================
echo.

echo [1/2] Instalando python-socketio y websocket-client...
pip install python-socketio>=5.10.0 websocket-client>=1.6.0
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas
echo.

echo [2/2] Verificando instalacion...
python -c "import socketio; import websocket; print('✅ socketio:', socketio.__version__); print('✅ websocket-client instalado')"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Las dependencias no se instalaron correctamente
    pause
    exit /b 1
)
echo.

echo ========================================
echo INSTALACION COMPLETADA
echo ========================================
echo.
echo Ahora puedes ejecutar el NUC Agent:
echo   .\ejecutar_nuc_agent_hikvision.bat
echo.
pause
