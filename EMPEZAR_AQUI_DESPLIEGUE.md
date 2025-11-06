# 🎯 EMPEZAR AQUÍ - DESPLIEGUE EN 15 MINUTOS

---

## 📋 **CHECKLIST ANTES DE EMPEZAR**

- [x] ✅ Código subido a GitHub (rama `backend`)
- [x] ✅ Cuenta en Render (https://render.com - GRATIS)
- [x] ✅ Cuenta en Vercel (https://vercel.com - GRATIS)

---

## 🚀 **SIGUE ESTOS 5 PASOS**

---

### **📦 PASO 1: CREAR BASE DE DATOS (2 minutos)**

1. **Abre en tu navegador:** https://dashboard.render.com
2. Haz clic en: **"New +"** → **"PostgreSQL"**
3. Llena el formulario:
   ```
   Name: retail-analytics-db
   Database: retail_analytics
   User: retail_user
   Region: Oregon (US West)
   PostgreSQL Version: 16
   Plan: Free ← IMPORTANTE
   ```
4. Clic en: **"Create Database"**
5. **ESPERA 1 minuto** hasta que diga "Available"
6. En la página de tu base de datos, busca **"Internal Database URL"**
7. **COPIA TODA LA URL** (empieza con `postgresql://...`)
   ```
   Ejemplo:
   postgresql://retail_user:xyz123abc@dpg-abc123.oregon-postgres.render.com/retail_analytics
   ```
8. **PÉGALA EN NOTEPAD** - la necesitarás en el siguiente paso

✅ **Base de datos lista**

---

### **🔧 PASO 2: DESPLEGAR BACKEND (5 minutos)**

1. En Render, clic en: **"New +"** → **"Web Service"**
2. Clic en: **"Build and deploy from a Git repository"** → **"Next"**
3. **Conecta GitHub:**
   - Si no está conectado: **"Connect GitHub"**
   - Busca: `Erick6485/ANKASoft`
   - Clic en **"Connect"**

4. **Configura el servicio:**
   ```
   Name: retail-analytics-api
   Region: Oregon (US West)
   Branch: backend
   Root Directory: BACKEND
   Runtime: Python 3
   Build Command: pip install -r requirements.txt && python init_db.py
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free ← IMPORTANTE
   ```

5. **Variables de Entorno** (clic en "Advanced" → "Add Environment Variable"):
   
   **Agrega estas 6 variables:**
   ```
   DATABASE_URL = [PEGA AQUÍ LA URL QUE COPIASTE EN EL PASO 1]
   
   SECRET_KEY = clave_secreta_hackaton_2025_fup
   
   JWT_SECRET_KEY = clave_secreta_hackaton_2025_fup
   
   JWT_ALGORITHM = HS256
   
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   
   DEBUG = False
   ```

6. Clic en: **"Create Web Service"**

7. **ESPERA 5-10 MINUTOS** mientras Render:
   - Descarga el código
   - Instala dependencias
   - Crea la base de datos
   - Carga los datos de ejemplo
   - Inicia el servidor

8. **Cuando termine** (estado: "Live"), verás tu URL en la parte superior:
   ```
   Ejemplo:
   https://retail-analytics-api-xyz123.onrender.com
   ```
9. **COPIA ESTA URL** y pégala en Notepad

10. **PRUEBA:** Abre en tu navegador:
    ```
    https://retail-analytics-api-xyz123.onrender.com/docs
    ```
    ¿Ves Swagger UI? ✅ **Backend funcionando!**

---

### **🎨 PASO 3: DESPLEGAR FRONTEND (3 minutos)**

1. **Abre en tu navegador:** https://vercel.com/new
2. **Conecta GitHub:**
   - Clic en: **"Import Git Repository"**
   - Busca: `Erick6485/ANKASoft`
   - Clic en **"Import"**

3. **Configura el proyecto:**
   ```
   Project Name: ankasoft-retail
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: (dejar por defecto: npm run build)
   Output Directory: (dejar por defecto: dist)
   Install Command: (dejar por defecto: npm install)
   ```

4. **Variables de Entorno** (clic en "Environment Variables"):
   
   **Agrega estas 2 variables:**
   ```
   Name: VITE_API_URL
   Value: [PEGA AQUÍ LA URL DEL BACKEND DEL PASO 2]
   
   Name: VITE_API_KEY
   Value: retail_hackaton_2025_fup
   ```

5. Clic en: **"Deploy"**

6. **ESPERA 2-3 MINUTOS** mientras Vercel:
   - Instala dependencias
   - Compila el código
   - Despliega

7. **Cuando termine**, verás:
   ```
   🎉 Congratulations!
   
   Your project is live at:
   https://ankasoft-retail.vercel.app
   ```

8. **COPIA ESTA URL** y pégala en Notepad

---

### **🔗 PASO 4: CONECTAR FRONTEND CON BACKEND (1 minuto)**

**IMPORTANTE:** Ahora necesitamos permitir que el frontend se conecte al backend (CORS).

1. En tu computadora, abre el archivo: `BACKEND/main.py`
2. Busca la línea ~27 que dice `allow_origins=[`
3. Agrega tu URL de Vercel:
   ```python
   allow_origins=[
       "https://ankasoft-retail.vercel.app",  # ← TU URL DE VERCEL
       "http://localhost:5173"
   ],
   ```
4. **Guarda el archivo**
5. En PowerShell, ejecuta:
   ```powershell
   cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft
   git add BACKEND/main.py
   git commit -m "fix: Configurar CORS para Vercel"
   git push origin backend
   ```
6. **Render redesplegará automáticamente** (espera 2-3 minutos)

---

### **✅ PASO 5: PROBAR TODO (1 minuto)**

1. **Abre tu URL de Vercel:**
   ```
   https://ankasoft-retail.vercel.app
   ```

2. **Inicia sesión:**
   ```
   Usuario: admin
   Contraseña: admin123
   ```

3. **Prueba los dashboards:**
   - ✅ ¿Ves el dashboard principal?
   - ✅ ¿Los KPIs muestran números?
   - ✅ ¿Las gráficas tienen datos?
   - ✅ ¿Puedes navegar a "Ventas", "Inventario", etc.?

4. **Si TODO funciona:**
   ```
   🎉 ¡PROYECTO DESPLEGADO EXITOSAMENTE! 🎉
   ```

---

## 🎬 **TUS URLs FINALES**

Después de completar, tendrás:

- **Frontend:** `https://ankasoft-retail.vercel.app`
- **Backend API:** `https://retail-analytics-api-xyz123.onrender.com`
- **Swagger Docs:** `https://retail-analytics-api-xyz123.onrender.com/docs`

---

## 🚨 **SI ALGO FALLA**

### **❌ Error: "Cannot connect to backend"**
**Solución:**
1. Verifica que agregaste `VITE_API_URL` en Vercel
2. Verifica que la URL del backend es correcta
3. Espera a que Render complete el redespliegue después del PASO 4

### **❌ Error: "Database connection failed"**
**Solución:**
1. Verifica que usaste **Internal Database URL** (no External)
2. Verifica que copiaste la URL completa (empieza con `postgresql://`)

### **❌ Backend da error 500**
**Solución:**
1. En Render, ve a tu servicio
2. Clic en "Logs" en la barra lateral
3. Lee los últimos errores
4. Probablemente falta una variable de entorno

### **❌ Frontend no muestra datos**
**Solución:**
1. Abre la consola del navegador (F12)
2. Ve a la pestaña "Console"
3. ¿Ves errores de CORS? → Revisa PASO 4
4. ¿Ves errores 401? → Prueba cerrar sesión y volver a entrar

---

## 💡 **TIPS PARA LA DEMO**

1. **Despierta el backend antes de presentar:**
   - Render pone a "dormir" apps gratuitas después de 15 min
   - Abre `https://tu-backend.onrender.com/docs` 2 minutos antes
   - Espera que cargue completamente (tarda ~30 segundos)

2. **Ten un backup:**
   - Graba un video de 2 minutos mostrando todas las funcionalidades
   - Toma screenshots de cada dashboard

3. **Habla mientras carga:**
   - Si tarda en cargar, explica la arquitectura mientras esperas

---

## 📊 **RESUMEN DE LO QUE DESPLEGASTE**

✅ **Base de Datos PostgreSQL:** 1 GB, 5 tablas, ~500 registros de ejemplo  
✅ **Backend FastAPI:** 33+ endpoints, JWT auth, API Key auth  
✅ **Frontend React:** 9 páginas, 7 dashboards, gráficas interactivas  
✅ **Características:** Algoritmo Apriori, KPIs en tiempo real, chatbot  

**Costo total:** $0/mes 🎉

---

## 🏆 **¡LISTO PARA LA HACKATÓN!**

**Siguiente paso:** Practica la demo navegando por todas las páginas.

**Tiempo total empleado:** ~15 minutos

**¿Problemas?** Lee `DESPLIEGUE_COMPLETO.md` para más detalles.

---

**¡ÉXITO EN LA HACKATÓN!** 🚀✨

