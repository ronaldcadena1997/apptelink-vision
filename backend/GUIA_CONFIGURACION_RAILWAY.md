# 🚂 Guía: Configuración de Railway

## 🎯 **Objetivo**
Configurar el backend en Railway para que se conecte al NUC a través de Tailscale y acceda a las cámaras.

---

## ✅ **PASO 1: Verificar que Railway está Desplegado**

### **1.1. Ve a Railway Dashboard:**
- Abre: https://railway.app
- Inicia sesión con tu cuenta
- Selecciona tu proyecto

### **1.2. Verifica que el despliegue está activo:**
- Ve a **Deployments**
- Debe haber un despliegue reciente (verde = activo)
- Si no hay despliegue, haz clic en **"Deploy"**

---

## ✅ **PASO 2: Configurar Variables de Entorno**

### **2.1. Ir a Settings:**
1. En tu proyecto de Railway, haz clic en **Settings**
2. Busca la sección **Variables**
3. Haz clic en **"New Variable"** para cada variable

### **2.2. Configurar NUC_URLS:**

**Variable:** `NUC_URLS`

**Valor:**
```
nuc_sede1:http://100.92.50.72:5000
```

**⚠️ IMPORTANTE:** 
- Reemplaza `100.92.50.72` con tu IP de Tailscale si es diferente
- Esta es la IP que obtuviste con `tailscale ip -4` en el NUC

**Formato para múltiples NUCs:**
```
nuc_sede1:http://100.92.50.72:5000,nuc_sede2:http://100.92.50.XX:5000
```

### **2.3. Configurar CAMARAS_IPS:**

**Variable:** `CAMARAS_IPS`

**Valor:**
```
192.168.60.65
```

**⚠️ IMPORTANTE:**
- Esta es la IP de tu cámara (según tu configuración)
- Si tienes más cámaras, sepáralas por comas:
  ```
  192.168.60.65,192.168.60.66,192.168.60.67
  ```

### **2.4. Variables Opcionales (si las necesitas):**

**USUARIO_CAMARAS:**
```
admin
```

**CONTRASENA_CAMARAS:**
```
citikold.2020
```

**⚠️ Nota:** Estas son opcionales si ya están en `config.py` o si usas los valores por defecto.

---

## ✅ **PASO 3: Verificar Configuración**

### **3.1. Verificar que las variables están configuradas:**

En Railway → Settings → Variables, debes ver:

```
✅ NUC_URLS = nuc_sede1:http://100.92.50.72:5000
✅ CAMARAS_IPS = 192.168.60.65
```

### **3.2. Verificar logs del despliegue:**

1. Ve a **Deployments**
2. Haz clic en el despliegue más reciente
3. Abre la pestaña **Logs**
4. Busca mensajes como:

```
📋 Usando variables de entorno
📹 IPs de cámaras configuradas: 1
   - 192.168.60.65: Cámara Principal
🔗 Modo PROXY activado. NUCs configurados: 1
   - nuc_sede1: http://100.92.50.72:5000
```

---

## ✅ **PASO 4: Probar la Conexión**

### **4.1. Obtener la URL de Railway:**

1. En Railway, ve a tu servicio
2. Haz clic en **Settings** → **Networking**
3. Copia la **Public Domain** (ejemplo: `tu-proyecto.up.railway.app`)

### **4.2. Probar el endpoint de estado:**

Abre en tu navegador o con curl:

```
https://tu-proyecto.up.railway.app/api/status
```

**Deberías ver:**
```json
{
  "status": "online",
  "timestamp": "2025-01-04T...",
  "version": "1.0.0",
  "modo": "proxy",
  "nucs_disponibles": 1
}
```

### **4.3. Probar listar NUCs:**

```
https://tu-proyecto.up.railway.app/api/nucs
```

**Deberías ver:**
```json
{
  "success": true,
  "modo": "proxy",
  "nucs": [
    {
      "id": "nuc_sede1",
      "url": "http://100.92.50.72:5000",
      "disponible": true
    }
  ],
  "total": 1
}
```

**⚠️ Si `"disponible": false`:**
- Verifica que el puente genérico esté corriendo en el NUC
- Verifica que Tailscale esté conectado
- Verifica que el puerto 5000 esté abierto

### **4.4. Probar detectar cámaras:**

```
https://tu-proyecto.up.railway.app/api/camaras/detectar
```

**Deberías ver:**
```json
{
  "success": true,
  "modo": "configurado",
  "camaras": [
    {
      "id": 1,
      "ip": "192.168.60.65",
      "url": "rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/101",
      "estado": "activa",
      "nombre": "Cámara Principal",
      "configurada": true
    }
  ],
  "total": 1
}
```

---

## 🔧 **Configuración Avanzada: Usar config.py en lugar de Variables**

### **Opción: Subir config.py a GitHub**

Si prefieres usar `config.py` en lugar de variables de entorno:

1. **Asegúrate de que `config.py` está en el repositorio:**
   ```powershell
   git add backend/config.py
   git commit -m "Agregar config.py con configuración"
   git push
   ```

2. **Railway usará automáticamente `config.py`** si no hay variables de entorno configuradas

3. **Las variables de entorno tienen prioridad** sobre `config.py`

---

## 🚨 **Troubleshooting**

### **Problema 1: "No se pudo conectar al NUC"**

**Causas posibles:**
- ❌ Tailscale no está corriendo en el NUC
- ❌ El puente genérico no está corriendo
- ❌ La IP de Tailscale en Railway es incorrecta
- ❌ El firewall de Windows está bloqueando el puerto 5000

**Solución:**
1. En el NUC, ejecuta: `.\verificar_servicios.bat`
2. Verifica que Tailscale tenga IP: `tailscale ip -4`
3. Verifica que el puente esté corriendo: `netstat -ano | findstr :5000`
4. Verifica la IP en Railway coincide con la del NUC

### **Problema 2: "No hay NUCs disponibles"**

**Causa:** La variable `NUC_URLS` no está configurada o está vacía.

**Solución:**
1. Ve a Railway → Settings → Variables
2. Verifica que `NUC_URLS` esté configurada
3. Formato correcto: `nuc_sede1:http://100.92.50.72:5000`

### **Problema 3: "No se encuentran cámaras"**

**Causas posibles:**
- ❌ La variable `CAMARAS_IPS` no está configurada
- ❌ Las IPs de las cámaras son incorrectas
- ❌ El NUC no puede acceder a las cámaras en su red local

**Solución:**
1. Verifica `CAMARAS_IPS` en Railway
2. Verifica que las IPs sean correctas
3. Desde el NUC, prueba: `ping 192.168.60.65`

### **Problema 4: "El puente no responde"**

**Causa:** El puente genérico se cerró o no está corriendo.

**Solución:**
1. En el NUC, ejecuta: `.\verificar_servicios.bat`
2. Si no está corriendo, inícialo manualmente:
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowApptelinkVision\backend
   python puente_generico_nuc.py
   ```
3. O verifica que el inicio automático esté configurado

---

## 📋 **Checklist de Configuración**

Antes de considerar que Railway está configurado:

- [ ] ✅ Proyecto desplegado en Railway
- [ ] ✅ Variable `NUC_URLS` configurada con tu IP de Tailscale
- [ ] ✅ Variable `CAMARAS_IPS` configurada con IPs de tus cámaras
- [ ] ✅ Logs muestran "Modo PROXY activado"
- [ ] ✅ Endpoint `/api/status` responde correctamente
- [ ] ✅ Endpoint `/api/nucs` muestra el NUC como "disponible: true"
- [ ] ✅ Endpoint `/api/camaras/detectar` muestra las cámaras
- [ ] ✅ El puente genérico está corriendo en el NUC
- [ ] ✅ Tailscale está conectado en el NUC

---

## 🔄 **Actualizar Configuración**

### **Si cambias la IP de Tailscale:**

1. Ve a Railway → Settings → Variables
2. Edita `NUC_URLS` con la nueva IP
3. Railway se reiniciará automáticamente

### **Si agregas más cámaras:**

1. Ve a Railway → Settings → Variables
2. Edita `CAMARAS_IPS` agregando las nuevas IPs separadas por comas
3. Railway se reiniciará automáticamente

### **Si agregas más NUCs:**

1. Ve a Railway → Settings → Variables
2. Edita `NUC_URLS` agregando más NUCs separados por comas:
   ```
   nuc_sede1:http://100.92.50.72:5000,nuc_sede2:http://100.92.50.XX:5000
   ```
3. Actualiza `CAMARAS_IPS` con todas las cámaras de todos los NUCs

---

## 📝 **Resumen de Variables de Entorno**

| Variable | Valor Ejemplo | Descripción |
|----------|---------------|-------------|
| **NUC_URLS** | `nuc_sede1:http://100.92.50.72:5000` | IP de Tailscale del NUC |
| **CAMARAS_IPS** | `192.168.60.65` | IPs de las cámaras (separadas por comas) |
| **USUARIO_CAMARAS** | `admin` | Usuario para acceder a cámaras (opcional) |
| **CONTRASENA_CAMARAS** | `citikold.2020` | Contraseña para acceder a cámaras (opcional) |

---

## 🎯 **Siguiente Paso**

Una vez que Railway esté configurado:

1. ✅ Verifica que todo funciona con los endpoints de prueba
2. ✅ Configura el frontend para usar la URL de Railway
3. ✅ Prueba la aplicación completa

---

## 📞 **Soporte Adicional**

- 📄 **Configuración de cámaras por NUC:** Ver `CONFIGURACION_CAMARAS_POR_NUC.md`
- 📄 **Pasos para ejecutar puente:** Ver `PASOS_EJECUTAR_PUENTE_NUC.md`
- 📄 **Mi configuración:** Ver `MI_CONFIGURACION.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
