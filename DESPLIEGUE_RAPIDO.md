# 🚀 DESPLIEGUE RÁPIDO - 5 PASOS

---

## ✅ **OPCIÓN 1: RENDER + VERCEL (RECOMENDADO)**

### **Paso 1: Base de Datos (2 minutos)**
1. Ve a https://dashboard.render.com
2. New + → PostgreSQL
3. Name: `retail-analytics-db`, Plan: Free
4. Copia el **Internal Database URL**

### **Paso 2: Backend (5 minutos)**
1. En Render: New + → Web Service
2. Conecta GitHub: `Erick6485/ANKASoft`, rama `backend`
3. Root Directory: `BACKEND`
4. Build: `pip install -r requirements.txt && python init_db.py`
5. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Variables de entorno:
   ```
   DATABASE_URL = [pega tu Internal Database URL]
   SECRET_KEY = clave_secreta_hackaton_2025_fup
   JWT_SECRET_KEY = clave_secreta_hackaton_2025_fup
   JWT_ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   DEBUG = False
   ```
7. Create Web Service
8. **Espera 5-10 minutos**, copia tu URL: `https://retail-analytics-api-xxxxx.onrender.com`

### **Paso 3: Frontend (3 minutos)**
1. Ve a https://vercel.com/new
2. Importa GitHub: `Erick6485/ANKASoft`
3. Root Directory: `frontend`
4. Framework: Vite
5. Variables de entorno:
   ```
   VITE_API_URL = [pega la URL de tu backend de Render]
   VITE_API_KEY = retail_hackaton_2025_fup
   ```
6. Deploy
7. Copia tu URL: `https://ankasoft.vercel.app`

### **Paso 4: Configurar CORS (1 minuto)**

En `BACKEND/main.py` línea 27, actualiza:

```python
allow_origins=[
    "https://ankasoft.vercel.app",  # ← Cambia por tu URL de Vercel
    "http://localhost:5173"
],
```

Haz commit y push:
```powershell
git add BACKEND/main.py
git commit -m "fix: Actualizar CORS para Vercel"
git push origin backend
```

Render redesplegará automáticamente.

### **Paso 5: Probar (1 minuto)**
1. Abre tu URL de Vercel: `https://ankasoft.vercel.app`
2. Login: `admin` / `admin123`
3. ✅ ¡Listo!

---

## ✅ **OPCIÓN 2: RAILWAY (MÁS FÁCIL)**

Railway despliega todo automáticamente desde GitHub:

### **Pasos:**
1. Ve a https://railway.app
2. New Project → Deploy from GitHub
3. Selecciona `Erick6485/ANKASoft`
4. Railway detecta automáticamente:
   - Backend (Python/FastAPI)
   - Frontend (Node.js/Vite)
   - PostgreSQL
5. Agrega variables de entorno (Railway te preguntará)
6. ¡Listo en 5 minutos!

**Variables necesarias:**
```
SECRET_KEY = clave_secreta_hackaton_2025_fup
JWT_SECRET_KEY = clave_secreta_hackaton_2025_fup
JWT_ALGORITHM = HS256
```

Railway genera automáticamente `DATABASE_URL`.

---

## 🔍 **VERIFICACIÓN**

### ✅ Backend funcionando:
- Ve a: `https://tu-backend.onrender.com/docs`
- Deberías ver Swagger UI

### ✅ Frontend funcionando:
- Ve a: `https://tu-frontend.vercel.app`
- Login: `admin` / `admin123`

### ✅ Conexión:
- Abre el dashboard
- ¿Ves datos en los KPIs?
- ¿Las gráficas muestran información?

---

## 🚨 **PROBLEMAS COMUNES**

| Problema | Solución |
|----------|----------|
| Backend da error 500 | Revisa logs en Render, verifica DATABASE_URL |
| Frontend no conecta | Actualiza VITE_API_URL en Vercel, verifica CORS |
| "Database connection failed" | Usa Internal URL, no External URL |
| Backend se "duerme" | Normal en plan Free, tarda 30s en despertar |

---

## 💡 **TIPS PARA LA HACKATÓN**

1. **Despierta el backend antes de la demo:**
   - Abre `https://tu-backend.onrender.com/docs` 1 minuto antes
   - Espera que cargue completamente

2. **Ten un plan B:**
   - Graba un video de la demo
   - Ten screenshots listos

3. **URLs cortas:**
   - En Vercel/Render puedes personalizar dominios

---

## 📊 **ESTADO DEL DESPLIEGUE**

Después de completar, tendrás:

✅ Base de datos PostgreSQL (Render)  
✅ Backend FastAPI (Render)  
✅ Frontend React (Vercel)  
✅ 33+ endpoints funcionando  
✅ 9 páginas navegables  
✅ Dashboards con datos reales  

**Costo total:** $0/mes 🎉

---

## 🎯 **SIGUIENTE PASO**

Sigue la **OPCIÓN 1** (Render + Vercel) paso a paso.

**Tiempo estimado:** 15 minutos

**¿Listo para empezar?** 🚀

