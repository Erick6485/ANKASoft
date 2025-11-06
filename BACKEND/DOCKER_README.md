# Docker - Retail Analytics Backend
## Hackatón 2025 - FUP

---

## 🐳 **CONFIGURACIÓN DE DOCKER**

Este proyecto incluye configuración completa de Docker para:
- ✅ Backend FastAPI
- ✅ Base de datos PostgreSQL
- ✅ Orquestación con Docker Compose

---

## 📋 **REQUISITOS PREVIOS**

### **Instalar Docker Desktop:**

1. **Windows:**
   - Descarga: https://www.docker.com/products/docker-desktop
   - Instala Docker Desktop
   - Reinicia tu computadora
   - Verifica: `docker --version`

2. **Linux/Mac:**
   ```bash
   # Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Docker Compose
   sudo apt-get install docker-compose
   ```

---

## 🚀 **INICIO RÁPIDO**

### **Opción 1: Script Automático (Recomendado)**

**Windows:**
```powershell
.\docker-start.bat
```

**Linux/Mac:**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

### **Opción 2: Comandos Manuales**

```bash
# 1. Construir imágenes
docker-compose build

# 2. Iniciar contenedores
docker-compose up -d

# 3. Esperar 10 segundos para que PostgreSQL inicie

# 4. Cargar datos de ejemplo
docker-compose exec backend python cargar_datos.py

# 5. Ver logs
docker-compose logs -f
```

---

## 📦 **SERVICIOS INCLUIDOS**

### **1. PostgreSQL (db)**
- **Imagen:** postgres:16-alpine
- **Puerto:** 5432
- **Usuario:** postgres
- **Contraseña:** hackaton2025
- **Base de datos:** retail_analytics
- **Volume:** postgres_data (persiste datos)

### **2. Backend FastAPI (backend)**
- **Puerto:** 8000
- **Auto-reload:** Activado
- **Depends on:** db (espera a PostgreSQL)
- **Volume:** Código montado para desarrollo

---

## 🌐 **ACCEDER A LA APLICACIÓN**

Una vez iniciado, accede a:

- **API Principal:** http://localhost:8000
- **Documentación Swagger:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **ReDoc:** http://localhost:8000/redoc

---

## 🔑 **AUTENTICACIÓN**

**API Key:** `retail_hackaton_2025_fup`

En Swagger UI:
1. Click en "Authorize"
2. Ingresa la API Key
3. Click en "Authorize" y "Close"

---

## 🛠️ **COMANDOS ÚTILES**

### **Ver estado de contenedores:**
```bash
docker-compose ps
```

### **Ver logs:**
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo base de datos
docker-compose logs -f db
```

### **Detener servicios:**
```bash
docker-compose down
```

### **Detener y eliminar datos:**
```bash
docker-compose down -v
```

### **Reiniciar servicios:**
```bash
docker-compose restart

# O solo uno
docker-compose restart backend
```

### **Reconstruir imágenes:**
```bash
docker-compose build --no-cache
docker-compose up -d
```

### **Ejecutar comandos dentro del contenedor:**
```bash
# Acceder a shell del backend
docker-compose exec backend bash

# Ejecutar script Python
docker-compose exec backend python cargar_datos.py

# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d retail_analytics
```

---

## 📊 **CARGAR DATOS DE EJEMPLO**

```bash
# Si los contenedores ya están corriendo
docker-compose exec backend python cargar_datos.py

# O desde dentro del contenedor
docker-compose exec backend bash
python cargar_datos.py
exit
```

---

## 🔧 **VARIABLES DE ENTORNO**

Configuradas en `docker-compose.yml`:

```yaml
environment:
  DATABASE_URL: postgresql://postgres:hackaton2025@db:5432/retail_analytics
  SECRET_KEY: clave_secreta_hackaton_2025_fup
  DEBUG: "True"
  API_KEY: retail_hackaton_2025_fup
```

**No necesitas crear archivo `.env` para Docker.**

---

## 🗄️ **PERSISTENCIA DE DATOS**

### **Volume de PostgreSQL:**
```bash
# Los datos se guardan en un volume Docker
# Nombre: retail_analytics_postgres_data

# Ver volumes
docker volume ls

# Eliminar datos (cuidado)
docker-compose down -v
```

---

## 🔍 **VERIFICAR QUE TODO FUNCIONA**

### **1. Verificar contenedores:**
```bash
docker-compose ps

# Deberías ver:
# retail_analytics_db       Up    5432/tcp
# retail_analytics_backend  Up    8000/tcp
```

### **2. Verificar logs:**
```bash
docker-compose logs backend

# Deberías ver:
# INFO: Application startup complete.
# INFO: Uvicorn running on http://0.0.0.0:8000
```

### **3. Verificar base de datos:**
```bash
docker-compose exec db psql -U postgres -d retail_analytics -c "\dt"

# Deberías ver las tablas:
# productos
# ventas
# sucursales
```

### **4. Verificar API:**
```bash
curl http://localhost:8000/health

