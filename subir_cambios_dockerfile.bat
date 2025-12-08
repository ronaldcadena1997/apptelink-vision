@echo off
cd /d "%~dp0"

echo ========================================
echo SUBIENDO CORRECCION DOCKERFILE
echo ========================================
echo.

echo [1] Agregando archivos...
git add Dockerfile
git add backend/Dockerfile.hikvision
git add backend/server_hikvision_style.py
git add backend/config.py
git add SOLUCION_ERROR_DOCKERFILE.md
echo [OK] Archivos agregados
echo.

echo [2] Verificando cambios...
git status --short
echo.

echo [3] Creando commit...
git commit -m "Corregir error Dockerfile: crear Dockerfile en raiz, verificar archivos copiados"
echo [OK] Commit creado
echo.

echo [4] Subiendo a GitHub...
git push
echo.

echo ========================================
echo COMPLETADO
echo ========================================
echo.
echo En Railway:
echo   1. Verifica que Dockerfile Path sea: Dockerfile
echo   2. Verifica que Root Directory este vacio
echo   3. Espera 2-5 minutos para que se redespliegue
pause
