# 🚀 Guía de Implementación: Arquitectura Estilo Hikvision

## 📋 **Resumen**

Esta arquitectura elimina la necesidad de Tailscale en Railway. El NUC se conecta al servidor central usando WebSocket, similar a cómo Hikvision usa Hik-Connect.

---

## 🏗️ **Arquitectura**

```
┌─────────────────────────────────┐
│  Frontend (React)              │ ← Railway
│  - Consulta API                │
│  - Recibe WebSocket updates    │
└──────────────┬──────────────────┘
               │ HTTP + WebSocket
┌──────────────▼──────────────────┐
│  Backend (Flask + SocketIO)     │ ← Railway
│  - Recibe conexiones de NUCs    │
│  - Almacena snapshots (Redis)   │
│  - Expone API para frontend    │
└──────────────┬──────────────────┘
               │ WebSocket (NUC → Servidor)
┌──────────────▼──────────────────┐
│  NUC Agent                      │ ← NUC Local
│  (nuc_agent_hikvision.py)       │
│  - Se conecta al servidor       │
│  - Envía snapshots              │
└──────────────┬──────────────────┘
               │ RTSP Local
┌──────────────▼──────────────────┐
│  Cámaras IP                     │ ← Red Local
└─────────────────────────────────┘
```

---

## ✅ **PASO 1: Actualizar Backend en Railway**

### **1.1. Actualizar `requirements.txt`**

Ya está actualizado con:
- `flask-socketio>=5.3.0`
- `python-socketio>=5.10.0`
- `eventlet>=0.33.0`
- `redis>=5.0.0`

### **1.2. Cambiar `server.py` por `server_hikvision_style.py`**

**Opción A: Renombrar archivo**
```bash
# En Railway, cambia el archivo principal
# O modifica el Dockerfile para usar server_hikvision_style.py
```

**Opción B: Actualizar `Dockerfile`**
```dockerfile
# Cambiar CMD a:
CMD ["python", "server_hikvision_style.py"]
```

### **1.3. Agregar Redis en Railway**

1. Ve a Railway → Tu proyecto
2. Click en **"+ New"** → **"Database"** → **"Add Redis"**
3. Railway creará automáticamente la variable `REDIS_URL`

### **1.4. Variables de Entorno en Railway**

No necesitas:
- ❌ `TAILSCALE_AUTHKEY` (ya no necesario)
- ❌ `NUC_URLS` (ya no necesario)

Solo necesitas:
- ✅ `REDIS_URL` (automático si agregas Redis)
- ✅ `PORT` (automático en Railway)

---

## ✅ **PASO 2: Configurar NUC Agent**

### **2.1. Instalar Dependencias en el NUC**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
pip install python-socketio opencv-python-headless
```

### **2.2. Configurar Variables de Entorno**

Crea un archivo `.env` en el directorio `backend`:

```env
SERVER_URL=https://apptelink-vision-production.up.railway.app
NUC_ID=nuc_sede1
CAMARAS_IPS=192.168.60.65
USUARIO_CAMARAS=admin
CONTRASENA_CAMARAS=citikold.2020
INTERVALO_SNAPSHOT=30
```

O configura variables de entorno del sistema:

```powershell
[System.Environment]::SetEnvironmentVariable('SERVER_URL', 'https://apptelink-vision-production.up.railway.app', 'User')
[System.Environment]::SetEnvironmentVariable('NUC_ID', 'nuc_sede1', 'User')
[System.Environment]::SetEnvironmentVariable('CAMARAS_IPS', '192.168.60.65', 'User')
```

### **2.3. Ejecutar el NUC Agent**

**Opción A: Manualmente**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\ejecutar_nuc_agent_hikvision.bat
```

**Opción B: Como Servicio Automático**

Usa el script `configurar_servicio_automatico.bat` pero modifica para usar `nuc_agent_hikvision.py`:

```batch
# En configurar_servicio_automatico.bat, cambia:
set SCRIPT_PATH=%~dp0ejecutar_nuc_agent_hikvision.bat
```

---

## ✅ **PASO 3: Verificar Funcionamiento**

### **3.1. Verificar Backend en Railway**

1. Ve a Railway → Logs del backend
2. Deberías ver:
   ```
   ✅ Servidor listo para recibir conexiones de NUCs
   ```

### **3.2. Verificar NUC Agent**

1. Ejecuta el NUC Agent
2. Deberías ver:
   ```
   ✅ Conectado al servidor central: https://...
   ✅ Servidor confirmó conexión
   📸 Capturando snapshot de 192.168.60.65...
   ✅ Snapshot enviado: 192.168.60.65
   ```

### **3.3. Verificar Frontend**

1. Abre el frontend en el navegador
2. Las cámaras deberían aparecer automáticamente
3. Los snapshots se actualizan cada 30 segundos

---

## 🔧 **Troubleshooting**

### **❌ Error: "ModuleNotFoundError: No module named 'socketio'"**

**Solución:**
```powershell
pip install python-socketio
```

### **❌ Error: "Connection refused" en el NUC Agent**

**Causa:** El backend no está corriendo o la URL es incorrecta.

**Solución:**
1. Verifica que el backend esté desplegado en Railway
2. Verifica que `SERVER_URL` sea correcta
3. Verifica que el backend use `server_hikvision_style.py`

### **❌ Error: "Redis connection failed"**

**Causa:** Redis no está configurado en Railway.

**Solución:**
1. Agrega Redis en Railway (Paso 1.3)
2. Verifica que `REDIS_URL` esté configurada automáticamente

### **❌ El NUC Agent se desconecta frecuentemente**

**Causa:** Problemas de red o timeout.

**Solución:**
1. Verifica la conexión a internet del NUC
2. Aumenta `reconnection_attempts` en `nuc_agent_hikvision.py`
3. Verifica que el firewall no bloquee WebSocket

---

## 📊 **Ventajas de Esta Arquitectura**

- ✅ **No necesita Tailscale en Railway:** Más simple
- ✅ **El NUC inicia la conexión:** Más fácil de firewall
- ✅ **Tiempo real:** WebSocket para comunicación instantánea
- ✅ **Escalable:** Fácil agregar más NUCs
- ✅ **Similar a Hikvision:** Arquitectura probada

---

## 🎯 **Próximos Pasos**

1. ✅ Actualizar backend en Railway
2. ✅ Configurar Redis
3. ✅ Ejecutar NUC Agent
4. ✅ Verificar funcionamiento
5. ✅ Configurar inicio automático del NUC Agent

---

## 📝 **Notas Importantes**

- **El NUC Agent debe estar corriendo siempre** para que el sistema funcione
- **No necesitas Tailscale en Railway** (solo en el NUC si quieres acceso remoto)
- **Redis es opcional** (puede usar memoria, pero se perderá al reiniciar)
- **El frontend no cambia** (sigue usando la misma API)

---

**¿Listo para implementar?** Sigue los pasos en orden y verifica cada uno antes de continuar.
