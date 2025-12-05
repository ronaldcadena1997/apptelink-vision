#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo de Configuración Centralizado
Contiene todas las IPs de NUCs y cámaras
"""

import os

# ============================================
# CONFIGURACIÓN DE NUCS
# ============================================

# IPs de NUCs (Tailscale)
# Formato: nombre:ip_tailscale:puerto o ip_tailscale:puerto
# Se puede configurar desde variable de entorno NUC_URLS o aquí directamente

NUC_URLS_STR = os.getenv('NUC_URLS', os.getenv('NUC_URL', None))

# Si no hay variable de entorno, usar configuración por defecto
if not NUC_URLS_STR:
    # CONFIGURACIÓN LOCAL (edita estas IPs según tus NUCs)
    NUCs_CONFIG = {
        'nuc_sede1': {
            'tailscale_ip': '100.92.50.72',  # Tu IP de Tailscale
            'puerto': 5000,
            'nombre': 'NUC Principal',
            'red_local': '192.168.60'  # Tu red local
        },
        # Si tienes más NUCs, agrégalos aquí:
        # 'nuc_sede2': {
        #     'tailscale_ip': '100.92.50.XX',  # IP de Tailscale del NUC 2
        #     'puerto': 5000,
        #     'nombre': 'NUC Sede 2',
        #     'red_local': '192.168.61'
        # },
    }
    
    # Construir URLs desde configuración
    NUC_URLS_STR = ','.join([
        f"{nombre}:http://{config['tailscale_ip']}:{config['puerto']}"
        for nombre, config in NUCs_CONFIG.items()
    ])
else:
    # Si hay variables de entorno, NUCs_CONFIG estará vacío
    # pero se parseará desde NUC_URLS_STR más abajo
    NUCs_CONFIG = {}

# Parsear NUCs
NUCs = {}
if NUC_URLS_STR:
    nucs_list = [n.strip() for n in NUC_URLS_STR.split(',')]
    for nuc in nucs_list:
        if ':' in nuc:
            # Formato: nombre:url
            partes = nuc.split(':', 1)
            if len(partes) == 2:
                nombre, url = partes
                NUCs[nombre.strip()] = url.strip()
        else:
            # Formato: url (nombre por defecto)
            nombre = f"nuc_{len(NUCs) + 1}"
            NUCs[nombre] = nuc.strip()

# ============================================
# CONFIGURACIÓN DE CÁMARAS
# ============================================

# IPs de cámaras
# Se puede configurar desde variable de entorno CAMARAS_IPS o aquí directamente
CAMARAS_IPS_STR = os.getenv('CAMARAS_IPS', '')

# Si no hay variable de entorno, usar configuración por defecto
if not CAMARAS_IPS_STR:
    # CONFIGURACIÓN LOCAL (edita estas IPs según tus cámaras)
    CAMARAS_CONFIG = [
        # Cámaras del NUC Principal
        {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},
        # Si tienes más cámaras, agrégalas aquí:
        # {'ip': '192.168.60.66', 'nombre': 'Cámara 2', 'nuc': 'nuc_sede1'},
        # {'ip': '192.168.60.67', 'nombre': 'Cámara 3', 'nuc': 'nuc_sede1'},
    ]
    
    # Extraer solo las IPs
    CAMARAS_IPS_STR = ','.join([cam['ip'] for cam in CAMARAS_CONFIG])
else:
    CAMARAS_CONFIG = []

# Parsear IPs de cámaras
CAMARAS_CONFIGURADAS = [ip.strip() for ip in CAMARAS_IPS_STR.split(',') if ip.strip()]

# Diccionario para acceso rápido por IP
CAMARAS_DICT = {}
if CAMARAS_CONFIG:
    for cam in CAMARAS_CONFIG:
        CAMARAS_DICT[cam['ip']] = cam
elif CAMARAS_CONFIGURADAS:
    # Si solo hay IPs, crear estructura básica
    for ip in CAMARAS_CONFIGURADAS:
        CAMARAS_DICT[ip] = {
            'ip': ip,
            'nombre': f'Cámara {ip}',
            'nuc': None  # Se detectará automáticamente
        }

# ============================================
# CONFIGURACIÓN DE CREDENCIALES DE CÁMARAS
# ============================================

# Usuario y contraseña para acceder a las cámaras
USUARIO_CAMARAS = os.getenv('USUARIO_CAMARAS', 'admin')
CONTRASENA_CAMARAS = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def obtener_nuc_por_camara(ip_camara):
    """Obtiene el NUC asociado a una IP de cámara"""
    # Si hay configuración detallada
    if ip_camara in CAMARAS_DICT and CAMARAS_DICT[ip_camara].get('nuc'):
        nuc_id = CAMARAS_DICT[ip_camara]['nuc']
        if nuc_id in NUCs:
            return NUCs[nuc_id]
    
    # Si no, intentar mapear por rango de red
    for nombre, url in NUCs.items():
        try:
            nuc_ip = url.split('//')[1].split(':')[0]
            # Si la IP de la cámara está en el mismo rango (primeros 3 octetos)
            if ip_camara.rsplit('.', 1)[0] == nuc_ip.rsplit('.', 1)[0]:
                return url
        except:
            pass
    
    # Por defecto: usar el primer NUC
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

# ============================================
# INFORMACIÓN DE CONFIGURACIÓN
# ============================================

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

# ============================================
# IMPRIMIR CONFIGURACIÓN AL IMPORTAR
# ============================================

if __name__ == '__main__':
    print("=" * 70)
    print("📋 Configuración Centralizada")
    print("=" * 70)
    print()
    
    print(f"🔗 NUCs configurados: {len(NUCs)}")
    for nombre, url in NUCs.items():
        print(f"   - {nombre}: {url}")
    print()
    
    print(f"📹 Cámaras configuradas: {len(CAMARAS_CONFIGURADAS)}")
    for ip in CAMARAS_CONFIGURADAS:
        info = obtener_info_camara(ip)
        print(f"   - {ip}: {info.get('nombre', 'Sin nombre')}")
    print()
    
    print("=" * 70)
    print()
    print("💡 Para usar esta configuración:")
    print("   1. Edita este archivo (config.py) con tus IPs")
    print("   2. O configura variables de entorno en Railway:")
    print("      - NUC_URLS=nombre1:http://ip1:5000,nombre2:http://ip2:5000")
    print("      - CAMARAS_IPS=192.168.60.64,192.168.60.65,...")
    print("=" * 70)
