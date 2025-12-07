@echo off
REM Script para verificar y subir el script de Tailscale

echo ========================================
echo VERIFICAR Y SUBIR SCRIPT DE TAILSCALE
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Verificando archivos...
if not exist "backend\start_with_tailscale.sh" (
    echo   [ERROR] start_with_tailscale.sh no existe en backend
    pause
    exit /b 1
)

if not exist "backend\Dockerfile" (
    echo   [ERROR] Dockerfile no existe en backend
    pause
    exit /b 1
)

echo   [OK] Archivos encontrados
echo.

echo [2/3] Verificando contenido del Dockerfile...
findstr /C:"start_with_tailscale.sh" backend\Dockerfile > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Dockerfile referencia start_with_tailscale.sh
) else (
    echo   [ERROR] Dockerfile NO referencia start_with_tailscale.sh
    echo   [INFO] Verifica que el Dockerfile tenga: CMD ["/app/start_with_tailscale.sh"]
    pause
    exit /b 1
)

findstr /C:"CMD" backend\Dockerfile | findstr /C:"start_with_tailscale" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Dockerfile tiene CMD correcto
) else (
    echo   [ADVERTENCIA] Dockerfile puede no tener el CMD correcto
    echo   [INFO] Verifica que tenga: CMD ["/app/start_with_tailscale.sh"]
)
echo.

echo [3/3] Agregando archivos a Git...
git add backend/start_with_tailscale.sh backend/Dockerfile 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Archivos agregados a Git
) else (
    echo   [ADVERTENCIA] No se pudieron agregar archivos (puede ser normal si ya estan agregados)
)

echo.
echo Verificando estado de Git...
git status backend/start_with_tailscale.sh backend/Dockerfile
echo.

echo ========================================
echo SIGUIENTE PASO
echo ========================================
echo.
echo Si los archivos tienen cambios, ejecuta:
echo   git commit -m "Asegurar que start_with_tailscale.sh este en el repositorio"
echo   git push
echo.
echo Luego en Railway Dashboard:
echo   1. Ve a Settings -^> Build
echo   2. Verifica que "Dockerfile Path" sea: backend/Dockerfile
echo   3. Haz "Redeploy"
echo.

pause
