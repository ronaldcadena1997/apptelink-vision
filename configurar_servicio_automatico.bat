@echo off
REM ========================================
REM CONFIGURAR SERVICIO AUTOMATICO
REM ========================================
REM Este script configura el API del NUC para ejecutarse
REM automaticamente al inicio y mantenerse corriendo
REM ========================================

setlocal enabledelayedexpansion

echo ========================================
echo CONFIGURAR SERVICIO AUTOMATICO
echo ========================================
echo.

REM Verificar permisos de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Se requieren permisos de administrador
    echo [INFO] Elevando permisos...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

REM Ruta del script que se ejecutará
set SCRIPT_PATH=%~dp0ejecutar_api_background.bat
set TASK_NAME=PuenteGenericoNUC_Auto

echo [1/3] Creando script de ejecucion en segundo plano...
echo.

REM Crear script que se ejecuta en segundo plano
(
echo @echo off
echo REM Script que ejecuta el API en segundo plano
echo cd /d "%~dp0backend"
echo 
echo REM Bucle infinito para mantener el API corriendo
echo :loop
echo     REM Verificar si Python esta corriendo
echo     tasklist /FI "IMAGENAME eq python.exe" 2^>nul ^| find /I "python.exe" ^> nul
echo     if %%ERRORLEVEL%% NEQ 0 (
echo         echo [%date% %time%] Iniciando API del NUC...
echo         start /B /MIN python puente_generico_nuc.py
echo         timeout /t 5 /nobreak ^> nul
echo     )
echo     
echo     REM Esperar 30 segundos antes de verificar de nuevo
echo     timeout /t 30 /nobreak ^> nul
echo goto loop
) > "%SCRIPT_PATH%"

echo [OK] Script creado: ejecutar_api_background.bat
echo.

echo [2/3] Creando tarea programada...
echo.

REM Eliminar tarea existente si existe
schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1

REM Crear nueva tarea programada
schtasks /Create /TN "%TASK_NAME%" /TR "\"%SCRIPT_PATH%\"" /SC ONLOGON /RL HIGHEST /F /RU "SYSTEM" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] Tarea programada creada exitosamente
    echo.
    echo [3/3] Configurando la tarea para ejecutarse en segundo plano...
    echo.
    
    REM Configurar la tarea para que no muestre ventana
    schtasks /Change /TN "%TASK_NAME%" /RU "SYSTEM" /RP "" >nul 2>&1
    
    echo [OK] Configuracion completada
    echo.
    echo ========================================
    echo CONFIGURACION EXITOSA
    echo ========================================
    echo.
    echo La tarea "%TASK_NAME%" se ejecutara automaticamente:
    echo   - Al iniciar Windows
    echo   - En segundo plano (sin ventana)
    echo   - Se reiniciara automaticamente si se cae
    echo.
    echo Para verificar la tarea:
    echo   1. Presiona Windows + R
    echo   2. Escribe: taskschd.msc
    echo   3. Busca: %TASK_NAME%
    echo.
    echo Para iniciar manualmente ahora:
    echo   .\ejecutar_api_background.bat
    echo.
) else (
    echo [ERROR] No se pudo crear la tarea programada
    echo [INFO] Intentando metodo alternativo...
    echo.
    
    REM Método alternativo: carpeta de inicio
    set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    copy "%SCRIPT_PATH%" "%STARTUP_FOLDER%\" >nul 2>&1
    
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Script copiado a carpeta de inicio
        echo [INFO] Se ejecutara al iniciar sesion
    ) else (
        echo [ERROR] No se pudo configurar inicio automatico
    )
)

echo.
pause
