# 🚀 Desplegar Frontend en Railway

## ❌ **Problema Actual**
- Frontend muestra "Not Found" en `impartial-wisdom-production-3c22.up.railway.app`
- El frontend no está desplegado correctamente

---

## ✅ **SOLUCIÓN: Configurar Frontend en Railway**

### **PASO 1: Verificar Servicios en Railway**

1. Ve a Railway → Tu proyecto
2. Verifica cuántos servicios tienes:
   - **Backend:** `apptelink-vision-production` (Python)
   - **Frontend:** `impartial-wisdom-production-3c22` (¿Está configurado?)

---

### **PASO 2: Configurar el Servicio Frontend**

Si el servicio frontend ya existe pero muestra "Not Found":

1. **Ve al servicio Frontend en Railway**
2. **Settings → Build:**
   - **Build Command:** `npm install && npm run build:web`
   - **Start Command:** `npx serve web-build -s -p $PORT`
   - **O:** `npx expo start --web --port $PORT`

3. **Settings → Deploy:**
   - **Root Directory:** (vacío)
   - **Dockerfile Path:** (vacío - usar Nixpacks)

---

### **PASO 3: Si el Frontend NO existe, crearlo**

1. **En Railway → Tu Proyecto:**
   - Haz clic en **"+ New"**
   - Selecciona **"GitHub Repo"**
   - Selecciona el mismo repositorio

2. **Railway detectará automáticamente** que es Node.js/Expo

3. **Configuración:**
   - **Root Directory:** (vacío)
   - **Build Command:** `npm install && npm run build:web`
   - **Start Command:** `npx serve web-build -s -p $PORT`

---

### **PASO 4: Alternativa - Usar Vercel (Más fácil para Expo)**

Vercel es más simple para frontends Expo:

1. **Ve a:** https://vercel.com
2. **Importa tu repositorio** de GitHub
3. **Framework Preset:** **Expo**
4. **Build Command:** `npm run build:web`
5. **Output Directory:** `web-build`
6. **Deploy**

**Ventajas:**
- ✅ Más rápido
- ✅ Mejor para Expo/React
- ✅ CDN global
- ✅ Configuración automática

---

## 📋 **Verificación**

Después de desplegar:

1. **Accede a la URL del frontend**
2. **Debe mostrar la aplicación** (no "Not Found")
3. **Verifica que puede acceder al backend:**
   - Abre la consola del navegador (F12)
   - Debe mostrar: `🌐 [RAILWAY] Usando backend en Railway: https://apptelink-vision-production.up.railway.app`

---

## 🆘 **Si Aún Muestra "Not Found"**

1. **Verifica los logs del frontend en Railway:**
   - ¿El build fue exitoso?
   - ¿Hay errores en los logs?

2. **Verifica que el build generó archivos:**
   - El comando `npm run build:web` debe generar la carpeta `web-build`

3. **Prueba usar Vercel** (más fácil para Expo)

---

**¡Con estos pasos deberías poder desplegar el frontend correctamente!** 🚀
