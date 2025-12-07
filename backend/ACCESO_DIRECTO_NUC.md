# 🌐 Acceso Directo al NUC por IP

## 🎯 **Objetivo:**
Conectarte directamente al backend en el NUC usando su IP, sin túneles.

---

## ✅ **OPCIÓN 1: IP Pública Estática (MEJOR)** ⭐

### **Requisitos:**
- Router con IP pública estática
- Port forwarding configurado
- Firewall configurado

### **Setup:**

**1. Configurar Port Forwarding en el Router:**
```
Puerto Externo: 5000 (o el que prefieras)
Puerto Interno: 5000
IP Interna: 192.168.60.15 (IP del NUC)
Protocolo: TCP
```

**2. Obtener IP Pública del Router:**
```bash
# En el NUC o cualquier PC de la red
curl ifconfig.me
# O visita: https://whatismyipaddress.com
```

**3. Configurar Firewall en el NUC:**
```bash
# Ubuntu/Debian
sudo ufw allow 5000/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

**4. Actualizar Frontend:**
```javascript
// En src/config/api.js
export const API_BASE_URL = 'http://TU_IP_PUBLICA:5000';
// O con HTTPS si tienes certificado:
// export const API_BASE_URL = 'https://TU_IP_PUBLICA:5000';
```

**Ventajas:**
- ✅ Acceso directo
- ✅ Sin servicios externos
- ✅ Control total
- ✅ Sin límites

**Desventajas:**
- ⚠️ Necesitas IP pública estática (puede costar $)
- ⚠️ Expones el puerto directamente

---

## ✅ **OPCIÓN 2: IP Pública Dinámica + DDNS (GRATIS)** ⭐⭐

### **Requisitos:**
- Router con IP pública (aunque sea dinámica)
- Servicio DDNS (gratis)
- Port forwarding

### **Servicios DDNS Gratis:**
- **No-IP** - https://www.noip.com (gratis)
- **DuckDNS** - https://www.duckdns.org (gratis)
- **FreeDNS** - https://freedns.afraid.org (gratis)

### **Setup con No-IP (Ejemplo):**

**1. Crear cuenta en No-IP:**
- Ve a: https://www.noip.com/sign-up
- Crea un hostname: `apptelink-backend.ddns.net`

**2. Instalar cliente DDNS en el NUC:**
```bash
# Descargar
wget https://www.noip.com/client/linux/noip-duc-linux.tar.gz
tar xzf noip-duc-linux.tar.gz
cd noip-2.1.9-1/

# Compilar
make
sudo make install

# Configurar
sudo /usr/local/bin/noip2 -C
# Ingresa tu usuario, contraseña y hostname
```

**3. Configurar como servicio:**
```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/noip.service
```

```ini
[Unit]
Description=No-IP Dynamic DNS Update Client
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/bin/noip2
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable noip
sudo systemctl start noip
```

**4. Configurar Port Forwarding:**
```
Puerto: 5000
IP: 192.168.60.15 (NUC)
```

**5. Actualizar Frontend:**
```javascript
export const API_BASE_URL = 'http://apptelink-backend.ddns.net:5000';
```

**Ventajas:**
- ✅ Gratis
- ✅ Funciona con IP dinámica
- ✅ Dominio fácil de recordar
- ✅ Sin límites

**Desventajas:**
- ⚠️ Requiere actualización periódica (automática)

---

## ✅ **OPCIÓN 3: Tailscale VPN (MUY FÁCIL)** ⭐⭐⭐

### **Ventajas:**
- ✅ Setup en 5 minutos
- ✅ 100% Gratis (hasta 100 dispositivos)
- ✅ IP privada accesible desde cualquier lugar
- ✅ Seguro (encriptado)
- ✅ Sin port forwarding

### **Setup:**

**1. Instalar Tailscale en el NUC:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**2. Instalar Tailscale en tu PC (opcional):**
- Descarga: https://tailscale.com/download
- Inicia sesión con la misma cuenta

**3. Obtener IP de Tailscale del NUC:**
```bash
# En el NUC
tailscale ip -4
# Te dará algo como: 100.x.x.x
```

**4. Actualizar Frontend:**
```javascript
export const API_BASE_URL = 'http://100.x.x.x:5000';
// O mejor, usa el hostname de Tailscale:
export const API_BASE_URL = 'http://nuc-hostname.tailnet.ts.net:5000';
```

**Ventajas:**
- ✅ Muy fácil de configurar
- ✅ Gratis
- ✅ Seguro
- ✅ Sin port forwarding
- ✅ Funciona desde cualquier lugar

**Desventajas:**
- ⚠️ Requiere instalar Tailscale en todos los dispositivos que accedan

---

## ✅ **OPCIÓN 4: WireGuard VPN (PROFESIONAL)**

### **Setup:**

**1. Instalar WireGuard en el NUC:**
```bash
sudo apt update
sudo apt install wireguard

