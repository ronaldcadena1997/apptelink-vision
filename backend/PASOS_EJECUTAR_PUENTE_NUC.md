# 🚀 Pasos para Ejecutar el Puente Genérico en el NUC

## 📋 **Resumen**
Este documento te guía paso a paso para ejecutar el puente genérico en tu NUC, que permite al backend en Railway acceder a las cámaras en tu red local.

---

## ✅ **PASO 1: Verificar que Tailscale está instalado y funcionando**

### **En el NUC (Windows):**

1. **Abre PowerShell o CMD** (presiona `Windows + X` y selecciona "Windows PowerShell")

2. **Verifica que Tailscale está corriendo:**
   ```powershell
   tailscale status
   ```
   
   **Deberías ver algo como:**
   ```
   100.92.50.72  desktop-9chgoud  ronaldalfredocadenamoran@  windows
   ```

3. **Obtén tu IP de Tailscale:**
   ```powershell
   tailscale ip -4
   ```
   
   **✅ Tu IP de Tailscale es: `100.92.50.72`**
   
   **⚠️ IMPORTANTE:** Esta IP la necesitarás para configurar Railway en el Paso 6.

---

## ✅ **PASO 2: Configurar la Red Local en el Script**

### **En el NUC:**

**📡 Información de tu red:**
- **IP local del NUC:** `192.168.60.8`
- **Gateway:** `192.168.60.1`
- **Red local:** `192.168.60.x`
- **IP de tu cámara:** `192.168.60.65`

1. **Abre el archivo del puente genérico:**
   ```
   C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend\puente_generico_nuc.py
   ```

2. **Verifica/Edita la línea 25:**
   ```python
   RED_LOCAL = "192.168.60"  # Tu red local
   ```
   
   **✅ Ya está configurado correctamente** - Tu red es `192.168.60.x` y tu cámara está en `192.168.60.65`, así que `"192.168.60"` es correcto.

3. **Guarda el archivo** (Ctrl + S) si hiciste algún cambio

---

## ✅ **PASO 3: Instalar Dependencias (Solo la primera vez)**

### **En el NUC (PowerShell):**

1. **Navega a la carpeta del backend:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   ```

2. **Instala las dependencias:**
   ```powershell
   pip install flask flask-cors requests
   ```

   **Nota:** Si tienes Python 3, usa `pip3` en lugar de `pip`:
   ```powershell
   pip3 install flask flask-cors requests
   ```

3. **Verifica la instalación:**
   ```powershell
   python -c "import flask; import requests; print('✅ Dependencias instaladas correctamente')"
   ```

---

## ✅ **PASO 4: Ejecutar el Puente Genérico**

### **En el NUC (PowerShell):**

1. **Asegúrate de estar en la carpeta correcta:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   ```

2. **Ejecuta el puente genérico:**
   ```powershell
   python puente_generico_nuc.py
   ```

   O si usas Python 3:
   ```powershell
   python3 puente_generico_nuc.py
   ```

3. **Deberías ver algo como:**
   ```
   ============================================================
   🌉 Puente Genérico NUC
   ============================================================
   Este puente permite al backend en Railway hacer peticiones
   a CUALQUIER recurso en la red local.
   
   🚀 Iniciando puente genérico en puerto 5000...
   📡 Red local permitida: 192.168.60.x
   
   * Running on http://0.0.0.0:5000
   ```

4. **⚠️ IMPORTANTE:** Deja esta ventana abierta. El puente debe estar corriendo todo el tiempo.

---

## ✅ **PASO 5: Verificar que el Puente Funciona**

### **En el NUC (otra ventana de PowerShell):**

1. **Prueba el endpoint de estado:**
   ```powershell
   curl http://localhost:5000/api/status
   ```

   O desde un navegador, abre:
   ```
   http://localhost:5000/api/status
   ```

2. **Deberías ver:**
   ```json
   {
     "status": "online",
     "tipo": "puente_generico",
     "red_local": "192.168.60",
     "timestamp": "2025-01-04T..."
   }
   ```

---

## ✅ **PASO 6: Configurar Railway (Backend en Servidor)**

### **⚠️ CONSIDERACIÓN IMPORTANTE: Cada NUC tiene diferentes cámaras**

**Cada NUC tiene sus propias cámaras.** El sistema mapea automáticamente qué cámara pertenece a qué NUC. Hay dos formas de configurarlo:

---

