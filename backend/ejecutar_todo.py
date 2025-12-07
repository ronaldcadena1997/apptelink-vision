#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script completo para detectar y configurar SIM7600
Ejecuta todo el proceso automáticamente
"""

import sys
import os
import time

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 70)
print("📡 DETECTOR Y CONFIGURADOR SIM7600")
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
        print("✅ pyserial instalado correctamente")
    except Exception as e:
        print(f"❌ Error al instalar pyserial: {e}")
        print("\nInstala manualmente con: pip install pyserial")
        input("\nPresiona Enter para salir...")
        sys.exit(1)

# Listar puertos COM
print("\n" + "=" * 70)
print("🔍 PASO 1: Buscando puertos COM disponibles...")
print("=" * 70)

ports = list(serial.tools.list_ports.comports())

if not ports:
    print("\n❌ No se encontraron puertos COM")
    print("\n💡 Verifica que:")
    print("   - El SIM7600 esté conectado por USB")
    print("   - Los drivers estén instalados")
    print("   - El cable esté bien conectado")
    print("\n💡 Si acabas de conectar el SIM7600, espera unos segundos")
    print("   y vuelve a ejecutar este script")
    input("\nPresiona Enter para salir...")
    sys.exit(1)

print(f"\n✅ Se encontraron {len(ports)} puerto(s) COM:\n")
for i, port in enumerate(ports, 1):
    print(f"{i}. {port.device}")
    print(f"   📝 Descripción: {port.description}")
    if port.manufacturer:
        print(f"   🏭 Fabricante: {port.manufacturer}")
    print(f"   🔧 Hardware ID: {port.hwid}")
    print()

# Probar puertos para encontrar SIM7600
print("=" * 70)
print("🔍 PASO 2: Probando puertos para encontrar SIM7600...")
print("=" * 70)

puerto_encontrado = None
baudrate_encontrado = None
baudrates = [115200, 9600, 230400, 57600]

for port in ports:
    port_name = port.device
    print(f"\n🔌 Probando {port_name}...")
    
    for baudrate in baudrates:
        try:
            ser = serial.Serial(
                port=port_name,
                baudrate=baudrate,
                timeout=3,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            
            time.sleep(2)  # Esperar a que el módulo esté listo
            
            # Limpiar buffers
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            
            # Enviar comando AT
            ser.write(b'AT\r\n')
            time.sleep(1)
            
            # Leer respuesta
            respuesta = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            ser.close()
            
            if 'OK' in respuesta.upper():
                print(f"   ✅ {port_name} responde correctamente!")
                print(f"   📊 Baud Rate: {baudrate}")
                print(f"   📥 Respuesta: {respuesta.strip()}")
                puerto_encontrado = port_name
                baudrate_encontrado = baudrate
                break
            else:
                print(f"   ⚠️  {port_name} no respondió (Baud: {baudrate})")
                
        except serial.SerialException as e:
            print(f"   ❌ Error de comunicación: {str(e)[:50]}")
            continue
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}")
            continue
    
    if puerto_encontrado:
        break

print("\n" + "=" * 70)

if puerto_encontrado:
    print(f"✅ SIM7600 ENCONTRADO!")
    print(f"   Puerto: {puerto_encontrado}")
    print(f"   Baud Rate: {baudrate_encontrado}")
    print("=" * 70)
    
    # Obtener información del módulo
    print("\n📋 Obteniendo información del módulo...")
    try:
        ser = serial.Serial(
            port=puerto_encontrado,
            baudrate=baudrate_encontrado,
            timeout=3
        )
        time.sleep(1)
        
        comandos_info = [
            ('ATI', 'Información'),
            ('AT+GMI', 'Fabricante'),
            ('AT+GMM', 'Modelo'),
            ('AT+GMR', 'Versión'),
        ]
        
        for cmd, desc in comandos_info:
            ser.reset_input_buffer()
            ser.write(f'{cmd}\r\n'.encode())
            time.sleep(0.5)
            respuesta = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            if respuesta.strip():
                print(f"   {desc}: {respuesta.strip().replace(chr(13), '').replace(chr(10), ' ')}")
        
        ser.close()
    except Exception as e:
        print(f"   ⚠️  No se pudo obtener información: {e}")
    
    print("\n" + "=" * 70)
    print("📝 CONFIGURACIÓN NECESARIA:")
    print("=" * 70)
    print(f"\n1. Edita el archivo: configurar_sim7600.py")
    print(f"2. Cambia estas líneas:")
    print(f"   PORT = '{puerto_encontrado}'")
    print(f"   BAUDRATE = {baudrate_encontrado}")
    print(f"   APN = 'TU_APN_AQUI'  # Ejemplo: 'internet.itelcel.com'")
    print(f"   SIM_PIN = ''  # O tu PIN si la SIM lo requiere")
    print(f"\n3. Luego ejecuta: python configurar_sim7600.py")
    print("\n💡 O ejecuta: python detectar_y_configurar_sim7600.py")
    print("   (te guiará paso a paso para configurar APN y PIN)")
    
else:
    print("❌ No se encontró ningún módulo SIM7600 respondiendo")
    print("\n💡 Posibles causas:")
    print("   - El módulo no está encendido")
    print("   - El módulo no está en modo AT")
    print("   - Necesitas instalar drivers específicos")
    print("   - El módulo está en otro puerto COM")
    print("   - El módulo necesita ser inicializado primero")

print("\n" + "=" * 70)
input("\nPresiona Enter para salir...")
