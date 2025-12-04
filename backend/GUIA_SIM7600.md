# 📡 Guía: Configurar SIM7600 para Internet en NUC (Windows)

## 📋 **Objetivo:**
Configurar el módulo SIM7600 para proporcionar conectividad a internet al NUC a través de redes celulares (3G/4G).

---

## ✅ **PASO 1: Verificar Hardware**

### **1.1. Conexiones del SIM7600**

Verifica que el módulo esté correctamente conectado:

- **SIM7600** → **NUC (Windows)**
  - **VCC** → 5V (o según especificaciones)
  - **GND** → GND
  - **TXD** → Puerto COM (RX del NUC)
  - **RXD** → Puerto COM (TX del NUC)
  - **SIM Card** → Insertada correctamente
  - **Antena** → Conectada

### **1.2. Identificar Puerto COM**

**En Windows (PowerShell o CMD):**

```powershell
# Ver puertos COM disponibles
Get-PnpDevice -Class Ports | Where-Object {$_.Status -eq "OK"}

# O usando Device Manager:
# Windows + X → Device Manager → Ports (COM & LPT)
```

**Anota el puerto COM** (ejemplo: `COM3`, `COM4`, etc.)

---

## ✅ **PASO 2: Instalar SSCOM**

### **2.1. Descargar SSCOM**

1. **Descarga SSCOM:**
   - Busca "SSCOM serial port tool" en Google
   - O descarga desde: https://www.mcu001.com/ (versión gratuita)
   - Versión recomendada: SSCOM 5.13.1 o superior

2. **Instala SSCOM:**
   - Ejecuta el instalador
   - Sigue las instrucciones
   - No requiere permisos de administrador

---

## ✅ **PASO 3: Configurar SIM7600 con SSCOM**

### **3.1. Abrir SSCOM y Conectar**

1. **Abre SSCOM**
2. **Selecciona el Puerto COM:**
   - En el menú desplegable, selecciona el puerto COM del SIM7600
   - Ejemplo: `COM3`

3. **Configura los parámetros:**
   - **Baud Rate:** `115200` (o según tu módulo)
   - **Data Bits:** `8`
   - **Stop Bits:** `1`
   - **Parity:** `None`
   - **Flow Control:** `None`

4. **Click en "Open"** para conectar

### **3.2. Verificar Comunicación**

**Envía estos comandos AT uno por uno** (escribe en la línea de comandos y presiona Enter):

```
AT
```

**Respuesta esperada:** `OK`

Si no responde:
- ✅ Verifica las conexiones
- ✅ Verifica el puerto COM
- ✅ Verifica el Baud Rate
- ✅ Verifica que el módulo esté encendido (LED encendido)

---

## ✅ **PASO 4: Configurar Tarjeta SIM**

### **4.1. Verificar SIM Card**

```
AT+CPIN?
```

**Respuesta esperada:**
- `+CPIN: READY` → SIM lista
- `+CPIN: SIM PIN` → Necesita PIN
- `+CPIN: SIM PUK` → Necesita PUK

### **4.2. Si Necesita PIN**

```
AT+CPIN="1234"
```

**Reemplaza `1234` con tu PIN real**

### **4.3. Verificar Operador**

```
AT+COPS?
```

**Respuesta esperada:** `+COPS: 0,0,"NOMBRE_OPERADOR"`

---

## ✅ **PASO 5: Configurar Internet (APN)**

### **5.1. Obtener APN de tu Operador**

**APNs comunes en México:**
- **Telcel:** `internet.itelcel.com`
- **Movistar:** `internet.movistar.mx`
- **AT&T:** `internet.att.com.mx`

**APNs comunes en otros países:**
- **España (Movistar):** `internet.movistar.es`
- **España (Vodafone):** `airtelnet.es`
- **Colombia (Claro):** `internet.claro.com.co`
- **Argentina (Claro):** `internet.claro.com.ar`

**💡 Busca el APN de tu operador** si no está en la lista.

### **5.2. Configurar APN**

**Reemplaza `TU_APN` con el APN de tu operador:**

```
AT+CGDCONT=1,"IP","TU_APN"
```

**Ejemplo para Telcel:**
```
AT+CGDCONT=1,"IP","internet.itelcel.com"
```

**Respuesta esperada:** `OK`

### **5.3. Activar Contexto PDP**

```
AT+CGACT=1,1
```

**Respuesta esperada:** `OK`

### **5.4. Verificar Registro en Red**

```
AT+CREG?
```

**Respuesta esperada:** `+CREG: 0,1` o `+CREG: 0,5` (registrado)

```
AT+CGREG?
```

**Respuesta esperada:** `+CGREG: 0,1` o `+CGREG: 0,5` (registrado en GPRS)

---

## ✅ **PASO 6: Obtener IP y Verificar Conexión**

### **6.1. Obtener Dirección IP**

```
AT+CGPADDR=1
```

**Respuesta esperada:** `+CGPADDR: 1,"10.XXX.XXX.XXX"`

**Anota la IP** que te da.

### **6.2. Verificar DNS**

