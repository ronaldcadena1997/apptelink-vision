"""
============================================
SERVIDOR API - APPTELINK VISION
============================================
Proporciona endpoints REST para:
- Detectar cámaras en la red
- Gestionar configuración de cercas
- Servir imágenes de intrusos
"""

from flask import Flask, jsonify, request, send_file, send_from_directory, Response
from flask_cors import CORS
import socket
import concurrent.futures
import os
import json
import cv2
from datetime import datetime
import base64
import threading
import time
import requests

# Configurar proxy para Tailscale userspace-networking
# Si Tailscale está usando userspace-networking, necesitamos usar proxy SOCKS5
TAILSCALE_PROXY = None

# Verificar si Tailscale está conectado y usar proxy SOCKS5
# En userspace-networking, el proxy está en localhost:1080
try:
    import subprocess
    import os
    
    # Verificar si Tailscale está conectado
    # Si estamos en Railway con Tailscale, asumimos que el proxy está disponible
    if os.getenv('TAILSCALE_AUTHKEY'):
        # Tailscale está configurado, intentar usar proxy SOCKS5
        # El proxy puede no estar disponible inmediatamente, pero lo intentaremos
        TAILSCALE_PROXY = {
            'http': 'socks5h://127.0.0.1:1080',
            'https': 'socks5h://127.0.0.1:1080'
        }
        print("✅ Proxy SOCKS5 configurado para Tailscale userspace-networking")
        print("   Si las conexiones fallan, el proxy puede no estar disponible aún")
    else:
        print("ℹ️  Tailscale no configurado, usando conexiones directas")
except Exception as e:
    print(f"⚠️  No se pudo configurar proxy SOCKS5: {e}")
    print("   Usando conexiones directas")

# Importar configuración centralizada
try:
    from config import (
        NUCs, CAMARAS_CONFIGURADAS, CAMARAS_DICT,
        obtener_nuc_por_camara, obtener_info_camara,
        listar_camaras_por_nuc, obtener_resumen_config,
        USUARIO_CAMARAS, CONTRASENA_CAMARAS
    )
    USAR_CONFIG_FILE = True
except ImportError:
    # Si no existe config.py, usar configuración por variables de entorno (comportamiento original)
    USAR_CONFIG_FILE = False
    NUCs = {}
    CAMARAS_CONFIGURADAS = []
    CAMARAS_DICT = {}
    USUARIO_CAMARAS = os.getenv('USUARIO_CAMARAS', 'admin')
    CONTRASENA_CAMARAS = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde cualquier origen

# Diccionario para almacenar streams activos
streams_activos = {}

# ============================================
# CONFIGURACIÓN DE PROXY (Backend en Servidor)
# ============================================
# Si no se usa config.py, leer desde variables de entorno
if not USAR_CONFIG_FILE:
    # Soporte para múltiples NUCs
    # Formato: NUC_URLS=url1,url2,url3 o NUC_URLS=nombre1:url1,nombre2:url2
    NUC_URLS_STR = os.getenv('NUC_URLS', os.getenv('NUC_URL', None))
    MODO_PROXY = NUC_URLS_STR is not None
    
    if MODO_PROXY:
        # Parsear lista de NUCs
        nucs_list = [n.strip() for n in NUC_URLS_STR.split(',')]
        for nuc in nucs_list:
            if ':' in nuc:
                # Formato: nombre:url
                nombre, url = nuc.split(':', 1)
                NUCs[nombre.strip()] = url.strip()
            else:
                # Formato: url (nombre por defecto)
                nombre = f"nuc_{len(NUCs) + 1}"
                NUCs[nombre] = nuc.strip()
    
    # IPs de cámaras configuradas en Railway (variables de entorno)
    CAMARAS_IPS_STR = os.getenv('CAMARAS_IPS', '')
    CAMARAS_CONFIGURADAS = [ip.strip() for ip in CAMARAS_IPS_STR.split(',') if ip.strip()]
else:
    MODO_PROXY = len(NUCs) > 0

# Mostrar configuración cargada
if USAR_CONFIG_FILE:
    print("📋 Usando archivo de configuración: config.py")
else:
    print("📋 Usando variables de entorno")

if CAMARAS_CONFIGURADAS:
    print(f"📹 IPs de cámaras configuradas: {len(CAMARAS_CONFIGURADAS)}")
    for ip in CAMARAS_CONFIGURADAS:
        info = obtener_info_camara(ip) if USAR_CONFIG_FILE else {'nombre': f'Cámara {ip}'}
        print(f"   - {ip}: {info.get('nombre', '')}")
else:
    print("📹 No hay IPs de cámaras configuradas (se detectarán automáticamente)")

if MODO_PROXY:
    print(f"🔗 Modo PROXY activado. NUCs configurados: {len(NUCs)}")
    for nombre, url in NUCs.items():
        print(f"   - {nombre}: {url}")
else:
    print("🏠 Modo LOCAL activado. Acceso directo a cámaras.")

def seleccionar_nuc(ip_camara=None, nuc_id=None):
    """Selecciona el NUC apropiado basado en IP de cámara o ID de NUC"""
    if not MODO_PROXY or not NUCs:
        return None
    
    # Si se especifica un NUC por ID
    if nuc_id and nuc_id in NUCs:
        return NUCs[nuc_id]
    
    # Si se usa config.py, usar función del módulo
    if USAR_CONFIG_FILE and ip_camara:
        return obtener_nuc_por_camara(ip_camara)
    
    # Si se especifica IP de cámara, intentar mapear a NUC
    if ip_camara:
        # Mapeo simple: basado en rango de IP
        for nombre, url in NUCs.items():
            # Extraer IP base del NUC de la URL
            try:
                nuc_ip = url.split('//')[1].split(':')[0]
                # Si la IP de la cámara está en el mismo rango (primeros 3 octetos)
                if ip_camara.rsplit('.', 1)[0] == nuc_ip.rsplit('.', 1)[0]:
                    return url
            except:
                pass
    
    # Por defecto: usar el primer NUC
    return list(NUCs.values())[0] if NUCs else None