### **Opción A: Usar config.py (Recomendado para mapeo explícito)**

Si subes el archivo `config.py` a GitHub, puedes especificar explícitamente qué cámara pertenece a qué NUC:

1. **Edita `backend/config.py`** en tu proyecto local:

```python
# NUCs
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.92.50.72',  # ← Tu IP de Tailscale
        'puerto': 5000,
        'nombre': 'NUC Principal',
        'red_local': '192.168.60'  # Tu red local
    },
    # Si tienes más NUCs, agrégalos aquí:
    # 'nuc_sede2': {
    #     'tailscale_ip': '100.92.50.XX',  # IP de Tailscale del NUC 2
    #     'puerto': 5000,
    #     'nombre': 'NUC Sede 2',
    #     'red_local': '192.168.61'
    # },
}

# Cámaras - ESPECIFICA QUÉ CÁMARA PERTENECE A QUÉ NUC
CAMARAS_CONFIG = [
    # Cámaras del NUC Principal
    {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},
    # Si tienes más cámaras, agrégalas aquí:
    # {'ip': '192.168.60.66', 'nombre': 'Cámara 2', 'nuc': 'nuc_sede1'},
    # {'ip': '192.168.60.67', 'nombre': 'Cámara 3', 'nuc': 'nuc_sede1'},
]
```

2. **Haz commit y push** del archivo `config.py` a GitHub
3. Railway usará automáticamente esta configuración

**Ventaja:** Mapeo explícito y claro de qué cámara pertenece a qué NUC.

---

### **Opción B: Usar Variables de Entorno en Railway**

Si prefieres usar variables de entorno (más flexible pero menos explícito):

1. **Ve a tu proyecto en Railway:**
   - Abre: https://railway.app
   - Selecciona tu proyecto

2. **Ve a Settings → Variables:**

3. **Agrega/Verifica estas variables de entorno:**

   **a) IP del NUC (Tailscale):**
   ```
   NUC_URLS=nuc_sede1:http://100.92.50.72:5000
   ```
   
   **✅ Esta es tu IP de Tailscale:** `100.92.50.72` (obtenida en el Paso 1)
   
   **Si tienes múltiples NUCs, agrega más separados por comas:**
   ```
   NUC_URLS=nuc_sede1:http://100.92.50.72:5000,nuc_sede2:http://100.92.50.XX:5000
   ```
   
   **Formato:** `nombre1:url1,nombre2:url2`

   **b) IPs de las Cámaras:**
   ```
   CAMARAS_IPS=192.168.60.65
   ```
   
   **✅ Esta es la IP de tu cámara:** `192.168.60.65` (según la configuración de tu cámara)
   
   **Si tienes más cámaras, sepáralas por comas:**
   ```
   CAMARAS_IPS=192.168.60.65,192.168.60.66,192.168.60.67
   ```
   
   **⚠️ IMPORTANTE:** El sistema mapeará automáticamente las cámaras a los NUCs basándose en:
   - El rango de red (ej: cámaras `192.168.60.x` → NUC con red `192.168.60`)
   - Si no puede mapear, usará el primer NUC disponible

4. **Guarda los cambios** (Railway reiniciará automáticamente)

**Nota:** Con variables de entorno, el mapeo es automático por rango de IP. Si tus cámaras están en diferentes redes, funcionará bien. Si todas están en la misma red, considera usar `config.py` para mapeo explícito.

---

### **¿Cuál opción usar?**

| Situación | Recomendación |
|-----------|--------------|
| **Cámaras en diferentes redes** (ej: 192.168.60.x y 192.168.61.x) | Variables de entorno (Opción B) - mapeo automático funciona bien |
| **Cámaras en la misma red** (ej: todas en 192.168.60.x) | `config.py` (Opción A) - mapeo explícito necesario |
| **Necesitas control total** | `config.py` (Opción A) - especificas exactamente qué cámara → qué NUC |
| **Configuración simple y rápida** | Variables de entorno (Opción B) |

---

## ✅ **PASO 7: Verificar que Todo Funciona**

### **Desde Railway:**

1. **Ve a tu servicio en Railway → Deployments**

2. **Abre los logs** y verifica que veas:
   ```
   📋 Usando variables de entorno
   📹 IPs de cámaras configuradas: 1
      - 192.168.60.65: Cámara Principal
   🔗 Modo PROXY activado. NUCs configurados: 1
      - nuc_sede1: http://100.92.50.72:5000
   ```
   
   **✅ Valores esperados:**
   - IP de Tailscale: `100.92.50.72`
   - IP de cámara: `192.168.60.65`

