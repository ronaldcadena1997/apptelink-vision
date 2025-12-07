# 🔗 Guía: Conectar IP Tailscale del NUC al API en Railway

## 📋 **Objetivo:**
Conectar el backend en Railway con el NUC usando la IP estática de Tailscale.

---

## ✅ **PASO 1: Obtener IP de Tailscale del NUC**

### **1.1. En el NUC (Windows):**

**Abre PowerShell o CMD y ejecuta:**

```powershell
tailscale ip -4
```

**Ejemplo de salida:**
```
100.64.0.15
```

**📝 Anota esta IP** - Esta es la IP estática de Tailscale que usarás.

---

### **1.2. Verificar que Tailscale está conectado:**

```powershell
tailscale status
```

**Debe mostrar:**
```
100.64.0.15  nuc-sede1    online    direct
```

Si muestra `offline`, ejecuta:
```powershell
tailscale up
```

---

### **1.3. Verificar que el backend está corriendo en el NUC:**

**⚠️ IMPORTANTE: El backend DEBE estar corriendo en el NUC**

**¿Por qué?** El backend en Railway actúa como **proxy/gateway**. No puede acceder directamente a las cámaras porque están en tu red local. Necesita conectarse al backend en el NUC, que SÍ tiene acceso a las cámaras.

**Inicia el backend en el NUC:**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
python server.py
```

**Verifica que esté funcionando:**
```powershell
# Opción 1: PowerShell
Invoke-WebRequest -Uri http://localhost:5000/api/status | Select-Object -ExpandProperty Content

# Opción 2: curl
curl http://localhost:5000/api/status
```

**Debe responder:**
```json
{
  "status": "online",
  "timestamp": "2025-01-XX...",
  "version": "1.0.0"
}
```

**💡 Para más detalles sobre por qué el backend debe correr en el NUC, ver:** `EXPLICACION_ARQUITECTURA.md`

---

## ✅ **PASO 2: Configurar Variables en Railway**

### **2.1. Acceder a Railway:**

1. Ve a: https://railway.app
2. Inicia sesión
3. Selecciona tu proyecto
4. Click en el servicio **Backend** (o crea uno si no existe)

---

### **2.2. Agregar Variable de Entorno:**

1. **Click en "Variables"** (en el menú lateral del servicio Backend)

2. **Click en "New Variable"**

3. **Para un solo NUC:**
   - **Nombre:** `NUC_URL`
   - **Valor:** `http://100.64.0.15:5000`
   - **Reemplaza `100.64.0.15` con la IP real de tu NUC**

4. **Para múltiples NUCs (Recomendado):**
   - **Nombre:** `NUC_URLS`
   - **Valor:** `nuc_sede1:http://100.64.0.15:5000,nuc_sede2:http://100.64.0.16:5000,nuc_sede3:http://100.64.0.17:5000`
   - **Reemplaza las IPs con las IPs reales de tus NUCs**

5. **Click en "Add"**

---

### **2.3. Formato de Variables:**

#### **Variable `NUC_URL` (un solo NUC):**
```
NUC_URL=http://100.64.0.15:5000
```

#### **Variable `NUC_URLS` (múltiples NUCs):**

**Formato con nombres:**
```
NUC_URLS=nuc_sede1:http://100.64.0.15:5000,nuc_sede2:http://100.64.0.16:5000
```

**Formato sin nombres (nombres automáticos):**
```
NUC_URLS=http://100.64.0.15:5000,http://100.64.0.16:5000,http://100.64.0.17:5000
```

**📝 Nota:** 
- Usa **`http://`** (no `https://`) porque es conexión interna de Tailscale
- El puerto es **`:5000`** (puerto donde corre el backend en el NUC)
- Las IPs son las de **Tailscale** (ej: `100.64.0.X`), NO las IPs locales (ej: `192.168.X.X`)

---

## ✅ **PASO 3: Verificar Conexión desde Railway**

### **3.1. Desplegar/Redesplegar Backend:**

Después de agregar las variables:

1. **Railway detectará los cambios automáticamente** y redesplegará
2. **O manualmente:** Click en "Deploy" → "Redeploy"

**⏱️ Espera 2-3 minutos** mientras Railway redespliega

