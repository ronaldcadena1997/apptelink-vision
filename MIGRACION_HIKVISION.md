# 🔄 Guía de Migración: Arquitectura Actual → Estilo Hikvision

## 📋 **Resumen de Cambios**

Esta migración elimina la necesidad de Tailscale en Railway y simplifica la arquitectura.

---

## ✅ **PASO 1: Actualizar Backend en Railway**

### **1.1. Cambiar Dockerfile**

**Opción A: Renombrar archivo**
```bash
# En Railway, renombra Dockerfile a Dockerfile.old
# Y renombra Dockerfile.hikvision a Dockerfile
```

**Opción B: Configurar en Railway**
1. Ve a Railway → Backend Service → Settings
2. En "Dockerfile Path", cambia a: `Dockerfile.hikvision`
3. O simplemente renombra `Dockerfile.hikvision` a `Dockerfile`

### **1.2. Eliminar Variables de Entorno (Opcional)**

Ya no necesitas:
- ❌ `TAILSCALE_AUTHKEY`
- ❌ `NUC_URLS`
- ❌ `NUC_URL`

Puedes eliminarlas de Railway (o dejarlas, no harán daño).

### **1.3. Agregar Redis (Recomendado)**

1. Ve a Railway → Tu proyecto
2. Click en **"+ New"** → **"Database"** → **"Add Redis"**
3. Railway creará automáticamente `REDIS_URL`

**Nota:** Si no agregas Redis, el sistema usará memoria (se perderá al reiniciar).

### **1.4. Desplegar**

Railway detectará los cambios automáticamente y desplegará.

**Verifica en los logs:**
```
✅ Servidor listo para recibir conexiones de NUCs
```

---

## ✅ **PASO 2: Configurar NUC Agent**

### **2.1. Instalar Dependencias**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
pip install python-socketio
```

### **2.2. Configurar Variables**

Crea un archivo `.env` en `backend` o configura variables de entorno:

```env
SERVER_URL=https://apptelink-vision-production.up.railway.app
NUC_ID=nuc_sede1
CAMARAS_IPS=192.168.60.65
USUARIO_CAMARAS=admin
CONTRASENA_CAMARAS=citikold.2020
INTERVALO_SNAPSHOT=30
```

### **2.3. Detener el API Anterior**

Si tienes `puente_generico_nuc.py` corriendo:
```powershell
# Detener procesos Python
taskkill /F /IM python.exe
```

### **2.4. Iniciar NUC Agent**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\ejecutar_nuc_agent_hikvision.bat
```

**Deberías ver:**
```
✅ Conectado al servidor central: https://...
✅ Servidor confirmó conexión
📸 Capturando snapshot de 192.168.60.65...
✅ Snapshot enviado: 192.168.60.65
```

### **2.5. Configurar Inicio Automático**

```powershell
.\configurar_nuc_agent_automatico.bat
```

---

## ✅ **PASO 3: Verificar Funcionamiento**

### **3.1. Verificar Backend**

1. Ve a Railway → Logs
2. Deberías ver: `✅ NUC conectado: nuc_sede1`

### **3.2. Verificar Frontend**

1. Abre el frontend en el navegador
2. Las cámaras deberían aparecer automáticamente
3. Los snapshots se actualizan cada 30 segundos

### **3.3. Verificar NUC Agent**

El NUC Agent debería mostrar:
- ✅ Conexión exitosa
- ✅ Snapshots enviados periódicamente
- ✅ Sin errores de conexión

---

## 🔄 **Rollback (Si Algo Sale Mal)**

Si necesitas volver a la arquitectura anterior:

1. **En Railway:**
   - Cambia `Dockerfile` de vuelta al original
   - Restaura variables `TAILSCALE_AUTHKEY` y `NUC_URLS`

2. **En el NUC:**
   - Detén el NUC Agent
   - Inicia `puente_generico_nuc.py` de nuevo

---

## 📊 **Comparación: Antes vs Después**

| Aspecto | Antes (Tailscale) | Después (Hikvision) |
|---------|-------------------|---------------------|
| **Tailscale en Railway** | ✅ Necesario | ❌ No necesario |
| **Conexión** | Servidor → NUC | NUC → Servidor |
| **Complejidad** | Alta (proxy SOCKS5) | Baja (WebSocket simple) |
| **Tiempo Real** | ⚠️ Con delay | ✅ Instantáneo |
| **Escalabilidad** | Media | Alta |

---

## 🎯 **Ventajas de la Nueva Arquitectura**

- ✅ **Más simple:** No necesita Tailscale en Railway
- ✅ **Más confiable:** El NUC inicia la conexión (más fácil de firewall)
- ✅ **Tiempo real:** WebSocket para comunicación instantánea
- ✅ **Escalable:** Fácil agregar más NUCs
- ✅ **Similar a Hikvision:** Arquitectura probada

---

## 📝 **Notas Importantes**

- **El NUC Agent debe estar corriendo siempre** para que el sistema funcione
- **No necesitas Tailscale en Railway** (solo en el NUC si quieres acceso remoto)
- **Redis es opcional** pero recomendado para persistencia
- **El frontend no cambia** (sigue usando la misma API)

---

**¿Listo para migrar?** Sigue los pasos en orden y verifica cada uno.
