"""
Script de verificación completa del proyecto
Verifica que todos los archivos esenciales existan y los imports sean correctos
"""

import os
import sys

def verificar_estructura():
    """Verifica que todos los archivos esenciales existan"""
    print("=" * 70)
    print("VERIFICACIÓN COMPLETA DEL PROYECTO")
    print("Retail Analytics Backend - Hackatón 2025")
    print("=" * 70)
    print()
    
    archivos_esenciales = {
        "Configuración Principal": [
            "main.py",
            "requirements.txt",
            ".gitignore",
            "README.md"
        ],
        "Scripts Útiles": [
            "cargar_datos.py",
            "migrar_base_datos.py"
        ],
        "Database": [
            "database/__init__.py",
            "database/connection.py",
            "database/models.py",
            "database/schemas.py"
        ],
        "Routers": [
            "routers/__init__.py",
            "routers/analytics.py",
            "routers/chatbot.py"
        ],
        "Services": [
            "services/__init__.py",
            "services/analytics_service.py",
            "services/chatbot_service.py",
            "services/association_rules.py"
        ],
        "Utils": [
            "utils/__init__.py",
            "utils/security.py",
            "utils/data_loader.py"
        ]
    }
    
    errores = []
    total_archivos = 0
    archivos_ok = 0
    
    for categoria, archivos in archivos_esenciales.items():
        print(f"\n[{categoria}]")
        for archivo in archivos:
            total_archivos += 1
            if os.path.exists(archivo):
                print(f"  ✅ {archivo}")
                archivos_ok += 1
            else:
                print(f"  ❌ {archivo} - FALTA")
                errores.append(f"Falta archivo: {archivo}")
    
    print()
    print("=" * 70)
    print(f"RESULTADO: {archivos_ok}/{total_archivos} archivos encontrados")
    print("=" * 70)
    
    if errores:
        print("\n❌ ERRORES ENCONTRADOS:")
        for error in errores:
            print(f"  - {error}")
        return False
    else:
        print("\n✅ TODOS LOS ARCHIVOS ESENCIALES ESTÁN PRESENTES")
        return True

def verificar_imports():
    """Verifica que los imports principales funcionen"""
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE IMPORTS")
    print("=" * 70)
    print()
    
    errores_import = []
    
    # Test 1: Database
    print("[1/7] Verificando database...")
    try:
        from database import models, connection, schemas
        print("  ✅ database OK")
    except Exception as e:
        print(f"  ❌ Error en database: {e}")
        errores_import.append(str(e))
    
    # Test 2: Services
    print("[2/7] Verificando services...")
    try:
        from services.analytics_service import AnalyticsService
        from services.chatbot_service import ChatbotService
        from services.association_rules import AssociationRulesService
        print("  ✅ services OK")
    except Exception as e:
        print(f"  ❌ Error en services: {e}")
        errores_import.append(str(e))
    
    # Test 3: Routers
    print("[3/7] Verificando routers...")
    try:
        from routers import analytics, chatbot
        print("  ✅ routers OK")
    except Exception as e:
        print(f"  ❌ Error en routers: {e}")
        errores_import.append(str(e))
    
    # Test 4: Utils
    print("[4/7] Verificando utils...")
    try:
        from utils.security import verify_api_key
        from utils.data_loader import cargar_datos_ejemplo
        print("  ✅ utils OK")
    except Exception as e:
        print(f"  ❌ Error en utils: {e}")
        errores_import.append(str(e))
    
    # Test 5: FastAPI
    print("[5/7] Verificando FastAPI...")
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        print("  ✅ FastAPI OK")
    except Exception as e:
        print(f"  ❌ Error en FastAPI: {e}")
        errores_import.append(str(e))
    
    # Test 6: SQLAlchemy
    print("[6/7] Verificando SQLAlchemy...")
    try:
        from sqlalchemy.orm import Session
        from sqlalchemy import func, extract
        print("  ✅ SQLAlchemy OK")
    except Exception as e:
        print(f"  ❌ Error en SQLAlchemy: {e}")
        errores_import.append(str(e))
    
    # Test 7: Main App
    print("[7/7] Verificando aplicación principal...")
    try:
        import main
        print("  ✅ main.py OK")
        print(f"  📝 Título: {main.app.title}")
        print(f"  📝 Versión: {main.app.version}")
        
        # Contar rutas
        rutas = [route.path for route in main.app.routes]
        print(f"  📝 Total de endpoints: {len(rutas)}")
        
    except Exception as e:
        print(f"  ❌ Error en main.py: {e}")
        errores_import.append(str(e))
    
    print()
    print("=" * 70)
    
    if errores_import:
        print("❌ ERRORES DE IMPORTACIÓN ENCONTRADOS")
        print("=" * 70)
        for error in errores_import:
            print(f"  - {error}")
        return False
    else:
        print("✅ TODOS LOS IMPORTS FUNCIONAN CORRECTAMENTE")
        print("=" * 70)
        return True

