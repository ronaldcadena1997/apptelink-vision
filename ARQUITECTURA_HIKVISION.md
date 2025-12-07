# 🎥 Arquitectura Hikvision - Cómo lo Hacen Ellos

## 📊 **Arquitectura de Hikvision**

Hikvision usa una arquitectura **híbrida** que combina:
1. **NVR local** (Network Video Recorder) en cada sitio
2. **Servidor central** (HikCentral/iVMS) en la nube o servidor
3. **Plataforma de conexión** (Hik-Connect) para conectar ambos

```
┌─────────────────────────────────┐
│  HikCentral / iVMS             │ ← Servidor Central (Cloud/Servidor)
│  (Gestión Centralizada)         │
└──────────────┬──────────────────┘
               │
               │ Hik-Connect Platform
               │ (Túnel/Relay)
               │
┌──────────────▼──────────────────┐
│  NVR Local                      │ ← En cada sitio (NUC en tu caso)
│  (Grabación Local)              │
│  - Almacena videos              │
│  - Procesa eventos              │
│  - Expone API local             │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  Cámaras IP                     │ ← Red Local
│  (RTSP/ONVIF)                   │
└─────────────────────────────────┘
```

---

## 🔑 **Características Clave de Hikvision**

### **1. NVR como Gateway Local**
- ✅ El NVR está **en cada sitio** (como tu NUC)
- ✅ El NVR **almacena videos localmente**
- ✅ El NVR **expone una API** para consultas
- ✅ El NVR se conecta **hacia afuera** (no necesita VPN entrante)

### **2. Hik-Connect Platform (Túnel Reverso)**
- ✅ El NVR **inicia la conexión** al servidor central
- ✅ Usa un **túnel persistente** (similar a WebSocket o TCP persistente)
- ✅ El servidor central puede **enviar comandos** al NVR
- ✅ El NVR **envía eventos y datos** al servidor

### **3. Servidor Central (HikCentral)**
- ✅ **No necesita VPN** para conectarse al NVR
- ✅ Solo **recibe conexiones** del NVR
- ✅ **Almacena metadatos** (no videos completos, solo eventos/snapshots)
- ✅ **Gestiona múltiples NVRs** de diferentes sitios

---

## 🎯 **Cómo Aplicar Esto a Tu Proyecto**

### **Arquitectura Recomendada (Estilo Hikvision):**

```
┌─────────────────────────────────┐
│  Backend + Frontend             │ ← Railway (Servidor Central)
│  (Flask + React)                │
│  - Almacena snapshots           │
│  - Gestiona múltiples NUCs     │
│  - Expone API para frontend    │
└──────────────┬──────────────────┘
               │
               │ HTTP/WebSocket (Túnel Reverso)
               │ El NUC inicia la conexión
               │
┌──────────────▼──────────────────┐
│  NUC Agent                      │ ← NUC Local (como NVR)
│  (puente_generico_nuc.py)       │
│  - Captura de cámaras           │
│  - Procesa eventos              │
│  - Se conecta al servidor       │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  Cámaras IP                     │ ← Red Local 192.168.60.x
│  (RTSP)                         │
└─────────────────────────────────┘
```

---

## 🚀 **Implementación: Arquitectura Hikvision-Style**

### **Opción 1: WebSocket Bidireccional (Más Similar a Hikvision)**

**Ventajas:**
- ✅ Conexión persistente (como Hik-Connect)
- ✅ Tiempo real
- ✅ El servidor puede enviar comandos al NUC
- ✅ El NUC puede enviar eventos inmediatamente

**Implementación:**

**1. Backend en Railway (servidor central):**
```python
# server_hikvision_style.py
from flask import Flask
from flask_socketio import SocketIO, emit
import redis

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Almacenamiento de snapshots
db = redis.from_url(os.getenv('REDIS_URL'))

# Conexiones activas de NUCs
nuc_connections = {}  # {nuc_id: socket_id}

@socketio.on('connect')
def handle_connect(auth):
    """NUC se conecta al servidor"""
    nuc_id = auth.get('nuc_id')
    nuc_connections[nuc_id] = request.sid
    print(f"✅ NUC conectado: {nuc_id}")
    emit('connected', {'status': 'ok'})

@socketio.on('snapshot')
def handle_snapshot(data):
    """NUC envía snapshot"""
    ip = data['ip']
    image = data['image']
    nuc_id = data['nuc_id']
    
    # Almacenar en Redis
    db.setex(f'snapshot:{ip}', 300, image)
    
    # Reenviar al frontend (broadcast)
    socketio.emit('snapshot_update', {
        'ip': ip,
        'image': image,
        'nuc_id': nuc_id
    })

@socketio.on('event')
def handle_event(data):
    """NUC envía evento (detección, alarma, etc.)"""
    # Procesar evento
    socketio.emit('event_update', data)

# Endpoint para que el servidor pida snapshot
@socketio.on('request_snapshot')
def request_snapshot(data):
    """Servidor pide snapshot al NUC"""
    nuc_id = data['nuc_id']
    ip = data['ip']
    
    if nuc_id in nuc_connections:
        socketio.emit('capture_snapshot', {
            'ip': ip
        }, room=nuc_connections[nuc_id])
```

