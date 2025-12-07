#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para detectar SIM7600 sin pausas
Guarda resultados en archivo
"""

import sys
import os
import time

# Redirigir salida a archivo también
class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    def flush(self):
        for f in self.files:
            f.flush()

log_file = open('resultado_deteccion.txt', 'w', encoding='utf-8')
sys.stdout = Tee(sys.stdout, log_file)
sys.stderr = Tee(sys.stderr, log_file)

print("=" * 70)
print("📡 DETECTOR SIM7600")
print("=" * 70)
print()

# Verificar/instalar pyserial
try:
    import serial
    import serial.tools.list_ports
    print("✅ pyserial disponible")
except ImportError:
    print("📦 Instalando pyserial...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import serial
        import serial.tools.list_ports
        print("✅ pyserial instalado")
    except:
        print("❌ Error al instalar pyserial")
        log_file.close()
        sys.exit(1)

# Listar puertos
print("\n🔍 Buscando puertos COM...")
ports = list(serial.tools.list_ports.comports())

if not ports:
    print("❌ No se encontraron puertos COM")
    print("\n💡 Verifica que el SIM7600 esté conectado")
    log_file.close()
    sys.exit(1)

print(f"\n✅ Se encontraron {len(ports)} puerto(s) COM:\n")
for i, port in enumerate(ports, 1):
    print(f"{i}. {port.device} - {port.description}")

# Probar puertos
print("\n🔍 Probando puertos...")
puerto_encontrado = None
baudrate_encontrado = None
baudrates = [115200, 9600, 230400]

for port in ports:
    port_name = port.device
    print(f"\nProbando {port_name}...")
    
    for baudrate in baudrates:
        try:
            ser = serial.Serial(port_name, baudrate, timeout=2)
            time.sleep(1.5)
            ser.reset_input_buffer()
            ser.write(b'AT\r\n')
            time.sleep(0.5)
            respuesta = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            ser.close()
            
            if 'OK' in respuesta.upper():
                print(f"✅ {port_name} responde! (Baud: {baudrate})")
                puerto_encontrado = port_name
                baudrate_encontrado = baudrate
                break
        except:
            continue
    if puerto_encontrado:
        break

print("\n" + "=" * 70)
if puerto_encontrado:
    print(f"✅ SIM7600 encontrado en: {puerto_encontrado}")
    print(f"   Baud Rate: {baudrate_encontrado}")
    print(f"\n📝 Configura en configurar_sim7600.py:")
    print(f"   PORT = '{puerto_encontrado}'")
    print(f"   BAUDRATE = {baudrate_encontrado}")
else:
    print("❌ No se encontró SIM7600")
    print("💡 Verifica conexión y drivers")

print("=" * 70)
log_file.close()