---

### **3.2. Verificar que el Backend en Railway Funciona:**

**Obtén la URL del backend en Railway:**
- Railway → Backend Service → Settings → Domains
- Copia la URL (ej: `https://tu-backend-production.up.railway.app`)

**Prueba el endpoint de status:**

```powershell
# En PowerShell
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/status | Select-Object -ExpandProperty Content

# O usando curl
curl https://tu-backend-production.up.railway.app/api/status
```

**Debe responder:**
```json
{
  "status": "online",
  "timestamp": "2025-01-XX...",
  "version": "1.0.0"
}
```

---

### **3.3. Probar Conexión al NUC desde Railway:**

**Prueba el endpoint que hace proxy al NUC:**

```powershell
# Detectar cámaras (hace proxy al NUC)
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/camaras/detectar | Select-Object -ExpandProperty Content

# O usando curl
curl https://tu-backend-production.up.railway.app/api/camaras/detectar
```

**Si funciona:** El backend en Railway está conectado correctamente al NUC a través de Tailscale.

**Si no funciona:** Revisa el [Troubleshooting](#-troubleshooting) más abajo.

---

## 🔄 **Flujo Completo de Conexión**

```
┌─────────────────────────────────────────────────────────┐
│  1. Frontend (Usuario)                                   │
│     https://tu-frontend.railway.app                      │
└──────────────────┬────────────────────────────────────────┘
                   │ HTTPS Request
                   │ GET /api/camaras/detectar
                   ▼
┌─────────────────────────────────────────────────────────┐
│  2. Backend en Railway                                   │
│     https://tu-backend.railway.app                      │
│                                                          │
│     Lee variable: NUC_URLS                               │
│     = http://100.64.0.15:5000                           │
└──────────────────┬────────────────────────────────────────┘
                   │ HTTP Request (a través de Tailscale)
                   │ GET http://100.64.0.15:5000/api/camaras/detectar
                   ▼
┌─────────────────────────────────────────────────────────┐
│  3. Tailscale VPN                                        │
│     Enruta a través de la red mesh                       │
│     IP: 100.64.0.15 (IP estática de Tailscale)          │
└──────────────────┬────────────────────────────────────────┘
                   │ Conexión directa
                   ▼
┌─────────────────────────────────────────────────────────┐
│  4. NUC Local (Windows)                                  │
│     IP Tailscale: 100.64.0.15                           │
│     Backend corriendo en: localhost:5000                 │
│                                                          │
│     Procesa request y devuelve respuesta                 │
└──────────────────┬────────────────────────────────────────┘
                   │ Respuesta JSON
                   │ (camaras detectadas)
                   ▼
┌─────────────────────────────────────────────────────────┐
│  5. Backend en Railway                                   │
│     Recibe respuesta del NUC                            │
│     Retorna al Frontend                                 │
└──────────────────┬────────────────────────────────────────┘
                   │ Respuesta JSON
                   ▼
┌─────────────────────────────────────────────────────────┐
│  6. Frontend (Usuario)                                   │
│     Muestra cámaras detectadas                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 **Troubleshooting**

### **❌ Error: "No se pudo conectar al NUC"**

**Causa:** El backend en Railway no puede alcanzar el NUC a través de Tailscale.

**Soluciones:**

1. **✅ Verifica que Tailscale esté corriendo en el NUC:**
   ```powershell
   # En el NUC (PowerShell)
   tailscale status
   ```
   - Debe mostrar `online` y `direct`
   - Si muestra `offline`, ejecuta: `tailscale up`

2. **✅ Verifica la IP de Tailscale del NUC:**
   ```powershell
   # En el NUC (PowerShell)
   tailscale ip -4
   ```
   - Anota la IP que muestra
   - Verifica que esta IP sea la misma que configuraste en Railway

3. **✅ Verifica que el backend esté corriendo en el NUC:**
   ```powershell
   # En el NUC (PowerShell)
   Invoke-WebRequest -Uri http://localhost:5000/api/status | Select-Object -ExpandProperty Content
   ```
   - Debe responder con `{"status": "online", ...}`

4. **✅ Verifica la variable en Railway:**
   - Ve a Railway → Backend Service → Variables
   - Verifica que `NUC_URL` o `NUC_URLS` esté configurada
   - Verifica que use `http://` (no `https://`)
   - Verifica que use la IP de Tailscale (ej: `100.64.0.15`), NO la IP local (ej: `192.168.60.15`)
   - Verifica que el puerto sea `:5000`

5. **✅ Prueba desde tu PC (con Tailscale instalado):**
   ```powershell
   # En tu PC (PowerShell)
   # Primero instala Tailscale: https://tailscale.com/download/windows
   # Luego inicia sesión con la misma cuenta
   
   # Prueba la conexión
   Invoke-WebRequest -Uri http://100.64.0.15:5000/api/status | Select-Object -ExpandProperty Content
   ```
   - Si funciona desde tu PC, debería funcionar desde Railway
   - Si no funciona desde tu PC, el problema está en el NUC o Tailscale

6. **✅ Verifica los logs de Railway:**
   - Railway → Backend Service → Deployments → Click en el último deployment
   - Revisa los logs para ver el error específico
   - Busca mensajes como "Connection refused", "Timeout", etc.

---

### **❌ Error: "Connection refused"**

**Causa:** El backend no está corriendo en el NUC o el puerto está bloqueado.

**Soluciones:**
1. ✅ Verifica que el backend esté corriendo: `python server.py`
2. ✅ Verifica que el puerto 5000 no esté bloqueado por firewall
3. ✅ Verifica que el backend esté escuchando en `0.0.0.0` o `localhost`

---

### **❌ Error: "Timeout"**

**Causa:** Railway no puede alcanzar el NUC a través de Tailscale.

**Soluciones:**
1. ✅ Verifica que Tailscale esté `online` y `direct`
2. ✅ Verifica que la IP de Tailscale sea correcta
3. ✅ Verifica que el NUC tenga conexión a internet (necesario para Tailscale)
4. ✅ Prueba desde tu PC con Tailscale instalado

---

### **❌ Error: "No hay NUCs disponibles"**

**Causa:** La variable `NUC_URLS` no está configurada o está vacía.

**Solución:**
1. ✅ Ve a Railway → Variables
2. ✅ Verifica que `NUC_URLS` esté configurada
3. ✅ Formato correcto: `url1,url2,url3` o `nombre1:url1,nombre2:url2`

---

## 📝 **Checklist de Verificación**

Antes de considerar que está conectado:

- [ ] Tailscale instalado en el NUC
- [ ] Tailscale conectado (`tailscale status` muestra `online`)
- [ ] IP de Tailscale obtenida (`tailscale ip -4`)
- [ ] Backend corriendo en el NUC (`python server.py`)
- [ ] Backend responde localmente (`curl http://localhost:5000/api/status`)
- [ ] Variable `NUC_URL` o `NUC_URLS` configurada en Railway
- [ ] Variable usa IP de Tailscale (ej: `100.64.0.15`)
- [ ] Variable usa `http://` (no `https://`)
- [ ] Variable incluye puerto `:5000`
- [ ] Backend en Railway redesplegado después de agregar variable
- [ ] Endpoint `/api/status` funciona desde Railway
- [ ] Endpoint `/api/camaras/detectar` funciona desde Railway
- [ ] Prueba desde PC con Tailscale funciona

---

## 🎯 **Resumen Rápido**

1. **En el NUC:** Obtén IP de Tailscale: `tailscale ip -4` → Ejemplo: `100.64.0.15`
2. **En Railway:** Agrega variable: `NUC_URL=http://100.64.0.15:5000`
3. **Verifica:** Prueba `https://tu-backend.railway.app/api/camaras/detectar`

**¡Listo!** El backend en Railway ahora puede conectarse al NUC a través de Tailscale.

---

## 📞 **Soporte Adicional**

- 📄 **Múltiples NUCs:** Ver `CONFIGURACION_MULTIPLES_NUCS.md`
- 📄 **Arquitectura:** Ver `ARQUITECTURA_SERVIDOR.md`
- 📄 **SIM7600:** Ver `GUIA_SIM7600.md`
- 🏗️ **¿Por qué el backend debe correr en el NUC?** Ver `EXPLICACION_ARQUITECTURA.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
