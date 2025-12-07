# 🔄 Resumen: Monitoreo Continuo de Servicios

## 🎯 **Funcionamiento del Monitoreo**

El sistema verifica **constantemente** que Tailscale y el puente genérico estén activos, incluso si el NUC no se reinicia.

---

## ⏱️ **Frecuencia de Verificación**

### **Cada 60 segundos (1 minuto):**

El script verifica:

1. **Tailscale:**
   - ✅ ¿El proceso `tailscaled.exe` está corriendo?
   - ✅ ¿Tailscale tiene una IP asignada?
   - ✅ ¿La IP es válida (empieza con `100.`)?

2. **Puente Genérico:**
   - ✅ ¿El puerto 5000 está en uso?
   - ✅ ¿El puente responde a peticiones HTTP? (prueba `/api/status`)

---

## 🔄 **Qué Hace si Detecta un Problema**

### **Si Tailscale se desconecta:**

1. **Detecta** que el proceso no está corriendo o no tiene IP
2. **Intenta reiniciar** Tailscale automáticamente
3. **Espera** hasta que Tailscale se reconecte y tenga IP válida
4. **Solo entonces** reinicia el puente genérico (si es necesario)

### **Si el Puente Genérico se cae:**

1. **Detecta** que el puerto 5000 no está en uso o no responde
2. **Mata** cualquier proceso de Python relacionado con el puente
3. **Espera** 5 segundos
4. **Reinicia** el puente genérico automáticamente

### **Si ambos están funcionando:**

- ✅ Continúa verificando cada minuto
- ✅ No hace nada, solo monitorea

---

## 📊 **Escenarios Cubiertos**

### **Escenario 1: NUC se reinicia**
- ✅ Tailscale se inicia automáticamente
- ✅ El puente se inicia automáticamente
- ✅ Verificación continua cada minuto

### **Escenario 2: Tailscale se desconecta (sin reiniciar NUC)**
- ✅ Detecta la desconexión en máximo 1 minuto
- ✅ Intenta reiniciar Tailscale
- ✅ Espera a que se reconecte
- ✅ Reinicia el puente si es necesario

### **Escenario 3: El puente se cae (sin reiniciar NUC)**
- ✅ Detecta que no responde en máximo 1 minuto
- ✅ Mata procesos relacionados
- ✅ Reinicia el puente automáticamente
- ✅ Verifica que Tailscale siga funcionando

### **Escenario 4: Ambos se desconectan**
- ✅ Detecta ambos problemas
- ✅ Primero restaura Tailscale
- ✅ Luego restaura el puente
- ✅ Continúa monitoreando

### **Escenario 5: Problema de red temporal**
- ✅ Detecta que Tailscale no tiene IP
- ✅ Espera a que se reconecte (hasta 30 segundos)
- ✅ Verifica periódicamente
- ✅ No reinicia el puente hasta que Tailscale esté listo

---

## 🔍 **Verificaciones Específicas**

### **Verificación de Tailscale:**

```batch
1. Proceso tailscaled.exe corriendo?
2. Comando "tailscale ip -4" funciona?
3. IP empieza con "100."?
```

**Si falla alguna:** Espera y reintenta hasta que funcione.

### **Verificación del Puente:**

```batch
1. Puerto 5000 en uso?
2. HTTP GET /api/status responde 200?
```

**Si falla alguna:** Mata procesos y reinicia.

---

## ⚡ **Tiempos de Respuesta**

| Evento | Tiempo de Detección | Acción |
|--------|---------------------|--------|
| **Tailscale se desconecta** | Máximo 60 segundos | Reiniciar Tailscale |
| **Puente se cae** | Máximo 60 segundos | Reiniciar puente |
| **Puente no responde** | Máximo 60 segundos | Reiniciar puente |
| **Ambos funcionan** | Cada 60 segundos | Solo verificar |

---

## 🛡️ **Protecciones Implementadas**

1. **Evita múltiples instancias:**
   - Verifica si el puente ya está corriendo antes de iniciarlo
   - Mata procesos antiguos antes de reiniciar

2. **Orden de inicio correcto:**
   - Primero verifica/inicia Tailscale
   - Solo después inicia el puente
   - No inicia el puente si Tailscale no está listo

3. **Reintentos automáticos:**
   - Si Tailscale no se conecta, espera y reintenta
   - Si el puente falla, lo reinicia automáticamente
   - No se da por vencido

4. **Verificación de salud:**
   - No solo verifica que el proceso esté corriendo
   - También verifica que responda correctamente (HTTP 200)

---

## 📝 **Logs y Monitoreo**

Para verificar manualmente el estado:

```powershell
# Verificar servicios
.\verificar_servicios.bat

# Ver procesos de Python
Get-Process python* | Where-Object {$_.Path -like "*proyectowebApptelinkVision*"}

# Ver puerto 5000
netstat -ano | findstr :5000

# Probar puente
curl http://localhost:5000/api/status
```

---

## ✅ **Resumen**

- ✅ **Verifica cada 60 segundos** que ambos servicios estén activos
- ✅ **Reinicia automáticamente** si detecta problemas
- ✅ **Funciona incluso si el NUC no se reinicia**
- ✅ **Mantiene el orden correcto:** Tailscale primero, luego puente
- ✅ **Verifica salud real:** No solo procesos, también respuestas HTTP

**El sistema es completamente autónomo y se auto-repara automáticamente.**

---

**© 2025 AppTelink Vision**  
**Versión 1.0.0**
