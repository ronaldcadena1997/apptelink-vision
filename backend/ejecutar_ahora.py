#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar la detección y configuración del SIM7600
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 70)
print("📡 Iniciando Detección y Configuración SIM7600")
print("=" * 70)
print()

# Primero verificar pyserial
try:
    import serial.tools.list_ports
    print("✅ pyserial disponible")
except ImportError:
    print("📦 Instalando pyserial...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import serial.tools.list_ports
        print("✅ pyserial instalado")
    except:
        print("❌ Error al instalar pyserial")
        print("   Instala manualmente con: pip install pyserial")
        sys.exit(1)

# Listar puertos
print("\n🔍 Buscando puertos COM...")
ports = serial.tools.list_ports.comports()

if not ports:
    print("❌ No se encontraron puertos COM")
    print("\n💡 Verifica que:")
    print("   - El SIM7600 esté conectado por USB")
    print("   - Los drivers estén instalados")
    print("   - El cable esté bien conectado")
    sys.exit(1)

print(f"\n✅ Se encontraron {len(ports)} puerto(s) COM:\n")
for i, port in enumerate(ports, 1):
    print(f"{i}. {port.device}")
    print(f"   📝 {port.description}")
    if port.manufacturer:
        print(f"   🏭 {port.manufacturer}")
    print()

# Intentar detectar SIM7600 en cada puerto
print("=" * 70)
print("🔍 Probando puertos para encontrar SIM7600...")
print("=" * 70)

import serial
import time

puerto_encontrado = None
baudrates = [115200, 9600, 230400]

for port in ports:
    port_name = port.device
    print(f"\n🔌 Probando {port_name}...")
    
    for baudrate in baudrates:
        try:
            ser = serial.Serial(
                port=port_name,
                baudrate=baudrate,
                timeout=2,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            
            time.sleep(1.5)
            
            # Limpiar buffer
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            
            # Enviar AT
            ser.write(b'AT\r\n')
            time.sleep(0.5)
            
            respuesta = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            ser.close()
            
            if 'OK' in respuesta:
                print(f"   ✅ {port_name} responde correctamente (Baud: {baudrate})")
                puerto_encontrado = port_name
                break
            else:
                print(f"   ⚠️  {port_name} no respondió (Baud: {baudrate})")
                
        except serial.SerialException as e:
            print(f"   ❌ Error: {e}")
            continue
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    if puerto_encontrado:
        break

print("\n" + "=" * 70)

if puerto_encontrado:
    print(f"✅ SIM7600 encontrado en: {puerto_encontrado}")
    print("\n📝 Para configurar:")
    print(f"   1. Edita configurar_sim7600.py")
    print(f"   2. Cambia: PORT = '{puerto_encontrado}'")
    print(f"   3. Configura tu APN y PIN")
    print(f"   4. Ejecuta: python configurar_sim7600.py")
    print("\n💡 O ejecuta: python detectar_y_configurar_sim7600.py")
    print("   (te guiará paso a paso)")
else:
    print("❌ No se encontró ningún módulo SIM7600 respondiendo")
    print("\n💡 Posibles causas:")
    print("   - El módulo no está encendido")
    print("   - El módulo no está en modo AT")
    print("   - Necesitas instalar drivers específicos")
    print("   - El módulo está en otro puerto COM")

print("=" * 70)
