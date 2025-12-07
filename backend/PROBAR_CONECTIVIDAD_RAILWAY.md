# 🔍 Probar Conectividad desde Railway al NUC

## 🚨 Problema Actual

**Las cámaras se detectan pero muestran "sin_acceso" porque Railway no puede conectarse al NUC para obtener snapshots.**

---

## ✅ Solución: Probar Conectividad

**He agregado un endpoint de prueba para diagnosticar la conectividad.**

### **Paso 1: Probar el Endpoint de Prueba**

**Abre en tu navegador:**

```
https://apptelink-vision-production.up.railway.app/api/test/nuc
```

**O desde PowerShell:**

```powershell
curl https://apptelink-vision-production.up.railway.app/api/test/nuc
```

**Este endpoint probará la conectividad desde Railway al NUC y te mostrará:**
- ✅ Si Railway puede conectarse al NUC
- ❌ Qué error específico está ocurriendo
- 📊 Detalles de la conexión

---

### **Paso 2: Revisar los Logs de Railway**

**Después de probar el endpoint, revisa los logs de Railway:**

**Busca mensajes como:**
- `🔍 [TEST] Probando: http://100.92.50.72:5000/api/status`
- `✅ NUC nuc_sede1 está disponible`
- `⏱️ [TEST] Timeout al conectar con...`
- `❌ [TEST] Error de conexión con...`

**Estos mensajes te dirán exactamente qué está fallando.**

---

## 🔍 Posibles Problemas y Soluciones

### **Problema 1: Railway No Puede Alcanzar el NUC a Través de Tailscale**

**Síntomas:**
- El endpoint de prueba muestra `ConnectionError` o `Timeout`
- Railway no puede conectarse a `100.92.50.72:5000`

**Posible Causa:**
- Tailscale userspace-networking puede tener limitaciones para conexiones salientes desde Railway

**Solución:**
- Verifica que Railway y NUC estén online en Tailscale Admin Console
- Verifica que el puente genérico esté corriendo en el NUC
- Verifica que el firewall esté abierto

---

### **Problema 2: El Puente No Está Escuchando Correctamente**

**Síntomas:**
- El puente responde localmente pero no desde Tailscale IP

**Solución:**
- Verifica que `puente_generico_nuc.py` use: `app.run(host='0.0.0.0', port=5000)`
- Verifica el firewall

---

## 📋 Checklist de Verificación

- [ ] ✅ Probé el endpoint: `https://apptelink-vision-production.up.railway.app/api/test/nuc`
- [ ] ✅ Revisé los logs de Railway después de probar
- [ ] ✅ Railway y NUC están online en Tailscale Admin Console
- [ ] ✅ Puente genérico corriendo en el NUC
- [ ] ✅ Firewall abierto en el NUC
- [ ] ✅ NUC responde desde IP de Tailscale localmente

---

## 🎯 Siguiente Acción

**Ahora mismo:**

1. ✅ **Abre en tu navegador:** `https://apptelink-vision-production.up.railway.app/api/test/nuc`
2. ✅ **Copia la respuesta JSON** que obtienes
3. ✅ **Revisa los logs de Railway** después de probar
4. ✅ **Comparte la respuesta y los mensajes de los logs**

**¿Qué respuesta obtienes cuando pruebas el endpoint `/api/test/nuc`?**
