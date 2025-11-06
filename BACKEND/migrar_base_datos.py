"""
Script para migrar la base de datos a la nueva estructura
con modelo de Sucursales
"""

import os
from database.connection import engine, Base
from database import models
from sqlalchemy import inspect

def migrar_base_datos():
    print("=" * 60)
    print("MIGRACIÓN DE BASE DE DATOS")
    print("Retail Analytics - Hackatón 2025")
    print("=" * 60)
    print()
    
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    print(f"Base de datos: {DATABASE_URL}")
    print()
    
    # Verificar si es SQLite o PostgreSQL
    es_sqlite = "sqlite" in DATABASE_URL.lower()
    
    print("⚠️  ADVERTENCIA:")
    print("Este script eliminará TODAS las tablas y datos existentes.")
    print("Solo usar en desarrollo/demo.")
    print()
    
    respuesta = input("¿Deseas continuar? (s/n): ")
    
    if respuesta.lower() != 's':
        print("❌ Migración cancelada")
        return
    
    print()
    print("[1/3] Eliminando tablas existentes...")
    try:
        # Eliminar todas las tablas
        Base.metadata.drop_all(bind=engine)
        print("✅ Tablas eliminadas")
    except Exception as e:
        print(f"⚠️  Error al eliminar tablas: {e}")
        print("Continuando...")
    
    print()
    print("[2/3] Creando nuevas tablas...")
    try:
        # Crear todas las tablas con la nueva estructura
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas:")
        
        # Listar tablas creadas
        inspector = inspect(engine)
        for table_name in inspector.get_table_names():
            print(f"   - {table_name}")
        
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return
    
    print()
    print("[3/3] Información de carga de datos...")
    print()
    print("=" * 60)
    print("MIGRACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("Próximos pasos:")
    print("1. Ejecutar: python cargar_datos.py")
    print("   O usar el endpoint: POST /api/analytics/cargar-datos-ejemplo")
    print()
    print("2. Iniciar servidor: python main.py")
    print()
    print("3. Probar chatbot en: http://localhost:8000/docs")
    print("   Endpoint: POST /api/chatbot/mensaje")
    print()
    print("=" * 60)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    migrar_base_datos()

