# 📋 INSTRUCCIONES MANUALES - Arquitectura Hikvision

## 🎯 **OBJETIVO**
Configurar completamente el sistema con la nueva arquitectura Hikvision, donde los NUCs se conectan al servidor central mediante WebSocket.

---

## 📦 **PARTE 1: INSTALAR DEPENDENCIAS EN EL NUC**

### **Paso 1.1: Verificar Python**
```powershell
python --version
```
**Debe mostrar:** Python 3.x

### **Paso 1.2: Instalar dependencias del NUC**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
pip install websocket-client>=1.6.0 python-socketio>=5.10.0 opencv-python-headless numpy
```

**Verificar instalación:**
```powershell
python -c "import websocket; print('✅ websocket-client OK')"
python -c "import socketio; print('✅ socketio OK')"
python -c "import cv2; print('✅ opencv OK')"
```

---

## ⚙️ **PARTE 2: CONFIGURAR `config.py`**

### **Paso 2.1: Abrir el archivo de configuración**
```powershell
notepad C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend\config.py
```

### **Paso 2.2: Configurar NUCs**
Busca la sección `NUCs_CONFIG` y configura tus NUCs:

```python
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.92.50.72',  # Solo para referencia (no se usa en nueva arquitectura)
        'puerto': 5000,
        'nombre': 'NUC Principal',
        'red_local': '192.168.60',
        'server_url': 'https://apptelink-vision-production.up.railway.app'  # ⚠️ IMPORTANTE: URL de tu Railway
    },
    # Agrega más NUCs si tienes:
    # 'nuc_sede2': {
    #     'tailscale_ip': '100.92.50.73',
    #     'puerto': 5000,
    #     'nombre': 'NUC Sede 2',
    #     'red_local': '192.168.61',
    #     'server_url': 'https://apptelink-vision-production.up.railway.app'
    # },
}
```

### **Paso 2.3: Configurar Cámaras**
Busca la sección `CAMARAS_CONFIG` y configura tus cámaras:

```python
CAMARAS_CONFIG = [
    {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},
    {'ip': '192.168.60.66', 'nombre': 'Cámara Entrada', 'nuc': 'nuc_sede1'},
    # Agrega más cámaras:
    # {'ip': '192.168.60.67', 'nombre': 'Cámara Patio', 'nuc': 'nuc_sede1'},
]
```

### **Paso 2.4: Configurar Credenciales de Cámaras**
Busca estas líneas y ajusta según tus cámaras:

```python
USUARIO_CAMARAS = 'admin'  # ⚠️ Cambia si es diferente
CONTRASENA_CAMARAS = 'citikold.2020'  # ⚠️ Cambia si es diferente
```

### **Paso 2.5: Configurar NUC_ID**
Si tienes **múltiples NUCs**, cada NUC debe tener su propio `NUC_ID`:

```python
NUC_ID = 'nuc_sede1'  # ⚠️ Cambia según el NUC (nuc_sede1, nuc_sede2, etc.)
```

**Si solo tienes UN NUC**, déjalo como está.

### **Paso 2.6: Guardar y cerrar**
- Guarda el archivo (Ctrl+S)
- Cierra el editor

---

## 🧪 **PARTE 3: PROBAR LA CONEXIÓN DE LA CÁMARA**

### **Paso 3.1: Verificar que la cámara responde**
```powershell
ping 192.168.60.65
```
**Debe mostrar:** Respuestas exitosas (time < 10ms)

### **Paso 3.2: Probar URL RTSP con VLC (OPCIONAL pero recomendado)**

1. Abre **VLC Media Player**
2. Ve a: **Media → Open Network Stream** (Ctrl+N)
3. Ingresa la URL:
   ```
   rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/101
   ```
4. Haz clic en **Play**
5. **Si funciona:** La cámara está bien configurada ✅
6. **Si NO funciona:** Revisa credenciales o IP en `config.py`

---

## 🚀 **PARTE 4: CONFIGURAR RAILWAY (Backend)**

### **Paso 4.1: Acceder a Railway**
1. Ve a: https://railway.app
2. Inicia sesión
3. Selecciona tu proyecto: **apptelink-vision**

### **Paso 4.2: Cambiar Dockerfile**
1. Ve a la pestaña **Settings** de tu servicio backend
2. Busca **"Dockerfile Path"** o **"Build Command"**
3. Cambia de:
   - `Dockerfile` (antiguo)
   - A: `Dockerfile.hikvision` (nuevo)
4. Guarda los cambios

### **Paso 4.3: Agregar Redis (OPCIONAL pero recomendado)**
1. En Railway, haz clic en **"+ New"**
2. Selecciona **"Database" → "Add Redis"**
3. Railway creará automáticamente una variable `REDIS_URL`
4. El backend la detectará automáticamente

**Si NO agregas Redis:**
- El sistema funcionará, pero los snapshots se perderán al reiniciar
- No es crítico para pruebas

### **Paso 4.4: Eliminar Variables de Entorno Antiguas (OPCIONAL)**
Si tienes estas variables, puedes eliminarlas (ya no se usan):
- `TAILSCALE_AUTHKEY`
- `NUC_URLS`
- `CAMARAS_IPS`

**NO elimines:**
- `PORT` (si existe)
- `REDIS_URL` (si agregaste Redis)

### **Paso 4.5: Desplegar Cambios**
1. Ve a la pestaña **"Deployments"**
2. Haz clic en **"Redeploy"** o espera a que Railway detecte los cambios de GitHub
3. Espera a que termine el despliegue (2-5 minutos)

### **Paso 4.6: Verificar que el Backend está funcionando**
1. Ve a la pestaña **"Logs"**
2. Debes ver algo como:
   ```
   Starting Container
   📋 Usando archivo de configuración: config.py
   ✅ Servidor SocketIO iniciado en modo: eventlet
   * Running on all addresses (0.0.0.0)
   ```

---

## 🖥️ **PARTE 5: CONFIGURAR EL NUC AGENT**

### **Paso 5.1: Verificar que `config.py` está correcto**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
notepad backend\config.py
```
- Verifica que `NUC_ID` corresponde a este NUC
- Verifica que `server_url` es la URL correcta de Railway
- Verifica que las cámaras tienen `'nuc': 'nuc_sede1'` (o el ID correcto)

