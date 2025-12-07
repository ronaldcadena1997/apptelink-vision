# 🚀 Pasos para Configurar Tailscale en Railway

## ✅ Paso 1: Generar Auth Key (Ya estás aquí)

**En la pantalla de Tailscale:**

1. **Haz clic en "Generate key"** (botón azul abajo a la derecha)
2. **Se mostrará la auth key** (algo como: `tskey-auth-xxxxx-xxxxx`)
3. **⚠️ COPIA LA AUTH KEY INMEDIATAMENTE** - Solo se muestra una vez
4. **Guárdala en un lugar seguro** (la necesitarás en Railway)

---

## 🔄 Paso 2: Renombrar Dockerfile

**En PowerShell, ejecuta:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend

# Renombrar Dockerfile actual
ren Dockerfile Dockerfile.original

# Renombrar Dockerfile con Tailscale
ren Dockerfile.tailscale Dockerfile
```

**Verificar que funcionó:**

```powershell
# Debe mostrar Dockerfile (no Dockerfile.tailscale)
dir Dockerfile*
```

---

## 📤 Paso 3: Hacer Push de los Cambios

**Agregar todos los archivos nuevos:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision

# Agregar archivos
git add backend/Dockerfile backend/Dockerfile.original backend/start_with_tailscale.sh backend/CONFIGURAR_TAILSCALE_RAILWAY.md

# Commit
git commit -m "Agregar soporte para Tailscale en Railway"

# Push
git push
```

---

## 🔧 Paso 4: Configurar Variable en Railway

**Después de hacer push:**

1. **Ve a Railway Dashboard:**
   - https://railway.app
   - Selecciona tu proyecto de **backend**

2. **Abre la pestaña "Variables"**

3. **Haz clic en "New Variable"**

4. **Agrega:**
   - **Name:** `TAILSCALE_AUTHKEY`
   - **Value:** La auth key que copiaste en el Paso 1
   - **Ejemplo:** `tskey-auth-xxxxx-xxxxx`

5. **Haz clic en "Add"**

6. **Railway se redesplegará automáticamente** (puede tardar unos minutos)

---

## ✅ Paso 5: Verificar que Funciona

### **5.1. Verificar en Railway Logs**

**En Railway Dashboard → Logs, busca:**

```
==========================================
Iniciando Tailscale en Railway
==========================================
[1/3] Iniciando Tailscale daemon...
[2/3] Conectando a Tailscale con authkey...
[3/3] Verificando conexión de Tailscale...
✅ Tailscale conectado. IP: 100.xx.xx.xx
==========================================
Iniciando servidor Python
==========================================
```

**Si ves esto:** ✅ Tailscale está funcionando

**Si ves errores:**
- `ERROR: TAILSCALE_AUTHKEY no está configurada` → Verifica la variable en Railway
- `tailscaled: command not found` → Verifica que el Dockerfile correcto esté en uso

---

### **5.2. Verificar en Tailscale Admin Console**

1. **Ve a:** https://login.tailscale.com/admin/machines
2. **Busca una máquina nueva** con nombre como:
   - `railway-xxxxx`
   - O el nombre de tu proyecto en Railway
3. **Verifica que esté "Online"** (punto verde)

---

### **5.3. Probar desde el Frontend**

1. **Abre:** https://impartial-wisdom-production-3c22.up.railway.app
2. **Verifica que las cámaras muestren imágenes** (no "sin_acceso")

---

## 📋 Resumen de Comandos

**Ejecuta estos comandos en orden:**

```powershell
# 1. Ir a la carpeta backend
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend

# 2. Renombrar Dockerfiles
ren Dockerfile Dockerfile.original
ren Dockerfile.tailscale Dockerfile

# 3. Volver a la raíz del proyecto
cd ..

# 4. Agregar cambios
git add backend/Dockerfile backend/Dockerfile.original backend/start_with_tailscale.sh

# 5. Commit
git commit -m "Agregar soporte para Tailscale en Railway"

# 6. Push
git push
```

**Luego:**
- Ve a Railway Dashboard
- Agrega la variable `TAILSCALE_AUTHKEY` con la auth key que copiaste
- Espera a que Railway se redesplegue

---

## 🎯 Siguiente Acción

**Ahora mismo:**

1. ✅ **Haz clic en "Generate key"** en Tailscale
2. ✅ **Copia la auth key** inmediatamente
3. ✅ **Ejecuta los comandos de renombrar Dockerfile** (arriba)
4. ✅ **Haz push de los cambios**
5. ✅ **Agrega la variable en Railway**

**¿Listo para continuar?** 🚀
