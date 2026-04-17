#!/usr/bin/env python3
"""
Script para verificar qué usuarios existen en Supabase intentando login.
Ejecutar: python verify_supabase_users.py
"""

import requests
import json

# Credenciales de Supabase
SUPABASE_URL = "https://xhgrocxmtjkfcbstivgw.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_jx_ZmJSiVvR14KbdZwFtOQ__MB1SpkL"

print("=" * 80)
print("🔐 VERIFICADOR DE USUARIOS EN SUPABASE")
print("=" * 80)

users_to_test = [
    {"email": "demo@example.com", "password": "demo1234"},
    {"email": "vendor@example.com", "password": "Test123!"},
    {"email": "demo@shoplotam.com", "password": "demo1234"},
    {"email": "vendor@test.com", "password": "Test123!"},
    {"email": "test@test.com", "password": "Test123!"},
    {"email": "admin@admin.com", "password": "admin123"},
]

url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"

headers = {
    "Content-Type": "application/json",
    "apikey": SUPABASE_ANON_KEY,
}

print("\n🔍 Intentando login con diferentes credenciales...\n")

for user in users_to_test:
    payload = {
        "email": user["email"],
        "password": user["password"],
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if resp.status_code == 200:
            print(f"  ✅ {user['email']} / {user['password']}")
            print(f"     USUARIO ENCONTRADO - LOGIN EXITOSO")
        elif resp.status_code == 400:
            error = resp.json().get("error_description", "")
            if "Invalid login credentials" in error or "Duplicate registration" in error:
                print(f"  ❌ {user['email']} - Usuario no existe o credenciales incorrectas")
            else:
                print(f"  ⚠️  {user['email']} - {error}")
        else:
            print(f"  ⚠️  {user['email']} - Error {resp.status_code}")
    except Exception as e:
        print(f"  ⚠️  {user['email']} - Error: {e}")

print("\n" + "=" * 80)
