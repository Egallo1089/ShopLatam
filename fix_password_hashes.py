#!/usr/bin/env python3
"""
Script para actualizar los hashes de contraseña directamente en SQLite.
Usa bcrypt para crear hashes válidos.
"""

import sqlite3
import subprocess
import sys

# Instalar bcrypt si no existe
try:
    import bcrypt
except ImportError:
    print("📦 Instalando bcrypt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bcrypt", "-q"])
    import bcrypt

def hash_password(password: str) -> str:
    """Hashear contraseña con bcrypt (compatible con passlib)"""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

db_path = "backend/shoplatam_local.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 80)
    print("🔐 ACTUALIZANDO HASHES DE CONTRASEÑA")
    print("=" * 80)

    # Actualizar usuario DEMO
    demo_hash = hash_password("demo1234")
    cursor.execute(
        "UPDATE users SET hashed_password = ? WHERE email = ?",
        (demo_hash, "demo@shoplatam.com")
    )
    print("\n✅ Usuario DEMO actualizado")
    print("   Email: demo@shoplatam.com")
    print("   Contraseña: demo1234")

    # Actualizar usuario TEST
    test_hash = hash_password("Test123!")
    cursor.execute(
        "UPDATE users SET hashed_password = ? WHERE email = ?",
        (test_hash, "vendor@test.com")
    )
    print("\n✅ Usuario TEST actualizado")
    print("   Email: vendor@test.com")
    print("   Contraseña: Test123!")

    conn.commit()

    # Verificar que se actualizaron
    cursor.execute("SELECT email, hashed_password FROM users ORDER BY id")
    users = cursor.fetchall()
    
    print("\n" + "=" * 80)
    print("📋 USUARIOS EN LA BASE DE DATOS:")
    print("=" * 80)
    for email, hashed_pw in users:
        print(f"\n📧 {email}")
        print(f"   Hash: {hashed_pw[:50]}...")
        print(f"   Long: {len(hashed_pw)} caracteres")

    conn.close()

    print("\n" + "=" * 80)
    print("✅ CREDENCIALES ACTUALIZADAS CORRECTAMENTE")
    print("=" * 80)
    print("\n🚀 AHORA PUEDES LOGIN CON:")
    print("\n  Opción 1 (Demo):")
    print("    Email: demo@shoplotam.com")
    print("    Contraseña: demo1234")
    print("\n  Opción 2 (Test):")
    print("    Email: vendor@test.com")
    print("    Contraseña: Test123!")
    print("\n📍 URL: http://localhost:3004/dashboard")
    print("\n")

except sqlite3.OperationalError as e:
    print(f"\n❌ Error: {e}")
    print("\n⚠️ La base de datos puede estar corrupta.")
    print("Intenta eliminarla y reiniciar el backend:\n")
    print("  python reset_db.py   # Script alternativo")
    exit(1)
