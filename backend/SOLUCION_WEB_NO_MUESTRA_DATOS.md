# 🔧 Solución: Web No Muestra Datos del API del NUC

## 🚨 **Problema**
La web está desplegada en Railway (`https://impartial-wisdom-production-3c22.up.railway.app/`) pero no muestra datos del API del NUC.

---

## ✅ **Diagnóstico**

El frontend está configurado para usar:
- `https://apptelink-vision-production.up.railway.app` (backend)

Pero el frontend está en:
- `https://impartial-wisdom-production-3c22.up.railway.app` (frontend)

---

## 🔍 **Verificar el Backend**

### **Paso 1: Verificar que el Backend está Funcionando**

Prueba directamente en tu navegador:

```
https://apptelink-vision-production.up.railway.app/api/status
```

**Deberías ver:**
```json
{
  "status": "online",
  "modo": "proxy",
  "nucs_disponibles": 1
}
```

**Si no responde:**
- El backend no está desplegado o está caído
- Ve a Railway → Backend Service → Verifica que esté activo (verde)

---

## 🔧 **Solución 1: Verificar URL del Backend**

### **Obtener la URL Correcta del Backend:**

1. Ve a Railway Dashboard: https://railway.app
2. Selecciona tu proyecto
3. Busca el servicio del **Backend** (no el frontend)
4. Haz clic en el servicio Backend
5. Ve a **Settings** → **Networking**
6. Copia la **Public Domain** del backend

### **Actualizar api.js:**

Si la URL del backend es diferente a `apptelink-vision-production.up.railway.app`, actualiza:

```javascript
const BACKEND_RAILWAY = 'https://TU-URL-BACKEND-REAL.up.railway.app';
```

---

## 🔧 **Solución 2: Verificar Variables de Entorno en Railway**

Si el frontend y backend están en el mismo proyecto de Railway, puedes usar variables de entorno:

### **En Railway → Frontend Service → Variables:**

Agrega:
```
REACT_APP_API_URL=https://apptelink-vision-production.up.railway.app
```

O si usas Vite:
```
VITE_API_URL=https://apptelink-vision-production.up.railway.app
```

---

## 🔧 **Solución 3: Verificar CORS**

El backend debe permitir peticiones desde el frontend. Verifica que `server.py` tenga:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Permitir peticiones desde cualquier origen
```

---

## 🔍 **Verificar en la Consola del Navegador**

1. Abre `https://impartial-wisdom-production-3c22.up.railway.app/`
2. Presiona `F12` → **Console**
3. Busca mensajes como:
   - `🌐 [RAILWAY] Usando backend en Railway: ...`
   - `✅ Backend en Railway está accesible`
   - O errores en rojo

4. Ve a la pestaña **Network**
5. Haz una consulta (ej: detectar cámaras)
6. Busca peticiones fallidas (aparecen en rojo)
7. Haz clic en la petición fallida y revisa:
   - **URL:** ¿Es la correcta?
   - **Status:** ¿Qué código de error muestra?
   - **Response:** ¿Qué mensaje de error aparece?

---

## 🚨 **Troubleshooting**

### **Problema 1: "Failed to fetch" o "Network error"**

**Causas posibles:**
- ❌ El backend no está desplegado
- ❌ La URL del backend es incorrecta
- ❌ Problema de CORS

**Solución:**
1. Verifica que el backend esté activo en Railway
2. Prueba la URL del backend directamente en el navegador
3. Verifica CORS en `server.py`

### **Problema 2: "CORS error"**

**Causa:** El backend no permite peticiones desde el dominio del frontend.

**Solución:**
Verifica que `server.py` tenga:
```python
CORS(app)  # O CORS(app, origins=["https://impartial-wisdom-production-3c22.up.railway.app"])
```

### **Problema 3: "404 Not Found"**

**Causa:** El endpoint no existe o la URL está mal formada.

**Solución:**
1. Verifica que la URL sea: `https://apptelink-vision-production.up.railway.app/api/status`
2. Prueba directamente en el navegador

### **Problema 4: "503 Service Unavailable" o "No se pudo conectar al NUC"**

**Causa:** El backend no puede conectarse al NUC vía Tailscale.

**Solución:**
1. Verifica que el puente genérico esté corriendo en el NUC
2. Verifica que Tailscale esté conectado en el NUC
3. Verifica las variables de entorno en Railway:
   - `NUC_URLS=nuc_sede1:http://100.92.50.72:5000`
   - `CAMARAS_IPS=192.168.60.65`

---

## 📋 **Checklist de Verificación**

- [ ] ✅ Backend desplegado y activo en Railway
- [ ] ✅ URL del backend correcta en `api.js`
- [ ] ✅ Backend responde a `/api/status` directamente
- [ ] ✅ CORS configurado en `server.py`
- [ ] ✅ Variables de entorno configuradas en Railway (NUC_URLS, CAMARAS_IPS)
- [ ] ✅ Puente genérico corriendo en el NUC
- [ ] ✅ Tailscale conectado en el NUC
- [ ] ✅ Consola del navegador muestra "Backend en Railway está accesible"
- [ ] ✅ Peticiones en Network tab muestran status 200

---

## 🎯 **Pasos Inmediatos**

1. **Prueba el backend directamente:**
   ```
   https://apptelink-vision-production.up.railway.app/api/status
   ```

2. **Si no responde:**
   - Ve a Railway → Backend Service
   - Verifica que esté desplegado (verde)
   - Revisa los logs para ver errores

3. **Si responde pero la web no muestra datos:**
   - Abre la consola del navegador (F12)
   - Revisa los errores
   - Verifica qué URL está usando el frontend

4. **Actualiza `api.js` si la URL del backend es diferente**

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
