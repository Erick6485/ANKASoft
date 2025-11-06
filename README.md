# 🏆 Retail Analytics - Sistema Completo
## Hackatón FUP 2025

Sistema fullstack de análisis de inventario y ventas para retail de ropa con Inteligencia Artificial.

---

## ✨ **CARACTERÍSTICAS PRINCIPALES**

### **🎨 Frontend (React)**
- Login/Registro con diseño moderno
- Dashboard interactivo con métricas en tiempo real
- Navegación lateral intuitiva
- Chatbot flotante integrado
- Diseño responsive

### **🔌 Backend (FastAPI)**
- 18 endpoints REST
- Autenticación JWT con roles
- 4 algoritmos de IA
- Chatbot con NLP
- Market Basket Analysis (Apriori)
- Sistema de recomendaciones
- Predicción de ventas

### **🗄️ Base de Datos (PostgreSQL)**
- 4 tablas normalizadas
- Relaciones optimizadas
- Índices para consultas rápidas

---

## 🚀 **INICIO RÁPIDO (1 COMANDO)**

### **Windows:**
```powershell
.\iniciar-proyecto.bat
```

### **Manual (2 Terminales):**

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

### **Acceder:**
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Documentación:** http://localhost:8000/docs

---

## 🔐 **USUARIOS DE PRUEBA**

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | ADMIN |
| gerente | gerente123 | GERENTE |
| vendedor | vendedor123 | VENDEDOR |

---

## 📊 **TECNOLOGÍAS**

### **Frontend:**
- React 19
- React Router v7
- TypeScript
- Axios
- Vite

### **Backend:**
- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT + Bcrypt
- Docker

---

## 🧠 **ALGORITMOS IA IMPLEMENTADOS**

1. **Chatbot con NLP** - Procesamiento de lenguaje natural
2. **Market Basket Analysis** - Algoritmo Apriori
3. **Sistema de Recomendaciones** - IA automática
4. **Predicción de Ventas** - Machine Learning

---

## 📡 **ENDPOINTS (18 TOTALES)**

### **Autenticación (4):**
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/login-json
- GET /api/auth/me

### **Analytics (10):**
- Productos más vendidos
- Rotación de tallas
- Alertas de stock
- Comparativo por géneros
- Recomendaciones inteligentes
- Predicción de ventas
- Dashboard resumen
- Reglas de asociación
- Recomendaciones cruzadas
- Cargar datos ejemplo

### **Chatbot (2):**
- POST /api/chatbot/mensaje
- GET /api/chatbot/ejemplos

### **Info (2):**
- GET /
- GET /health

---

## 🎯 **CUMPLIMIENTO DEL RETO**

✅ Software web funcional (MVP)  
✅ Análisis de rotación mensual  
✅ Control de inventario eficiente  
✅ Decisiones basadas en datos  
✅ Reducir pérdidas (stock/desabastecimiento)  
✅ Visualizaciones gráficas (Dashboard)  
✅ Carga de datos históricos  
✅ KPIs: productos más vendidos, tallas, comparativos  
✅ Recomendaciones automáticas  
✅ **INNOVACIÓN EXTRA:** IA, Chatbot, Market Basket  

---

## 🏗️ **INSTALACIÓN COMPLETA**

### **1. Clonar Repositorio**
```bash
git clone https://github.com/Erick6485/ANKASoft.git
cd ANKASoft
```

### **2. Configurar Backend**
```powershell
cd BACKEND
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python migrar_base_datos.py
python cargar_datos.py
```

### **3. Configurar Frontend**
```powershell
cd ../frontend
npm install
```

### **4. Iniciar Proyecto**
```powershell
cd ..
.\iniciar-proyecto.bat
```

---

## 🐳 **CON DOCKER**

```bash
cd BACKEND
docker-compose up -d
cd ../frontend
npm run dev
```

---

## 📝 **ESTRUCTURA DE CARPETAS**

```
ANKASoft/
├── BACKEND/                 ✅ API REST + BD
├── frontend/                ✅ Aplicación Web
├── iniciar-proyecto.bat     ✅ Script inicio
├── PROYECTO_COMPLETO_README.md
└── README.md               ← Estás aquí
```

---

## 🎓 **EQUIPO DE DESARROLLO**

- Backend: Anny Diaz
- Frontend: Equipo ANKASoft
- Hackatón: FUP 2025

---

## 📄 **LICENCIA**

Proyecto desarrollado para Hackatón FUP 2025.

---

## 🔗 **RECURSOS**

- [Documentación Backend](./BACKEND/README.md)
- [Documentación Frontend](./frontend/README_FRONTEND.md)
- [Guía Docker](./BACKEND/DOCKER_README.md)
- [Sistema de Login](./BACKEND/SISTEMA_LOGIN.md)
- [Inicio Completo](./INICIAR_PROYECTO_COMPLETO.md)

---

## 🏆 **INNOVACIONES DESTACADAS**

- 🤖 Chatbot conversacional con NLP
- 🛒 Market Basket Analysis (Apriori)
- 💡 Sistema de recomendaciones IA
- 📈 Predicción de ventas
- 🔐 Autenticación JWT profesional
- 📊 Dashboard TODO-EN-UNO
- 🐳 Containerización con Docker

---

## ✅ **ESTADO DEL PROYECTO**

**COMPLETO Y FUNCIONAL** ✅

- Frontend: ✅
- Backend: ✅
- Base de Datos: ✅
- Autenticación: ✅
- IA/ML: ✅
- Docker: ✅
- Documentación: ✅

---

**¡Proyecto listo para presentar y ganar la hackatón!** 🏆🚀

Para más información, consulta [PROYECTO_COMPLETO_README.md](./PROYECTO_COMPLETO_README.md)
