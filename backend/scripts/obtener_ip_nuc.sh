#!/bin/bash
# Script para obtener todas las IPs del NUC

echo "============================================"
echo "  IPs DEL NUC"
echo "============================================"
echo ""

echo "📍 IP LOCAL (Red 192.168.60.x):"
ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v '127.0.0.1' | head -1
echo ""

echo "🌐 IP PÚBLICA (Internet):"
curl -s ifconfig.me
echo ""
echo ""

# Verificar Tailscale
if command -v tailscale &> /dev/null; then
    echo "🔷 TAILSCALE:"
    tailscale ip -4 2>/dev/null || echo "  No conectado"
    echo ""
fi

# Verificar ZeroTier
if command -v zerotier-cli &> /dev/null; then
    echo "🔶 ZEROTIER:"
    zerotier-cli listnetworks 2>/dev/null | grep -E "zt|10\." | head -1 || echo "  No conectado"
    echo ""
fi

# Verificar WireGuard
if command -v wg &> /dev/null; then
    echo "🔐 WIREGUARD:"
    sudo wg show 2>/dev/null | grep -E "interface|inet" || echo "  No configurado"
    echo ""
fi

echo "============================================"
echo ""
echo "💡 Para usar en el frontend, actualiza:"
echo "   src/config/api.js"
echo ""
echo "   Ejemplo:"
echo "   export const API_BASE_URL = 'http://IP_AQUI:5000';"
echo ""

