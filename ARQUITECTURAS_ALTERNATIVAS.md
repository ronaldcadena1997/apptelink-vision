# 🏗️ Arquitecturas Alternativas para el Proyecto

## 📊 **Arquitectura Actual (Con Problemas)**

```
┌─────────────────┐
│  Frontend       │ ← Railway
│  (React/Expo)   │
└────────┬────────┘
         │ HTTP
┌────────▼────────┐
│  Backend API    │ ← Railway (con Tailscale userspace-networking)
│  (Flask)        │    Problema: Complejo, proxy SOCKS5, timeouts
└────────┬────────┘
         │ Tailscale VPN
┌────────▼────────┐
│  NUC Bridge     │ ← NUC Local
│  (puente_gen)   │
└────────┬────────┘
         │ RTSP/HTTP Local
┌────────▼────────┐
│   Cámaras       │ ← Red Local 192.168.60.x
└─────────────────┘
```

**Problemas:**
- ❌ Tailscale en Railway es complejo (userspace-networking, proxy SOCKS5)
- ❌ Timeouts y problemas de conectividad
- ❌ Configuración complicada
- ❌ Dependencia de VPN en el servidor

---

## 🎯 **Arquitectura Alternativa 1: Polling/Webhook (RECOMENDADA)**

### **Descripción:**
El NUC envía datos periódicamente al backend en Railway. No necesita Tailscale en Railway.

```
┌─────────────────┐
│  Frontend       │ ← Railway
│  (React/Expo)   │
└────────┬────────┘
         │ HTTP
┌────────▼────────┐
│  Backend API    │ ← Railway (simple, sin VPN)
│  (Flask)        │    + Base de Datos (PostgreSQL/Redis)
└────────┬────────┘
         │ HTTP POST (Polling cada 30s)
┌────────▼────────┐
│  NUC Agent      │ ← NUC Local
│  (envía datos)  │    Solo necesita salida HTTP (no VPN)
└────────┬────────┘
         │ RTSP/HTTP Local
┌────────▼────────┐
│   Cámaras       │ ← Red Local
└─────────────────┘
```

### **Ventajas:**
- ✅ **Simple:** No necesita Tailscale en Railway
- ✅ **Confiable:** El NUC solo necesita salida HTTP (más fácil que VPN)
- ✅ **Escalable:** Fácil agregar más NUCs
- ✅ **Sin problemas de conectividad:** El NUC inicia la conexión

### **Desventajas:**
- ⚠️ **No es tiempo real:** Hay un delay de 30-60 segundos
- ⚠️ **Requiere base de datos:** Para almacenar snapshots/estado

### **Implementación:**

**1. Backend en Railway (simple):**
```python
# server.py
from flask import Flask, jsonify
import redis  # o PostgreSQL

app = Flask(__name__)
db = redis.Redis(host='redis', port=6379)  # Railway Redis

@app.route('/api/camaras', methods=['GET'])
def listar_camaras():
    # Leer desde base de datos
    camaras = db.get('camaras') or []
    return jsonify(camaras)

@app.route('/api/camaras/<ip>/snapshot', methods=['POST'])
def recibir_snapshot(ip):
    # El NUC envía snapshots aquí
    snapshot = request.json['image']
    db.set(f'snapshot:{ip}', snapshot, ex=300)  # Expira en 5 min
    return jsonify({'success': True})
```

**2. NUC Agent (envía datos):**
```python
# nuc_agent.py (en el NUC)
import requests
import cv2
import time
import base64

RAILWAY_URL = "https://apptelink-vision-production.up.railway.app"

def enviar_snapshot(ip_camara):
    # Capturar imagen
    cap = cv2.VideoCapture(f"rtsp://admin:pass@{ip_camara}:554/...")
    ret, frame = cap.read()
    cap.release()
    
    # Convertir a base64
    _, buffer = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(buffer).decode()
    
    # Enviar al servidor
    requests.post(
        f"{RAILWAY_URL}/api/camaras/{ip_camara}/snapshot",
        json={'image': img_base64, 'timestamp': time.time()}
    )

# Bucle principal
while True:
    for ip in ['192.168.60.65']:
        enviar_snapshot(ip)
    time.sleep(30)  # Cada 30 segundos
```

---

## 🎯 **Arquitectura Alternativa 2: Túnel HTTP Reverso (ngrok/Cloudflare Tunnel)**

### **Descripción:**
El NUC expone su API públicamente usando un túnel HTTP. Railway hace requests HTTP normales.

