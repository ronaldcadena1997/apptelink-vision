#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend con Arquitectura Polling/Webhook
=========================================
Este backend recibe datos del NUC y los almacena en Redis/PostgreSQL.
No necesita Tailscale, solo recibe HTTP POST del NUC.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime
import redis

# ============================================
# CONFIGURACIÓN
# ============================================

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Base de datos (Redis o PostgreSQL)
# Opción 1: Redis (más simple, Railway tiene Redis)
try:
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    db = redis.from_url(REDIS_URL, decode_responses=True)
    print("✅ Conectado a Redis")
except:
    # Fallback: usar diccionario en memoria (no persistente)
    db = {}
    print("⚠️  Redis no disponible, usando almacenamiento en memoria")

# Tiempo de expiración de snapshots (segundos)
SNAPSHOT_EXPIRY = int(os.getenv('SNAPSHOT_EXPIRY', '300'))  # 5 minutos

# ============================================
# ENDPOINTS PARA RECIBIR DATOS DEL NUC
# ============================================

@app.route('/api/camaras/<ip>/snapshot', methods=['POST'])
def recibir_snapshot(ip):
    """
    Recibe un snapshot del NUC
    """
    try:
        data = request.get_json()
        
        nuc_id = data.get('nuc_id', 'unknown')
        image_base64 = data.get('image')
        estado = data.get('estado', 'activa')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        if not image_base64:
            return jsonify({'success': False, 'error': 'No se recibió imagen'}), 400
        
        # Almacenar en base de datos
        snapshot_data = {
            'ip': ip,
            'nuc_id': nuc_id,
            'image': image_base64,
            'estado': estado,
            'timestamp': timestamp
        }
        
        if isinstance(db, dict):
            # Almacenamiento en memoria
            db[f'snapshot:{ip}'] = json.dumps(snapshot_data)
        else:
            # Redis
            db.setex(
                f'snapshot:{ip}',
                SNAPSHOT_EXPIRY,
                json.dumps(snapshot_data)
            )
        
        print(f"✅ Snapshot recibido de {nuc_id} - Cámara {ip}")
        return jsonify({'success': True, 'message': 'Snapshot recibido'})
        
    except Exception as e:
        print(f"❌ Error al recibir snapshot: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/camaras/<ip>/estado', methods=['POST'])
def recibir_estado(ip):
    """
    Recibe el estado de una cámara del NUC
    """
    try:
        data = request.get_json()
        
        nuc_id = data.get('nuc_id', 'unknown')
        estado = data.get('estado', 'unknown')
        error = data.get('error')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        estado_data = {
            'ip': ip,
            'nuc_id': nuc_id,
            'estado': estado,
            'error': error,
            'timestamp': timestamp
        }
        
        if isinstance(db, dict):
            db[f'estado:{ip}'] = json.dumps(estado_data)
        else:
            db.setex(
                f'estado:{ip}',
                600,  # 10 minutos
                json.dumps(estado_data)
            )
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# ENDPOINTS PARA EL FRONTEND
# ============================================

@app.route('/api/status', methods=['GET'])
def status():
    """Estado del servidor"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'arquitectura': 'polling/webhook'
    })

@app.route('/api/camaras', methods=['GET'])
def listar_camaras():
    """
    Lista todas las cámaras con su último snapshot
    """
    try:
        camaras = []
        
        if isinstance(db, dict):
            # Buscar en memoria
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
            # Buscar en Redis
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
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/camaras/<ip>/snapshot', methods=['GET'])
def obtener_snapshot(ip):
    """
    Obtiene el último snapshot de una cámara
    """
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
        
        data = json.loads(data_str)
        
        return jsonify({
            'success': True,
            'ip': ip,
            'image': data.get('image'),
            'estado': data.get('estado'),
            'timestamp': data.get('timestamp')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/camaras/detectar', methods=['GET'])
def detectar_camaras():
    """
    Detecta cámaras basándose en los datos recibidos del NUC
    """
    try:
        camaras = []
        
        if isinstance(db, dict):
            for key in db.keys():
                if key.startswith('snapshot:') or key.startswith('estado:'):
                    ip = key.replace('snapshot:', '').replace('estado:', '')
                    
                    # Obtener snapshot
                    snapshot_data = None
                    if f'snapshot:{ip}' in db:
                        snapshot_data = json.loads(db[f'snapshot:{ip}'])
                    
                    # Obtener estado
                    estado_data = None
                    if f'estado:{ip}' in db:
                        estado_data = json.loads(db[f'estado:{ip}'])
                    
                    estado = estado_data.get('estado') if estado_data else snapshot_data.get('estado', 'sin_acceso')
                    
                    camaras.append({
                        'ip': ip,
                        'nombre': f'Cámara {ip}',
                        'estado': estado,
                        'configurada': True,
                        'nuc_id': snapshot_data.get('nuc_id') if snapshot_data else None
                    })
        else:
            # Redis
            seen_ips = set()
            for key in db.scan_iter('snapshot:*'):
                ip = key.replace('snapshot:', '')
                if ip in seen_ips:
                    continue
                seen_ips.add(ip)
                
                snapshot_data_str = db.get(key)
                estado_data_str = db.get(f'estado:{ip}')
                
                snapshot_data = json.loads(snapshot_data_str) if snapshot_data_str else None
                estado_data = json.loads(estado_data_str) if estado_data_str else None
                
                estado = estado_data.get('estado') if estado_data else snapshot_data.get('estado', 'sin_acceso')
                
                camaras.append({
                    'ip': ip,
                    'nombre': f'Cámara {ip}',
                    'estado': estado,
                    'configurada': True,
                    'nuc_id': snapshot_data.get('nuc_id') if snapshot_data else None
                })
        
        return jsonify({
            'success': True,
            'camaras': camaras,
            'total': len(camaras),
            'modo': 'configurado',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# INICIO DEL SERVIDOR
# ============================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    print("=" * 70)
    print("Backend con Arquitectura Polling/Webhook")
    print("=" * 70)
    print(f"Puerto: {port}")
    print(f"Redis: {'✅' if not isinstance(db, dict) else '❌ (memoria)'}")
    print("=" * 70)
    app.run(host='0.0.0.0', port=port, debug=False)