def verificar_dependencias():
    """Verifica que las dependencias críticas estén instaladas"""
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print("=" * 70)
    print()
    
    dependencias = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-dotenv"
    ]
    
    errores_deps = []
    
    for dep in dependencias:
        try:
            __import__(dep.replace("-", "_"))
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} - NO INSTALADO")
            errores_deps.append(dep)
    
    print()
    print("=" * 70)
    
    if errores_deps:
        print("❌ DEPENDENCIAS FALTANTES")
        print("=" * 70)
        print("\nEjecuta: pip install -r requirements.txt")
        return False
    else:
        print("✅ TODAS LAS DEPENDENCIAS INSTALADAS")
        print("=" * 70)
        return True

def resumen_endpoints():
    """Muestra resumen de endpoints disponibles"""
    print("\n" + "=" * 70)
    print("RESUMEN DE ENDPOINTS")
    print("=" * 70)
    print()
    
    try:
        import main
        
        analytics_count = 0
        chatbot_count = 0
        otros_count = 0
        
        for route in main.app.routes:
            if hasattr(route, 'path'):
                if '/api/analytics/' in route.path:
                    analytics_count += 1
                elif '/api/chatbot/' in route.path:
                    chatbot_count += 1
                else:
                    otros_count += 1
        
        print(f"  📊 Analytics:  {analytics_count} endpoints")
        print(f"  🤖 Chatbot:    {chatbot_count} endpoints")
        print(f"  📝 Otros:      {otros_count} endpoints")
        print(f"  ━" * 35)
        print(f"  📈 TOTAL:      {analytics_count + chatbot_count + otros_count} endpoints")
        
    except Exception as e:
        print(f"  ⚠️ No se pudo generar resumen: {e}")

def main_verificacion():
    print()
    
    # Verificaciones
    estructura_ok = verificar_estructura()
    imports_ok = verificar_imports()
    deps_ok = verificar_dependencias()
    resumen_endpoints()
    
    # Resultado final
    print("\n" + "=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print()
    
    if estructura_ok and imports_ok and deps_ok:
        print("✅✅✅ PROYECTO COMPLETAMENTE FUNCIONAL ✅✅✅")
        print()
        print("El proyecto está listo para:")
        print("  🚀 Ejecutar: python main.py")
        print("  📊 Cargar datos: python cargar_datos.py")
        print("  🌐 Acceder a: http://localhost:8000/docs")
        print()
        print("=" * 70)
        return 0
    else:
        print("❌ HAY PROBLEMAS QUE RESOLVER")
        print()
        if not estructura_ok:
            print("  ⚠️ Faltan archivos esenciales")
        if not imports_ok:
            print("  ⚠️ Hay errores de importación")
        if not deps_ok:
            print("  ⚠️ Faltan dependencias")
        print()
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main_verificacion())

