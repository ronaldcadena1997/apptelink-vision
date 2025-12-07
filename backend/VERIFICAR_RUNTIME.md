# 🔍 Verificar Runtime: Por Qué No Se Ejecuta el Script

## ✅ Build Correcto

**El build está funcionando correctamente:**
- ✅ Dockerfile detectado
- ✅ Script copiado: `start_with_tailscale.sh`
- ✅ Permisos de ejecución dados
- ✅ Build completado

**Pero el script NO se ejecuta cuando el contenedor inicia.**

---

## 🔍 Diagnóstico: Revisar Logs de Runtime

**Después de que el build termine, el contenedor inicia. En los logs, busca:**

### **Lo que DEBERÍAS ver:**

```
Starting Container
==========================================
Iniciando Tailscale en Railway
==========================================
[1/3] Iniciando Tailscale daemon...
```

### **Lo que ESTÁS viendo:**

```
Starting Container
 * Serving Flask app 'server'
```

**Esto significa que el script NO se está ejecutando.**

---

## 🔧 Posibles Causas

### **Causa 1: Railway Está Sobrescribiendo el CMD**

**Railway puede estar usando un comando diferente al del Dockerfile.**

**Solución:**
1. Ve a Railway Dashboard → Settings → Deploy
2. Verifica si hay algún "Start Command" configurado
3. Si hay un "Start Command", elimínalo o déjalo vacío
4. Railway debe usar el CMD del Dockerfile

---

### **Causa 2: El Script Tiene un Error que Hace que Falle Silenciosamente**

**El script puede estar fallando antes de mostrar los mensajes.**

**Solución:** Modificar el script para que muestre más información de depuración.

---

### **Causa 3: Problema con la Ruta del Script**

**El script puede no estar en la ubicación correcta.**

**Solución:** Verificar que el script esté en `/app/start_with_tailscale.sh`

---

## ✅ Solución: Verificar Start Command en Railway

### **Paso 1: Verificar Start Command**

1. **Ve a Railway Dashboard:**
   - https://railway.app
   - Selecciona tu proyecto de **backend**

2. **Abre la pestaña "Settings"**

3. **Busca la sección "Deploy" o "Start Command"**

4. **Verifica si hay un "Start Command" configurado:**
   - Si hay algo como `python server.py`, **elimínalo**
   - Debe estar **vacío** para que use el CMD del Dockerfile

---

### **Paso 2: Si Hay Start Command, Eliminarlo**

1. **Elimina cualquier "Start Command" configurado**
2. **Guarda los cambios**
3. **Railway se redesplegará automáticamente**

---

### **Paso 3: Forzar Redespliegue**

**Después de eliminar el Start Command:**

1. **Haz clic en "Redeploy"**
2. **Espera a que termine el build y el despliegue**
3. **Revisa los logs desde "Starting Container"**

**Ahora deberías ver:**
```
Starting Container
==========================================
Iniciando Tailscale en Railway
==========================================
```

---

## 📋 Checklist

- [ ] ✅ Build completado correctamente
- [ ] ✅ Script copiado en el build
- [ ] ✅ Verifiqué Settings → Deploy → Start Command
- [ ] ✅ Start Command está vacío (NO tiene `python server.py`)
- [ ] ✅ Railway redesplegado después de eliminar Start Command
- [ ] ✅ Logs muestran "Iniciando Tailscale en Railway"

---

## 🎯 Siguiente Acción

**Ahora mismo:**

1. ✅ **Ve a Railway Dashboard → Settings → Deploy**
2. ✅ **Busca "Start Command" o "Command"**
3. ✅ **Si hay algo configurado (como `python server.py`), elimínalo**
4. ✅ **Guarda los cambios**
5. ✅ **Haz "Redeploy"**
6. ✅ **Revisa los logs desde "Starting Container"**

**¿Hay algún "Start Command" configurado en Railway Dashboard → Settings → Deploy?**
