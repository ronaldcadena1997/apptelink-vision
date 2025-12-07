#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para listar puertos COM disponibles
"""

try:
    import serial.tools.list_ports
    
    print("=" * 70)
    print("🔍 Puertos COM Disponibles")
    print("=" * 70)
    
    ports = serial.tools.list_ports.comports()
    
    if ports:
        print(f"\n✅ Se encontraron {len(ports)} puerto(s) COM:\n")
        for i, port in enumerate(ports, 1):
            print(f"{i}. {port.device}")
            print(f"   📝 Descripción: {port.description}")
            if port.manufacturer:
                print(f"   🏭 Fabricante: {port.manufacturer}")
            print(f"   🔧 Hardware ID: {port.hwid}")
            print()
        
        print("=" * 70)
        print("\n💡 Para configurar el SIM7600:")
        print("   1. Identifica el puerto COM de tu SIM7600")
        print("   2. Ejecuta: python detectar_y_configurar_sim7600.py")
        print("   3. O edita configurar_sim7600.py y cambia PORT = 'COMX'")
        print("=" * 70)
    else:
        print("\n❌ No se encontraron puertos COM")
        print("\nVerifica que:")
        print("  - El SIM7600 esté conectado por USB")
        print("  - Los drivers estén instalados")
        print("  - El cable esté bien conectado")
        print("\n💡 Si acabas de conectar el SIM7600, espera unos segundos")
        print("   y vuelve a ejecutar este script")
        print("=" * 70)
    
except ImportError:
    print("❌ Error: pyserial no está instalado")
    print("\n📦 Instalando pyserial...")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ pyserial instalado correctamente")
        print("\n🔄 Ejecuta este script nuevamente")
    except:
        print("❌ Error al instalar. Instala manualmente con:")
        print("   pip install pyserial")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

input("\nPresiona Enter para salir...")
