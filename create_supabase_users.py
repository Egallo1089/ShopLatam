#!/usr/bin/env python3
"""
Script para crear usuarios en Supabase usando la API de admin.
Ejecutar: python create_supabase_users.py
"""

import requests
import json

# Credenciales de Supabase (del archivo .env del frontend)
SUPABASE_URL = "https://xhgrocxmtjkfcbstivgw.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_jx_ZmJSiVvR14KbdZwFtOQ__MB1SpkL"

print("=" * 80)
print("👤 CREADOR DE USUARIOS EN SUPABASE")
print("=" * 80)

# Intenta crear usuario usando el endpoint de signup
users_to_create = [
    {
        "email": "demo@example.com",
        "password": "demo1234",
        "full_name": "Demo Store Owner",
        "phone": "+593999999999"
    },
    {
        "email": "vendor@example.com",
        "password": "Test123!",
        "full_name": "Test Vendor",
        "phone": "+593987654321"
    }
]

for user in users_to_create:
    print(f"\n📝 Creando usuario: {user['email']}...")
    
    # Endpoint de signup de Supabase
    url = f"{SUPABASE_URL}/auth/v1/signup"
    
    payload = {
        "email": user["email"],
        "password": user["password"],
    }
    
    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_ANON_KEY,
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            print(f"  ✅ Usuario creado exitosamente")
            print(f"     Email: {user['email']}")
            print(f"     Contraseña: {user['password']}")
        elif resp.status_code == 422:
            error_msg = resp.json().get("error_description", "Unknown error")
            if "already registered" in error_msg:
                print(f"  ℹ️  El usuario ya existe ✅")
            else:
                print(f"  ⚠️ Error: {error_msg}")
        else:
            print(f"  ❌ Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")

print("\n" + "=" * 80)
print("📝 CREDENCIALES")
print("=" * 80)
print("\nUsa estas credenciales en http://localhost:3004/dashboard:")
print("\n  📧 demo@shoplotam.com / demo1234")
print("  📧 vendor@test.com / Test123!")
print("\n")
