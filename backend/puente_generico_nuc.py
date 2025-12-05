#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puente Genérico para NUC
Proxy HTTP genérico que permite al backend en Railway hacer peticiones
a cualquier recurso en la red local del NUC.

NO requiere cambios cuando se agregan endpoints nuevos.
"""

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import socket
from urllib.parse import urljoin
import os
import base64
from datetime import datetime

# Intentar importar OpenCV (opcional, solo si está instalado)
try:
    import cv2
    OPENCV_DISPONIBLE = True
except ImportError:
    OPENCV_DISPONIBLE = False
    print("⚠️  OpenCV no está instalado. El endpoint /api/camaras/<ip>/snapshot no funcionará.")
    print("   Instala con: pip install opencv-python-headless")

app = Flask(__name__)
CORS(app)

# ============================================
# CONFIGURACIÓN
# ============================================

# Red local donde están las cámaras
RED_LOCAL = "192.168.60"  # Ajusta según tu red

# Timeout para peticiones
TIMEOUT = 30

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def es_ip_local(ip):
    """Verifica si una IP está en la red local permitida"""
    return ip.startswith(RED_LOCAL + ".")

def obtener_ip_local(hostname):
    """Resuelve un hostname a IP local"""
    try:
        ip = socket.gethostbyname(hostname)
        return ip if es_ip_local(ip) else None
    except:
        return None

# ============================================
# PROXY GENÉRICO
# ============================================

@app.route('/proxy/<path:target_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_generico(target_path):
    """
    Proxy genérico que permite al backend en Railway hacer peticiones
    a cualquier recurso en la red local.
    
    Uso desde Railway:
    GET http://100.64.0.15:5000/proxy/192.168.60.10:554/stream
    GET http://100.64.0.15:5000/proxy/192.168.60.10/api/status
    """
    try:
        # Parsear la ruta: puede ser IP:puerto/ruta o hostname/ruta
        parts = target_path.split('/', 1)
        target = parts[0]
        path = '/' + parts[1] if len(parts) > 1 else '/'
        
        # Si no tiene puerto, usar 80 por defecto
        if ':' in target:
            target_host, target_port = target.split(':')
            target_port = int(target_port)
        else:
            target_host = target
            target_port = 80
        
        # Verificar que sea IP local
        if not es_ip_local(target_host):
            # Intentar resolver hostname
            resolved_ip = obtener_ip_local(target_host)
            if not resolved_ip:
                return jsonify({
                    "success": False,
                    "error": f"IP {target_host} no está en la red local permitida"
                }), 403
            target_host = resolved_ip
        
        # Construir URL completa
        protocol = 'http' if target_port != 443 else 'https'
        target_url = f"{protocol}://{target_host}:{target_port}{path}"
        
        # Agregar query parameters si existen
        if request.query_string:
            target_url += '?' + request.query_string.decode()
        
        # Hacer la petición
        if request.method == 'GET':
            response = requests.get(target_url, timeout=TIMEOUT, headers=dict(request.headers))
        elif request.method == 'POST':
            response = requests.post(
                target_url,
                data=request.get_data(),
                headers=dict(request.headers),
                timeout=TIMEOUT
            )
        elif request.method == 'PUT':
            response = requests.put(
                target_url,
                data=request.get_data(),
                headers=dict(request.headers),
                timeout=TIMEOUT
            )
        elif request.method == 'DELETE':
            response = requests.delete(target_url, timeout=TIMEOUT, headers=dict(request.headers))
        elif request.method == 'PATCH':
            response = requests.patch(
                target_url,
                data=request.get_data(),
                headers=dict(request.headers),
                timeout=TIMEOUT
            )
        else:
            return jsonify({"success": False, "error": "Método no soportado"}), 405
        
        # Retornar respuesta
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
        
    except requests.exceptions.Timeout:
        return jsonify({"success": False, "error": "Timeout"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"success": False, "error": "No se pudo conectar"}), 502
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================
# ENDPOINTS DE AYUDA (Opcionales)
# ============================================

@app.route('/api/status', methods=['GET'])
def status():
    """Estado del puente"""
    return jsonify({
        "status": "online",
        "tipo": "puente_generico",
        "red_local": RED_LOCAL,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })

@app.route('/api/red/escaneo', methods=['GET'])
def escanear_red():
    """
    Escanea la red local para encontrar dispositivos
    Útil para detectar cámaras automáticamente
    """
    dispositivos = []
    rango_inicio = int(request.args.get('inicio', 1))
    rango_fin = int(request.args.get('fin', 255))
    
    for i in range(rango_inicio, rango_fin + 1):
        ip = f"{RED_LOCAL}.{i}"
        try:
            # Intentar conectar a puerto común de cámaras (554 RTSP)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, 554))
            sock.close()
            
            if result == 0:
                dispositivos.append({
                    "ip": ip,
                    "puerto": 554,
                    "tipo": "posible_camara"
                })
        except:
            continue
    
    return jsonify({
        "success": True,
        "dispositivos": dispositivos,
        "total": len(dispositivos)
    })

@app.route('/api/camaras/<ip>/snapshot', methods=['GET'])
def snapshot_camara(ip):
    """
    Obtiene un snapshot de una cámara usando RTSP
    Este endpoint permite a Railway obtener imágenes de las cámaras
    """
    if not OPENCV_DISPONIBLE:
        return jsonify({
            "success": False,
            "error": "OpenCV no está instalado. Instala con: pip install opencv-python-headless"
        }), 503
    
    # Verificar que la IP esté en la red local permitida
    if not es_ip_local(ip):
        return jsonify({
            "success": False,
            "error": f"IP {ip} no está en la red local permitida ({RED_LOCAL}.x)"
        }), 403
    
    # Credenciales de la cámara (obtener de variables de entorno o usar valores por defecto)
    usuario = os.getenv('USUARIO_CAMARAS', 'admin')
    contrasena = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')
    
    # URLs RTSP a probar (formato común de cámaras Hikvision/Dahua)
    urls = [
        f"rtsp://{usuario}:{contrasena}@{ip}:554/Streaming/Channels/101",
        f"rtsp://{usuario}:{contrasena}@{ip}:554/Streaming/Channels/1",
        f"rtsp://{usuario}:{contrasena}@{ip}:554/h264/ch1/main/av_stream",
    ]
    
    cap = None
    for url in urls:
        try:
            # Configurar timeout para OpenCV
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000000"  # 5 segundos
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)  # 5 segundos timeout
            cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
            
            if cap.isOpened():
                ret, frame = cap.read()
                
                if ret and frame is not None:
                    # Convertir a JPEG con calidad 85
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    # IMPORTANTE: Liberar recursos inmediatamente
                    cap.release()
                    cap = None
                    
                    return jsonify({
                        "success": True,
                        "image": f"data:image/jpeg;base64,{img_base64}",
                        "timestamp": datetime.now().isoformat(),
                        "ip": ip,
                        "url_rtsp": url
                    })
                else:
                    # Si no pudo leer frame, liberar y continuar
                    if cap:
                        cap.release()
                        cap = None
        except Exception as e:
            print(f"Error obteniendo snapshot de {ip} con URL {url}: {e}")
            # Asegurarse de liberar recursos en caso de error
            if cap:
                try:
                    cap.release()
                except:
                    pass
                cap = None
            continue
    
    # Asegurarse de liberar recursos al final
    if cap:
        try:
            cap.release()
        except:
            pass
    
    return jsonify({
        "success": False,
        "error": "No se pudo capturar imagen de la cámara. Verifica credenciales y conectividad."
    }), 500

# ============================================
# INICIO
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🌉 Puente Genérico NUC")
    print("=" * 60)
    print("Este puente permite al backend en Railway hacer peticiones")
    print("a CUALQUIER recurso en la red local.")
    print()
    print("Ejemplos de uso desde Railway:")
    print("  GET /proxy/192.168.60.10:554/stream")
    print("  GET /proxy/192.168.60.10/api/status")
    print("  POST /proxy/192.168.60.10/api/config")
    print()
    print("NO necesitas cambiar este código cuando agregues endpoints.")
    print("=" * 60)
    print()
    
    # Instalar dependencias si no están
    try:
        import flask
        import requests
    except ImportError:
        print("⚠️  Instalando dependencias...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "requests"])
    
    # Verificar OpenCV
    if not OPENCV_DISPONIBLE:
        print("⚠️  OpenCV no está instalado.")
        print("   Para usar /api/camaras/<ip>/snapshot, instala con:")
        print("   pip install opencv-python-headless")
    else:
        print("✅ OpenCV disponible. Endpoint /api/camaras/<ip>/snapshot activo.")
    
    print("🚀 Iniciando puente genérico en puerto 5000...")
    print(f"📡 Red local permitida: {RED_LOCAL}.x")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
