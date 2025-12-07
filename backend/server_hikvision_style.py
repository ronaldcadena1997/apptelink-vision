#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend Estilo Hikvision
=========================
Servidor central que recibe conexiones de NUCs (como HikCentral)
No necesita Tailscale, los NUCs se conectan al servidor.
Usa config.py para configuración de NUCs y cámaras.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
import time
from datetime import datetime
import redis

# Importar configuración centralizada
try:
    from config import (
        CAMARAS_CONFIGURADAS, CAMARAS_DICT, CAMARAS_CONFIG,
        obtener_info_camara, listar_camaras_por_nuc
    )
    USAR_CONFIG_FILE = True
except ImportError:
    USAR_CONFIG_FILE = False
    CAMARAS_CONFIGURADAS = []
    CAMARAS_DICT = {}

# ============================================
# CONFIGURACIÓN
# ============================================

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# WebSocket para comunicación en tiempo real
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=True,
    engineio_logger=True
)

# Base de datos (Redis)
try:
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    db = redis.from_url(REDIS_URL, decode_responses=True)
    print("✅ Conectado a Redis")
except:
    db = {}
    print("⚠️  Redis no disponible, usando memoria")

# Registro de NUCs conectados
nucs_conectados = {}  # {nuc_id: {'socket_id': ..., 'last_heartbeat': ..., 'camaras': [...]}}

# Tiempo de expiración
SNAPSHOT_EXPIRY = 300  # 5 minutos

# ============================================
# WEBSOCKET: CONEXIONES DE NUCS
# ============================================

@socketio.on('connect')
def handle_connect(auth):
    """NUC se conecta al servidor (como Hik-Connect)"""
    nuc_id = auth.get('nuc_id', 'unknown')
    
    nucs_conectados[nuc_id] = {
        'socket_id': request.sid,
        'last_heartbeat': time.time(),
        'camaras': [],
        'connected_at': datetime.now().isoformat()
    }
    
    print(f"✅ NUC conectado: {nuc_id} (Socket: {request.sid})")
    
    emit('connected', {
        'status': 'ok',
        'nuc_id': nuc_id,
        'message': 'Conectado al servidor central'
    })

@socketio.on('disconnect')
def handle_disconnect():
    """NUC se desconecta"""
    # Buscar y eliminar NUC desconectado
    for nuc_id, info in list(nucs_conectados.items()):
        if info['socket_id'] == request.sid:
            print(f"❌ NUC desconectado: {nuc_id}")
            del nucs_conectados[nuc_id]
            break

@socketio.on('nuc_register')
def handle_nuc_register(data):
    """NUC se registra con información de sus cámaras"""
    nuc_id = data.get('nuc_id')
    camaras = data.get('camaras', [])
    
    if nuc_id in nucs_conectados:
        nucs_conectados[nuc_id]['camaras'] = camaras
        print(f"📋 NUC {nuc_id} registrado con {len(camaras)} cámaras")
        
        emit('registered', {
            'status': 'ok',
            'nuc_id': nuc_id
        })

@socketio.on('snapshot')
def handle_snapshot(data):
    """NUC envía snapshot de una cámara"""
    try:
        nuc_id = data.get('nuc_id')
        ip = data.get('ip')
        image = data.get('image')
        estado = data.get('estado', 'activa')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        if not image:
            print(f"⚠️  Snapshot sin imagen recibido: {nuc_id} - {ip}")
            return
        
        # Validar que la imagen no esté vacía
        if len(image) < 100:  # Imagen muy pequeña, probablemente error
            print(f"⚠️  Snapshot con imagen inválida recibido: {nuc_id} - {ip}")
            return
        
        # Almacenar en Redis
        snapshot_data = {
            'nuc_id': nuc_id,
            'ip': ip,
            'image': image,
            'estado': estado,
            'timestamp': timestamp
        }
        
        try:
            if isinstance(db, dict):
                db[f'snapshot:{ip}'] = json.dumps(snapshot_data)
            else:
                db.setex(
                    f'snapshot:{ip}',
                    SNAPSHOT_EXPIRY,
                    json.dumps(snapshot_data)
                )
        except Exception as db_error:
            print(f"⚠️  Error al guardar en DB: {db_error}")
            # Continuar aunque falle la DB
        
        # Actualizar heartbeat
        if nuc_id in nucs_conectados:
            nucs_conectados[nuc_id]['last_heartbeat'] = time.time()
        
        # Reenviar al frontend (broadcast a todos los clientes web)
        try:
            socketio.emit('snapshot_update', {
                'nuc_id': nuc_id,
                'ip': ip,
                'image': image,
                'estado': estado,
                'timestamp': timestamp
            }, namespace='/', room=None)  # Broadcast a todos
        except Exception as emit_error:
            print(f"⚠️  Error al emitir snapshot: {emit_error}")
        
        print(f"📸 Snapshot recibido: {nuc_id} - {ip}")
        
    except Exception as e:
        print(f"❌ Error al procesar snapshot: {e}")
        import traceback
        traceback.print_exc()

