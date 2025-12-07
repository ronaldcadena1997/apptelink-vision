@echo off
REM Verificar si se está ejecutando como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    REM No es administrador, elevar permisos automáticamente
    echo Elevando permisos de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ========================================
echo Configurar Inicio Automatico del Puente
echo ========================================
echo.
echo [INFO] Ejecutando como Administrador
echo Este script configurara el puente generico para
echo ejecutarse automaticamente al iniciar Windows.
echo.
timeout /t 2 /nobreak > nul

REM Obtener la ruta completa del script
REM Usar la versión silenciosa para ejecución en segundo plano
set SCRIPT_PATH=%~dp0ejecutar_puente_silencioso.bat
set SCRIPT_NAME=PuenteGenericoNUC

echo [1/2] Creando tarea programada...
echo.

REM Crear tarea programada que se ejecuta al inicio con privilegios elevados
schtasks /Create /TN "%SCRIPT_NAME%" /TR "\"%SCRIPT_PATH%\"" /SC ONLOGON /RL HIGHEST /F /RU "SYSTEM"

if %ERRORLEVEL% EQU 0 (
    echo [OK] Tarea programada creada exitosamente
    echo.
    echo La tarea se ejecutara automaticamente cuando inicies sesion.
    echo.
) else (
    echo [ERROR] No se pudo crear la tarea programada
    echo.
    echo Intentando metodo alternativo (carpeta de inicio)...
    echo.
    
    REM Metodo alternativo: copiar a carpeta de inicio
    set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    copy "%SCRIPT_PATH%" "%STARTUP_FOLDER%\" > nul 2>&1
    
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Script copiado a carpeta de inicio
        echo El puente se ejecutara al iniciar sesion.
    ) else (
        echo [ERROR] No se pudo configurar inicio automatico
        echo Por favor, ejecuta este script como Administrador
    )
)

echo.
echo [2/2] Verificando configuracion...
schtasks /Query /TN "%SCRIPT_NAME%" > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Tarea configurada correctamente
    echo.
    echo Para verificar: Abre "Tareas programadas" y busca "%SCRIPT_NAME%"
    echo Para eliminar: Ejecuta "eliminar_inicio_automatico.bat"
) else (
    echo [INFO] Usando metodo de carpeta de inicio
)

echo.
echo ========================================
echo Configuracion completada
echo ========================================
echo.
echo La tarea se ejecutara automaticamente al iniciar Windows.
echo El script se cerrara en 5 segundos...
timeout /t 5 /nobreak > nul
exit
