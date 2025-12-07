# 📋 Guía: Archivo de Configuración Centralizado (config.py)

## 🎯 **Objetivo:**
Tener todas las IPs de NUCs y cámaras en un solo archivo Python (`config.py`) para fácil gestión y mantenimiento.

---

## 📁 **Archivo: `backend/config.py`**

Este archivo contiene toda la configuración centralizada:

### **1. IPs de NUCs:**
```python
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.64.0.15',
        'puerto': 5000,
        'nombre': 'NUC Sede 1',
        'red_local': '192.168.60'
    },
    'nuc_sede2': {
        'tailscale_ip': '100.64.0.16',
        'puerto': 5000,
        'nombre': 'NUC Sede 2',
        'red_local': '192.168.61'
    },
}
```

### **2. IPs de Cámaras:**
```python
CAMARAS_CONFIG = [
    {'ip': '192.168.60.64', 'nombre': 'Cámara Entrada', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.65', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cámara Garage', 'nuc': 'nuc_sede1'},
]
```

---

## ✅ **PASO 1: Crear/Editar config.py**

### **1.1. Si no existe config.py:**

Copia el archivo de ejemplo:
```powershell
# En PowerShell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
copy config.ejemplo.py config.py
```

### **1.2. Abre el archivo:**
```
backend/config.py
```

### **1.2. Configura tus NUCs:**

Edita la sección `NUCs_CONFIG`:

```python
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.64.0.15',  # ← IP de Tailscale del NUC
        'puerto': 5000,
        'nombre': 'NUC Sede 1',
        'red_local': '192.168.60'  # ← Red local donde están las cámaras
    },
    # Agrega más NUCs aquí
    'nuc_sede2': {
        'tailscale_ip': '100.64.0.16',
        'puerto': 5000,
        'nombre': 'NUC Sede 2',
        'red_local': '192.168.61'
    },
}
```

### **1.3. Configura tus Cámaras:**

Edita la sección `CAMARAS_CONFIG`:

```python
CAMARAS_CONFIG = [
    # Sede 1
    {'ip': '192.168.60.64', 'nombre': 'Cámara Entrada', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.65', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cámara Garage', 'nuc': 'nuc_sede1'},
    
    # Sede 2
    {'ip': '192.168.61.10', 'nombre': 'Cámara Recepción', 'nuc': 'nuc_sede2'},
    {'ip': '192.168.61.11', 'nombre': 'Cámara Almacén', 'nuc': 'nuc_sede2'},
    
    # Agrega más cámaras aquí
]
```

### **1.4. Configura Credenciales (Opcional):**

```python
# En config.py o como variables de entorno
USUARIO_CAMARAS = 'admin'
CONTRASENA_CAMARAS = 'citikold.2020'
```

---

## ✅ **PASO 2: Usar en Railway (Opcional)**

### **Opción A: Usar config.py directamente**

Si subes `config.py` a GitHub, Railway lo usará automáticamente.

### **Opción B: Usar Variables de Entorno (Recomendado para Railway)**

En Railway, puedes sobrescribir la configuración con variables de entorno:

```
# Variables de entorno en Railway
NUC_URLS=nuc_sede1:http://100.64.0.15:5000,nuc_sede2:http://100.64.0.16:5000
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66
```

**Las variables de entorno tienen prioridad sobre config.py**

---

## 🔄 **Cómo Funciona:**

### **Prioridad de Configuración:**

1. **Variables de Entorno** (Railway) → Tienen máxima prioridad
2. **config.py** → Se usa si no hay variables de entorno
3. **Valores por defecto** → Si no hay nada configurado

### **Ejemplo:**

```python
# En Railway (variables de entorno):
NUC_URLS=nuc_sede1:http://100.64.0.15:5000
CAMARAS_IPS=192.168.60.64,192.168.60.65

# Railway usará estas variables (ignora config.py)

# Si NO hay variables de entorno:
# Railway usará config.py
```

---

## ✅ **Ventajas:**

### **1. Configuración Local:**
- ✅ Editas `config.py` con todas las IPs
- ✅ Fácil de mantener y versionar
- ✅ Puedes tener diferentes configuraciones por entorno

### **2. Flexibilidad:**
- ✅ Funciona con `config.py` (local)
- ✅ Funciona con variables de entorno (Railway)
- ✅ Puedes combinar ambos

### **3. Organización:**
- ✅ Todas las IPs en un solo lugar
- ✅ Fácil agregar/quitar NUCs y cámaras
- ✅ Estructura clara y documentada

---

## 📝 **Ejemplo Completo de config.py:**

