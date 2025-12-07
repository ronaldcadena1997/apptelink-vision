# 🌐 Configurar Túnel en el NUC para Backend Local

## 📋 **Problema:**
El backend en Railway no puede acceder a las cámaras porque están en la red local del NUC (192.168.60.x).

## ✅ **Solución: Backend Local en NUC + Túnel ngrok**

### **Paso 1: En el NUC (donde están las cámaras)**

1. **Descarga ngrok para Linux:**
   ```bash
   wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
   tar xvzf ngrok-v3-stable-linux-amd64.tgz
   sudo mv ngrok /usr/local/bin/
   ```

2. **Crea cuenta en ngrok:**
   - Ve a: https://dashboard.ngrok.com/signup
   - Copia tu **authtoken**

3. **Configura ngrok:**
   ```bash
   ngrok config add-authtoken TU_TOKEN_AQUI
   ```

4. **Inicia el backend Python en el NUC:**
   ```bash
   cd /ruta/al/backend
   python server.py
   ```

5. **En otra terminal, inicia el túnel:**
   ```bash
   ngrok http 5000
   ```

6. **Copia la URL que te da:**
   ```
   https://abc123.ngrok-free.app
   ```

---

### **Paso 2: Actualizar Frontend en Railway**

Actualiza `src/config/api.js` con la URL del túnel del NUC.

---

### **Paso 3: Configuración Permanente (Opcional)**

Para que el túnel se inicie automáticamente en el NUC:

**Crea archivo: `/etc/systemd/system/ngrok-tunnel.service`**
```ini
[Unit]
Description=Ngrok Tunnel for AppTelink Backend
After=network.target

[Service]
Type=simple
User=tu_usuario
ExecStart=/usr/local/bin/ngrok http 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Activar:**
```bash
sudo systemctl enable ngrok-tunnel.service
sudo systemctl start ngrok-tunnel.service
```

---

## 🎯 **Resultado:**

- ✅ Backend corre en el NUC (acceso a cámaras)
- ✅ Túnel expone el backend a internet
- ✅ Frontend en Railway se conecta al túnel
- ✅ Funciona desde cualquier lugar

---

## 📝 **Alternativa: Cloudflare Tunnel (Gratis, Sin Límites)**

Si prefieres algo más estable que ngrok:

```bash
# Instalar cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

# Iniciar túnel
cloudflared tunnel --url http://localhost:5000
```

---

## ⚠️ **IMPORTANTE:**

1. El backend DEBE correr en el NUC (no en Railway)
2. El túnel DEBE estar activo siempre
3. Si el NUC se reinicia, reinicia el túnel también

