# 🌐 Cloudflare Tunnel - Solución Profesional para Producción

## ✅ **Ventajas sobre ngrok:**
- ✅ **100% Gratis** - Sin límites de tiempo
- ✅ **Sin límites** - Tráfico ilimitado
- ✅ **Estable** - Para producción real
- ✅ **HTTPS automático** - Certificados SSL incluidos
- ✅ **Dominio personalizado** - Puedes usar tu propio dominio
- ✅ **Sin reinicios** - Túnel permanente

---

## 📋 **Instalación en el NUC (Linux)**

### **Paso 1: Instalar cloudflared**

```bash
# Descargar cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64

# Dar permisos
chmod +x cloudflared-linux-amd64

# Mover a /usr/local/bin
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

### **Paso 2: Autenticarse con Cloudflare**

```bash
cloudflared tunnel login
```

Esto abrirá el navegador para autorizar.

### **Paso 3: Crear túnel**

```bash
cloudflared tunnel create apptelink-backend
```

Esto crea un túnel llamado `apptelink-backend` y te da un UUID.

### **Paso 4: Configurar túnel**

Crea archivo: `/home/usuario/.cloudflared/config.yml`

```yaml
tunnel: TU_UUID_AQUI
credentials-file: /home/usuario/.cloudflared/TU_UUID_AQUI.json

ingress:
  - hostname: apptelink-backend.tu-dominio.com  # Opcional: dominio personalizado
    service: http://localhost:5000
  - service: http_status:404
```

### **Paso 5: Configurar como servicio systemd**

Crea: `/etc/systemd/system/cloudflared.service`

```ini
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=tu_usuario
ExecStart=/usr/local/bin/cloudflared tunnel --config /home/usuario/.cloudflared/config.yml run
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### **Paso 6: Activar servicio**

```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

---

## 🎯 **URL del Túnel**

Después de configurar, obtendrás una URL como:
```
https://apptelink-backend.tu-dominio.com
```

O si no usas dominio personalizado:
```
https://TU_UUID.cfargotunnel.com
```

---

## 📝 **Actualizar Frontend**

En `src/config/api.js`, actualiza:
```javascript
const BACKEND_TUNEL = 'https://TU-URL-DE-CLOUDFLARE';
```

---

## ✅ **Ventajas para Producción:**

1. **Siempre activo** - Se reinicia automáticamente
2. **Sin límites** - Tráfico ilimitado
3. **Estable** - Usado por empresas grandes
4. **Gratis** - Sin costos ocultos
5. **Dominio propio** - Puedes usar tu dominio

---

## 🔧 **Mantenimiento:**

Ver logs:
```bash
sudo journalctl -u cloudflared -f
```

Reiniciar:
```bash
sudo systemctl restart cloudflared
```

---

## 📞 **Soporte:**

Documentación oficial: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

