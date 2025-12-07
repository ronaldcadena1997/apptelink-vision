@echo off
REM ========================================
REM VERIFICAR ESTADO DEL API
REM ========================================

echo ========================================
echo ESTADO DEL API DEL NUC
echo ========================================
echo.

echo [1] Verificando si el API esta corriendo...
netstat -ano | findstr ":5000" | findstr "LISTENING" > nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] API esta corriendo en puerto 5000
    netstat -ano | findstr ":5000" | findstr "LISTENING"
) else (
    echo [ERROR] API NO esta corriendo
)
echo.

echo [2] Verificando procesos Python...
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Procesos Python encontrados:
    tasklist /FI "IMAGENAME eq python.exe"
) else (
    echo [ERROR] No hay procesos Python corriendo
)
echo.

echo [3] Verificando respuesta del API...
curl -s http://localhost:5000/api/status > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] API responde correctamente:
    curl http://localhost:5000/api/status
) else (
    echo [ERROR] API NO responde
)
echo.

echo [4] Verificando Tailscale...
tailscale status >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Tailscale esta corriendo
    for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do echo    IP: %%i
) else (
    echo [ERROR] Tailscale NO esta corriendo
)
echo.

echo ========================================
pause
