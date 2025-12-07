#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NUC Agent - Estilo Hikvision
==============================
Este agente se conecta al servidor central (como Hik-Connect)
y mantiene una conexión persistente para enviar datos.
"""

import socketio
import cv2
import base64
import time
import os
from datetime import datetime

# Importar configuración centralizada
try:
    from config import (
        CAMARAS_CONFIGURADAS, CAMARAS_DICT, CAMARAS_CONFIG,
        USUARIO_CAMARAS, CONTRASENA_CAMARAS,
        obtener_info_camara
    )
    USAR_CONFIG_FILE = True
except ImportError:
    USAR_CONFIG_FILE = False
    CAMARAS_CONFIGURADAS = []
    CAMARAS_DICT = {}
    USUARIO_CAMARAS = os.getenv('USUARIO_CAMARAS', 'admin')
    CONTRASENA_CAMARAS = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')

# ============================================
# CONFIGURACIÓN
# ============================================

# URL del servidor central (Railway)
SERVER_URL = os.getenv(
    'SERVER_URL',
    'https://apptelink-vision-production.up.railway.app'
)

# ID del NUC - Se obtiene de variable de entorno o config.py
# Si hay config.py con NUCs_CONFIG, usar el primero disponible
if USAR_CONFIG_FILE:
    try:
        from config import NUCs_CONFIG
        # Si hay NUCs configurados, usar el primero como default
        if NUCs_CONFIG:
            NUC_ID = os.getenv('NUC_ID', list(NUCs_CONFIG.keys())[0])
        else:
            NUC_ID = os.getenv('NUC_ID', 'nuc_sede1')
    except:
        NUC_ID = os.getenv('NUC_ID', 'nuc_sede1')
else:
    NUC_ID = os.getenv('NUC_ID', 'nuc_sede1')

# Obtener SERVER_URL desde config.py si está disponible
if USAR_CONFIG_FILE:
    try:
        from config import NUCs_CONFIG
        if NUC_ID in NUCs_CONFIG and 'server_url' in NUCs_CONFIG[NUC_ID]:
            SERVER_URL = os.getenv('SERVER_URL', NUCs_CONFIG[NUC_ID]['server_url'])
    except:
        pass

# IPs de cámaras - Desde config.py (filtrar por NUC_ID) o variable de entorno
if USAR_CONFIG_FILE and CAMARAS_CONFIGURADAS:
    # Filtrar cámaras que pertenecen a este NUC
    if CAMARAS_CONFIG:
        CAMARAS_IPS = [cam['ip'] for cam in CAMARAS_CONFIG if cam.get('nuc') == NUC_ID]
        if not CAMARAS_IPS:
            # Si no hay cámaras específicas para este NUC, usar todas
            CAMARAS_IPS = CAMARAS_CONFIGURADAS
    else:
        CAMARAS_IPS = CAMARAS_CONFIGURADAS
else:
    CAMARAS_IPS_STR = os.getenv('CAMARAS_IPS', '192.168.60.65')
    CAMARAS_IPS = [ip.strip() for ip in CAMARAS_IPS_STR.split(',') if ip.strip()]

# Intervalo de envío de snapshots (segundos)
INTERVALO_SNAPSHOT = int(os.getenv('INTERVALO_SNAPSHOT', '30'))

# ============================================
# CLIENTE WEBSOCKET
# ============================================

sio = socketio.Client(reconnection=True, reconnection_attempts=10, reconnection_delay=5)

# ============================================
# FUNCIONES
# ============================================

def capturar_snapshot(ip_camara):
    """Captura snapshot de una cámara"""
    try:
        rtsp_url = f"rtsp://{USUARIO_CAMARAS}:{CONTRASENA_CAMARAS}@{ip_camara}:554/Streaming/Channels/101"
        
        cap = cv2.VideoCapture(rtsp_url)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
        
        if not cap.isOpened():
            return None, "No se pudo abrir la cámara"
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return None, "No se pudo capturar frame"
        
        # Redimensionar si es muy grande
        height, width = frame.shape[:2]
        if width > 1920:
            scale = 1920 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Convertir a base64
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return img_base64, None
        
    except Exception as e:
        return None, str(e)

# ============================================
# EVENTOS WEBSOCKET
# ============================================

@sio.on('connect')
def on_connect():
    """Cuando se conecta al servidor"""
    print(f"✅ Conectado al servidor central: {SERVER_URL}")
    print(f"   NUC ID: {NUC_ID}")
    
    # Enviar información del NUC
    sio.emit('nuc_register', {
        'nuc_id': NUC_ID,
        'camaras': CAMARAS_IPS,
        'timestamp': datetime.now().isoformat()
    })

@sio.on('disconnect')
def on_disconnect():
    """Cuando se desconecta del servidor"""
    print("❌ Desconectado del servidor. Intentando reconectar...")

@sio.on('connected')
def on_connected(data):
    """Respuesta del servidor cuando se conecta"""
    print(f"✅ Servidor confirmó conexión: {data}")

@sio.on('capture_snapshot')
def on_capture_request(data):
    """Servidor pide capturar snapshot de una cámara específica"""
    ip = data.get('ip')
    if not ip:
        return
    
    print(f"📸 Servidor solicita snapshot de {ip}...")
    
    snapshot, error = capturar_snapshot(ip)
    
    if snapshot:
        sio.emit('snapshot', {
            'nuc_id': NUC_ID,
            'ip': ip,
            'image': snapshot,
            'timestamp': datetime.now().isoformat(),
            'estado': 'activa'
        })
        print(f"✅ Snapshot enviado: {ip}")
    else:
        sio.emit('snapshot_error', {
            'nuc_id': NUC_ID,
            'ip': ip,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        print(f"❌ Error al capturar {ip}: {error}")

@sio.on('ping')
def on_ping(data):
    """Servidor hace ping para verificar conexión"""
    sio.emit('pong', {
        'nuc_id': NUC_ID,
        'timestamp': datetime.now().isoformat()
    })

# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def enviar_snapshots_periodicos():
    """Envía snapshots periódicamente a todas las cámaras"""
    while sio.connected:
        for ip_camara in CAMARAS_IPS:
            ip_camara = ip_camara.strip()
            if not ip_camara:
                continue
            
            print(f"📸 Capturando snapshot de {ip_camara}...")
            
            snapshot, error = capturar_snapshot(ip_camara)
            
            if snapshot:
                sio.emit('snapshot', {
                    'nuc_id': NUC_ID,
                    'ip': ip_camara,
                    'image': snapshot,
                    'timestamp': datetime.now().isoformat(),
                    'estado': 'activa'
                })
                print(f"✅ Snapshot enviado: {ip_camara}")
            else:
                sio.emit('snapshot_error', {
                    'nuc_id': NUC_ID,
                    'ip': ip_camara,
                    'error': error,
                    'timestamp': datetime.now().isoformat()
                })
                print(f"❌ Error: {ip_camara} - {error}")
        
        # Esperar antes del siguiente ciclo
        time.sleep(INTERVALO_SNAPSHOT)

def main():
    """Función principal"""
    print("=" * 70)
    print("NUC Agent - Estilo Hikvision")
    print("=" * 70)
    print(f"Servidor: {SERVER_URL}")
    print(f"NUC ID: {NUC_ID}")
    print(f"Cámaras: {', '.join(CAMARAS_IPS)}")
    print(f"Intervalo: {INTERVALO_SNAPSHOT} segundos")
    print("=" * 70)
    print()
    
    # Conectar al servidor
    try:
        print("🔌 Conectando al servidor central...")
        sio.connect(
            SERVER_URL,
            auth={'nuc_id': NUC_ID},
            wait_timeout=10
        )
        
        # Iniciar envío periódico de snapshots en un hilo separado
        import threading
        snapshot_thread = threading.Thread(target=enviar_snapshots_periodicos, daemon=True)
        snapshot_thread.start()
        
        # Mantener conexión viva
        print("✅ Conectado. Enviando snapshots periódicamente...")
        print("   Presiona CTRL+C para detener")
        print()
        
        sio.wait()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo NUC Agent...")
        sio.disconnect()
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
