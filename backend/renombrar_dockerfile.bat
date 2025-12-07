@echo off
REM Script para renombrar los Dockerfiles para usar Tailscale

echo ========================================
echo RENOMBRAR DOCKERFILE PARA TAILSCALE
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Verificando archivos...
if not exist "Dockerfile" (
    echo   [ERROR] Dockerfile no existe
    echo   [INFO] Verifica que estes en la carpeta backend
    pause
    exit /b 1
)

if not exist "Dockerfile.tailscale" (
    echo   [ERROR] Dockerfile.tailscale no existe
    echo   [INFO] Verifica que el archivo este en la carpeta
    pause
    exit /b 1
)

echo   [OK] Archivos encontrados
echo.

echo [2/3] Renombrando Dockerfiles...
if exist "Dockerfile.original" (
    echo   [INFO] Dockerfile.original ya existe, se mantendra
) else (
    ren Dockerfile Dockerfile.original
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Dockerfile renombrado a Dockerfile.original
    ) else (
        echo   [ERROR] No se pudo renombrar Dockerfile
        pause
        exit /b 1
    )
)

ren Dockerfile.tailscale Dockerfile
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Dockerfile.tailscale renombrado a Dockerfile
) else (
    echo   [ERROR] No se pudo renombrar Dockerfile.tailscale
    pause
    exit /b 1
)
echo.

echo [3/3] Verificando resultado...
if exist "Dockerfile" (
    echo   [OK] Dockerfile existe (con Tailscale)
) else (
    echo   [ERROR] Dockerfile no existe despues de renombrar
    pause
    exit /b 1
)

if exist "Dockerfile.original" (
    echo   [OK] Dockerfile.original existe (backup)
)

echo.
echo ========================================
echo COMPLETADO
echo ========================================
echo.
echo Archivos:
dir Dockerfile* /b
echo.
echo Siguiente paso:
echo   1. Haz push de los cambios: git add Dockerfile Dockerfile.original start_with_tailscale.sh
echo   2. git commit -m "Agregar soporte para Tailscale en Railway"
echo   3. git push
echo   4. Agrega la variable TAILSCALE_AUTHKEY en Railway Dashboard
echo.
pause
