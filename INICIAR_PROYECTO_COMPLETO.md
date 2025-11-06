# Iniciar Proyecto Completo
## Frontend + Backend - Retail Analytics
## Hackatón 2025 - FUP

---

## 🚀 **INICIO RÁPIDO - 5 PASOS**

### **PASO 1: Preparar Backend**

```powershell
# Ir al directorio backend
cd BACKEND

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias (si no están)
pip install -r requirements.txt

# Migrar base de datos
python migrar_base_datos.py
# Escribe 's' para continuar

# Cargar datos
python cargar_datos.py
```

---

### **PASO 2: Iniciar Backend**

```powershell
# En el directorio BACKEND (misma terminal)
python main.py
```

Deberías ver:
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.
```

✅ **Backend corriendo en:** http://localhost:8000

---

### **PASO 3: Preparar Frontend**

**ABRIR NUEVA TERMINAL** (PowerShell)

```powershell
# Ir al directorio frontend
cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft\frontend

# Instalar dependencias (si no están)
npm install
```

---

### **PASO 4: Iniciar Frontend**

```powershell
# En el directorio frontend (segunda terminal)
npm run dev
```

Deberías ver:
```
VITE v... ready in ...ms
➜ Local:   http://localhost:5173/
```

✅ **Frontend corriendo en:** http://localhost:5173

---

### **PASO 5: Probar la Aplicación**

1. **Abre tu navegador:** http://localhost:5173

2. **Verás la página de login**

3. **Ingresa:**
   - Usuario: `admin`
   - Contraseña: `admin123`

4. **Click en "Iniciar Sesión"**

5. **¡Listo!** Verás el dashboard con todas las métricas

---

## 📊 **VERIFICAR QUE TODO FUNCIONA**

### **Backend:**
- ✅ http://localhost:8000 - Debe mostrar info de la API
- ✅ http://localhost:8000/docs - Documentación Swagger
- ✅ http://localhost:8000/health - {"status": "healthy"}

### **Frontend:**
- ✅ http://localhost:5173 - Página de login
- ✅ http://localhost:5173/dashboard - Dashboard (requiere login)

---

## 🖥️ **CONFIGURACIÓN DE TERMINALES**

### **Terminal 1 (Backend):**
```
C:\...\ANKASoft\BACKEND> python main.py
INFO: Uvicorn running on http://0.0.0.0:8000
```

### **Terminal 2 (Frontend):**
```
C:\...\ANKASoft\frontend> npm run dev
➜ Local: http://localhost:5173/
```

---

## 🔐 **USUARIOS DE PRUEBA**

| Usuario | Contraseña | Rol | Descripción |
|---------|------------|-----|-------------|
| admin | admin123 | ADMIN | Acceso total |
| gerente | gerente123 | GERENTE | Gestión |
| vendedor | vendedor123 | VENDEDOR | Lectura |

---

## ⚠️ **PROBLEMAS COMUNES**

### **Backend no inicia:**
```powershell
# Verificar puerto 8000 libre
netstat -ano | findstr :8000

# Si está ocupado, matar proceso o cambiar puerto
```

### **Frontend no inicia:**
```powershell
# Verificar puerto 5173 libre
netstat -ano | findstr :5173

# Reinstalar dependencias
rm -rf node_modules
npm install
```

### **Error de CORS:**
El backend ya tiene CORS configurado para `*`. Si hay problemas, verificar en `BACKEND/main.py`

### **Error 401 en peticiones:**
- Verificar que el backend esté corriendo
- Verificar que hiciste login correctamente
- Revisar consola del navegador (F12)

---

## 🐳 **ALTERNATIVA: CON DOCKER**

### **Opción A: Solo Backend**

```bash
cd BACKEND
docker-compose up -d
```

Backend en: http://localhost:8000  
Frontend manual: `npm run dev`

### **Opción B: Todo con Docker** (Avanzado)

Crear `docker-compose.yml` en raíz con ambos servicios.

---

## 📱 **FLUJO COMPLETO**

```
Usuario → http://localhost:5173 (Frontend React)
           ↓
        Página Login
           ↓
     Ingresa credenciales
           ↓
   POST http://localhost:8000/api/auth/login (Backend)
           ↓
     Recibe Token JWT
           ↓
   Guarda en localStorage
           ↓
     Redirige a /dashboard
           ↓
   GET http://localhost:8000/api/analytics/dashboard-resumen
           ↓
  Muestra métricas y gráficos
```

---

## 🎯 **PARA LA PRESENTACIÓN**

### **Demo en Vivo:**

1. **Mostrar login** (localhost:5173)
2. **Ingresar como admin**
3. **Ver dashboard cargando**
4. **Mostrar métricas:**
   - Ventas totales
   - Productos en stock
   - Alertas activas
5. **Mostrar productos destacados**
6. **Mostrar alertas de stock**
7. **Probar chatbot** (botón flotante)

### **Mencionar:**
- ✅ "Frontend en React con diseño moderno"
- ✅ "Conectado a backend con JWT"
- ✅ "Dashboard en tiempo real"
- ✅ "Chatbot integrado"

---

## ✅ **CHECKLIST PRE-PRESENTACIÓN**

- [ ] Backend corriendo (puerto 8000)
- [ ] Frontend corriendo (puerto 5173)
- [ ] Base de datos con datos cargados
- [ ] Usuarios creados (admin/gerente/vendedor)
- [ ] Login funciona
- [ ] Dashboard carga correctamente
- [ ] Métricas se muestran
- [ ] Sin errores en consola
- [ ] Internet disponible (opcional, para fuentes)

---

## 🔧 **DETENER SERVICIOS**

### **Backend:**
```
CTRL + C en la terminal del backend
```

### **Frontend:**
```
CTRL + C en la terminal del frontend
```

---

## 📝 **ARCHIVOS PRINCIPALES**

### **Backend:**
- `BACKEND/main.py` - Servidor FastAPI
- `BACKEND/routers/auth.py` - Login/Register
- `BACKEND/routers/analytics.py` - Endpoints datos

### **Frontend:**
- `frontend/app/routes/login.tsx` - Página login
- `frontend/app/routes/dashboard.tsx` - Dashboard
- `frontend/app/services/api.ts` - Conexión backend

---

## 🌐 **URLs IMPORTANTES**

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:5173 | Aplicación web |
| Backend API | http://localhost:8000 | API REST |
| Swagger Docs | http://localhost:8000/docs | Documentación |

---

## 🎉 **¡PROYECTO COMPLETO!**

Tienes:
- ✅ Backend con 18 endpoints
- ✅ Frontend con login y dashboard
- ✅ Autenticación JWT funcionando
- ✅ Diseño moderno y profesional
- ✅ Conexión Backend ↔ Frontend
- ✅ Chatbot integrado
- ✅ Listo para demostrar

---

**¡Todo funcionando! Frontend + Backend integrados.** 🎨🔌🚀

