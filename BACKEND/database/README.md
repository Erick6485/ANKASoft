# Base de Datos - Retail Analytics

Este directorio contiene los archivos relacionados con la base de datos del proyecto.

## 📁 Archivos

- **`export_schema.sql`** - Esquema completo de la base de datos (estructura de tablas)
- **`sample_data.sql`** - Datos de ejemplo (opcional, para referencia)

## 🗄️ Estructura de la Base de Datos

### Tabla: `productos`
- **id** - PRIMARY KEY (SERIAL)
- **nombre** - VARCHAR(100)
- **categoria** - VARCHAR(50)
- **genero_cliente** - VARCHAR(10) - 'mujer', 'hombre', 'niño', 'niña'
- **talla** - VARCHAR(10)
- **precio** - FLOAT
- **stock_actual** - INTEGER
- **stock_minimo** - INTEGER

### Tabla: `ventas`
- **id** - PRIMARY KEY (SERIAL)
- **producto_id** - FOREIGN KEY → productos.id
- **fecha** - DATE
- **cantidad** - INTEGER
- **sucursal** - VARCHAR(50)
- **total** - FLOAT

## 🔧 Crear la Base de Datos

### Opción 1: Automático (Recomendado)
Las tablas se crean automáticamente cuando ejecutas la aplicación FastAPI:

```bash
python main.py
```

SQLAlchemy creará las tablas usando el esquema definido en `models.py`.

### Opción 2: Manual
Si prefieres crearlo manualmente:

```bash
# Crear base de datos
createdb -U postgres retail_analytics

# Ejecutar esquema
psql -U postgres -d retail_analytics -f export_schema.sql
```

## 📤 Exportar Base de Datos

Para generar el archivo `export_schema.sql`:

```bash
# Windows
.\database\export_database.bat

# Linux/Mac
chmod +x database/export_database.sh
./database/export_database.sh
```

O manualmente:

```bash
pg_dump -U postgres -d retail_analytics --schema-only --no-owner --no-privileges > database/export_schema.sql
```

## 📥 Importar Base de Datos

Para restaurar desde el esquema:

```bash
psql -U postgres -d retail_analytics -f database/export_schema.sql
```

## 🔄 Cargar Datos de Ejemplo

Después de crear las tablas, carga datos de ejemplo:

```bash
# Opción 1: Script Python
python cargar_datos.py

# Opción 2: Endpoint API
# POST http://localhost:8000/api/analytics/cargar-datos-ejemplo
```

Esto cargará:
- ~300+ productos
- 500 ventas históricas
- 4 sucursales diferentes

## 🔍 Verificar Datos

```sql
-- Conectar a la base de datos
\c retail_analytics

-- Ver tablas
\dt

-- Contar productos
SELECT COUNT(*) FROM productos;

-- Contar ventas
SELECT COUNT(*) FROM ventas;

-- Ver primeros 5 productos
SELECT * FROM productos LIMIT 5;

-- Top productos más vendidos
SELECT p.nombre, SUM(v.cantidad) as total
FROM ventas v
JOIN productos p ON v.producto_id = p.id
GROUP BY p.nombre
ORDER BY total DESC
LIMIT 10;
```

## 📝 Notas Importantes

1. **No subir `.env`** - El archivo `.env` con contraseñas NO debe subirse a Git
2. **Solo esquema** - El archivo `export_schema.sql` contiene solo la estructura, no datos sensibles
3. **Datos de ejemplo** - Los datos se generan con el script `cargar_datos.py`
4. **Migraciones** - SQLAlchemy maneja las migraciones automáticamente

## 🔐 Seguridad

- ✅ `export_schema.sql` - Seguro para Git (solo estructura)
- ✅ `sample_data.sql` - Seguro para Git (solo datos de ejemplo)
- ❌ `.env` - NO subir a Git (contiene credenciales)
- ❌ Backups completos - NO subir a Git (contienen datos reales)

## 📚 Recursos

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [pg_dump Documentation](https://www.postgresql.org/docs/current/app-pgdump.html)

