# ✅ Checklist: Pasos Pendientes para Implementar Arquitectura Hikvision

## 📋 **Resumen de lo que falta**

---

## ✅ **PASO 1: Subir Cambios a GitHub**

### **Opción A: Usar el Script**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\subir_hikvision_simple.bat
```

### **Opción B: Comandos Manuales**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision

git add backend/server_hikvision_style.py
git add backend/nuc_agent_hikvision.py
git add backend/config.py
git add backend/requirements.txt
git add backend/Dockerfile.hikvision
git add ejecutar_nuc_agent_hikvision.bat
git add configurar_nuc_agent_automatico.bat
git add *.md

git commit -m "Implementar arquitectura estilo Hikvision - Usa config.py"

git push
```

**✅ Verificar:** Ve a GitHub y confirma que los cambios se subieron.

---

## ✅ **PASO 2: Configurar Backend en Railway**

### **2.1. Cambiar Dockerfile**

1. Ve a Railway → Tu proyecto → Backend Service
2. Click en **"Settings"**
3. Busca **"Dockerfile Path"** o **"Build Command"**
4. Cambia a: `Dockerfile.hikvision`
   - O renombra `Dockerfile.hikvision` a `Dockerfile` en GitHub

### **2.2. Agregar Redis (Recomendado)**

1. En Railway → Tu proyecto
2. Click en **"+ New"** → **"Database"** → **"Add Redis"**
3. Railway creará automáticamente la variable `REDIS_URL`
4. El backend la detectará automáticamente

**⚠️ Nota:** Si no agregas Redis, el sistema usará memoria (se perderá al reiniciar).

### **2.3. Eliminar Variables Antiguas (Opcional)**

Ya no necesitas estas variables:
- ❌ `TAILSCALE_AUTHKEY` (puedes eliminarla)
- ❌ `NUC_URLS` (puedes eliminarla)
- ❌ `NUC_URL` (puedes eliminarla)

**✅ Verificar:** Ve a Railway → Logs y deberías ver:
```
✅ Servidor listo para recibir conexiones de NUCs
```

---

## ✅ **PASO 3: Configurar config.py con tus NUCs y Cámaras**

### **3.1. Editar config.py**

Abre `backend/config.py` y edita:

```python
# CONFIGURACIÓN DE NUCS
NUCs_CONFIG = {
    'nuc_sede1': {
        'nombre': 'NUC Principal',
        'red_local': '192.168.60',  # Tu red local
        'server_url': 'https://apptelink-vision-production.up.railway.app'
    },
    # Agrega más NUCs aquí si tienes:
    # 'nuc_sede2': {
    #     'nombre': 'NUC Sede 2',
    #     'red_local': '192.168.61',
    #     'server_url': 'https://apptelink-vision-production.up.railway.app'
    # },
}

# CONFIGURACIÓN DE CÁMARAS
CAMARAS_CONFIG = [
    # Cámaras del NUC Principal
    {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},
    # Agrega más cámaras aquí:
    # {'ip': '192.168.60.66', 'nombre': 'Cámara 2', 'nuc': 'nuc_sede1'},
]
```

### **3.2. Subir config.py actualizado**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
git add backend/config.py
git commit -m "Actualizar config.py con NUCs y camaras reales"
git push
```

**✅ Verificar:** Confirma que `config.py` tiene tus NUCs y cámaras correctas.

---

## ✅ **PASO 4: Configurar NUC Agent en Cada NUC**

### **4.1. Instalar Dependencias**

En cada NUC, ejecuta:

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
pip install python-socketio opencv-python-headless
```

### **4.2. Configurar NUC_ID (Solo si tienes múltiples NUCs)**

Si tienes múltiples NUCs, en cada uno configura cuál es:

```powershell
# En el NUC Principal (nuc_sede1)
[System.Environment]::SetEnvironmentVariable('NUC_ID', 'nuc_sede1', 'User')

# En el NUC Sede 2 (nuc_sede2)
[System.Environment]::SetEnvironmentVariable('NUC_ID', 'nuc_sede2', 'User')
```

**Si solo tienes un NUC:** No necesitas hacer nada, usará el primero de `config.py`.

### **4.3. Probar el NUC Agent**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\ejecutar_nuc_agent_hikvision.bat
```

**Deberías ver:**
```
✅ Conectado al servidor central: https://...
✅ Servidor confirmó conexión
📸 Capturando snapshot de 192.168.60.65...
✅ Snapshot enviado: 192.168.60.65
```

### **4.4. Configurar Inicio Automático**

```powershell
.\configurar_nuc_agent_automatico.bat
```

Esto configurará el NUC Agent para ejecutarse automáticamente al iniciar Windows.

**✅ Verificar:** Reinicia el NUC y verifica que el agente se ejecuta automáticamente.

---

## ✅ **PASO 5: Verificar que Todo Funciona**

### **5.1. Verificar Backend en Railway**

1. Ve a Railway → Logs del backend
2. Deberías ver:
   ```
   ✅ NUC conectado: nuc_sede1
   📸 Snapshot recibido: nuc_sede1 - 192.168.60.65
   ```

### **5.2. Verificar Frontend**

1. Abre el frontend en el navegador
2. Las cámaras deberían aparecer automáticamente
3. Los snapshots se actualizan cada 30 segundos

### **5.3. Verificar NUC Agent**

En cada NUC, verifica que el agente esté corriendo:
```powershell
tasklist | findstr python
```

---

## 📊 **Resumen de Checklist**

- [ ] **PASO 1:** Subir cambios a GitHub
- [ ] **PASO 2.1:** Cambiar Dockerfile en Railway a `Dockerfile.hikvision`
- [ ] **PASO 2.2:** Agregar Redis en Railway (opcional pero recomendado)
- [ ] **PASO 2.3:** Eliminar variables antiguas (opcional)
- [ ] **PASO 3.1:** Editar `config.py` con tus NUCs y cámaras
- [ ] **PASO 3.2:** Subir `config.py` actualizado
- [ ] **PASO 4.1:** Instalar dependencias en cada NUC
- [ ] **PASO 4.2:** Configurar NUC_ID en cada NUC (solo si múltiples)
- [ ] **PASO 4.3:** Probar NUC Agent
- [ ] **PASO 4.4:** Configurar inicio automático del NUC Agent
- [ ] **PASO 5.1:** Verificar backend en Railway
- [ ] **PASO 5.2:** Verificar frontend
- [ ] **PASO 5.3:** Verificar NUC Agent en cada NUC

---

## 🎯 **Orden Recomendado**

1. **Primero:** Subir cambios a GitHub (PASO 1)
2. **Segundo:** Configurar Railway (PASO 2)
3. **Tercero:** Configurar config.py (PASO 3)
4. **Cuarto:** Configurar NUCs (PASO 4)
5. **Quinto:** Verificar todo (PASO 5)

---

## 🆘 **Si Algo No Funciona**

### **El backend no inicia:**
- Verifica que `Dockerfile.hikvision` esté configurado
- Verifica los logs de Railway para ver el error

### **El NUC Agent no se conecta:**
- Verifica que `SERVER_URL` sea correcta en `config.py`
- Verifica que el backend esté desplegado y funcionando
- Verifica la conexión a internet del NUC

### **Las cámaras no aparecen:**
- Verifica que `config.py` tenga las cámaras correctas
- Verifica que el NUC Agent esté enviando snapshots
- Verifica los logs del backend en Railway

---

**¿Necesitas ayuda con algún paso específico?** Dime cuál y te ayudo.
