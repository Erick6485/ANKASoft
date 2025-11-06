"""
Script de inicialización de la base de datos para producción
Se ejecuta automáticamente al desplegar
"""
from database.connection import engine
from database import models
from database.connection import SessionLocal
from utils.data_loader import cargar_datos_ejemplo

print("=" * 60)
print("INICIALIZANDO BASE DE DATOS EN PRODUCCIÓN")
print("=" * 60)

# Crear todas las tablas
print("\n1. Creando tablas...")
models.Base.metadata.create_all(bind=engine)
print("   ✅ Tablas creadas")

# Cargar datos de ejemplo
print("\n2. Cargando datos de ejemplo...")
db = SessionLocal()
try:
    resultado = cargar_datos_ejemplo(db)
    print(f"   ✅ Datos cargados: {resultado}")
except Exception as e:
    print(f"   ⚠️ Datos ya existentes o error: {e}")
finally:
    db.close()

print("\n" + "=" * 60)
print("✅ BASE DE DATOS LISTA PARA PRODUCCIÓN")
print("=" * 60)

