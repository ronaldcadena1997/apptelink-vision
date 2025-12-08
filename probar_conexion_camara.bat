@echo off
cd /d "%~dp0"

echo ========================================
echo PROBAR CONEXION A LA CAMARA
echo ========================================
echo.

echo [1] Verificando que la camara responde...
ping -n 1 192.168.60.65
if %ERRORLEVEL% EQU 0 (
    echo [OK] La camara responde al ping
) else (
    echo [ERROR] La camara NO responde al ping
    echo    Verifica que la IP sea correcta y que la camara este encendida
    pause
    exit /b 1
)
echo.

echo [2] Verificando credenciales en config.py...
python -c "from backend.config import USUARIO_CAMARAS, CONTRASENA_CAMARAS; print(f'   Usuario: {USUARIO_CAMARAS}'); print(f'   Contrasena: {CONTRASENA_CAMARAS}')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se pudo leer config.py
)
echo.

echo [3] Probando HTTP Snapshot...
echo    Abriendo navegador con URL de prueba...
echo.
echo    Si te pide credenciales, usa las que aparecen arriba
echo    Si ves la imagen, las credenciales son correctas
echo    Si NO ves la imagen, las credenciales son incorrectas
echo.

python -c "from backend.config import USUARIO_CAMARAS, CONTRASENA_CAMARAS; import webbrowser; url = f'http://{USUARIO_CAMARAS}:{CONTRASENA_CAMARAS}@192.168.60.65/ISAPI/Streaming/channels/101/picture'; webbrowser.open(url); print(f'   URL probada: http://{USUARIO_CAMARAS}:***@192.168.60.65/ISAPI/Streaming/channels/101/picture')" 2>nul

echo.
echo [4] Instrucciones:
echo    - Si ves la imagen en el navegador: Las credenciales son correctas
echo    - Si NO ves la imagen: Actualiza las credenciales en config.py
echo.
echo    Para actualizar credenciales:
echo    1. Abre: backend\config.py
echo    2. Cambia USUARIO_CAMARAS y CONTRASENA_CAMARAS
echo    3. Guarda el archivo
echo    4. Reinicia el NUC Agent
echo.

pause
