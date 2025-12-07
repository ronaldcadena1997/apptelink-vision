#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EJEMPLO de Archivo de Configuración
Copia este archivo como config.py y edita con tus IPs reales
"""

import os

# ============================================
# CONFIGURACIÓN DE NUCS
# ============================================

# Si hay variables de entorno, se usan (tienen prioridad)
# Si NO hay variables de entorno, se usa la configuración de abajo

NUC_URLS_STR = os.getenv('NUC_URLS', os.getenv('NUC_URL', None))

if not NUC_URLS_STR:
    # ⬇️ EDITA AQUÍ: Configura tus NUCs
    NUCs_CONFIG = {
        'nuc_sede1': {
            'tailscale_ip': '100.64.0.15',  # ← IP de Tailscale del NUC 1
            'puerto': 5000,
            'nombre': 'NUC Sede Principal',
            'red_local': '192.168.60'  # ← Red local donde están las cámaras
        },
        'nuc_sede2': {
            'tailscale_ip': '100.64.0.16',  # ← IP de Tailscale del NUC 2
            'puerto': 5000,
            'nombre': 'NUC Sede Secundaria',
            'red_local': '192.168.61'
        },
        # Agrega más NUCs aquí:
        # 'nuc_sede3': {
        #     'tailscale_ip': '100.64.0.17',
        #     'puerto': 5000,
        #     'nombre': 'NUC Sede 3',
        #     'red_local': '192.168.62'
        # },
    }
    
    NUC_URLS_STR = ','.join([
        f"{nombre}:http://{config['tailscale_ip']}:{config['puerto']}"
        for nombre, config in NUCs_CONFIG.items()
    ])
else:
    NUCs_CONFIG = {}

# Parsear NUCs
NUCs = {}
if NUC_URLS_STR:
    nucs_list = [n.strip() for n in NUC_URLS_STR.split(',')]
    for nuc in nucs_list:
        if ':' in nuc:
            partes = nuc.split(':', 1)
            if len(partes) == 2:
                nombre, url = partes
                NUCs[nombre.strip()] = url.strip()
        else:
            nombre = f"nuc_{len(NUCs) + 1}"
            NUCs[nombre] = nuc.strip()

# ============================================
# CONFIGURACIÓN DE CÁMARAS
# ============================================

CAMARAS_IPS_STR = os.getenv('CAMARAS_IPS', '')

if not CAMARAS_IPS_STR:
    # ⬇️ EDITA AQUÍ: Configura tus cámaras
    CAMARAS_CONFIG = [
        # Sede 1 (NUC 1)
        {'ip': '192.168.60.64', 'nombre': 'Cámara Entrada Principal', 'nuc': 'nuc_sede1'},
        {'ip': '192.168.60.65', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
        {'ip': '192.168.60.66', 'nombre': 'Cámara Garage', 'nuc': 'nuc_sede1'},
        {'ip': '192.168.60.67', 'nombre': 'Cámara Trasera', 'nuc': 'nuc_sede1'},
        
        # Sede 2 (NUC 2)
        # {'ip': '192.168.61.10', 'nombre': 'Cámara Recepción', 'nuc': 'nuc_sede2'},
        # {'ip': '192.168.61.11', 'nombre': 'Cámara Almacén', 'nuc': 'nuc_sede2'},
        
        # Agrega más cámaras aquí:
        # {'ip': '192.168.60.68', 'nombre': 'Cámara Nueva', 'nuc': 'nuc_sede1'},
    ]
    
    CAMARAS_IPS_STR = ','.join([cam['ip'] for cam in CAMARAS_CONFIG])
else:
    CAMARAS_CONFIG = []

# Parsear IPs
CAMARAS_CONFIGURADAS = [ip.strip() for ip in CAMARAS_IPS_STR.split(',') if ip.strip()]

# Diccionario para acceso rápido
CAMARAS_DICT = {}
if CAMARAS_CONFIG:
    for cam in CAMARAS_CONFIG:
        CAMARAS_DICT[cam['ip']] = cam
elif CAMARAS_CONFIGURADAS:
    for ip in CAMARAS_CONFIGURADAS:
        CAMARAS_DICT[ip] = {
            'ip': ip,
            'nombre': f'Cámara {ip}',
            'nuc': None
        }

# ============================================
# CREDENCIALES DE CÁMARAS
# ============================================

USUARIO_CAMARAS = os.getenv('USUARIO_CAMARAS', 'admin')
CONTRASENA_CAMARAS = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def obtener_nuc_por_camara(ip_camara):
    """Obtiene el NUC asociado a una IP de cámara"""
    if ip_camara in CAMARAS_DICT and CAMARAS_DICT[ip_camara].get('nuc'):
        nuc_id = CAMARAS_DICT[ip_camara]['nuc']
        if nuc_id in NUCs:
            return NUCs[nuc_id]
    
    for nombre, url in NUCs.items():
        try:
            nuc_ip = url.split('//')[1].split(':')[0]
            if ip_camara.rsplit('.', 1)[0] == nuc_ip.rsplit('.', 1)[0]:
                return url
        except:
            pass
    
    return list(NUCs.values())[0] if NUCs else None

def obtener_info_camara(ip_camara):
    """Obtiene información de una cámara por su IP"""
    return CAMARAS_DICT.get(ip_camara, {
        'ip': ip_camara,
        'nombre': f'Cámara {ip_camara}',
        'nuc': None
    })

def listar_camaras_por_nuc(nuc_id=None):
    """Lista las cámaras agrupadas por NUC"""
    if not CAMARAS_CONFIG and not CAMARAS_CONFIGURADAS:
        return {}
    
    camaras_por_nuc = {}
    for ip in CAMARAS_CONFIGURADAS:
        info = obtener_info_camara(ip)
        nuc = info.get('nuc') or nuc_id or 'default'
        
        if nuc not in camaras_por_nuc:
            camaras_por_nuc[nuc] = []
        
        camaras_por_nuc[nuc].append({
            'ip': ip,
            'nombre': info.get('nombre', f'Cámara {ip}')
        })
    
    return camaras_por_nuc

def obtener_resumen_config():
    """Obtiene un resumen de la configuración actual"""
    return {
        'nucs': {
            'total': len(NUCs),
            'nucs': [
                {
                    'id': nombre,
                    'url': url,
                    'config': NUCs_CONFIG.get(nombre, {})
                }
                for nombre, url in NUCs.items()
            ]
        },
        'camaras': {
            'total': len(CAMARAS_CONFIGURADAS),
            'configuradas': CAMARAS_CONFIGURADAS,
            'detalladas': CAMARAS_CONFIG if CAMARAS_CONFIG else None
        },
        'modo': 'configurado' if CAMARAS_CONFIGURADAS else 'automatico'
    }

if __name__ == '__main__':
    print("=" * 70)
    print("📋 EJEMPLO de Configuración")
    print("=" * 70)
    print()
    print("💡 Copia este archivo como 'config.py' y edita con tus IPs reales")
    print("=" * 70)
