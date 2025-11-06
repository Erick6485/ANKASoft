# Sistema de Login y Autenticación JWT
## Retail Analytics Backend - Hackatón 2025

---

## 🔐 **SISTEMA DE AUTENTICACIÓN IMPLEMENTADO**

Tu API ahora tiene **DOS sistemas de autenticación:**

1. **API Key** - Para acceso rápido (demos)
2. **JWT (Login tradicional)** - Usuarios individuales con sesiones

---

## 👥 **USUARIOS DE EJEMPLO**

Al cargar datos (`python cargar_datos.py`), se crean 3 usuarios:

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `admin123` | ADMIN | Acceso total |
| `gerente` | `gerente123` | GERENTE | Gestión + Lectura |
| `vendedor` | `vendedor123` | VENDEDOR | Solo lectura |

---

## 🔑 **ENDPOINTS DE AUTENTICACIÓN**

### **1. POST /api/auth/register** - Registrar Usuario

**Request:**
```json
{
  "username": "nuevo_usuario",
  "email": "usuario@email.com",
  "password": "contraseña123",
  "nombre_completo": "Nombre Completo",
  "rol": "vendedor"
}
```

**Response:**
```json
{
  "id": 4,
  "username": "nuevo_usuario",
  "email": "usuario@email.com",
  "nombre_completo": "Nombre Completo",
  "rol": "vendedor",
  "activo": true,
  "fecha_creacion": "2025-11-06T10:00:00"
}
```

---

### **2. POST /api/auth/login** - Iniciar Sesión (Form)

**Request:** (usando form-data)
```
username: admin
password: admin123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@retailanalytics.com",
    "nombre_completo": "Administrador del Sistema",
    "rol": "admin",
    "activo": true
  }
}
```

---

### **3. POST /api/auth/login-json** - Iniciar Sesión (JSON)

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:** (igual que login)

---

### **4. GET /api/auth/me** - Mi Perfil

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@retailanalytics.com",
  "nombre_completo": "Administrador del Sistema",
  "rol": "admin",
  "activo": true
}
```

---

## 🚀 **CÓMO USAR EN SWAGGER UI**

### **PASO 1: Iniciar Sesión**

1. Ve a http://localhost:8000/docs
2. Busca **POST /api/auth/login**
3. Click en "Try it out"
4. Ingresa:
   - **username:** `admin`
   - **password:** `admin123`
5. Click en "Execute"
6. **COPIA el `access_token`** de la respuesta

---

### **PASO 2: Autorizar con el Token**

1. Click en el botón **"Authorize"** 🔓 (arriba a la derecha)
2. Verás dos opciones:
   - **APIKeyHeader (apiKey)** - Sistema antiguo
   - **OAuth2PasswordBearer (OAuth2)** - Sistema nuevo JWT

3. **En OAuth2PasswordBearer:**
   - Ingresa: `admin`
   - Password: `admin123`
   - Click en "Authorize"

4. **O pega el token** directamente si lo copiaste

5. Click en "Close"

---

### **PASO 3: Usar Endpoints Protegidos**

Ahora todos los endpoints funcionarán con tu sesión activa.

---

## 💻 **CÓMO USAR CON CÓDIGO**

### **Python:**

```python
import requests

# 1. Login
login_url = "http://localhost:8000/api/auth/login-json"
login_data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(login_url, json=login_data)
token_data = response.json()
access_token = token_data["access_token"]

print(f"✅ Login exitoso!")
print(f"Usuario: {token_data['user']['username']}")
print(f"Rol: {token_data['user']['rol']}")

# 2. Usar el token en peticiones
headers = {
    "Authorization": f"Bearer {access_token}"
}

# 3. Llamar a endpoints protegidos
api_url = "http://localhost:8000/api/analytics/dashboard-resumen"
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Datos obtenidos: {data['resumen_general']}")
else:
    print(f"❌ Error: {response.json()}")
```

---

### **JavaScript/Fetch:**

```javascript
// 1. Login
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/auth/login-json', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  
  // Guardar token
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
}

// 2. Usar token en peticiones
async function getDashboard() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/api/analytics/dashboard-resumen', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
}

// Uso
login('admin', 'admin123').then(data => {
  console.log('Login exitoso:', data.user);
  getDashboard().then(dashboard => {
    console.log('Dashboard:', dashboard);
  });
});
```

---

### **curl:**

```bash
# 1. Login
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

# 2. Usar token
curl -X GET "http://localhost:8000/api/analytics/dashboard-resumen" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔒 **DOBLE AUTENTICACIÓN**

