# 🏗️ Arquitectura: Backend en Servidor + NUC Local

## 🎯 **Objetivo:**
- ✅ Backend Python en servidor (Railway/VPS)
- ✅ Frontend Web en servidor (Railway/Vercel)
- ✅ Backend se conecta al NUC local para acceder a cámaras

---

## 📐 **Arquitectura:**

```
┌─────────────────────────────────┐
│  INTERNET                       │
└──────────────┬──────────────────┘
               │
    ┌──────────▼──────────┐
    │  Frontend Web       │ ← Railway/Vercel
    │  (React/Expo)       │   https://tu-app.web
    └──────────┬──────────┘
               │ HTTPS
    ┌──────────▼──────────┐
    │  Backend Python     │ ← Railway/VPS
    │  (Flask API)        │   https://tu-api.railway.app
    └──────────┬──────────┘
               │ VPN/Túnel
    ┌──────────▼──────────┐
    │  NUC Local          │ ← Red Local
    │  (192.168.60.15)    │   Acceso a cámaras
    └─────────────────────┘
```

---

## ✅ **SOLUCIÓN: Backend Híbrido**

El backend en el servidor actúa como **proxy/gateway** que se conecta al NUC local.

### **Cómo Funciona:**

1. **Frontend** hace request a: `https://tu-api.railway.app/api/camaras`
2. **Backend en servidor** recibe la petición
3. **Backend** hace proxy al NUC local: `http://IP_NUC:5000/api/camaras`
4. **NUC** procesa y devuelve respuesta
5. **Backend** retorna respuesta al frontend

---

## 🔧 **Configuración:**

### **Paso 1: Exponer NUC Local**

El NUC debe ser accesible desde internet. Opciones:

**A) Tailscale (Recomendado - 5 min):**
```bash
# En el NUC:
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Obtén la IP (ej: 100.64.0.1)
```

**B) ZeroTier:**
```bash
# En el NUC:
curl -s https://install.zerotier.com | sudo bash
sudo zerotier-cli join TU_NETWORK_ID
# Obtén la IP (ej: 10.147.20.5)
```

**C) IP Pública + Port Forwarding:**
- Configura port forwarding en router
- Puerto 5000 → 192.168.60.15:5000
- Obtén IP pública del router

---

### **Paso 2: Configurar Backend en Servidor**

El backend en Railway/VPS necesita saber la URL del NUC.

**Opción A: Variable de Entorno (Recomendado)**

En Railway, agrega variable:
```
NUC_URL=http://100.64.0.1:5000
```

**Opción B: Archivo de Configuración**

Crea `backend/config.py`:
```python
import os

# URL del NUC local (vía VPN/Túnel)
NUC_URL = os.getenv('NUC_URL', 'http://192.168.60.15:5000')

# Modo: 'local' o 'proxy'
MODO = os.getenv('MODO', 'proxy')
```

---

### **Paso 3: Modificar Backend para Proxy**

El backend debe detectar si está en servidor o local y hacer proxy cuando sea necesario.

Ver: `backend/server_proxy.py` (se creará)

---

## 📝 **Implementación:**

### **Backend en Servidor (Railway):**

1. **Variables de Entorno:**
   ```
   NUC_URL=http://100.64.0.1:5000  # IP del NUC vía VPN
   MODO=proxy
   ```

2. **Backend hace proxy:**
   - Recibe petición del frontend
   - Hace request al NUC
   - Retorna respuesta

### **Backend Local (NUC):**

1. **Corre normalmente:**
   ```bash
   python server.py
   ```

2. **Accede directamente a cámaras:**
   - Escanea red 192.168.60.x
   - Procesa imágenes
   - Devuelve resultados

---

## 🚀 **Pasos de Deployment:**

### **1. Backend en Railway:**

```bash
# En Railway, configura:
NUC_URL=http://TU_IP_NUC:5000
MODO=proxy
```

### **2. Frontend en Railway/Vercel:**

```javascript
// En src/config/api.js
export const API_BASE_URL = 'https://tu-api.railway.app';
```

### **3. NUC Local:**

- Instala Tailscale/ZeroTier
- Inicia backend: `python server.py`
- Obtén IP de VPN

---

## ✅ **Ventajas:**

- ✅ Backend y Frontend en servidores (escalables)
- ✅ NUC local accede a cámaras directamente
- ✅ Frontend accesible desde cualquier lugar
- ✅ Backend accesible desde cualquier lugar
- ✅ Separación de responsabilidades

---

## 📊 **Flujo Completo:**

```
Usuario → Frontend (Railway)
           ↓
        Backend (Railway)
           ↓
        VPN/Túnel
           ↓
        NUC Local
           ↓
        Cámaras (192.168.60.x)
```

---

## 🎯 **Siguiente Paso:**

1. Elige método para exponer NUC (Tailscale recomendado)
2. Configura variable NUC_URL en Railway
3. Modifica backend para hacer proxy
4. Despliega frontend apuntando al backend en servidor

