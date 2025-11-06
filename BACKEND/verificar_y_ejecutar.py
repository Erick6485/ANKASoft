"""
Script de verificación y ejecución del backend
"""
import sys
import os

print("=" * 60)
print("VERIFICANDO SISTEMA BACKEND")
print("=" * 60)

# 1. Verificar imports críticos
print("\n1. Verificando imports...")
try:
    from database.connection import Base, engine, get_db
    print("   ✅ database.connection - OK")
except Exception as e:
    print(f"   ❌ database.connection - ERROR: {e}")
    sys.exit(1)

try:
    from database import models
    print("   ✅ database.models - OK")
except Exception as e:
    print(f"   ❌ database.models - ERROR: {e}")
    sys.exit(1)

try:
    from database import schemas
    print("   ✅ database.schemas - OK")
except Exception as e:
    print(f"   ❌ database.schemas - ERROR: {e}")
    sys.exit(1)

try:
    from utils import auth
    print("   ✅ utils.auth - OK")
except Exception as e:
    print(f"   ❌ utils.auth - ERROR: {e}")
    sys.exit(1)

# 2. Verificar routers
print("\n2. Verificando routers...")
routers_list = ['analytics', 'chatbot', 'auth', 'inventario', 'ventas', 'kpis', 'reportes']
for router_name in routers_list:
    try:
        __import__(f'routers.{router_name}')
        print(f"   ✅ routers.{router_name} - OK")
    except Exception as e:
        print(f"   ❌ routers.{router_name} - ERROR: {e}")
        sys.exit(1)

# 3. Verificar base de datos
print("\n3. Verificando base de datos...")
try:
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"   ✅ Base de datos conectada - {len(tables)} tablas encontradas")
    if tables:
        print(f"   📊 Tablas: {', '.join(tables)}")
except Exception as e:
    print(f"   ⚠️  Base de datos - WARNING: {e}")
    print("   ℹ️  Ejecuta: python migrar_base_datos.py")

# 4. Verificar FastAPI
print("\n4. Verificando FastAPI...")
try:
    from fastapi import FastAPI
    print("   ✅ FastAPI instalado - OK")
except Exception as e:
    print(f"   ❌ FastAPI - ERROR: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TODAS LAS VERIFICACIONES COMPLETADAS")
print("=" * 60)
print("\n🚀 Iniciando servidor...")
print("   URL: http://localhost:8000")
print("   Docs: http://localhost:8000/docs")
print("   Presiona Ctrl+C para detener\n")

# 5. Iniciar servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