```
AT+CDNSCFG="8.8.8.8","8.8.4.4"
```

Esto configura DNS de Google.

### **6.3. Probar Conexión a Internet**

```
AT+HTTPINIT
AT+HTTPPARA="URL","http://www.google.com"
AT+HTTPACTION=0
```

**Respuesta esperada:** `+HTTPACTION: 0,200,XXX` (200 = éxito)

---

## ✅ **PASO 7: Configurar Windows para Usar SIM7600**

### **7.1. Instalar Driver del SIM7600 (Si es necesario)**

Algunos módulos SIM7600 necesitan drivers específicos:
- Busca el driver en el sitio del fabricante
- O usa drivers genéricos de módulos USB-to-Serial

### **7.2. Crear Conexión de Red en Windows**

**Opción A: Usando Script PowerShell (Recomendado)**

Crea un archivo `configurar_sim7600.ps1`:

```powershell
# Configurar SIM7600 como conexión de red
# Ejecutar como Administrador

# 1. Instalar módulo necesario (solo primera vez)
# Install-Module -Name NetAdapter -Force

# 2. Verificar que el módulo esté conectado
Get-PnpDevice | Where-Object {$_.FriendlyName -like "*SIM7600*" -or $_.FriendlyName -like "*Modem*"}

# 3. Si aparece como modem, Windows debería detectarlo automáticamente
# Si no, necesitas configurar manualmente en:
# Settings → Network & Internet → Dial-up
```

**Opción B: Configuración Manual**

1. **Abre Settings:**
   - `Windows + I` → **Network & Internet**

2. **Dial-up:**
   - Click en **"Dial-up"** en el menú lateral
   - Click en **"Set up a new connection"**
   - Selecciona **"Connect to the Internet"**
   - Selecciona **"Dial-up"**
   - Ingresa:
     - **Phone number:** `*99#` o `*99***1#`
     - **Username:** (dejar vacío o según operador)
     - **Password:** (dejar vacío o según operador)
     - **Connection name:** `SIM7600 Internet`

3. **Conectar:**
   - Click en **"Connect"**
   - Espera a que se establezca la conexión

---

## ✅ **PASO 8: Verificar Internet en Windows**

### **8.1. Probar Conexión**

**En PowerShell o CMD:**

```powershell
# Verificar IP asignada
ipconfig

# Probar conexión a internet
ping 8.8.8.8

# Probar DNS
nslookup google.com

# Probar HTTP
Invoke-WebRequest -Uri http://www.google.com
```

### **8.2. Si No Funciona**

1. **Verifica que el módulo esté registrado:**
   ```
   AT+CREG?
   AT+CGREG?
   ```

2. **Verifica APN:**
   ```
   AT+CGDCONT?
   ```

3. **Reinicia el contexto PDP:**
   ```
   AT+CGACT=0,1
   AT+CGACT=1,1
   ```

4. **Verifica señal:**
   ```
   AT+CSQ
   ```
   - Valores: `0-31` (mayor = mejor señal)
   - Si es `99`, no hay señal

---

## ✅ **PASO 9: Configuración Automática (Opcional)**

### **9.1. Script para Configurar SIM7600 Automáticamente**

Crea un archivo `configurar_sim7600.bat`:

```batch
@echo off
echo Configurando SIM7600...

REM Reemplaza COM3 con tu puerto COM
REM Reemplaza el APN con el de tu operador

echo AT > COM3
timeout /t 1
echo AT+CPIN? > COM3
timeout /t 1
echo AT+CGDCONT=1,"IP","internet.itelcel.com" > COM3
timeout /t 1
echo AT+CGACT=1,1 > COM3
timeout /t 1
echo AT+CREG? > COM3
timeout /t 1
echo AT+CGREG? > COM3
timeout /t 1
echo AT+CGPADDR=1 > COM3

echo Configuracion completada!
pause
```

**⚠️ Nota:** Este método básico puede no funcionar. Es mejor usar SSCOM o un script Python.

### **9.2. Script Python para Configuración Automática**

Crea un archivo `configurar_sim7600.py`:

```python
import serial
import time

# Configuración
PORT = 'COM3'  # Cambia por tu puerto COM
BAUDRATE = 115200
APN = 'internet.itelcel.com'  # Cambia por tu APN

# Comandos AT
comandos = [
    'AT',  # Test
    'AT+CPIN?',  # Verificar SIM
    f'AT+CGDCONT=1,"IP","{APN}"',  # Configurar APN
    'AT+CGACT=1,1',  # Activar contexto
    'AT+CREG?',  # Verificar registro
    'AT+CGREG?',  # Verificar registro GPRS
    'AT+CSQ',  # Verificar señal
    'AT+CGPADDR=1',  # Obtener IP
]

try:
    # Abrir puerto serial
    ser = serial.Serial(PORT, BAUDRATE, timeout=5)
    print(f"Conectado a {PORT}")
    time.sleep(2)
    
    # Enviar comandos
    for cmd in comandos:
        print(f"\nEnviando: {cmd}")
        ser.write(f'{cmd}\r\n'.encode())
        time.sleep(1)
        
        # Leer respuesta
        if ser.in_waiting:
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            print(f"Respuesta: {response}")
        time.sleep(1)
    
    ser.close()
    print("\n✅ Configuración completada!")
    
except serial.SerialException as e:
    print(f"❌ Error: {e}")
    print("Verifica que el puerto COM sea correcto y que el módulo esté conectado")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Para ejecutar:**

```powershell
# Instalar pyserial (si no está instalado)
pip install pyserial

