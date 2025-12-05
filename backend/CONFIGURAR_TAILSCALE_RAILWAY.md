# 🔗 Configurar Tailscale en Railway

## 📋 Resumen

Este guía te ayudará a configurar Tailscale en Railway para que pueda conectarse al NUC y obtener snapshots de las cámaras.

---

## ✅ Prerrequisitos

- ✅ Tailscale instalado y funcionando en el NUC
- ✅ IP de Tailscale del NUC: `100.92.50.72`
- ✅ Cuenta de Tailscale (gratis)

---

## 🔑 Paso 1: Obtener Auth Key de Tailscale

**Necesitas crear una "Auth Key" en Tailscale para que Railway se conecte.**

### **Opción A: Desde Tailscale Admin Console (Recomendado)**

1. **Ve a:** https://login.tailscale.com/admin/settings/keys
2. **Haz clic en "Generate auth key"**
3. **Configura:**
   - **Reusable:** ✅ Sí (para que funcione después de reinicios)
   - **Ephemeral:** ❌ No (para que sea permanente)
   - **Preauthorized:** ✅ Sí (para que se conecte automáticamente)
4. **Copia la auth key** (algo como: `tskey-auth-xxxxx-xxxxx`)

### **Opción B: Desde la línea de comandos**

```powershell
# En el NUC o cualquier máquina con Tailscale
tailscale authkey
```

**⚠️ IMPORTANTE:** Guarda esta auth key de forma segura. La necesitarás en Railway.

---

## 🚀 Paso 2: Configurar Railway

### **2.1. Renombrar Dockerfile**

**En Railway, necesitas usar el Dockerfile con Tailscale:**

**Opción A: Renombrar archivos (Recomendado)**

1. **Renombra el Dockerfile actual:**
   ```powershell
   # En tu computadora local
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   ren Dockerfile Dockerfile.original
   ren Dockerfile.tailscale Dockerfile
   ```

2. **Haz commit y push:**
   ```powershell
   git add Dockerfile Dockerfile.original start_with_tailscale.sh
   git commit -m "Agregar soporte para Tailscale en Railway"
   git push
   ```

**Opción B: Configurar en Railway Dashboard**

1. Ve a Railway Dashboard → Tu proyecto backend
2. Settings → Build
3. Cambia "Dockerfile Path" a: `backend/Dockerfile.tailscale`

---

### **2.2. Agregar Variable de Entorno en Railway**

1. **Ve a Railway Dashboard:**
   - https://railway.app
   - Selecciona tu proyecto de **backend**

2. **Abre la pestaña "Variables"**

3. **Agrega esta variable:**
   - **Nombre:** `TAILSCALE_AUTHKEY`
   - **Valor:** La auth key que obtuviste en el Paso 1
   - **Ejemplo:** `tskey-auth-xxxxx-xxxxx`

4. **Guarda los cambios**

---

### **2.3. Verificar Variables Existentes**

**Asegúrate de que estas variables estén configuradas:**

- ✅ `NUC_URLS` = `nuc_sede1:http://100.92.50.72:5000`
- ✅ `CAMARAS_IPS` = `192.168.60.65`
- ✅ `TAILSCALE_AUTHKEY` = `tskey-auth-xxxxx-xxxxx` (nueva)

---

## 🔄 Paso 3: Redesplegar en Railway

**Después de agregar la variable `TAILSCALE_AUTHKEY`:**

1. Railway detectará el cambio automáticamente
2. O puedes hacer "Redeploy" manualmente desde Railway Dashboard
3. Railway reconstruirá la imagen con Tailscale instalado
4. Railway se conectará a Tailscale usando la auth key

---

## ✅ Paso 4: Verificar que Funciona

### **4.1. Verificar en Railway Logs**

**En Railway Dashboard → Logs, busca:**

```
✅ Tailscale conectado. IP: 100.xx.xx.xx
Iniciando servidor Python
```

**Si ves errores:**
- `ERROR: TAILSCALE_AUTHKEY no está configurada` → Verifica la variable de entorno
- `tailscaled: command not found` → El Dockerfile no se aplicó correctamente

### **4.2. Verificar en Tailscale Admin Console**

1. **Ve a:** https://login.tailscale.com/admin/machines
2. **Busca una máquina nueva** con nombre como "railway-xxxxx"
3. **Verifica que esté "Online"**

### **4.3. Probar desde el Frontend**

1. **Abre el frontend:** https://impartial-wisdom-production-3c22.up.railway.app
2. **Verifica que las cámaras muestren imágenes** (no "sin_acceso")

---

## 🚨 Troubleshooting

### **Problema 1: "TAILSCALE_AUTHKEY no está configurada"**

**Solución:**
- Verifica que la variable esté en Railway Dashboard → Variables
- Asegúrate de que el nombre sea exactamente: `TAILSCALE_AUTHKEY`
- Haz "Redeploy" después de agregar la variable

---

### **Problema 2: "tailscaled: command not found"**

**Solución:**
- Verifica que el Dockerfile correcto esté en uso
- Verifica que `start_with_tailscale.sh` esté en el repositorio
- Haz push de los cambios a GitHub

---

### **Problema 3: Tailscale se conecta pero Railway aún no puede alcanzar el NUC**

**Solución:**
1. **Verifica que el NUC esté en la misma red Tailscale:**
   ```powershell
   # En el NUC
   tailscale status
   ```

2. **Verifica que Railway esté en la red Tailscale:**
   - Ve a Tailscale Admin Console → Machines
   - Busca la máquina de Railway

3. **Prueba la conectividad desde Railway logs:**
   - Railway debería poder hacer `curl http://100.92.50.72:5000/api/status`

---

### **Problema 4: La auth key expiró**

**Solución:**
- Genera una nueva auth key en Tailscale Admin Console
- Actualiza la variable `TAILSCALE_AUTHKEY` en Railway
- Haz "Redeploy"

---

## 📋 Checklist Final

- [ ] ✅ Auth key de Tailscale obtenida
- [ ] ✅ Variable `TAILSCALE_AUTHKEY` configurada en Railway
- [ ] ✅ Dockerfile con Tailscale en uso
- [ ] ✅ `start_with_tailscale.sh` en el repositorio
- [ ] ✅ Cambios pusheados a GitHub
- [ ] ✅ Railway redesplegado
- [ ] ✅ Tailscale conectado (verificar en logs)
- [ ] ✅ Railway puede conectarse al NUC (verificar en logs)
- [ ] ✅ Frontend muestra imágenes (no "sin_acceso")

---

## 🎯 Siguiente Paso

**Después de configurar Tailscale en Railway:**

1. ✅ Railway se conectará a la red Tailscale
2. ✅ Railway podrá alcanzar el NUC en `100.92.50.72:5000`
3. ✅ Railway podrá obtener snapshots de las cámaras
4. ✅ El frontend mostrará las imágenes correctamente

**¡Todo debería funcionar ahora!** 🎉

---

## 📞 Si Necesitas Ayuda

**Si algo no funciona:**
1. Revisa los logs de Railway
2. Verifica que Tailscale esté conectado en Railway
3. Verifica que el NUC esté accesible desde Tailscale
4. Revisa la sección de Troubleshooting arriba
