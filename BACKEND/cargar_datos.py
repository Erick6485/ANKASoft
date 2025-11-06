"""
Script para cargar datos de ejemplo en la base de datos
Ejecutar con: python cargar_datos.py
"""

from database.connection import SessionLocal
from utils.data_loader import cargar_datos_ejemplo

def main():
    print("=" * 60)
    print("CARGADOR DE DATOS DE EJEMPLO")
    print("Retail Analytics API - Hackatón 2025")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    try:
        resultado = cargar_datos_ejemplo(db)
        if resultado:
            print()
            print("=" * 60)
            print(f"📊 Resumen:")
            print(f"   - Productos creados: {resultado['productos']}")
            print(f"   - Ventas creadas: {resultado['ventas']}")
            print("=" * 60)
            print()
            print("✅ Ahora puedes probar los endpoints en:")
            print("   http://localhost:8000/docs")
            print()
    except Exception as e:
        print(f"❌ Error al cargar datos: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()

