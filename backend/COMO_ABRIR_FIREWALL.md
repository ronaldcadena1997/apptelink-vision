# 🔥 Cómo Abrir el Firewall (Solución al Error de Permisos)

## 🚨 Problema

El script `.bat` no puede crear la regla de firewall aunque ejecutes como administrador porque necesita ejecutar comandos de PowerShell con permisos elevados.

---

## ✅ Solución: 3 Opciones

### **Opción 1: Script Automático (Más Fácil)**

**Ejecuta este archivo haciendo doble clic:**

```
abrir_firewall_como_admin.bat
```

Este script:
- ✅ Solicita permisos de administrador automáticamente
- ✅ Ejecuta PowerShell con los permisos necesarios
- ✅ Crea la regla de firewall

**Si aparece UAC (Control de Cuentas de Usuario):**
- Haz clic en **"Sí"** para permitir

---

### **Opción 2: PowerShell Manual (Recomendado)**

**Pasos:**

1. **Abre PowerShell como Administrador:**
   - Presiona `Windows + X`
   - Selecciona **"Windows PowerShell (Administrador)"** o **"Terminal (Administrador)"**
   - O busca "PowerShell" en el menú Inicio → Click derecho → **"Ejecutar como administrador"**

2. **Navega a la carpeta:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   ```

3. **Ejecuta el script:**
   ```powershell
   .\abrir_firewall_ps1.ps1
   ```

4. **Si aparece un error de política de ejecución:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Luego vuelve a ejecutar el script.

---

### **Opción 3: Comando Directo (Más Rápido)**

**En PowerShell como Administrador:**

```powershell
New-NetFirewallRule -DisplayName "Puente Genérico NUC" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

**Verificar que se creó:**
```powershell
Get-NetFirewallRule -DisplayName "Puente Genérico NUC"
```

---

## 🔍 Verificar que Funcionó

**Después de ejecutar cualquiera de las opciones, verifica:**

```powershell
# Ver la regla creada
Get-NetFirewallRule -DisplayName "Puente Genérico NUC" | Select-Object DisplayName, Enabled, Direction, Action
```

**Debe mostrar:**
- `DisplayName: Puente Genérico NUC`
- `Enabled: True`
- `Direction: Inbound`
- `Action: Allow`

---

## 🚨 Si Aún No Funciona

### **Problema: "No se puede ejecutar scripts"**

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problema: "Acceso denegado"**

**Solución:**
1. Asegúrate de que PowerShell esté ejecutándose como Administrador
2. Verifica que tu cuenta tenga permisos de administrador
3. Intenta ejecutar el comando directamente en PowerShell (Opción 3)

---

## 📋 Resumen Rápido

**La forma más fácil:**

1. Doble clic en: `abrir_firewall_como_admin.bat`
2. Click en **"Sí"** cuando aparezca UAC
3. Listo ✅

---

## ✅ Después de Abrir el Firewall

Una vez que el firewall esté abierto:

1. **Verifica que el puente esté corriendo:**
   ```powershell
   netstat -ano | findstr :5000
   ```

2. **Prueba la conectividad desde la IP de Tailscale:**
   ```powershell
   curl http://100.92.50.72:5000/api/status
   ```

3. **Si funciona:** Railway debería poder conectarse ahora.

---

## 🔗 Archivos Relacionados

- `abrir_firewall_como_admin.bat` - Script automático que solicita permisos
- `abrir_firewall_ps1.ps1` - Script PowerShell que crea la regla
- `solucion_rapida_502.bat` - Solución completa (incluye abrir firewall)
