@echo off
REM ========================================
REM SCRIPT COMPLETO: Iniciar Todo en el NUC
REM ========================================
REM Este script verifica e inicia:
REM   1. Tailscale (si no está corriendo)
REM   2. Puente genérico del NUC (si no está corriendo)
REM   3. Verifica que todo funcione correctamente
REM ========================================

setlocal enabledelayedexpansion

echo ========================================
echo INICIAR TODO - API DEL NUC
echo ========================================
echo.
echo Este script verificara e iniciara:
echo   [1] Tailscale
echo   [2] Puente generico del NUC
echo   [3] Verificacion de conectividad
echo.

cd /d "%~dp0"

REM ========================================
REM PASO 1: Verificar e Iniciar Tailscale
REM ========================================
echo [1/3] Verificando Tailscale...
echo.

REM Verificar si Tailscale está corriendo
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Tailscale esta corriendo
) else (
    echo   [INFO] Tailscale NO esta corriendo, iniciando...
    
    REM Buscar e iniciar Tailscale
    if exist "C:\Program Files\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files\Tailscale\tailscaled.exe"
        echo   [OK] Comando de inicio enviado
    ) else if exist "C:\Program Files (x86)\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files (x86)\Tailscale\tailscaled.exe"
        echo   [OK] Comando de inicio enviado
    ) else (
        echo   [ERROR] No se encontro Tailscale instalado
        echo   [INFO] Instala Tailscale desde: https://tailscale.com/download
        pause
        exit /b 1
    )
    
    REM Esperar a que Tailscale se inicie
    echo   [INFO] Esperando a que Tailscale se inicie (15 segundos)...
    timeout /t 15 /nobreak > nul
)

REM Verificar que Tailscale tenga IP
echo   [INFO] Verificando IP de Tailscale...
set TAILSCALE_IP=
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i

if not "!TAILSCALE_IP!"=="" (
    echo   [OK] IP de Tailscale: !TAILSCALE_IP!
    
    REM Verificar que la IP sea válida (debe empezar con 100.)
    echo !TAILSCALE_IP! | findstr /R "^100\." > nul
    if !ERRORLEVEL! EQU 0 (
        echo   [OK] IP de Tailscale es valida
    ) else (
        echo   [ADVERTENCIA] IP de Tailscale no es valida (debe empezar con 100.)
        echo   [INFO] Esperando a que Tailscale se conecte completamente...
        timeout /t 10 /nobreak > nul
        
        REM Reintentar
        set TAILSCALE_IP=
        for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
        if not "!TAILSCALE_IP!"=="" (
            echo   [OK] IP de Tailscale: !TAILSCALE_IP!
        ) else (
            echo   [ERROR] Tailscale no tiene IP asignada
            echo   [INFO] Verifica que Tailscale este conectado correctamente
        )
    )
) else (
    echo   [ERROR] Tailscale no tiene IP asignada
    echo   [INFO] Verifica que Tailscale este conectado correctamente
    echo   [INFO] Ejecuta: tailscale up
    pause
    exit /b 1
)

echo.

REM ========================================
REM PASO 2: Verificar e Iniciar Puente Genérico
REM ========================================
echo [2/3] Verificando puente generico del NUC...
echo.

REM Verificar si el puente está corriendo
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Puente generico esta corriendo (puerto 5000)
    
    REM Verificar que responda
    echo   [INFO] Verificando que el puente responda...
    curl -s http://localhost:5000/api/status > nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] El puente responde correctamente
    ) else (
        echo   [ADVERTENCIA] El puente no responde, puede estar bloqueado
        echo   [INFO] Intentando reiniciar el puente...
        
        REM Matar procesos de Python en el puerto 5000
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
            taskkill /F /PID %%a > nul 2>&1
        )
        timeout /t 2 /nobreak > nul
    )
) else (
    echo   [INFO] Puente generico NO esta corriendo, iniciando...
)

