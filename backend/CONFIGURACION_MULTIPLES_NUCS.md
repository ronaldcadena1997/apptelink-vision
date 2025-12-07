# 🔗 Configuración para Múltiples NUCs

## 🎯 **Objetivo:**
Configurar el backend en servidor para que se conecte a **múltiples NUCs** y seleccione automáticamente el NUC correcto según la IP de la cámara.

---

## 📐 **Arquitectura:**

```
┌─────────────────────────────────┐
│  Frontend (Railway)             │
└──────────────┬──────────────────┘
               │
    ┌──────────▼──────────┐
    │  Backend (Railway)  │ ← Servidor
    └──────────┬──────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│ NUC 1 │ │ NUC 2 │ │ NUC 3 │ ← Múltiples NUCs
│(VPN)  │ │(VPN)  │ │(VPN)  │
└───────┘ └───────┘ └───────┘
    │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│Cámaras│ │Cámaras│ │Cámaras│
│192.168│ │192.168│ │192.168│
│.60.x  │ │.61.x  │ │.62.x  │
└───────┘ └───────┘ └───────┘
```

---

## ✅ **PASO 1: Exponer Cada NUC**

### **Para cada NUC, instala Tailscale/ZeroTier:**

**NUC 1:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Anota la IP (ej: 100.64.0.1)
```

**NUC 2:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Anota la IP (ej: 100.64.0.2)
```

**NUC 3:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Anota la IP (ej: 100.64.0.3)
```

---

## ✅ **PASO 2: Configurar Backend en Railway**

### **Opción A: Lista Simple (Sin nombres)**

En Railway → Settings → Variables:

```
NUC_URLS=http://100.64.0.1:5000,http://100.64.0.2:5000,http://100.64.0.3:5000
```

El backend asignará nombres automáticos: `nuc_1`, `nuc_2`, `nuc_3`

---

### **Opción B: Con Nombres Personalizados (Recomendado)**

```
NUC_URLS=nuc_sede1:http://100.64.0.1:5000,nuc_sede2:http://100.64.0.2:5000,nuc_sede3:http://100.64.0.3:5000
```

Esto te permite identificar cada NUC por nombre.

---

## ✅ **PASO 3: Selección Automática de NUC**

El backend selecciona automáticamente el NUC correcto basado en:

1. **Parámetro `nuc_id`** (si se especifica)
2. **IP de la cámara** (mapeo por rango de red)
3. **Primer NUC disponible** (por defecto)

### **Ejemplo de uso:**

```javascript
// Detectar cámaras en un NUC específico
fetch('https://tu-api.railway.app/api/camaras/detectar?nuc_id=nuc_sede1')

// Obtener snapshot de una cámara (selección automática por IP)
fetch('https://tu-api.railway.app/api/camaras/192.168.60.10/snapshot')

// Obtener cercas de una cámara (selección automática por IP)
fetch('https://tu-api.railway.app/api/cercas/192.168.60.10')
```

---

## ✅ **PASO 4: Listar NUCs Disponibles**

El backend expone un endpoint para listar todos los NUCs:

```bash
curl https://tu-api.railway.app/api/nucs
```

**Respuesta:**
```json
{
  "success": true,
  "modo": "proxy",
  "nucs": [
    {
      "id": "nuc_sede1",
      "url": "http://100.64.0.1:5000",
      "disponible": true
    },
    {
      "id": "nuc_sede2",
      "url": "http://100.64.0.2:5000",
      "disponible": true
    },
    {
      "id": "nuc_sede3",
      "url": "http://100.64.0.3:5000",
      "disponible": false
    }
  ],
  "total": 3
}
```

---

## 🔧 **Mapeo Automático por IP**

El backend intenta mapear automáticamente las cámaras a NUCs basándose en el rango de IP:

- **Cámaras 192.168.60.x** → NUC con IP que empiece con 192.168.60
- **Cámaras 192.168.61.x** → NUC con IP que empiece con 192.168.61

**Nota:** Si los NUCs están en diferentes redes (vía VPN), el mapeo se hace por los primeros 3 octetos de la IP.

---

## 📝 **Ejemplos de Uso**

### **1. Detectar cámaras en todos los NUCs:**

```javascript
// Obtener lista de NUCs
const nucs = await fetch('https://tu-api.railway.app/api/nucs').then(r => r.json());

// Detectar cámaras en cada NUC
for (const nuc of nucs.nucs) {
  const camaras = await fetch(
    `https://tu-api.railway.app/api/camaras/detectar?nuc_id=${nuc.id}`
  ).then(r => r.json());
  
  console.log(`Cámaras en ${nuc.id}:`, camaras);
}
```

### **2. Obtener snapshot de una cámara específica:**

```javascript
// El backend selecciona automáticamente el NUC basado en la IP
const snapshot = await fetch(
  'https://tu-api.railway.app/api/camaras/192.168.60.10/snapshot'
).then(r => r.json());
```

### **3. Especificar NUC manualmente:**

```javascript
// Forzar uso de un NUC específico
const snapshot = await fetch(
  'https://tu-api.railway.app/api/camaras/192.168.60.10/snapshot?nuc_id=nuc_sede1'
).then(r => r.json());
```

---

## 🔧 **Troubleshooting**

### **Error: "No hay NUCs disponibles"**

**Causa:** No se configuró la variable `NUC_URLS` o está vacía.

**Solución:**
1. Verifica la variable en Railway
2. Formato correcto: `url1,url2,url3` o `nombre1:url1,nombre2:url2`

---

### **Error: "No se pudo conectar al NUC"**

**Causa:** El NUC no está accesible o está caído.

**Solución:**
1. Verifica que Tailscale/ZeroTier esté corriendo en el NUC
2. Verifica que el backend esté corriendo en el NUC: `curl http://localhost:5000/api/status`
3. Prueba la conexión desde tu PC (con VPN instalado)

---

### **El NUC incorrecto está siendo seleccionado**

**Causa:** El mapeo automático por IP no funciona correctamente.

**Solución:**
1. Usa el parámetro `nuc_id` explícitamente
2. O personaliza la lógica de mapeo en `seleccionar_nuc()` en `server.py`

---

## 📊 **Resumen de Configuración:**

| Variable | Formato | Ejemplo |
|----------|---------|---------|
| **NUC_URLS** | `url1,url2,url3` | `http://100.64.0.1:5000,http://100.64.0.2:5000` |
| **NUC_URLS** | `nombre:url,nombre:url` | `nuc1:http://100.64.0.1:5000,nuc2:http://100.64.0.2:5000` |

---

## ✅ **Checklist:**

- [ ] Tailscale/ZeroTier instalado en cada NUC
- [ ] IP de cada NUC obtenida
- [ ] Backend corriendo en cada NUC
- [ ] Variable `NUC_URLS` configurada en Railway
- [ ] Endpoint `/api/nucs` responde correctamente
- [ ] Detección de cámaras funciona en cada NUC
- [ ] Todo funcionando ✅

---

## 🎯 **Siguiente Paso:**

1. Configura cada NUC con Tailscale/ZeroTier
2. Configura la variable `NUC_URLS` en Railway
3. Prueba el endpoint `/api/nucs`
4. ¡Disfruta tu sistema multi-NUC! 🎉

