import requests

API_KEY = "retail_hackaton_2025_fup"
BASE_URL = "http://localhost:8000"

print("=" * 60)
print("PROBANDO ALGORITMO DE PATRONES DE COMPRA (APRIORI)")
print("=" * 60)

# Probar con diferentes parámetros
parametros = [
    (0.4, 0.05, "Parámetros normales"),
    (0.3, 0.03, "Parámetros más bajos"),
    (0.2, 0.01, "Parámetros muy bajos"),
]

for conf, sop, desc in parametros:
    print(f"\n📊 {desc}:")
    print(f"   Confianza mínima: {conf*100}%")
    print(f"   Soporte mínimo: {sop*100}%")
    
    try:
        url = f"{BASE_URL}/api/analytics/reglas-asociacion?confianza_minima={conf}&soporte_minimo={sop}"
        response = requests.get(url, headers={"X-API-Key": API_KEY})
        
        if response.status_code == 200:
            data = response.json()
            total_reglas = data.get("total_reglas", 0)
            reglas = data.get("reglas", [])
            
            print(f"   ✅ Reglas encontradas: {total_reglas}")
            
            if reglas:
                print(f"\n   🔍 Ejemplo de regla:")
                regla = reglas[0]
                print(f"      {regla['antecedente']} → {regla['consecuente']}")
                print(f"      Confianza: {regla['confianza']}%")
                print(f"      Soporte: {regla['soporte']}%")
                break  # Encontramos reglas, salir
        else:
            print(f"   ❌ Error {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("EXPLICACIÓN DEL ALGORITMO APRIORI")
print("=" * 60)
print("""
🧠 CÓMO FUNCIONA:

1. El algoritmo analiza las VENTAS agrupadas por día y sucursal
2. Busca productos que se venden JUNTOS en la misma transacción
3. Calcula dos métricas:
   - SOPORTE: ¿Qué % de ventas incluyen ambos productos?
   - CONFIANZA: ¿Qué % de clientes que compran A también compran B?

4. Solo muestra reglas con soporte y confianza por encima de los umbrales

⚠️ SI NO HAY REGLAS:
- Las ventas están distribuidas en diferentes días/sucursales
- No hay suficiente coincidencia de productos en las mismas transacciones
- Necesitas más datos o parámetros más bajos

💡 SOLUCIÓN:
- Bajar los umbrales en el código del frontend
- O generar más ventas con productos relacionados
""")