Ahora tienes **dos formas** de autenticarte:

### **Opción A: API Key (Simple)**
```python
headers = {"X-API-Key": "retail_hackaton_2025_fup"}
response = requests.get(url, headers=headers)
```

### **Opción B: JWT (Profesional)**
```python
# 1. Login primero
token = login("admin", "admin123")

# 2. Usar token
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(url, headers=headers)
```

---

## 📊 **TABLA DE USUARIOS EN BD**

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100),
    rol VARCHAR(10),  -- admin, gerente, vendedor
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 **SEGURIDAD**

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Tokens JWT con expiración (24 horas)
- ✅ Verificación de usuario activo
- ✅ Roles y permisos
- ✅ Emails únicos
- ✅ Usernames únicos

---

## 🎯 **FLUJO COMPLETO**

```
1. Usuario abre app
2. Ve formulario de login
3. Ingresa: admin / admin123
4. POST /api/auth/login
5. Recibe token JWT
6. Guarda token en localStorage/cookie
7. Todas las peticiones incluyen: Authorization: Bearer <token>
8. Token válido por 24 horas
9. Después de 24h, debe hacer login de nuevo
```

---

## 🆕 **MIGRAR BASE DE DATOS**

**IMPORTANTE:** Agregamos la tabla de usuarios, necesitas migrar:

```powershell
# 1. Migrar
python migrar_base_datos.py

# Escribe 's' para continuar

# 2. Cargar datos (incluye usuarios)
python cargar_datos.py

# Verás:
# ✅ 3 usuarios creados
#    - admin / admin123 (Rol: ADMIN)
#    - gerente / gerente123 (Rol: GERENTE)
#    - vendedor / vendedor123 (Rol: VENDEDOR)

# 3. Reiniciar servidor
python main.py
```

---

## 🧪 **PROBAR EL SISTEMA**

### **1. Registrar nuevo usuario:**

En Swagger:
- POST /api/auth/register
- Body:
```json
{
  "username": "test",
  "email": "test@test.com",
  "password": "test123",
  "nombre_completo": "Usuario de Prueba",
  "rol": "vendedor"
}
```

### **2. Login:**

- POST /api/auth/login
- Username: `test`
- Password: `test123`
- Copiar `access_token`

### **3. Usar token:**

- Click en "Authorize"
- Pegar token en OAuth2PasswordBearer
- Probar cualquier endpoint

---

## ⚙️ **CONFIGURACIÓN**

En `utils/auth.py`:

```python
SECRET_KEY = "clave_secreta_hackaton_2025_fup_jwt_token"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 horas
```

**Para producción:** Usar variables de entorno.

---

## 📝 **ENDPOINTS TOTALES AHORA**

| Categoría | Endpoints |
|-----------|-----------|
| **Autenticación** | 4 |
| Analytics Básicos | 4 |
| Analytics Innovadores | 5 |
| Chatbot IA | 2 |
| Utilidades | 1 |
| Info | 2 |
| **TOTAL** | **18** |

---

## 🏆 **VENTAJAS DEL SISTEMA JWT**

### **Para la Hackatón:**
- ✅ Demuestra conocimiento de seguridad
- ✅ Sistema real de autenticación
- ✅ Manejo de sesiones
- ✅ Roles y permisos
- ✅ Más profesional

### **Técnicas:**
- ✅ JWT estándar
- ✅ Bcrypt para passwords
- ✅ OAuth2 compatible
- ✅ Tokens con expiración
- ✅ Refresh posible (futuro)

---

## 💡 **PARA LA PRESENTACIÓN**

**Menciona:**
- ✅ "Sistema de autenticación con JWT"
- ✅ "Contraseñas hasheadas con bcrypt"
- ✅ "Roles: Admin, Gerente, Vendedor"
- ✅ "Tokens con expiración de 24 horas"

**Demuestra:**
1. Registrar un usuario nuevo
2. Hacer login
3. Obtener token
4. Usar endpoint protegido
5. Ver perfil con GET /api/auth/me

---

## 🔧 **PRÓXIMO PASO**

```powershell
# 1. Instalar nuevas dependencias
pip install python-jose[cryptography] passlib[bcrypt]

# 2. Migrar BD (agrega tabla usuarios)
python migrar_base_datos.py

# 3. Cargar datos (crea usuarios)
python cargar_datos.py

# 4. Reiniciar servidor
python main.py

# 5. Probar login en:
# http://localhost:8000/docs
```

---

**¡Sistema de Login JWT completo implementado!** 🔐✨

