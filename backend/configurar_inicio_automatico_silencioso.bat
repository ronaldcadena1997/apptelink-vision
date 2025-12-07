@echo off
REM Script completamente silencioso - Sin pausas ni confirmaciones
REM Se ejecuta automáticamente como administrador

REM Verificar si se está ejecutando como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    REM No es administrador, elevar permisos automáticamente
    powershell -Command "Start-Process '%~f0' -Verb RunAs -WindowStyle Hidden"
    exit /b
)

REM Obtener la ruta completa del script
set SCRIPT_PATH=%~dp0ejecutar_puente_silencioso.bat
set SCRIPT_NAME=PuenteGenericoNUC

REM Crear tarea programada que se ejecuta al inicio con privilegios elevados
schtasks /Create /TN "%SCRIPT_NAME%" /TR "\"%SCRIPT_PATH%\"" /SC ONLOGON /RL HIGHEST /F /RU "SYSTEM" > nul 2>&1

if %ERRORLEVEL% EQU 0 (
    REM Tarea creada exitosamente
    exit 0
) else (
    REM Intentar método alternativo (carpeta de inicio)
    set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    copy "%SCRIPT_PATH%" "%STARTUP_FOLDER%\" > nul 2>&1
    exit %ERRORLEVEL%
)
