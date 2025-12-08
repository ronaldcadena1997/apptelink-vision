@echo off
cd /d "%~dp0"

echo ========================================
echo SUBIENDO CORRECCIÓN ERROR 500
echo ========================================
echo.

echo [1] Verificando cambios...
git status --short
echo.

echo [2] Agregando archivos corregidos...
git add backend/server_hikvision_style.py
echo [OK] Archivo agregado
echo.

echo [3] Creando commit...
git commit -m "Corregir error 500 en endpoints /api/camaras y /api/camaras/detectar: agregar manejo robusto de errores"
echo [OK] Commit creado
echo.

echo [4] Subiendo a GitHub...
git push
echo.

echo ========================================
echo COMPLETADO
echo ========================================
echo.
echo Los cambios se subirán a Railway automáticamente.
echo Espera 2-5 minutos y prueba de nuevo los endpoints:
echo   - /api/camaras
echo   - /api/camaras/detectar
pause
