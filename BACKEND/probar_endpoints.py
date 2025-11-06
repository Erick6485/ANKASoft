"""
Script para probar los endpoints del backend
"""
import requests

API_KEY = "retail_hackaton_2025_fup"
BASE_URL = "http://localhost:8000"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print("=" * 60)
print("PROBANDO ENDPOINTS DEL BACKEND")
print("=" * 60)

# Probar endpoints
endpoints = [
    ("GET", "/api/kpis/dashboard", "Dashboard de KPIs"),
    ("GET", "/api/ventas/dashboard-ventas", "Dashboard de Ventas"),
    ("GET", "/api/inventario/dashboard-inventario", "Dashboard de Inventario"),
    ("GET", "/api/analytics/dashboard-resumen", "Dashboard General"),
    ("GET", "/api/analytics/alertas-stock", "Alertas de Stock"),
]

for method, endpoint, nombre in endpoints:
    try:
        print(f"\n📡 Probando: {nombre}")
        print(f"   Endpoint: {method} {endpoint}")
        
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code} OK")
            print(f"   📊 Datos recibidos: {len(str(data))} caracteres")
            
            # Mostrar preview de datos
            if isinstance(data, dict):
                for key in list(data.keys())[:3]:
                    print(f"      - {key}: {str(data[key])[:80]}...")
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print("\n✅ Si todos los endpoints responden con 200 OK,")
print("   el backend está funcionando correctamente.")
print("\n🌐 Ahora prueba el frontend en: http://localhost:5173")
print("   Login: admin / admin123\n")

