@echo off
cd /d "%~dp0"

echo ========================================
echo SUBIENDO CORRECCIONES - SIN ACCESO
echo ========================================
echo.

echo [1] Agregando archivos modificados...
git add backend/server_hikvision_style.py
git add backend/nuc_agent_hikvision.py
git add backend/config.py
git add backend/Dockerfile.hikvision
git add .
echo [OK] Archivos agregados
echo.

echo [2] Verificando cambios...
git status --short
echo.

echo [3] Creando commit...
git commit -m "Corregir problema sin acceso: mejorar deteccion de estado, agregar logging, soporte HTTP snapshots Hikvision, verificar snapshots guardados"
echo [OK] Commit creado
echo.

echo [4] Subiendo a GitHub...
git push
echo.

echo ========================================
echo COMPLETADO
echo ========================================
echo.
echo Los cambios se subiran a Railway automaticamente.
echo Espera 2-5 minutos y verifica los logs.
pause
