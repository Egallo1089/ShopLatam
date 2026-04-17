#!/usr/bin/env python3
"""Diagnóstico completo del flujo de autenticación"""
import requests
import json
import sys

API_URL = "http://localhost:8000"

def test_login():
    """Test POST /auth/login"""
    print("\n" + "="*60)
    print("1️⃣  PROBANDO POST /auth/login")
    print("="*60)
    
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": "demo@shoplotam.com",
                "password": "demo1234"
            },
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}\n")
        print(f"Body:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"\n✅ LOGIN OK - Token: {token[:50]}...")
            return token
        else:
            print(f"\n❌ LOGIN FAILED - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def test_auth_me(token):
    """Test GET /auth/me"""
    print("\n" + "="*60)
    print("2️⃣  PROBANDO GET /auth/me")
    print("="*60)
    
    if not token:
        print("❌ Sin token, saltando...")
        return
    
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}\n")
        print(f"Body:\n{response.text[:500]}")
        
        if response.status_code == 200:
            print(f"\n✅ /auth/me OK")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"\n❌ /auth/me FAILED - Status {response.status_code}")
            try:
                print(f"Error: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Body: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_debug_token(token):
    """Test debug endpoint"""
    print("\n" + "="*60)
    print("2.5️⃣  PROBANDO DEBUG /auth/debug/token-info")
    print("="*60)
    
    if not token:
        print("❌ Sin token, saltando...")
        return
    
    try:
        response = requests.get(
            f"{API_URL}/auth/debug/token-info?token={token}",
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_cors_headers():
    """Verificar CORS"""
    print("\n" + "="*60)
    print("3️⃣  VERIFICANDO CORS HEADERS")
    print("="*60)
    
    try:
        response = requests.get(
            f"{API_URL}/docs",  # Docs siempre está disponible
            headers={"Origin": "http://localhost:3004"},
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        cors_headers = {k: v for k, v in response.headers.items() if 'access-control' in k.lower()}
        
        if cors_headers:
            print("CORS Headers encontrados:")
            for k, v in cors_headers.items():
                print(f"  {k}: {v}")
        else:
            print("⚠️  No se encontraron headers CORS")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    print("🔍 DIAGNÓSTICO DE AUTENTICACIÓN - ShopLatam")
    print(f"API URL: {API_URL}\n")
    
    # Test CORS
    test_cors_headers()
    
    # Test Login
    token = test_login()
    
    # Test debug token
    if token:
        test_debug_token(token)
    
    # Test /auth/me
    if token:
        test_auth_me(token)
    
    print("\n" + "="*60)
    print("✅ Diagnóstico completado")
    print("="*60)

if __name__ == "__main__":
    main()
