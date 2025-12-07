@echo off
cd /d "%~dp0"

echo ========================================
echo SUBIENDO CAMBIOS - ARQUITECTURA HIKVISION
echo ========================================
echo.

echo [1] Agregando archivos...
git add backend/server_hikvision_style.py
git add backend/nuc_agent_hikvision.py
git add backend/config.py
git add backend/requirements.txt
git add backend/Dockerfile.hikvision
git add ejecutar_nuc_agent_hikvision.bat
git add configurar_nuc_agent_automatico.bat
git add ARQUITECTURA_HIKVISION.md
git add ARQUITECTURAS_ALTERNATIVAS.md
git add GUIA_IMPLEMENTACION_HIKVISION.md
git add MIGRACION_HIKVISION.md
git add CONFIGURACION_NUCS_CAMARAS.md
echo [OK] Archivos agregados
echo.

echo [2] Creando commit...
git commit -m "Implementar arquitectura estilo Hikvision con config.py"
echo [OK] Commit creado
echo.

echo [3] Subiendo a GitHub...
git push
echo.

echo ========================================
echo COMPLETADO
echo ========================================
pause
