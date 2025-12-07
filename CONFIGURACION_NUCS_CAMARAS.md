# 📋 Guía: Configurar NUCs y Cámaras en config.py

## 📝 **Resumen**

El archivo `config.py` centraliza la configuración de todos los NUCs y sus cámaras. **No necesitas usar variables de entorno**, solo edita este archivo.

---

## 🔧 **Configuración de NUCs**

Edita la sección `NUCs_CONFIG` en `config.py`:

```python
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.92.50.72',  # Solo para arquitectura antigua
        'puerto': 5000,
        'nombre': 'NUC Principal',
        'red_local': '192.168.60',
        'server_url': 'https://apptelink-vision-production.up.railway.app'  # URL del servidor
    },
    'nuc_sede2': {
        'tailscale_ip': '100.92.50.73',  # Solo para arquitectura antigua
        'puerto': 5000,
        'nombre': 'NUC Sede 2',
        'red_local': '192.168.61',
        'server_url': 'https://apptelink-vision-production.up.railway.app'
    },
    # Agrega más NUCs aquí...
}
```

### **Campos:**
- `'nuc_sede1'`: **ID del NUC** (debe ser único)
- `'nombre'`: Nombre descriptivo del NUC
- `'red_local'`: Red local donde están las cámaras (ej: '192.168.60')
- `'server_url'`: URL del servidor central en Railway
- `'tailscale_ip'`: Solo necesario para arquitectura antigua (puedes dejarlo vacío)

---

## 📹 **Configuración de Cámaras**

Edita la sección `CAMARAS_CONFIG` en `config.py`:

```python
CAMARAS_CONFIG = [
    # Cámaras del NUC Principal (nuc_sede1)
    {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cámara Entrada', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.67', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
    
    # Cámaras del NUC Sede 2 (nuc_sede2)
    {'ip': '192.168.61.65', 'nombre': 'Cámara Sede 2 - Principal', 'nuc': 'nuc_sede2'},
    {'ip': '192.168.61.66', 'nombre': 'Cámara Sede 2 - Entrada', 'nuc': 'nuc_sede2'},
    
    # Agrega más cámaras aquí...
]
```

### **Campos:**
- `'ip'`: **IP de la cámara** (obligatorio)
- `'nombre'`: Nombre descriptivo de la cámara
- `'nuc'`: **ID del NUC** al que pertenece (debe coincidir con un NUC en `NUCs_CONFIG`)

---

## 🎯 **Ejemplo Completo**

```python
# ============================================
# CONFIGURACIÓN DE NUCS
# ============================================

NUCs_CONFIG = {
    'nuc_sede1': {
        'nombre': 'NUC Principal',
        'red_local': '192.168.60',
        'server_url': 'https://apptelink-vision-production.up.railway.app'
    },
    'nuc_sede2': {
        'nombre': 'NUC Sede 2',
        'red_local': '192.168.61',
        'server_url': 'https://apptelink-vision-production.up.railway.app'
    },
    'nuc_sede3': {
        'nombre': 'NUC Sede 3',
        'red_local': '192.168.62',
        'server_url': 'https://apptelink-vision-production.up.railway.app'
    }
}

# ============================================
# CONFIGURACIÓN DE CÁMARAS
# ============================================

CAMARAS_CONFIG = [
    # Cámaras del NUC Principal
    {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cámara Entrada', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.67', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
    
    # Cámaras del NUC Sede 2
    {'ip': '192.168.61.65', 'nombre': 'Cámara Sede 2 - Principal', 'nuc': 'nuc_sede2'},
    {'ip': '192.168.61.66', 'nombre': 'Cámara Sede 2 - Entrada', 'nuc': 'nuc_sede2'},
    
    # Cámaras del NUC Sede 3
    {'ip': '192.168.62.65', 'nombre': 'Cámara Sede 3 - Principal', 'nuc': 'nuc_sede3'},
]
```

---

## 🚀 **Cómo Usar en Cada NUC**

### **En el NUC (nuc_agent_hikvision.py):**

El agente lee automáticamente `config.py` y:
1. Obtiene el `NUC_ID` desde la variable de entorno `NUC_ID` o usa el primer NUC de `NUCs_CONFIG`
2. Filtra las cámaras que pertenecen a ese NUC
3. Obtiene `SERVER_URL` desde `NUCs_CONFIG[NUC_ID]['server_url']`

**Para especificar qué NUC es este:**
```powershell
# Opción 1: Variable de entorno
[System.Environment]::SetEnvironmentVariable('NUC_ID', 'nuc_sede1', 'User')

# Opción 2: Editar config.py y poner este NUC primero en NUCs_CONFIG
```

---

## ✅ **Ventajas de Usar config.py**

- ✅ **Centralizado:** Toda la configuración en un solo archivo
- ✅ **Fácil de editar:** No necesitas variables de entorno
- ✅ **Versionado:** Se puede subir a Git
- ✅ **Múltiples NUCs:** Fácil agregar más NUCs y cámaras
- ✅ **Organizado:** Cada cámara sabe a qué NUC pertenece

---

## 📝 **Notas Importantes**

1. **El `'nuc'` en `CAMARAS_CONFIG` debe coincidir** con una clave en `NUCs_CONFIG`
2. **Cada NUC debe tener su propio `config.py`** o usar `NUC_ID` para filtrar
3. **El `server_url` puede ser el mismo** para todos los NUCs (todos se conectan al mismo servidor)
4. **Las IPs de cámaras deben ser únicas** (no puede haber dos cámaras con la misma IP)

---

## 🔄 **Actualizar Configuración**

1. Edita `config.py`
2. Guarda el archivo
3. Reinicia el NUC Agent (si está corriendo)
4. El backend en Railway leerá automáticamente la nueva configuración

---

**¿Listo para configurar?** Edita `backend/config.py` con tus NUCs y cámaras.
