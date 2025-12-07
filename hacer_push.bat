@echo off
echo ========================================
echo Haciendo push a GitHub...
echo ========================================
echo.

cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision"

echo [1/4] Verificando estado de git...
git status
echo.

echo [2/4] Agregando archivos modificados...
git add src/config/api.js
git add backend/SOLUCION_FRONTEND_NO_FUNCIONA.md
echo.

echo [3/4] Haciendo commit...
git commit -m "Fix: Actualizar api.js para usar Railway en produccion automaticamente"
echo.

echo [4/4] Haciendo push a GitHub...
git push
echo.

echo ========================================
echo Push completado!
echo ========================================
echo.
echo Verifica en Railway que el despliegue se active automaticamente.
pause
