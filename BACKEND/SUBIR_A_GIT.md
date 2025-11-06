# Guía: Subir Backend a Git
## Retail Analytics - Hackatón 2025

---

## 🚀 **PASOS PARA SUBIR A LA RAMA BACKEND**

### **PASO 1: Verificar archivos**

```powershell
cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft

# Ver estado
git status

# Ver qué archivos se van a subir
git status --short
```

---

### **PASO 2: Crear/Cambiar a rama backend**

```powershell
# Crear y cambiar a la rama backend
git checkout -b backend

# Si la rama ya existe:
# git checkout backend
```

---

### **PASO 3: Agregar archivos del backend**

```powershell
# Agregar todo el directorio BACKEND
git add BACKEND/

# Verificar (NO debe aparecer .env ni venv/)
git status
```

**Verificación crítica:**  
Asegúrate de que NO aparezcan:
- ❌ `BACKEND/.env`
- ❌ `BACKEND/venv/`
- ❌ `BACKEND/__pycache__/`
- ❌ `BACKEND/*.db`

Si aparecen, ejecutar:
```powershell
git reset HEAD BACKEND/.env
git reset HEAD BACKEND/venv/
```

---

### **PASO 4: Hacer commit**

```powershell
git commit -m "feat: Backend completo con Docker - Hackatón 2025

Características implementadas:
- FastAPI con 14 endpoints REST
- Autenticación con API Key
- Base de datos PostgreSQL normalizada (3 tablas)
- Chatbot con NLP (7 intenciones)
- Market Basket Analysis (Algoritmo Apriori)
- Sistema de recomendaciones inteligentes
- Predicción de ventas con ML
- Dashboard TODO-EN-UNO
- Reglas de asociación para cross-selling
- Configuración completa de Docker
- Docker Compose para BD + Backend
- Scripts de migración y carga de datos
- Documentación completa en Swagger

Tecnologías:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Docker
- Docker Compose

Endpoints:
- 10 Analytics (básicos + innovadores)
- 2 Chatbot IA
- 2 Info/Health"
```

---

### **PASO 5: Subir a GitHub**

```powershell
# Subir rama backend
git push -u origin backend
```

---

## 📋 **ARCHIVOS QUE SE SUBIRÁN**

### **✅ Código Fuente:**
```
BACKEND/database/*.py           (4 archivos)
BACKEND/routers/*.py            (3 archivos)
BACKEND/services/*.py           (4 archivos)
BACKEND/utils/*.py              (3 archivos)
BACKEND/main.py
BACKEND/cargar_datos.py
BACKEND/migrar_base_datos.py
BACKEND/verificar_proyecto.py
```

### **✅ Configuración:**
```
BACKEND/requirements.txt
BACKEND/.gitignore
BACKEND/.dockerignore
BACKEND/Dockerfile
BACKEND/docker-compose.yml
```

### **✅ Scripts:**
```
BACKEND/docker-start.bat
BACKEND/docker-start.sh
BACKEND/database/export_database.bat
BACKEND/database/export_database.sh
```

### **✅ Documentación:**
```
BACKEND/README.md
BACKEND/DOCKER_README.md
BACKEND/DOCKER_QUICKSTART.md
BACKEND/database/README.md
```

### **❌ NO se subirán (protegidos):**
```
BACKEND/.env                    (en .gitignore)
BACKEND/venv/                   (en .gitignore)
BACKEND/__pycache__/            (en .gitignore)
BACKEND/*.db                    (en .gitignore)
BACKEND/*.sqlite3               (en .gitignore)
```

---

## 🔍 **VERIFICAR ANTES DE SUBIR**

```powershell
# 1. Ver archivos preparados
git status

# 2. Ver diferencias
git diff --cached

# 3. Contar archivos
git status --short | Measure-Object -Line
```

---

## ✅ **CHECKLIST PRE-COMMIT**

- [ ] `.env` NO está en git status
- [ ] `venv/` NO está en git status
- [ ] Archivos `.pyc` NO están
- [ ] Archivos `.db` NO están
- [ ] `Dockerfile` SÍ está
- [ ] `docker-compose.yml` SÍ está
- [ ] `requirements.txt` SÍ está
- [ ] Todos los `.py` están

---

## 🎯 **COMANDOS COMPLETOS (Copia y pega)**

```powershell
# Desde el directorio raíz del proyecto
cd C:\Users\ANNY\Desktop\ANKASotf\ANKASoft

# 1. Crear/cambiar a rama backend
git checkout -b backend

# 2. Agregar archivos
git add BACKEND/

# 3. Verificar (muy importante)
git status

# 4. Si todo está OK, hacer commit
git commit -m "feat: Backend completo con Docker - Hackatón 2025"

# 5. Subir a GitHub
git push -u origin backend
```

---

## 🐳 **DESPUÉS DE SUBIR**

En GitHub verás:
- ✅ Rama `backend` creada
- ✅ Todo el código del backend
- ✅ Configuración de Docker
- ✅ Documentación completa
- ✅ Sin archivos sensibles (.env)

---

## 🏆 **VENTAJAS DE INCLUIR DOCKER**

Para la hackatón:
- ✅ Demuestra conocimiento de DevOps
- ✅ Facilita la evaluación del proyecto
- ✅ "Un comando para levantar todo"
- ✅ Portable entre sistemas
- ✅ Profesionalismo técnico

---

## 📝 **PARA TUS COMPAÑEROS**

Cuando clonen el repo:

```bash
# 1. Clonar
git clone https://github.com/Erick6485/ANKASoft.git

# 2. Cambiar a rama backend
git checkout backend

# 3. Ir al directorio
cd BACKEND

# 4. Iniciar con Docker
docker-compose up -d

# 5. Listo!
# http://localhost:8000/docs
```

---

## 🔄 **INTEGRACIÓN CON FRONTEND**

Cuando tu compañero suba el frontend:

```bash
# Hacer pull
git pull origin main

# Verás el frontend en otra carpeta
# Docker Compose se puede extender para incluirlo
```

---

**¡Docker configurado! Cuando estés listo, ejecuta los comandos y sube todo a Git.** 🐳🚀
