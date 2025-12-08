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
import subprocess
import socket
import requests
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
    import subprocess
    import socket
    
    # Primero verificar que la cámara responde al ping
    try:
        result = subprocess.run(
            ['ping', '-n', '1', '-w', '1000', ip_camara],
            capture_output=True,
            timeout=2
        )
        if result.returncode != 0:
            return None, f"La cámara {ip_camara} no responde al ping. Verifica que esté encendida y en la red."
    except:
        pass  # Continuar aunque el ping falle
    
    # Verificar que el puerto 554 está abierto
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip_camara, 554))
        sock.close()
        if result != 0:
            return None, f"El puerto 554 (RTSP) está cerrado en {ip_camara}. Verifica configuración de la cámara."
    except:
        pass  # Continuar aunque la verificación de puerto falle
    
    cap = None
    urls_intentadas = []
    
    try:
        # URLs específicas para Hikvision (DS-2CD1047G2)
        # Orden: primero HTTP (más rápido y confiable), luego RTSP
        urls = [
            # HTTP Snapshots (Hikvision ISAPI) - Más confiable
            f"http://{ip_camara}/ISAPI/Streaming/channels/101/picture",
            f"http://{ip_camara}/ISAPI/Streaming/channels/1/picture",
            f"http://{ip_camara}/cgi-bin/snapshot.cgi?channel=1",
            f"http://{ip_camara}/Streaming/channels/101/picture",
            # RTSP Streams (Hikvision)
            f"rtsp://{USUARIO_CAMARAS}:{CONTRASENA_CAMARAS}@{ip_camara}:554/Streaming/Channels/101",
            f"rtsp://{USUARIO_CAMARAS}:{CONTRASENA_CAMARAS}@{ip_camara}:554/Streaming/Channels/1",
            f"rtsp://{USUARIO_CAMARAS}:{CONTRASENA_CAMARAS}@{ip_camara}:554/h264/ch1/main/av_stream",
            f"rtsp://{USUARIO_CAMARAS}:{CONTRASENA_CAMARAS}@{ip_camara}:554/Streaming/Channels/102",
        ]
        
        for url in urls:
            try:
                # Ocultar credenciales en el log
                url_log = url.split('@')[1] if '@' in url else url
                urls_intentadas.append(url_log)
                
                # Si es HTTP, intentar descargar snapshot directamente
                if url.startswith('http://'):
                    try:
                        # Para Hikvision, usar autenticación básica
                        response = requests.get(
                            url, 
                            timeout=5, 
                            auth=(USUARIO_CAMARAS, CONTRASENA_CAMARAS),
                            stream=True
                        )
                        if response.status_code == 200:
                            # Verificar que es una imagen
                            content_type = response.headers.get('content-type', '')
                            if 'image' in content_type or len(response.content) > 100:
                                # Convertir imagen HTTP a base64
                                img_base64 = base64.b64encode(response.content).decode('utf-8')
                                return img_base64, None
                    except Exception as e:
                        continue  # Intentar siguiente URL
                
                # Si es RTSP, usar OpenCV
                if url.startswith('rtsp://'):
                    # Configurar timeout más corto
                    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000000"  # 5 segundos
                    
                    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
                    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
                    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
                    
                    if not cap.isOpened():
                        if cap:
                            cap.release()
                        continue  # Intentar siguiente URL
                    
                    # Intentar leer frame con timeout
                    ret, frame = cap.read()
                    
                    if ret and frame is not None:
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
                        
                        if cap:
                            cap.release()
                        
                        return img_base64, None
                    else:
                        if cap:
                            cap.release()
                        continue  # Intentar siguiente URL
                    
            except Exception as e:
                if cap:
                    cap.release()
                continue  # Intentar siguiente URL
        
        # Si llegamos aquí, ninguna URL funcionó
        error_msg = f"No se pudo conectar a {ip_camara}. URLs intentadas: {', '.join(urls_intentadas)}"
        error_msg += f"\n   Verifica: IP ({ip_camara}), credenciales (usuario: {USUARIO_CAMARAS}), y que la cámara esté encendida"
        return None, error_msg
        
    except Exception as e:
        if cap:
            cap.release()
        return None, f"Error al capturar de {ip_camara}: {str(e)}"

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
                print(f"✅ Snapshot capturado y enviado: {ip_camara} ({len(snapshot)} bytes)")
            else:
                sio.emit('snapshot_error', {
                    'nuc_id': NUC_ID,
                    'ip': ip_camara,
                    'error': error,
                    'timestamp': datetime.now().isoformat()
                })
                # Mostrar error de forma más clara
                error_lines = error.split('\n') if error else [str(error)]
                print(f"❌ Error al capturar {ip_camara}:")
                for line in error_lines:
                    if line.strip():
                        print(f"   {line.strip()}")
        
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
