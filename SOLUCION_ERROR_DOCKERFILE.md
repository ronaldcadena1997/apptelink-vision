# 🔧 Solución: Error "server_hikvision_style.py could not be found"

## ❌ **Error en Railway**
```
The executable `server_hikvision_style.py` could not be found.
```

---

## 🔍 **Causa**
Railway no encuentra el archivo `server_hikvision_style.py` en el contenedor Docker.

**Posibles causas:**
1. El Dockerfile no está copiando el archivo correctamente
2. El contexto de build está mal configurado en Railway
3. El archivo no está en el directorio correcto

---

## ✅ **SOLUCIONES**

### **Solución 1: Verificar configuración en Railway**

1. Ve a Railway → Tu proyecto → Settings
2. Verifica:
   - **Root Directory:** Debe estar vacío o ser `backend`
   - **Dockerfile Path:** `backend/Dockerfile.hikvision` o `Dockerfile.hikvision`
   - **Build Command:** (vacío)
   - **Start Command:** (vacío)

**Si el Root Directory está vacío:**
- El Dockerfile debe estar en la raíz del proyecto
- O cambia Root Directory a `backend`

**Si el Root Directory es `backend`:**
- El Dockerfile debe estar en `backend/`
- El Dockerfile Path debe ser `Dockerfile.hikvision`

---

### **Solución 2: Mover Dockerfile a la raíz (Alternativa)**

Si Railway está configurado para usar la raíz del proyecto:

1. **Copia el Dockerfile a la raíz:**
   ```powershell
   copy backend\Dockerfile.hikvision Dockerfile.hikvision
   ```

2. **Modifica el Dockerfile para que copie desde backend:**
   ```dockerfile
   # Copiar desde backend
   COPY backend/requirements.txt .
   COPY backend/server_hikvision_style.py .
   COPY backend/config.py .
   # ... otros archivos necesarios
   ```

3. **En Railway, cambia:**
   - Dockerfile Path: `Dockerfile.hikvision`
   - Root Directory: (vacío)

---

### **Solución 3: Verificar que el archivo está en Git**

```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
git ls-files backend/server_hikvision_style.py
```

**Si no aparece:**
- El archivo no está en Git
- Agrégalo: `git add backend/server_hikvision_style.py`

---

### **Solución 4: Usar Dockerfile en la raíz con contexto backend**

Crea un `Dockerfile` en la raíz del proyecto:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN pip install --upgrade pip

# Copiar requirements y archivos desde backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos del backend
COPY backend/server_hikvision_style.py .
COPY backend/config.py .

# Verificar que el archivo existe
RUN ls -la /app/server_hikvision_style.py

EXPOSE 8080

CMD ["python", "server_hikvision_style.py"]
```

**En Railway:**
- Root Directory: (vacío)
- Dockerfile Path: `Dockerfile`

---

## 📋 **Checklist**

- [ ] El archivo `server_hikvision_style.py` existe en `backend/`
- [ ] El archivo está en Git (`git ls-files backend/server_hikvision_style.py`)
- [ ] Railway está configurado con el Dockerfile correcto
- [ ] Root Directory está configurado correctamente
- [ ] Dockerfile Path apunta al archivo correcto

---

## 🆘 **Si Aún No Funciona**

1. **Verifica en Railway → Settings:**
   - Root Directory
   - Dockerfile Path
   - Build Command

2. **Verifica que el archivo está en Git:**
   ```powershell
   git ls-files | findstr server_hikvision_style
   ```

3. **Prueba crear un Dockerfile simple en la raíz** (Solución 4)

---

**¡Con estas soluciones deberías poder resolver el error de Dockerfile!** 🔧
