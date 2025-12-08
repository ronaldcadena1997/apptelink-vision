# 🔍 Diagnóstico: Cámaras con "Sin Acceso"

## ✅ **Estado Actual**
- ✅ Backend funcionando correctamente
- ✅ Endpoints `/api/camaras` y `/api/camaras/detectar` responden sin error 500
- ❌ Cámaras aparecen como "sin acceso"

## 🔍 **Causa Probable**
El NUC Agent no está corriendo o no se ha conectado al servidor, por lo que no hay snapshots en Redis.

---

## 📋 **PASO 1: Verificar que el NUC Agent está corriendo**

### **En el NUC (Windows):**

```powershell
# Verificar procesos de Python
tasklist | findstr python

# Verificar si hay algo escuchando en puertos relacionados
netstat -ano | findstr python
```

**Si NO hay procesos de Python corriendo:**
→ El NUC Agent no está ejecutándose

**Solución:**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\ejecutar_nuc_agent_hikvision.bat
```

---

## 📋 **PASO 2: Verificar conexión al servidor**

### **En el NUC, ejecuta el NUC Agent manualmente:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
python nuc_agent_hikvision.py
```

**Debes ver:**
```
✅ Conectado al servidor central: https://apptelink-vision-production.up.railway.app
✅ Servidor confirmó conexión: {'status': 'ok', 'nuc_id': 'nuc_sede1', ...}
📸 Capturando snapshot de 192.168.60.65...
✅ Snapshot capturado: 192.168.60.65 (12345 bytes)
```

**Si ves errores:**
- `Connection refused` → El servidor no está accesible o la URL es incorrecta
- `websocket-client package not installed` → Ejecuta: `pip install websocket-client`
- `No se pudo abrir la cámara` → Revisa credenciales/IP en `config.py`

---

## 📋 **PASO 3: Verificar configuración en `config.py`**

### **Abre y verifica:**

```powershell
notepad C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend\config.py
```

**Verifica estas secciones:**

1. **`NUCs_CONFIG`** - Debe tener tu NUC:
   ```python
   NUCs_CONFIG = {
       'nuc_sede1': {
           'server_url': 'https://apptelink-vision-production.up.railway.app'  # ✅ Correcto
       }
   }
   ```

2. **`CAMARAS_CONFIG`** - Debe tener tus cámaras:
   ```python
   CAMARAS_CONFIG = [
       {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},  # ✅ Correcto
   ]
   ```

3. **Credenciales de cámaras:**
   ```python
   USUARIO_CAMARAS = 'admin'  # ✅ Verifica que sea correcto
   CONTRASENA_CAMARAS = 'citikold.2020'  # ✅ Verifica que sea correcto
   ```

---

## 📋 **PASO 4: Verificar logs del servidor (Railway)**

1. Ve a Railway: https://railway.app
2. Selecciona tu proyecto
3. Ve a la pestaña **"Logs"**
4. Busca mensajes como:
   ```
   ✅ NUC conectado: nuc_sede1
   📸 Snapshot recibido: nuc_sede1 - 192.168.60.65
   ```

**Si NO ves estos mensajes:**
→ El NUC Agent no se ha conectado al servidor

---

## 📋 **PASO 5: Verificar que las cámaras son accesibles**

### **En el NUC:**

```powershell
# Verificar que la cámara responde
ping 192.168.60.65

# Probar URL RTSP con VLC (opcional pero recomendado)
# Abre VLC → Media → Open Network Stream
# URL: rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/101
```

**Si el ping falla:**
→ La cámara no está en la red o la IP es incorrecta

**Si VLC no puede conectarse:**
→ Las credenciales o la URL RTSP son incorrectas

---

## 🔧 **SOLUCIONES PASO A PASO**

### **Solución 1: Iniciar el NUC Agent manualmente**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\ejecutar_nuc_agent_hikvision.bat
```

**Deja esta ventana abierta** y observa los logs. Debes ver:
- ✅ Conexión al servidor
- ✅ Snapshots siendo capturados y enviados

---

### **Solución 2: Configurar inicio automático**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\configurar_nuc_agent_automatico.bat
```

Esto creará una tarea programada para que el NUC Agent inicie automáticamente al arrancar Windows.

---

### **Solución 3: Verificar dependencias**

```powershell
# Instalar dependencias si faltan
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\instalar_dependencias_nuc.bat

# Verificar instalación
python -c "import websocket; print('✅ websocket-client OK')"
python -c "import socketio; print('✅ socketio OK')"
python -c "import cv2; print('✅ opencv OK')"
```

---

### **Solución 4: Corregir credenciales/IPs**

Si las credenciales o IPs son incorrectas:

1. Edita `backend/config.py`:
   ```powershell
   notepad C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend\config.py
   ```

2. Corrige:
   - `USUARIO_CAMARAS`
   - `CONTRASENA_CAMARAS`
   - IPs en `CAMARAS_CONFIG`

3. Reinicia el NUC Agent

---

## ✅ **CHECKLIST DE VERIFICACIÓN**

Antes de reportar problemas, verifica:

- [ ] NUC Agent está corriendo (`tasklist | findstr python`)
- [ ] NUC Agent se conecta al servidor (ver logs del NUC Agent)
- [ ] Servidor recibe conexiones (ver logs de Railway)
- [ ] Cámaras son accesibles (`ping 192.168.60.65`)
- [ ] Credenciales son correctas (probar en VLC)
- [ ] `config.py` está correctamente configurado
- [ ] Dependencias están instaladas (`websocket-client`, `socketio`, `opencv`)

---

## 🆘 **ERRORES COMUNES Y SOLUCIONES**

### **Error: "websocket-client package not installed"**
```powershell
pip install websocket-client>=1.6.0
```

### **Error: "No se pudo abrir la cámara"**
1. Verifica IP: `ping 192.168.60.65`
2. Verifica credenciales en `config.py`
3. Prueba URL RTSP en VLC

### **Error: "Connection refused"**
1. Verifica que Railway está desplegado
2. Verifica que `server_url` en `config.py` es correcta
3. Verifica que el backend está usando `Dockerfile.hikvision`

### **Error: "NUC Agent se conecta pero no envía snapshots"**
1. Verifica que `CAMARAS_IPS` tiene las IPs correctas
2. Verifica que las cámaras tienen `'nuc': 'nuc_sede1'` en `CAMARAS_CONFIG`
3. Verifica que `NUC_ID` coincide con el NUC configurado

---

## 📞 **SIGUIENTE PASO**

Después de verificar todo lo anterior:

1. **Ejecuta el NUC Agent manualmente** para ver los logs en tiempo real
2. **Observa los logs de Railway** para ver si recibe los snapshots
3. **Espera 30-60 segundos** (el agente captura cada 30 segundos)
4. **Refresca el frontend** para ver las imágenes

---

**¡Con estos pasos deberías poder resolver el problema de "sin acceso"!** 🎯
