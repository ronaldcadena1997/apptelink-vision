@echo off
REM ========================================
REM EJECUTAR API EN SEGUNDO PLANO
REM ========================================
REM Este script mantiene el API corriendo
REM Se reinicia automaticamente si se cae
REM ========================================

cd /d "%~dp0backend"

REM Bucle infinito para mantener el API corriendo
:loop
    REM Verificar si el puerto 5000 está en uso (API corriendo)
    netstat -ano | findstr ":5000" | findstr "LISTENING" > nul
    if %ERRORLEVEL% NEQ 0 (
        REM El puerto no está en uso, iniciar el API
        echo [%date% %time%] Iniciando API del NUC...
        start /B /MIN python puente_generico_nuc.py
        timeout /t 10 /nobreak > nul
        
        REM Verificar que se inició correctamente
        netstat -ano | findstr ":5000" | findstr "LISTENING" > nul
        if %ERRORLEVEL% EQU 0 (
            echo [%date% %time%] API iniciado correctamente
        ) else (
            echo [%date% %time%] ERROR: API no se pudo iniciar
        )
    )
    
    REM Esperar 60 segundos antes de verificar de nuevo
    timeout /t 60 /nobreak > nul
goto loop
