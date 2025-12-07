#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puente Mínimo para NUC
Solo expone endpoints necesarios para acceso a cámaras
NO es un backend completo, solo un puente/acceso
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import socket
import cv2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================
# FUNCIONES MÍNIMAS - Solo acceso a cámaras
# ============================================

def escanear_red_local(rango_inicio=1, rango_fin=255):
    """Escanea la red local para encontrar cámaras"""
    camaras = []
    red_base = "192.168.60"  # Ajusta según tu red
    
    for i in range(rango_inicio, rango_fin + 1):
        ip = f"{red_base}.{i}"
        try:
            # Intentar conectar al puerto 554 (RTSP común)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, 554))
            sock.close()
            
            if result == 0:
                camaras.append({
                    "ip": ip,
                    "puerto": 554,
                    "url_rtsp": f"rtsp://{ip}:554/stream"
                })
        except:
            continue
    
    return camaras

def obtener_snapshot_camara(ip_camara, puerto=554):
    """Obtiene un snapshot de una cámara"""
    try:
        url_rtsp = f"rtsp://{ip_camara}:{puerto}/stream"
        cap = cv2.VideoCapture(url_rtsp)
        
        if not cap.isOpened():
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Guardar temporalmente
            ruta_temp = f"temp_snapshot_{ip_camara.replace('.', '_')}.jpg"
            cv2.imwrite(ruta_temp, frame)
            return ruta_temp
        
        return None
    except Exception as e:
        print(f"Error obteniendo snapshot: {e}")
        return None

# ============================================
# ENDPOINTS MÍNIMOS - Solo lo necesario
# ============================================

@app.route('/api/status', methods=['GET'])
def status():
    """Endpoint de estado mínimo"""
    return jsonify({
        "status": "online",
        "tipo": "puente_nuc",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/camaras/detectar', methods=['GET'])
def detectar_camaras():
    """Detecta cámaras en la red local"""
    try:
        camaras = escanear_red_local()
        return jsonify({
            "success": True,
            "camaras": camaras,
            "total": len(camaras)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/camaras/<ip>/snapshot', methods=['GET'])
def snapshot(ip):
    """Obtiene snapshot de una cámara"""
    try:
        ruta_imagen = obtener_snapshot_camara(ip)
        if ruta_imagen and os.path.exists(ruta_imagen):
            return send_file(ruta_imagen, mimetype='image/jpeg')
        else:
            return jsonify({
                "success": False,
                "error": "No se pudo obtener snapshot"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/camaras/<ip>/info', methods=['GET'])
def info_camara(ip):
    """Información básica de una cámara"""
    return jsonify({
        "ip": ip,
        "puerto": 554,
        "url_rtsp": f"rtsp://{ip}:554/stream",
        "disponible": True
    })

# ============================================
# INICIO
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🌉 Puente Mínimo NUC")
    print("=" * 60)
    print("Este script solo actúa como puente para acceso a cámaras")
    print("NO es un backend completo, solo expone endpoints mínimos")
    print("=" * 60)
    print()
    
    # Instalar dependencias mínimas si no están
    try:
        import flask
        import cv2
    except ImportError:
        print("⚠️  Instalando dependencias mínimas...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "opencv-python"])
    
    # Iniciar servidor
    print("🚀 Iniciando puente en puerto 5000...")
    print("📡 El backend en Railway se conectará a: http://TU_IP_TAILSCALE:5000")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
