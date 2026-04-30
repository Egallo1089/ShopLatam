#!/usr/bin/env python3
"""
Script SIMPLE para crear nuevas credenciales através del API backend.
El backend debe estar ejecutándose en http://localhost:8000

Ejecutar: python create_new_user_via_api.py
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

print("=" * 80)
print("👤 CREADOR DE USUARIOS VÍA API SHOPLA TAM")
print("=" * 80)

# Verificar que el backend está activo
print("\n🔍 Verificando conexión al backend...")
try:
    resp = requests.get(f"{API_URL}/health", timeout=3)
    if resp.status_code == 200:
        print("  ✅ Backend activo en", API_URL)
    else:
        print("  ⚠️  Backend respondió con error:", resp.status_code)
except requests.exceptions.ConnectionError:
    print(f"\n❌ NO SE PUEDE CONECTAR A {API_URL}")
    print("\n⚠️  SOLUCIÓN: Abre otra terminal y ejecuta:")
    print("   python -m uvicorn backend.main_local:app --reload")
    print("\nLuego vuelve a ejecutar este script.")
    exit(1)

# Intentar crear usuario DEMO
print("\n📝 Creando usuario DEMO...")
demo_creds = {
    "email": "demo@shoplotam.com",
    "password": "demo1234",
    "full_name": "Demo Store Owner",
    "phone": "+593999999999"
}

resp = requests.post(f"{API_URL}/auth/register", json=demo_creds)
if resp.status_code in [200, 201]:
    print("  ✅ Email: demo@shoplotam.com")
    print("  ✅ Contraseña: demo1234")
elif resp.status_code == 400 and "ya está registrado" in resp.json().get("detail", ""):
    print("  ℹ️  Usuario DEMO ya existe ✅")
else:
    print(f"  ⚠️  Error: {resp.json()}")

time.sleep(0.5)

# Intentar crear usuario TEST
print("\n📝 Creando usuario TEST...")
test_creds = {
    "email": "vendor@test.com",
    "password": "Test123!",
    "full_name": "Test Vendor",
    "phone": "+593987654321"
}

resp = requests.post(f"{API_URL}/auth/register", json=test_creds)
if resp.status_code in [200, 201]:
    print("  ✅ Email: vendor@test.com")
    print("  ✅ Contraseña: Test123!")
elif resp.status_code == 400 and "ya está registrado" in resp.json().get("detail", ""):
    print("  ℹ️  Usuario TEST ya existe ✅")
else:
    print(f"  ⚠️  Error: {resp.json()}")

# Verificar login
print("\n🔐 VERIFICANDO CREDENCIALES:\n")

for creds in [demo_creds, test_creds]:
    email = creds["email"]
    password = creds["password"]
    login_data = {"email": email, "password": password}
    
    resp = requests.post(f"{API_URL}/auth/login", json=login_data)
    if resp.status_code == 200:
        print(f"  ✅ {email} - LOGIN EXITOSO")
    else:
        error = resp.json().get("detail", "Error desconocido")
        print(f"  ❌ {email} - {error}")

print("\n" + "=" * 80)
print("✅ CREDENCIALES LISTAS")
print("=" * 80)
print("\nAccede a: http://localhost:3004/dashboard")
print("\nCon cualquiera de estas credenciales:")
print("  📧 demo@shoplotam.com / demo1234")
print("  📧 vendor@test.com / Test123!")
print("\n")