**2. NUC Agent (se conecta al servidor):**
```python
# nuc_agent_hikvision_style.py
import socketio
import cv2
import base64
import time

# Conectar al servidor
sio = socketio.Client()
sio.connect(
    'https://apptelink-vision-production.up.railway.app',
    auth={'nuc_id': 'nuc_sede1'}
)

@sio.on('connected')
def on_connected(data):
    print("✅ Conectado al servidor central")

@sio.on('capture_snapshot')
def on_capture_request(data):
    """Servidor pide capturar snapshot"""
    ip = data['ip']
    snapshot = capturar_snapshot(ip)
    
    sio.emit('snapshot', {
        'ip': ip,
        'image': snapshot,
        'nuc_id': 'nuc_sede1'
    })

# Enviar snapshots periódicamente
def enviar_snapshots_periodicos():
    while True:
        for ip in ['192.168.60.65']:
            snapshot = capturar_snapshot(ip)
            sio.emit('snapshot', {
                'ip': ip,
                'image': snapshot,
                'nuc_id': 'nuc_sede1'
            })
        time.sleep(30)

# Mantener conexión viva
sio.wait()
```

---

### **Opción 2: HTTP con Heartbeat (Más Simple, Similar a Hikvision)**

**Ventajas:**
- ✅ Más simple que WebSocket
- ✅ Funciona con cualquier firewall
- ✅ El NUC inicia todas las conexiones

**Implementación:**

**1. Backend en Railway:**
```python
# server_hikvision_http.py
from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
db = redis.from_url(os.getenv('REDIS_URL'))

# Registro de NUCs conectados
nucs_activos = {}  # {nuc_id: last_heartbeat}

@app.route('/api/nuc/heartbeat', methods=['POST'])
def heartbeat():
    """NUC envía heartbeat (cada 30 segundos)"""
    data = request.get_json()
    nuc_id = data['nuc_id']
    nucs_activos[nuc_id] = time.time()
    return jsonify({'status': 'ok'})

@app.route('/api/nuc/snapshot', methods=['POST'])
def recibir_snapshot():
    """NUC envía snapshot"""
    data = request.get_json()
    ip = data['ip']
    image = data['image']
    nuc_id = data['nuc_id']
    
    db.setex(f'snapshot:{ip}', 300, image)
    return jsonify({'success': True})

@app.route('/api/nuc/event', methods=['POST'])
def recibir_evento():
    """NUC envía evento"""
    # Procesar evento
    return jsonify({'success': True})

# El servidor puede pedir datos haciendo polling
# o el NUC envía periódicamente
```

**2. NUC Agent:**
```python
# nuc_agent_hikvision_http.py
import requests
import time

RAILWAY_URL = "https://apptelink-vision-production.up.railway.app"
NUC_ID = "nuc_sede1"

def enviar_heartbeat():
    """Enviar heartbeat cada 30 segundos"""
    requests.post(
        f"{RAILWAY_URL}/api/nuc/heartbeat",
        json={'nuc_id': NUC_ID},
        timeout=5
    )

def enviar_snapshots():
    """Enviar snapshots periódicamente"""
    for ip in ['192.168.60.65']:
        snapshot = capturar_snapshot(ip)
        requests.post(
            f"{RAILWAY_URL}/api/nuc/snapshot",
            json={
                'nuc_id': NUC_ID,
                'ip': ip,
                'image': snapshot
            },
            timeout=10
        )

# Bucle principal
while True:
    enviar_heartbeat()
    enviar_snapshots()
    time.sleep(30)
```

---

## 📊 **Comparación: Hikvision vs Tu Proyecto**

| Característica | Hikvision | Tu Proyecto Actual | Recomendación |
|----------------|-----------|-------------------|---------------|
| **NVR Local** | ✅ Sí (hardware) | ✅ Sí (NUC software) | ✅ Mantener |
| **Conexión** | Túnel Hik-Connect | Tailscale VPN | ⚠️ Cambiar a HTTP/WebSocket |
| **Iniciador** | NVR → Servidor | Servidor → NUC | ✅ Cambiar: NUC → Servidor |
| **Almacenamiento** | Local + Cloud | Solo Cloud | ✅ Agregar local opcional |
| **Tiempo Real** | ✅ Sí | ⚠️ Con delay | ✅ Mejorar con WebSocket |

---

## 🎯 **Recomendación Final: Arquitectura Hikvision-Style**

### **Implementación Recomendada:**

1. **NUC Agent (en el NUC):**
   - Se conecta al servidor usando WebSocket o HTTP
   - Envía snapshots periódicamente
   - Envía eventos en tiempo real
   - Mantiene conexión persistente

2. **Backend en Railway:**
   - Recibe conexiones del NUC (no inicia conexiones)
   - Almacena snapshots en Redis/PostgreSQL
   - Expone API para el frontend
   - Puede enviar comandos al NUC vía WebSocket

3. **Frontend:**
   - Consulta al backend en Railway
   - Recibe actualizaciones en tiempo real (WebSocket)
   - No se conecta directamente al NUC

### **Ventajas:**
- ✅ **Simple:** No necesita Tailscale en Railway
- ✅ **Confiable:** El NUC inicia la conexión (más fácil de firewall)
- ✅ **Tiempo real:** Con WebSocket
- ✅ **Escalable:** Fácil agregar más NUCs
- ✅ **Similar a Hikvision:** Arquitectura probada

---

## 🚀 **Próximos Pasos**

¿Quieres que implemente la arquitectura estilo Hikvision?

Puedo crear:
1. ✅ Backend con WebSocket (estilo Hik-Connect)
2. ✅ NUC Agent que se conecta al servidor
3. ✅ Sistema de heartbeat y reconexión automática
4. ✅ Almacenamiento local opcional en el NUC

**¿Cuál prefieres?**
