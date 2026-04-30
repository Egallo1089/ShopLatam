#!/usr/bin/env python3
"""
Script para probar credenciales en el API backend.
Ejecutar: python verify_credentials.py
"""

import requests
import json

API_URL = "http://localhost:8000"

# Credenciales a probar
test_credentials = [
    {"email": "vendor@test.com", "password": "Test123!"},
    {"email": "admin@shop.com", "password": "admin123"},
    {"email": "test@example.com", "password": "Test123!"},
]

print("🔐 Verificando credenciales en el API backend...\n")

for creds in test_credentials:
    print(f"Probando: {creds['email']} / {creds['password']}")
    try:
        resp = requests.post(f"{API_URL}/auth/login", json=creds, timeout=5)
        if resp.status_code == 200:
            print(f"  ✅ LOGIN EXITOSO")
            data = resp.json()
            print(f"     Token: {data.get('access_token', 'N/A')[:30]}...")
        else:
            print(f"  ❌ Error {resp.status_code}: {resp.json().get('detail', 'Unknown')}")
    except requests.exceptions.ConnectionError:
        print(f"  ❌ No se puede conectar al servidor en {API_URL}")
        break
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

print("\n📝 Si ninguna credencial funciona, puedes registrar una nueva:")
print("  curl -X POST http://localhost:8000/auth/register -H 'Content-Type: application/json' -d '")
print('    {"email":"nuevousuario@test.com","password":"Tu_Password123","full_name":"Tu Nombre"}"')
