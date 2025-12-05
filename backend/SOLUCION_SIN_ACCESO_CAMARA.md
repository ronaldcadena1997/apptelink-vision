# 🔧 Solución: "SIN ACCESO" en Cámaras

## 🚨 **Problema**
La aplicación web detecta la cámara (`192.168.60.65`) pero muestra "SIN ACCESO" cuando intentas verla o capturar una imagen.

---

## ✅ **Causa del Problema**

El puente genérico del NUC **NO tiene el endpoint** `/api/camaras/<ip>/snapshot`. Solo tiene:
- `/api/status` ✅
- `/proxy/<path>` ✅ (para proxy genérico)

Cuando Railway intenta obtener un snapshot, hace proxy al NUC buscando `/api/camaras/<ip>/snapshot`, pero ese endpoint no existe en el puente genérico.

---

## 🔧 **Solución: Agregar Endpoint de Snapshot al Puente Genérico**

Necesitamos agregar un endpoint al puente genérico que procese snapshots usando OpenCV.

### **Paso 1: Actualizar `puente_generico_nuc.py`**

Agrega este código al archivo `puente_generico_nuc.py`:

```python
import cv2
import base64
from datetime import datetime

@app.route('/api/camaras/<ip>/snapshot', methods=['GET'])
def snapshot_camara(ip):
    """Obtiene un snapshot de una cámara usando RTSP"""
    # Verificar que la IP esté en la red local permitida
    if not es_ip_local(ip):
        return jsonify({
            "success": False,
            "error": f"IP {ip} no está en la red local permitida"
        }), 403
    
    # Credenciales de la cámara (puedes obtenerlas de variables de entorno)
    usuario = os.getenv('USUARIO_CAMARAS', 'admin')
    contrasena = os.getenv('CONTRASENA_CAMARAS', 'citikold.2020')
    
    # URLs RTSP a probar
    urls = [
        f"rtsp://{usuario}:{contrasena}@{ip}:554/Streaming/Channels/101",
        f"rtsp://{usuario}:{contrasena}@{ip}:554/Streaming/Channels/1",
    ]
    
    for url in urls:
        try:
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)  # 5 segundos timeout
            
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                
                if ret and frame is not None:
                    # Convertir a JPEG
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    return jsonify({
                        "success": True,
                        "image": f"data:image/jpeg;base64,{img_base64}",
                        "timestamp": datetime.now().isoformat(),
                        "ip": ip
                    })
        except Exception as e:
            print(f"Error obteniendo snapshot de {ip}: {e}")
            continue
    
    return jsonify({
        "success": False,
        "error": "No se pudo capturar imagen de la cámara"
    }), 500
```

### **Paso 2: Instalar OpenCV en el NUC**

En el NUC, ejecuta:

```powershell
pip install opencv-python-headless
```

O si ya lo tienes instalado, verifica:

```powershell
python -c "import cv2; print(cv2.__version__)"
```

---

## 🔄 **Alternativa: Usar el Proxy Genérico Directamente**

Si no quieres modificar el puente genérico, Railway puede usar el proxy genérico para acceder directamente a la cámara, pero necesita procesar el stream RTSP.

**Problema:** El proxy genérico puede hacer proxy a HTTP, pero RTSP es un protocolo diferente que requiere procesamiento especial.

---

## ✅ **Solución Recomendada: Agregar Endpoint al Puente**

La mejor solución es agregar el endpoint `/api/camaras/<ip>/snapshot` al puente genérico porque:

1. ✅ El puente genérico está en el NUC (tiene acceso directo a las cámaras)
2. ✅ Puede usar OpenCV para procesar RTSP
3. ✅ Railway solo necesita hacer proxy a ese endpoint
4. ✅ No requiere cambios en Railway

---

## 📝 **Pasos Completos**

### **1. En el NUC:**

1. **Abre `puente_generico_nuc.py`**
2. **Agrega el código del endpoint de snapshot** (ver arriba)
3. **Instala OpenCV si no lo tienes:**
   ```powershell
   pip install opencv-python-headless
   ```
4. **Reinicia el puente genérico:**
   - Detén el proceso actual (Ctrl+C)
   - Ejecuta: `python puente_generico_nuc.py`

### **2. Verificar que Funciona:**

Desde el NUC, prueba:

```powershell
curl http://localhost:5000/api/camaras/192.168.60.65/snapshot
```

Debería retornar JSON con `"success": true` y una imagen en base64.

### **3. Verificar desde Railway:**

Prueba desde Railway:

```
https://tu-backend.up.railway.app/api/camaras/192.168.60.65/snapshot
```

Debería retornar el snapshot de la cámara.

---

## 🚨 **Troubleshooting**

### **Problema 1: "ModuleNotFoundError: No module named 'cv2'"**

**Solución:**
```powershell
pip install opencv-python-headless
```

### **Problema 2: "No se pudo capturar imagen"**

**Causas posibles:**
- ❌ Credenciales incorrectas
- ❌ La cámara no está accesible desde el NUC
- ❌ El puerto RTSP está bloqueado

**Solución:**
1. Verifica las credenciales: `USUARIO_CAMARAS` y `CONTRASENA_CAMARAS`
2. Prueba desde el NUC: `ping 192.168.60.65`
3. Verifica que el puerto 554 esté abierto

### **Problema 3: "Timeout"**

**Causa:** La cámara tarda mucho en responder.

**Solución:**
- Aumenta el timeout en el código (línea `cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 10000)`)
- Verifica que la cámara esté funcionando

---

## 📋 **Checklist**

- [ ] ✅ OpenCV instalado en el NUC (`opencv-python-headless`)
- [ ] ✅ Endpoint `/api/camaras/<ip>/snapshot` agregado al puente genérico
- [ ] ✅ Puente genérico reiniciado
- [ ] ✅ Prueba local funciona (`curl http://localhost:5000/api/camaras/192.168.60.65/snapshot`)
- [ ] ✅ Prueba desde Railway funciona
- [ ] ✅ La aplicación web muestra la imagen correctamente

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
