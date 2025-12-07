#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NUC Agent Simple - Arquitectura Polling/Webhook
================================================
Este script corre en el NUC y envía datos periódicamente al backend en Railway.
No necesita Tailscale en Railway, solo salida HTTP.
"""

import requests
import cv2
import time
import base64
import os
from datetime import datetime

# ============================================
# CONFIGURACIÓN
# ============================================

# URL del backend en Railway
RAILWAY_BACKEND_URL = os.getenv(
    'RAILWAY_BACKEND_URL',
    'https://apptelink-vision-production.up.railway.app'
)

# ID del NUC (para identificar de qué NUC vienen los datos)
NUC_ID = os.getenv('NUC_ID', 'nuc_sede1')

# IPs de cámaras en este NUC
CAMARAS_IPS = os.getenv('CAMARAS_IPS', '192.168.60.65').split(',')

# Credenciales de cámaras
USUARIO_CAMARAS = os.getenv('USUARIO_CAMARAS', 'admin')
CONTRASENA_CAMARAS = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')

# Intervalo de envío (segundos)
INTERVALO_ENVIO = int(os.getenv('INTERVALO_ENVIO', '30'))

# ============================================
# FUNCIONES
# ============================================

def capturar_snapshot(ip_camara):
    """
    Captura un snapshot de una cámara
    Retorna: (success, image_base64, error)
    """
    try:
        # Construir URL RTSP
        rtsp_url = f"rtsp://{USUARIO_CAMARAS}:{CONTRASENA_CAMARAS}@{ip_camara}:554/Streaming/Channels/101"
        
        # Capturar frame
        cap = cv2.VideoCapture(rtsp_url)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
        
        if not cap.isOpened():
            return False, None, "No se pudo abrir la cámara"
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            return False, None, "No se pudo capturar frame"
        
        # Redimensionar si es muy grande (opcional)
        height, width = frame.shape[:2]
        if width > 1920:
            scale = 1920 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Convertir a JPEG y luego a base64
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return True, img_base64, None
        
    except Exception as e:
        return False, None, str(e)

def enviar_snapshot_al_servidor(ip_camara, image_base64, estado='activa'):
    """
    Envía un snapshot al backend en Railway
    """
    try:
        url = f"{RAILWAY_BACKEND_URL}/api/camaras/{ip_camara}/snapshot"
        
        data = {
            'nuc_id': NUC_ID,
            'ip': ip_camara,
            'image': image_base64,
            'estado': estado,
            'timestamp': datetime.now().isoformat()
        }
        
        response = requests.post(
            url,
            json=data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            return True, None
        else:
            return False, f"Error {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return False, "Timeout al conectar con el servidor"
    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con el servidor"
    except Exception as e:
        return False, str(e)

def registrar_estado_camara(ip_camara, estado, error=None):
    """
    Registra el estado de una cámara en el servidor
    """
    try:
        url = f"{RAILWAY_BACKEND_URL}/api/camaras/{ip_camara}/estado"
        
        data = {
            'nuc_id': NUC_ID,
            'ip': ip_camara,
            'estado': estado,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }
        
        requests.post(
            url,
            json=data,
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
    except:
        pass  # No crítico si falla

def main():
    """
    Bucle principal: captura snapshots y los envía al servidor
    """
    print("=" * 70)
    print("NUC Agent - Enviando datos al servidor")
    print("=" * 70)
    print(f"Backend URL: {RAILWAY_BACKEND_URL}")
    print(f"NUC ID: {NUC_ID}")
    print(f"Cámaras: {', '.join(CAMARAS_IPS)}")
    print(f"Intervalo: {INTERVALO_ENVIO} segundos")
    print("=" * 70)
    print()
    
    ciclo = 0
    
    while True:
        ciclo += 1
        print(f"[Ciclo {ciclo}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for ip_camara in CAMARAS_IPS:
            ip_camara = ip_camara.strip()
            if not ip_camara:
                continue
            
            print(f"  📹 Procesando cámara {ip_camara}...", end=' ')
            
            # Capturar snapshot
            success, image_base64, error = capturar_snapshot(ip_camara)
            
            if success and image_base64:
                # Enviar al servidor
                envio_ok, envio_error = enviar_snapshot_al_servidor(ip_camara, image_base64, 'activa')
                
                if envio_ok:
                    print("✅ OK")
                    registrar_estado_camara(ip_camara, 'activa')
                else:
                    print(f"❌ Error al enviar: {envio_error}")
                    registrar_estado_camara(ip_camara, 'error', envio_error)
            else:
                print(f"❌ Error al capturar: {error}")
                registrar_estado_camara(ip_camara, 'sin_acceso', error)
        
        print(f"  ⏳ Esperando {INTERVALO_ENVIO} segundos...")
        print()
        time.sleep(INTERVALO_ENVIO)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDeteniendo NUC Agent...")
    except Exception as e:
        print(f"\n\nError fatal: {e}")
        import traceback
        traceback.print_exc()