```python
# NUCs
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.64.0.15',
        'puerto': 5000,
        'nombre': 'NUC Sede Principal',
        'red_local': '192.168.60'
    },
    'nuc_sede2': {
        'tailscale_ip': '100.64.0.16',
        'puerto': 5000,
        'nombre': 'NUC Sede Secundaria',
        'red_local': '192.168.61'
    },
}

# Cámaras
CAMARAS_CONFIG = [
    # Sede 1
    {'ip': '192.168.60.64', 'nombre': 'Cámara Entrada Principal', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.65', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cámara Garage', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.67', 'nombre': 'Cámara Trasera', 'nuc': 'nuc_sede1'},
    
    # Sede 2
    {'ip': '192.168.61.10', 'nombre': 'Cámara Recepción', 'nuc': 'nuc_sede2'},
    {'ip': '192.168.61.11', 'nombre': 'Cámara Almacén', 'nuc': 'nuc_sede2'},
]
```

---

## 🔧 **Agregar Nueva Cámara:**

### **1. Edita config.py:**

```python
CAMARAS_CONFIG = [
    # ... cámaras existentes ...
    {'ip': '192.168.60.68', 'nombre': 'Cámara Nueva', 'nuc': 'nuc_sede1'},  # ← Agregar aquí
]
```

### **2. Guarda el archivo**

### **3. Si estás en Railway:**
- Opción A: Sube el cambio a GitHub (Railway se actualizará automáticamente)
- Opción B: Agrega la IP en Railway → Variables: `CAMARAS_IPS=...,192.168.60.68`

**NO necesitas modificar código en el NUC.**

---

## 🔧 **Agregar Nuevo NUC:**

### **1. Edita config.py:**

```python
NUCs_CONFIG = {
    # ... NUCs existentes ...
    'nuc_sede3': {  # ← Agregar aquí
        'tailscale_ip': '100.64.0.17',
        'puerto': 5000,
        'nombre': 'NUC Sede 3',
        'red_local': '192.168.62'
    },
}
```

### **2. Agrega cámaras de ese NUC:**

```python
CAMARAS_CONFIG = [
    # ... cámaras existentes ...
    {'ip': '192.168.62.10', 'nombre': 'Cámara Sede 3', 'nuc': 'nuc_sede3'},  # ← Agregar aquí
]
```

---

## 📊 **Verificar Configuración:**

### **Ejecutar config.py directamente:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
python config.py
```

**Salida esperada:**
```
======================================================================
📋 Configuración Centralizada
======================================================================

🔗 NUCs configurados: 2
   - nuc_sede1: http://100.64.0.15:5000
   - nuc_sede2: http://100.64.0.16:5000

📹 Cámaras configuradas: 6
   - 192.168.60.64: Cámara Entrada
   - 192.168.60.65: Cámara Patio
   ...

======================================================================
```

---

## 🔄 **Flujo de Uso:**

### **1. Desarrollo Local:**
- Editas `config.py` con tus IPs
- Ejecutas `python server.py`
- El servidor usa la configuración de `config.py`

### **2. Producción (Railway):**
- Opción A: Subes `config.py` a GitHub (Railway lo usa)
- Opción B: Configuras variables de entorno en Railway (tienen prioridad)

---

## ✅ **Ventajas de esta Solución:**

| Aspecto | Variables de Entorno | config.py |
|---------|---------------------|-----------|
| **Fácil de editar** | ⭐⭐⭐ (en Railway) | ⭐⭐⭐⭐⭐ (archivo local) |
| **Versionado** | ❌ No | ✅ Sí (Git) |
| **Múltiples entornos** | ⚠️ Difícil | ✅ Fácil (ramas Git) |
| **Organización** | ⚠️ Disperso | ✅ Centralizado |

**Recomendación:** Usa `config.py` para desarrollo y variables de entorno para producción en Railway.

---

## 📝 **Resumen:**

- ✅ **Archivo `config.py`** con todas las IPs (NUCs y cámaras)
- ✅ **Fácil de editar** (solo editas un archivo)
- ✅ **Funciona localmente** y en Railway
- ✅ **Variables de entorno tienen prioridad** (flexibilidad)
- ✅ **NO necesitas modificar código en los NUCs**

---

## 📝 **Archivo de Ejemplo:**

Si no existe `config.py`, copia `config.ejemplo.py`:

```powershell
copy config.ejemplo.py config.py
```

Luego edita `config.py` con tus IPs reales.

---

## 📞 **Soporte Adicional**

- 📄 **Configurar IPs en Railway:** Ver `GUIA_CONFIGURAR_IPS_CAMARAS.md`
- 📄 **Puente genérico:** Ver `SOLUCION_PUENTE_GENERICO.md`
- 📄 **Conexión Tailscale:** Ver `GUIA_CONEXION_TAILSCALE_RAILWAY.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
