# 🚀 Guía: Inicio Automático del Puente Genérico

## 🎯 **Objetivo**
Configurar el puente genérico para que se ejecute automáticamente cuando el NUC se reinicia, sin necesidad de intervención manual.

---

## ✅ **Método 1: Tarea Programada (Recomendado)**

### **Ventajas:**
- ✅ Se ejecuta automáticamente al iniciar Windows
- ✅ Funciona incluso si no hay usuario logueado (opcional)
- ✅ Más confiable y robusto
- ✅ Fácil de gestionar desde el Panel de Control

### **Pasos:**

1. **Ejecuta el script de configuración (UNA SOLA VEZ):**
   
   **Opción A - Desde PowerShell (Recomendado):**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   .\configurar_inicio_automatico.bat
   ```
   
   **Opción B - Doble clic:**
   - Haz doble clic en `configurar_inicio_automatico.bat`
   
   **Opción C - Completamente silencioso (sin ventanas):**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   .\configurar_inicio_automatico_silencioso.bat
   ```
   
   **✅ El script se ejecutará automáticamente como administrador** - Solo necesitas ejecutarlo UNA VEZ. Después de eso, el puente se iniciará automáticamente cada vez que reinicies el NUC.
   
   **⚠️ Nota:** Si aparece el UAC (Control de cuentas de usuario), solo necesitas aceptar UNA VEZ. Después de eso, todo funcionará automáticamente.

2. **Verificar que se creó:**
   - Presiona `Windows + R`
   - Escribe: `taskschd.msc` y presiona Enter
   - Busca la tarea: `PuenteGenericoNUC`

---

## ✅ **Método 2: Carpeta de Inicio (Alternativa Simple)**

### **Ventajas:**
- ✅ Muy simple de configurar
- ✅ No requiere permisos de administrador
- ✅ Se ejecuta cuando el usuario inicia sesión

### **Pasos:**

1. **Presiona `Windows + R`**

2. **Escribe:**
   ```
   shell:startup
   ```
   Y presiona Enter

3. **Copia el archivo `ejecutar_puente_inicio.bat`** a esa carpeta

4. **Listo** - Se ejecutará automáticamente al iniciar sesión

---

## ✅ **Método 3: Servicio de Windows (Avanzado)**

Para ejecutar como servicio de Windows (más profesional, pero más complejo):

### **Usando NSSM (Non-Sucking Service Manager):**

1. **Descarga NSSM:**
   - Ve a: https://nssm.cc/download
   - Descarga la versión para Windows 64-bit

2. **Extrae y ejecuta:**
   ```powershell
   # Como Administrador
   nssm install PuenteGenericoNUC
   ```

3. **Configura:**
   - **Path:** `C:\Python311\python.exe` (o tu ruta de Python)
   - **Startup directory:** `C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend`
   - **Arguments:** `puente_generico_nuc.py`

4. **Inicia el servicio:**
   ```powershell
   nssm start PuenteGenericoNUC
   ```

---

## 🔧 **Verificar que Funciona**

### **1. Verificación Rápida (Script):**

Ejecuta el script de verificación:
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
.\verificar_servicios.bat
```

Este script verifica:
- ✅ Si Tailscale está corriendo
- ✅ Si Tailscale tiene IP asignada
- ✅ Si el puente genérico está corriendo
- ✅ Si el puente responde correctamente

### **2. Reiniciar el NUC:**
```powershell
# Reiniciar ahora
shutdown /r /t 0
```

### **3. Después del reinicio, verificar:**

**Opción A - Script de verificación:**
```powershell
.\verificar_servicios.bat
```

**Opción B - Desde PowerShell:**
```powershell
# Verificar Tailscale
tailscale status
tailscale ip -4

