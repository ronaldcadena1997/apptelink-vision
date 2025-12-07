@echo off
REM Script para ejecutar el puente genérico al inicio del sistema
REM Verifica Tailscale y el puente, se reinicia automáticamente si falla

cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend"

:inicio
REM ========================================
REM Verificar Tailscale
REM ========================================
:verificar_tailscale
tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
if %ERRORLEVEL% NEQ 0 (
    REM Intentar iniciar Tailscale
    if exist "C:\Program Files\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files\Tailscale\tailscaled.exe"
    ) else if exist "C:\Program Files (x86)\Tailscale\tailscaled.exe" (
        start "" "C:\Program Files (x86)\Tailscale\tailscaled.exe"
    )
    timeout /t 15 /nobreak > nul
    goto verificar_tailscale
)

REM Verificar que Tailscale tenga IP
tailscale ip -4 > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    timeout /t 10 /nobreak > nul
    goto verificar_tailscale
)

REM ========================================
REM Verificar si el puente ya está corriendo
REM ========================================
netstat -ano | findstr :5000 > nul
if %ERRORLEVEL% EQU 0 (
    REM Ya está corriendo, verificar periódicamente (cada 60 segundos)
    :verificar_ambos
    timeout /t 60 /nobreak > nul
    
    REM Verificar Tailscale
    tasklist /FI "IMAGENAME eq tailscaled.exe" 2>nul | find /I "tailscaled.exe" > nul
    if %ERRORLEVEL% NEQ 0 goto verificar_tailscale
    
    tailscale ip -4 > nul 2>&1
    if %ERRORLEVEL% NEQ 0 goto verificar_tailscale
    
    REM Verificar puente
    netstat -ano | findstr :5000 > nul
    if %ERRORLEVEL% NEQ 0 goto inicio
    
    REM Verificar que el puente responda
    curl -s -o nul -w "%%{http_code}" http://localhost:5000/api/status 2>nul | findstr /R "^200" > nul
    if %ERRORLEVEL% NEQ 0 (
        REM No responde, reiniciar
        taskkill /F /IM pythonw.exe /FI "COMMANDLINE eq *puente_generico_nuc.py*" > nul 2>&1
        taskkill /F /IM python.exe /FI "COMMANDLINE eq *puente_generico_nuc.py*" > nul 2>&1
        timeout /t 5 /nobreak > nul
        goto inicio
    )
    
    goto verificar_ambos
)

REM ========================================
REM Iniciar el puente
REM ========================================
pythonw puente_generico_nuc.py 2>nul
if %ERRORLEVEL% NEQ 0 (
    python puente_generico_nuc.py
)

REM Si se cierra, reiniciar
timeout /t 5 /nobreak > nul
goto inicio