### **Paso 5.2: Probar el NUC Agent manualmente**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\ejecutar_nuc_agent_hikvision.bat
```

**Debes ver:**
```
✅ Conectado al servidor central: https://apptelink-vision-production.up.railway.app
✅ Servidor confirmó conexión: {'status': 'ok', 'nuc_id': 'nuc_sede1', ...}
📸 Capturando snapshot de 192.168.60.65...
✅ Snapshot capturado: 192.168.60.65 (12345 bytes)
```

**Si ves errores:**
- `websocket-client package not installed` → Ejecuta: `pip install websocket-client`
- `No se pudo abrir la cámara` → Revisa credenciales/IP en `config.py`
- `Connection refused` → Verifica que Railway está desplegado y la URL es correcta

### **Paso 5.3: Detener el NUC Agent (si está corriendo)**
Presiona **Ctrl+C** en la ventana donde está corriendo

---

## 🔄 **PARTE 6: CONFIGURAR INICIO AUTOMÁTICO DEL NUC AGENT**

### **Paso 6.1: Ejecutar el script de configuración**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\configurar_nuc_agent_automatico.bat
```

**Este script:**
- Crea una Tarea Programada de Windows
- Configura el NUC Agent para iniciar automáticamente al arrancar Windows
- Ejecuta en segundo plano sin mostrar ventanas

