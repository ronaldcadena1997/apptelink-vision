# 🚀 Guía: Configurar API del NUC como Servicio Automático

## ✅ **Solución Simple y Automática**

Esta solución configura el API del NUC para que:
- ✅ Se ejecute automáticamente al iniciar Windows
- ✅ Se ejecute en segundo plano (sin ventana)
- ✅ Se reinicie automáticamente si se cae
- ✅ No requiera intervención manual

---

## 📋 **Pasos para Configurar (UNA SOLA VEZ)**

### **Paso 1: Ejecutar el Script de Configuración**

1. **Haz doble clic en:**
   ```
   configurar_servicio_automatico.bat
   ```

2. **Si te pide permisos de administrador:**
   - Haz clic en "Sí" o "Aceptar"
   - El script se ejecutará automáticamente como administrador

3. **Espera a que termine:**
   - Verás mensajes de confirmación
   - Cuando termine, presiona cualquier tecla

**¡Listo!** El API se ejecutará automáticamente cada vez que el NUC se reinicie.

---

## 🔧 **Scripts Disponibles**

### **1. `configurar_servicio_automatico.bat`**
- **Uso:** Ejecutar UNA SOLA VEZ para configurar el inicio automático
- **Qué hace:** Crea una tarea programada de Windows que ejecuta el API automáticamente

### **2. `ejecutar_api_background.bat`**
- **Uso:** Se ejecuta automáticamente (no necesitas hacer nada)
- **Qué hace:** Mantiene el API corriendo y lo reinicia si se cae

### **3. `verificar_estado.bat`**
- **Uso:** Ejecutar cuando quieras verificar si el API está funcionando
- **Qué hace:** Muestra el estado del API, procesos Python, y Tailscale

### **4. `detener_api.bat`**
- **Uso:** Ejecutar si necesitas detener el API manualmente
- **Qué hace:** Detiene todos los procesos del API

---

## ✅ **Verificar que Funciona**

### **Método 1: Usar el Script de Verificación**
```powershell
.\verificar_estado.bat
```

### **Método 2: Verificar Manualmente**
```powershell
# Verificar que el API responde
Invoke-WebRequest http://localhost:5000/api/status

# Verificar que el puerto está en uso
netstat -ano | findstr ":5000"
```

### **Método 3: Verificar la Tarea Programada**
1. Presiona `Windows + R`
2. Escribe: `taskschd.msc` y presiona Enter
3. Busca la tarea: `PuenteGenericoNUC_Auto`
4. Debe estar en estado "Listo" o "Ejecutándose"

---

## 🔄 **Reiniciar el API Manualmente**

Si necesitas reiniciar el API:

1. **Detener:**
   ```powershell
   .\detener_api.bat
   ```

2. **Esperar 5 segundos**

3. **Iniciar (se iniciará automáticamente en 60 segundos, o puedes ejecutar):**
   ```powershell
   .\ejecutar_api_background.bat
   ```

---

## ❌ **Desinstalar el Servicio Automático**

Si quieres desactivar el inicio automático:

1. Presiona `Windows + R`
2. Escribe: `taskschd.msc` y presiona Enter
3. Busca la tarea: `PuenteGenericoNUC_Auto`
4. Haz clic derecho → "Eliminar"

---

## 🐛 **Solución de Problemas**

### **El API no se inicia automáticamente**

1. **Verifica que la tarea programada existe:**
   ```powershell
   schtasks /Query /TN "PuenteGenericoNUC_Auto"
   ```

2. **Ejecuta la tarea manualmente para probar:**
   ```powershell
   schtasks /Run /TN "PuenteGenericoNUC_Auto"
   ```

3. **Verifica los logs de la tarea:**
   - Abre el Programador de tareas (`taskschd.msc`)
   - Busca `PuenteGenericoNUC_Auto`
   - Haz clic derecho → "Ver historial"

### **El API se detiene frecuentemente**

1. **Verifica que Python esté instalado correctamente:**
   ```powershell
   python --version
   ```

2. **Verifica que las dependencias estén instaladas:**
   ```powershell
   cd backend
   pip install flask flask-cors requests opencv-python-headless
   ```

3. **Revisa los logs del API:**
   - El script `ejecutar_api_background.bat` muestra mensajes en la ventana
   - Si hay errores, aparecerán ahí

---

## 📝 **Notas Importantes**

- ✅ El API se ejecuta en segundo plano, no verás una ventana
- ✅ El API se reinicia automáticamente cada 60 segundos si se cae
- ✅ No necesitas hacer nada después de configurarlo
- ✅ Funciona incluso si no hay usuario logueado (si se configuró como SYSTEM)

---

## 🎯 **Resumen**

1. **Ejecuta UNA VEZ:** `configurar_servicio_automatico.bat`
2. **Verifica:** `verificar_estado.bat`
3. **¡Listo!** El API se ejecutará automáticamente para siempre

**No necesitas hacer nada más.** El sistema se mantendrá funcionando automáticamente.
