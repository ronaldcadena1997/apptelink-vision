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

echo [2/5] Agregando archivos modificados...
git add src/config/api.js
git add backend/server.py
git add backend/puente_generico_nuc.py
git add backend/SOLUCION_WEB_NO_MUESTRA_DATOS.md
git add backend/DIAGNOSTICO_FRONTEND.md
git add backend/SOLUCION_SIN_ACCESO_CAMARA.md
echo.

echo [3/5] Verificando archivos en staging...
git status --short
echo.

echo [4/5] Haciendo commit...
git commit -m "Fix: Mejorar conexion frontend-backend y agregar endpoint snapshot al puente NUC"
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
echo Push completado!
echo ========================================
echo.
echo Railway detectara los cambios automaticamente y desplegara.
echo Espera 2-3 minutos para que Railway termine el despliegue.
echo.
pause
