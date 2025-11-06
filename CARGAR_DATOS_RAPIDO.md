# 🚀 CARGAR DATOS EN LA BASE DE DATOS - GUÍA RÁPIDA

---

## ⚡ **OPCIÓN 1: COMANDO RÁPIDO (RECOMENDADO)**

Abre PowerShell en la carpeta `BACKEND` y ejecuta:

```powershell
cd BACKEND
.\venv\Scripts\Activate.ps1
python cargar_datos.py
```

**Output esperado:**
```
🔄 Cargando datos de ejemplo...
✅ 4 sucursales creadas
✅ 864 productos creados
✅ 500 ventas de ejemplo creadas
✅ 3 usuarios creados
🎉 Datos de ejemplo cargados exitosamente!
{'productos': 864, 'ventas': 500, 'sucursales': 4, 'usuarios': 3}
```

---

## 📊 **DATOS QUE SE CREARÁN**

### **Sucursales (4):**
- Sucursal Norte
- Sucursal Sur
- Sucursal Centro
- Sucursal Este

### **Productos (864):**
- Abrigos, Bermudas, Buzos, Camisas, Faldas, Jeans, Pantalones, Vestidos, Polos
- Para: Mujer, Hombre, Niño, Niña
- Tallas: XXS, XS, S, M, L, XL (adultos) | 4, 6, 8, 10, 12, 14, 16 (niños)
- Precios: $15 - $150 (aleatorios)
- Stock: 0 - 100 unidades (aleatorio)

### **Ventas (500):**
- Últimos 90 días
- Productos aleatorios
- Cantidades: 1-3 unidades por venta
- Distribuidas entre las 4 sucursales

### **Usuarios (3):**
| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | ADMIN |
| gerente | gerente123 | GERENTE |
| vendedor | vendedor123 | VENDEDOR |

---

## 🔧 **SI HAY PROBLEMAS**

### **Problema 1: "ModuleNotFoundError: No module named 'database'"**

**Solución:**
```powershell
cd BACKEND
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python cargar_datos.py
```

---

### **Problema 2: "Ya existen datos en la base de datos"**

**Solución A - Mantener datos existentes:**
```
El script detecta automáticamente si hay datos y NO los duplica.
✅ Simplemente continúa.
```

**Solución B - Borrar y recargar (CUIDADO):**
```powershell
# Borrar la base de datos SQLite
Remove-Item retail_analytics.db

# O si usas PostgreSQL, ejecuta en psql:
# DROP DATABASE retail_analytics;
# CREATE DATABASE retail_analytics;

# Luego migra y carga:
python migrar_base_datos.py
python cargar_datos.py
```

---

### **Problema 3: "error: subprocess-exited-with-error"**

**Solución:**
```powershell
# Asegúrate de que el venv está activado
.\venv\Scripts\Activate.ps1

# Reinstala dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ✅ **VERIFICAR QUE LOS DATOS SE CARGARON**

### **Opción 1: Desde Python**
```powershell
python
```

```python
from database.connection import SessionLocal
from database.models import Producto, Venta, Usuario

db = SessionLocal()

# Contar productos
print(f"Productos: {db.query(Producto).count()}")

# Contar ventas
print(f"Ventas: {db.query(Venta).count()}")

# Contar usuarios
print(f"Usuarios: {db.query(Usuario).count()}")

# Ver primeros 5 productos
for p in db.query(Producto).limit(5).all():
    print(f"- {p.nombre} | ${p.precio} | Stock: {p.stock_actual}")

db.close()
exit()
```

**Output esperado:**
```
Productos: 864
Ventas: 500
Usuarios: 3
- Abrigo Mujer Talla XXS | $89.5 | Stock: 45
- Abrigo Mujer Talla XS | $92.3 | Stock: 12
- Bermuda Mujer Talla XXS | $34.2 | Stock: 8
- Bermuda Mujer Talla XS | $41.7 | Stock: 67
- Buzos Mujer Talla XXS | $78.4 | Stock: 23
```

---

### **Opción 2: Desde el Backend API**

1. **Inicia el backend:**
```powershell
python main.py
```

2. **Abre el navegador:**
```
http://localhost:8000/docs
```

3. **Prueba el endpoint:**
- Clic en `GET /api/analytics/dashboard-resumen`
- Clic en "Try it out"
- Clic en "Execute"

**Verás:**
```json
{
  "resumen_general": {
    "total_productos": 864,
    "total_ventas_mes": 150,
    "alertas_activas": 45,
    "recomendaciones": 12
  },
  ...
}
```

---

## 🎯 **FLUJO COMPLETO PARA PROBAR**

### **Paso 1: Cargar Datos**
```powershell
cd BACKEND
.\venv\Scripts\Activate.ps1
python cargar_datos.py
```

### **Paso 2: Iniciar Backend**
```powershell
python main.py
```

### **Paso 3: Iniciar Frontend (Nueva terminal)**
```powershell
cd ..\frontend
npm run dev
```

### **Paso 4: Probar la Aplicación**
1. Abrir: http://localhost:5173
2. Login: `admin` / `admin123`
3. Dashboard cargará con datos reales
4. Probar:
   - 📊 Analytics → Aplicar filtros
   - 🧠 Patrones → Ver reglas descubiertas
   - ⚠️ Alertas → Ver productos con stock bajo

---

## 🔍 **VERIFICACIÓN VISUAL EN EL FRONTEND**

Cuando los datos estén cargados, verás:

### **Dashboard:**
- ✅ "Ventas Totales: 0" → Cambia a número real
- ✅ "Productos en Stock: 864"
- ✅ "Alertas Activas: ~45"
- ✅ Lista de productos destacados con nombres reales

### **Analytics:**
- ✅ Tabla con productos reales
- ✅ Filtros funcionando
- ✅ Grid de tallas con datos

### **Patrones:**
- ✅ Reglas descubiertas (ej: "CAMISETAS → JEANS 68%")
- ✅ Búsqueda de recomendaciones funciona

### **Alertas:**
- ✅ Cards con contadores reales
- ✅ Lista de productos con stock bajo
- ✅ Productos con stock 0 marcados como "CRÍTICO"

---

## ⚠️ **IMPORTANTE**

**SI VES NÚMEROS EN 0 O VACÍO:**

1. Verifica que el backend esté corriendo
2. Abre la consola del navegador (F12)
3. Ve a la pestaña "Network"
4. Refresca la página
5. Busca peticiones a `localhost:8000`
6. Si hay errores 401: Verifica la API Key
7. Si hay errores 500: Revisa logs del backend

---

## 📝 **COMANDOS RESUMIDOS**

```powershell
# TERMINAL 1 - Backend
cd BACKEND
.\venv\Scripts\Activate.ps1
python cargar_datos.py     # ✅ CARGAR DATOS
python main.py             # ✅ INICIAR BACKEND

# TERMINAL 2 - Frontend (nueva terminal)
cd frontend
npm run dev                # ✅ INICIAR FRONTEND

# NAVEGADOR
# http://localhost:5173
# Login: admin / admin123
```

---

**¡Listo para probar con datos reales!** 🎉✨

