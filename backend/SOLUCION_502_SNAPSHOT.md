# 🔧 Solución: Error 502 al Obtener Snapshots

## 🚨 Problema

**El frontend funciona correctamente:**
- ✅ Se conecta a Railway
- ✅ Detecta las cámaras
- ✅ Obtiene la lista de cámaras

**Pero cuando intenta obtener el snapshot (imagen), aparece error 502.**

---

## 🔍 Diagnóstico: Revisar Logs de Railway

**El error 502 ocurre cuando Railway intenta conectarse al NUC para obtener el snapshot.**

### **Paso 1: Revisar Logs de Railway**

**En Railway Dashboard → Logs, busca mensajes cuando intentas ver una cámara:**

**Busca específicamente:**
- `📸 Obteniendo snapshot desde NUC: http://100.92.50.72:5000/api/camaras/192.168.60.65/snapshot`
- `❌ Error de conexión con NUC: ...`
- `⏱️ Timeout al conectar con NUC: ...`
- `ConnectTimeoutError`
- `Connection refused`

**Estos mensajes te dirán exactamente qué está fallando.**

---

## ✅ Posibles Causas y Soluciones

### **Causa 1: Railway No Puede Alcanzar el NUC a Través de Tailscale**

**Síntomas:**
- Logs muestran: `ConnectTimeoutError` o `Connection refused`
- Railway no puede conectarse a `100.92.50.72:5000`

**Solución:**

1. **Verifica que el NUC esté en la misma red Tailscale:**
   ```powershell
   # En el NUC
   tailscale status
   ```
   - Debe mostrar el NUC como "online"
   - Debe mostrar Railway como "online" también

2. **Verifica que Railway pueda alcanzar el NUC:**
   - En Tailscale Admin Console, verifica que ambas máquinas estén "Online"
   - Railway: IP `100.71.162.68`
   - NUC: IP `100.92.50.72`

3. **Prueba la conectividad desde Railway:**
   - En los logs de Railway, deberías ver intentos de conexión
   - Si falla, puede ser un problema de routing en Tailscale

---

### **Causa 2: El Puente Genérico No Está Corriendo en el NUC**

**Síntomas:**
- Logs muestran: `Connection refused`
- El puerto 5000 no responde

**Solución:**

1. **Verifica en el NUC:**
   ```powershell
   # En el NUC
   netstat -ano | findstr :5000
   ```

2. **Si no está corriendo, inicia el puente:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   .\ejecutar_puente_silencioso.bat
   ```

---

### **Causa 3: El Firewall del NUC Está Bloqueando**

**Síntomas:**
- Logs muestran: `Connection refused` o timeout
- El puente está corriendo pero no responde desde fuera

**Solución:**

1. **Abre el firewall en el NUC:**
   ```powershell
   # Ejecuta como Administrador
   .\abrir_firewall_ps1.ps1
   ```

---

### **Causa 4: El Endpoint de Snapshot Falla en el NUC**

**Síntomas:**
- Railway se conecta al NUC, pero el snapshot falla
- Logs muestran errores del endpoint `/api/camaras/<ip>/snapshot`

**Solución:**

1. **Verifica que OpenCV esté instalado en el NUC:**
   ```powershell
   # En el NUC
   python -c "import cv2; print('OpenCV OK')"
   ```

2. **Si no está instalado:**
   ```powershell
   pip install opencv-python-headless
   ```

3. **Prueba el endpoint localmente en el NUC:**
   ```powershell
   curl http://localhost:5000/api/camaras/192.168.60.65/snapshot
   ```

---

## 🔍 Verificación Paso a Paso

### **Paso 1: Verificar en Tailscale Admin Console**

1. **Ve a:** https://login.tailscale.com/admin/machines
2. **Verifica que ambas máquinas estén "Online":**
   - Railway: IP `100.71.162.68`
   - NUC: IP `100.92.50.72`

**Si ambas están online:** ✅ Tailscale está funcionando

---

### **Paso 2: Verificar Puente en el NUC**

**En el NUC:**

```powershell
# Verificar que está corriendo
netstat -ano | findstr :5000

# Probar localmente
curl http://localhost:5000/api/status

# Probar desde IP de Tailscale
curl http://100.92.50.72:5000/api/status
```

**Si funciona localmente pero no desde Tailscale IP:** Problema de firewall o routing

---

### **Paso 3: Revisar Logs de Railway en Tiempo Real**

1. **Abre Railway Dashboard → Logs**
2. **Abre el frontend en otra pestaña**
3. **Intenta ver una cámara** (esto generará una petición)
4. **Inmediatamente revisa los logs de Railway**

**Busca mensajes como:**
- `📸 Obteniendo snapshot desde NUC: ...`
- `❌ Error de conexión...`
- `⏱️ Timeout...`

---

## 📋 Checklist de Diagnóstico

- [ ] ✅ Railway está online en Tailscale (IP: 100.71.162.68)
- [ ] ✅ NUC está online en Tailscale (IP: 100.92.50.72)
- [ ] ✅ Puente genérico corriendo en el NUC (puerto 5000)
- [ ] ✅ Firewall abierto en el NUC
- [ ] ✅ OpenCV instalado en el NUC
- [ ] ✅ Endpoint de snapshot funciona localmente en el NUC
- [ ] ✅ Revisé los logs de Railway cuando intento obtener snapshot

---

## 🎯 Siguiente Acción

**Ahora mismo:**

1. ✅ **Abre Railway Dashboard → Logs**
2. ✅ **Abre el frontend y intenta ver una cámara**
3. ✅ **Inmediatamente revisa los logs de Railway**
4. ✅ **Busca mensajes relacionados con el snapshot**
5. ✅ **Copia los mensajes de error que veas**

**¿Qué mensajes ves en los logs de Railway cuando intentas obtener un snapshot?**