# Ejecutar script
python configurar_sim7600.py
```

---

## 🔧 **Troubleshooting**

### **❌ Error: "No Response" o "Timeout"**

**Soluciones:**
1. ✅ Verifica que el puerto COM sea correcto
2. ✅ Verifica el Baud Rate (prueba 9600, 115200, 230400)
3. ✅ Verifica las conexiones TX/RX (pueden estar invertidas)
4. ✅ Verifica que el módulo esté encendido
5. ✅ Prueba otro cable USB/Serial

---

### **❌ Error: "+CPIN: SIM PIN"**

**Solución:**
```
AT+CPIN="TU_PIN"
```

---

### **❌ Error: "+CREG: 0,0" (No registrado)**

**Soluciones:**
1. ✅ Verifica que la SIM tenga saldo/plan de datos
2. ✅ Verifica que la SIM esté activada
3. ✅ Verifica la señal: `AT+CSQ`
4. ✅ Cambia de ubicación (mejor señal)
5. ✅ Verifica que la antena esté conectada

---

### **❌ Error: "+CGREG: 0,0" (No registrado en GPRS)**

**Soluciones:**
1. ✅ Verifica el APN: `AT+CGDCONT?`
2. ✅ Configura el APN correcto
3. ✅ Activa el contexto: `AT+CGACT=1,1`
4. ✅ Espera unos segundos y verifica: `AT+CGREG?`

---

### **❌ No Obtiene IP**

**Soluciones:**
1. ✅ Verifica APN: `AT+CGDCONT?`
2. ✅ Verifica registro: `AT+CGREG?`
3. ✅ Reinicia contexto:
   ```
   AT+CGACT=0,1
   AT+CGACT=1,1
   ```
4. ✅ Reinicia el módulo (desconecta y conecta)

---

### **❌ Internet No Funciona en Windows**

**Soluciones:**
1. ✅ Verifica que Windows detecte el módulo como modem
2. ✅ Configura la conexión dial-up manualmente
3. ✅ Verifica que la conexión esté activa en Network Settings
4. ✅ Prueba con otro navegador
5. ✅ Verifica firewall/antivirus

---

## 📝 **Comandos AT Útiles**

```
# Información del módulo
ATI                    # Información del módulo
AT+GMI                 # Fabricante
AT+GMM                 # Modelo
AT+GMR                 # Versión

# SIM Card
AT+CPIN?               # Estado del PIN
AT+CPIN="1234"         # Ingresar PIN
AT+CCID                # Número de serie de la SIM

# Red
AT+COPS?               # Operador actual
AT+CREG?               # Registro en red
AT+CGREG?              # Registro GPRS
AT+CSQ                 # Intensidad de señal (0-31)

# Internet
AT+CGDCONT?            # Ver APN configurado
AT+CGDCONT=1,"IP","APN" # Configurar APN
AT+CGACT=1,1           # Activar contexto
AT+CGPADDR=1           # Obtener IP
AT+CDNSCFG="8.8.8.8","8.8.4.4" # Configurar DNS

# Reiniciar
AT+CFUN=1,1            # Reiniciar módulo
```

---

## ✅ **Checklist Final**

Antes de considerar que está configurado:

- [ ] SIM7600 conectado correctamente
- [ ] Puerto COM identificado
- [ ] SSCOM instalado y conectado
- [ ] Comando `AT` responde `OK`
- [ ] SIM Card insertada y reconocida
- [ ] PIN ingresado (si es necesario)
- [ ] APN configurado correctamente
- [ ] Registrado en red (`+CREG: 0,1` o `0,5`)
- [ ] Registrado en GPRS (`+CGREG: 0,1` o `0,5`)
- [ ] IP obtenida (`AT+CGPADDR=1`)
- [ ] Conexión a internet funcionando en Windows
- [ ] Puede hacer ping a 8.8.8.8
- [ ] Puede acceder a sitios web

---

## 🎉 **¡Listo!**

Si completaste todos los pasos, tu NUC ahora tiene acceso a internet a través del SIM7600.

**Próximos pasos:**
- ✅ Configura Tailscale en el NUC para acceso remoto
- ✅ Inicia el backend: `python server.py`
- ✅ Configura Railway con la IP de Tailscale

---

## 📞 **Soporte Adicional**

Si necesitas más ayuda:
- 📄 **Tailscale:** Ver `QUE_ES_TAILSCALE.md`
- 📄 **Backend:** Ver `GUIA_CONFIGURACION_SERVIDOR.md`
- 📄 **Deployment:** Ver `README_DEPLOYMENT_COMPLETO.md`

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
