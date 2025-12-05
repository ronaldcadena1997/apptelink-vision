# 📹 Configuración: Cámaras por NUC

## 🎯 **Consideración Importante**

**Cada NUC tiene diferentes cámaras.** Es crucial configurar correctamente qué cámara pertenece a qué NUC para que el sistema funcione correctamente.

---

## 📐 **Escenario Típico:**

```
┌─────────────────────────────────────────┐
│  Backend en Railway (Servidor)        │
└──────────────┬────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│ NUC 1 │ │ NUC 2 │ │ NUC 3 │
│(Sede1)│ │(Sede2)│ │(Sede3)│
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│Cam 1  │ │Cam 4  │ │Cam 7  │
│Cam 2  │ │Cam 5  │ │Cam 8  │
│Cam 3  │ │Cam 6  │ │       │
└───────┘ └───────┘ └───────┘
```

**Cada NUC solo puede acceder a sus propias cámaras en su red local.**

---

## ✅ **Método 1: Configuración Explícita con config.py (Recomendado)**

### **Ventajas:**
- ✅ Mapeo explícito y claro
- ✅ Funciona incluso si todas las cámaras están en la misma red
- ✅ Fácil de mantener y versionar
- ✅ Control total sobre qué cámara → qué NUC

### **Cómo Configurar:**

1. **Edita `backend/config.py`:**

```python
# NUCs
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.64.0.15',  # IP de Tailscale del NUC 1
        'puerto': 5000,
        'nombre': 'NUC Sede Principal',
        'red_local': '192.168.60'  # Red local del NUC 1
    },
    'nuc_sede2': {
        'tailscale_ip': '100.64.0.16',  # IP de Tailscale del NUC 2
        'puerto': 5000,
        'nombre': 'NUC Sede Secundaria',
        'red_local': '192.168.61'  # Red local del NUC 2
    },
    'nuc_sede3': {
        'tailscale_ip': '100.64.0.17',  # IP de Tailscale del NUC 3
        'puerto': 5000,
        'nombre': 'NUC Sede 3',
        'red_local': '192.168.62'  # Red local del NUC 3
    },
}

# Cámaras - ESPECIFICA EXPLÍCITAMENTE QUÉ CÁMARA PERTENECE A QUÉ NUC
CAMARAS_CONFIG = [
    # Cámaras del NUC 1 (Sede Principal)
    {'ip': '192.168.60.64', 'nombre': 'Cámara Entrada Principal', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.65', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cámara Garage', 'nuc': 'nuc_sede1'},
    
    # Cámaras del NUC 2 (Sede Secundaria)
    {'ip': '192.168.61.10', 'nombre': 'Cámara Recepción', 'nuc': 'nuc_sede2'},
    {'ip': '192.168.61.11', 'nombre': 'Cámara Almacén', 'nuc': 'nuc_sede2'},
    {'ip': '192.168.61.12', 'nombre': 'Cámara Oficina', 'nuc': 'nuc_sede2'},
    
    # Cámaras del NUC 3 (Sede 3)
    {'ip': '192.168.62.20', 'nombre': 'Cámara Exterior', 'nuc': 'nuc_sede3'},
    {'ip': '192.168.62.21', 'nombre': 'Cámara Interior', 'nuc': 'nuc_sede3'},
]
```

2. **Haz commit y push a GitHub:**
```powershell
git add backend/config.py
git commit -m "Configurar mapeo de cámaras por NUC"
git push
```

3. **Railway usará automáticamente esta configuración**

---

## ✅ **Método 2: Variables de Entorno (Mapeo Automático)**

### **Ventajas:**
- ✅ Configuración rápida en Railway
- ✅ No necesitas subir archivos
- ✅ Funciona bien si las cámaras están en diferentes redes

### **Limitaciones:**
- ⚠️ Mapeo automático por rango de IP
- ⚠️ Si todas las cámaras están en la misma red, puede no funcionar correctamente
- ⚠️ Menos control sobre el mapeo

### **Cómo Configurar:**

En Railway → Settings → Variables:

```
NUC_URLS=nuc_sede1:http://100.64.0.15:5000,nuc_sede2:http://100.64.0.16:5000,nuc_sede3:http://100.64.0.17:5000
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66,192.168.61.10,192.168.61.11,192.168.61.12,192.168.62.20,192.168.62.21
```

**Cómo funciona el mapeo automático:**

El sistema intenta mapear cada cámara a un NUC basándose en:

1. **Rango de red:** Si la cámara está en `192.168.60.x` y hay un NUC con red `192.168.60`, se mapea a ese NUC
2. **Primer NUC disponible:** Si no puede mapear, usa el primer NUC de la lista

**⚠️ Problema:** Si todas las cámaras están en la misma red (ej: todas en `192.168.60.x`), el sistema no puede distinguir a qué NUC pertenece cada cámara.

**Solución:** Usa `config.py` (Método 1) para mapeo explícito.

---

## 🔍 **Cómo Verificar el Mapeo**

### **1. Ver configuración completa:**

```bash
curl https://tu-api.railway.app/api/configuracion
```

**Respuesta:**
```json
{
  "success": true,
  "usando_config_file": true,
  "nucs": {
    "total": 3,
    "nucs": [
      {"id": "nuc_sede1", "url": "http://100.64.0.15:5000"},
      {"id": "nuc_sede2", "url": "http://100.64.0.16:5000"},
      {"id": "nuc_sede3", "url": "http://100.64.0.17:5000"}
    ]
  },
  "camaras": {
    "total": 8,
    "configuradas": ["192.168.60.64", "192.168.60.65", ...],
    "detalladas": [
      {"ip": "192.168.60.64", "nombre": "Cámara Entrada Principal", "nuc": "nuc_sede1"},
      {"ip": "192.168.60.65", "nombre": "Cámara Patio", "nuc": "nuc_sede1"},
      ...
    ]
  }
}
```

