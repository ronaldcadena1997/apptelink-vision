# 🔧 Solución: No Puedo Conectarme a la Cámara

## 🔍 **Causas Más Comunes**

Basado en tu cámara Hikvision DS-2CD1047G2 detectada por SADP:

1. ❌ **Credenciales incorrectas** (MÁS PROBABLE - 90%)
2. ❌ **URL RTSP incorrecta**
3. ❌ **Puerto bloqueado por firewall**
4. ❌ **Stream RTSP deshabilitado en la cámara**

---

## ✅ **SOLUCIÓN PASO A PASO**

### **PASO 1: Obtener las Credenciales Correctas**

#### **Opción A: Usar SADP (Recomendado)**

1. En la herramienta SADP que tienes abierta
2. Haz clic en la cámara (debe estar seleccionada)
3. En el campo **"Administrator Password"**, ingresa la contraseña
4. Si no la conoces, haz clic en **"Forgot Password"** para resetearla

#### **Opción B: Acceder por Interfaz Web**

1. Abre el navegador
2. Ve a: `http://192.168.60.65`
3. Intenta iniciar sesión con:
   - Usuario: `admin`
   - Contraseña: `citikold.2020` (o la que tengas configurada)

**Si no puedes iniciar sesión:**
- Las credenciales son incorrectas
- Necesitas resetear la contraseña usando SADP

---

### **PASO 2: Verificar Credenciales en config.py**

1. Abre `backend/config.py`:
   ```powershell
   notepad C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend\config.py
   ```

2. Verifica estas líneas (alrededor de la línea 119-120):
   ```python
   USUARIO_CAMARAS = 'admin'  # ⚠️ Verifica que sea correcto
   CONTRASENA_CAMARAS = 'citikold.2020'  # ⚠️ Verifica que sea correcto
   ```

3. **Si las credenciales son diferentes:**
   - Actualiza `USUARIO_CAMARAS` con el usuario correcto
   - Actualiza `CONTRASENA_CAMARAS` con la contraseña correcta
   - Guarda el archivo (Ctrl+S)

---

### **PASO 3: Probar Conexión Manualmente**

#### **Prueba 1: HTTP Snapshot (Más fácil)**

1. Abre el navegador
2. Ve a esta URL (reemplaza con tus credenciales):
   ```
   http://admin:TU_CONTRASENA@192.168.60.65/ISAPI/Streaming/channels/101/picture
   ```
   
   **Ejemplo si la contraseña es "citikold.2020":**
   ```
   http://admin:citikold.2020@192.168.60.65/ISAPI/Streaming/channels/101/picture
   ```

3. **Si ves la imagen:**
   - ✅ Las credenciales son correctas
   - ✅ La cámara está accesible
   - ✅ El problema está en el código (ya lo corregimos)

4. **Si NO ves la imagen:**
   - ❌ Las credenciales son incorrectas
   - ❌ O la URL no es correcta para tu modelo

#### **Prueba 2: RTSP en VLC**

1. Abre VLC Media Player
2. Ve a: **Media → Open Network Stream** (Ctrl+N)
3. Ingresa esta URL (reemplaza con tus credenciales):
   ```
   rtsp://admin:TU_CONTRASENA@192.168.60.65:554/Streaming/Channels/101
   ```

4. **Si funciona:**
   - ✅ Las credenciales y URL RTSP son correctas

5. **Si NO funciona:**
   - ❌ Las credenciales son incorrectas
   - ❌ O el puerto 554 está bloqueado

---

### **PASO 4: Verificar Firewall**

```powershell
# Verificar que el puerto 554 está abierto
netstat -ano | findstr :554
```

Si el puerto está bloqueado, agrega una excepción en el firewall de Windows.

---

### **PASO 5: Reiniciar NUC Agent**

Después de corregir las credenciales:

1. **Detén el NUC Agent actual:**
   - Presiona **Ctrl+C** en la ventana donde está corriendo

2. **Reinicia el NUC Agent:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
   .\ejecutar_nuc_agent_hikvision.bat
   ```

3. **Debes ver:**
   ```
   ✅ Snapshot capturado y enviado: 192.168.60.65 (12345 bytes)
   ```

---

## 🆘 **Si Aún No Funciona**

### **Problema: No Conozco la Contraseña**

1. Usa SADP:
   - Selecciona la cámara
   - Haz clic en **"Forgot Password"**
   - Sigue las instrucciones para resetear

2. O contacta al administrador que configuró la cámara

### **Problema: La URL HTTP no funciona**

Prueba estas URLs alternativas:

```
http://192.168.60.65/Streaming/channels/101/picture
http://192.168.60.65/cgi-bin/snapshot.cgi?channel=1
http://192.168.60.65/cgi-bin/snapshot.cgi
```

### **Problema: RTSP no funciona pero HTTP sí**

El código ya está configurado para usar HTTP primero (más confiable). Solo necesitas:
1. Verificar que las credenciales en `config.py` sean correctas
2. Reiniciar el NUC Agent

---

## 📋 **Checklist de Verificación**

Antes de reportar que no funciona, verifica:

- [ ] Las credenciales en `config.py` son correctas
- [ ] Puedes acceder a `http://192.168.60.65` en el navegador
- [ ] Puedes ver la imagen en: `http://admin:CONTRASENA@192.168.60.65/ISAPI/Streaming/channels/101/picture`
- [ ] El NUC Agent se reinició después de cambiar las credenciales
- [ ] No hay errores de firewall bloqueando el puerto 80 o 554

---

## 🎯 **Resumen**

**El problema más probable es que las credenciales en `config.py` no coinciden con las credenciales reales de la cámara.**

**Solución:**
1. Obtén las credenciales correctas (usando SADP o interfaz web)
2. Actualiza `config.py` con las credenciales correctas
3. Reinicia el NUC Agent

**¡Con las credenciales correctas debería funcionar inmediatamente!** ✅
