@echo off
REM Script para verificar la configuración de Tailscale en Railway

echo ========================================
echo VERIFICAR CONFIGURACION DE TAILSCALE
echo ========================================
echo.

echo [INFO] Este script te ayudara a verificar que todo este configurado
echo        correctamente para Tailscale en Railway.
echo.

echo ========================================
echo CHECKLIST
echo ========================================
echo.

echo 1. AUTH KEY DE TAILSCALE
echo    [ ] Tienes el valor completo de la auth key?
echo        - Debe empezar con: tskey-auth-
echo        - Formato: tskey-auth-xxxxx-xxxxx
echo        - NO es solo el ID (kq9X3n6tJ211CNTRL)
echo.
echo    Si NO lo tienes:
echo    - Ve a: https://login.tailscale.com/admin/settings/keys
echo    - Genera una nueva auth key
echo    - Copia el valor completo
echo.

echo 2. VARIABLE EN RAILWAY
echo    [ ] Variable TAILSCALE_AUTHKEY configurada en Railway?
echo    [ ] El valor es el valor completo (tskey-auth-...)?
echo.
echo    Verifica en: Railway Dashboard -^> Tu proyecto -^> Variables
echo.

echo 3. ARCHIVOS EN GITHUB
echo    [ ] Dockerfile tiene Tailscale instalado?
echo    [ ] start_with_tailscale.sh esta en el repositorio?
echo.
echo    Si no estan:
echo    - Ejecuta: subir_cambios_tailscale.bat
echo.

echo 4. DESPLIEGUE EN RAILWAY
echo    [ ] Railway se redesplego despues de agregar la variable?
echo    [ ] En los logs de Railway ves mensajes de Tailscale?
echo.
echo    Verifica en: Railway Dashboard -^> Tu proyecto -^> Logs
echo    Busca: "Iniciando Tailscale en Railway"
echo.

echo 5. TAILSCALE ADMIN CONSOLE
echo    [ ] Ves una maquina nueva de Railway en Tailscale?
echo    [ ] Esta marcada como "Online"?
echo.
echo    Verifica en: https://login.tailscale.com/admin/machines
echo.

echo 6. FRONTEND
echo    [ ] Las camaras muestran imagenes (no "sin_acceso")?
echo.
echo    Verifica en: https://impartial-wisdom-production-3c22.up.railway.app
echo.

echo ========================================
echo SIGUIENTE PASO
echo ========================================
echo.
echo 1. Abre Railway Dashboard
echo 2. Ve a tu proyecto de BACKEND
echo 3. Abre la pestaña "Logs"
echo 4. Busca mensajes que digan:
echo    - "Iniciando Tailscale en Railway"
echo    - "Tailscale conectado. IP: 100.xx.xx.xx"
echo.
echo Si ves estos mensajes: Todo esta funcionando!
echo Si ves errores: Revisa la seccion de troubleshooting.
echo.

pause
