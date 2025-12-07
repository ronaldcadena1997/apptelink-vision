@echo off
echo ========================================
echo Haciendo Git Push de los cambios
echo ========================================
echo.

cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision"

echo [1/5] Verificando estado de Git...
git status
echo.

echo [2/5] Agregando archivos modificados...
git add backend/config.py
git add backend/MI_CONFIGURACION.md
git add backend/PASOS_EJECUTAR_PUENTE_NUC.md
git add backend/CONFIGURACION_CAMARAS_POR_NUC.md
echo.

echo [3/5] Verificando cambios a commitear...
git status
echo.

echo [4/5] Haciendo commit...
git commit -m "Config: Actualizar config.py con IPs específicas (Tailscale: 100.92.50.72, Cámara: 192.168.60.65)"
echo.

echo [5/5] Haciendo push al repositorio remoto...
git push
echo.

echo ========================================
echo Proceso completado
echo ========================================
echo.
echo Si hay errores, verifica:
echo 1. Que estes conectado a internet
echo 2. Que tengas permisos en el repositorio
echo 3. Que la rama sea correcta (main/master)
echo.
pause
