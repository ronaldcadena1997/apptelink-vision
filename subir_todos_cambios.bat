@echo off
cd /d "%~dp0"

echo ========================================
echo SUBIENDO TODOS LOS CAMBIOS
echo ========================================
echo.

echo [1] Verificando estado de Git...
git status
echo.

echo [2] Agregando todos los archivos modificados...
git add -A
echo [OK] Archivos agregados
echo.

echo [3] Mostrando archivos que se subirán...
git status --short
echo.

echo [4] Creando commit...
git commit -m "Implementacion completa arquitectura Hikvision: NUC agent, backend SocketIO, mejoras en frontend, instrucciones manuales"
echo [OK] Commit creado
echo.

echo [5] Subiendo a GitHub...
git push
echo.

echo ========================================
echo COMPLETADO
echo ========================================
echo.
echo Verifica en GitHub que los cambios se subieron correctamente.
pause