### **2. Ver cámaras agrupadas por NUC:**

```bash
curl https://tu-api.railway.app/api/camaras/configuradas
```

---

## 🔧 **Agregar Nueva Cámara a un NUC Específico**

### **Con config.py:**

1. **Edita `backend/config.py`:**

```python
CAMARAS_CONFIG = [
    # ... cámaras existentes ...
    {'ip': '192.168.60.67', 'nombre': 'Cámara Nueva', 'nuc': 'nuc_sede1'},  # ← Agregar aquí
]
```

2. **Haz commit y push**

### **Con Variables de Entorno:**

1. **Agrega la IP a `CAMARAS_IPS` en Railway:**
```
CAMARAS_IPS=...,192.168.60.67
```

2. **El sistema intentará mapearla automáticamente** (puede no funcionar si está en la misma red que otras cámaras)

---

## 🔧 **Mover Cámara de un NUC a Otro**

### **Con config.py:**

1. **Edita `backend/config.py`:**

```python
CAMARAS_CONFIG = [
    # Cambiar 'nuc_sede1' a 'nuc_sede2'
    {'ip': '192.168.60.64', 'nombre': 'Cámara Entrada', 'nuc': 'nuc_sede2'},  # ← Cambiado
]
```

2. **Haz commit y push**

### **Con Variables de Entorno:**

⚠️ **No es posible mover explícitamente.** El mapeo es automático y no puedes controlarlo.

**Solución:** Usa `config.py` para control explícito.

---

## 📊 **Comparación de Métodos**

| Aspecto | config.py | Variables de Entorno |
|---------|-----------|---------------------|
| **Mapeo explícito** | ✅ Sí | ❌ No (automático) |
| **Misma red** | ✅ Funciona | ⚠️ Puede fallar |
| **Diferentes redes** | ✅ Funciona | ✅ Funciona |
| **Control total** | ✅ Sí | ❌ No |
| **Fácil de editar** | ✅ Archivo local | ⚠️ En Railway |
| **Versionado** | ✅ Git | ❌ No |

---

## ✅ **Recomendación Final**

### **Usa config.py si:**
- ✅ Tienes múltiples NUCs con cámaras en la misma red
- ✅ Necesitas control explícito sobre el mapeo
- ✅ Quieres versionar la configuración
- ✅ Tienes muchas cámaras y NUCs

### **Usa Variables de Entorno si:**
- ✅ Todas las cámaras están en diferentes redes
- ✅ Configuración simple y rápida
- ✅ No necesitas control explícito

---

## 🚨 **Troubleshooting**

### **Problema: "Cámara no accesible desde Railway"**

**Causa:** La cámara está mapeada al NUC incorrecto.

**Solución:**
1. Verifica el mapeo con `/api/configuracion`
2. Si usas variables de entorno, cambia a `config.py` para mapeo explícito
3. Verifica que el NUC correcto tenga acceso a esa cámara en su red local

### **Problema: "Todas las cámaras se mapean al mismo NUC"**

**Causa:** Todas las cámaras están en la misma red y usas variables de entorno.

**Solución:** Cambia a `config.py` y especifica explícitamente qué cámara pertenece a qué NUC.

---

## 📝 **Ejemplo Completo**

### **Escenario:**
- **NUC 1:** 3 cámaras en red `192.168.60.x`
- **NUC 2:** 2 cámaras en red `192.168.61.x`
- **NUC 3:** 2 cámaras en red `192.168.60.x` (misma red que NUC 1)

### **Solución con config.py:**

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
    'nuc_sede3': {
        'tailscale_ip': '100.64.0.17',
        'puerto': 5000,
        'nombre': 'NUC Sede 3',
        'red_local': '192.168.60'  # Misma red que NUC 1
    },
}

CAMARAS_CONFIG = [
    # NUC 1 - Red 192.168.60.x
    {'ip': '192.168.60.64', 'nombre': 'Cam NUC1-1', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.65', 'nombre': 'Cam NUC1-2', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cam NUC1-3', 'nuc': 'nuc_sede1'},
    
    # NUC 2 - Red 192.168.61.x
    {'ip': '192.168.61.10', 'nombre': 'Cam NUC2-1', 'nuc': 'nuc_sede2'},
    {'ip': '192.168.61.11', 'nombre': 'Cam NUC2-2', 'nuc': 'nuc_sede2'},
    
    # NUC 3 - Red 192.168.60.x (misma que NUC 1, pero diferentes IPs)
    {'ip': '192.168.60.80', 'nombre': 'Cam NUC3-1', 'nuc': 'nuc_sede3'},
    {'ip': '192.168.60.81', 'nombre': 'Cam NUC3-2', 'nuc': 'nuc_sede3'},
]
```

**Con variables de entorno, esto NO funcionaría correctamente** porque NUC 1 y NUC 3 tienen cámaras en la misma red (`192.168.60.x`), y el sistema no podría distinguirlas.

---

## 📞 **Soporte Adicional**

- 📄 **Guía completa de config.py:** Ver `GUIA_ARCHIVO_CONFIG.md`
- 📄 **Configuración múltiples NUCs:** Ver `CONFIGURACION_MULTIPLES_NUCS.md`
- 📄 **Pasos para ejecutar puente:** Ver `PASOS_EJECUTAR_PUENTE_NUC.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
