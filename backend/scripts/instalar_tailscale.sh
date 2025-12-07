#!/bin/bash
# Script para instalar Tailscale en el NUC

echo "============================================"
echo "  INSTALACIÓN DE TAILSCALE EN NUC"
echo "============================================"
echo ""

# Verificar si ya está instalado
if command -v tailscale &> /dev/null; then
    echo "✅ Tailscale ya está instalado"
    tailscale version
    echo ""
    echo "Para iniciar: sudo tailscale up"
    echo "Para ver tu IP: tailscale ip -4"
    exit 0
fi

# Detectar sistema operativo
if [ -f /etc/debian_version ]; then
    echo "📦 Detectado: Debian/Ubuntu"
    curl -fsSL https://tailscale.com/install.sh | sh
elif [ -f /etc/redhat-release ]; then
    echo "📦 Detectado: RedHat/CentOS"
    curl -fsSL https://tailscale.com/install.sh | sh
else
    echo "⚠️  Sistema no detectado. Instalación manual requerida."
    echo "Visita: https://tailscale.com/download"
    exit 1
fi

echo ""
echo "============================================"
echo "  CONFIGURACIÓN"
echo "============================================"
echo ""
echo "1. Ejecuta: sudo tailscale up"
echo "2. Abre el enlace que te muestra en el navegador"
echo "3. Inicia sesión o crea una cuenta"
echo "4. Autoriza el dispositivo"
echo ""
echo "Para obtener tu IP de Tailscale:"
echo "  tailscale ip -4"
echo ""
echo "Para ver el hostname:"
echo "  tailscale status"
echo ""

