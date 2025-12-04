# 🚀 Guía de Deployment - AppTelink Vision

Esta guía te ayudará a desplegar tu aplicación en servidores para acceso desde internet.

---

## 📋 Tabla de Contenidos

- [Opción 1: Railway (Recomendada)](#opción-1-railway-recomendada)
- [Opción 2: Render](#opción-2-render)
- [Opción 3: Vercel + Railway](#opción-3-vercel--railway)
- [Configuración de Variables](#configuración-de-variables)

---

## 🚂 Opción 1: Railway (Recomendada)

Railway es gratuito y permite hostear backend y frontend en un solo lugar.

### **Paso 1: Preparar el Backend**

✅ Ya están creados:
- `backend/Procfile`
- `backend/requirements.txt`
- `server.py` actualizado con PORT dinámico

### **Paso 2: Crear cuenta en Railway**

1. Ve a [railway.app](https://railway.app)
2. Registrate con GitHub
3. Crea un nuevo proyecto

### **Paso 3: Desplegar el Backend**

1. En Railway, click en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Conecta tu repositorio (o sube los archivos)
4. Railway detectará automáticamente que es Python
5. Configura la carpeta raíz como `backend`
6. Click en **"Deploy"**

**Variables de entorno necesarias:**
```
PORT=5000
```

Railway te dará una URL pública como:
```
https://apptelink-vision-production.up.railway.app
```

### **Paso 4: Configurar el Frontend**

Actualiza `src/config/api.js`:

```javascript
export const API_BASE_URL = 'https://tu-app-backend.up.railway.app';
```

### **Paso 5: Desplegar el Frontend**

**Opción A - En Railway:**
1. Crea otro servicio en Railway
2. Sube el proyecto completo
3. Railway detectará Expo/React
4. Configura el build command: `npm run web`

**Opción B - En Vercel (más rápido para web):**
1. Ve a [vercel.com](https://vercel.com)
2. Importa tu repositorio
3. Framework: **Expo**
4. Build command: `npm run build`
5. Output: `.next` o `web-build`

---

## 🎨 Opción 2: Render

Render es otra alternativa gratuita y confiable.

### **Backend en Render:**

1. Ve a [render.com](https://render.com)
2. Click en **"New Web Service"**
3. Conecta tu repositorio
4. Configuración:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
   - **Root Directory:** `backend`
5. **Variables de entorno:**
   ```
   PORT=10000
   ```

Render te dará una URL como:
```
https://apptelink-vision.onrender.com
```

### **Frontend en Render:**

1. Nuevo servicio "Static Site"
2. Build command: `npm run build`
3. Publish directory: `web-build`

---

## ⚡ Opción 3: Vercel + Railway

Combinación óptima para mejor rendimiento.

### **Backend:** Railway (como arriba)
### **Frontend:** Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Importa tu repositorio
4. Framework preset: **Expo**
5. Build command: `npx expo export:web`
6. Output directory: `web-build`
7. Variables de entorno:
   ```
   EXPO_PUBLIC_API_URL=https://tu-backend.railway.app
   ```

---

## 🔧 Configuración de Variables

### **Backend (server.py):**

El backend ya está configurado para leer el PORT del entorno:
```python
port = int(os.environ.get('PORT', 5000))
```

### **Frontend (api.js):**

Actualiza para usar variable de entorno:

```javascript
// src/config/api.js
export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.60.15:5000';
```

---

## 📱 Para iOS/Android (Expo Go)

Una vez desplegado el backend:

1. Actualiza `src/config/api.js` con la URL pública
2. Sube los cambios a GitHub
3. En Expo, ejecuta:
   ```bash
   npx expo publish
   ```
4. Escanea el QR desde cualquier lugar

---

## 🔐 Consideraciones de Seguridad

### **1. Variables de Entorno**
No subas credenciales al repositorio. Usa variables de entorno:

```python
# En server.py
USUARIO = os.environ.get('CAMERA_USER', 'admin')
CONTRASENA = os.environ.get('CAMERA_PASS', 'password')
```

### **2. CORS**
El backend ya tiene CORS habilitado. Si necesitas restringirlo:

```python
from flask_cors import CORS

# Permitir solo tu dominio
CORS(app, origins=['https://tu-dominio.vercel.app'])
```

### **3. HTTPS**
Todos estos servicios proveen HTTPS automáticamente.

---

## 💰 Costos

| Servicio | Backend | Frontend | Límites Gratis |
|----------|---------|----------|----------------|
| **Railway** | ✅ Gratis | ✅ Gratis | 500 horas/mes, $5 crédito |
| **Render** | ✅ Gratis | ✅ Gratis | Suspende después de inactividad |
| **Vercel** | ❌ | ✅ Gratis | 100GB bandwidth |
| **Netlify** | ❌ | ✅ Gratis | 100GB bandwidth |

---

## 🎯 Recomendación Final

**Para empezar rápido:**
1. **Backend:** Railway (5 minutos)
2. **Frontend:** Vercel (3 minutos)

**Total: 8 minutos para estar online** 🚀

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway/Render
2. Verifica las variables de entorno
3. Asegúrate de que las URLs estén actualizadas en `api.js`

---

**© 2025 Apptelink Vision**