### **Paso 6.2: Verificar que la tarea se creó**
1. Presiona **Win + R**
2. Escribe: `taskschd.msc` y presiona Enter
3. Ve a: **Task Scheduler Library**
4. Busca: **"NUC Agent Hikvision - Auto Start"**
5. Debe aparecer con estado **"Ready"**

### **Paso 6.3: Probar la tarea manualmente**
1. En Task Scheduler, haz clic derecho en **"NUC Agent Hikvision - Auto Start"**
2. Selecciona **"Run"**
3. Espera 10 segundos
4. Verifica que el NUC Agent está corriendo:
   ```powershell
   netstat -ano | findstr ":5000"
   ```
   O verifica en los logs de Railway que está recibiendo snapshots

---

## ✅ **PARTE 7: VERIFICAR QUE TODO FUNCIONA**

### **Paso 7.1: Verificar NUC Agent está corriendo**
```powershell
tasklist | findstr python
```
Debe mostrar procesos de Python corriendo

### **Paso 7.2: Verificar conexión WebSocket**
1. Ve a Railway → Logs
2. Debes ver mensajes como:
   ```
   ✅ NUC conectado: nuc_sede1
   📸 Snapshot recibido de 192.168.60.65
   ```

### **Paso 7.3: Verificar Frontend**
1. Abre tu aplicación web en Railway
2. Debe mostrar las cámaras detectadas
3. Al hacer clic en una cámara, debe mostrar la imagen

**Si no muestra imágenes:**
- Verifica que el NUC Agent está enviando snapshots (revisa Railway logs)
- Verifica que las credenciales de la cámara son correctas
- Espera 30-60 segundos (el agente captura cada 30 segundos)

---

## 🔧 **PARTE 8: SOLUCIÓN DE PROBLEMAS**

### **Problema: "websocket-client package not installed"**
**Solución:**
```powershell
pip install websocket-client>=1.6.0
```

### **Problema: "No se pudo abrir la cámara"**
**Solución:**
1. Verifica IP: `ping 192.168.60.65`
2. Verifica credenciales en `config.py`
3. Prueba URL RTSP en VLC

### **Problema: "Connection refused" o "Timeout"**
**Solución:**
1. Verifica que Railway está desplegado (revisa logs)
2. Verifica que `server_url` en `config.py` es correcta
3. Verifica que el backend está usando `Dockerfile.hikvision`

### **Problema: "Cámaras no aparecen en el frontend"**
**Solución:**
1. Verifica que el NUC Agent está corriendo
2. Verifica que está enviando snapshots (Railway logs)
3. Espera 30-60 segundos
4. Refresca la página del frontend

### **Problema: "NUC Agent no inicia automáticamente"**
**Solución:**
1. Verifica que la tarea programada existe: `taskschd.msc`
2. Verifica que está habilitada (Enabled = Yes)
3. Ejecuta manualmente la tarea para ver errores

---

## 📝 **CHECKLIST FINAL**

Antes de considerar que todo está listo, verifica:

- [ ] Dependencias instaladas en el NUC (`websocket-client`, `socketio`, `opencv`)
- [ ] `config.py` configurado con NUCs y cámaras correctas
- [ ] Credenciales de cámaras correctas en `config.py`
- [ ] Railway configurado con `Dockerfile.hikvision`
- [ ] Redis agregado en Railway (opcional)
- [ ] Backend desplegado y funcionando (verificar logs)
- [ ] NUC Agent probado manualmente y funcionando
- [ ] Tarea programada creada para inicio automático
- [ ] Frontend muestra cámaras y snapshots

---

## 🆘 **SOPORTE**

Si algo no funciona:
1. Revisa los logs de Railway
2. Revisa los logs del NUC Agent (si lo ejecutas manualmente)
3. Verifica que todos los pasos anteriores están completos
4. Revisa `RESUMEN_EJECUCION.md` para más detalles

---

**¡Listo! Sigue estos pasos en orden y todo debería funcionar correctamente.** 🎉
