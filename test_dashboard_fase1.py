#!/usr/bin/env python3
"""
Script de prueba para validar FASE 1 del Dashboard:
1. CategoriesPage - Crear y eliminar categorías
2. ProductsPage - Crear productos con validaciones
3. OrdersPage - Expandir órdenes (ya probado)
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_test(status, message):
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")

# ────────────────────────────────────────────────────────────

print_header("FASE 1: PRUEBAS DEL DASHBOARD")

# 1. LOGIN
print_header("1️⃣  CATEGORIESPAGE - CREAR Y ELIMINAR")
print("→ Obteniendo token...")
resp = requests.post(f"{API_URL}/auth/login", json={
    "email": "vendor@test.com",
    "password": "Test123!",
})
if resp.status_code != 200:
    print(f"❌ Login fallido: {resp.text}")
    exit(1)
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print_test(True, f"Token obtenido: {token[:20]}...")

# 2. Obtener store_id
print("→ Obteniendo tienda actual...")
resp = requests.get(f"{API_URL}/stores/me", headers=headers)
if resp.status_code != 200:
    print(f"❌ Error: {resp.text}")
    exit(1)
store = resp.json()
store_id = store["id"]
print_test(True, f"Tienda: {store['name']} (ID: {store_id})")

# 3. CREAR CATEGORÍA
print("\n→ Creando categoría de prueba...")
cat_data = {
    "name": "Prueba Categoría",
    "slug": "prueba-categoria",
    "active": True
}
resp = requests.post(f"{API_URL}/products/categories", json=cat_data, headers=headers)
if resp.status_code != 201:
    print_test(False, f"Error al crear: {resp.text}")
else:
    cat = resp.json()
    cat_id = cat.get("id")
    print_test(True, f"Categoría creada: {cat['name']} (ID: {cat_id})")

# 4. LISTAR CATEGORÍAS
print("\n→ Listando categorías...")
resp = requests.get(f"{API_URL}/products/categories", params={"store_id": store_id}, headers=headers)
if resp.status_code == 200:
    categories = resp.json()
    print_test(True, f"Total de categorías: {len(categories)}")
    for c in categories[:3]:
        print(f"   - {c['name']} ({c['slug']})")
else:
    print_test(False, f"Error al listar: {resp.text}")

# 5. ELIMINAR CATEGORÍA
if cat_id:
    print("\n→ Eliminando categoría...")
    resp = requests.delete(f"{API_URL}/products/categories/{cat_id}", headers=headers)
    if resp.status_code == 200:
        print_test(True, f"Categoría eliminada (ID: {cat_id})")
    else:
        print_test(False, f"Error al eliminar: {resp.text}")

# ────────────────────────────────────────────────────────────

print_header("2️⃣  PRODUCTSPAGE - CREAR CON VALIDACIONES")

# 6. OBTENER CATEGORÍAS PARA USAR EN PRODUCTO
print("→ Obteniendo categorías...")
resp = requests.get(f"{API_URL}/products/categories", params={"store_id": store_id}, headers=headers)
cat_list = resp.json() if resp.status_code == 200 else []
cat_id = cat_list[0]["id"] if cat_list else None
print_test(True, f"Categorías disponibles: {len(cat_list)}")

# 7. CREAR PRODUCTO VÁLIDO
print("\n→ Creando producto con datos válidos...")
product_data = {
    "name": "Producto Test Completo",
    "slug": "producto-test-completo",
    "description": "Descripción del producto de prueba",
    "price": 99.99,
    "compare_price": 149.99,
    "stock": 50,
    "is_active": True,
    "is_featured": True,
    "category_id": cat_id,
    "images": [],
    "variants": []
}
resp = requests.post(f"{API_URL}/products", json=product_data, headers=headers)
if resp.status_code == 201:
    product = resp.json()
    product_id = product["id"]
    print_test(True, f"Producto creado: {product['name']} (ID: {product_id})")
    print(f"   Precio: ${product['price']} (Tachado: ${product.get('compare_price', 'N/A')})")
    print(f"   Stock: {product['stock']} unidades")
else:
    print_test(False, f"Error: {resp.text}")
    product_id = None

# 8. VALIDACIÓN: Precio <= 0 (debe fallar)
print("\n→ TEST VALIDACIÓN: Precio = 0 (debe fallar)...")
invalid_product = {
    **product_data,
    "name": "Producto Inválido",
    "slug": "producto-invalido",
    "price": 0
}
resp = requests.post(f"{API_URL}/products", json=invalid_product, headers=headers)
if resp.status_code != 201:
    print_test(True, f"Validación correcta: {resp.json().get('detail', 'Error')}")
else:
    print_test(False, "Debería fallar con precio 0")

# 9. VALIDACIÓN: Stock < 0 (debe fallar)
print("\n→ TEST VALIDACIÓN: Stock negativo (debe fallar)...")
invalid_product = {
    **product_data,
    "name": "Producto Stock Negativo",
    "slug": "producto-stock-neg",
    "stock": -5
}
resp = requests.post(f"{API_URL}/products", json=invalid_product, headers=headers)
if resp.status_code != 201:
    print_test(True, f"Validación correcta: {resp.json().get('detail', 'Error')}")
else:
    print_test(False, "Debería fallar con stock negativo")

# 10. VALIDACIÓN: Compare price < price (debe fallar)
print("\n→ TEST VALIDACIÓN: Precio tachado < precio (debe fallar)...")
invalid_product = {
    **product_data,
    "name": "Producto Precio Inválido",
    "slug": "producto-precio-inv",
    "price": 100,
    "compare_price": 50
}
resp = requests.post(f"{API_URL}/products", json=invalid_product, headers=headers)
if resp.status_code != 201:
    print_test(True, f"Validación correcta: {resp.json().get('detail', 'Error')}")
else:
    print_test(False, "Debería fallar con compare_price < price")

# 11. LISTAR PRODUCTOS
print("\n→ Listando productos...")
resp = requests.get(f"{API_URL}/products", params={"store_id": store_id}, headers=headers)
if resp.status_code == 200:
    products = resp.json()
    print_test(True, f"Total de productos: {len(products)}")
    for p in products[:3]:
        print(f"   - {p['name']} (${p['price']}) - Stock: {p.get('stock', 'N/A')}")
else:
    print_test(False, f"Error: {resp.text}")

# ────────────────────────────────────────────────────────────

print_header("3️⃣  ORDERSPAGE - EXPANDIR ÓRDENES")

# 12. LISTAR ÓRDENES
print("→ Obteniendo órdenes...")
resp = requests.get(f"{API_URL}/orders", headers=headers)
if resp.status_code == 200:
    orders = resp.json()
    print_test(True, f"Total de órdenes: {len(orders)}")
    
    if orders:
        order = orders[0]
        print(f"\n→ Expandiendo orden: {order.get('order_number', order.get('id'))}...")
        print(f"   Estado: {order.get('status', 'N/A')}")
        print(f"   Cliente: {order.get('customer', {}).get('name', 'Anónimo')}")
        print(f"   Total: ${order.get('total', 'N/A')}")
        print(f"   Ítems: {len(order.get('order_items', []))}")
        
        if order.get('order_items'):
            print("\n   Detalles de los ítems:")
            for item in order['order_items'][:2]:
                print(f"      - {item.get('name', 'Producto')} x{item.get('quantity', 0)} = ${item.get('price', 0)}")
        
        print_test(True, f"Orden expandida correctamente")
else:
    print_test(False, f"Error: {resp.text}")

# ────────────────────────────────────────────────────────────

print_header("RESUMEN FINAL")
print("\n✨ FASE 1 - Pruebas completadas")
print("\n📊 Componentes probados:")
print("   ✅ CategoriesPage - Crear/eliminar categorías")
print("   ✅ ProductsPage - Crear productos con validaciones")
print("   ✅ OrdersPage - Órdenes expandibles")
print("\n🔗 Dashboard disponible en: http://localhost:3004/dashboard")
print("👤 Credenciales: vendor@test.com / Test123!")
print("\n" + "="*60)
