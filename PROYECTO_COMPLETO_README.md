# Retail Analytics - Proyecto Completo
## Frontend + Backend - Hackatón 2025 FUP

---

## 🏆 **PROYECTO FULLSTACK COMPLETO**

Sistema completo de análisis de retail con:
- ✅ Backend API REST (FastAPI)
- ✅ Frontend Web (React)
- ✅ Base de Datos (PostgreSQL)
- ✅ Autenticación JWT
- ✅ Chatbot IA
- ✅ Market Basket Analysis
- ✅ Docker

---

## 🚀 **INICIO ULTRA RÁPIDO**

### **Windows:**
```powershell
.\iniciar-proyecto.bat
```

Esto abrirá 2 ventanas automáticamente:
- Backend en puerto 8000
- Frontend en puerto 5173

### **Manual:**

**Terminal 1 - Backend:**
```powershell
cd BACKEND
.\venv\Scripts\Activate.ps1
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 🌐 **ACCEDER**

1. **Abre:** http://localhost:5173
2. **Login con:** admin / admin123
3. **¡Disfruta del dashboard!**

---

## 📊 **ARQUITECTURA**

```
┌─────────────────┐
│   FRONTEND      │
│   React + Vite  │
│   Port: 5173    │
└────────┬────────┘
         │
         │ HTTP/REST
         │ JWT Token
         ↓
┌─────────────────┐
│   BACKEND       │
│   FastAPI       │
│   Port: 8000    │
└────────┬────────┘
         │
         │ SQLAlchemy
         ↓
┌─────────────────┐
│  PostgreSQL     │
│  Port: 5432     │
└─────────────────┘
```

---

## 🎨 **FRONTEND**

### **Páginas:**
- 🔐 Login/Registro
- 📊 Dashboard principal
- 📈 Métricas en tiempo real
- 🤖 Chatbot flotante

### **Tecnologías:**
- React Router v7
- TypeScript
- Axios
- React Icons
- CSS Moderno

---

## 🔌 **BACKEND**

### **Endpoints:**
- 📝 4 Autenticación
- 📊 10 Analytics
- 🤖 2 Chatbot
- ℹ️ 2 Info

### **Tecnologías:**
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT
- Bcrypt

---

## 🎯 **FEATURES DESTACADAS**

### **1. Login Completo** 🔐
- Sistema JWT profesional
- Registro de usuarios
- 3 roles (Admin, Gerente, Vendedor)
- Tokens con expiración

### **2. Dashboard Interactivo** 📊
- 4 métricas principales
- Productos más vendidos
- Comparativo por género
- Alertas de stock en tiempo real

### **3. Chatbot IA** 🤖
- Botón flotante
- Procesamiento lenguaje natural
- 7 intenciones detectadas
- Respuestas contextualizadas

### **4. Market Basket Analysis** 🛒
- Algoritmo Apriori
- Patrones de compra
- Recomendaciones cross-selling

### **5. Predicciones** 📈
- Machine Learning básico
- Tendencias automáticas
- Predicción por categoría

---

## 👥 **USUARIOS DE PRUEBA**

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| admin | admin123 | ADMIN | ✅ Todo |
| gerente | gerente123 | GERENTE | ✅ Gestión |
| vendedor | vendedor123 | VENDEDOR | ✅ Lectura |

---

## 🔍 **VERIFICACIÓN COMPLETA**

### **1. Backend funcionando:**
```bash
curl http://localhost:8000/health
# Response: {"status":"healthy"}
```

### **2. Frontend funcionando:**
- Abre: http://localhost:5173
- Debes ver página de login

### **3. Conexión funcionando:**
- Haz login
- Si redirige a dashboard → ✅ CONECTADO
- Si muestra error → Verifica backend

---

## 📁 **ESTRUCTURA DEL PROYECTO**

```
ANKASoft/
├── BACKEND/                    # API Backend
│   ├── database/               # Modelos y esquemas
│   ├── routers/                # Endpoints (auth, analytics, chatbot)
│   ├── services/               # Lógica de negocio
│   ├── utils/                  # Utilidades (auth, security)
│   ├── main.py                 # Aplicación principal
│   ├── Dockerfile              # Docker backend
│   └── docker-compose.yml      # Backend + PostgreSQL
│
├── frontend/                   # Aplicación Web
│   ├── app/
│   │   ├── routes/             # Páginas (login, dashboard)
│   │   ├── services/           # Conexión API
│   │   └── globals.css         # Estilos globales
│   ├── package.json
│   └── vite.config.ts
│
└── iniciar-proyecto.bat        # Script inicio automático
```

---

## 🐳 **ALTERNATIVA: CON DOCKER**

```bash
# Solo backend con Docker
cd BACKEND
docker-compose up -d

