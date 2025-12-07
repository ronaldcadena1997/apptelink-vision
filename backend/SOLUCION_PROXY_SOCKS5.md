# 🔧 Solución: Configurar Proxy SOCKS5 para Tailscale

## 🚨 Problema

**Railway no puede conectarse al NUC a través de Tailscale userspace-networking porque las aplicaciones no están usando el proxy SOCKS5.**

**Tailscale userspace-networking requiere que las aplicaciones usen un proxy SOCKS5 para hacer conexiones salientes a otros dispositivos Tailscale.**

---

## ✅ Solución Implementada

**He configurado:**

1. ✅ **Proxy SOCKS5 en Tailscale** (se habilita automáticamente en userspace-networking)
2. ✅ **Variables de entorno** para el proxy
3. ✅ **Código Python** para usar el proxy en todas las peticiones al NUC
4. ✅ **Dependencias** (`requests[socks]` y `PySocks`)

---

## 📤 Paso 1: Subir los Cambios

**Ejecuta:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\subir_cambios_proxy.bat
```

**O manualmente:**

```powershell
git add backend/server.py backend/start_with_tailscale.sh backend/requirements.txt
git commit -m "Configurar proxy SOCKS5 para Tailscale userspace-networking"
git push
```

---

## ⏳ Paso 2: Esperar Redespliegue

**Railway se redesplegará automáticamente (2-3 minutos).**

**En los logs de Railway, busca:**

```
✅ Proxy SOCKS5 de Tailscale detectado y configurado
```

**O:**

```
⚠️  Proxy SOCKS5 no disponible, usando conexiones directas
```

---

## ✅ Paso 3: Probar el Endpoint de Prueba

**Después del redespliegue, prueba:**

```
https://apptelink-vision-production.up.railway.app/api/test/nuc
```

**Ahora deberías ver:**

```json
{
  "success": true,
  "resultados": [{
    "nuc": "nuc_sede1",
    "tests": {
      "status": {
        "success": true,
        "status_code": 200,
        "response": {...}
      }
    }
  }]
}
```

**Si funciona:** ✅ El proxy está funcionando

**Si aún falla:** Revisa los logs para ver si el proxy se detectó correctamente

---

## 🔍 Verificación en Logs

**En Railway Dashboard → Logs, busca:**

### ✅ Si Funciona:

```
✅ Proxy SOCKS5 de Tailscale detectado y configurado
📸 Obteniendo snapshot desde NUC: http://100.92.50.72:5000/api/camaras/...
   Usando proxy SOCKS5 para conexión a través de Tailscale
✅ Snapshot obtenido exitosamente
```

### ❌ Si No Funciona:

```
⚠️  Proxy SOCKS5 no disponible, usando conexiones directas
⏱️ Timeout al conectar con NUC: ...
```

**Si el proxy no se detecta:**
- El proxy SOCKS5 puede no estar disponible en el puerto 1080
- Puede necesitar más tiempo para iniciarse

---

## 📋 Checklist

- [ ] ✅ Cambios pusheados a GitHub
- [ ] ✅ Railway redesplegado
- [ ] ✅ Logs muestran "Proxy SOCKS5 detectado" o "Proxy no disponible"
- [ ] ✅ Endpoint `/api/test/nuc` funciona
- [ ] ✅ Frontend muestra imágenes (no "sin_acceso")

---

## 🎯 Siguiente Acción

**Ahora mismo:**

1. ✅ **Sube los cambios:** `.\subir_cambios_proxy.bat`
2. ✅ **Espera a que Railway se redesplegue (2-3 minutos)**
3. ✅ **Revisa los logs** para ver si el proxy se detectó
4. ✅ **Prueba el endpoint:** `/api/test/nuc`
5. ✅ **Prueba el frontend** para ver las imágenes

**¿Puedes subir los cambios y probar nuevamente?**
