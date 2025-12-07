# 📹 Configuración Centralizada de IPs de Cámaras

## ❓ **Tu Necesidad:**
"Tengo scripts con IPs por cada cámara y debo agregar esas IPs por cada cámara. Quiero configurarlas centralmente sin modificar código en cada NUC."

## ✅ **Solución: Configuración en Railway (Variables de Entorno)**

---

## 🎯 **Arquitectura:**

```
┌─────────────────────────────────────────────────────────┐
│  Railway (Backend)                                       │
│  ✅ Variables de Entorno con IPs de cámaras              │
│  ✅ CAMARAS_IPS=192.168.60.64,192.168.60.65,...        │
│  ✅ Toda la lógica conoce las IPs                       │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP Request usando IPs configuradas
                   │ GET http://100.64.0.15:5000/proxy/192.168.60.64:554/stream
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Puente Genérico en NUC                                  │
│  ✅ NO sabe qué cámaras existen                          │
│  ✅ Solo hace proxy a cualquier IP                      │
│  ✅ NO necesita cambios                                  │
└──────────────────┬──────────────────────────────────────┘
                   │ Acceso directo
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Cámaras (IPs configuradas en Railway)                  │
│  192.168.60.64, 192.168.60.65, etc.                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 **PASO 1: Configurar IPs de Cámaras en Railway**

### **En Railway → Backend Service → Variables:**

**Agrega esta variable:**

```
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66,192.168.60.67
```

**Formato:**
- **Lista simple:** `ip1,ip2,ip3,ip4`
- **Con nombres (opcional):** `camara1:192.168.60.64,camara2:192.168.60.65`

**📝 Ejemplo con múltiples cámaras:**
```
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66,192.168.60.67,192.168.60.68
```

---

## 📋 **PASO 2: Modificar Backend para Usar IPs Configuradas**

El backend en Railway leerá las IPs desde la variable de entorno y las usará para hacer peticiones al puente genérico.

### **Ejemplo de código en Railway:**

```python
import os

# Leer IPs de cámaras desde variable de entorno
CAMARAS_IPS_STR = os.getenv('CAMARAS_IPS', '')
CAMARAS = [ip.strip() for ip in CAMARAS_IPS_STR.split(',') if ip.strip()]

# IP del NUC (Tailscale)
NUC_TAILSCALE_IP = os.getenv('NUC_TAILSCALE_IP', '100.64.0.15')
NUC_PORT = 5000

@app.route('/api/camaras', methods=['GET'])
def listar_camaras():
    """Lista todas las cámaras configuradas"""
    return jsonify({
        "success": True,
        "camaras": [
            {"ip": ip, "nombre": f"Camara_{i+1}"} 
            for i, ip in enumerate(CAMARAS)
        ]
    })

@app.route('/api/camaras/<ip>/snapshot', methods=['GET'])
def obtener_snapshot(ip):
    """Obtiene snapshot de una cámara usando el puente genérico"""
    if ip not in CAMARAS:
        return jsonify({"success": False, "error": "Cámara no configurada"}), 404
    
    # Usar puente genérico para acceder a la cámara
    response = requests.get(
        f'http://{NUC_TAILSCALE_IP}:{NUC_PORT}/proxy/{ip}:554/stream'
    )
    return Response(response.content, mimetype='image/jpeg')
```

---

## 🔄 **Flujo Completo:**

1. **Usuario** → Frontend: "Ver cámaras"
2. **Frontend** → Backend Railway: `GET /api/camaras`
3. **Backend Railway** → Lee `CAMARAS_IPS` de variables de entorno
4. **Backend Railway** → Retorna lista de cámaras configuradas
5. **Usuario** → Frontend: Click en cámara
6. **Frontend** → Backend Railway: `GET /api/camaras/192.168.60.64/snapshot`
7. **Backend Railway** → Puente NUC: `GET http://100.64.0.15:5000/proxy/192.168.60.64:554/stream`
8. **Puente NUC** → Cámara: `http://192.168.60.64:554/stream`
9. **Puente NUC** → Backend Railway: Retorna imagen
10. **Backend Railway** → Frontend: Retorna imagen
11. **Frontend** → Usuario: Muestra imagen

---

## ✅ **Ventajas:**

### **1. Configuración Centralizada:**
- ✅ Todas las IPs en Railway (variables de entorno)
- ✅ NO necesitas modificar código en el NUC
- ✅ Agregas/quitas cámaras solo cambiando variables en Railway

### **2. Sin Cambios en el NUC:**
- ✅ El puente genérico NO necesita saber qué cámaras existen
- ✅ Solo hace proxy a cualquier IP que le pidas
- ✅ NO requiere actualizaciones cuando agregas cámaras

### **3. Escalable:**
- ✅ Agregas nuevas cámaras → Solo agregas IP en Railway
- ✅ Quitas cámaras → Solo quitas IP en Railway
- ✅ El código NO cambia

---

## 📝 **Ejemplo Completo de Configuración en Railway:**

### **Variables de Entorno:**

```
# IP del NUC (Tailscale)
NUC_TAILSCALE_IP=100.64.0.15

# IPs de las cámaras (separadas por comas)
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66,192.168.60.67

# O con nombres (opcional)
CAMARAS_CONFIG=camara_entrada:192.168.60.64,camara_patio:192.168.60.65,camara_garage:192.168.60.66
```

---

## 🔧 **Modificar server.py para Usar IPs Configuradas:**

Voy a crear una versión mejorada del backend que lea las IPs desde variables de entorno.

---

## 📊 **Comparación:**

| Aspecto | IPs Hardcodeadas | IPs en Variables |
|---------|------------------|------------------|
| **Dónde se configuran** | En código (cada NUC) | Railway (centralizado) |
| **Agregar cámara** | Cambiar código en NUC | Cambiar variable en Railway |
| **Múltiples NUCs** | Cambiar en cada uno | Cambiar una vez en Railway |
| **Mantenimiento** | Complejo | ⭐ Simple |

---

## ✅ **Resumen:**

- ✅ **IPs de cámaras en Railway** (variables de entorno)
- ✅ **Backend en Railway** lee las IPs y las usa
- ✅ **Puente genérico en NUC** no necesita saber qué cámaras existen
- ✅ **Agregas cámaras** → Solo cambias variable en Railway
- ✅ **NO necesitas modificar código en el NUC**

---

## 📞 **Soporte Adicional**

- 📄 **Puente genérico:** Ver `SOLUCION_PUENTE_GENERICO.md`
- 📄 **Código del puente:** Ver `puente_generico_nuc.py`
- 📄 **Conexión Tailscale:** Ver `GUIA_CONEXION_TAILSCALE_RAILWAY.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
