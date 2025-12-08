# ✅ Resumen de Verificación del Sistema

## 📋 **Estado Actual del Sistema**

### **1. Procesos de Python**
```powershell
tasklist | findstr python
```
**Resultado:** Verificar manualmente si hay procesos de Python corriendo.

**Si NO hay procesos:**
- El NUC Agent no está ejecutándose
- **Solución:** Ejecuta `.\ejecutar_nuc_agent_hikvision.bat`

---

### **2. Dependencias Instaladas**

#### **websocket-client**
```powershell
python -c "import websocket; print('✅ websocket-client OK')"
```
**Si falla:**
```powershell
pip install websocket-client>=1.6.0
```

#### **socketio**
```powershell
python -c "import socketio; print('✅ socketio OK')"
```
**Si falla:**
```powershell
pip install python-socketio>=5.10.0
```

#### **opencv**
```powershell
python -c "import cv2; print('✅ opencv OK')"
```
**Si falla:**
```powershell
pip install opencv-python-headless
```

---

### **3. Conectividad de la Cámara**

```powershell
ping 192.168.60.65
```

**Si el ping falla:**
- La cámara no está en la red
- La IP es incorrecta
- Hay problemas de red

**Solución:** Verifica la IP de la cámara en `backend/config.py`

---

### **4. Configuración en `config.py`**

Verifica que estos valores estén correctos:

```python
# NUCs_CONFIG
NUCs_CONFIG = {
    'nuc_sede1': {
        'server_url': 'https://apptelink-vision-production.up.railway.app'  # ✅ Verificar
    }
}

# CAMARAS_CONFIG
CAMARAS_CONFIG = [
    {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},  # ✅ Verificar
]

# Credenciales
USUARIO_CAMARAS = 'admin'  # ✅ Verificar
CONTRASENA_CAMARAS = 'citikold.2020'  # ✅ Verificar
```

---

## 🚀 **Pasos para Iniciar el NUC Agent**

### **Opción 1: Ejecutar Manualmente (Para Pruebas)**

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

---

### **Opción 2: Configurar Inicio Automático**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\configurar_nuc_agent_automatico.bat
```

Esto creará una tarea programada para que el NUC Agent inicie automáticamente.

---

## 🔍 **Verificar en Railway (Servidor)**

1. Ve a: https://railway.app
2. Selecciona tu proyecto
3. Ve a la pestaña **"Logs"**
4. Busca mensajes como:
   ```
   ✅ NUC conectado: nuc_sede1
   📸 Snapshot recibido: nuc_sede1 - 192.168.60.65
   ```

**Si NO ves estos mensajes:**
- El NUC Agent no se ha conectado
- Verifica que el NUC Agent esté corriendo
- Verifica que `server_url` en `config.py` sea correcta

---

## ✅ **Checklist Completo**

Antes de considerar que todo está funcionando:

- [ ] **NUC Agent está corriendo** (`tasklist | findstr python`)
- [ ] **Dependencias instaladas** (websocket-client, socketio, opencv)
- [ ] **Cámara accesible** (`ping 192.168.60.65`)
- [ ] **Config.py correcto** (server_url, cámaras, credenciales)
- [ ] **NUC Agent se conecta** (ver logs del NUC Agent)
- [ ] **Servidor recibe datos** (ver logs de Railway)
- [ ] **Frontend muestra cámaras** (refrescar después de 30-60 segundos)

---

## 🆘 **Si Algo No Funciona**

### **Problema: NUC Agent no inicia**
1. Verifica dependencias: `.\instalar_dependencias_nuc.bat`
2. Verifica Python: `python --version`
3. Ejecuta manualmente para ver errores: `python backend\nuc_agent_hikvision.py`

### **Problema: No se conecta al servidor**
1. Verifica `server_url` en `config.py`
2. Verifica que Railway está desplegado
3. Verifica conectividad a internet desde el NUC

### **Problema: No captura snapshots**
1. Verifica IP de la cámara: `ping 192.168.60.65`
2. Verifica credenciales en `config.py`
3. Prueba URL RTSP en VLC

---

## 📞 **Próximos Pasos**

1. **Ejecuta el NUC Agent:** `.\ejecutar_nuc_agent_hikvision.bat`
2. **Observa los logs** para ver si hay errores
3. **Verifica en Railway** que recibe los snapshots
4. **Espera 30-60 segundos** (el agente captura cada 30 segundos)
5. **Refresca el frontend** para ver las imágenes

---

**¡Con esta verificación deberías poder identificar y resolver cualquier problema!** 🎯
