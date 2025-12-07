# 🔧 Corregir Auth Key de Tailscale

## 🚨 Problema Detectado

**Tu variable `TAILSCALE_AUTHKEY` tiene el valor incorrecto:**

```
tskey-api-kXk3Krqx2P11CNTRL-uhYm91JvC1FLXC6AC8TezE8axL4yA7ntg
```

**El problema:**
- ❌ Empieza con `tskey-api-` (esta es una **API key**, no una **Auth key**)
- ✅ Debe empezar con `tskey-auth-` (esta es una **Auth key** para autenticar dispositivos)

**Las API keys (`tskey-api-`) son para usar la API de Tailscale, NO para autenticar dispositivos.**

---

## ✅ Solución: Generar una Nueva Auth Key

### **Paso 1: Generar Auth Key en Tailscale**

1. **Ve a:** https://login.tailscale.com/admin/settings/keys

2. **Haz clic en "Generate auth key..."** (NO uses "API access tokens")

3. **Configura:**
   - **Reusable:** ✅ Sí
   - **Ephemeral:** ❌ No
   - **Expiration:** 90 días

4. **Haz clic en "Generate key"**

5. **⚠️ COPIA EL VALOR COMPLETO** (debe empezar con `tskey-auth-`)
   - Solo se muestra una vez
   - Guárdalo en un lugar seguro
   - Ejemplo: `tskey-auth-xxxxx-xxxxx`

---

### **Paso 2: Actualizar Variable en Railway**

1. **Ve a Railway Dashboard:**
   - https://railway.app
   - Selecciona tu proyecto de **backend**

2. **Abre la pestaña "Variables"**

3. **Edita la variable `TAILSCALE_AUTHKEY`**

4. **Reemplaza el valor:**
   - ❌ Valor actual: `tskey-api-...` (elimínalo)
   - ✅ Nuevo valor: `tskey-auth-...` (el que copiaste en el Paso 1)

5. **Haz clic en "Save" o el ícono de checkmark (✓)**

6. **Railway se redesplegará automáticamente** (puede tardar 2-3 minutos)

---

## ✅ Paso 3: Verificar que Funciona

**Después de actualizar la variable, Railway se redesplegará. En los logs, busca:**

### ✅ Si Funciona Correctamente:

```
==========================================
Iniciando Tailscale en Railway
==========================================
[1/3] Iniciando Tailscale daemon...
[2/3] Conectando a Tailscale con authkey...
[3/3] Verificando conexión de Tailscale...
✅ Tailscale conectado. IP: 100.xx.xx.xx
==========================================
Iniciando servidor Python
==========================================
```

**Si ves esto:** ✅ Tailscale está funcionando

---

## 🔍 Diferencia Entre Auth Key y API Key

### **Auth Key (`tskey-auth-...`):**
- ✅ Para autenticar dispositivos en la red Tailscale
- ✅ Es lo que necesitas para Railway
- ✅ Se genera en: Admin Console → Settings → Keys → "Generate auth key..."

### **API Key (`tskey-api-...`):**
- ❌ Para usar la API de Tailscale (programación)
- ❌ NO sirve para autenticar dispositivos
- ❌ Se genera en: Admin Console → Settings → Keys → "API access tokens"

---

## 📋 Checklist

- [ ] ✅ Generaste una nueva **Auth key** (empieza con `tskey-auth-`)
- [ ] ✅ Copiaste el valor completo de la auth key
- [ ] ✅ Actualizaste la variable `TAILSCALE_AUTHKEY` en Railway
- [ ] ✅ El nuevo valor empieza con `tskey-auth-` (NO `tskey-api-`)
- [ ] ✅ Railway se redesplegó después de actualizar la variable
- [ ] ✅ Logs muestran "Iniciando Tailscale en Railway"
- [ ] ✅ Logs muestran "Tailscale conectado. IP: 100.xx.xx.xx"

---

## 🎯 Siguiente Acción

**Ahora mismo:**

1. ✅ **Ve a Tailscale Admin Console → Settings → Keys**
2. ✅ **Haz clic en "Generate auth key..."** (NO "API access tokens")
3. ✅ **Configura: Reusable ✅, Ephemeral ❌, 90 días**
4. ✅ **Copia el valor completo** (empieza con `tskey-auth-`)
5. ✅ **Actualiza la variable en Railway** con el nuevo valor
6. ✅ **Espera a que Railway se redesplegue**
7. ✅ **Revisa los logs para ver los mensajes de Tailscale**

---

## ⚠️ Importante

**NO uses:**
- ❌ `tskey-api-...` (API key - no funciona para autenticar dispositivos)
- ❌ Solo el ID de la key (ej: `kq9X3n6tJ211CNTRL`)

**SÍ usa:**
- ✅ `tskey-auth-...` (Auth key - para autenticar dispositivos)
