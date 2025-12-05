# 📋 Mi Configuración - Resumen Rápido

## 🔑 **Información de Red**

### **Tailscale:**
- **IP de Tailscale:** `100.92.50.72`
- **Hostname:** `desktop-9chgoud`
- **Usuario:** `ronaldalfredocadenamoran@`

### **Red Local:**
- **IP del NUC:** `192.168.60.8`
- **Gateway:** `192.168.60.1`
- **Red local:** `192.168.60.x`
- **SSID Wi-Fi:** `AppInvitados`
- **Protocolo:** Wi-Fi 5 (802.11ac)

### **Cámara:**
- **IP de cámara:** `192.168.60.65`
- **Puerto HTTP:** `80`
- **Puerto SDK:** `8000`
- **Subnet Mask:** `255.255.255.0`
- **Gateway:** `192.168.60.1`
- **Serial No:** `DS-2CD1047G2H-LIU20250319AA`
- **Short Serial:** `FX6269211`

---

## ⚙️ **Configuración para Railway**

### **Variables de Entorno en Railway:**

```
NUC_URLS=nuc_sede1:http://100.92.50.72:5000
CAMARAS_IPS=192.168.60.65
```

### **Si usas config.py:**

```python
NUCs_CONFIG = {
    'nuc_sede1': {
        'tailscale_ip': '100.92.50.72',
        'puerto': 5000,
        'nombre': 'NUC Principal',
        'red_local': '192.168.60'
    },
}

CAMARAS_CONFIG = [
    {'ip': '192.168.60.65', 'nombre': 'Cámara Principal', 'nuc': 'nuc_sede1'},
]
```

---

## ✅ **Comandos Rápidos**

### **Verificar Tailscale:**
```powershell
tailscale status
tailscale ip -4
```

### **Ejecutar Puente Genérico:**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
python puente_generico_nuc.py
```

### **Verificar que el puente funciona:**
```powershell
curl http://localhost:5000/api/status
```

---

## 🔧 **Configuración del Puente Genérico**

**Archivo:** `puente_generico_nuc.py`

**Línea 25:**
```python
RED_LOCAL = "192.168.60"  # ✅ Ya está correcto
```

---

## 📝 **Notas Importantes**

1. ✅ **Tailscale IP:** `100.92.50.72` - Esta es la IP que Railway necesita para conectarse al NUC
2. ✅ **Red local:** `192.168.60.x` - Todas tus cámaras están en esta red
3. ✅ **Cámara:** `192.168.60.65` - Esta es la IP de tu cámara configurada
4. ✅ **Puente genérico:** Debe correr en el puerto `5000` en el NUC

---

## 🚀 **Próximos Pasos**

1. ✅ Verificar Tailscale está corriendo
2. ✅ Configurar `RED_LOCAL = "192.168.60"` en `puente_generico_nuc.py`
3. ✅ Ejecutar el puente genérico
4. ✅ Configurar Railway con:
   - `NUC_URLS=nuc_sede1:http://100.92.50.72:5000`
   - `CAMARAS_IPS=192.168.60.65`
5. ✅ Verificar que todo funciona

---

**Última actualización:** 2025-01-04
