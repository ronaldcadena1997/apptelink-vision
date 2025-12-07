@echo off
REM ========================================
REM SUBIR CAMBIOS - ARQUITECTURA HIKVISION
REM ========================================

cd /d "%~dp0"

echo ========================================
echo SUBIENDO CAMBIOS - ARQUITECTURA HIKVISION
echo ========================================
echo.

REM Verificar que estamos en un repositorio git
git status >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se encontro repositorio git
    echo [INFO] Asegurate de estar en el directorio del proyecto
    pause
    exit /b 1
)

echo [1/4] Agregando archivos modificados...
echo.

REM Agregar archivos del backend
git add backend/server_hikvision_style.py
git add backend/nuc_agent_hikvision.py
git add backend/config.py
git add backend/requirements.txt
git add backend/Dockerfile.hikvision

REM Agregar scripts
git add ejecutar_nuc_agent_hikvision.bat
git add configurar_nuc_agent_automatico.bat

REM Agregar documentación
git add ARQUITECTURA_HIKVISION.md
git add ARQUITECTURAS_ALTERNATIVAS.md
git add GUIA_IMPLEMENTACION_HIKVISION.md
git add MIGRACION_HIKVISION.md

echo [OK] Archivos agregados
echo.

echo [2/4] Verificando cambios...
echo.
git status --short
echo.

echo [3/4] Creando commit...
echo.
git commit -m "Implementar arquitectura estilo Hikvision

- Agregar server_hikvision_style.py (backend con WebSocket)
- Agregar nuc_agent_hikvision.py (agente que se conecta al servidor)
- Actualizar requirements.txt con flask-socketio y redis
- Agregar Dockerfile.hikvision (sin Tailscale)
- Usar config.py para configuración de NUCs y cámaras
- Agregar scripts de ejecución y configuración automática
- Agregar documentación completa"

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se pudo crear el commit
    echo [INFO] Verifica que hay cambios para commitear
    pause
    exit /b 1
)

echo [OK] Commit creado
echo.

echo [4/4] Subiendo cambios a GitHub...
echo.
git push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo CAMBIOS SUBIDOS EXITOSAMENTE
    echo ========================================
    echo.
    echo Proximos pasos:
    echo   1. En Railway, cambia Dockerfile a Dockerfile.hikvision
    echo   2. Agrega Redis en Railway (opcional pero recomendado)
    echo   3. Ejecuta nuc_agent_hikvision.py en el NUC
    echo.
) else (
    echo.
    echo [ERROR] No se pudo subir los cambios
    echo [INFO] Verifica tu conexion a internet y permisos de git
    echo.
)

pause
