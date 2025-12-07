# 🔧 Solución: "sin_acceso" en Cámaras

## 🚨 Problema

Las cámaras aparecen detectadas pero muestran **"sin_acceso"** en lugar de la imagen.

**Esto significa:**
- ✅ El backend en Railway puede conectarse al NUC
- ✅ El NUC puede detectar las cámaras
- ❌ El snapshot (imagen) no se puede obtener

---

## 🔍 Diagnóstico

### Paso 1: Verificar OpenCV en el NUC

**El endpoint de snapshot requiere OpenCV para capturar imágenes desde RTSP.**

**Ejecuta en el NUC:**

```powershell
# Verificar si OpenCV está instalado
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

**Si sale error:** OpenCV no está instalado.

**Instalar OpenCV:**

```powershell
pip install opencv-python-headless
```

**O ejecuta el script automático:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
.\verificar_opencv.bat
```

---

### Paso 2: Probar Snapshot Localmente

**En el NUC, prueba el endpoint de snapshot directamente:**

```powershell
# Probar snapshot localmente
pero
```

**Debe responder con:**
```json
{
  "success": true,
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "timestamp": "2025-12-05T...",
  "ip": "192.168.60.65"
}
```

**Si responde con error:**
- Verifica que OpenCV esté instalado
- Verifica que la cámara esté accesible desde el NUC
- Verifica las credenciales de la cámara

---

### Paso 3: Verificar que Railway puede Conectarse

**El problema más común:** Railway no puede conectarse al NUC para obtener snapshots.

**Revisa los logs de Railway:**
1. Ve a Railway Dashboard
2. Selecciona tu proyecto de **backend**
3. Abre la pestaña **"Logs"**
4. Busca mensajes como:
   - `📸 Obteniendo snapshot desde NUC: http://100.92.50.72:5000/api/camaras/...`
   - `❌ Error de conexión con NUC: ...`
   - `⏱️ Timeout al conectar con NUC: ...`

**Si ves errores de conexión:**
- El firewall puede estar bloqueando (ya lo abrimos)
- Railway no tiene acceso a Tailscale (problema principal)

---

## ✅ Soluciones

### Solución 1: Instalar OpenCV (Si no está instalado)

```powershell
pip install opencv-python-headless
```

**Luego reinicia el puente genérico:**

```powershell
# Detener el puente actual
taskkill /F /IM pythonw.exe /FI "COMMANDLINE eq *puente_generico_nuc.py*" 2>nul
taskkill /F /IM python.exe /FI "COMMANDLINE eq *puente_generico_nuc.py*" 2>nul

# Reiniciar
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
.\ejecutar_puente_silencioso.bat
```

---

### Solución 2: Verificar Conectividad desde Railway

**El problema principal:** Railway no puede usar Tailscale directamente.

**Opciones:**

#### Opción A: Configurar Tailscale en Railway (Complejo)

Requiere modificar el Dockerfile de Railway para instalar Tailscale.

#### Opción B: Usar Túnel Público (Más Simple)

Exponer el NUC usando un servicio como:
- **ngrok** (gratis, fácil de usar)
- **Cloudflare Tunnel** (gratis, más estable)
- **LocalTunnel** (gratis, simple)

---

### Solución 3: Verificar Credenciales de Cámara

**Si OpenCV está instalado pero el snapshot falla:**

**Verifica las credenciales en `puente_generico_nuc.py`:**

```python
# Líneas 216-217
usuario = os.getenv('USUARIO_CAMARAS', 'admin')
contrasena = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')
```

**O configura variables de entorno en el NUC:**

```powershell
# En PowerShell
$env:USUARIO_CAMARAS = "admin"
$env:CONTRASENA_CAMARAS = "citikold.2020"
```

---

## 🧪 Pruebas de Diagnóstico

### Test 1: OpenCV

```powershell
python -c "import cv2; print('OpenCV OK:', cv2.__version__)"
```

### Test 2: Snapshot Local

```powershell
curl http://localhost:5000/api/camaras/192.168.60.65/snapshot
```

### Test 3: Snapshot desde Tailscale IP

```powershell
# Obtener IP de Tailscale
$tailscaleIP = tailscale ip -4

# Probar snapshot
curl http://$tailscaleIP:5000/api/camaras/192.168.60.65/snapshot
```

### Test 4: Verificar Logs de Railway

Revisa los logs de Railway para ver el error exacto cuando intenta obtener el snapshot.

---

## 📋 Checklist

- [ ] ✅ OpenCV instalado en el NUC: `pip install opencv-python-headless`
- [ ] ✅ Snapshot funciona localmente: `curl http://localhost:5000/api/camaras/192.168.60.65/snapshot`
- [ ] ✅ Firewall abierto (ya lo hicimos)
- [ ] ✅ Puente genérico corriendo
- [ ] ✅ Railway puede conectarse al NUC (verificar en logs)
- [ ] ✅ Credenciales de cámara correctas

---

## 🚨 Problema Principal: Railway y Tailscale

**Railway es un servicio en la nube** y no tiene Tailscale instalado por defecto.

**Para que Railway pueda conectarse al NUC:**

1. **Opción 1:** Instalar Tailscale en Railway (requiere modificar Dockerfile)
2. **Opción 2:** Usar un túnel público (ngrok, Cloudflare Tunnel, etc.)

**Si Railway no puede conectarse al NUC, verás:**
- Cámaras detectadas ✅
- Pero "sin_acceso" ❌ (porque no puede obtener snapshots)

---

## 💡 Solución Rápida

**Ejecuta en el NUC:**

```powershell
# 1. Verificar/instalar OpenCV
python -c "import cv2" 2>$null || pip install opencv-python-headless

# 2. Probar snapshot localmente
curl http://localhost:5000/api/camaras/192.168.60.65/snapshot

# 3. Si funciona localmente pero no desde Railway:
#    El problema es que Railway no puede conectarse al NUC
#    Necesitas configurar Tailscale en Railway o usar un túnel
```

---

## 📞 Siguiente Paso

**Si OpenCV está instalado y el snapshot funciona localmente:**

El problema es que **Railway no puede conectarse al NUC** a través de Tailscale.

**Opciones:**
1. Configurar Tailscale en Railway (te puedo ayudar)
2. Usar un túnel público como ngrok (más fácil)

¿Quieres que te ayude a configurar Tailscale en Railway o prefieres usar un túnel público?
