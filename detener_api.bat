@echo off
REM ========================================
REM DETENER API DEL NUC
REM ========================================

echo Deteniendo API del NUC...
echo.

REM Buscar y terminar procesos Python que estén ejecutando el puente genérico
for /f "tokens=2" %%i in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo Terminando proceso en puerto 5000 (PID: %%i)
    taskkill /F /PID %%i >nul 2>&1
)

REM También terminar cualquier Python que pueda estar corriendo el script
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" > nul
if %ERRORLEVEL% EQU 0 (
    echo Terminando procesos Python relacionados...
    REM Nota: Esto terminará TODOS los procesos Python
    REM Si tienes otros scripts Python corriendo, no uses esto
    REM taskkill /F /IM python.exe >nul 2>&1
)

echo.
echo [OK] API detenido
echo.
pause
