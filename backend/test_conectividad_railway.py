#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar conectividad desde Railway al NUC
Se puede ejecutar manualmente o agregar como endpoint de prueba
"""

import requests
import os

# IP del NUC en Tailscale
NUC_IP = "100.92.50.72"
NUC_PORT = 5000
NUC_URL = f"http://{NUC_IP}:{NUC_PORT}"

def test_conectividad():
    """Prueba la conectividad desde Railway al NUC"""
    print("=" * 60)
    print("PRUEBA DE CONECTIVIDAD RAILWAY -> NUC")
    print("=" * 60)
    print()
    
    # Test 1: Status endpoint
    print(f"[1/3] Probando: {NUC_URL}/api/status")
    try:
        response = requests.get(f"{NUC_URL}/api/status", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ OK - Status: {response.status_code}")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"   ❌ Error - Status: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except requests.exceptions.Timeout:
        print(f"   ❌ TIMEOUT - No se pudo conectar en 10 segundos")
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ CONNECTION ERROR - {e}")
    except Exception as e:
        print(f"   ❌ ERROR - {e}")
    print()
    
    # Test 2: Snapshot endpoint (sin IP específica, solo probar conectividad)
    print(f"[2/3] Probando conectividad general a {NUC_URL}")
    try:
        # Intentar cualquier endpoint para ver si hay conectividad
        response = requests.get(f"{NUC_URL}/api/status", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Conectividad OK")
        else:
            print(f"   ⚠️  Conectividad parcial - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Sin conectividad - {e}")
    print()
    
    # Test 3: Verificar IP de Tailscale de Railway
    print(f"[3/3] Información de Tailscale")
    try:
        import subprocess
        result = subprocess.run(['tailscale', 'ip', '-4'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            railway_ip = result.stdout.strip()
            print(f"   Railway Tailscale IP: {railway_ip}")
        else:
            print(f"   ⚠️  No se pudo obtener IP de Tailscale de Railway")
    except Exception as e:
        print(f"   ⚠️  No se pudo verificar IP de Tailscale: {e}")
    print()
    
    print("=" * 60)
    print("FIN DE PRUEBA")
    print("=" * 60)

if __name__ == "__main__":
    test_conectividad()
