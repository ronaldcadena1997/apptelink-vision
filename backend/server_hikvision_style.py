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
    print("✅ Configuración cargada desde config.py")
except ImportError as e:
    USAR_CONFIG_FILE = False
    CAMARAS_CONFIGURADAS = []
    CAMARAS_DICT = {}
    print(f"⚠️  No se pudo importar config.py: {e}")
    # Crear función por defecto
    def obtener_info_camara(ip):
        return {'ip': ip, 'nombre': f'Cámara {ip}', 'nuc': None}
except Exception as e:
    USAR_CONFIG_FILE = False
    CAMARAS_CONFIGURADAS = []
    CAMARAS_DICT = {}
    print(f"⚠️  Error al cargar config.py: {e}")
    # Crear función por defecto
    def obtener_info_camara(ip):
        return {'ip': ip, 'nombre': f'Cámara {ip}', 'nuc': None}

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
    try:
        # El auth puede venir como dict o como query string
        if isinstance(auth, dict):
            nuc_id = auth.get('nuc_id', 'unknown')
        else:
            # Si viene como query string, obtener de request.args
            nuc_id = request.args.get('nuc_id', 'unknown')
        
        nucs_conectados[nuc_id] = {
            'socket_id': request.sid,
            'last_heartbeat': time.time(),
            'camaras': [],
            'connected_at': datetime.now().isoformat()
        }
        
        print(f"✅ NUC conectado: {nuc_id} (Socket: {request.sid})")
        print(f"   Total NUCs conectados: {len(nucs_conectados)}")
        
        emit('connected', {
            'status': 'ok',
            'nuc_id': nuc_id,
            'message': 'Conectado al servidor central'
        })
    except Exception as e:
        print(f"❌ Error en handle_connect: {e}")
        import traceback
        traceback.print_exc()

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
        
        print(f"📸 Snapshot recibido: {nuc_id} - {ip} ({len(image)} bytes)")
        # Verificar que se guardó correctamente
        try:
            if isinstance(db, dict):
                db[f'snapshot:{ip}'] = json.dumps(snapshot_data)  # Guardar de nuevo para asegurar
                saved = db.get(f'snapshot:{ip}')
                if saved:
                    print(f"✅ Snapshot guardado en memoria para {ip} (tamaño: {len(saved)} bytes)")
                else:
                    print(f"⚠️  Snapshot NO se guardó en memoria para {ip}")
            else:
                db.setex(f'snapshot:{ip}', SNAPSHOT_EXPIRY, json.dumps(snapshot_data))  # Guardar de nuevo
                saved = db.get(f'snapshot:{ip}')
                if saved:
                    print(f"✅ Snapshot guardado en Redis para {ip} (tamaño: {len(saved)} bytes)")
                else:
                    print(f"⚠️  Snapshot NO se guardó en Redis para {ip}")
        except Exception as verify_error:
            print(f"⚠️  Error al verificar snapshot guardado: {verify_error}")
            import traceback
            traceback.print_exc()
        
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
    try:
        camaras = []
        
        # Obtener de Redis
        try:
            if isinstance(db, dict):
                for key, value in list(db.items()):  # Convertir a lista para evitar cambios durante iteración
                    try:
                        if key.startswith('snapshot:'):
                            ip = key.replace('snapshot:', '')
                            try:
                                data = json.loads(value)
                                camaras.append({
                                    'ip': ip,
                                    'nuc_id': data.get('nuc_id'),
                                    'estado': data.get('estado'),
                                    'timestamp': data.get('timestamp'),
                                    'tiene_snapshot': True
                                })
                            except (json.JSONDecodeError, TypeError) as e:
                                print(f"⚠️  Error al parsear snapshot de {ip}: {e}")
                                continue
                    except Exception as e:
                        print(f"⚠️  Error al procesar key {key}: {e}")
                        continue
            else:
                # Redis real
                try:
                    for key in db.scan_iter('snapshot:*'):
                        try:
                            ip = key.replace('snapshot:', '')
                            data_str = db.get(key)
                            if data_str:
                                try:
                                    data = json.loads(data_str)
                                    camaras.append({
                                        'ip': ip,
                                        'nuc_id': data.get('nuc_id'),
                                        'estado': data.get('estado'),
                                        'timestamp': data.get('timestamp'),
                                        'tiene_snapshot': True
                                    })
                                except (json.JSONDecodeError, TypeError) as e:
                                    print(f"⚠️  Error al parsear snapshot de {ip}: {e}")
                                    continue
                        except Exception as e:
                            print(f"⚠️  Error al procesar key {key}: {e}")
                            continue
                except Exception as e:
                    print(f"⚠️  Error al iterar Redis: {e}")
        except Exception as e:
            print(f"⚠️  Error al leer de Redis: {e}")
        
        return jsonify({
            'success': True,
            'camaras': camaras,
            'total': len(camaras)
        })
        
    except Exception as e:
        print(f"❌ Error crítico en listar_camaras: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error al listar cámaras: {str(e)}',
            'camaras': [],
            'total': 0
        }), 500

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
    try:
        camaras = []
        seen_ips = set()
        
        # Primero, obtener cámaras de config.py si está disponible
        if USAR_CONFIG_FILE and CAMARAS_CONFIGURADAS:
            for ip in CAMARAS_CONFIGURADAS:
                try:
                    if ip in seen_ips:
                        continue
                    seen_ips.add(ip)
                    
                    # Obtener info de la cámara con manejo de errores
                    try:
                        info = obtener_info_camara(ip)
                    except Exception as e:
                        print(f"⚠️  Error al obtener info de cámara {ip}: {e}")
                        info = {'nombre': f'Cámara {ip}', 'nuc': None}
                    
                    # Verificar si hay snapshot en Redis
                    snapshot_data_str = None
                    estado_data_str = None
                    
                    try:
                        if isinstance(db, dict):
                            snapshot_data_str = db.get(f'snapshot:{ip}')
                            estado_data_str = db.get(f'estado:{ip}')
                        else:
                            snapshot_data_str = db.get(f'snapshot:{ip}')
                            estado_data_str = db.get(f'estado:{ip}')
                    except Exception as e:
                        print(f"⚠️  Error al leer de Redis para {ip}: {e}")
                    
                    # Parsear JSON con manejo de errores
                    estado_data = None
                    snapshot_data = None
                    
                    try:
                        if estado_data_str:
                            estado_data = json.loads(estado_data_str)
                    except (json.JSONDecodeError, TypeError) as e:
                        print(f"⚠️  Error al parsear estado_data para {ip}: {e}")
                    
                    try:
                        if snapshot_data_str:
                            snapshot_data = json.loads(snapshot_data_str)
                            # Verificar que el snapshot es reciente (últimos 60 segundos)
                            if snapshot_data:
                                timestamp_str = snapshot_data.get('timestamp', '')
                                if timestamp_str:
                                    try:
                                        snapshot_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                                        now = datetime.now(snapshot_time.tzinfo) if snapshot_time.tzinfo else datetime.now()
                                        time_diff = (now - snapshot_time).total_seconds()
                                        if time_diff > 60:
                                            # Snapshot muy antiguo, considerar como sin acceso
                                            snapshot_data = None
                                            print(f"⚠️  Snapshot de {ip} es muy antiguo ({int(time_diff)}s), ignorando")
                                    except:
                                        pass  # Si no se puede parsear, usar el snapshot de todas formas
                    except (json.JSONDecodeError, TypeError) as e:
                        print(f"⚠️  Error al parsear snapshot_data para {ip}: {e}")
                        print(f"   Contenido raw: {snapshot_data_str[:200] if snapshot_data_str else 'None'}...")
                    
                    # Debug: mostrar qué se encontró
                    if snapshot_data_str:
                        print(f"🔍 DEBUG {ip}: snapshot_data_str encontrado ({len(snapshot_data_str)} bytes)")
                    else:
                        print(f"🔍 DEBUG {ip}: NO hay snapshot_data_str en DB")
                        # Intentar leer todas las keys para debug
                        try:
                            if isinstance(db, dict):
                                keys = [k for k in db.keys() if 'snapshot' in k]
                                print(f"   Keys en memoria con 'snapshot': {keys}")
                            else:
                                keys = list(db.scan_iter('snapshot:*'))
                                print(f"   Keys en Redis con 'snapshot': {[k for k in keys]}")
                        except:
                            pass
                    
                    # Determinar estado
                    # Si hay snapshot reciente, la cámara está activa
                    if snapshot_data:
                        estado = 'activa'  # Forzar 'activa' si hay snapshot reciente
                        print(f"✅ Cámara {ip} tiene snapshot reciente - Estado: activa")
                    elif estado_data:
                        # Si hay estado de error, usar ese estado
                        estado = estado_data.get('estado', 'sin_acceso')
                        print(f"⚠️  Cámara {ip} tiene estado de error - Estado: {estado}")
                    else:
                        # Si no hay datos, verificar si hay NUC conectado para esta cámara
                        nuc_asociado = info.get('nuc')
                        if nuc_asociado and nuc_asociado in nucs_conectados:
                            # NUC conectado pero sin snapshot aún - puede estar procesando
                            # Verificar si el NUC ha enviado snapshots recientemente
                            nuc_info = nucs_conectados.get(nuc_asociado, {})
                            last_heartbeat = nuc_info.get('last_heartbeat', 0)
                            time_since_heartbeat = time.time() - last_heartbeat
                            
                            if time_since_heartbeat < 60:  # NUC activo en últimos 60 segundos
                                estado = 'sin_acceso'  # NUC conectado pero sin snapshot aún
                                print(f"⚠️  Cámara {ip} - NUC conectado pero sin snapshot aún (heartbeat hace {int(time_since_heartbeat)}s)")
                            else:
                                estado = 'sin_acceso'  # NUC no está activo
                                print(f"❌ Cámara {ip} - NUC no está activo (último heartbeat hace {int(time_since_heartbeat)}s)")
                        else:
                            estado = 'sin_acceso'  # No hay datos ni NUC conectado
                            print(f"❌ Cámara {ip} - Sin datos ni NUC conectado")
                    
                    camaras.append({
                        'ip': ip,
                        'nombre': info.get('nombre', f'Cámara {ip}'),
                        'estado': estado,
                        'configurada': True,
                        'nuc_id': info.get('nuc') or (snapshot_data.get('nuc_id') if snapshot_data else None)
                    })
                except Exception as e:
                    print(f"⚠️  Error al procesar cámara {ip}: {e}")
                    # Continuar con la siguiente cámara
                    continue
        
        # También agregar cámaras que vienen de snapshots pero no están en config
        try:
            if isinstance(db, dict):
                for key in list(db.keys()):  # Convertir a lista para evitar cambios durante iteración
                    try:
                        if key.startswith('snapshot:'):
                            ip = key.replace('snapshot:', '')
                            if ip not in seen_ips:
                                seen_ips.add(ip)
                                try:
                                    data = json.loads(db[key])
                                    camaras.append({
                                        'ip': ip,
                                        'nombre': f'Cámara {ip}',
                                        'estado': data.get('estado', 'activa'),
                                        'configurada': False,
                                        'nuc_id': data.get('nuc_id')
                                    })
                                except (json.JSONDecodeError, TypeError) as e:
                                    print(f"⚠️  Error al parsear snapshot de {ip}: {e}")
                    except Exception as e:
                        print(f"⚠️  Error al procesar key {key}: {e}")
                        continue
            else:
                # Redis real
                try:
                    for key in db.scan_iter('snapshot:*'):
                        try:
                            ip = key.replace('snapshot:', '')
                            if ip not in seen_ips:
                                seen_ips.add(ip)
                                data_str = db.get(key)
                                if data_str:
                                    try:
                                        data = json.loads(data_str)
                                        camaras.append({
                                            'ip': ip,
                                            'nombre': f'Cámara {ip}',
                                            'estado': data.get('estado', 'activa'),
                                            'configurada': False,
                                            'nuc_id': data.get('nuc_id')
                                        })
                                    except (json.JSONDecodeError, TypeError) as e:
                                        print(f"⚠️  Error al parsear snapshot de {ip}: {e}")
                        except Exception as e:
                            print(f"⚠️  Error al procesar key {key}: {e}")
                            continue
                except Exception as e:
                    print(f"⚠️  Error al iterar Redis: {e}")
        except Exception as e:
            print(f"⚠️  Error al leer snapshots de Redis: {e}")
        
        return jsonify({
            'success': True,
            'camaras': camaras,
            'total': len(camaras),
            'modo': 'configurado' if USAR_CONFIG_FILE else 'automatico',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Error crítico en detectar_camaras: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error al detectar cámaras: {str(e)}',
            'camaras': [],
            'total': 0,
            'modo': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

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
