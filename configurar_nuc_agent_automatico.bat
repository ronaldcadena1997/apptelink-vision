@echo off
REM ========================================
REM CONFIGURAR NUC AGENT AUTOMATICO
REM ========================================
REM Configura el NUC Agent para ejecutarse automáticamente
REM ========================================

setlocal enabledelayedexpansion

echo ========================================
echo CONFIGURAR NUC AGENT AUTOMATICO
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
set SCRIPT_PATH=%~dp0ejecutar_nuc_agent_hikvision.bat
set TASK_NAME=NUC_Agent_Hikvision_Auto

echo [1/3] Verificando script...
echo.

if not exist "%SCRIPT_PATH%" (
    echo [ERROR] No se encontro ejecutar_nuc_agent_hikvision.bat
    pause
    exit /b 1
)

echo [OK] Script encontrado
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
    echo [3/3] Configurando la tarea...
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
    echo   - Se reconectara automaticamente si se cae
    echo.
    echo Para verificar la tarea:
    echo   1. Presiona Windows + R
    echo   2. Escribe: taskschd.msc
    echo   3. Busca: %TASK_NAME%
    echo.
    echo Para iniciar manualmente ahora:
    echo   .\ejecutar_nuc_agent_hikvision.bat
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
