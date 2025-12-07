@echo off
cd /d "%~dp0"

echo ========================================
echo SUBIENDO CORRECCIONES DE ERRORES
echo ========================================
echo.

echo [1] Agregando archivos corregidos...
git add backend/nuc_agent_hikvision.py
git add backend/server_hikvision_style.py
git add backend/requirements_nuc.txt
git add instalar_dependencias_nuc.bat
git add src/config/api.js
git add src/screens/CamaraScreen.js
echo [OK] Archivos agregados
echo.

echo [2] Creando commit...
git commit -m "Corregir errores: websocket-client, captura de camaras, manejo de errores 500 en frontend"
echo [OK] Commit creado
echo.

echo [3] Subiendo a GitHub...
git push
echo.

echo ========================================
echo COMPLETADO
echo ========================================
pause
