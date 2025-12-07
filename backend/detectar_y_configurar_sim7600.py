#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para detectar puertos COM y configurar SIM7600
"""

import sys
import os

def verificar_pyserial():
    """Verifica si pyserial está instalado"""
    try:
        import serial
        import serial.tools.list_ports
        return True
    except ImportError:
        print("❌ Error: pyserial no está instalado")
        print("\n📦 Instalando pyserial...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"])
            print("✅ pyserial instalado correctamente")
            import serial
            import serial.tools.list_ports
            return True
        except Exception as e:
            print(f"❌ Error al instalar pyserial: {e}")
            print("\nInstala manualmente con:")
            print("   pip install pyserial")
            return False

def listar_puertos_com():
    """Lista todos los puertos COM disponibles"""
    try:
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        return ports
    except Exception as e:
        print(f"❌ Error al listar puertos: {e}")
        return []

def probar_puerto(port_name, baudrate=115200):
    """Prueba si un puerto responde a comandos AT"""
    try:
        import serial
        import time
        
        print(f"\n🔍 Probando {port_name}...")
        ser = serial.Serial(
            port=port_name,
            baudrate=baudrate,
            timeout=3,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        
        time.sleep(2)  # Esperar a que el módulo esté listo
        
        # Enviar comando AT
        ser.write(b'AT\r\n')
        time.sleep(1)
        
        respuesta = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
        ser.close()
        
        if 'OK' in respuesta:
            print(f"✅ {port_name} responde correctamente!")
            return True
        else:
            print(f"⚠️  {port_name} no respondió con OK")
            return False
            
    except serial.SerialException as e:
        print(f"❌ Error al abrir {port_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 70)
    print("📡 Detector y Configurador SIM7600")
    print("=" * 70)
    
    # Verificar pyserial
    if not verificar_pyserial():
        return
    
    # Listar puertos COM
    print("\n🔍 Buscando puertos COM disponibles...\n")
    ports = listar_puertos_com()
    
    if not ports:
        print("❌ No se encontraron puertos COM")
        print("\nVerifica que:")
        print("  - El SIM7600 esté conectado por USB")
        print("  - Los drivers estén instalados")
        print("  - El cable esté bien conectado")
        input("\nPresiona Enter para salir...")
        return
    
    print(f"✅ Se encontraron {len(ports)} puerto(s) COM:\n")
    for i, port in enumerate(ports, 1):
        print(f"{i}. {port.device}")
        print(f"   📝 Descripción: {port.description}")
        print(f"   🔧 Hardware ID: {port.hwid}")
        print()
    
    # Preguntar qué puerto probar
    print("=" * 70)
    print("\n¿Qué puerto quieres probar?")
    print("(Ingresa el número o el nombre del puerto, ej: 1 o COM3)")
    print("(O presiona Enter para probar todos)")
    
    seleccion = input("\n👉 Tu elección: ").strip()
    
    puertos_a_probar = []
    
    if not seleccion:
        # Probar todos
        puertos_a_probar = [port.device for port in ports]
        print("\n🔍 Probando todos los puertos...")
    elif seleccion.isdigit():
        # Selección por número
        idx = int(seleccion) - 1
        if 0 <= idx < len(ports):
            puertos_a_probar = [ports[idx].device]
        else:
            print("❌ Número inválido")
            return
    else:
        # Selección por nombre
        if seleccion.upper() in [port.device.upper() for port in ports]:
            puertos_a_probar = [seleccion.upper()]
        else:
            print(f"❌ Puerto {seleccion} no encontrado")
            return
    
    # Probar puertos
    puerto_encontrado = None
    for port_name in puertos_a_probar:
        if probar_puerto(port_name):
            puerto_encontrado = port_name
            break
    
    if not puerto_encontrado:
        print("\n❌ No se encontró ningún módulo SIM7600 respondiendo")
        print("\nPosibles causas:")
        print("  - El módulo no está encendido")
        print("  - El Baud Rate es incorrecto (prueba 9600 o 115200)")
        print("  - El módulo no está en modo AT")
        input("\nPresiona Enter para salir...")
        return
    
    print("\n" + "=" * 70)
    print(f"✅ Módulo SIM7600 encontrado en: {puerto_encontrado}")
    print("=" * 70)
    
    # Preguntar por APN
    print("\n📡 Configuración del APN:")
    print("\nAPNs comunes:")
    print("  - Telcel México: internet.itelcel.com")
    print("  - Movistar México: internet.movistar.mx")
    print("  - AT&T México: internet.att.com.mx")
    print("  - Claro Colombia: internet.claro.com.co")
    print("  - Movistar España: internet.movistar.es")
    
    apn = input("\n👉 Ingresa el APN (o Enter para usar 'internet.itelcel.com'): ").strip()
    if not apn:
        apn = 'internet.itelcel.com'
    
    # Preguntar por PIN
    print("\n🔐 PIN de la SIM:")
    sim_pin = input("👉 Ingresa el PIN (o Enter si no tiene PIN): ").strip()
    
    # Generar script de configuración
    print("\n" + "=" * 70)
    print("📝 Generando configuración...")
    print("=" * 70)
    
    script_config = f"""# Configuración automática generada
PORT = '{puerto_encontrado}'
BAUDRATE = 115200
APN = '{apn}'
SIM_PIN = '{sim_pin}'
"""
    
    # Actualizar el script principal
    script_path = os.path.join(os.path.dirname(__file__), 'configurar_sim7600.py')
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar y reemplazar la sección de configuración
        import re
        patron = r'(PORT = ).*?\n(BAUDRATE = ).*?\n(APN = ).*?\n(SIM_PIN = ).*?\n'
        reemplazo = f'\\1\'{puerto_encontrado}\'\\n\\2{115200}\\n\\3\'{apn}\'\\n\\4\'{sim_pin}\'\\n'
        contenido_nuevo = re.sub(patron, reemplazo, contenido, count=1)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print(f"\n✅ Script configurado correctamente!")
        print(f"   Puerto: {puerto_encontrado}")
        print(f"   APN: {apn}")
        print(f"   PIN: {'Configurado' if sim_pin else 'Sin PIN'}")
        
        # Preguntar si ejecutar ahora
        print("\n" + "=" * 70)
        ejecutar = input("¿Ejecutar la configuración ahora? (s/n): ").strip().lower()
        
        if ejecutar == 's' or ejecutar == 'si' or ejecutar == 'y' or ejecutar == 'yes':
            print("\n🚀 Ejecutando configuración...\n")
            print("=" * 70)
            
            # Importar y ejecutar el script de configuración
            import importlib.util
            spec = importlib.util.spec_from_file_location("configurar_sim7600", script_path)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            
            if hasattr(modulo, 'main'):
                modulo.main()
        else:
            print("\n✅ Configuración guardada. Ejecuta cuando quieras con:")
            print(f"   python {script_path}")
            
    except Exception as e:
        print(f"\n❌ Error al actualizar el script: {e}")
        print("\nConfiguración manual:")
        print(script_config)
    
    input("\nPresiona Enter para salir...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
