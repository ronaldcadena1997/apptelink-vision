# 🔍 Diagnóstico: Error de Timeout al Conectar a la Cámara

## ❌ **Problema Detectado**
- **Error:** `ERR_CONNECTION_TIMED_OUT` al acceder a `192.168.60.65`
- **Causa:** La cámara no responde en el puerto HTTP (80)
- **Nota:** SADP detecta la cámara como "Active", pero el navegador no puede conectarse

---

## 🔍 **VERIFICACIONES INMEDIATAS**

### **1. Verificar que la cámara responde al ping**

```powershell
ping 192.168.60.65
```

**Si el ping funciona:**
- ✅ La cámara está en la red
- ✅ El problema es del puerto HTTP o firewall

**Si el ping NO funciona:**
- ❌ La cámara no está accesible desde este equipo
- ❌ Puede estar en una red diferente o VLAN

---

### **2. Verificar desde el mismo equipo donde funciona SADP**

**IMPORTANTE:** ¿Estás ejecutando el NUC Agent y probando el navegador desde el **mismo equipo** donde SADP detecta la cámara?

- **Si SADP funciona en otro equipo:**
  - El problema puede ser que el NUC y la cámara están en redes diferentes
  - O hay un firewall entre ellos

- **Si SADP funciona en el mismo equipo:**
  - El problema es específico del puerto HTTP o configuración de la cámara

---

### **3. Verificar Firewall de Windows**

```powershell
# Verificar reglas de firewall
netsh advfirewall firewall show rule name=all | findstr 192.168.60.65
```

**Solución temporal (solo para pruebas):**
```powershell
# Deshabilitar firewall temporalmente (SOLO PARA PRUEBAS)
netsh advfirewall set allprofiles state off
```

**Después de probar, vuelve a habilitarlo:**
```powershell
netsh advfirewall set allprofiles state on
```

---

### **4. Verificar que el puerto 80 está abierto**

```powershell
# Probar conexión al puerto 80
Test-NetConnection -ComputerName 192.168.60.65 -Port 80
```

**Si el puerto está cerrado:**
- El firewall está bloqueando
- O el servicio HTTP de la cámara está deshabilitado

---

### **5. Verificar configuración de red del NUC**

```powershell
# Verificar IP del NUC
ipconfig

# Verificar que está en la misma red (192.168.60.x)
```

**Debe mostrar algo como:**
```
IPv4 Address. . . . . . . . . . . : 192.168.60.XXX
Subnet Mask . . . . . . . . . . . : 255.255.255.0
Default Gateway . . . . . . . . . : 192.168.60.1
```

**Si el NUC está en una red diferente (ej: 192.168.1.x):**
- ❌ No podrá acceder a la cámara en 192.168.60.65
- ✅ Necesitas configurar el NUC en la misma red

---

## 🔧 **SOLUCIONES**

### **Solución 1: Verificar desde el equipo donde SADP funciona**

1. **En el equipo donde SADP detecta la cámara:**
   - Abre el navegador
   - Ve a: `http://192.168.60.65`
   - **Si funciona aquí:** El problema es de red entre el NUC y la cámara
   - **Si NO funciona aquí:** El problema es de la cámara o firewall local

---

### **Solución 2: Configurar el NUC en la misma red**

Si el NUC está en una red diferente:

1. **Cambiar IP del NUC:**
   - Ve a: Configuración → Red e Internet → Ethernet
   - Cambia a IP estática: `192.168.60.XXX` (donde XXX es diferente de 65)
   - Máscara: `255.255.255.0`
   - Gateway: `192.168.60.1`

2. **Verificar conectividad:**
   ```powershell
   ping 192.168.60.65
   ```

---

### **Solución 3: Verificar Firewall de la Cámara**

1. **Usa SADP:**
   - Selecciona la cámara
   - Ingresa la contraseña de administrador
   - Haz clic en "Modify"
   - Verifica que el puerto HTTP (80) esté habilitado

2. **O accede por interfaz web (si puedes):**
   - Configuración → Red → Avanzado
   - Verifica que HTTP esté habilitado

---

### **Solución 4: Probar puerto alternativo**

Algunas cámaras Hikvision usan puerto 8000 para HTTP:

```
http://192.168.60.65:8000
```

Prueba esta URL en el navegador.

---

### **Solución 5: Usar RTSP directamente (si HTTP no funciona)**

Si HTTP no funciona pero RTSP sí:

1. **Prueba RTSP en VLC:**
   ```
   rtsp://admin:CONTRASENA@192.168.60.65:554/Streaming/Channels/101
   ```

2. **Si RTSP funciona:**
   - El código ya está configurado para intentar RTSP
   - Solo necesitas verificar las credenciales en `config.py`

---

## 📋 **CHECKLIST DE DIAGNÓSTICO**

Ejecuta estos comandos y comparte los resultados:

```powershell
# 1. Ping a la cámara
ping 192.168.60.65

# 2. Verificar IP del NUC
ipconfig | findstr IPv4

# 3. Probar puerto 80
Test-NetConnection -ComputerName 192.168.60.65 -Port 80

# 4. Verificar puerto 8000
Test-NetConnection -ComputerName 192.168.60.65 -Port 8000

# 5. Verificar puerto 554 (RTSP)
Test-NetConnection -ComputerName 192.168.60.65 -Port 554
```

---

## 🆘 **SI NADA FUNCIONA**

1. **Verifica que estás en el mismo equipo donde SADP funciona:**
   - Si SADP funciona en otro equipo, el problema es de red
   - Configura el NUC en la misma red que la cámara

2. **Verifica VLANs:**
   - Si hay VLANs configuradas, el NUC y la cámara deben estar en la misma VLAN

3. **Contacta al administrador de red:**
   - Puede haber reglas de firewall bloqueando la comunicación
   - O la cámara puede estar en una red aislada

---

## 🎯 **RESUMEN**

**El error `ERR_CONNECTION_TIMED_OUT` indica:**
- ❌ Problema de conectividad de red (más probable)
- ❌ Firewall bloqueando el puerto 80
- ❌ El NUC y la cámara están en redes diferentes

**Solución inmediata:**
1. Verifica que el NUC está en la misma red (192.168.60.x)
2. Prueba desde el mismo equipo donde SADP funciona
3. Verifica firewall de Windows

**¡Comparte los resultados de los comandos de diagnóstico para ayudarte mejor!** 🔍
