# ✅ PASOS FINALES PARA EJECUTAR TODO
## Retail Analytics - Hackatón 2025

---

## 🚀 **EJECUTA ESTOS COMANDOS EN ORDEN**

### **TERMINAL BACKEND:**

```powershell
# 1. Ir al directorio BACKEND
cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft\BACKEND

# 2. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias necesarias
pip install python-jose[cryptography] email-validator

# 4. Migrar base de datos (agrega tabla usuarios)
python migrar_base_datos.py
# Escribe 's' cuando pregunte

# 5. Cargar datos (crea usuarios, productos, ventas)
python cargar_datos.py

# Deberías ver:
# ✅ 3 usuarios creados
#    - admin / admin123 (Rol: ADMIN)
#    - gerente / gerente123 (Rol: GERENTE)
#    - vendedor / vendedor123 (Rol: VENDEDOR)
# ✅ 4 sucursales creadas
# ✅ 300+ productos creados
# ✅ 500 ventas creadas

# 6. Iniciar el backend
python main.py

# Deberías ver:
# INFO: Uvicorn running on http://0.0.0.0:8000
# INFO: Application startup complete.
```

**DEJA ESTA TERMINAL ABIERTA** con el backend corriendo.

---

### **TERMINAL FRONTEND:**

Abre una **NUEVA terminal PowerShell**:

```powershell
# 1. Ir al directorio frontend
cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft\frontend

# 2. Iniciar el frontend
npm run dev

# Deberías ver:
# VITE v... ready in ...ms
# ➜ Local: http://localhost:5173/
```

**DEJA ESTA TERMINAL ABIERTA** con el frontend corriendo.

---

### **NAVEGADOR:**

1. **Abre:** http://localhost:5173

2. **Verás la página de login**

3. **Ingresa:**
   - Usuario: `admin`
   - Contraseña: `admin123`

4. **Click en "Iniciar Sesión"**

5. **¡Debería redirigir al dashboard!** ✅

---

## ⚠️ **SI AÚN SE QUEDA EN "PROCESANDO..."**

### **Verificar backend:**

```powershell
# En una tercera terminal
curl http://localhost:8000/health
```

**Debe responder:** `{"status":"healthy"}`

### **Verificar login:**

```powershell
curl -X POST "http://localhost:8000/api/auth/login-json" `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"admin\",\"password\":\"admin123\"}'
```

**Debe responder:** JSON con `access_token`

### **Ver errores en navegador:**

1. Presiona **F12** en el navegador
2. Ve a **Console**
3. Busca errores en rojo
4. Compártelos conmigo

---

## 📋 **CHECKLIST**

- [ ] Backend corriendo en http://localhost:8000
- [ ] Frontend corriendo en http://localhost:5173
- [ ] Base de datos migrada
- [ ] Usuarios creados (admin, gerente, vendedor)
- [ ] Productos y ventas cargados
- [ ] Sin errores en terminal backend
- [ ] Sin errores en terminal frontend

---

## ✅ **CUANDO TODO ESTÉ CORRIENDO**

Deberías tener:
- **Terminal 1:** Backend (python main.py)
- **Terminal 2:** Frontend (npm run dev)
- **Navegador:** http://localhost:5173 (página de login)

---

## 🎯 **RESUMEN**

```powershell
# Terminal 1 - Backend
cd BACKEND
.\venv\Scripts\Activate.ps1
pip install python-jose[cryptography] email-validator
python migrar_base_datos.py
python cargar_datos.py
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev

# Navegador
http://localhost:5173
Login: admin / admin123
```

---

**Ejecuta los comandos y avísame si funciona o qué error te sale.** 🔧✅

