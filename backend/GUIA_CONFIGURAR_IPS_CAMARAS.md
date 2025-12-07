# 📹 Guía: Configurar IPs de Cámaras Centralmente en Railway

## 🎯 **Objetivo:**
Configurar las IPs de las cámaras en Railway (variables de entorno) para no tener que modificar código en cada NUC.

---

## ✅ **PASO 1: Obtener IPs de tus Cámaras**

### **Opción A: Desde tus Scripts Actuales**

Si ya tienes scripts con IPs hardcodeadas, copia esas IPs:

```python
# Ejemplo de tu script actual
CAMARAS = [
    "192.168.60.64",
    "192.168.60.65",
    "192.168.60.66",
]
```

**Anota estas IPs.**

### **Opción B: Detectar Automáticamente**

Ejecuta el endpoint de detección una vez para obtener las IPs:

```powershell
# Desde el NUC o desde Railway
curl http://localhost:5000/api/camaras/detectar
```

**Copia las IPs de las cámaras detectadas.**

---

## ✅ **PASO 2: Configurar IPs en Railway**

### **2.1. Acceder a Railway:**

1. Ve a: https://railway.app
2. Inicia sesión
3. Selecciona tu proyecto
4. Click en el servicio **Backend**

### **2.2. Agregar Variable de Entorno:**

1. **Click en "Variables"** (en el menú lateral)

2. **Click en "New Variable"**

3. **Configura la variable:**
   - **Nombre:** `CAMARAS_IPS`
   - **Valor:** `192.168.60.64,192.168.60.65,192.168.60.66,192.168.60.67`
   - **Reemplaza con las IPs reales de tus cámaras**

4. **Click en "Add"**

### **2.3. Formato de la Variable:**

**Formato simple (recomendado):**
```
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66
```

**Ejemplo con muchas cámaras:**
```
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66,192.168.60.67,192.168.60.68,192.168.60.69,192.168.60.70
```

**📝 Nota:**
- Separa las IPs con comas (`,`)
- Sin espacios (o con espacios, el código los elimina automáticamente)
- Una IP por cámara

---

## ✅ **PASO 3: Verificar Configuración**

### **3.1. Redesplegar Backend en Railway:**

Después de agregar la variable:

1. **Railway detectará los cambios automáticamente** y redesplegará
2. **O manualmente:** Click en "Deploy" → "Redeploy"

**⏱️ Espera 2-3 minutos** mientras Railway redespliega

### **3.2. Verificar que Funciona:**

**Prueba el endpoint de cámaras configuradas:**

```powershell
# En PowerShell
Invoke-WebRequest -Uri https://tu-backend.railway.app/api/camaras/configuradas | Select-Object -ExpandProperty Content

# O usando curl
curl https://tu-backend.railway.app/api/camaras/configuradas
```

**Debe responder:**
```json
{
  "success": true,
  "camaras_configuradas": [
    "192.168.60.64",
    "192.168.60.65",
    "192.168.60.66"
  ],
  "total": 3,
  "modo": "configurado"
}
```

### **3.3. Probar Detección de Cámaras:**

```powershell
# Detectar cámaras (usará las IPs configuradas)
Invoke-WebRequest -Uri https://tu-backend.railway.app/api/camaras/detectar | Select-Object -ExpandProperty Content
```

**Debe responder con las cámaras configuradas:**
```json
{
  "success": true,
  "modo": "configurado",
  "camaras": [
    {
      "id": 1,
      "ip": "192.168.60.64",
      "estado": "activa",
      "configurada": true
    },
    ...
  ]
}
```

---

## 🔄 **Cómo Funciona:**

### **Con IPs Configuradas:**
1. Backend en Railway lee `CAMARAS_IPS` de variables de entorno
2. Usa esas IPs directamente (más rápido, no escanea toda la red)
3. Hace peticiones al puente genérico en el NUC usando esas IPs
4. El puente genérico accede a las cámaras y retorna datos

### **Sin IPs Configuradas:**
1. Backend en Railway escanea la red automáticamente
2. Detecta cámaras disponibles
3. Funciona igual que antes (comportamiento por defecto)

---

## ✅ **Ventajas:**

### **1. Configuración Centralizada:**
- ✅ Todas las IPs en Railway (una sola vez)
- ✅ NO necesitas modificar código en cada NUC
- ✅ NO necesitas modificar scripts en cada NUC

