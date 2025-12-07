# 🔍 Diagnóstico: Cámara muestra "Activa" pero no carga imagen

## ✅ Estado Actual

- ✅ **CORS:** Resuelto
- ✅ **Detección de cámaras:** Funciona (muestra "Activa")
- ❌ **Carga de imágenes:** No funciona

---

## 🔍 Pasos de Diagnóstico

### **Paso 1: Verificar en los Logs de Railway**

**Busca en Railway Dashboard → Logs cuando intentas ver la imagen:**

1. **¿Aparece el mensaje "📸 Obteniendo snapshot desde NUC"?**
   - ✅ **Sí:** El frontend está llamando al endpoint correctamente
   - ❌ **No:** El frontend no está llamando al endpoint

2. **¿Aparece "✅ Usando proxy SOCKS5" o "⚠️ NO se está usando proxy SOCKS5"?**
   - Si aparece "⚠️ NO se está usando proxy SOCKS5": El proxy no está configurado
   - Si aparece "✅ Usando proxy SOCKS5": El proxy está configurado

3. **¿Aparece algún error de timeout o conexión?**
   - `⏱️ Timeout al conectar con NUC`: Railway no puede conectarse al NUC
   - `❌ Error de conexión con NUC`: Problema de conectividad

---

### **Paso 2: Probar el Endpoint Directamente**

**Abre en el navegador:**

```
https://apptelink-vision-production.up.railway.app/api/camaras/192.168.60.65/snapshot
```

**¿Qué respuesta obtienes?**

- ✅ **JSON con `"success": true` y `"image": "data:image/..."`:** El endpoint funciona
- ❌ **JSON con `"success": false` y `"error": "..."`:** Hay un problema
- ❌ **Timeout o error 504:** Railway no puede conectarse al NUC

---

### **Paso 3: Verificar en la Consola del Navegador**

**Abre las herramientas de desarrollador (F12) → Console:**

1. **¿Hay errores al intentar cargar la imagen?**
   - Busca errores relacionados con `/api/camaras/192.168.60.65/snapshot`
   - Busca errores de CORS (aunque ya debería estar resuelto)

2. **¿El frontend está llamando al endpoint correcto?**
   - Busca peticiones a `/api/camaras/192.168.60.65/snapshot` en la pestaña Network

---

### **Paso 4: Verificar Conectividad Railway-NUC**

**Prueba el endpoint de diagnóstico:**

```
https://apptelink-vision-production.up.railway.app/api/test/nuc
```

**¿Qué respuesta obtienes?**

- ✅ **`"success": true` y `"tests": {"status": {"success": true}}`:** Railway puede conectarse al NUC
- ❌ **`"success": true` pero `"tests": {"status": {"success": false, "error": "Timeout"}}`:** Railway NO puede conectarse al NUC

---

## 🔧 Soluciones Posibles

### **Solución 1: Proxy SOCKS5 no está funcionando**

**Si los logs muestran "⚠️ NO se está usando proxy SOCKS5":**

1. Verifica que Tailscale esté conectado en Railway
2. Verifica que el proxy SOCKS5 esté habilitado en `tailscaled`
3. Revisa los logs de Railway al inicio para ver si Tailscale se conectó correctamente

---

### **Solución 2: Timeout al conectar con el NUC**

**Si los logs muestran "⏱️ Timeout al conectar con NUC":**

1. **Verifica que el puente genérico esté corriendo en el NUC:**
   ```powershell
   # En el NUC
   curl http://localhost:5000/api/status
   ```

2. **Verifica que el NUC esté online en Tailscale:**
   ```powershell
   # En el NUC
   tailscale status
   ```

3. **Verifica que el firewall permita conexiones:**
   - El puerto 5000 debe estar abierto en el firewall del NUC

---

### **Solución 3: El frontend no está llamando al endpoint**

**Si no aparecen peticiones a `/api/camaras/{ip}/snapshot` en los logs:**

1. Verifica que el frontend esté usando la URL correcta
2. Revisa la consola del navegador para ver si hay errores
3. Verifica que el botón "Capturar" o similar esté funcionando

---

## 📋 Checklist de Verificación

- [ ] ✅ Cámara muestra "Activa" (no "SIN ACCESO")
- [ ] ✅ Logs de Railway muestran "📸 Obteniendo snapshot desde NUC"
- [ ] ✅ Logs muestran "✅ Usando proxy SOCKS5" o "⚠️ NO se está usando proxy SOCKS5"
- [ ] ✅ Endpoint `/api/test/nuc` funciona
- [ ] ✅ Endpoint `/api/camaras/192.168.60.65/snapshot` funciona cuando se prueba directamente
- [ ] ✅ Frontend muestra errores en la consola del navegador (si los hay)

---

## 🎯 Siguiente Paso

**Comparte conmigo:**
1. ¿Qué aparece en los logs de Railway cuando intentas ver la imagen?
2. ¿Qué respuesta obtienes al probar el endpoint directamente?
3. ¿Qué errores aparecen en la consola del navegador?

Con esta información podré identificar exactamente dónde está el problema.
