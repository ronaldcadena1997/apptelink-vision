@echo off
cd /d "%~dp0"

echo ========================================
echo DIAGNOSTICO DE RED - CAMARA
echo ========================================
echo.

echo [1] Verificando ping a la camara (192.168.60.65)...
ping -n 4 192.168.60.65
if %ERRORLEVEL% EQU 0 (
    echo [OK] La camara responde al ping
) else (
    echo [ERROR] La camara NO responde al ping
    echo    - Verifica que la IP sea correcta
    echo    - Verifica que la camara este encendida
    echo    - Verifica que el NUC este en la misma red (192.168.60.x)
)
echo.

echo [2] Verificando configuracion de red del NUC...
ipconfig | findstr /C:"IPv4" /C:"Subnet" /C:"Gateway"
echo.

echo [3] Verificando puerto 80 (HTTP)...
powershell -Command "Test-NetConnection -ComputerName 192.168.60.65 -Port 80 -InformationLevel Quiet" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] El puerto 80 esta abierto
) else (
    echo [ERROR] El puerto 80 esta cerrado o bloqueado
    echo    - Puede ser firewall
    echo    - O el servicio HTTP de la camara esta deshabilitado
)
echo.

echo [4] Verificando puerto 8000 (HTTP alternativo)...
powershell -Command "Test-NetConnection -ComputerName 192.168.60.65 -Port 8000 -InformationLevel Quiet" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] El puerto 8000 esta abierto
) else (
    echo [ADVERTENCIA] El puerto 8000 esta cerrado
)
echo.

echo [5] Verificando puerto 554 (RTSP)...
powershell -Command "Test-NetConnection -ComputerName 192.168.60.65 -Port 554 -InformationLevel Quiet" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] El puerto 554 (RTSP) esta abierto
) else (
    echo [ADVERTENCIA] El puerto 554 (RTSP) esta cerrado
)
echo.

echo ========================================
echo RESUMEN
echo ========================================
echo.
echo Si el ping funciona pero los puertos estan cerrados:
echo    - Verifica firewall de Windows
echo    - Verifica que los servicios de la camara esten habilitados
echo.
echo Si el ping NO funciona:
echo    - El NUC y la camara estan en redes diferentes
echo    - Configura el NUC en la misma red (192.168.60.x)
echo.
echo Si SADP funciona en otro equipo:
echo    - Prueba desde ese equipo primero
echo    - Luego configura el NUC en la misma red
echo.

pause