@socketio.on('snapshot_error')
def handle_snapshot_error(data):
    """NUC reporta error al capturar snapshot"""
    nuc_id = data.get('nuc_id')
    ip = data.get('ip')
    error = data.get('error')
    
    # Almacenar estado de error
    estado_data = {
        'nuc_id': nuc_id,
        'ip': ip,
        'estado': 'sin_acceso',
        'error': error,
        'timestamp': datetime.now().isoformat()
    }
    
    if isinstance(db, dict):
        db[f'estado:{ip}'] = json.dumps(estado_data)
    else:
        db.setex(f'estado:{ip}', 600, json.dumps(estado_data))
    
    print(f"⚠️  Error en snapshot: {nuc_id} - {ip}: {error}")

@socketio.on('pong')
def handle_pong(data):
    """Respuesta a ping del servidor"""
    nuc_id = data.get('nuc_id')
    if nuc_id in nucs_conectados:
        nucs_conectados[nuc_id]['last_heartbeat'] = time.time()

@socketio.on('event')
def handle_event(data):
    """NUC envía evento (detección, alarma, etc.)"""
    # Procesar evento y reenviar al frontend
    socketio.emit('event_update', data)

# ============================================
# ENDPOINTS HTTP PARA EL FRONTEND
# ============================================

@app.route('/api/status', methods=['GET'])
def status():
    """Estado del servidor"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'arquitectura': 'hikvision-style',
        'nucs_conectados': len(nucs_conectados),
        'usar_config_file': USAR_CONFIG_FILE
    })

@app.route('/api/nucs', methods=['GET'])
def listar_nucs():
    """Lista todos los NUCs conectados"""
    nucs = []
    for nuc_id, info in nucs_conectados.items():
        nucs.append({
            'nuc_id': nuc_id,
            'conectado': True,
            'camaras': info.get('camaras', []),
            'connected_at': info.get('connected_at'),
            'last_heartbeat': info.get('last_heartbeat')
        })
    
    return jsonify({
        'success': True,
        'nucs': nucs,
        'total': len(nucs)
    })

@app.route('/api/camaras', methods=['GET'])
def listar_camaras():
    """Lista todas las cámaras de todos los NUCs"""
    camaras = []
    
    # Obtener de Redis
    if isinstance(db, dict):
        for key, value in db.items():
            if key.startswith('snapshot:'):
                ip = key.replace('snapshot:', '')
                data = json.loads(value)
                camaras.append({
                    'ip': ip,
                    'nuc_id': data.get('nuc_id'),
                    'estado': data.get('estado'),
                    'timestamp': data.get('timestamp'),
                    'tiene_snapshot': True
                })
    else:
        for key in db.scan_iter('snapshot:*'):
            ip = key.replace('snapshot:', '')
            data_str = db.get(key)
            if data_str:
                data = json.loads(data_str)
                camaras.append({
                    'ip': ip,
                    'nuc_id': data.get('nuc_id'),
                    'estado': data.get('estado'),
                    'timestamp': data.get('timestamp'),
                    'tiene_snapshot': True
                })
    
    return jsonify({
        'success': True,
        'camaras': camaras,
        'total': len(camaras)
    })

@app.route('/api/camaras/<ip>/snapshot', methods=['GET'])
def obtener_snapshot(ip):
    """Obtiene el último snapshot de una cámara"""
    try:
        if isinstance(db, dict):
            data_str = db.get(f'snapshot:{ip}')
        else:
            data_str = db.get(f'snapshot:{ip}')
        
        if not data_str:
            return jsonify({
                'success': False,
                'error': 'No hay snapshot disponible'
            }), 404
        
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear JSON del snapshot: {e}")
            return jsonify({
                'success': False,
                'error': 'Error al procesar snapshot'
            }), 500
        
        image = data.get('image')
        if not image:
            return jsonify({
                'success': False,
                'error': 'Snapshot sin imagen'
            }), 404
        
        return jsonify({
            'success': True,
            'ip': ip,
            'image': image,
            'estado': data.get('estado', 'activa'),
            'timestamp': data.get('timestamp')
        })
        
    except Exception as e:
        print(f"❌ Error en obtener_snapshot: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/camaras/detectar', methods=['GET'])
def detectar_camaras():
    """Detecta cámaras basándose en los datos recibidos y config.py"""
    camaras = []
    seen_ips = set()
    
    # Primero, obtener cámaras de config.py si está disponible
    if USAR_CONFIG_FILE and CAMARAS_CONFIGURADAS:
        for ip in CAMARAS_CONFIGURADAS:
            if ip in seen_ips:
                continue
            seen_ips.add(ip)
            
            info = obtener_info_camara(ip)
            
            # Verificar si hay snapshot en Redis
            if isinstance(db, dict):
                snapshot_data_str = db.get(f'snapshot:{ip}')
            else:
                snapshot_data_str = db.get(f'snapshot:{ip}')
            
            # Verificar estado
            if isinstance(db, dict):
                estado_data_str = db.get(f'estado:{ip}')
            else:
                estado_data_str = db.get(f'estado:{ip}')
            
            estado_data = json.loads(estado_data_str) if estado_data_str else None
            snapshot_data = json.loads(snapshot_data_str) if snapshot_data_str else None
            
            # Determinar estado
            if snapshot_data:
                estado = snapshot_data.get('estado', 'activa')
            elif estado_data:
                estado = estado_data.get('estado', 'sin_acceso')
            else:
                estado = 'sin_acceso'  # No hay datos aún
            
            camaras.append({
                'ip': ip,
                'nombre': info.get('nombre', f'Cámara {ip}'),
                'estado': estado,
                'configurada': True,
                'nuc_id': info.get('nuc') or snapshot_data.get('nuc_id') if snapshot_data else None
            })
    
    # También agregar cámaras que vienen de snapshots pero no están en config
    if isinstance(db, dict):
        for key in db.keys():
            if key.startswith('snapshot:'):
                ip = key.replace('snapshot:', '')
                if ip not in seen_ips:
                    seen_ips.add(ip)
                    data = json.loads(db[key])
                    camaras.append({
                        'ip': ip,
                        'nombre': f'Cámara {ip}',
                        'estado': data.get('estado', 'activa'),
                        'configurada': False,
                        'nuc_id': data.get('nuc_id')
                    })
    else:
        for key in db.scan_iter('snapshot:*'):
            ip = key.replace('snapshot:', '')
            if ip not in seen_ips:
                seen_ips.add(ip)
                data_str = db.get(key)
                if data_str:
                    data = json.loads(data_str)
                    camaras.append({
                        'ip': ip,
                        'nombre': f'Cámara {ip}',
                        'estado': data.get('estado', 'activa'),
                        'configurada': False,
                        'nuc_id': data.get('nuc_id')
                    })
    
    return jsonify({
        'success': True,
        'camaras': camaras,
        'total': len(camaras),
        'modo': 'configurado' if USAR_CONFIG_FILE else 'automatico',
        'timestamp': datetime.now().isoformat()
    })

# ============================================
# INICIO DEL SERVIDOR
# ============================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    
    print("=" * 70)
    print("Backend Estilo Hikvision")
    print("=" * 70)
    print(f"Puerto: {port}")
    print(f"Redis: {'✅' if not isinstance(db, dict) else '❌ (memoria)'}")
    print(f"Config File: {'✅' if USAR_CONFIG_FILE else '❌'}")
    if USAR_CONFIG_FILE:
        print(f"Cámaras configuradas: {len(CAMARAS_CONFIGURADAS)}")
    print("=" * 70)
    print()
    print("✅ Servidor listo para recibir conexiones de NUCs")
    print("   Los NUCs se conectarán automáticamente vía WebSocket")
    print()
    
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
