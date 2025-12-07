# 🚀 Instrucciones: Iniciar Todo en el NUC

## 📋 Script Completo

**He creado el script `iniciar_todo_nuc.bat` que hace TODO automáticamente:**

1. ✅ **Verifica Tailscale** - Si no está corriendo, lo inicia
2. ✅ **Verifica el puente genérico** - Si no está corriendo, lo inicia
3. ✅ **Verifica el firewall** - Crea la regla si no existe
4. ✅ **Verifica conectividad** - Prueba que todo funcione

---

## 🎯 Cómo Usar

### **Opción 1: Ejecutar Manualmente (Una Vez)**

**Ejecuta:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\iniciar_todo_nuc.bat
```

**El script:**
- Verificará Tailscale e iniciará si es necesario
- Verificará el puente genérico e iniciará si es necesario
- Verificará el firewall y creará regla si es necesario
- Te mostrará un resumen de todo

---

### **Opción 2: Configurar Inicio Automático**

**Para que se ejecute automáticamente al iniciar Windows:**

1. **Ejecuta una vez:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   .\configurar_inicio_automatico.bat
   ```

2. **Esto configurará `ejecutar_puente_silencioso.bat` para iniciar automáticamente**

3. **O puedes modificar la tarea programada para usar `iniciar_todo_nuc.bat`**

---

## ✅ Qué Hace el Script

### **1. Verifica e Inicia Tailscale**

- ✅ Verifica si `tailscaled.exe` está corriendo
- ✅ Si no está, lo inicia automáticamente
- ✅ Espera a que se conecte (15 segundos)
- ✅ Verifica que tenga IP de Tailscale (debe empezar con `100.`)
- ✅ Muestra la IP de Tailscale

---

### **2. Verifica e Inicia el Puente Genérico**

- ✅ Verifica si el puerto 5000 está en uso
- ✅ Si no está, inicia el puente genérico
- ✅ Verifica que responda en `http://localhost:5000/api/status`
- ✅ Si no responde, reinicia el puente

---

### **3. Verifica el Firewall**

- ✅ Verifica si existe regla de firewall para puerto 5000
- ✅ Si no existe, intenta crearla automáticamente
- ✅ Si requiere admin, te indica que ejecutes `abrir_firewall_como_admin.bat`

---

### **4. Verificación Final**

- ✅ Muestra resumen de Tailscale (IP)
- ✅ Muestra resumen del puente (estado)
- ✅ Muestra configuración para Railway

---

## 📋 Resumen del Script

**El script `iniciar_todo_nuc.bat` hace:**

```
[1/3] Verificando Tailscale...
  ✅ Tailscale está corriendo
  ✅ IP de Tailscale: 100.92.50.72

[2/3] Verificando puente genérico del NUC...
  ✅ Puente genérico está corriendo
  ✅ El puente responde correctamente

[3/3] Verificación final...
  ✅ Tailscale IP: 100.92.50.72
  ✅ Puente genérico responde en http://localhost:5000
  ✅ Puente accesible desde Tailscale IP: http://100.92.50.72:5000

CONFIGURACIÓN PARA RAILWAY:
  NUC_URLS=nuc_sede1:http://100.92.50.72:5000
  CAMARAS_IPS=192.168.60.65
```

---

## 🔧 Si Algo Falla

### **Si Tailscale no se inicia:**

1. **Verifica que Tailscale esté instalado:**
   ```powershell
   tailscale version
   ```

2. **Si no está instalado, instálalo:**
   - Descarga desde: https://tailscale.com/download
   - Instala y ejecuta `tailscale up`

---

### **Si el puente no se inicia:**

1. **Verifica que Python esté instalado:**
   ```powershell
   python --version
   ```

2. **Verifica que las dependencias estén instaladas:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   pip install flask flask-cors requests opencv-python-headless
   ```

3. **Verifica que el archivo exista:**
   ```powershell
   dir puente_generico_nuc.py
   ```

---

### **Si el firewall bloquea:**

1. **Ejecuta como administrador:**
   ```powershell
   cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
   .\abrir_firewall_como_admin.bat
   ```

2. **O manualmente:**
   - Abre "Firewall de Windows Defender"
   - Crea regla de entrada para puerto 5000 TCP

---

## 🎯 Uso Recomendado

**Para uso diario:**

1. **Ejecuta `iniciar_todo_nuc.bat` una vez al día** (o cuando reinicies el NUC)
2. **O configura inicio automático** para que se ejecute al iniciar Windows

**El script verifica e inicia todo automáticamente, así que solo necesitas ejecutarlo una vez.**

---

## ✅ Checklist Final

Después de ejecutar el script, verifica:

- [ ] ✅ Tailscale está corriendo y tiene IP (100.xx.xx.xx)
- [ ] ✅ Puente genérico está corriendo en puerto 5000
- [ ] ✅ Puente responde en `http://localhost:5000/api/status`
- [ ] ✅ Puente accesible desde Tailscale IP
- [ ] ✅ Firewall permite conexiones en puerto 5000

**Si todo está ✅, el API del NUC está funcional y Railway puede conectarse.**

---

## 🚀 Ejecutar Ahora

**Ejecuta:**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
.\iniciar_todo_nuc.bat
```

**El script hará todo automáticamente.**
