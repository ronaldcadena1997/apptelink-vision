# 🔧 Solución: Error 502 en Frontend

## 🚨 Problema

El frontend muestra un error **502 (Bad Gateway)** cuando intenta obtener snapshots de las cámaras.

**Causa:** Railway no puede conectarse al NUC a través de Tailscale para obtener las imágenes.

---

## 🔍 Diagnóstico

### Paso 1: Verificar que Railway puede conectarse al NUC

**Desde el NUC, prueba si puedes conectarte desde fuera:**

```powershell
# Verificar que el puente está escuchando en todas las interfaces
netstat -ano | findstr :5000

# Debe mostrar algo como:
# TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING
```

**Si solo muestra `127.0.0.1:5000`:** El puente solo está escuchando en localhost. Necesitas verificar que esté configurado para escuchar en `0.0.0.0`.

---

### Paso 2: Verificar Firewall de Windows

El firewall de Windows puede estar bloqueando conexiones entrantes en el puerto 5000.

**Abrir el puerto 5000 en el firewall:**

```powershell
# Ejecuta como Administrador
New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

**Verificar que la regla existe:**

```powershell
Get-NetFirewallRule -DisplayName "Puente Genérico NUC"
```

---

### Paso 3: Verificar Tailscale

**Verificar que Tailscale está corriendo y tiene IP:**

```powershell
# Verificar proceso
tasklist /FI "IMAGENAME eq tailscaled.exe"

# Verificar IP
tailscale ip -4

# Debe mostrar: 100.92.50.72
```

**Verificar conectividad desde Tailscale:**

```powershell
# Desde el NUC, prueba conectarte a ti mismo usando la IP de Tailscale
curl http://100.92.50.72:5000/api/status

# Debe responder igual que localhost:5000/api/status
```

**Si esto falla:** Tailscale no está configurado correctamente para permitir conexiones entrantes.

---

### Paso 4: Verificar Configuración en Railway

**En Railway Dashboard:**

1. Ve a tu proyecto de **backend**
2. Abre la pestaña **"Variables"**
3. Verifica que tienes:

```
NUC_URLS=nuc_sede1:http://100.92.50.72:5000
CAMARAS_IPS=192.168.60.65
```

**⚠️ IMPORTANTE:** Railway **NO puede usar Tailscale directamente** porque Railway es un servicio en la nube.

**Solución:** Necesitas que Railway pueda conectarse al NUC. Hay dos opciones:

#### Opción A: Tailscale en Railway (Recomendado)

Railway puede usar Tailscale si instalas Tailscale en el contenedor de Railway. Sin embargo, esto requiere configuración adicional.

#### Opción B: Túnel/Relay (Alternativa)

Usar un servicio de túnel (como ngrok, Cloudflare Tunnel, o similar) para exponer el NUC a Railway.

---

## ✅ Solución Recomendada: Verificar Conectividad

### 1. Verificar que el NUC es accesible desde Railway

**Problema común:** Railway no puede conectarse porque:
- El firewall bloquea conexiones
- Tailscale no permite conexiones desde Railway
- El puente no está escuchando en la interfaz correcta

### 2. Probar conectividad manualmente

**Desde el NUC, prueba:**

```powershell
# 1. Verificar que el puente escucha en todas las interfaces
netstat -ano | findstr :5000

# 2. Probar desde la IP de Tailscale
curl http://100.92.50.72:5000/api/status

# 3. Verificar firewall
Get-NetFirewallRule -DisplayName "*5000*" | Select-Object DisplayName, Enabled, Direction
```

---

## 🔧 Soluciones Paso a Paso

### Solución 1: Abrir Firewall (Más Común)

```powershell
# Ejecuta como Administrador en PowerShell
New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

**Verificar:**

```powershell
# Probar desde otra máquina en la misma red Tailscale
# (o desde Railway si tiene acceso a Tailscale)
curl http://100.92.50.72:5000/api/status
```

---

### Solución 2: Verificar que el Puente Escucha Correctamente

**Verifica en `puente_generico_nuc.py`:**

```python
# Debe ser:
app.run(host='0.0.0.0', port=5000, debug=False)

# NO debe ser:
app.run(host='127.0.0.1', port=5000, debug=False)  # ❌ Solo localhost
```

---

### Solución 3: Configurar Tailscale para Permitir Conexiones

**En Tailscale Admin Console:**

