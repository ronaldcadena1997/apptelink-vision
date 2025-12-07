# 🌐 Instrucciones para Exponer Backend Local a Internet

## 📋 **Problema:**
El backend en Railway no puede acceder a las cámaras porque están en tu red local (192.168.60.x).

## ✅ **Solución: Backend Local + Túnel**

### **Opción A: Usar ngrok (Más Fácil)**

1. **Descarga ngrok:**
   - Ve a: https://ngrok.com/download
   - Descarga para Windows
   - Extrae `ngrok.exe` en una carpeta (ej: `C:\ngrok\`)

2. **Crea cuenta gratuita:**
   - Ve a: https://dashboard.ngrok.com/signup
   - Copia tu **authtoken**

3. **Configura ngrok:**
   ```bash
   ngrok config add-authtoken TU_TOKEN_AQUI
   ```

4. **Inicia el túnel:**
   ```bash
   ngrok http 5000
   ```

5. **Copia la URL que te da:**
   ```
   https://abc123.ngrok-free.app
   ```

6. **Actualiza `src/config/api.js` con esa URL**

---

### **Opción B: Usar Cloudflare Tunnel (Gratis y Sin Límites)**

1. **Instala cloudflared:**
   - Descarga: https://github.com/cloudflare/cloudflared/releases
   - Extrae `cloudflared.exe`

2. **Inicia túnel:**
   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```

3. **Copia la URL que te da**

---

### **Opción C: Mantener Todo Local (Más Simple)**

Si solo necesitas acceso desde tu red local:

1. **Backend local:** `http://192.168.60.15:5000`
2. **Frontend local:** `http://localhost:8081`
3. **iOS/Android:** Misma red WiFi

**Actualiza `api.js` a:**
```javascript
export const API_BASE_URL = 'http://192.168.60.15:5000';
```

---

## 🎯 **Recomendación:**

**Para desarrollo/testing:** Opción C (todo local)  
**Para acceso remoto:** Opción A (ngrok) - 5 minutos de setup

---

## 📝 **Después de configurar el túnel:**

1. Actualiza `src/config/api.js` con la URL del túnel
2. Sube los cambios a GitHub
3. Railway redesplegará automáticamente
4. ¡Funciona desde cualquier lugar! 🎉

