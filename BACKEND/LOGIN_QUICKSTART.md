# Login - Inicio Rápido
## 3 Pasos para Iniciar Sesión

---

## ⚡ **INICIO RÁPIDO**

### **PASO 1: Migrar y Cargar Datos**

```powershell
python migrar_base_datos.py
python cargar_datos.py
python main.py
```

Esto crea 3 usuarios:
- ✅ admin / admin123
- ✅ gerente / gerente123
- ✅ vendedor / vendedor123

---

### **PASO 2: Hacer Login en Swagger**

1. **Abre:** http://localhost:8000/docs

2. **Busca:** POST /api/auth/login

3. **Click en "Try it out"**

4. **Ingresa:**
   - username: `admin`
   - password: `admin123`

5. **Click en "Execute"**

6. **Copia el `access_token`** de la respuesta

---

### **PASO 3: Autorizar en Swagger**

1. **Click en "Authorize"** 🔓 (arriba a la derecha)

2. **Verás dos secciones:**
   - APIKeyHeader (apiKey) ← Sistema antiguo
   - **OAuth2PasswordBearer (OAuth2)** ← ¡USAR ESTE!

3. **En OAuth2PasswordBearer, ingresa:**
   - Username: `admin`
   - Password: `admin123`

4. **Click en "Authorize"**

5. **Click en "Close"**

✅ **¡Listo! Ya estás autenticado**

---

## 🎯 **AHORA PUEDES USAR TODOS LOS ENDPOINTS**

Todos los endpoints protegidos funcionarán automáticamente.

---

## 👤 **USUARIOS DISPONIBLES**

### **Admin** (Acceso total)
```
Username: admin
Password: admin123
Rol: ADMIN
```

### **Gerente** (Gestión)
```
Username: gerente
Password: gerente123
Rol: GERENTE
```

### **Vendedor** (Solo lectura)
```
Username: vendedor
Password: vendedor123
Rol: VENDEDOR
```

---

## 🔐 **DOS FORMAS DE AUTENTICAR**

### **Forma 1: JWT (Recomendado - Nuevo)**
1. Login → Obtener token
2. Usar token en cada petición
3. Token expira en 24 horas

### **Forma 2: API Key (Simple - Antiguo)**
1. Usar directamente: `retail_hackaton_2025_fup`
2. Header: `X-API-Key`

---

## 🧪 **PROBAR LOGIN**

```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Copiar el access_token y usar:
curl -X GET "http://localhost:8000/api/analytics/dashboard-resumen" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## ✅ **VERIFICAR QUE FUNCIONA**

```bash
# Ver mi perfil
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer TU_TOKEN"
```

---

**¡Sistema de Login listo en 3 pasos!** 🔐🚀

