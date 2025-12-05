# 🔧 Solución: Frontend No Muestra Datos

## 🚨 **Problema**
El backend en Railway está funcionando correctamente (según los logs), pero cuando abres la web y haces consultas, no aparece nada.

---

## ✅ **Causa Principal**

El frontend está apuntando a una **IP local** en lugar de la **URL de Railway**.

---

## 🔧 **Solución: Actualizar api.js**

### **Paso 1: Obtener la URL de Railway**

1. Ve a Railway Dashboard: https://railway.app
2. Selecciona tu proyecto
3. Ve a tu servicio (Backend)
4. Haz clic en **Settings** → **Networking**
5. Copia la **Public Domain** (ejemplo: `apptelink-vision-production.up.railway.app`)

### **Paso 2: Actualizar api.js**

Abre el archivo:
```
src/config/api.js
```

**Opción A - Si ya está actualizado automáticamente:**
El archivo ya detecta automáticamente si estás en producción y usa Railway.

**Opción B - Configuración manual:**

Si necesitas configurarlo manualmente, busca esta línea:

```javascript
const BACKEND_RAILWAY = 'https://apptelink-vision-production.up.railway.app';
```

**Reemplaza con tu URL real de Railway** (la que copiaste en el Paso 1).

---

## 🔍 **Verificar que Está Configurado Correctamente**

### **1. Abre la consola del navegador:**

- Presiona `F12` en tu navegador
- Ve a la pestaña **Console**

### **2. Deberías ver:**

```
🌐 Usando backend en Railway: https://tu-url.up.railway.app
```

Si ves esto, está usando Railway correctamente.

Si ves:
```
🏠 Usando backend local: http://192.168.60.8:5000
```

Entonces está usando la IP local (incorrecto para producción web).

---

## 🚨 **Troubleshooting**

### **Problema 1: "CORS error" o "Network error"**

**Causa:** El backend en Railway no permite peticiones desde tu dominio.

**Solución:** El backend ya tiene CORS habilitado, pero verifica:

1. En Railway, verifica los logs
2. Prueba directamente la URL:
   ```
   https://tu-backend.up.railway.app/api/status
   ```
3. Debe responder con JSON

### **Problema 2: "Failed to fetch"**

**Causas posibles:**
- ❌ La URL de Railway es incorrecta
- ❌ El backend no está desplegado
- ❌ Problemas de red

**Solución:**
1. Verifica que la URL de Railway sea correcta
2. Prueba la URL directamente en el navegador
3. Verifica los logs de Railway

### **Problema 3: "No se encuentran cámaras"**

**Causas posibles:**
- ❌ El puente genérico no está corriendo en el NUC
- ❌ Tailscale no está conectado
- ❌ Las variables de entorno en Railway no están configuradas

**Solución:**
1. En el NUC, ejecuta: `.\verificar_servicios.bat`
2. Verifica que Railway tenga las variables configuradas:
   - `NUC_URLS=nuc_sede1:http://100.92.50.72:5000`
   - `CAMARAS_IPS=192.168.60.65`

### **Problema 4: "El frontend carga pero no muestra datos"**

**Causa:** El frontend está haciendo peticiones pero el backend no responde correctamente.

**Solución:**
1. Abre la consola del navegador (F12)
2. Ve a la pestaña **Network**
3. Haz una consulta en la web
4. Busca las peticiones que fallan (aparecen en rojo)
5. Haz clic en la petición fallida y revisa el error

---

## ✅ **Verificación Paso a Paso**

### **1. Verificar que Railway está funcionando:**

Abre en tu navegador:
```
https://tu-backend.up.railway.app/api/status
```

**Debe responder:**
```json
{
  "status": "online",
  "modo": "proxy",
  "nucs_disponibles": 1
}
```

### **2. Verificar que el frontend apunta a Railway:**

1. Abre tu aplicación web
2. Presiona `F12` → **Console**
3. Debe aparecer: `🌐 Usando backend en Railway: https://...`

### **3. Verificar peticiones:**

1. Presiona `F12` → **Network**
2. Haz una consulta (ej: detectar cámaras)
3. Busca peticiones a `/api/camaras/detectar`
4. Verifica que la URL sea: `https://tu-backend.up.railway.app/api/camaras/detectar`
5. Verifica que el status sea `200 OK`

---

## 📝 **Configuración Correcta de api.js**

El archivo `api.js` ahora está configurado para:

1. **Detectar automáticamente** si estás en producción o desarrollo
2. **Usar Railway** cuando estás en producción web
3. **Usar IP local** cuando estás en desarrollo local

**No necesitas cambiar nada manualmente** si:
- ✅ Estás accediendo desde internet (no localhost)
- ✅ El archivo ya tiene la URL de Railway configurada

---

## 🔄 **Si Necesitas Cambiar la URL Manualmente**

Si la detección automática no funciona, puedes forzar el uso de Railway:

```javascript
// Forzar uso de Railway (comentar las otras opciones)
export const API_BASE_URL = 'https://apptelink-vision-production.up.railway.app';
```

**⚠️ Reemplaza con tu URL real de Railway**

---

## 📋 **Checklist de Verificación**

- [ ] ✅ Backend en Railway está desplegado y activo
- [ ] ✅ URL de Railway obtenida (Settings → Networking → Public Domain)
- [ ] ✅ `api.js` tiene la URL de Railway configurada
- [ ] ✅ Consola del navegador muestra "Usando backend en Railway"
- [ ] ✅ Endpoint `/api/status` responde correctamente desde Railway
- [ ] ✅ Peticiones en Network tab muestran URLs de Railway
- [ ] ✅ El puente genérico está corriendo en el NUC
- [ ] ✅ Tailscale está conectado en el NUC

---

## 🎯 **Siguiente Paso**

Una vez que `api.js` esté actualizado:

1. **Haz commit y push:**
   ```powershell
   git add src/config/api.js
   git commit -m "Actualizar api.js para usar Railway en producción"
   git push
   ```

2. **Si el frontend está en Railway:**
   - Railway se actualizará automáticamente
   - Espera 2-3 minutos

3. **Si el frontend está local:**
   - Recarga la página (Ctrl + F5)
   - Verifica en la consola que use Railway

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
