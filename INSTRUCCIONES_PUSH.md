# 📤 Instrucciones para Hacer Push a GitHub

## ⚠️ **Problema**
Los comandos de git no están mostrando salida en el terminal automático.

## ✅ **Solución: Ejecutar Manualmente**

### **Opción 1: Usar el Script Batch (Recomendado)**

1. **Abre PowerShell o CMD**
2. **Ejecuta:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
   .\push_cambios.bat
   ```

3. **Sigue las instrucciones en pantalla**

---

### **Opción 2: Comandos Manuales Paso a Paso**

Abre **PowerShell** o **CMD** y ejecuta uno por uno:

```powershell
# 1. Ir a la carpeta del proyecto
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision

# 2. Verificar estado
git status

# 3. Agregar archivos modificados
git add src/config/api.js
git add backend/SOLUCION_FRONTEND_NO_FUNCIONA.md

# 4. Verificar qué se va a subir
git status

# 5. Hacer commit
git commit -m "Fix: Forzar uso de Railway siempre (puente NUC no tiene endpoints de camaras)"

# 6. Hacer push
git push
```

**Si el push falla, intenta:**
```powershell
git push origin main
```

**O si tu rama es `master`:**
```powershell
git push origin master
```

---

## 🔍 **Verificar que Funcionó**

### **1. Verificar en GitHub:**
1. Ve a tu repositorio en GitHub
2. Debe aparecer el último commit: "Fix: Forzar uso de Railway siempre..."

### **2. Verificar en Railway:**
1. Ve a Railway Dashboard
2. Debe aparecer un nuevo despliegue en progreso (amarillo) o completado (verde)

---

## 🚨 **Si Aparece Error de Autenticación**

Si te pide usuario/contraseña:

1. **Usa un Personal Access Token** (no tu contraseña de GitHub)
2. **O configura SSH** si ya lo tienes

**Para crear un Personal Access Token:**
1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Selecciona permisos: `repo`
4. Copia el token y úsalo como contraseña cuando git lo pida

---

## 📝 **Archivos que se Subirán**

- ✅ `src/config/api.js` - Configuración actualizada para usar Railway
- ✅ `backend/SOLUCION_FRONTEND_NO_FUNCIONA.md` - Guía de solución

---

## ✅ **Después del Push**

1. **Espera 2-3 minutos** para que Railway detecte los cambios
2. **Verifica en Railway** que el despliegue esté activo
3. **Recarga tu aplicación web** con `Ctrl + Shift + R` (sin caché)
4. **Verifica en la consola** (`F12`) que use Railway

---

**© 2025 AppTelink Vision**
