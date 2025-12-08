# 🔧 Solución: Timeout al Conectar con la Cámara

## ❌ **Problema Actual**
```
[ WARN:0@30.020] global cap_ffmpeg_impl.hpp:453 _opencv_ffmpeg_interrupt_callback Stream timeout triggered after 30019.093000 ms
```

El NUC Agent se conecta al servidor correctamente, pero **no puede conectarse a la cámara**.

---

## 🔍 **Causas Posibles**

1. **IP incorrecta** - La cámara no está en `192.168.60.65`
2. **Credenciales incorrectas** - Usuario/contraseña no son correctos
3. **URL RTSP incorrecta** - La cámara usa una URL RTSP diferente
4. **Cámara no accesible** - La cámara está apagada o no está en la red
5. **Firewall bloqueando** - El firewall está bloqueando el puerto 554

---

## ✅ **Soluciones Paso a Paso**

### **PASO 1: Verificar que la cámara responde**

```powershell
ping 192.168.60.65
```

**Si el ping falla:**
- La cámara no está en la red
- La IP es incorrecta
- La cámara está apagada

**Solución:** Verifica la IP correcta de la cámara.

---

### **PASO 2: Verificar credenciales**

Abre `backend/config.py` y verifica:

```python
USUARIO_CAMARAS = 'admin'  # ⚠️ ¿Es correcto?
CONTRASENA_CAMARAS = 'citikold.2020'  # ⚠️ ¿Es correcto?
```

**Solución:** 
1. Verifica las credenciales en la interfaz web de la cámara
2. Actualiza `config.py` con las credenciales correctas
3. Reinicia el NUC Agent

---

### **PASO 3: Probar URL RTSP con VLC (RECOMENDADO)**

1. Abre **VLC Media Player**
2. Ve a: **Media → Open Network Stream** (Ctrl+N)
3. Prueba estas URLs una por una:

   ```
   rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/101
   rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/1
   rtsp://admin:citikold.2020@192.168.60.65:554/h264/ch1/main/av_stream
   ```

4. **Si alguna funciona en VLC:**
   - Esa es la URL RTSP correcta
   - El problema puede ser con OpenCV o las credenciales

5. **Si ninguna funciona en VLC:**
   - Las credenciales son incorrectas
   - O la URL RTSP es diferente
   - Consulta el manual de la cámara para la URL RTSP correcta

---

### **PASO 4: Verificar en la interfaz web de la cámara**

1. Abre el navegador
2. Ve a: `http://192.168.60.65` (o la IP de tu cámara)
3. Inicia sesión con las credenciales
4. Busca la sección de **"RTSP"** o **"Streaming"**
5. Verifica:
   - La URL RTSP correcta
   - El puerto (generalmente 554)
   - Las credenciales

---

### **PASO 5: Verificar firewall**

```powershell
# Verificar si el puerto 554 está bloqueado
netstat -ano | findstr :554
```

Si el firewall está bloqueando, agrega una excepción para el puerto 554.

---

## 🔧 **Correcciones Implementadas**

He mejorado el código del NUC Agent para:

1. ✅ **Intentar más URLs RTSP** (5 diferentes en lugar de 3)
2. ✅ **Mostrar mensajes de error más claros** con información sobre qué se intentó
3. ✅ **Mejor manejo de errores** para identificar el problema específico

---

## 📋 **Próximos Pasos**

1. **Verifica la IP de la cámara:**
   ```powershell
   ping 192.168.60.65
   ```

2. **Prueba la URL RTSP en VLC:**
   - Abre VLC
   - Media → Open Network Stream
   - Prueba las URLs mencionadas arriba

3. **Si VLC funciona pero el NUC Agent no:**
   - Verifica que las credenciales en `config.py` sean exactamente las mismas
   - Reinicia el NUC Agent

4. **Si VLC tampoco funciona:**
   - Las credenciales o la IP son incorrectas
   - Verifica en la interfaz web de la cámara

---

## 🆘 **Si Nada Funciona**

1. **Verifica el modelo de la cámara:**
   - Diferentes marcas usan URLs RTSP diferentes
   - Consulta el manual de la cámara

2. **Verifica la configuración de red:**
   - La cámara debe estar en la misma red que el NUC
   - Verifica que no haya VLANs o subredes separadas

3. **Contacta al soporte de la cámara:**
   - Pregunta por la URL RTSP correcta
   - Pregunta por las credenciales por defecto si las cambiaste

---

## ✅ **Después de Corregir**

1. **Actualiza `config.py`** con las credenciales/IP correctas
2. **Reinicia el NUC Agent:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
   .\ejecutar_nuc_agent_hikvision.bat
   ```
3. **Debes ver:**
   ```
   ✅ Snapshot capturado y enviado: 192.168.60.65 (12345 bytes)
   ```
   En lugar de:
   ```
   ❌ Error al capturar 192.168.60.65: ...
   ```

---

**¡Con estos pasos deberías poder resolver el problema de timeout!** 🎯