### **2. Más Rápido:**
- ✅ No escanea toda la red (usa IPs conocidas)
- ✅ Respuesta más rápida
- ✅ Menos carga en la red

### **3. Más Confiable:**
- ✅ Siempre usa las mismas IPs
- ✅ No depende del escaneo de red
- ✅ Funciona aunque el escaneo falle

### **4. Escalable:**
- ✅ Agregas nueva cámara → Solo agregas IP en Railway
- ✅ Quitas cámara → Solo quitas IP en Railway
- ✅ El código NO cambia

---

## 📝 **Agregar o Quitar Cámaras:**

### **Agregar Nueva Cámara:**

1. **Obtén la IP de la nueva cámara**
2. **Ve a Railway → Variables**
3. **Edita `CAMARAS_IPS`**
4. **Agrega la nueva IP al final:**
   ```
   CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66,192.168.60.67
   ```
   (Agregaste `192.168.60.67`)
5. **Railway redesplegará automáticamente**

### **Quitar Cámara:**

1. **Ve a Railway → Variables**
2. **Edita `CAMARAS_IPS`**
3. **Quita la IP de la cámara:**
   ```
   CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66
   ```
   (Quitaste `192.168.60.67`)
4. **Railway redesplegará automáticamente**

**NO necesitas modificar código en ningún lado.**

---

## 🔧 **Troubleshooting**

### **❌ Error: "No se detectan las cámaras configuradas"**

**Soluciones:**
1. ✅ Verifica que la variable `CAMARAS_IPS` esté configurada en Railway
2. ✅ Verifica el formato (IPs separadas por comas, sin espacios extra)
3. ✅ Verifica que Railway haya redesplegado después de agregar la variable
4. ✅ Prueba el endpoint: `/api/camaras/configuradas` para ver las IPs leídas

### **❌ Error: "Cámara no accesible"**

**Soluciones:**
1. ✅ Verifica que la IP de la cámara sea correcta
2. ✅ Verifica que la cámara esté encendida
3. ✅ Verifica que el NUC pueda acceder a esa IP (misma red local)
4. ✅ Verifica que el puente genérico esté corriendo en el NUC

### **❌ Las cámaras no aparecen en el frontend**

**Soluciones:**
1. ✅ Verifica que `CAMARAS_IPS` esté configurada
2. ✅ Verifica que el endpoint `/api/camaras/detectar` funcione
3. ✅ Verifica que el frontend esté usando la URL correcta del backend

---

## 📊 **Resumen de Variables en Railway:**

### **Variables Necesarias:**

```
# IP del NUC (Tailscale)
NUC_TAILSCALE_IP=100.64.0.15
# O
NUC_URL=http://100.64.0.15:5000

# IPs de las cámaras (separadas por comas)
CAMARAS_IPS=192.168.60.64,192.168.60.65,192.168.60.66
```

---

## ✅ **Checklist:**

- [ ] IPs de cámaras obtenidas y anotadas
- [ ] Variable `CAMARAS_IPS` configurada en Railway
- [ ] Formato correcto (IPs separadas por comas)
- [ ] Backend en Railway redesplegado
- [ ] Endpoint `/api/camaras/configuradas` funciona
- [ ] Endpoint `/api/camaras/detectar` muestra las cámaras configuradas
- [ ] Frontend muestra las cámaras correctamente

---

## 🎯 **Resumen Rápido:**

1. **Obtén las IPs de tus cámaras** (de tus scripts o detectando)
2. **En Railway → Variables:** Agrega `CAMARAS_IPS=ip1,ip2,ip3`
3. **Railway redesplegará automáticamente**
4. **Verifica:** Prueba `/api/camaras/configuradas`

**¡Listo!** Ahora todas las IPs están centralizadas en Railway y NO necesitas modificar código en los NUCs.

---

## 📞 **Soporte Adicional**

- 📄 **Puente genérico:** Ver `SOLUCION_PUENTE_GENERICO.md`
- 📄 **Conexión Tailscale:** Ver `GUIA_CONEXION_TAILSCALE_RAILWAY.md`
- 📄 **Configuración múltiples NUCs:** Ver `CONFIGURACION_MULTIPLES_NUCS.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