3. **Prueba el endpoint de estado desde Railway:**
   - Abre la URL pública de Railway (ejemplo: `https://tu-app.up.railway.app/api/status`)
   - Deberías ver el estado del servidor

4. **Prueba detectar cámaras:**
   - Abre: `https://tu-app.up.railway.app/api/camaras/detectar`
   - Deberías ver la lista de cámaras configuradas

---

## 🔧 **Ejecutar el Puente en Segundo Plano (Opcional)**

Si quieres que el puente se ejecute en segundo plano y no necesites tener la ventana abierta:

### **Opción 1: Usar `start` (Windows):**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
start /B python puente_generico_nuc.py
```

### **Opción 2: Crear un archivo .bat para ejecutar fácilmente:**

1. **Crea un archivo `ejecutar_puente.bat`** en la carpeta `backend`:

```batch
@echo off
cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend"
python puente_generico_nuc.py
pause
```

2. **Ejecuta haciendo doble clic en `ejecutar_puente.bat`**

### **Opción 3: Ejecutar como Servicio de Windows (Avanzado):**

Puedes usar herramientas como NSSM (Non-Sucking Service Manager) para ejecutarlo como servicio de Windows.

---

## 🚨 **Troubleshooting (Solución de Problemas)**

### **Problema 1: "ModuleNotFoundError: No module named 'flask'"**

**Solución:**
```powershell
pip install flask flask-cors requests
```

### **Problema 2: "Address already in use" (Puerto 5000 ocupado)**

**Solución:**
- Cierra otros programas que usen el puerto 5000
- O cambia el puerto en `puente_generico_nuc.py` (línea 218):
  ```python
  app.run(host='0.0.0.0', port=5001, debug=False)  # Cambia 5000 a 5001
  ```
- Y actualiza Railway: `NUC_URLS=nuc_sede1:http://100.92.50.72:5001`

### **Problema 3: "No se puede conectar al NUC desde Railway"**

**Verifica:**
1. ✅ Tailscale está corriendo en el NUC
2. ✅ El puente genérico está corriendo (ver Paso 4)
3. ✅ La IP de Tailscale en Railway es correcta
4. ✅ El firewall de Windows permite conexiones en el puerto 5000

**Abrir puerto en Firewall de Windows:**
```powershell
# Ejecuta como Administrador
New-NetFirewallRule -DisplayName "Puente Genérico" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

### **Problema 4: "IP no está en la red local permitida"**

**Solución:**
- Verifica que la `RED_LOCAL` en `puente_generico_nuc.py` coincida con la red de tus cámaras
- Si tus cámaras están en `192.168.1.x`, cambia a `RED_LOCAL = "192.168.1"`

---

## ✅ **Checklist Final**

Antes de considerar que todo está listo, verifica:

- [ ] ✅ Tailscale está instalado y corriendo → **Tu IP: `100.92.50.72`**
- [ ] ✅ Tienes la IP de Tailscale → **`100.92.50.72`** (verificada en Paso 1)
- [ ] ✅ El puente genérico está corriendo (puerto 5000)
- [ ] ✅ La red local está configurada → **`192.168.60`** (correcto para tu red)
- [ ] ✅ Railway tiene configurado `NUC_URLS` → **`nuc_sede1:http://100.92.50.72:5000`**
- [ ] ✅ Railway tiene configurado `CAMARAS_IPS` → **`192.168.60.65`** (tu cámara)
- [ ] ✅ Puedes acceder a `http://localhost:5000/api/status` desde el NUC
- [ ] ✅ El backend en Railway muestra la cámara correctamente

**📋 Resumen de tu configuración:**
- **Tailscale IP:** `100.92.50.72`
- **Red local:** `192.168.60.x`
- **IP del NUC:** `192.168.60.8`
- **IP de cámara:** `192.168.60.65`
- **Gateway:** `192.168.60.1`

---

## 📞 **Siguiente Paso**

Una vez que todo esté funcionando:

1. ✅ El puente genérico está corriendo en el NUC
2. ✅ Railway está configurado con las IPs correctas
3. ✅ Puedes acceder a las cámaras desde Railway

**¡Ya puedes usar tu aplicación!** 🎉

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