# Generar claves
wg genkey | sudo tee /etc/wireguard/private.key
sudo chmod 600 /etc/wireguard/private.key
sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key
```

**2. Configurar servidor VPN:**
```bash
sudo nano /etc/wireguard/wg0.conf
```

```ini
[Interface]
PrivateKey = TU_PRIVATE_KEY
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = CLIENT_PUBLIC_KEY
AllowedIPs = 10.0.0.2/32
```

**3. Iniciar VPN:**
```bash
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

**4. Conectarte desde Railway/Internet:**
- Configura cliente WireGuard
- Conéctate a la VPN
- Accede a `192.168.60.15:5000` como si estuvieras en la red local

**Ventajas:**
- ✅ Muy seguro
- ✅ Gratis
- ✅ Control total
- ✅ Acceso como red local

**Desventajas:**
- ⚠️ Setup más complejo
- ⚠️ Requiere cliente VPN

---

## ✅ **OPCIÓN 5: ZeroTier (FÁCIL Y GRATIS)** ⭐⭐⭐

### **Setup:**

**1. Crear cuenta en ZeroTier:**
- Ve a: https://my.zerotier.com
- Crea una red

**2. Instalar ZeroTier en el NUC:**
```bash
curl -s https://install.zerotier.com | sudo bash
sudo zerotier-cli join TU_NETWORK_ID
```

**3. Autorizar el NUC en el dashboard de ZeroTier**

**4. Obtener IP de ZeroTier:**
```bash
zerotier-cli listnetworks
# Te mostrará la IP asignada (ej: 10.147.20.x)
```

**5. Actualizar Frontend:**
```javascript
export const API_BASE_URL = 'http://10.147.20.x:5000';
```

**Ventajas:**
- ✅ Muy fácil
- ✅ Gratis (hasta 25 dispositivos)
- ✅ Sin port forwarding
- ✅ Funciona desde cualquier lugar

**Desventajas:**
- ⚠️ Requiere cuenta en ZeroTier

---

## 📊 **Comparativa:**

| Solución | Dificultad | Costo | Seguridad | Port Forwarding |
|----------|-----------|-------|-----------|-----------------|
| **IP Pública Estática** | Media | $ | ⭐⭐⭐ | ✅ Requerido |
| **DDNS (No-IP)** | Media | Gratis | ⭐⭐⭐ | ✅ Requerido |
| **Tailscale** | Fácil | Gratis | ⭐⭐⭐⭐⭐ | ❌ No |
| **WireGuard** | Alta | Gratis | ⭐⭐⭐⭐⭐ | ⚠️ Opcional |
| **ZeroTier** | Fácil | Gratis | ⭐⭐⭐⭐ | ❌ No |

---

## 🎯 **Recomendación:**

### **Para empezar rápido:**
**Tailscale** o **ZeroTier** - 5 minutos, gratis, sin port forwarding

### **Para producción:**
**DDNS + Port Forwarding** - Más control, IP directa

---

## 🚀 **Siguiente Paso:**

¿Cuál opción prefieres? Te guío paso a paso con la que elijas.