```
┌─────────────────┐
│  Frontend       │ ← Railway
└────────┬────────┘
         │
┌────────▼────────┐
│  Backend API    │ ← Railway
└────────┬────────┘
         │ HTTP (público)
┌────────▼────────┐
│  ngrok/CF      │ ← Túnel HTTP (gratis)
│  Tunnel         │    Ej: https://abc123.ngrok.io
└────────┬────────┘
         │ HTTP Local
┌────────▼────────┐
│  NUC API        │ ← NUC Local
│  (puente_gen)   │
└────────┬────────┘
         │ RTSP Local
┌────────▼────────┐
│   Cámaras       │
└─────────────────┘
```

### **Ventajas:**
- ✅ **Muy simple:** Solo HTTP, sin VPN
- ✅ **Tiempo real:** Requests directos
- ✅ **Sin configuración compleja:** ngrok es muy fácil

### **Desventajas:**
- ⚠️ **URL pública:** Necesitas autenticación fuerte
- ⚠️ **Dependencia de servicio externo:** ngrok puede tener límites
- ⚠️ **URL cambia:** (a menos que uses plan de pago)

### **Implementación:**

**1. En el NUC:**
```bash
# Instalar ngrok
# Descargar de https://ngrok.com/download

# Exponer puerto 5000
ngrok http 5000

# Obtener URL: https://abc123.ngrok.io
```

**2. En Railway (Backend):**
```python
# server.py
NUC_URL = os.getenv('NUC_URL', 'https://abc123.ngrok.io')

@app.route('/api/camaras/<ip>/snapshot')
def snapshot_camara(ip):
    # Request directo al NUC vía ngrok
    response = requests.get(f"{NUC_URL}/api/camaras/{ip}/snapshot")
    return response.json()
```

---

## 🎯 **Arquitectura Alternativa 3: WebSocket Bidireccional**

### **Descripción:**
El NUC mantiene una conexión WebSocket persistente con Railway. Railway puede enviar comandos y recibir datos en tiempo real.

```
┌─────────────────┐
│  Frontend       │ ← Railway
└────────┬────────┘
         │
┌────────▼────────┐
│  Backend API    │ ← Railway
│  + WebSocket    │
└────────┬────────┘
         │ WebSocket (persistente)
┌────────▼────────┐
│  NUC Agent      │ ← NUC Local
│  (WebSocket)    │    Mantiene conexión abierta
└────────┬────────┘
         │ RTSP Local
┌────────▼────────┐
│   Cámaras       │
└─────────────────┘
```

### **Ventajas:**
- ✅ **Tiempo real:** Comunicación bidireccional instantánea
- ✅ **Eficiente:** Una sola conexión persistente
- ✅ **Sin polling:** El servidor puede pedir datos cuando quiera

### **Desventajas:**
- ⚠️ **Más complejo:** Requiere manejo de WebSocket
- ⚠️ **Reconexión:** Si se cae la conexión, necesita reconectar
- ⚠️ **Firewall:** Algunos firewalls bloquean WebSocket

### **Implementación:**

**1. Backend en Railway:**
```python
# server.py
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

nuc_connections = {}  # {nuc_id: socket_id}

@socketio.on('connect')
def handle_connect(auth):
    nuc_id = auth.get('nuc_id')
    nuc_connections[nuc_id] = request.sid
    emit('connected', {'status': 'ok'})

@socketio.on('snapshot')
def handle_snapshot(data):
    # El NUC envía snapshot
    ip = data['ip']
    image = data['image']
    # Guardar o reenviar al frontend
    socketio.emit('snapshot_update', {'ip': ip, 'image': image})
```

**2. NUC Agent:**
```python
# nuc_agent.py
import socketio

sio = socketio.Client()
sio.connect('https://apptelink-vision-production.up.railway.app',
           auth={'nuc_id': 'nuc_sede1'})

@sio.on('request_snapshot')
def on_snapshot_request(data):
    ip = data['ip']
    # Capturar y enviar
    snapshot = capturar_snapshot(ip)
    sio.emit('snapshot', {'ip': ip, 'image': snapshot})
```

---

## 🎯 **Arquitectura Alternativa 4: Base de Datos Compartida**

### **Descripción:**
El NUC escribe directamente a una base de datos (PostgreSQL/MongoDB). El backend solo lee de la base de datos.

