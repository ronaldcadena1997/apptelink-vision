@echo off
REM Versión silenciosa - Sin ventanas, solo en segundo plano
REM Verifica Tailscale y el puente genérico

cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend"

:inicio
REM ========================================
REM PASO 1: Verificar que Tailscale esté corriendo
REM ========================================
:verificar_tailscale
REM Verificar si el proceso de Tailscale está corriendo
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% NEQ 0 (
    REM Tailscale no está corriendo, intentar iniciarlo
    REM Buscar Tailscale en ubicaciones comunes
    if exist "C:\Program Files\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files\Tailscale\tailscaled.exe"
        timeout /t 5 /nobreak > nul
    ) else if exist "C:\Program Files (x86)\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files (x86)\Tailscale\tailscaled.exe"
        timeout /t 5 /nobreak > nul
    )
    
    REM Esperar a que Tailscale se inicie
    timeout /t 10 /nobreak > nul
    goto verificar_tailscale
)

REM Verificar que Tailscale tenga una IP asignada
tailscale ip -4 > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    REM Tailscale no tiene IP, esperar y reintentar
    timeout /t 10 /nobreak > nul
    goto verificar_tailscale
)

REM Verificar que la IP sea válida (debe empezar con 100.)
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
echo %TAILSCALE_IP% | findstr /R "^100\." > nul
if %ERRORLEVEL% NEQ 0 (
    REM IP no válida, esperar y reintentar
    timeout /t 10 /nobreak > nul
    goto verificar_tailscale
)

REM ========================================
REM PASO 2: Verificar si el puente ya está corriendo
REM ========================================
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    REM El puente ya está corriendo, solo verificar periódicamente
    :verificar_ambos
    timeout /t 300 /nobreak > nul
    
    REM Verificar Tailscale
    tailscale ip -4 > nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        REM Tailscale se desconectó, esperar a que se reconecte
        goto verificar_tailscale
    )
    
    REM Verificar puente
    netstat -ano | findstr :5000 > nul
    if %ERRORLEVEL% NEQ 0 (
        REM El puente se cerró, reiniciar
        goto inicio
    )
    
    goto verificar_ambos
)

REM ========================================
REM PASO 3: Iniciar el puente genérico
REM ========================================
REM Ejecutar en segundo plano sin ventana
start /B pythonw puente_generico_nuc.py 2>nul

REM Si falla, intentar con python normal en ventana minimizada
if %ERRORLEVEL% NEQ 0 (
    start /MIN python puente_generico_nuc.py
)

REM Esperar y verificar que se inició correctamente
timeout /t 10 /nobreak > nul
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% NEQ 0 (
    REM No está corriendo, reiniciar
    timeout /t 5 /nobreak > nul
    goto inicio
)

REM ========================================
REM PASO 4: Verificación periódica continua
REM ========================================
REM Está corriendo, verificar constantemente que ambos sigan activos
REM Verifica cada 60 segundos (1 minuto) para detectar problemas rápidamente
:verificar_periodico
timeout /t 60 /nobreak > nul

REM ========================================
REM Verificar Tailscale (cada minuto)
REM ========================================
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% NEQ 0 (
    REM Tailscale se cerró, intentar reiniciarlo
    if exist "C:\Program Files\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files\Tailscale\tailscaled.exe"
    ) else if exist "C:\Program Files (x86)\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files (x86)\Tailscale\tailscaled.exe"
    )
    timeout /t 15 /nobreak > nul
    goto verificar_tailscale
)

REM Verificar que Tailscale tenga IP válida
tailscale ip -4 > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    REM Tailscale no tiene IP, esperar a que se reconecte
    timeout /t 30 /nobreak > nul
    goto verificar_tailscale
)

REM Verificar que la IP sea válida (debe empezar con 100.)
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
echo %TAILSCALE_IP% | findstr /R "^100\." > nul
if %ERRORLEVEL% NEQ 0 (
    REM IP no válida, esperar a que se reconecte
    timeout /t 30 /nobreak > nul
    goto verificar_tailscale
)

REM ========================================
REM Verificar puente genérico (cada minuto)
REM ========================================
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% NEQ 0 (
    REM El puente se cerró, reiniciarlo
    timeout /t 5 /nobreak > nul
    goto inicio
)

REM Verificar que el puente responda (prueba de conectividad)
REM Intentar conectar al endpoint de status
curl -s -o nul -w "%%{http_code}" http://localhost:5000/api/status 2>nul | findstr /R "^200" > nul
if %ERRORLEVEL% NEQ 0 (
    REM El puente no responde correctamente, reiniciarlo
    REM Matar procesos de Python relacionados con el puente
    taskkill /F /FI "WINDOWTITLE eq *puente*" > nul 2>&1
    taskkill /F /IM pythonw.exe /FI "COMMANDLINE eq *puente_generico_nuc.py*" > nul 2>&1
    taskkill /F /IM python.exe /FI "COMMANDLINE eq *puente_generico_nuc.py*" > nul 2>&1
    timeout /t 5 /nobreak > nul
    goto inicio
)

REM ========================================
REM Ambos están funcionando correctamente
REM ========================================
REM Continuar verificando cada minuto
goto verificar_periodico
