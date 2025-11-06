# 🚀 DESPLIEGUE COMPLETO DEL PROYECTO - GUÍA PASO A PASO

---

## 🎯 **ARQUITECTURA DE DESPLIEGUE**

```
┌─────────────────┐
│  VERCEL         │  ← Frontend (React)
│  (Frontend)     │     URL: https://tu-app.vercel.app
└────────┬────────┘
         │
         ↓ API Calls
┌─────────────────┐
│  RENDER         │  ← Backend (FastAPI)
│  (Backend)      │     URL: https://tu-api.onrender.com
└────────┬────────┘
         │
         ↓ Conexión DB
┌─────────────────┐
│  RENDER         │  ← Base de Datos (PostgreSQL)
│  (PostgreSQL)   │     Incluido en Render
└─────────────────┘
```

---

## 📋 **REQUISITOS PREVIOS**

1. ✅ Cuenta en GitHub (ya tienes el código subido)
2. ✅ Cuenta en Render: https://render.com (gratis)
3. ✅ Cuenta en Vercel: https://vercel.com (gratis)

---

## 🗄️ **PASO 1: DESPLEGAR BASE DE DATOS (Render PostgreSQL)**

### **1.1. Crear Base de Datos:**

1. Ve a: https://dashboard.render.com
2. Clic en **"New +"** → **"PostgreSQL"**
3. Configura:
   - **Name:** `retail-analytics-db`
   - **Database:** `retail_analytics`
   - **User:** `retail_user`
   - **Region:** Oregon (US West) - Gratis
   - **PostgreSQL Version:** 16
   - **Plan:** Free

4. Clic en **"Create Database"**

5. **IMPORTANTE:** Copia estos datos (los necesitarás):
   - **Internal Database URL:** `postgresql://retail_user:...@...`
   - **External Database URL:** `postgresql://retail_user:...@...`

---

## 🔧 **PASO 2: DESPLEGAR BACKEND (Render Web Service)**

### **2.1. Preparar el código del Backend:**

Primero, actualiza el archivo `BACKEND/requirements.txt` para producción:

```txt
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
sqlalchemy>=2.0.36
psycopg2-binary>=2.9.9
pydantic>=2.10.0
python-dotenv>=1.0.1
python-multipart>=0.0.12
python-jose[cryptography]>=3.3.0
gunicorn>=21.2.0
```

### **2.2. Crear Web Service en Render:**

1. En Render, clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub: `Erick6485/ANKASoft`
3. Configura:
   - **Name:** `retail-analytics-api`
   - **Region:** Oregon (US West)
   - **Branch:** `backend`
   - **Root Directory:** `BACKEND`
   - **Runtime:** Python 3
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** Free

4. **Variables de Entorno** (Environment Variables):
   ```
   DATABASE_URL = [Pega aquí el Internal Database URL de tu PostgreSQL]
   SECRET_KEY = clave_secreta_hackaton_2025_fup
   JWT_SECRET_KEY = clave_secreta_hackaton_2025_fup
   JWT_ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   DEBUG = False
   ```

5. Clic en **"Create Web Service"**

6. **Espera 5-10 minutos** mientras Render construye y despliega.

### **2.3. Cargar Datos en la Base de Datos:**

Una vez desplegado, ve a la consola de Render (Shell) y ejecuta:

```bash
python migrar_base_datos.py
python cargar_datos.py
```

O crea un archivo `BACKEND/init_db.py`:

```python
from database.connection import SessionLocal, engine
from database import models
from utils.data_loader import cargar_datos_ejemplo

# Crear tablas
models.Base.metadata.create_all(bind=engine)

# Cargar datos
db = SessionLocal()
cargar_datos_ejemplo(db)
db.close()

print("✅ Base de datos inicializada")
```

Y en el **Build Command** de Render:
```bash
pip install -r requirements.txt && python init_db.py
```

---

## 🎨 **PASO 3: DESPLEGAR FRONTEND (Vercel)**

### **3.1. Preparar el Frontend:**

Actualiza `frontend/app/services/api.ts`:

```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://retail-analytics-api.onrender.com';
```