def hacer_proxy(endpoint, method='GET', data=None, params=None, files=None, nuc_url=None, ip_camara=None, nuc_id=None):
    """Hace proxy de la petición al NUC local"""
    if not MODO_PROXY:
        return None  # No está en modo proxy
    
    # Seleccionar NUC si no se especifica
    if not nuc_url:
        nuc_url = seleccionar_nuc(ip_camara, nuc_id)
        if not nuc_url:
            return {"success": False, "error": "No hay NUCs disponibles"}
    
    try:
        url = f"{nuc_url}{endpoint}"
        # Timeout más corto para evitar que se cuelgue (15 segundos en lugar de 30)
        timeout = 15 if '/snapshot' in endpoint else 30
        
        # Usar proxy SOCKS5 si está disponible (Tailscale userspace-networking)
        proxies = TAILSCALE_PROXY if TAILSCALE_PROXY else None
        
        if method == 'GET':
            response = requests.get(url, params=params, timeout=timeout, proxies=proxies)
        elif method == 'POST':
            if files:
                response = requests.post(url, data=data, files=files, params=params, timeout=timeout, proxies=proxies)
            else:
                response = requests.post(url, json=data, params=params, timeout=timeout, proxies=proxies)
        elif method == 'PUT':
            response = requests.put(url, json=data, params=params, timeout=timeout, proxies=proxies)
        elif method == 'DELETE':
            response = requests.delete(url, params=params, timeout=timeout, proxies=proxies)
        else:
            return None
        
        if response.status_code == 200:
            # Intentar parsear como JSON, si falla devolver texto
            try:
                return response.json()
            except:
                return {"success": True, "data": response.text}
        else:
            return {"success": False, "error": f"Error {response.status_code}"}
    except Exception as e:
        print(f"❌ Error en proxy: {e}")
        return {"success": False, "error": str(e)}

def proxy_endpoint(endpoint_path):
    """Decorador para hacer proxy automático de endpoints"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Si está en modo proxy, hacer proxy
            if MODO_PROXY:
                # Construir endpoint con parámetros de ruta
                endpoint = endpoint_path
                for key, value in kwargs.items():
                    endpoint = endpoint.replace(f'<{key}>', str(value))
                    endpoint = endpoint.replace(f'<path:{key}>', str(value))
                
                # Obtener método HTTP
                method = request.method
                
                # Obtener datos según el método
                data = None
                if method in ['POST', 'PUT']:
                    if request.is_json:
                        data = request.get_json()
                    else:
                        data = request.form.to_dict()
                
                # Hacer proxy
                resultado = hacer_proxy(endpoint, method, data, request.args, request.files)
                if resultado:
                    return jsonify(resultado)
                return jsonify({"success": False, "error": "No se pudo conectar al NUC"}), 503
            
            # Modo local: ejecutar función normal
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

# ============================================
# CONFIGURACIÓN
# ============================================
# Credenciales de cámaras (se obtienen de config.py o variables de entorno)
USUARIO = USUARIO_CAMARAS if USAR_CONFIG_FILE else os.getenv('USUARIO_CAMARAS', 'admin')
CONTRASENA = CONTRASENA_CAMARAS if USAR_CONFIG_FILE else os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')
CARPETA_INTRUSOS = r"C:\Users\Administrator\Desktop\deteccion_sospechosa"
CARPETA_INTRUSOS_ALT = r"C:\Users\Administrator\Desktop\acceso\deteccion_sospechosa"
CARPETA_VIDEOS = r"C:\Users\Administrator\Desktop\videos_intrusion"
CARPETA_CONFIG = r"C:\Users\Administrator\Desktop\acceso"

def get_archivo_config(ip_camara=None):
    """Obtiene el archivo de configuración para una cámara específica"""
    if ip_camara:
        # Reemplazar puntos por guiones bajos para el nombre del archivo
        ip_safe = ip_camara.replace('.', '_')
        return os.path.join(CARPETA_CONFIG, f"config_cercas_{ip_safe}.json")
    else:
        # Archivo por defecto (compatibilidad)
        return os.path.join(CARPETA_CONFIG, "config_cercas.json")

# Cache de cámaras detectadas
camaras_cache = []
ultimo_escaneo = None

# ============================================
# FUNCIONES DE DETECCIÓN DE CÁMARAS
# ============================================

def obtener_red_local():
    """Detecta la red local del PC"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        partes = ip_local.split('.')
        red = f"{partes[0]}.{partes[1]}.{partes[2]}."
        return ip_local, red
    except:
        return None, "192.168.1."