```
┌─────────────────┐
│  Frontend       │ ← Railway
└────────┬────────┘
         │
┌────────▼────────┐
│  Backend API    │ ← Railway
│  (solo lectura) │
└────────┬────────┘
         │ SQL/NoSQL
┌────────▼────────┐
│  PostgreSQL/    │ ← Railway (o externa)
│  MongoDB        │
└────────┬────────┘
         │ SQL/NoSQL
┌────────▼────────┐
│  NUC Agent      │ ← NUC Local
│  (escribe)      │    Solo necesita salida SQL
└────────┬────────┘
         │ RTSP Local
┌────────▼────────┐
│   Cámaras       │
└─────────────────┘
```

### **Ventajas:**
- ✅ **Muy simple:** El backend solo lee, el NUC solo escribe
- ✅ **Desacoplado:** No hay comunicación directa
- ✅ **Escalable:** Múltiples NUCs pueden escribir a la misma DB

### **Desventajas:**
- ⚠️ **Requiere DB accesible:** El NUC necesita acceso a la base de datos
- ⚠️ **No es tiempo real:** Depende de la frecuencia de escritura
- ⚠️ **Seguridad:** Necesitas exponer la DB o usar VPN para el NUC

---

## 🎯 **Arquitectura Alternativa 5: Message Queue (RabbitMQ/Redis)**

### **Descripción:**
El NUC publica eventos a una cola de mensajes. El backend consume de la cola.

```
┌─────────────────┐
│  Frontend       │ ← Railway
└────────┬────────┘
         │
┌────────▼────────┐
│  Backend API    │ ← Railway
│  (consume)      │
└────────┬────────┘
         │ Consume
┌────────▼────────┐
│  RabbitMQ/      │ ← Railway (o CloudAMQP)
│  Redis Queue    │
└────────┬────────┘
         │ Publish
┌────────▼────────┐
│  NUC Agent      │ ← NUC Local
│  (publica)      │
└────────┬────────┘
         │ RTSP Local
┌────────▼────────┐
│   Cámaras       │
└─────────────────┘
```

### **Ventajas:**
- ✅ **Desacoplado:** NUC y Backend no se conocen
- ✅ **Escalable:** Múltiples consumidores
- ✅ **Confiabilidad:** Los mensajes se guardan si el backend está caído

### **Desventajas:**
- ⚠️ **Complejidad:** Requiere infraestructura adicional
- ⚠️ **Overhead:** Puede ser excesivo para un proyecto pequeño

---

## 📊 **Comparación de Arquitecturas**

| Arquitectura | Simplicidad | Tiempo Real | Escalabilidad | Costo | Recomendación |
|--------------|-------------|-------------|---------------|-------|---------------|
| **Actual (Tailscale)** | ⭐⭐ | ✅ | ⭐⭐⭐ | Gratis | ❌ No (muy complejo) |
| **Polling/Webhook** | ⭐⭐⭐⭐⭐ | ⚠️ (30s delay) | ⭐⭐⭐⭐ | Gratis | ✅ **SÍ (más simple)** |
| **Túnel HTTP (ngrok)** | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐ | Gratis/Pago | ✅ **SÍ (muy simple)** |
| **WebSocket** | ⭐⭐⭐ | ✅ | ⭐⭐⭐ | Gratis | ⚠️ Medio |
| **Base de Datos** | ⭐⭐⭐⭐ | ⚠️ | ⭐⭐⭐⭐ | Pago DB | ⚠️ Medio |
| **Message Queue** | ⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ | Pago | ❌ No (complejo) |

---

## 🎯 **Recomendación Final**

### **Para tu caso, recomiendo: Arquitectura 1 (Polling/Webhook)**

**Razones:**
1. ✅ **Más simple:** No necesita Tailscale en Railway
2. ✅ **Más confiable:** El NUC solo necesita salida HTTP (más fácil que VPN)
3. ✅ **Fácil de implementar:** Cambios mínimos en el código
4. ✅ **Escalable:** Fácil agregar más NUCs
5. ✅ **Gratis:** No requiere servicios adicionales

**Si necesitas tiempo real:** Usa **Arquitectura 2 (ngrok/Cloudflare Tunnel)**

---

## 🚀 **Próximos Pasos**

¿Quieres que implemente alguna de estas arquitecturas? Puedo:
1. Crear el código para la arquitectura de Polling/Webhook
2. Configurar ngrok en el NUC
3. Implementar WebSocket bidireccional
4. O cualquier otra que prefieras

**¿Cuál prefieres?**
