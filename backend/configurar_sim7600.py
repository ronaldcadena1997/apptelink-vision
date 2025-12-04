#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar SIM7600 automáticamente
Configura APN, activa conexión y verifica estado
"""

import serial
import time
import sys

# ============================================
# CONFIGURACIÓN - MODIFICA ESTOS VALORES
# ============================================

# Puerto COM del SIM7600 (ejemplo: 'COM3', 'COM4')
PORT = 'COM3'

# Velocidad de comunicación (115200 es común para SIM7600)
BAUDRATE = 115200

# APN de tu operador (ejemplos):
# Telcel México: 'internet.itelcel.com'
# Movistar México: 'internet.movistar.mx'
# AT&T México: 'internet.att.com.mx'
# Claro Colombia: 'internet.claro.com.co'
# Movistar España: 'internet.movistar.es'
APN = 'internet.itelcel.com'  # <-- CAMBIA ESTO

# PIN de la SIM (dejar vacío '' si no tiene PIN)
SIM_PIN = ''  # <-- CAMBIA ESTO si tu SIM tiene PIN

# ============================================
# NO MODIFICAR DE AQUÍ EN ADELANTE
# ============================================

def enviar_comando(ser, comando, esperar_respuesta=True, timeout=5):
    """
    Envía un comando AT y espera la respuesta
    """
    try:
        # Limpiar buffer
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Enviar comando
        comando_completo = f'{comando}\r\n'
        ser.write(comando_completo.encode('utf-8'))
        print(f'📤 Enviando: {comando}')
        
        if not esperar_respuesta:
            time.sleep(0.5)
            return None
        
        # Esperar respuesta
        time.sleep(1)
        respuesta = ''
        inicio = time.time()
        
        while (time.time() - inicio) < timeout:
            if ser.in_waiting:
                datos = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                respuesta += datos
                # Si recibimos OK o ERROR, terminamos
                if 'OK' in respuesta or 'ERROR' in respuesta:
                    break
            time.sleep(0.1)
        
        # Mostrar respuesta
        if respuesta.strip():
            print(f'📥 Respuesta: {respuesta.strip()}')
        
        return respuesta.strip()
    
    except Exception as e:
        print(f'❌ Error enviando comando: {e}')
        return None


def verificar_sim(ser):
    """
    Verifica el estado de la SIM Card
    """
    print('\n🔍 Verificando SIM Card...')
    
    respuesta = enviar_comando(ser, 'AT+CPIN?')
    
    if '+CPIN: READY' in respuesta:
        print('✅ SIM Card lista')
        return True
    elif '+CPIN: SIM PIN' in respuesta:
        if SIM_PIN:
            print(f'🔐 Ingresando PIN: {SIM_PIN}')
            respuesta_pin = enviar_comando(ser, f'AT+CPIN="{SIM_PIN}"')
            if 'OK' in respuesta_pin:
                print('✅ PIN ingresado correctamente')
                return True
            else:
                print('❌ Error al ingresar PIN')
                return False
        else:
            print('❌ SIM requiere PIN pero no está configurado')
            print('   Configura SIM_PIN en el script')
            return False
    else:
        print(f'❌ Estado de SIM desconocido: {respuesta}')
        return False


def configurar_apn(ser):
    """
    Configura el APN
    """
    print(f'\n🌐 Configurando APN: {APN}...')
    
    respuesta = enviar_comando(ser, f'AT+CGDCONT=1,"IP","{APN}"')
    
    if 'OK' in respuesta:
        print('✅ APN configurado correctamente')
        return True
    else:
        print('❌ Error al configurar APN')
        return False


def activar_conexion(ser):
    """
    Activa el contexto PDP para conectarse a internet
    """
    print('\n🔌 Activando conexión...')
    
    # Primero desactivar si está activo
    enviar_comando(ser, 'AT+CGACT=0,1', esperar_respuesta=False)
    time.sleep(2)
    
    # Activar
    respuesta = enviar_comando(ser, 'AT+CGACT=1,1')
    
    if 'OK' in respuesta:
        print('✅ Conexión activada')
        time.sleep(3)  # Esperar a que se establezca
        return True
    else:
        print('❌ Error al activar conexión')
        return False


def verificar_registro(ser):
    """
    Verifica el registro en la red
    """
    print('\n📶 Verificando registro en red...')
    
    # Registro en red celular
    respuesta_creg = enviar_comando(ser, 'AT+CREG?')
    if '+CREG: 0,1' in respuesta_creg or '+CREG: 0,5' in respuesta_creg:
        print('✅ Registrado en red celular')
    else:
        print('⚠️  No registrado en red celular')
    
    # Registro en GPRS
    respuesta_cgreg = enviar_comando(ser, 'AT+CGREG?')
    if '+CGREG: 0,1' in respuesta_cgreg or '+CGREG: 0,5' in respuesta_cgreg:
        print('✅ Registrado en GPRS')
        return True
    else:
        print('⚠️  No registrado en GPRS')
        return False


def obtener_ip(ser):
    """
    Obtiene la dirección IP asignada
    """
    print('\n🌐 Obteniendo dirección IP...')
    
    respuesta = enviar_comando(ser, 'AT+CGPADDR=1')
    
    if '+CGPADDR: 1,' in respuesta:
        # Extraer IP de la respuesta
        try:
            ip = respuesta.split('"')[1]
            print(f'✅ IP asignada: {ip}')
            return ip
        except:
            print('⚠️  No se pudo extraer la IP')
            return None
    else:
        print('❌ No se obtuvo IP')
        return None


def verificar_senal(ser):
    """
    Verifica la intensidad de señal
    """
    print('\n📡 Verificando señal...')
    
    respuesta = enviar_comando(ser, 'AT+CSQ')
    
    if '+CSQ:' in respuesta:
        try:
            # Extraer valor de señal (formato: +CSQ: XX,YY)
            valores = respuesta.split(':')[1].strip().split(',')
            rssi = int(valores[0])
            
            if rssi == 99:
                print('❌ Sin señal')
            elif rssi >= 20:
                print(f'✅ Señal excelente ({rssi}/31)')
            elif rssi >= 15:
                print(f'✅ Señal buena ({rssi}/31)')
            elif rssi >= 10:
                print(f'⚠️  Señal regular ({rssi}/31)')
            else:
                print(f'⚠️  Señal débil ({rssi}/31)')
        except:
            print('⚠️  No se pudo leer la señal')
    else:
        print('❌ Error al verificar señal')


def configurar_dns(ser):
    """
    Configura servidores DNS
    """
    print('\n🔧 Configurando DNS...')
    
    respuesta = enviar_comando(ser, 'AT+CDNSCFG="8.8.8.8","8.8.4.4"')
    
    if 'OK' in respuesta:
        print('✅ DNS configurado (Google DNS)')
        return True
    else:
        print('⚠️  No se pudo configurar DNS (puede no ser crítico)')
        return False


def probar_internet(ser):
    """
    Prueba la conexión a internet
    """
    print('\n🌍 Probando conexión a internet...')
    
    # Inicializar HTTP
    respuesta = enviar_comando(ser, 'AT+HTTPINIT')
    if 'OK' not in respuesta:
        print('⚠️  No se pudo inicializar HTTP (puede ser normal)')
        return False
    
    # Configurar URL
    enviar_comando(ser, 'AT+HTTPPARA="URL","http://www.google.com"', esperar_respuesta=False)
    time.sleep(1)
    
    # Realizar petición
    respuesta = enviar_comando(ser, 'AT+HTTPACTION=0', timeout=10)
    
    if '+HTTPACTION: 0,200' in respuesta:
        print('✅ Conexión a internet funcionando')
        return True
    else:
        print('⚠️  No se pudo verificar conexión HTTP')
        return False


def main():
    """
    Función principal
    """
    print('=' * 60)
    print('📡 Configurador SIM7600')
    print('=' * 60)
    print(f'Puerto: {PORT}')
    print(f'Baud Rate: {BAUDRATE}')
    print(f'APN: {APN}')
    print('=' * 60)
    
    try:
        # Abrir puerto serial
        print(f'\n🔌 Conectando a {PORT}...')
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            timeout=5,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        
        # Esperar a que el módulo esté listo
        time.sleep(2)
        
        # Test básico
        print('\n🧪 Probando comunicación...')
        respuesta = enviar_comando(ser, 'AT')
        if 'OK' not in respuesta:
            print('❌ El módulo no responde. Verifica:')
            print('   - Puerto COM correcto')
            print('   - Baud Rate correcto')
            print('   - Conexiones TX/RX')
            print('   - Módulo encendido')
            ser.close()
            return False
        
        print('✅ Comunicación establecida')
        
        # Verificar información del módulo
        print('\n📋 Información del módulo:')
        enviar_comando(ser, 'ATI')
        enviar_comando(ser, 'AT+GMI')
        enviar_comando(ser, 'AT+GMM')
        
        # Verificar SIM
        if not verificar_sim(ser):
            print('\n❌ Error con la SIM Card. Abortando...')
            ser.close()
            return False
        
        # Verificar señal
        verificar_senal(ser)
        
        # Verificar operador
        print('\n📱 Verificando operador...')
        enviar_comando(ser, 'AT+COPS?')
        
        # Configurar APN
        if not configurar_apn(ser):
            print('\n❌ Error al configurar APN. Abortando...')
            ser.close()
            return False
        
        # Activar conexión
        if not activar_conexion(ser):
            print('\n⚠️  No se pudo activar conexión, pero continuando...')
        
        # Verificar registro
        verificar_registro(ser)
        
        # Obtener IP
        ip = obtener_ip(ser)
        
        # Configurar DNS
        configurar_dns(ser)
        
        # Probar internet (opcional, puede fallar pero no es crítico)
        probar_internet(ser)
        
        # Resumen
        print('\n' + '=' * 60)
        print('✅ Configuración completada')
        print('=' * 60)
        if ip:
            print(f'🌐 IP asignada: {ip}')
        print('\n📝 Próximos pasos:')
        print('   1. Verifica que Windows detecte el módulo como modem')
        print('   2. Configura conexión dial-up en Windows')
        print('   3. Conecta a internet desde Windows')
        print('=' * 60)
        
        ser.close()
        return True
        
    except serial.SerialException as e:
        print(f'\n❌ Error de comunicación serial: {e}')
        print('\nVerifica:')
        print(f'   - Puerto COM: {PORT}')
        print(f'   - Baud Rate: {BAUDRATE}')
        print('   - Que el módulo esté conectado')
        print('   - Que ningún otro programa esté usando el puerto')
        return False
    
    except KeyboardInterrupt:
        print('\n\n⚠️  Interrumpido por el usuario')
        if 'ser' in locals():
            ser.close()
        return False
    
    except Exception as e:
        print(f'\n❌ Error inesperado: {e}')
        if 'ser' in locals():
            ser.close()
        return False


if __name__ == '__main__':
    # Verificar que pyserial esté instalado
    try:
        import serial
    except ImportError:
        print('❌ Error: pyserial no está instalado')
        print('\nInstala con:')
        print('   pip install pyserial')
        sys.exit(1)
    
    # Ejecutar
    exito = main()
    sys.exit(0 if exito else 1)