def escanear_puerto(ip, puerto, timeout=0.3):
    """Verifica si un puerto está abierto"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultado = sock.connect_ex((ip, puerto))
        sock.close()
        return resultado == 0
    except:
        return False

def probar_rtsp(ip, usuario, contrasena, timeout=3):
    """Intenta conectarse a una cámara por RTSP"""
    urls = [
        f"rtsp://{usuario}:{contrasena}@{ip}:554/Streaming/Channels/101",
        f"rtsp://{usuario}:{contrasena}@{ip}:554/Streaming/Channels/1",
        f"rtsp://{usuario}:{contrasena}@{ip}:554/h264/ch1/main/av_stream",
    ]
    
    for url in urls:
        try:
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = f"timeout;{timeout*1000000}"
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, timeout*1000)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    alto, ancho = frame.shape[:2]
                    cap.release()
                    return True, url, f"{ancho}x{alto}"
                cap.release()
        except:
            pass
    
    return False, None, None

def escanear_ip(args):
    """Escanea una IP específica"""
    ip, puertos_camara = args
    puertos_abiertos = []
    
    for puerto, nombre in puertos_camara.items():
        if escanear_puerto(ip, puerto, timeout=0.3):
            puertos_abiertos.append({"puerto": puerto, "nombre": nombre})
    
    if puertos_abiertos:
        return {"ip": ip, "puertos": puertos_abiertos}
    return None

# ============================================
# ENDPOINTS API
# ============================================

@app.route('/api/status', methods=['GET'])
def status():
    """Estado del servidor"""
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "modo": "proxy" if MODO_PROXY else "local",
        "nucs_disponibles": len(NUCs) if MODO_PROXY else 0
    })

@app.route('/api/nucs', methods=['GET'])
def listar_nucs():
    """Lista los NUCs disponibles"""
    if not MODO_PROXY:
        return jsonify({
            "success": True,
            "modo": "local",
            "nucs": []
        })
    
    nucs_info = []
    for nombre, url in NUCs.items():
        # Verificar si el NUC está disponible
        disponible = False
        error_msg = None
        try:
            print(f"🔍 Probando conectividad a NUC: {url}/api/status")
            if TAILSCALE_PROXY:
                print(f"   Usando proxy SOCKS5 para conexión a través de Tailscale")
            response = requests.get(f"{url}/api/status", timeout=10, proxies=TAILSCALE_PROXY if TAILSCALE_PROXY else None)
            disponible = response.status_code == 200
            if disponible:
                print(f"✅ NUC {nombre} está disponible")
            else:
                error_msg = f"Status code: {response.status_code}"
                print(f"⚠️ NUC {nombre} responde con status {response.status_code}")
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout: {str(e)}"
            print(f"⏱️ Timeout al conectar con NUC {nombre}: {url}")
        except requests.exceptions.ConnectionError as e:
            error_msg = f"ConnectionError: {str(e)}"
            print(f"❌ Error de conexión con NUC {nombre}: {url} - {e}")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ Error inesperado con NUC {nombre}: {e}")
        
        nucs_info.append({
            "id": nombre,
            "url": url,
            "disponible": disponible,
            "error": error_msg
        })
    
    return jsonify({
        "success": True,
        "modo": "proxy",
        "nucs": nucs_info,
        "total": len(nucs_info)
    })

@app.route('/api/test/nuc', methods=['GET'])
def test_conectividad_nuc():
    """Endpoint de prueba para verificar conectividad al NUC"""
    if not MODO_PROXY:
        return jsonify({
            "success": False,
            "error": "No está en modo proxy"
        }), 400
    
    resultados = []
    for nombre, url in NUCs.items():
        resultado = {
            "nuc": nombre,
            "url": url,
            "tests": {}
        }
        
        # Test 1: Status endpoint
        try:
            print(f"🔍 [TEST] Probando: {url}/api/status")
            print(f"   Railway Tailscale IP: Verificando...")
            if TAILSCALE_PROXY:
                print(f"   Usando proxy SOCKS5: {TAILSCALE_PROXY}")
            # Intentar con timeout más largo y verificar conectividad
            # Usar proxy si está disponible (Tailscale userspace-networking)
            response = requests.get(f"{url}/api/status", timeout=30, proxies=TAILSCALE_PROXY if TAILSCALE_PROXY else None)
            resultado["tests"]["status"] = {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else response.text[:200]
            }
        except requests.exceptions.Timeout:
            resultado["tests"]["status"] = {
                "success": False,
                "error": "Timeout después de 10 segundos"
            }
            print(f"⏱️ [TEST] Timeout al conectar con {url}")
        except requests.exceptions.ConnectionError as e:
            resultado["tests"]["status"] = {
                "success": False,
                "error": f"ConnectionError: {str(e)}"
            }
            print(f"❌ [TEST] Error de conexión con {url}: {e}")
        except Exception as e:
            resultado["tests"]["status"] = {
                "success": False,
                "error": f"Error: {str(e)}"
            }
            print(f"❌ [TEST] Error inesperado con {url}: {e}")
        
        resultados.append(resultado)
    
    return jsonify({
        "success": True,
        "resultados": resultados
    })

@app.route('/api/ip', methods=['GET'])
def obtener_ip():
    """Obtiene todas las IPs del servidor (local, pública, VPN)"""
    import subprocess
    import requests
    
    ips = {
        "local": None,
        "publica": None,
        "tailscale": None,
        "zerotier": None,
        "wireguard": None
    }
    
    # IP Local
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips["local"] = s.getsockname()[0]
        s.close()
    except:
        pass
    
    # IP Pública
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        ips["publica"] = response.text.strip()
    except:
        try:
            response = requests.get("https://ifconfig.me", timeout=5)
            ips["publica"] = response.text.strip()
        except:
            pass
    
    # Tailscale
    try:
        result = subprocess.run(['tailscale', 'ip', '-4'], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            ips["tailscale"] = result.stdout.strip()
    except:
        pass
    
    # ZeroTier
    try:
        result = subprocess.run(['zerotier-cli', 'listnetworks'], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            # Buscar IP en la salida
            for line in result.stdout.split('\n'):
                if '10.' in line or '172.' in line:
                    parts = line.split()
                    for part in parts:
                        if '.' in part and part.count('.') == 3:
                            ips["zerotier"] = part.split('/')[0]
                            break
    except:
        pass
    
    # WireGuard
    try:
        result = subprocess.run(['wg', 'show'], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0 and 'interface' in result.stdout:
            # Extraer IP de la interfaz
            for line in result.stdout.split('\n'):
                if 'inet' in line:
                    ips["wireguard"] = line.split()[2].split('/')[0]
                    break
    except:
        pass
    
    # IP recomendada (prioridad: Tailscale > ZeroTier > Local > Pública)
    ip_recomendada = (
        ips["tailscale"] or 
        ips["zerotier"] or 
        ips["local"] or 
        ips["publica"]
    )
    
    return jsonify({
        "success": True,
        "ips": ips,
        "ip_recomendada": ip_recomendada,
        "url_recomendada": f"http://{ip_recomendada}:5000" if ip_recomendada else None,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/camaras/detectar', methods=['GET'])
def detectar_camaras():
    """Detecta cámaras en la red local"""
    # Si está en modo proxy, hacer proxy al NUC
    if MODO_PROXY:
        # Si hay IPs configuradas, usarlas directamente (más rápido)
        if CAMARAS_CONFIGURADAS:
            camaras_activas = []
            for i, ip in enumerate(CAMARAS_CONFIGURADAS):
                # Verificar si la cámara está accesible usando el puente genérico
                nuc_url = seleccionar_nuc(ip_camara=ip)
                if nuc_url:
                    try:
                        # Probar acceso a la cámara a través del puente
                        test_url = f"{nuc_url}/proxy/{ip}:554/stream"
                        response = requests.get(test_url, timeout=2)
                        estado = "activa" if response.status_code == 200 else "sin_acceso"
                    except:
                        estado = "sin_acceso"
                else:
                    estado = "sin_nuc"
                
                camaras_activas.append({
                    "id": i + 1,
                    "ip": ip,
                    "url": f"rtsp://{USUARIO}:{CONTRASENA}@{ip}:554/Streaming/Channels/101",
                    "resolucion": None,
                    "puertos": [{"puerto": 554, "nombre": "RTSP"}],
                    "estado": estado,
                    "nombre": f"Cámara {i + 1}",
                    "configurada": True
                })
            
            return jsonify({
                "success": True,
                "modo": "configurado",
                "camaras": camaras_activas,
                "total": len(camaras_activas),
                "timestamp": datetime.now().isoformat()
            })
        
        # Si no hay IPs configuradas, hacer proxy al NUC para escaneo
        nuc_id = request.args.get('nuc_id', None)
        resultado = hacer_proxy('/api/camaras/detectar', 'GET', params=request.args, nuc_id=nuc_id)
        if resultado:
            return jsonify(resultado)
        return jsonify({"success": False, "error": "No se pudo conectar al NUC"}), 503
    
    # Modo local: usar IPs configuradas o escanear
    global camaras_cache, ultimo_escaneo
    
    # Si hay IPs configuradas, usarlas directamente
    if CAMARAS_CONFIGURADAS:
        camaras_activas = []
        for i, ip in enumerate(CAMARAS_CONFIGURADAS):
            # Probar conexión RTSP
            exito, url, resolucion = probar_rtsp(ip, USUARIO, CONTRASENA)
            
            camaras_activas.append({
                "id": i + 1,
                "ip": ip,
                "url": url if exito else None,
                "resolucion": resolucion if exito else None,
                "puertos": [{"puerto": 554, "nombre": "RTSP"}] if exito else [],
                "estado": "activa" if exito else "sin_acceso",
                "nombre": f"Cámara {i + 1}",
                "configurada": True
            })
        
        camaras_cache = camaras_activas
        ultimo_escaneo = datetime.now().isoformat()
        
        return jsonify({
            "success": True,
            "modo": "configurado",
            "camaras": camaras_activas,
            "total": len(camaras_activas),
            "timestamp": ultimo_escaneo
        })
    
    # Si no hay IPs configuradas, escanear la red (lógica original)
    ip_local, red = obtener_red_local()
    
    puertos_camara = {
        554: "RTSP",
        80: "HTTP",
        8000: "SDK Hikvision",
        443: "HTTPS"
    }
    
    # Paso 1: Escanear dispositivos
    args_list = [(f"{red}{i}", puertos_camara) for i in range(1, 255)]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        resultados = list(executor.map(escanear_ip, args_list))
    
    dispositivos = [r for r in resultados if r is not None]
    
    # Paso 2: Probar conexión RTSP
    camaras_activas = []
    
    for disp in dispositivos:
        tiene_rtsp = any(p["puerto"] == 554 for p in disp["puertos"])
        if tiene_rtsp:
            exito, url, resolucion = probar_rtsp(disp["ip"], USUARIO, CONTRASENA)
            
            if exito:
                camaras_activas.append({
                    "id": len(camaras_activas) + 1,
                    "ip": disp["ip"],
                    "url": url,
                    "resolucion": resolucion,
                    "puertos": disp["puertos"],
                    "estado": "activa",
                    "nombre": f"Cámara {len(camaras_activas) + 1}",
                    "configurada": False
                })
            else:
                camaras_activas.append({
                    "id": len(camaras_activas) + 1,
                    "ip": disp["ip"],
                    "url": None,
                    "resolucion": None,
                    "puertos": disp["puertos"],
                    "estado": "sin_acceso",
                    "nombre": f"Cámara {len(camaras_activas) + 1}",
                    "configurada": False
                })
    
    camaras_cache = camaras_activas
    ultimo_escaneo = datetime.now().isoformat()
    
    return jsonify({
        "success": True,
        "modo": "escaneo",
        "ip_local": ip_local,
        "red": f"{red}0/24",
        "total_dispositivos": len(dispositivos),
        "camaras": camaras_activas,
        "timestamp": ultimo_escaneo
    })

@app.route('/api/camaras', methods=['GET'])
def obtener_camaras():
    """Obtiene las cámaras del cache"""
    return jsonify({
        "success": True,
        "camaras": camaras_cache,
        "ultimo_escaneo": ultimo_escaneo
    })

@app.route('/api/camaras/configuradas', methods=['GET'])
def obtener_camaras_configuradas():
    """Obtiene la lista de IPs de cámaras configuradas"""
    camaras_info = []
    for ip in CAMARAS_CONFIGURADAS:
        info = obtener_info_camara(ip) if USAR_CONFIG_FILE else {'nombre': f'Cámara {ip}'}
        camaras_info.append({
            'ip': ip,
            'nombre': info.get('nombre', f'Cámara {ip}'),
            'nuc': info.get('nuc')
        })
    
    return jsonify({
        "success": True,
        "camaras_configuradas": CAMARAS_CONFIGURADAS,
        "camaras_detalladas": camaras_info,
        "total": len(CAMARAS_CONFIGURADAS),
        "modo": "configurado" if CAMARAS_CONFIGURADAS else "automatico",
        "usando_config_file": USAR_CONFIG_FILE
    })

@app.route('/api/configuracion', methods=['GET'])
def obtener_configuracion_completa():
    """Obtiene la configuración completa (NUCs y cámaras)"""
    if USAR_CONFIG_FILE:
        try:
            resumen = obtener_resumen_config()
            return jsonify({
                "success": True,
                "usando_config_file": True,
                **resumen
            })
        except:
            pass
    
    # Si no usa config.py, retornar información básica
    return jsonify({
        "success": True,
        "usando_config_file": False,
        "nucs": {
            "total": len(NUCs),
            "nucs": [{"id": nombre, "url": url} for nombre, url in NUCs.items()]
        },
        "camaras": {
            "total": len(CAMARAS_CONFIGURADAS),
            "configuradas": CAMARAS_CONFIGURADAS
        },
        "modo": "variables_entorno"
    })

@app.route('/api/camaras/<ip>/snapshot', methods=['GET'])
def snapshot_camara(ip):
    """Captura una imagen de la cámara"""
    # Si está en modo proxy, usar puente genérico directamente
    if MODO_PROXY:
        nuc_url = seleccionar_nuc(ip_camara=ip)
        if nuc_url:
            try:
                # Usar el endpoint /api/camaras/<ip>/snapshot del puente genérico
                # Este endpoint procesa el snapshot usando OpenCV en el NUC
                snapshot_url = f"{nuc_url}/api/camaras/{ip}/snapshot"
                print(f"📸 Obteniendo snapshot desde NUC: {snapshot_url}")
                if TAILSCALE_PROXY:
                    print(f"   Usando proxy SOCKS5 para conexión a través de Tailscale")
                
                # Timeout aumentado para dar más tiempo a través de Tailscale
                # Usar proxy si está disponible (Tailscale userspace-networking)
                response = requests.get(snapshot_url, timeout=30, proxies=TAILSCALE_PROXY if TAILSCALE_PROXY else None)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get('success') and data.get('image'):
                            # Retornar directamente la respuesta del puente genérico
                            return jsonify(data)
                        else:
                            print(f"⚠️ Respuesta del NUC sin imagen: {data}")
                            return jsonify(data), response.status_code
                    except ValueError:
                        # Si no es JSON, retornar el contenido tal cual
                        return Response(response.content, mimetype=response.headers.get('Content-Type', 'application/json'))
                else:
                    print(f"❌ Error del NUC: {response.status_code} - {response.text}")
                    return jsonify({
                        "success": False,
                        "error": f"Error del NUC: {response.status_code}"
                    }), response.status_code
                    
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout al conectar con NUC: {nuc_url}")
                print(f"   Detalles: Railway no pudo conectarse a {nuc_url} en 15 segundos")
                print(f"   Verifica:")
                print(f"   1. Que el puente genérico esté corriendo en el NUC")
                print(f"   2. Que Railway y NUC estén online en Tailscale")
                print(f"   3. Que el firewall del NUC permita conexiones en puerto 5000")
                return jsonify({
                    "success": False,
                    "error": "Timeout al conectar con el NUC. Verifica que el puente genérico esté corriendo.",
                    "nuc_url": nuc_url,
                    "detalles": "Railway no pudo conectarse al NUC a través de Tailscale"
                }), 504
            except requests.exceptions.ConnectionError as e:
                print(f"❌ Error de conexión con NUC: {e}")
                print(f"   Detalles: Railway no puede alcanzar {nuc_url}")
                print(f"   Verifica:")
                print(f"   1. Que Railway y NUC estén online en Tailscale")
                print(f"   2. Que el puente genérico esté corriendo en el NUC")
                print(f"   3. Que el firewall del NUC permita conexiones en puerto 5000")
                return jsonify({
                    "success": False,
                    "error": f"No se pudo conectar al NUC en {nuc_url}. Verifica Tailscale y que el puente esté corriendo.",
                    "nuc_url": nuc_url,
                    "detalles": str(e)
                }), 503
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        return jsonify({
            "success": False,
            "error": "No hay NUCs disponibles para esta cámara"
        }), 503
    
    # Modo local: ejecutar lógica normal
    urls = [
        f"rtsp://{USUARIO}:{CONTRASENA}@{ip}:554/Streaming/Channels/101",
        f"rtsp://{USUARIO}:{CONTRASENA}@{ip}:554/Streaming/Channels/1",
    ]
    
    for url in urls:
        try:
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    # Convertir a JPEG
                    _, buffer = cv2.imencode('.jpg', frame)
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
                    return jsonify({
                        "success": True,
                        "image": f"data:image/jpeg;base64,{img_base64}",
                        "timestamp": datetime.now().isoformat()
                    })
        except:
            pass
    
    return jsonify({"success": False, "error": "No se pudo capturar imagen"})

def generar_frames(ip):
    """Generador de frames para streaming MJPEG"""
    urls = [
        f"rtsp://{USUARIO}:{CONTRASENA}@{ip}:554/Streaming/Channels/101",
        f"rtsp://{USUARIO}:{CONTRASENA}@{ip}:554/Streaming/Channels/1",
    ]
    
    cap = None
    for url in urls:
        try:
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            if cap.isOpened():
                break
        except:
            continue
    
    if not cap or not cap.isOpened():
        # Enviar imagen de error
        error_img = crear_imagen_error("No se pudo conectar a la cámara")
        _, buffer = cv2.imencode('.jpg', error_img)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        return
    
    streams_activos[ip] = True
    
    try:
        while streams_activos.get(ip, False):
            ret, frame = cap.read()
            if not ret:
                # Reconectar si falla
                cap.release()
                time.sleep(0.5)
                cap = cv2.VideoCapture(urls[0], cv2.CAP_FFMPEG)
                continue
            
            # Redimensionar para mejor rendimiento (720p)
            altura, ancho = frame.shape[:2]
            if ancho > 1280:
                escala = 1280 / ancho
                nuevo_ancho = 1280
                nuevo_alto = int(altura * escala)
                frame = cv2.resize(frame, (nuevo_ancho, nuevo_alto))
            
            # Agregar timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"IP: {ip}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (0, 255, 255), 1)
            
            # Convertir a JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.033)  # ~30 FPS
    finally:
        cap.release()
        streams_activos.pop(ip, None)

def crear_imagen_error(mensaje):
    """Crea una imagen con un mensaje de error"""
    img = cv2.imread(None) if False else None
    import numpy as np
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = (30, 30, 40)
    cv2.putText(img, mensaje, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (0, 0, 255), 2)
    return img

@app.route('/api/camaras/<ip>/stream')
def stream_camara(ip):
    """Stream MJPEG de la cámara"""
    return Response(
        generar_frames(ip),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/api/camaras/<ip>/stream/stop', methods=['POST'])
def detener_stream(ip):
    """Detiene el stream de una cámara"""
    streams_activos[ip] = False
    return jsonify({"success": True, "message": f"Stream de {ip} detenido"})

# ============================================
# ENDPOINTS DE CONFIGURACIÓN DE CERCAS (POR CÁMARA)
# ============================================

@app.route('/api/cercas/<ip_camara>', methods=['GET'])
def obtener_cercas(ip_camara):
    """Obtiene la configuración de cercas para una cámara específica"""
    # Si está en modo proxy, hacer proxy al NUC
    if MODO_PROXY:
        nuc_id = request.args.get('nuc_id', None)
        resultado = hacer_proxy(f'/api/cercas/{ip_camara}', 'GET', params=request.args, ip_camara=ip_camara, nuc_id=nuc_id)
        if resultado:
            return jsonify(resultado)
        return jsonify({"success": False, "error": "No se pudo conectar al NUC"}), 503
    
    # Modo local: ejecutar lógica normal
    try:
        archivo_config = get_archivo_config(ip_camara)
        
        if os.path.exists(archivo_config):
            with open(archivo_config, 'r') as f:
                data = json.load(f)
                
            # Formatear datos para la app
            lineas_formateadas = []
            colores = ["Amarillo", "Naranja", "Magenta", "Cyan", "Verde", "Rojo", "Azul"]
            
            for linea in data.get('lineas', []):
                lineas_formateadas.append({
                    "x1": linea[0],
                    "y1": linea[1],
                    "x2": linea[2],
                    "y2": linea[3],
                    "nombre": linea[4],
                    "color": colores[linea[5] % len(colores)],
                    "color_index": linea[5],
                    "activa": True
                })
            
            return jsonify({
                "success": True,
                "cercas": lineas_formateadas,
                "total": len(lineas_formateadas),
                "camara": ip_camara
            })
        else:
            return jsonify({
                "success": True,
                "cercas": [],
                "total": 0,
                "camara": ip_camara
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/cercas/<ip_camara>', methods=['POST'])
def guardar_cercas(ip_camara):
    """Guarda la configuración de cercas para una cámara específica"""
    try:
        data = request.json
        lineas = data.get('lineas', [])
        
        # Convertir al formato del script Python
        lineas_python = []
        for linea in lineas:
            lineas_python.append([
                linea['x1'],
                linea['y1'],
                linea['x2'],
                linea['y2'],
                linea['nombre'],
                linea.get('color_index', 0)
            ])
        
        config = {
            "lineas": lineas_python,
            "camara": ip_camara
        }
        
        archivo_config = get_archivo_config(ip_camara)
        
        with open(archivo_config, 'w') as f:
            json.dump(config, f, indent=2)
        
        return jsonify({
            "success": True,
            "message": f"Guardadas {len(lineas)} cercas para cámara {ip_camara}",
            "archivo": archivo_config
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/cercas/<ip_camara>/<nombre>', methods=['DELETE'])
def eliminar_cerca(ip_camara, nombre):
    """Elimina una cerca específica de una cámara"""
    try:
        archivo_config = get_archivo_config(ip_camara)
        
        if os.path.exists(archivo_config):
            with open(archivo_config, 'r') as f:
                data = json.load(f)
            
            lineas = data.get('lineas', [])
            lineas = [l for l in lineas if l[4] != nombre]
            
            with open(archivo_config, 'w') as f:
                json.dump({"lineas": lineas, "camara": ip_camara}, f, indent=2)
            
            return jsonify({"success": True, "message": f"Cerca {nombre} eliminada de cámara {ip_camara}"})
        
        return jsonify({"success": False, "error": "Archivo de configuración no encontrado"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Endpoint para listar todas las configuraciones de cercas
@app.route('/api/cercas', methods=['GET'])
def listar_todas_cercas():
    """Lista todas las configuraciones de cercas de todas las cámaras"""
    try:
        configuraciones = []
        
        if os.path.exists(CARPETA_CONFIG):
            for archivo in os.listdir(CARPETA_CONFIG):
                if archivo.startswith('config_cercas_') and archivo.endswith('.json'):
                    ruta = os.path.join(CARPETA_CONFIG, archivo)
                    with open(ruta, 'r') as f:
                        data = json.load(f)
                    
                    # Extraer IP del nombre del archivo
                    ip = archivo.replace('config_cercas_', '').replace('.json', '').replace('_', '.')
                    
                    configuraciones.append({
                        "camara": ip,
                        "total_cercas": len(data.get('lineas', [])),
                        "archivo": archivo
                    })
        
        return jsonify({
            "success": True,
            "configuraciones": configuraciones,
            "total_camaras": len(configuraciones)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ============================================
# ENDPOINTS DE IMÁGENES DE INTRUSOS
# ============================================

@app.route('/api/intrusos', methods=['GET'])
def obtener_intrusos():
    """Lista las imágenes de intrusos"""
    imagenes = []
    
    # Buscar en ambas carpetas
    carpetas = [CARPETA_INTRUSOS, CARPETA_INTRUSOS_ALT]
    
    for carpeta in carpetas:
        if os.path.exists(carpeta):
            for archivo in os.listdir(carpeta):
                if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                    ruta_completa = os.path.join(carpeta, archivo)
                    
                    # Extraer información del nombre
                    # Formato: ALERTA_LINEA_X_YYYYMMDD_HHMMSS.jpg
                    partes = archivo.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
                    
                    try:
                        # Intentar parsear fecha y hora
                        if len(partes) >= 4:
                            fecha_str = partes[-2]  # YYYYMMDD
                            hora_str = partes[-1]   # HHMMSS
                            linea = '_'.join(partes[1:-2])  # LINEA_X o LINEA_INFERIOR
                            
                            fecha = f"{fecha_str[:4]}-{fecha_str[4:6]}-{fecha_str[6:]}"
                            hora = f"{hora_str[:2]}:{hora_str[2:4]}:{hora_str[4:]}"
                        else:
                            fecha = "Desconocida"
                            hora = "Desconocida"
                            linea = "Desconocida"
                    except:
                        fecha = "Desconocida"
                        hora = "Desconocida"
                        linea = "Desconocida"
                    
                    # Obtener tamaño del archivo
                    tamano = os.path.getsize(ruta_completa)
                    modificado = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
                    
                    imagenes.append({
                        "id": len(imagenes) + 1,
                        "archivo": archivo,
                        "ruta": ruta_completa,
                        "carpeta": carpeta,
                        "fecha": fecha,
                        "hora": hora,
                        "linea": linea,
                        "tamano": tamano,
                        "modificado": modificado.isoformat()
                    })
    
    # Ordenar por fecha de modificación (más reciente primero)
    imagenes.sort(key=lambda x: x['modificado'], reverse=True)
    
    return jsonify({
        "success": True,
        "imagenes": imagenes,
        "total": len(imagenes)
    })

@app.route('/api/intrusos/<path:archivo>', methods=['GET'])
def obtener_imagen(archivo):
    """Devuelve una imagen específica"""
    # Buscar en ambas carpetas
    carpetas = [CARPETA_INTRUSOS, CARPETA_INTRUSOS_ALT]
    
    for carpeta in carpetas:
        ruta = os.path.join(carpeta, archivo)
        if os.path.exists(ruta):
            return send_file(ruta, mimetype='image/jpeg')
    
    return jsonify({"success": False, "error": "Imagen no encontrada"}), 404

@app.route('/api/intrusos/<archivo>/base64', methods=['GET'])
def obtener_imagen_base64(archivo):
    """Devuelve una imagen en base64"""
    carpetas = [CARPETA_INTRUSOS, CARPETA_INTRUSOS_ALT]
    
    for carpeta in carpetas:
        ruta = os.path.join(carpeta, archivo)
        if os.path.exists(ruta):
            with open(ruta, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode('utf-8')
            return jsonify({
                "success": True,
                "image": f"data:image/jpeg;base64,{img_data}",
                "archivo": archivo
            })
    
    return jsonify({"success": False, "error": "Imagen no encontrada"})

@app.route('/api/intrusos/<archivo>', methods=['DELETE'])
def eliminar_imagen(archivo):
    """Elimina una imagen de intruso"""
    carpetas = [CARPETA_INTRUSOS, CARPETA_INTRUSOS_ALT]
    
    for carpeta in carpetas:
        ruta = os.path.join(carpeta, archivo)
        if os.path.exists(ruta):
            os.remove(ruta)
            return jsonify({"success": True, "message": f"Imagen {archivo} eliminada"})
    
    return jsonify({"success": False, "error": "Imagen no encontrada"})

# ============================================
# ENDPOINTS DE VIDEOS DE INTRUSIÓN
# ============================================

@app.route('/api/videos', methods=['GET'])
def obtener_videos():
    """Lista los videos de intrusión"""
    videos = []
    
    if os.path.exists(CARPETA_VIDEOS):
        for archivo in os.listdir(CARPETA_VIDEOS):
            if archivo.lower().endswith(('.mp4', '.avi', '.mov')):
                ruta_completa = os.path.join(CARPETA_VIDEOS, archivo)
                
                # Extraer información del nombre
                # Formato: VIDEO_LINEA_X_YYYYMMDD_HHMMSS.mp4
                partes = archivo.replace('.mp4', '').replace('.avi', '').replace('.mov', '').split('_')
                
                try:
                    if len(partes) >= 4:
                        fecha_str = partes[-2]
                        hora_str = partes[-1]
                        linea = '_'.join(partes[1:-2])
                        
                        fecha = f"{fecha_str[:4]}-{fecha_str[4:6]}-{fecha_str[6:]}"
                        hora = f"{hora_str[:2]}:{hora_str[2:4]}:{hora_str[4:]}"
                    else:
                        fecha = "Desconocida"
                        hora = "Desconocida"
                        linea = "Desconocida"
                except:
                    fecha = "Desconocida"
                    hora = "Desconocida"
                    linea = "Desconocida"
                
                # Obtener información del archivo
                tamano = os.path.getsize(ruta_completa)
                modificado = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
                
                videos.append({
                    "id": len(videos) + 1,
                    "archivo": archivo,
                    "ruta": ruta_completa,
                    "fecha": fecha,
                    "hora": hora,
                    "linea": linea,
                    "tamano": tamano,
                    "duracion": 5,  # 5 segundos
                    "modificado": modificado.isoformat()
                })
    
    # Ordenar por fecha (más reciente primero)
    videos.sort(key=lambda x: x['modificado'], reverse=True)
    
    return jsonify({
        "success": True,
        "videos": videos,
        "total": len(videos)
    })

@app.route('/api/videos/<path:archivo>', methods=['GET'])
def obtener_video(archivo):
    """Devuelve un video específico con soporte para range requests"""
    ruta = os.path.join(CARPETA_VIDEOS, archivo)
    if os.path.exists(ruta):
        return send_file(
            ruta, 
            mimetype='video/mp4',
            conditional=True,
            download_name=archivo,
            as_attachment=False
        )
    
    return jsonify({"success": False, "error": "Video no encontrado"}), 404

@app.route('/api/videos/<archivo>', methods=['DELETE'])
def eliminar_video(archivo):
    """Elimina un video de intrusión"""
    ruta = os.path.join(CARPETA_VIDEOS, archivo)
    if os.path.exists(ruta):
        os.remove(ruta)
        return jsonify({"success": True, "message": f"Video {archivo} eliminado"})
    
    return jsonify({"success": False, "error": "Video no encontrado"})

# ============================================
# EJECUTAR SCRIPTS EXTERNOS
# ============================================

@app.route('/api/ejecutar/detectar-camaras', methods=['POST'])
def ejecutar_detectar_camaras():
    """Ejecuta el script de detección de cámaras"""
    try:
        script_path = r"C:\Users\Administrator\Desktop\acceso\detectar_camaras_red.py"
        os.system(f'start cmd /k python "{script_path}"')
        return jsonify({"success": True, "message": "Script iniciado"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/ejecutar/configurar-cercas', methods=['POST'])
def ejecutar_configurar_cercas():
    """Ejecuta el script de configuración de cercas"""
    try:
        script_path = r"C:\Users\Administrator\Desktop\acceso\configurar_cercas.py"
        os.system(f'start cmd /k python "{script_path}"')
        return jsonify({"success": True, "message": "Configurador iniciado"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/ejecutar/vigilancia/<ip_camara>', methods=['POST'])
def ejecutar_vigilancia(ip_camara):
    """Ejecuta el script de vigilancia con detección para una cámara específica"""
    try:
        import subprocess
        
        # Matar procesos anteriores de camara_ligera
        try:
            subprocess.run(['taskkill', '/F', '/FI', 'WINDOWTITLE eq *Vigilancia*'], 
                          capture_output=True, timeout=5)
        except:
            pass
        
        script_path = r"C:\Users\Administrator\Desktop\acceso\camara_ligera.py"
        python_path = r"C:\Program Files\Python311\python.exe"
        
        # Ejecutar en una nueva ventana de comando con comillas escapadas correctamente
        cmd = f'start "Vigilancia-{ip_camara}" /min cmd /c ""{python_path}" "{script_path}" {ip_camara} & pause"'
        os.system(cmd)
        
        return jsonify({
            "success": True, 
            "message": f"Vigilancia iniciada para cámara {ip_camara}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/ejecutar/monitoreo', methods=['POST'])
def ejecutar_monitoreo():
    """Ejecuta el monitoreo múltiple de todas las cámaras"""
    try:
        import subprocess
        
        # Matar procesos anteriores de monitoreo
        try:
            subprocess.run(['taskkill', '/F', '/FI', 'WINDOWTITLE eq *Monitoreo*'], 
                          capture_output=True, timeout=5)
        except:
            pass
        
        script_path = r"C:\Users\Administrator\Desktop\acceso\monitoreo_camaras.py"
        python_path = r"C:\Program Files\Python311\python.exe"
        
        cmd = f'start "Monitoreo" cmd /c ""{python_path}" "{script_path}" & pause"'
        os.system(cmd)
        
        return jsonify({
            "success": True, 
            "message": "Monitoreo múltiple iniciado"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/ejecutar/monitoreo-cercas', methods=['POST'])
def ejecutar_monitoreo_cercas():
    """Ejecuta el monitoreo múltiple con cercas de detección"""
    try:
        import subprocess
        
        # Matar procesos anteriores
        try:
            subprocess.run(['taskkill', '/F', '/FI', 'WINDOWTITLE eq *Monitoreo*'], 
                          capture_output=True, timeout=5)
        except:
            pass
        
        script_path = r"C:\Users\Administrator\Desktop\acceso\monitoreo_camaras.py"
        python_path = r"C:\Program Files\Python311\python.exe"
        
        cmd = f'start "Monitoreo-Cercas" cmd /c ""{python_path}" "{script_path}" --con-cercas & pause"'
        os.system(cmd)
        
        return jsonify({
            "success": True, 
            "message": "Monitoreo con cercas iniciado"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    print("="*60)
    print("       SERVIDOR API - APPTELINK VISION")
    print("="*60)
    print(f"\nIniciando servidor en http://0.0.0.0:{port}")
    print("\nEndpoints disponibles:")
    print("  GET  /api/status              - Estado del servidor")
    print("  GET  /api/camaras/detectar    - Detectar cámaras")
    print("  GET  /api/camaras             - Listar cámaras")
    print("  GET  /api/camaras/<ip>/snapshot - Capturar imagen")
    print("  GET  /api/cercas              - Obtener cercas")
    print("  POST /api/cercas              - Guardar cercas")
    print("  GET  /api/intrusos            - Listar imágenes")
    print("  GET  /api/intrusos/<archivo>  - Obtener imagen")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

