#!/bin/bash
# Script para instalar ZeroTier en el NUC

echo "============================================"
echo "  INSTALACIÓN DE ZEROTIER EN NUC"
echo "============================================"
echo ""

# Verificar si ya está instalado
if command -v zerotier-cli &> /dev/null; then
    echo "✅ ZeroTier ya está instalado"
    zerotier-cli --version
    echo ""
    echo "Para unirte a una red: sudo zerotier-cli join NETWORK_ID"
    echo "Para ver tu IP: zerotier-cli listnetworks"
    exit 0
fi

# Instalar ZeroTier
echo "📦 Instalando ZeroTier..."
curl -s https://install.zerotier.com | sudo bash

echo ""
echo "============================================"
echo "  CONFIGURACIÓN"
echo "============================================"
echo ""
echo "1. Crea una cuenta en: https://my.zerotier.com"
echo "2. Crea una nueva red"
echo "3. Copia el Network ID"
echo "4. Ejecuta: sudo zerotier-cli join TU_NETWORK_ID"
echo "5. Autoriza el dispositivo en el dashboard"
echo ""
echo "Para ver tu IP asignada:"
echo "  zerotier-cli listnetworks"
echo ""
echo "Para ver el estado:"
echo "  sudo zerotier-cli status"
echo ""

