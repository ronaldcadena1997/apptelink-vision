@echo off
REM Script para subir los cambios de Tailscale a Railway

echo ========================================
echo SUBIR CAMBIOS DE TAILSCALE
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Verificando archivos necesarios...
if not exist "backend\Dockerfile" (
    echo   [ERROR] Dockerfile no existe
    pause
    exit /b 1
)

if not exist "backend\start_with_tailscale.sh" (
    echo   [ERROR] start_with_tailscale.sh no existe
    pause
    exit /b 1
)

echo   [OK] Archivos encontrados
echo.

echo [2/4] Agregando archivos a Git...
git add backend/Dockerfile backend/start_with_tailscale.sh backend/Dockerfile.original 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados
) else (
    echo   [ADVERTENCIA] Algunos archivos pueden no existir
)
echo.

echo [3/4] Haciendo commit...
git commit -m "Agregar soporte para Tailscale en Railway"
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Commit realizado
) else (
    echo   [ADVERTENCIA] No hay cambios nuevos o commit fallo
)
echo.

echo [4/4] Haciendo push a GitHub...
git push
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Push realizado exitosamente
    echo.
    echo ========================================
    echo SIGUIENTE PASO
    echo ========================================
    echo.
    echo 1. Ve a Railway Dashboard
    echo 2. Selecciona tu proyecto de BACKEND
    echo 3. Abre la pestaña "Variables"
    echo 4. Agrega una nueva variable:
    echo    - Name: TAILSCALE_AUTHKEY
    echo    - Value: (la auth key que copiaste de Tailscale)
    echo 5. Railway se redesplegara automaticamente
    echo.
) else (
    echo   [ERROR] Push fallo
    echo   [INFO] Verifica tu conexion a internet y credenciales de Git
)
echo.

pause
