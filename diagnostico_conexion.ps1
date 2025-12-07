Write-Host "============================================" -ForegroundColor Cyan
Write-Host "DIAGNOSTICO DE CONEXION NUC - RAILWAY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/5] Verificando API local del NUC..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/status" -UseBasicParsing -TimeoutSec 3
    Write-Host "[OK] API local funcionando" -ForegroundColor Green
    Write-Host $response.Content
} catch {
    Write-Host "[ERROR] API local NO responde: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "[2/5] Verificando Tailscale en NUC..." -ForegroundColor Yellow
try {
    $tailscaleStatus = tailscale status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Tailscale esta corriendo" -ForegroundColor Green
        Write-Host $tailscaleStatus
    } else {
        Write-Host "[ERROR] Tailscale NO esta corriendo" -ForegroundColor Red
    }
} catch {
    Write-Host "[ERROR] No se pudo verificar Tailscale: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "[3/5] Obteniendo IP de Tailscale del NUC..." -ForegroundColor Yellow
try {
    $tailscaleIP = tailscale ip -4 2>&1 | Out-String
    $tailscaleIP = $tailscaleIP.Trim()
    if ($tailscaleIP -match '^\d+\.\d+\.\d+\.\d+') {
        Write-Host "[OK] IP de Tailscale: $tailscaleIP" -ForegroundColor Green
        $script:TAILSCALE_IP = $tailscaleIP
    } else {
        Write-Host "[ERROR] No se pudo obtener IP de Tailscale" -ForegroundColor Red
        $script:TAILSCALE_IP = $null
    }
} catch {
    Write-Host "[ERROR] Error al obtener IP: $($_.Exception.Message)" -ForegroundColor Red
    $script:TAILSCALE_IP = $null
}
Write-Host ""

Write-Host "[4/5] Verificando que el API responda desde la IP de Tailscale..." -ForegroundColor Yellow
if ($script:TAILSCALE_IP) {
    try {
        $response = Invoke-WebRequest -Uri "http://$($script:TAILSCALE_IP):5000/api/status" -UseBasicParsing -TimeoutSec 5
        Write-Host "[OK] API accesible desde Tailscale" -ForegroundColor Green
        Write-Host $response.Content
    } catch {
        Write-Host "[ERROR] API NO accesible desde Tailscale: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "[ERROR] No se puede verificar - IP de Tailscale no disponible" -ForegroundColor Red
}
Write-Host ""

Write-Host "[5/5] Verificando procesos Python..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "[OK] Procesos Python encontrados:" -ForegroundColor Green
    $pythonProcesses | Select-Object Id, ProcessName, StartTime | Format-Table
} else {
    Write-Host "[ERROR] No se encontraron procesos Python" -ForegroundColor Red
}
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "DIAGNOSTICO COMPLETADO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
