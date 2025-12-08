# 🔧 Configurar NUC en la Red de la Cámara

## ❌ **Problema Identificado**
- **NUC está en:** `192.168.100.172` (red 192.168.100.x)
- **Cámara está en:** `192.168.60.65` (red 192.168.60.x)
- **Resultado:** No pueden comunicarse (redes diferentes)

---

## ✅ **SOLUCIÓN: Configurar NUC en la Red 192.168.60.x**

### **OPCIÓN 1: Configurar Ethernet (Recomendado)**

El adaptador "Ethernet 2" tiene IP APIPA (`169.254.99.37`), lo que significa que no está configurado. Vamos a configurarlo:

#### **Paso 1: Abrir Configuración de Red**

1. Presiona **Win + I** (abre Configuración)
2. Ve a: **Red e Internet → Ethernet**
3. Haz clic en **"Ethernet 2"** (o el adaptador Ethernet que uses)
4. Haz clic en **"Editar"** junto a "Asignación de IP"

#### **Paso 2: Configurar IP Estática**

1. Cambia de **"Automático (DHCP)"** a **"Manual"**
2. Activa el interruptor de **"IPv4"**
3. Ingresa estos valores:
   - **Dirección IP:** `192.168.60.100` (o cualquier IP libre en 192.168.60.x, excepto 65)
   - **Longitud del prefijo de subred:** `24` (o `255.255.255.0`)
   - **Puerta de enlace:** `192.168.60.1`
   - **DNS preferido:** `192.168.60.1` (o `8.8.8.8`)
   - **DNS alternativo:** `8.8.4.4` (opcional)

4. Haz clic en **"Guardar"**

#### **Paso 3: Verificar Conectividad**

```powershell
# Verificar nueva IP
ipconfig

# Probar ping a la cámara
ping 192.168.60.65
```

**Debe mostrar:**
- IP del NUC: `192.168.60.100` (o la que configuraste)
- Ping exitoso a `192.168.60.65`

---

### **OPCIÓN 2: Conectar Ethernet Físicamente**

Si el adaptador Ethernet no está conectado:

1. **Conecta el cable Ethernet** del NUC al mismo switch/router donde está la cámara
2. **Espera unos segundos** para que obtenga IP automáticamente
3. **Verifica:**
   ```powershell
   ipconfig
   ```
   Debe mostrar una IP en `192.168.60.x`

---

### **OPCIÓN 3: Cambiar Red Wi-Fi (Si es posible)**

Si puedes cambiar la red Wi-Fi:

1. Ve a: **Configuración → Red e Internet → Wi-Fi**
2. Conecta a la red Wi-Fi que esté en `192.168.60.x`
3. O configura IP estática en Wi-Fi (similar a Opción 1)

---

## 🧪 **Verificar que Funciona**

Después de configurar:

### **1. Verificar IP del NUC**
```powershell
ipconfig | findstr IPv4
```

**Debe mostrar:** `192.168.60.XXX`

### **2. Probar Ping a la Cámara**
```powershell
ping 192.168.60.65
```

**Debe mostrar:** Respuestas exitosas (time < 10ms)

### **3. Probar en el Navegador**
```
http://192.168.60.65
```

**Debe mostrar:** Interfaz web de la cámara (o pedir credenciales)

### **4. Reiniciar NUC Agent**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\ejecutar_nuc_agent_hikvision.bat
```

**Debe mostrar:**
```
✅ Snapshot capturado y enviado: 192.168.60.65 (12345 bytes)
```

---

## 🔧 **Configuración Rápida por PowerShell (Alternativa)**

Si prefieres usar PowerShell:

```powershell
# Configurar IP estática en Ethernet
New-NetIPAddress -InterfaceAlias "Ethernet 2" -IPAddress 192.168.60.100 -PrefixLength 24 -DefaultGateway 192.168.60.1

# Configurar DNS
Set-DnsClientServerAddress -InterfaceAlias "Ethernet 2" -ServerAddresses 192.168.60.1,8.8.8.8
```

**Verificar:**
```powershell
ipconfig
ping 192.168.60.65
```

---

## ⚠️ **IMPORTANTE**

1. **Asegúrate de que el cable Ethernet esté conectado** al mismo switch/router que la cámara
2. **Verifica que la IP que elijas no esté en uso** (no uses 192.168.60.65, esa es de la cámara)
3. **Después de configurar, reinicia el NUC Agent** para que use la nueva configuración

---

## 📋 **Checklist**

Después de configurar, verifica:

- [ ] El NUC tiene IP en `192.168.60.x` (verificar con `ipconfig`)
- [ ] El ping a `192.168.60.65` funciona
- [ ] Puedes acceder a `http://192.168.60.65` en el navegador
- [ ] El NUC Agent puede capturar snapshots

---

## 🆘 **Si Aún No Funciona**

1. **Verifica que el cable Ethernet esté conectado**
2. **Verifica que esté conectado al mismo switch/router que la cámara**
3. **Verifica que no haya VLANs separadas**
4. **Contacta al administrador de red** si hay configuración especial

---

**¡Una vez que el NUC esté en la misma red (192.168.60.x), debería poder conectarse a la cámara sin problemas!** ✅