### **3.2. Crear archivo de configuración `.env` en frontend:**

```
REACT_APP_API_URL=https://retail-analytics-api.onrender.com
```

### **3.3. Desplegar en Vercel:**

**Opción A - Desde GitHub:**

1. Ve a: https://vercel.com/new
2. Importa tu repositorio: `Erick6485/ANKASoft`
3. Configura:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

4. **Environment Variables:**
   ```
   REACT_APP_API_URL = https://retail-analytics-api.onrender.com
   ```

5. Clic en **"Deploy"**

**Opción B - Desde CLI:**

```powershell
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

---

## 🔌 **PASO 4: CONFIGURAR CORS EN EL BACKEND**

Actualiza `BACKEND/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-app.vercel.app",  # ← Cambia por tu URL de Vercel
        "http://localhost:5173"  # Para desarrollo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Luego haz commit y push:

```powershell
git add BACKEND/main.py
git commit -m "fix: Actualizar CORS para producción"
git push origin backend
```

Render redesplegará automáticamente.

---

## ✅ **VERIFICACIÓN FINAL**

### **Backend:**
1. Ve a: `https://retail-analytics-api.onrender.com/docs`
2. ¿Ves Swagger UI? → ✅ Backend funcionando

### **Frontend:**
1. Ve a: `https://tu-app.vercel.app`
2. Login: `admin` / `admin123`
3. ¿Ves el dashboard? → ✅ Frontend funcionando

### **Conexión:**
1. En el frontend, abre la consola (F12)
2. Ve a la pestaña "Network"
3. ¿Ves peticiones a `.onrender.com`? → ✅ Conectado

---

## 🚨 **PROBLEMAS COMUNES**

### **Error: "Internal Server Error" en Backend**

**Solución:**
- Revisa los logs en Render Dashboard
- Verifica que `DATABASE_URL` esté configurada
- Ejecuta `python migrar_base_datos.py` en la consola

### **Error: "CORS policy" en Frontend**

**Solución:**
- Actualiza `allow_origins` en `main.py`
- Agrega tu URL de Vercel
- Haz push y espera redespliegue

### **Error: "Cannot connect to database"**

**Solución:**
- Verifica que usaste el **Internal Database URL**
- No uses el External (ese es para conexiones externas)

---

## 💰 **COSTOS (TODO GRATIS)**

| Servicio | Plan | Costo | Límites |
|----------|------|-------|---------|
| **Render Backend** | Free | $0/mes | 750 hrs/mes, sleep después de 15 min inactivo |
| **Render PostgreSQL** | Free | $0/mes | 1 GB, expira en 90 días |
| **Vercel Frontend** | Hobby | $0/mes | 100 GB bandwidth/mes |

**Total:** $0/mes ✅

---

## ⚡ **DESPLIEGUE RÁPIDO (ALTERNATIVA)**

Si quieres algo más rápido para la hackatón:

### **Railway (Todo en uno):**

1. Ve a: https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Selecciona tu repo
4. Railway detecta automáticamente Python y Node.js
5. Configura variables de entorno
6. ¡Listo en 5 minutos!

---

## 📝 **CHECKLIST DE DESPLIEGUE**

- [ ] Base de datos PostgreSQL creada en Render
- [ ] DATABASE_URL copiada
- [ ] Backend desplegado en Render
- [ ] Variables de entorno configuradas
- [ ] Datos cargados (migrar + cargar_datos)
- [ ] Backend accesible en /docs
- [ ] Frontend desplegado en Vercel
- [ ] API_URL actualizada en frontend
- [ ] CORS configurado correctamente
- [ ] Login funciona en producción
- [ ] Todos los dashboards cargan datos

---

## 🎯 **URLs FINALES**

Después del despliegue tendrás:

- **Frontend:** https://ankasoft.vercel.app
- **Backend API:** https://retail-analytics-api.onrender.com
- **Swagger Docs:** https://retail-analytics-api.onrender.com/docs

---

**¡Listo para la hackatón!** 🏆🚀✨

**Siguiente paso:** Sigue las instrucciones paso a paso o dime qué servicio prefieres usar.