1. Ve a https://login.tailscale.com/admin/machines
2. Encuentra tu NUC (IP: 100.92.50.72)
3. Verifica que está marcado como "Online"
4. Verifica que tiene permisos para recibir conexiones

**O desde el NUC:**

```powershell
# Verificar estado de Tailscale
tailscale status

# Debe mostrar tu máquina como "online"
```

---

### Solución 4: Probar Endpoint de Snapshot Directamente

**Desde el NUC:**

```powershell
# Probar el endpoint de snapshot directamente
curl http://localhost:5000/api/camaras/192.168.60.65/snapshot

# Debe responder con un JSON que contiene "image" en base64
```

**Si esto funciona localmente pero falla desde Railway:**

El problema es de conectividad entre Railway y el NUC.

---

## 🧪 Pruebas de Diagnóstico

### Test 1: Verificar NUC Local

```powershell
curl http://localhost:5000/api/status
# ✅ Debe funcionar
```

### Test 2: Verificar NUC desde Tailscale IP

```powershell
curl http://100.92.50.72:5000/api/status
# ✅ Debe funcionar si Tailscale y firewall están bien
```

### Test 3: Verificar Snapshot Local

```powershell
curl http://localhost:5000/api/camaras/192.168.60.65/snapshot
# ✅ Debe devolver JSON con imagen base64
```

### Test 4: Verificar Railway Backend

```powershell
curl https://apptelink-vision-production.up.railway.app/api/status
# ✅ Debe funcionar
```

### Test 5: Verificar Railway → NUC (Este es el que falla)

```powershell
# Desde Railway logs, busca errores de conexión
# O prueba desde el navegador:
# https://apptelink-vision-production.up.railway.app/api/camaras/192.168.60.65/snapshot
```

---

## 🚨 Problema Específico: Railway no puede usar Tailscale

**Railway es un servicio en la nube** y no tiene Tailscale instalado por defecto. Para que Railway pueda conectarse al NUC:

### Opción 1: Instalar Tailscale en Railway (Complejo)

Requiere modificar el Dockerfile para instalar Tailscale en el contenedor de Railway.

### Opción 2: Usar Túnel Público (Más Simple)

Exponer el NUC usando un túnel público (ngrok, Cloudflare Tunnel, etc.) y configurar Railway para usar esa URL pública.

### Opción 3: Verificar que Railway tiene Acceso a Tailscale

Si Railway está en la misma red Tailscale (poco probable), debería funcionar. Verifica en Railway logs si hay errores de conexión.

---

## 📋 Checklist de Verificación

- [ ] ✅ NUC local funciona: `curl http://localhost:5000/api/status`
- [ ] ✅ Puente escucha en `0.0.0.0:5000` (no solo `127.0.0.1`)
- [ ] ✅ Firewall permite conexiones en puerto 5000
- [ ] ✅ Tailscale está corriendo y tiene IP: `100.92.50.72`
- [ ] ✅ NUC responde desde IP de Tailscale: `curl http://100.92.50.72:5000/api/status`
- [ ] ✅ Railway tiene `NUC_URLS` configurado: `nuc_sede1:http://100.92.50.72:5000`
- [ ] ✅ Railway puede conectarse al NUC (verificar en logs)

---

## 🔍 Revisar Logs de Railway

**En Railway Dashboard:**

1. Ve a tu proyecto de backend
2. Abre la pestaña **"Logs"**
3. Busca mensajes como:
   - `📸 Obteniendo snapshot desde NUC: http://100.92.50.72:5000/api/camaras/...`
   - `❌ Error de conexión con NUC: ...`
   - `⏱️ Timeout al conectar con NUC: ...`

**Estos logs te dirán exactamente qué está fallando.**

---

## 💡 Solución Rápida

**Ejecuta estos comandos en el NUC (como Administrador):**

```powershell
# 1. Abrir firewall
New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# 2. Verificar que funciona
curl http://100.92.50.72:5000/api/status

# 3. Reiniciar el puente genérico
# (Detén el proceso actual y vuelve a ejecutar ejecutar_puente_silencioso.bat)
```

**Luego verifica en Railway logs si la conexión funciona.**

---

## 📞 Si el Problema Persiste

1. **Revisa los logs de Railway** para ver el error exacto
2. **Verifica que Railway tiene acceso a Tailscale** (puede que necesites configurar Tailscale en Railway)
3. **Considera usar un túnel público** como alternativa a Tailscale para Railway
