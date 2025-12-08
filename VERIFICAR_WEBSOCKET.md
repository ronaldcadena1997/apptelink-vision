# 🔍 Verificar: ¿El Backend está Recibiendo Snapshots?

## ❌ **Problema**
- ✅ NUC Agent envía snapshots: `✅ Snapshot capturado y enviado: 192.168.60.65 (272532 bytes)`
- ❌ Backend retorna: `"estado": "sin_acceso"`
- ❌ No se ven logs de WebSocket en Railway

---

## 🔍 **VERIFICACIÓN**

### **1. Verificar que el Backend está usando el archivo correcto**

En Railway:
1. Ve a tu proyecto
2. Verifica que el **Dockerfile** sea: `Dockerfile.hikvision`
3. Verifica que el **Start Command** esté vacío o sea: `python server_hikvision_style.py`

---

### **2. Verificar logs de WebSocket en Railway**

En Railway → Logs, busca mensajes como:
```
✅ NUC conectado: nuc_sede1
📸 Snapshot recibido: nuc_sede1 - 192.168.60.65
✅ Snapshot guardado en Redis/memoria para 192.168.60.65
```

**Si NO ves estos mensajes:**
- ❌ El backend no está recibiendo los snapshots
- ❌ Puede haber un problema con la conexión WebSocket

---

### **3. Verificar que Redis está disponible**

En Railway → Logs, busca:
```
✅ Conectado a Redis
```

O:
```
⚠️  Redis no disponible, usando memoria
```

**Si está usando memoria:**
- Los snapshots pueden perderse entre requests
- **Solución:** Agrega Redis en Railway

---

### **4. Probar endpoint directamente**

Abre en el navegador:
```
https://apptelink-vision-production.up.railway.app/api/camaras/detectar
```

**Verifica:**
- ¿El estado es "sin_acceso" o "activa"?
- ¿Hay algún campo `nuc_id`?

---

## 🔧 **SOLUCIONES**

### **Solución 1: Agregar Redis (CRÍTICO)**

Si Redis no está disponible:

1. En Railway, haz clic en **"+ New"**
2. Selecciona **"Database" → "Add Redis"**
3. Railway creará automáticamente `REDIS_URL`
4. El backend la detectará automáticamente
5. Espera 2-3 minutos
6. Reinicia el NUC Agent

**Ventajas:**
- ✅ Los snapshots persisten
- ✅ Múltiples instancias comparten datos
- ✅ No se pierden datos entre requests

---

### **Solución 2: Verificar que el Backend está corriendo**

En Railway → Logs, busca:
```
Backend Estilo Hikvision
✅ Servidor listo para recibir conexiones de NUCs
```

**Si NO ves esto:**
- El backend puede no estar usando `server_hikvision_style.py`
- Verifica el Dockerfile en Railway

---

### **Solución 3: Verificar conexión WebSocket**

El NUC Agent se conecta así:
```python
sio.connect(SERVER_URL, auth={'nuc_id': NUC_ID})
```

**Verifica en Railway logs:**
- ¿Aparece "✅ NUC conectado: nuc_sede1"?
- Si NO aparece, hay un problema con la conexión WebSocket

---

## 📋 **Checklist de Diagnóstico**

- [ ] Backend está usando `Dockerfile.hikvision`
- [ ] Backend está usando `server_hikvision_style.py`
- [ ] Redis está disponible (ver logs)
- [ ] Se ven logs de "NUC conectado" en Railway
- [ ] Se ven logs de "Snapshot recibido" en Railway
- [ ] El endpoint `/api/camaras/detectar` retorna estado correcto

---

## 🆘 **Si No Funciona**

1. **Verifica Railway:**
   - ¿El Dockerfile es `Dockerfile.hikvision`?
   - ¿Redis está agregado?

2. **Verifica logs:**
   - ¿Aparecen mensajes de WebSocket?
   - ¿Aparecen mensajes de snapshots recibidos?

3. **Prueba el endpoint:**
   - `https://apptelink-vision-production.up.railway.app/api/camaras/detectar`
   - Verifica el estado retornado

---

**¡Con estas verificaciones podrás identificar dónde está el problema!** 🔍
