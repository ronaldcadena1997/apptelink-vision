@echo off
cd /d "%~dp0"

echo ========================================
echo CONFIGURAR IP ESTATICA PARA CAMARA
echo ========================================
echo.
echo Este script configurara el adaptador Ethernet
echo para estar en la misma red que la camara (192.168.60.x)
echo.
echo IMPORTANTE: Asegurate de que el cable Ethernet
echo este conectado al mismo switch/router que la camara.
echo.
pause

echo.
echo [1] Listando adaptadores de red...
powershell -Command "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Format-Table Name, InterfaceAlias, Status"
echo.

echo [2] Configurando IP estatica en Ethernet 2...
echo    IP: 192.168.60.100
echo    Gateway: 192.168.60.1
echo    Subnet: 255.255.255.0
echo.

powershell -Command "$ErrorActionPreference = 'Stop'; try { New-NetIPAddress -InterfaceAlias 'Ethernet 2' -IPAddress 192.168.60.100 -PrefixLength 24 -DefaultGateway 192.168.60.1 -ErrorAction Stop; Set-DnsClientServerAddress -InterfaceAlias 'Ethernet 2' -ServerAddresses 192.168.60.1,8.8.8.8; Write-Host '[OK] IP configurada correctamente' -ForegroundColor Green } catch { Write-Host '[ERROR] No se pudo configurar. Verifica que el adaptador Ethernet 2 existe y esta conectado.' -ForegroundColor Red; Write-Host $_.Exception.Message }"

echo.
echo [3] Verificando nueva configuracion...
ipconfig | findstr /C:"IPv4" /C:"Subnet" /C:"Gateway"
echo.

echo [4] Probando conectividad a la camara...
ping -n 2 192.168.60.65
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] La camara es accesible!
    echo    Ahora puedes reiniciar el NUC Agent.
) else (
    echo.
    echo [ERROR] Aun no se puede acceder a la camara.
    echo    - Verifica que el cable Ethernet este conectado
    echo    - Verifica que este conectado al mismo switch que la camara
    echo    - Verifica que la IP 192.168.60.100 no este en uso
)
echo.

pause