REM Si el puente no está corriendo o no responde, iniciarlo
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% NEQ 0 (
    echo   [INFO] Iniciando puente generico...
    
    REM Cambiar al directorio del backend
    cd /d "%~dp0backend"
    
    REM Verificar que Python esté instalado
    python --version > nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo   [ERROR] Python no esta instalado o no esta en el PATH
        echo   [INFO] Instala Python 3.11 o superior
        pause
        exit /b 1
    )
    
    REM Verificar que el archivo del puente exista
    if not exist "puente_generico_nuc.py" (
        echo   [ERROR] No se encontro puente_generico_nuc.py
        echo   [INFO] Verifica que el archivo exista en el directorio backend
        pause
        exit /b 1
    )
    
    REM Iniciar el puente en segundo plano
    echo   [INFO] Iniciando puente generico en segundo plano...
    start /B "" python puente_generico_nuc.py
    
    REM Esperar a que el puente se inicie
    echo   [INFO] Esperando a que el puente se inicie (5 segundos)...
    timeout /t 5 /nobreak > nul
    
    REM Verificar que el puente esté corriendo
    netstat -ano | findstr :5000 > nul
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Puente generico iniciado correctamente
    ) else (
        echo   [ERROR] No se pudo iniciar el puente generico
        echo   [INFO] Verifica que no haya errores en el codigo
        pause
        exit /b 1
    )
    
    REM Esperar un poco más para que el puente esté listo
    timeout /t 3 /nobreak > nul
)

REM Verificar que el puente responda
echo   [INFO] Verificando que el puente responda...
curl -s http://localhost:5000/api/status > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] El puente responde correctamente
) else (
    echo   [ERROR] El puente no responde
    echo   [INFO] Revisa los logs del puente para ver errores
    pause
    exit /b 1
)

echo.

REM ========================================
REM PASO 3: Verificación Final
REM ========================================
echo [3/3] Verificacion final...
echo.

REM Verificar Tailscale nuevamente
echo   [INFO] Verificando Tailscale...
set TAILSCALE_IP=
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
if not "!TAILSCALE_IP!"=="" (
    echo   [OK] Tailscale IP: !TAILSCALE_IP!
) else (
    echo   [ERROR] Tailscale no tiene IP
)

REM Verificar puente genérico
echo   [INFO] Verificando puente generico...
curl -s http://localhost:5000/api/status > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Puente generico responde en http://localhost:5000
) else (
    echo   [ERROR] Puente generico no responde
)

REM Verificar acceso desde Tailscale IP
if not "!TAILSCALE_IP!"=="" (
    echo   [INFO] Verificando acceso desde IP de Tailscale...
    curl -s http://!TAILSCALE_IP!:5000/api/status > nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo   [OK] Puente accesible desde Tailscale IP: http://!TAILSCALE_IP!:5000
    ) else (
        echo   [ADVERTENCIA] Puente no accesible desde Tailscale IP
        echo   [INFO] Verificando regla de firewall...
        
        REM Verificar si existe regla de firewall
        netsh advfirewall firewall show rule name="Puente Generico NUC" > nul 2>&1
        if !ERRORLEVEL! NEQ 0 (
            echo   [INFO] Regla de firewall no encontrada
            echo   [INFO] Intentando crear regla de firewall...
            
            REM Intentar crear regla de firewall (puede requerir admin)
            netsh advfirewall firewall add rule name="Puente Generico NUC" dir=in action=allow protocol=TCP localport=5000 > nul 2>&1
            if !ERRORLEVEL! EQU 0 (
                echo   [OK] Regla de firewall creada
            ) else (
                echo   [ADVERTENCIA] No se pudo crear regla de firewall (puede requerir admin)
                echo   [INFO] Ejecuta como administrador: abrir_firewall_como_admin.bat
            )
        ) else (
            echo   [OK] Regla de firewall existe
        )
    )
)

echo.
echo ========================================
echo RESUMEN
echo ========================================
echo.
if not "!TAILSCALE_IP!"=="" (
    echo   [OK] Tailscale: !TAILSCALE_IP!
) else (
    echo   [ERROR] Tailscale: No conectado
)

netstat -ano | findstr :5000 > nul
if !ERRORLEVEL! EQU 0 (
    echo   [OK] Puente generico: Corriendo en puerto 5000
) else (
    echo   [ERROR] Puente generico: No esta corriendo
)

echo.
echo ========================================
echo CONFIGURACION PARA RAILWAY
echo ========================================
echo.
if not "!TAILSCALE_IP!"=="" (
    echo   En Railway Dashboard, configura:
    echo   NUC_URLS=nuc_sede1:http://!TAILSCALE_IP!:5000
    echo   CAMARAS_IPS=192.168.60.65
    echo.
) else (
    echo   [ERROR] No se puede obtener IP de Tailscale
    echo   [INFO] Configura Railway manualmente cuando Tailscale este conectado
    echo.
)

echo ========================================
echo Verificacion completada
echo ========================================
echo.
echo El sistema deberia estar funcionando ahora.
echo Si hay problemas, revisa los logs arriba.
echo.
pause
