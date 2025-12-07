# Script PowerShell para abrir el puerto 5000 en el firewall
# DEBE ejecutarse como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ABRIR PUERTO 5000 EN FIREWALL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si se ejecuta como Administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Este script requiere permisos de Administrador" -ForegroundColor Red
    Write-Host "[INFO] Cierra este script y ejecuta PowerShell como Administrador:" -ForegroundColor Yellow
    Write-Host "  1. Busca 'PowerShell' en el menú Inicio" -ForegroundColor Yellow
    Write-Host "  2. Click derecho -> 'Ejecutar como administrador'" -ForegroundColor Yellow
    Write-Host "  3. Navega a la carpeta y ejecuta: .\abrir_firewall_ps1.ps1" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "[OK] Ejecutando como Administrador" -ForegroundColor Green
Write-Host ""

# Verificar si ya existe la regla
$reglaExistente = Get-NetFirewallRule -DisplayName "Puente Genérico NUC" -ErrorAction SilentlyContinue

if ($reglaExistente) {
    Write-Host "[INFO] La regla de firewall ya existe" -ForegroundColor Yellow
    Write-Host "[INFO] Verificando estado..." -ForegroundColor Yellow
    Get-NetFirewallRule -DisplayName "Puente Genérico NUC" | Select-Object DisplayName, Enabled, Direction | Format-Table
    Write-Host ""
    
    # Habilitar la regla si está deshabilitada
    Enable-NetFirewallRule -DisplayName "Puente Genérico NUC" -ErrorAction SilentlyContinue
    Write-Host "[OK] Regla habilitada" -ForegroundColor Green
} else {
    Write-Host "[INFO] Creando nueva regla de firewall..." -ForegroundColor Yellow
    try {
        New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow -ErrorAction Stop
        Write-Host "[OK] Regla de firewall creada exitosamente" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] No se pudo crear la regla de firewall: $_" -ForegroundColor Red
        Write-Host "[INFO] Verifica que tengas permisos de Administrador" -ForegroundColor Yellow
        pause
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICACION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Reglas de firewall para puerto 5000:" -ForegroundColor Cyan
Get-NetFirewallRule -DisplayName "*5000*" -ErrorAction SilentlyContinue | Select-Object DisplayName, Enabled, Direction, Action | Format-Table

Write-Host ""

# Obtener IP de Tailscale
try {
    $tailscaleIP = tailscale ip -4 2>$null
    if ($tailscaleIP) {
        Write-Host "IP de Tailscale: $tailscaleIP" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Ahora prueba desde Railway o desde otra maquina:" -ForegroundColor Yellow
        Write-Host "  curl http://$tailscaleIP:5000/api/status" -ForegroundColor Yellow
        Write-Host ""
    }
} catch {
    Write-Host "[INFO] No se pudo obtener IP de Tailscale" -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COMPLETADO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
pause