# Frontend normal
cd ../frontend
npm run dev
```

---

## 🎓 **TECNOLOGÍAS USADAS**

### **Frontend:**
- ⚛️ React 18
- 🔀 React Router v7
- 📘 TypeScript
- ⚡ Vite
- 🎨 CSS Moderno

### **Backend:**
- 🐍 Python 3.11+
- ⚡ FastAPI
- 🗄️ PostgreSQL
- 🔐 JWT + Bcrypt
- 🐳 Docker

### **IA/ML:**
- 🤖 NLP básico (Chatbot)
- 🛒 Apriori (Market Basket)
- 📈 Predicción ventas
- 💡 Recomendaciones

---

## 📊 **DATOS CARGADOS**

Al ejecutar `python cargar_datos.py`:
- ✅ 3 Usuarios (admin, gerente, vendedor)
- ✅ 4 Sucursales
- ✅ 300+ Productos
- ✅ 500 Ventas (últimos 3 meses)

---

## 🎯 **PARA LA PRESENTACIÓN**

### **Script de Demo (5 min):**

1. **[30 seg] Mostrar login**
   - Ingresar como admin
   - Explicar autenticación JWT

2. **[1 min] Dashboard**
   - Métricas principales
   - Productos destacados
   - Alertas de stock

3. **[1 min] Chatbot**
   - Click en botón flotante
   - Preguntar: "productos más vendidos"
   - Mostrar respuesta inteligente

4. **[1 min] Backend**
   - Mostrar Swagger: localhost:8000/docs
   - Explicar algoritmos IA
   - Market Basket Analysis

5. **[1 min] Docker**
   - Mostrar docker-compose.yml
   - "Un comando para levantar todo"

6. **[30 seg] Cierre**
   - Tecnologías usadas
   - Innovación aplicada

---

## ✅ **CUMPLIMIENTO DEL RETO**

| Requisito | Estado |
|-----------|--------|
| Software web funcional | ✅ 100% |
| Análisis de rotación | ✅ 100% |
| Control de inventario | ✅ 100% |
| Decisiones basadas en datos | ✅ 100% |
| Visualizaciones gráficas | ✅ 100% |
| Dashboard | ✅ 100% |
| Carga de datos históricos | ✅ 100% |
| KPIs requeridos | ✅ 100% |
| Recomendaciones automáticas | ✅ 100% |
| **Innovación extra** | ✅ IA, Chatbot, Market Basket |

---

## 🏅 **PUNTOS FUERTES**

1. **Fullstack Completo** - Frontend + Backend + BD
2. **4 Algoritmos IA** - NLP, Apriori, ML, Recomendaciones
3. **Autenticación Real** - JWT con roles
4. **Docker** - DevOps profesional
5. **UX Excepcional** - Diseño moderno y limpio
6. **Chatbot** - Interacción natural
7. **Market Basket** - Data mining real

---

## 🚀 **COMANDOS RÁPIDOS**

```powershell
# Iniciar todo
.\iniciar-proyecto.bat

# O manualmente
cd BACKEND && python main.py
cd frontend && npm run dev

# Acceder
start http://localhost:5173
```

---

**¡PROYECTO FULLSTACK COMPLETO Y FUNCIONANDO!** 🎨🔌🚀🏆

