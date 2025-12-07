#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para verificar puertos COM disponibles
"""

try:
    import serial.tools.list_ports
    
    print("=" * 60)
    print("🔍 Buscando puertos COM disponibles...")
    print("=" * 60)
    
    ports = serial.tools.list_ports.comports()
    
    if ports:
        print(f"\n✅ Se encontraron {len(ports)} puerto(s) COM:\n")
        for i, port in enumerate(ports, 1):
            print(f"{i}. {port.device}")
            print(f"   Descripción: {port.description}")
            print(f"   Hardware ID: {port.hwid}")
            print()
    else:
        print("\n❌ No se encontraron puertos COM")
        print("\nVerifica que:")
        print("  - El SIM7600 esté conectado")
        print("  - Los drivers estén instalados")
        print("  - El cable USB esté bien conectado")
    
    print("=" * 60)
    
except ImportError:
    print("❌ Error: pyserial no está instalado")
    print("\nInstala con:")
    print("   pip install pyserial")
except Exception as e:
    print(f"❌ Error: {e}")
