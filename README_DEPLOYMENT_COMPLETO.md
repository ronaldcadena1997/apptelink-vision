# 🚀 Guía Completa de Deployment - AppTelink Vision

## 📋 **Índice**

1. [Requisitos Previos](#requisitos-previos)
2. [Paso 1: Configurar NUCs Locales](#paso-1-configurar-nucs-locales)
3. [Paso 2: Configurar Backend en Servidor (Railway)](#paso-2-configurar-backend-en-servidor-railway)
4. [Paso 3: Configurar Frontend en Servidor (Railway)](#paso-3-configurar-frontend-en-servidor-railway)
5. [Paso 4: Verificar Todo](#paso-4-verificar-todo)
6. [Troubleshooting](#troubleshooting)

---

## ✅ **Requisitos Previos**

Antes de empezar, necesitas:

- [ ] Cuenta en Railway (gratis): https://railway.app
- [ ] Cuenta en GitHub (gratis): https://github.com
- [ ] Código del proyecto en GitHub
- [ ] Acceso a cada NUC (donde están las cámaras) - **Windows**
- [ ] Acceso a Railway dashboard
- [ ] Git instalado en tu PC (Windows): https://git-scm.com/download/win
- [ ] Python instalado en cada NUC: https://www.python.org/downloads/

**📝 Nota:** Esta guía está diseñada para **Windows**. Todos los comandos son para PowerShell o CMD.

**💡 Cómo abrir PowerShell:**
- Presiona `Windows + X` y selecciona "Windows PowerShell" o "Terminal"
- O busca "PowerShell" en el menú de inicio
- O presiona `Windows + R`, escribe `powershell` y presiona Enter

**💡 Cómo abrir CMD:**
- Presiona `Windows + R`, escribe `cmd` y presiona Enter
- O busca "Command Prompt" en el menú de inicio

**📡 Si tu NUC no tiene internet (SIM7600):**
Si tu NUC no tiene conexión a internet y usas un módulo SIM7600, consulta la guía:
- 📄 **Ver:** `backend/GUIA_SIM7600.md` - Configuración completa del SIM7600 con SSCOM

---

## 📍 **PASO 1: Configurar NUCs Locales**

### **1.1. Para cada NUC, instala Tailscale**

**En cada NUC (Windows):**

1. **Descarga Tailscale para Windows:**
   - Ve a: https://tailscale.com/download/windows
   - Descarga el instalador `.exe`
   - Ejecuta el instalador y sigue las instrucciones

2. **Inicia Tailscale:**
   - Abre Tailscale desde el menú de inicio
   - Click en "Log in" o "Sign up"
   - Inicia sesión o crea una cuenta

3. **Obtén la IP de Tailscale:**
   - Abre PowerShell o CMD
   - Ejecuta:
   ```powershell
   tailscale ip -4
   ```
   - Copia la IP que muestra (ejemplo: `100.64.0.1`)

**📝 Anota la IP de cada NUC:**
- NUC 1: `100.64.0.1` (ejemplo)
- NUC 2: `100.64.0.2` (ejemplo)
- NUC 3: `100.64.0.3` (ejemplo)

---

### **1.2. Iniciar Backend en cada NUC**

**⚠️ IMPORTANTE: El backend DEBE estar corriendo en el NUC**

**¿Por qué?** El backend en Railway actúa como **proxy/gateway**. No puede acceder directamente a las cámaras porque están en tu red local. Necesita conectarse al backend en el NUC, que SÍ tiene acceso a las cámaras.

**En cada NUC (Windows):**

1. **Abre PowerShell o CMD como Administrador**

2. **Navega a la carpeta del backend:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   ```

3. **Verifica que Python esté instalado:**
   ```powershell
   python --version
   ```
   Si no está instalado, descarga desde: https://www.python.org/downloads/
   **Importante:** Al instalar, marca la opción "Add Python to PATH"

4. **Instala dependencias (si no están instaladas):**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Inicia el backend:**
   ```powershell
   python server.py
   ```
   
   **💡 Este backend debe estar corriendo SIEMPRE** para que Railway pueda conectarse a él y acceder a las cámaras.

**✅ Verificar que funciona:**
- Abre otra ventana de PowerShell o CMD
- Ejecuta:
  ```powershell
  # Opción 1: Usando PowerShell
  Invoke-WebRequest -Uri http://localhost:5000/api/status | Select-Object -ExpandProperty Content
  
  # Opción 2: Usando curl (si está disponible)
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

**📝 Repite este paso en cada NUC**

---

### **1.3. Verificar acceso desde tu PC (Opcional pero recomendado)**

**En tu PC (Windows):**

1. **Instala Tailscale:**
   - Descarga: https://tailscale.com/download/windows
   - Instala y ejecuta Tailscale
   - Inicia sesión con la misma cuenta que usaste en los NUCs

2. **Prueba la conexión:**
   ```powershell
   # En PowerShell
   Invoke-WebRequest -Uri http://100.64.0.1:5000/api/status | Select-Object -ExpandProperty Content
   
   # O usando curl
   curl http://100.64.0.1:5000/api/status
   ```
   
   **Reemplaza `100.64.0.1` con la IP real de tu NUC**

**✅ Si funciona, el NUC está correctamente configurado**

---

## 🖥️ **PASO 2: Configurar Backend en Servidor (Railway)**

### **2.1. Conectar Repositorio a Railway**

1. **Ve a Railway:** https://railway.app
2. **Click en "New Project"**
3. **Selecciona "Deploy from GitHub repo"**
4. **Autoriza Railway** para acceder a tu repositorio
5. **Selecciona tu repositorio:** `proyectowebApptelinkVision`
6. **Selecciona la rama:** `main` (o la que uses)

---

### **2.2. Configurar Servicio Backend**

1. **Railway detectará automáticamente** el backend
2. **Si no, crea un nuevo servicio:**
   - Click en "New" → "GitHub Repo"
   - Selecciona el mismo repositorio
   - Selecciona la carpeta `backend`

---

### **2.3. Obtener IP de Tailscale del NUC**

**Antes de configurar Railway, necesitas la IP de Tailscale de cada NUC:**

**En cada NUC (PowerShell o CMD):**
```powershell
tailscale ip -4
```

**Ejemplo de salida:**
```
100.64.0.15
```

**📝 Anota la IP de cada NUC:**
- NUC 1: `100.64.0.15` (ejemplo)
- NUC 2: `100.64.0.16` (ejemplo)
- NUC 3: `100.64.0.17` (ejemplo)

**✅ Verifica que Tailscale esté conectado:**
```powershell
tailscale status
```
Debe mostrar `online` y `direct`. Si no, ejecuta: `tailscale up`

---

### **2.4. Configurar Variables de Entorno en Railway**

**En Railway → Tu Proyecto → Backend Service → Variables:**

**Click en "New Variable" y agrega:**

#### **Para un solo NUC:**
- **Nombre:** `NUC_URL`
- **Valor:** `http://100.64.0.15:5000`
- **Reemplaza `100.64.0.15` con la IP real de tu NUC (de Tailscale)**

**📝 Importante:**
- Usa **`http://`** (no `https://`) porque es conexión interna de Tailscale
- Usa la **IP de Tailscale** (ej: `100.64.0.15`), NO la IP local (ej: `192.168.60.15`)
- El puerto es **`:5000`** (puerto donde corre el backend en el NUC)

---

#### **Para múltiples NUCs (Recomendado):**

- **Nombre:** `NUC_URLS`
- **Valor:** `nuc_sede1:http://100.64.0.15:5000,nuc_sede2:http://100.64.0.16:5000,nuc_sede3:http://100.64.0.17:5000`

**Formato:**
- **Con nombres:** `nombre1:url1,nombre2:url2,nombre3:url3`
- **Sin nombres:** `url1,url2,url3` (se asignarán nombres automáticos: `nuc_1`, `nuc_2`, etc.)

**📝 Reemplaza las IPs con las IPs reales de tus NUCs (de Tailscale)**

---

#### **Configurar IPs de Cámaras (Opcional pero Recomendado):**

- **Nombre:** `CAMARAS_IPS`
- **Valor:** `192.168.60.64,192.168.60.65,192.168.60.66`

**Formato:** IPs separadas por comas (sin espacios)

**Ventajas:**
- ✅ No necesitas modificar código en cada NUC
- ✅ Configuración centralizada en Railway
- ✅ Más rápido (no escanea toda la red)
- ✅ Agregas/quitas cámaras solo cambiando esta variable

**💡 Para más detalles sobre configuración de IPs de cámaras, ver:** `backend/GUIA_CONFIGURAR_IPS_CAMARAS.md`

**💡 Para más detalles sobre la conexión Tailscale → Railway, ver:** `backend/GUIA_CONEXION_TAILSCALE_RAILWAY.md`

---

### **2.5. Configurar Build Settings (Si es necesario)**

**En Railway → Backend Service → Settings → Build:**

- **Build Command:** (dejar vacío, Railway lo detecta automáticamente)
- **Start Command:** `python server.py`

---

### **2.6. Desplegar Backend**

1. **Railway desplegará automáticamente** cuando hagas push a GitHub
2. **O manualmente:** Click en "Deploy" → "Redeploy"

**⏱️ Espera 2-3 minutos** mientras Railway construye y despliega

---

### **2.7. Obtener URL del Backend**

**En Railway → Backend Service → Settings → Domains:**

1. **Click en "Generate Domain"** (si no hay uno)
2. **Copia la URL:** `https://tu-backend-production.up.railway.app`

**📝 Anota esta URL, la necesitarás para el frontend**

---

### **2.8. Verificar Backend Desplegado**

**Prueba estos endpoints (en PowerShell o CMD):**

```powershell
# Status del backend
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/status | Select-Object -ExpandProperty Content

# Listar NUCs (si configuraste múltiples)
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/nucs | Select-Object -ExpandProperty Content

# Detectar cámaras (debe hacer proxy al NUC)
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/camaras/detectar | Select-Object -ExpandProperty Content
```

**O usando curl (si está disponible):**
```powershell
curl https://tu-backend-production.up.railway.app/api/status
curl https://tu-backend-production.up.railway.app/api/nucs
curl https://tu-backend-production.up.railway.app/api/camaras/detectar
```

**✅ Si todo funciona, el backend está correctamente configurado**

---

## 🌐 **PASO 3: Configurar Frontend en Servidor (Railway)**

### **3.1. Actualizar URL del API en el Frontend**

**En tu PC, edita el archivo:**

`src/config/api.js`

**Cambia esta línea:**

```javascript
// ANTES (local):
// export const API_BASE_URL = 'http://192.168.60.15:5000';

// DESPUÉS (producción):
export const API_BASE_URL = 'https://tu-backend-production.up.railway.app';
```

**📝 Reemplaza `tu-backend-production.up.railway.app` con la URL real de tu backend en Railway**

---

### **3.2. Subir Cambios a GitHub**

**En tu PC (PowerShell o CMD):**

```powershell
# Navegar a la carpeta del proyecto
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision

# Agregar cambios
git add src/config/api.js

# Commit
git commit -m "Update API URL to Railway backend"

# Push a GitHub
git push
```

**Si Git no está configurado, primero configura tu usuario:**
```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

### **3.3. Configurar Servicio Frontend en Railway**

1. **En Railway → Tu Proyecto**
2. **Click en "New" → "GitHub Repo"**
3. **Selecciona el mismo repositorio**
4. **Railway detectará automáticamente** que es un proyecto Expo/React

---

### **3.4. Configurar Build Settings del Frontend**

**En Railway → Frontend Service → Settings → Build:**

- **Build Command:** `npm install && npm run build`
- **Start Command:** `npx serve dist -s -p $PORT`

**O si Railway usa Dockerfile:**
- Railway usará automáticamente el `Dockerfile` en la raíz del proyecto

---

### **3.5. Desplegar Frontend**

1. **Railway desplegará automáticamente** después del push
2. **O manualmente:** Click en "Deploy" → "Redeploy"

**⏱️ Espera 3-5 minutos** mientras Railway construye y despliega

---

### **3.6. Obtener URL del Frontend**

**En Railway → Frontend Service → Settings → Domains:**

1. **Click en "Generate Domain"** (si no hay uno)
2. **Copia la URL:** `https://tu-frontend-production.up.railway.app`

**📝 Esta es la URL pública de tu aplicación web**

---

## ✅ **PASO 4: Verificar Todo**

### **4.1. Verificar Backend**

**En PowerShell o CMD:**

```powershell
# 1. Status del backend
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/status | Select-Object -ExpandProperty Content

# 2. Listar NUCs (si configuraste múltiples)
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/nucs | Select-Object -ExpandProperty Content

# 3. Detectar cámaras
Invoke-WebRequest -Uri https://tu-backend-production.up.railway.app/api/camaras/detectar | Select-Object -ExpandProperty Content
```

**O usando curl:**
```powershell
curl https://tu-backend-production.up.railway.app/api/status
curl https://tu-backend-production.up.railway.app/api/nucs
curl https://tu-backend-production.up.railway.app/api/camaras/detectar
```

**✅ Debe responder con las cámaras detectadas**

---

### **4.2. Verificar Frontend**

1. **Abre en el navegador:**
   ```
   https://tu-frontend-production.up.railway.app
   ```

2. **Prueba las funcionalidades:**
   - ✅ Ver cámaras
   - ✅ Detectar cámaras
   - ✅ Ver snapshots
   - ✅ Configurar cercas
   - ✅ Ver intrusos

**✅ Si todo funciona, ¡estás listo!**

---

### **4.3. Verificar desde Móvil (iOS/Android)**

1. **Abre Expo Go** en tu móvil
2. **Escanea el QR** que muestra Railway (si está disponible)
3. **O usa la URL** del frontend en el navegador móvil

**✅ Debe funcionar igual que en web**

---

## 🔧 **Troubleshooting**

### **❌ Error: "No se pudo conectar al NUC"**

**Causa:** El backend en Railway no puede alcanzar el NUC.

**Soluciones:**
1. ✅ Verifica que Tailscale esté corriendo en el NUC:
   - Abre Tailscale en el NUC (busca "Tailscale" en el menú de inicio)
   - Verifica que esté conectado (debe mostrar "Connected")
   - O en PowerShell:
   ```powershell
   tailscale status
   ```

2. ✅ Verifica la IP del NUC:
   ```powershell
   # En el NUC (PowerShell)
   tailscale ip -4
   ```

3. ✅ Verifica que el backend esté corriendo en el NUC:
   ```powershell
   # En el NUC (PowerShell)
   Invoke-WebRequest -Uri http://localhost:5000/api/status | Select-Object -ExpandProperty Content
   
   # O usando curl
   curl http://localhost:5000/api/status
   ```

4. ✅ Verifica la variable `NUC_URL` o `NUC_URLS` en Railway:
   - Debe ser: `http://IP_DE_TAILSCALE:5000`
   - No debe ser: `http://192.168.60.15:5000` (IP local no funciona)

5. ✅ Prueba desde tu PC (con Tailscale instalado):
   ```powershell
   # En tu PC (PowerShell)
   Invoke-WebRequest -Uri http://100.64.0.1:5000/api/status | Select-Object -ExpandProperty Content
   
   # O usando curl
   curl http://100.64.0.1:5000/api/status
   ```

---

### **❌ Error: "No hay NUCs disponibles"**

**Causa:** La variable `NUC_URLS` no está configurada o está vacía.

**Solución:**
1. ✅ Ve a Railway → Variables
2. ✅ Verifica que `NUC_URLS` esté configurada
3. ✅ Formato correcto: `url1,url2,url3` o `nombre1:url1,nombre2:url2`

---

### **❌ Error: "Network request timed out" en el Frontend**

**Causa:** El frontend no puede conectarse al backend.

**Soluciones:**
1. ✅ Verifica que la URL del API en `src/config/api.js` sea correcta
2. ✅ Verifica que el backend esté desplegado y funcionando
3. ✅ Verifica que no haya errores en la consola del navegador (F12)

---

### **❌ Las cámaras no aparecen**

**Causa:** El NUC no puede escanear la red local.

**Soluciones:**
1. ✅ Verifica que el backend en el NUC esté en la misma red que las cámaras
2. ✅ Prueba desde el NUC directamente:
   ```powershell
   # En el NUC (PowerShell)
   Invoke-WebRequest -Uri http://localhost:5000/api/camaras/detectar | Select-Object -ExpandProperty Content
   
   # O usando curl
   curl http://localhost:5000/api/camaras/detectar
   ```
3. ✅ Verifica que las cámaras estén encendidas y accesibles

---

### **❌ Error en el build del Frontend**

**Causa:** Problemas con dependencias o configuración.

**Soluciones:**
1. ✅ Verifica que `package.json` tenga todas las dependencias
2. ✅ Verifica que el `Dockerfile` esté correcto
3. ✅ Revisa los logs de Railway para ver el error específico

---

## 📊 **Resumen de URLs y Configuración**

### **URLs Importantes:**

| Componente | URL | Dónde encontrarla |
|------------|-----|-------------------|
| **Frontend** | `https://tu-frontend.up.railway.app` | Railway → Frontend Service → Domains |
| **Backend** | `https://tu-backend.up.railway.app` | Railway → Backend Service → Domains |
| **NUC 1** | `http://100.64.0.1:5000` | Tailscale: `tailscale ip -4` |
| **NUC 2** | `http://100.64.0.2:5000` | Tailscale: `tailscale ip -4` |

---

### **Variables de Entorno en Railway:**

**Backend Service → Variables:**

```
NUC_URLS=nuc_sede1:http://100.64.0.1:5000,nuc_sede2:http://100.64.0.2:5000
```

---

### **Archivos a Modificar:**

1. **`src/config/api.js`** - URL del backend:
   ```javascript
   export const API_BASE_URL = 'https://tu-backend.up.railway.app';
   ```

---

## ✅ **Checklist Final**

Antes de considerar que todo está listo:

- [ ] Tailscale instalado en cada NUC
- [ ] IP de cada NUC obtenida y anotada
- [ ] Backend corriendo en cada NUC (`python server.py`)
- [ ] Backend desplegado en Railway
- [ ] Variable `NUC_URLS` configurada en Railway
- [ ] Frontend actualizado con URL del backend
- [ ] Frontend desplegado en Railway
- [ ] Endpoint `/api/status` funciona
- [ ] Endpoint `/api/nucs` funciona (si múltiples NUCs)
- [ ] Endpoint `/api/camaras/detectar` funciona
- [ ] Frontend web accesible y funcionando
- [ ] Cámaras aparecen en el frontend
- [ ] Snapshots funcionan
- [ ] Todo funcionando correctamente ✅

---

## 🎉 **¡Listo!**

Si completaste todos los pasos y el checklist, tu aplicación está completamente desplegada y funcionando.

**Tu aplicación ahora:**
- ✅ Está accesible desde cualquier lugar (internet)
- ✅ Se conecta a múltiples NUCs
- ✅ Accede a las cámaras en red local
- ✅ Funciona en web, iOS y Android

---

## 📞 **Soporte Adicional**

Si necesitas más ayuda:

- 📄 **Múltiples NUCs:** Ver `backend/CONFIGURACION_MULTIPLES_NUCS.md`
- 📄 **Arquitectura:** Ver `backend/ARQUITECTURA_SERVIDOR.md`
- 📄 **Acceso Directo:** Ver `backend/ACCESO_DIRECTO_NUC.md`
- 📡 **SIM7600 (Internet Celular):** Ver `backend/GUIA_SIM7600.md`
- 🔗 **Conexión Tailscale → Railway:** Ver `backend/GUIA_CONEXION_TAILSCALE_RAILWAY.md`
- 🏗️ **¿Por qué el backend debe correr en el NUC?** Ver `backend/EXPLICACION_ARQUITECTURA.md`
- 📋 **Archivo de configuración centralizado:** Ver `backend/GUIA_ARCHIVO_CONFIG.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**

