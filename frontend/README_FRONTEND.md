# Frontend - Retail Analytics
## Hackatón 2025 - FUP

---

## 🎨 **FRONTEND IMPLEMENTADO**

Frontend moderno con React Router v7 conectado al backend FastAPI.

---

## ✅ **CARACTERÍSTICAS**

### **Páginas:**
- ✅ Login/Registro con diseño moderno
- ✅ Dashboard con métricas en tiempo real
- ✅ Navegación lateral intuitiva
- ✅ Chatbot flotante
- ✅ Diseño responsive

### **Conexión Backend:**
- ✅ Autenticación JWT
- ✅ Llamadas a API con axios
- ✅ Manejo de tokens automático
- ✅ Gestión de errores

### **Visualizaciones:**
- ✅ Métricas principales (4 cards)
- ✅ Productos destacados
- ✅ Gráfico de barras por género
- ✅ Lista de alertas de stock

---

## 🚀 **INICIO RÁPIDO**

### **1. Instalar dependencias:**

```bash
cd frontend
npm install
```

### **2. Iniciar el frontend:**

```bash
npm run dev
```

### **3. Iniciar el backend (en otra terminal):**

```bash
cd ../BACKEND
python migrar_base_datos.py
python cargar_datos.py
python main.py
```

### **4. Acceder:**

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000

---

## 🔐 **USUARIOS DE PRUEBA**

Usa estos usuarios para hacer login:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `admin123` | ADMIN |
| `gerente` | `gerente123` | GERENTE |
| `vendedor` | `vendedor123` | VENDEDOR |

---

## 📁 **ESTRUCTURA**

```
frontend/
├── app/
│   ├── routes/
│   │   ├── login.tsx           # Página de login
│   │   ├── login.css           # Estilos login
│   │   ├── dashboard.tsx       # Dashboard principal
│   │   └── dashboard.css       # Estilos dashboard
│   ├── services/
│   │   └── api.ts              # Servicios API
│   ├── globals.css             # Estilos globales
│   └── routes.ts               # Configuración de rutas
├── package.json
└── vite.config.ts
```

---

## 🔌 **ENDPOINTS CONECTADOS**

- ✅ POST /api/auth/login-json
- ✅ POST /api/auth/register
- ✅ GET /api/analytics/dashboard-resumen
- ✅ GET /api/analytics/productos-mas-vendidos
- ✅ GET /api/analytics/comparativo-generos
- ✅ GET /api/analytics/alertas-stock
- ✅ POST /api/chatbot/mensaje

---

## 🎯 **FLUJO DE USUARIO**

1. Usuario accede a http://localhost:5173
2. Ve página de login
3. Ingresa: admin / admin123
4. Sistema hace POST /api/auth/login-json
5. Recibe token JWT
6. Guarda token en localStorage
7. Redirige a /dashboard
8. Dashboard carga datos automáticamente
9. Todas las peticiones incluyen el token

---

## 💻 **COMANDOS ÚTILES**

```bash
# Desarrollo
npm run dev

# Build producción
npm run build

# Preview producción
npm run preview

# Linter
npm run lint
```

---

## 🔧 **CONFIGURACIÓN**

### **URL del Backend:**
En `app/services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

Para producción, cambiar a tu dominio.

---

## 🎨 **ESTILOS**

- Diseño moderno y limpio
- Colores: Azul (#3b82f6), gris (#1e293b)
- Tarjetas con sombras suaves
- Transiciones y animaciones
- Responsive para móviles

---

## ✅ **TODO LISTO**

El frontend está completamente funcional y conectado al backend.

**Próximo paso:** Iniciar ambos servicios y probar!

