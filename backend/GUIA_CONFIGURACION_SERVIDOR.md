# 🚀 Guía: Backend en Servidor + NUC Local

## 📋 **Objetivo:**
- Backend Python en servidor (Railway)
- Frontend Web en servidor (Railway/Vercel)
- Backend se conecta al NUC local para acceder a cámaras

---

## ✅ **PASO 1: Exponer NUC Local (5 minutos)**

### **Opción A: Tailscale (Recomendado)**

**En el NUC:**
```bash
# Instalar Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Iniciar
sudo tailscale up

# Copiar la IP que muestra (ej: 100.64.0.1)
tailscale ip -4
```

**En tu PC (opcional, para probar):**
- Descarga Tailscale: https://tailscale.com/download
- Inicia sesión con la misma cuenta
- Ya puedes acceder al NUC

**Resultado:** Obtienes una IP como `100.64.0.1`

---

### **Opción B: ZeroTier**

**En el NUC:**
```bash
# Instalar ZeroTier
curl -s https://install.zerotier.com | sudo bash

# Unirse a red (crea cuenta en https://my.zerotier.com)
sudo zerotier-cli join TU_NETWORK_ID

# Ver IP asignada
zerotier-cli listnetworks
```

**Resultado:** Obtienes una IP como `10.147.20.5`

---

## ✅ **PASO 2: Iniciar Backend en el NUC**

**En el NUC:**
```bash
cd /ruta/al/backend
python server.py
```

El backend debe estar corriendo en el puerto 5000.

**Verificar:**
```bash
curl http://localhost:5000/api/status
# Debe responder: {"status": "online", ...}
```

---

## ✅ **PASO 3: Configurar Backend en Railway**

### **3.1. Variables de Entorno en Railway:**

Ve a tu proyecto en Railway → Settings → Variables

**Para un solo NUC:**
```
NUC_URL=http://100.64.0.1:5000
```

**Para múltiples NUCs (recomendado):**
```
NUC_URLS=nuc_sede1:http://100.64.0.1:5000,nuc_sede2:http://100.64.0.2:5000,nuc_sede3:http://100.64.0.3:5000
```

**Reemplaza las IPs con las que obtuviste de cada NUC (Tailscale/ZeroTier)**

📄 **Para más detalles sobre múltiples NUCs, ver:** [Configuración Múltiples NUCs](CONFIGURACION_MULTIPLES_NUCS.md)

---

### **3.2. Verificar que el Backend Funciona:**

Después de desplegar, prueba:
```bash
curl https://tu-api.railway.app/api/status
```

Debería responder con el status del backend en Railway.

---

### **3.3. Probar Conexión al NUC:**

```bash
curl https://tu-api.railway.app/api/camaras/detectar
```

Si funciona, el backend en Railway está haciendo proxy correctamente al NUC.

---

## ✅ **PASO 4: Configurar Frontend**

### **4.1. Actualizar API URL:**

En `src/config/api.js`:
```javascript
// Backend en Railway
export const API_BASE_URL = 'https://tu-api.railway.app';
```

### **4.2. Desplegar Frontend:**

**En Railway:**
- El frontend ya está desplegado
- Solo necesitas actualizar la URL del API

**O en Vercel:**
```bash
git add src/config/api.js
git commit -m "Update API URL to Railway backend"
git push
```

---

## ✅ **PASO 5: Verificar Todo**

### **Flujo Completo:**

1. **Frontend** → `https://tu-frontend.railway.app`
2. **Frontend** hace request a → `https://tu-api.railway.app/api/camaras`
3. **Backend en Railway** recibe petición
4. **Backend en Railway** hace proxy a → `http://100.64.0.1:5000/api/camaras`
5. **NUC** procesa y devuelve respuesta
6. **Backend en Railway** retorna respuesta
7. **Frontend** muestra cámaras

---

## 🔧 **Troubleshooting**

### **Error: "No se pudo conectar al NUC"**

**Causa:** El backend en Railway no puede alcanzar el NUC.

**Soluciones:**
1. Verifica que Tailscale/ZeroTier esté corriendo en el NUC
2. Verifica la IP del NUC: `tailscale ip -4` o `zerotier-cli listnetworks`
3. Verifica que el backend esté corriendo en el NUC: `curl http://localhost:5000/api/status`
4. Verifica la variable `NUC_URL` en Railway
5. Prueba desde tu PC (con Tailscale/ZeroTier instalado):
   ```bash
   curl http://100.64.0.1:5000/api/status
   ```

---

### **Error: "Timeout"**

**Causa:** La conexión al NUC es lenta o está caída.

**Soluciones:**
1. Verifica que el NUC esté encendido
2. Verifica que Tailscale/ZeroTier esté activo
3. Aumenta el timeout en `server.py` (línea de `hacer_proxy`)

---

### **Las cámaras no aparecen**

**Causa:** El NUC no puede escanear la red local.

**Verificar:**
1. El backend en el NUC debe estar en la misma red que las cámaras
2. Prueba desde el NUC directamente:
   ```bash
   curl http://localhost:5000/api/camaras/detectar
   ```

---

## 📊 **Resumen de URLs:**

| Componente | URL |
|------------|-----|
| **Frontend** | `https://tu-frontend.railway.app` |
| **Backend (Railway)** | `https://tu-api.railway.app` |
| **NUC (Tailscale)** | `http://100.64.0.1:5000` |
| **NUC (ZeroTier)** | `http://10.147.20.5:5000` |

---

## ✅ **Checklist:**

- [ ] Tailscale/ZeroTier instalado en NUC
- [ ] IP del NUC obtenida
- [ ] Backend corriendo en NUC (`python server.py`)
- [ ] Variable `NUC_URL` configurada en Railway
- [ ] Backend desplegado en Railway
- [ ] Frontend actualizado con URL del backend
- [ ] Todo funcionando ✅

---

## 🎯 **Siguiente Paso:**

1. Elige método para exponer NUC (Tailscale recomendado)
2. Sigue los pasos arriba
3. ¡Disfruta tu aplicación funcionando! 🎉