# Verificar puente
netstat -ano | findstr :5000
curl http://localhost:5000/api/status
```

**Opción C - Desde navegador:**
```
http://localhost:5000/api/status
```

Deberías ver:
```json
{
  "status": "online",
  "tipo": "puente_generico",
  "red_local": "192.168.60"
}
```

---

## 🚨 **Troubleshooting**

### **Problema: "El puente no se inicia automáticamente"**

**Solución 1:** Verificar que la tarea programada existe
```powershell
schtasks /Query /TN "PuenteGenericoNUC"
```

**Solución 2:** Verificar los logs de la tarea
- Abre "Tareas programadas" (`taskschd.msc`)
- Busca `PuenteGenericoNUC`
- Haz clic derecho → "Ejecutar"
- Revisa el "Historial" para ver errores

**Solución 3:** Verificar que Python está en el PATH
```powershell
python --version
```

Si no funciona, usa la ruta completa en el script:
```batch
C:\Python311\python.exe puente_generico_nuc.py
```

### **Problema: "Se abre una ventana al iniciar"**

**Solución:** Usa `pythonw` en lugar de `python` en el script:
```batch
start /B pythonw puente_generico_nuc.py
```

`pythonw` ejecuta Python sin ventana de consola.

### **Problema: "El puente se cierra después de un tiempo"**

**Solución:** Agregar manejo de errores y reinicio automático:

Edita `ejecutar_puente_inicio.bat`:
```batch
:inicio
cd /d "C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend"
python puente_generico_nuc.py
timeout /t 5
goto inicio
```

Esto reiniciará el puente si se cierra.

---

## 🔄 **Eliminar Inicio Automático**

Si quieres desactivar el inicio automático:

1. **Ejecuta:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   .\eliminar_inicio_automatico.bat
   ```

2. **O manualmente:**
   - Abre "Tareas programadas" (`taskschd.msc`)
   - Busca `PuenteGenericoNUC`
   - Haz clic derecho → "Eliminar"

---

## 📋 **Archivos Creados**

1. **`ejecutar_puente_inicio.bat`** - Script que ejecuta el puente (con verificación de Tailscale)
2. **`ejecutar_puente_silencioso.bat`** - Versión silenciosa (sin ventanas, con verificación de Tailscale)
3. **`configurar_inicio_automatico.bat`** - Configura el inicio automático
4. **`eliminar_inicio_automatico.bat`** - Elimina el inicio automático
5. **`verificar_servicios.bat`** - Script para verificar manualmente el estado de Tailscale y el puente

---

## ✅ **Checklist de Configuración**

- [ ] Script `ejecutar_puente_inicio.bat` creado
- [ ] Ejecutado `configurar_inicio_automatico.bat`
- [ ] Tarea programada creada (verificar en `taskschd.msc`)
- [ ] Probado reiniciando el NUC
- [ ] Verificado que el puente se ejecuta automáticamente
- [ ] Verificado que responde en `http://localhost:5000/api/status`

---

## 🎯 **Recomendación Final**

**Usa el Método 1 (Tarea Programada)** porque:
- ✅ Es el más confiable
- ✅ Funciona incluso si no hay usuario logueado
- ✅ Fácil de gestionar
- ✅ Se puede configurar para reiniciar automáticamente si falla
- ✅ **Verifica automáticamente que Tailscale esté corriendo antes de iniciar el puente**
- ✅ **Reinicia el puente si Tailscale se desconecta**

## 🔄 **Funcionamiento Automático**

El script ahora verifica automáticamente:

1. **Tailscale:**
   - ✅ Verifica que el proceso `tailscaled.exe` esté corriendo
   - ✅ Verifica que Tailscale tenga una IP asignada (debe empezar con `100.`)
   - ✅ Si no está corriendo, intenta iniciarlo automáticamente
   - ✅ Espera hasta que Tailscale esté completamente funcional

2. **Puente Genérico:**
   - ✅ Verifica que el puerto 5000 esté en uso
   - ✅ Solo inicia el puente si Tailscale está funcionando
   - ✅ Verifica periódicamente que ambos sigan activos
   - ✅ Reinicia el puente si se cierra o si Tailscale se desconecta

**Orden de inicio:**
1. Verificar/iniciar Tailscale
2. Esperar a que Tailscale tenga IP
3. Verificar si el puente ya está corriendo
4. Si no está corriendo, iniciarlo
5. Verificar periódicamente ambos servicios

---

## 📝 **Configuración Avanzada (Opcional)**

### **Hacer que la tarea se ejecute incluso sin usuario logueado:**

1. Abre "Tareas programadas" (`taskschd.msc`)
2. Busca `PuenteGenericoNUC`
3. Haz clic derecho → "Propiedades"
4. Ve a la pestaña "General"
5. Marca: "Ejecutar tanto si el usuario ha iniciado sesión como si no"
6. Marca: "No almacenar contraseña"
7. Acepta

**Nota:** Esto requiere permisos de administrador.

---

## 🔐 **Seguridad**

El script se ejecuta con los permisos del usuario que inició sesión. Si necesitas más seguridad:

1. Crea un usuario específico para el puente
2. Configura la tarea para ejecutarse con ese usuario
3. Limita los permisos de ese usuario

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