# Respuesta:
# {"status":"healthy","service":"retail-analytics-api"}
```

---

## 🎯 **DESARROLLO CON DOCKER**

### **Hot Reload Activado:**
Los cambios en el código se reflejan automáticamente:
1. Edita un archivo Python
2. Guarda
3. El servidor se reinicia automáticamente
4. Recarga la página

### **Ver logs en tiempo real:**
```bash
docker-compose logs -f backend
```

---

## 🚀 **DESPLIEGUE (Producción)**

### **Para producción, ajustar:**

1. **Cambiar DEBUG a False**
2. **Usar secretos seguros**
3. **Configurar ALLOWED_ORIGINS específicos**
4. **Usar variables de entorno desde archivo**
5. **Configurar reverse proxy (Nginx)**

---

## 🛑 **DETENER TODO**

```bash
# Detener contenedores (mantiene datos)
docker-compose down

# Detener y eliminar datos
docker-compose down -v

# Detener y eliminar todo (incluyendo imágenes)
docker-compose down -v --rmi all
```

---

## 🔄 **REINICIAR DESDE CERO**

```bash
# 1. Detener y limpiar todo
docker-compose down -v

# 2. Reconstruir
docker-compose build --no-cache

# 3. Iniciar
docker-compose up -d

# 4. Cargar datos
docker-compose exec backend python cargar_datos.py
```

---

## 📝 **ESTRUCTURA DE ARCHIVOS DOCKER**

```
BACKEND/
├── Dockerfile              ✅ Configuración del contenedor backend
├── docker-compose.yml      ✅ Orquestación de servicios
├── .dockerignore          ✅ Archivos a ignorar
├── .env.docker            ✅ Variables de ejemplo
├── docker-start.bat       ✅ Script inicio Windows
└── docker-start.sh        ✅ Script inicio Linux/Mac
```

---

## 🐛 **SOLUCIÓN DE PROBLEMAS**

### **Error: Puerto 8000 en uso**
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8000

# Cambiar el puerto en docker-compose.yml:
ports:
  - "8001:8000"  # Usar 8001 externamente
```

### **Error: Puerto 5432 en uso**
```bash
# Si tienes PostgreSQL local corriendo
# Detenerlo o cambiar puerto en docker-compose.yml:
ports:
  - "5433:5432"  # Usar 5433 externamente
```

### **Error: Contenedor no inicia**
```bash
# Ver logs detallados
docker-compose logs backend

# Reconstruir desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### **Base de datos no conecta**
```bash
# Verificar que PostgreSQL esté listo
docker-compose logs db

# Esperar más tiempo
docker-compose restart backend
```

---

## 💡 **VENTAJAS DE USAR DOCKER**

### **Para la Hackatón:**
- ✅ **Portabilidad:** "Funciona en mi máquina" → "Funciona en todas"
- ✅ **Fácil setup:** Un comando para iniciar todo
- ✅ **Profesionalismo:** Demuestra conocimiento de DevOps
- ✅ **Reproducibilidad:** Mismo entorno siempre
- ✅ **Aislamiento:** No afecta tu sistema

### **Para Presentación:**
- ✅ Demo rápida sin configuración
- ✅ No depende del SO del jurado
- ✅ Impresiona técnicamente
- ✅ Fácil de compartir

---

## 🎓 **COMANDOS PARA LA PRESENTACIÓN**

```bash
# Inicio en segundos
docker-compose up -d

# Mostrar que funciona
curl http://localhost:8000

# Abrir en navegador
start http://localhost:8000/docs

# Ver logs en vivo (opcional)
docker-compose logs -f backend
```

---

## 📦 **COMPARTIR EL PROYECTO**

### **Opción 1: Con Docker Hub (Avanzado)**
```bash
# Build
docker build -t usuario/retail-analytics-backend:v1.0 .

# Push
docker push usuario/retail-analytics-backend:v1.0

# Otros pueden usar:
docker pull usuario/retail-analytics-backend:v1.0
```

### **Opción 2: Con GitHub (Recomendado)**
```bash
# Subir el código con Docker files
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "feat: Agregar configuración de Docker"
git push origin backend

# Otros clonan y ejecutan:
git clone <repo>
cd BACKEND
docker-compose up -d
```

---

## ✅ **CHECKLIST DOCKER**

Antes de presentar:

- [ ] Docker Desktop instalado y corriendo
- [ ] `docker-compose up -d` funciona sin errores
- [ ] http://localhost:8000/docs es accesible
- [ ] Datos de ejemplo cargados
- [ ] Todos los endpoints responden
- [ ] Logs sin errores críticos

---

## 🏆 **PARA LA PRESENTACIÓN**

**Menciona:**
- ✅ "Implementamos Docker para facilitar el despliegue"
- ✅ "Toda la infraestructura en contenedores"
- ✅ "Un comando para levantar todo el sistema"
- ✅ "Portable y reproducible"

**Demuestra:**
```bash
docker-compose up -d
# Esperar 15 segundos
# Abrir http://localhost:8000/docs
# ¡Funciona!
```

---

## 📚 **RECURSOS**

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)

---

**¡Configuración de Docker completa y lista para usar!** 🐳🚀

