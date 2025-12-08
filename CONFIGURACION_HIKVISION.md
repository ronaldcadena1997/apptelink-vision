# 📹 Configuración para Cámara Hikvision DS-2CD1047G2

## ✅ **Información Confirmada**
- **Modelo:** DS-2CD1047G2 (Hikvision)
- **IP:** 192.168.60.65
- **Estado:** Active (detectada por SADP)
- **Puerto HTTP:** 80
- **Puerto SDK:** 8000

---

## 🔧 **URLs de Acceso para Hikvision**

### **1. HTTP Snapshots (RECOMENDADO - Más rápido y confiable)**

Estas URLs funcionan mejor que RTSP para snapshots:

```
http://192.168.60.65/ISAPI/Streaming/channels/101/picture
http://192.168.60.65/ISAPI/Streaming/channels/1/picture
http://192.168.60.65/cgi-bin/snapshot.cgi?channel=1
```

**Ventajas:**
- ✅ Más rápido que RTSP
- ✅ Menos recursos
- ✅ Más confiable
- ✅ No requiere streaming continuo

---

### **2. RTSP Streams (Para video en vivo)**

Si necesitas streaming de video:

```
rtsp://admin:password@192.168.60.65:554/Streaming/Channels/101
rtsp://admin:password@192.168.60.65:554/Streaming/Channels/1
rtsp://admin:password@192.168.60.65:554/h264/ch1/main/av_stream
```

---

## 🔐 **Verificar Credenciales**

### **Paso 1: Acceder a la interfaz web**

1. Abre el navegador
2. Ve a: `http://192.168.60.65`
3. Inicia sesión con las credenciales

### **Paso 2: Verificar credenciales en config.py**

Abre `backend/config.py` y verifica:

```python
USUARIO_CAMARAS = 'admin'  # ⚠️ ¿Es correcto?
CONTRASENA_CAMARAS = 'citikold.2020'  # ⚠️ ¿Es correcto?
```

**Si las credenciales son diferentes:**
1. Actualiza `config.py` con las credenciales correctas
2. Reinicia el NUC Agent

---

## 🧪 **Probar URLs Manualmente**

### **Opción 1: Probar HTTP Snapshot en el navegador**

1. Abre el navegador
2. Ve a: `http://admin:citikold.2020@192.168.60.65/ISAPI/Streaming/channels/101/picture`
3. Si te pide credenciales, ingrésalas
4. **Si ves la imagen:** ✅ Las credenciales y URL son correctas
5. **Si no ves la imagen:** ❌ Verifica credenciales o prueba otras URLs

### **Opción 2: Probar RTSP en VLC**

1. Abre VLC Media Player
2. Media → Open Network Stream (Ctrl+N)
3. URL: `rtsp://admin:citikold.2020@192.168.60.65:554/Streaming/Channels/101`
4. **Si funciona:** ✅ Las credenciales y URL RTSP son correctas
5. **Si no funciona:** ❌ Verifica credenciales

---

## 🔄 **Actualizar Código**

He actualizado el código para:

1. ✅ **Priorizar HTTP snapshots** (más rápido y confiable para Hikvision)
2. ✅ **Usar URLs específicas de Hikvision** (ISAPI)
3. ✅ **Intentar múltiples URLs** en orden de preferencia

---

## 📋 **Próximos Pasos**

1. **Verifica las credenciales:**
   - Accede a `http://192.168.60.65` en el navegador
   - Confirma usuario y contraseña

2. **Prueba HTTP snapshot:**
   - Ve a: `http://admin:citikold.2020@192.168.60.65/ISAPI/Streaming/channels/101/picture`
   - Si funciona, actualiza `config.py` con las credenciales correctas

3. **Reinicia el NUC Agent:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
   .\ejecutar_nuc_agent_hikvision.bat
   ```

4. **Debes ver:**
   ```
   ✅ Snapshot capturado y enviado: 192.168.60.65 (12345 bytes)
   ```

---

## 🆘 **Si Aún No Funciona**

1. **Verifica que las credenciales sean correctas:**
   - Usa SADP para cambiar la contraseña si es necesario
   - O verifica en la interfaz web de la cámara

2. **Verifica el firewall:**
   - El puerto 80 (HTTP) debe estar abierto
   - El puerto 554 (RTSP) debe estar abierto si usas RTSP

3. **Consulta el manual de la cámara:**
   - Busca la sección de "API" o "ISAPI"
   - Verifica las URLs correctas para tu modelo específico

---

**¡Con estas URLs específicas de Hikvision deberías poder capturar los snapshots correctamente!** 🎯
