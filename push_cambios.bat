@echo off
chcp 65001 >nul
echo ========================================
echo Subiendo cambios a GitHub...
echo ========================================
echo.

cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision"

echo [1/5] Verificando estado de git...
git status
echo.
echo Presiona una tecla para continuar...
pause >nul

echo [2/5] Agregando archivos modificados...
git add src/config/api.js
git add backend/SOLUCION_FRONTEND_NO_FUNCIONA.md
echo Archivos agregados.
echo.

echo [3/5] Verificando archivos en staging...
git status --short
echo.

echo [4/5] Haciendo commit...
git commit -m "Fix: Forzar uso de Railway siempre (puente NUC no tiene endpoints de camaras)"
echo Commit realizado.
echo.

echo [5/5] Haciendo push a GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo Intentando con 'master'...
    git push origin master
)
echo.

echo ========================================
echo Proceso completado!
echo ========================================
echo.
echo Verifica en Railway que el despliegue se active automaticamente.
echo.
pause
