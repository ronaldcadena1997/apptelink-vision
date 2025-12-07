# 🔍 Diagnóstico Detallado del Error 502

## 🚨 Problema

**No aparecen peticiones a `/api/camaras/<ip>/snapshot` en los logs de Railway, pero el frontend muestra error 502.**

---

## 🔍 Paso 1: Revisar Consola del Navegador

**El error 502 puede estar ocurriendo antes de que la petición llegue al backend.**

1. **Abre el frontend:** https://impartial-wisdom-production-3c22.up.railway.app
2. **Abre la consola del navegador:**
   - Presiona `F12` o `Ctrl + Shift + I`
   - Ve a la pestaña **"Console"**
3. **Intenta ver una cámara** (haz clic en una cámara o botón de capturar)
4. **Busca en la consola:**
   - ¿Qué URL está intentando acceder?
   - ¿Qué error exacto aparece?
   - ¿Aparece `502 Bad Gateway`?

**Ejemplo de lo que deberías ver:**
```
GET https://apptelink-vision-production.up.railway.app/api/camaras/192.168.60.65/snapshot 502 (Bad Gateway)
```

---

## 🔍 Paso 2: Revisar Pestaña Network del Navegador

1. **En la consola del navegador, ve a la pestaña "Network"**
2. **Intenta ver una cámara nuevamente**
3. **Busca la petición a `/api/camaras/<ip>/snapshot`**
4. **Haz clic en la petición y revisa:**
   - **Status:** ¿Qué código de estado muestra? (502, 503, 504, etc.)
   - **Response:** ¿Qué mensaje de error muestra?
   - **Headers:** ¿Qué headers tiene la petición?

**Esto te dirá exactamente qué está fallando.**

---

## 🔍 Paso 3: Revisar Logs de Railway en Tiempo Real

**Cuando intentas obtener un snapshot:**

1. **Abre Railway Dashboard → Logs** (en una pestaña)
2. **Abre el frontend** (en otra pestaña)
3. **Intenta ver una cámara** (haz clic en capturar snapshot)
4. **Inmediatamente revisa los logs de Railway**

**Busca específicamente:**
- `📸 Obteniendo snapshot desde NUC: http://100.92.50.72:5000/api/camaras/192.168.60.65/snapshot`
- `❌ Error de conexión con NUC: ...`
- `⏱️ Timeout al conectar con NUC: ...`
- `GET /api/camaras/192.168.60.65/snapshot`

**Si NO ves ningún mensaje relacionado con snapshot:**
- La petición está fallando antes de llegar al backend
- Puede ser un problema de CORS o de routing en Railway

---

## ✅ Posibles Causas

### **Causa 1: La Petición No Llega al Backend**

**Síntomas:**
- No aparece ninguna petición en los logs de Railway
- El error 502 aparece inmediatamente en el navegador

**Solución:**
- Verifica que la URL del backend sea correcta
- Verifica que Railway esté funcionando: `https://apptelink-vision-production.up.railway.app/api/status`

---

### **Causa 2: Railway No Puede Conectarse al NUC**

**Síntomas:**
- Aparece `📸 Obteniendo snapshot desde NUC: ...` en los logs
- Luego aparece `❌ Error de conexión...` o `⏱️ Timeout...`

**Solución:**
- Verifica que Railway y NUC estén online en Tailscale
- Verifica que el puente genérico esté corriendo en el NUC
- Verifica que el firewall esté abierto

---

### **Causa 3: El Endpoint de Snapshot Falla en el NUC**

**Síntomas:**
- Railway se conecta al NUC
- Pero el endpoint `/api/camaras/<ip>/snapshot` falla

**Solución:**
- Verifica que OpenCV esté instalado en el NUC
- Prueba el endpoint localmente en el NUC

---

## 📋 Checklist de Diagnóstico

- [ ] ✅ Revisé la consola del navegador (F12)
- [ ] ✅ Revisé la pestaña Network del navegador
- [ ] ✅ Vi qué URL está intentando acceder el frontend
- [ ] ✅ Vi el código de estado exacto (502, 503, 504, etc.)
- [ ] ✅ Revisé los logs de Railway en tiempo real cuando intento obtener snapshot
- [ ] ✅ Busqué mensajes relacionados con snapshot en los logs

---

## 🎯 Siguiente Acción

**Ahora mismo:**

1. ✅ **Abre el frontend y la consola del navegador (F12)**
2. ✅ **Ve a la pestaña "Network"**
3. ✅ **Intenta ver una cámara**
4. ✅ **Busca la petición a `/api/camaras/<ip>/snapshot`**
5. ✅ **Haz clic en la petición y revisa:**
   - Status code
   - Response (mensaje de error)
   - Request URL
6. ✅ **Copia esa información y compártela**

**¿Qué ves en la pestaña Network del navegador cuando intentas obtener un snapshot?**
