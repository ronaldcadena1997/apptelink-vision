# 🚨 URGENTE: Verificar Configuración de la Cámara

## ❌ **Problema Crítico**
La cámara en `192.168.60.65` **NO está respondiendo** a ninguna conexión RTSP. El NUC Agent intenta conectarse cada 30 segundos pero siempre falla con timeout.

---

## 🔍 **VERIFICACIÓN INMEDIATA**

### **1. Verificar que la cámara responde**

```powershell
ping 192.168.60.65
```

**Si el ping falla:**
- ❌ La IP es incorrecta
- ❌ La cámara está apagada
- ❌ La cámara no está en la red

**Solución:** Verifica la IP correcta de la cámara.

---

### **2. Verificar credenciales**

Abre `backend/config.py` y verifica:

```python
USUARIO_CAMARAS = 'admin'  # ⚠️ ¿Es correcto?
CONTRASENA_CAMARAS = 'citikold.2020'  # ⚠️ ¿Es correcto?
```

**Solución:**
1. Accede a la interfaz web de la cámara: `http://192.168.60.65`
2. Verifica las credenciales
3. Actualiza `config.py` si son diferentes

---

### **3. Probar URL RTSP con VLC (CRÍTICO)**

1. Abre **VLC Media Player**
2. Ve a: **Media → Open Network Stream** (Ctrl+N)
3. Prueba estas URLs **UNA POR UNA**:

   ```
   rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/101
   rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/1
   rtsp://admin:citikold.2020@192.168.60.65:554/h264/ch1/main/av_stream
   ```

4. **Si alguna funciona en VLC:**
   - ✅ Esa es la URL RTSP correcta
   - El problema puede ser con OpenCV o las credenciales
   - Verifica que las credenciales en `config.py` sean **exactamente** las mismas

5. **Si ninguna funciona en VLC:**
   - ❌ Las credenciales son incorrectas
   - ❌ O la URL RTSP es diferente
   - Consulta el manual de la cámara para la URL RTSP correcta

---

### **4. Verificar en la interfaz web de la cámara**

1. Abre el navegador
2. Ve a: `http://192.168.60.65`
3. Inicia sesión con las credenciales
4. Busca la sección de **"RTSP"** o **"Streaming"**
5. Verifica:
   - La URL RTSP correcta
   - El puerto (generalmente 554)
   - Las credenciales

---

## 🔧 **SOLUCIÓN TEMPORAL: Reducir Intentos**

Mientras verificas la configuración, puedes **detener el NUC Agent** para evitar logs excesivos:

1. Presiona **Ctrl+C** en la ventana donde está corriendo el NUC Agent
2. O cierra la ventana

---

## ✅ **DESPUÉS DE CORREGIR**

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
   ❌ Error: 192.168.60.65 - No se pudo abrir la cámara
   ```

---

## 🆘 **SI NADA FUNCIONA**

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

## 📋 **CHECKLIST**

Antes de continuar, verifica:

- [ ] La cámara responde al ping (`ping 192.168.60.65`)
- [ ] Las credenciales son correctas (probar en interfaz web)
- [ ] La URL RTSP funciona en VLC
- [ ] `config.py` tiene las credenciales correctas
- [ ] El NUC Agent se reinicia después de corregir

---

**⚠️ IMPORTANTE: El problema NO es del código, es de la configuración de la cámara. Debes verificar la IP, credenciales y URL RTSP correctas.** 🎯
