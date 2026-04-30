#!/usr/bin/env python3
"""
Script para crear datos de prueba en el backend.
Ejecutar: python test_orders.py
"""

import requests
import json
from datetime import datetime, timedelta

API_URL = "http://localhost:8000"

# 1. Register or login a test user
print("📝 [1/5] Registrando/Verificando usuario de prueba...")
user_data = {
    "email": "vendor@test.com",
    "password": "Test123!",
}

# Try to login first
resp = requests.post(f"{API_URL}/auth/login", json=user_data)
if resp.status_code == 200:
    print("  ✅ Usuario ya existe, login exitoso")
    user = resp.json()
else:
    # Try to register
    user_data["full_name"] = "Test Vendor"
    resp = requests.post(f"{API_URL}/auth/register", json=user_data)
    if resp.status_code != 200:
        print(f"  ❌ Error: {resp.text}")
        exit(1)
    print("  ✅ Usuario creado")
    user = resp.json()

token = user.get("access_token")
if not token:
    print(f"  ❌ No token: {user}")
    exit(1)
print(f"  ✅ Token obtenido: {token[:20]}...")

headers = {"Authorization": f"Bearer {token}"}

# 2. Get or create a test store
print("\n🏪 [2/5] Obteniendo/Creando tienda de prueba...")
resp = requests.get(f"{API_URL}/stores/me", headers=headers)
if resp.status_code == 200:
    print("  ✅ Tienda ya existe")
    store = resp.json()
    store_id = store["id"]
else:
    store_data = {
        "name": "Tienda Test",
        "slug": "tienda-test",
        "description": "Tienda de prueba para órdenes",
        "primary_color": "#E63B5A",
        "whatsapp_number": "+593987654321"
    }
    resp = requests.post(f"{API_URL}/stores", json=store_data, headers=headers)
    if resp.status_code != 201:
        print(f"  ❌ Error: {resp.text}")
        exit(1)
    store = resp.json()
    store_id = store["id"]
    print(f"  ✅ Tienda creada: {store['name']}")

print(f"  Store ID: {store_id}, Name: {store.get('name', 'Unknown')}")

# 3. Create test products
print("\n📦 [3/5] Creando productos de prueba...")
products = []
for i in range(3):
    product_data = {
        "name": f"Producto Test {i+1}",
        "slug": f"producto-test-{i+1}",
        "description": f"Descripción del producto {i+1}",
        "price": 50.00 + (i * 10),
        "old_price": 80.00 + (i * 10),
        "stock": 20,
        "category": "Prueba",
        "image_url": "https://via.placeholder.com/300"
    }
    resp = requests.post(f"{API_URL}/products", json=product_data, headers=headers)
    if resp.status_code != 201:
        print(f"  ❌ Error en producto {i+1}: {resp.text}")
    else:
        product = resp.json()
        products.append(product)
        print(f"  ✅ Producto {i+1} creado: {product['name']} (${product['price']})")

if not products:
    print("  ❌ No hay productos para crear órdenes")
    exit(1)

# 4. Create test orders
print("\n📋 [4/5] Creando órdenes de prueba...")
created_orders = []
statuses = ["nuevo", "confirmado", "preparando", "enviado", "entregado"]

for order_num in range(5):
    order_data = {
        "customer_data": {
            "name": f"Cliente Test {order_num+1}",
            "phone": f"+593987654{order_num:03d}",
            "email": f"cliente{order_num+1}@test.com",
            "address": f"Calle Test {order_num+1}, Apt {order_num+1}",
            "city": "Guayaquil"
        },
        "payment_method": "contra_entrega",
        "notes": f"Pedido de prueba #{order_num+1}",
        "items": [
            {
                "product_id": products[order_num % len(products)]["id"],
                "quantity": (order_num % 3) + 1,
                "unit_price": products[order_num % len(products)]["price"]
            }
        ]
    }
    
    # Create public order (without auth, through store slug)
    resp = requests.post(
        f"{API_URL}/orders/public/tienda-test",
        json=order_data
    )
    
    if resp.status_code != 201:
        print(f"  ❌ Error en orden {order_num+1}: {resp.text}")
    else:
        order = resp.json()
        created_orders.append(order)
        print(f"  ✅ Orden {order_num+1} creada: {order['order_number']} (${order['total']})")

# 5. Update some orders to different statuses
print("\n🔄 [5/5] Actualizando estados de órdenes...")
if created_orders:
    # Get orders with auth
    resp = requests.get(f"{API_URL}/orders", headers=headers)
    if resp.status_code == 200:
        orders = resp.json()
        for idx, order in enumerate(orders[:len(statuses)]):
            new_status = statuses[idx]
            resp = requests.patch(
                f"{API_URL}/orders/{order['id']}",
                json={"status": new_status},
                headers=headers
            )
            if resp.status_code == 200:
                print(f"  ✅ Orden #{order['order_number']} → {new_status}")
            else:
                print(f"  ⚠️  Error actualizando orden: {resp.text}")

print("\n✨ ¡Datos de prueba creados exitosamente!")
print(f"👤 Usuario: vendor@test.com / Test123!")
print(f"🏪 Tienda: tienda-test")
print(f"📊 Órdenes creadas: {len(created_orders)}")
print("\n🔗 Acceso al dashboard: http://localhost:3004/dashboard")
