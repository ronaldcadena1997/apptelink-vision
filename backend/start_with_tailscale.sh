#!/bin/bash
# Script para iniciar Tailscale y luego el servidor Python

set -e

echo "=========================================="
echo "Iniciando Tailscale en Railway"
echo "=========================================="

# Verificar que TAILSCALE_AUTHKEY esté configurada
if [ -z "$TAILSCALE_AUTHKEY" ]; then
    echo "ERROR: TAILSCALE_AUTHKEY no está configurada"
    echo "Configura esta variable de entorno en Railway Dashboard"
    echo "Continuando sin Tailscale (modo fallback)..."
    exec python server.py
    exit 0
fi

echo "[1/3] Iniciando Tailscale daemon..."
# Crear directorios necesarios
mkdir -p /var/lib/tailscale
mkdir -p /var/run/tailscale

# Iniciar tailscaled en segundo plano con userspace-networking
# Esto no requiere privilegios especiales ni acceso a /dev/net/tun
tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/var/run/tailscale/tailscaled.sock --tun=userspace-networking &
TAILSCALED_PID=$!

# Esperar a que tailscaled se inicie
echo "Esperando a que tailscaled se inicie..."
sleep 5

echo "[2/3] Conectando a Tailscale con authkey..."
tailscale up --authkey=$TAILSCALE_AUTHKEY --accept-routes --accept-dns=false

# Esperar a que Tailscale se conecte
echo "Esperando conexión de Tailscale..."
sleep 5

echo "[3/3] Verificando conexión de Tailscale..."
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "")
if [ -z "$TAILSCALE_IP" ]; then
    echo "⚠️  ADVERTENCIA: Tailscale no tiene IP aún"
    echo "Continuando... Railway intentará conectarse de todas formas"
else
    echo "✅ Tailscale conectado. IP: $TAILSCALE_IP"
fi

echo ""
echo "=========================================="
echo "Iniciando servidor Python"
echo "=========================================="
echo ""

# Función para limpiar al salir
cleanup() {
    echo "Cerrando Tailscale..."
    tailscale down 2>/dev/null || true
    kill $TAILSCALED_PID 2>/dev/null || true
}
trap cleanup EXIT

# Iniciar el servidor Python
exec python server.py
