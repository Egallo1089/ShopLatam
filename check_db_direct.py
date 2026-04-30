#!/usr/bin/env python3
"""
Script para inspeccionar la base de datos SQLite directamente.
Ejecutar: python check_db_direct.py
"""

import sqlite3
import os

db_path = "backend/shoplatam_local.db"

if not os.path.exists(db_path):
    print(f"❌ Base de datos no encontrada: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 70)
print("📋 USUARIO EN LA BASE DE DATOS")
print("=" * 70)

try:
    cursor.execute("SELECT id, email, full_name, is_active, role FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("❌ NO HAY USUARIOS EN LA BASE DE DATOS\n")
    else:
        print(f"\n✅ Encontrados {len(users)} usuario(s):\n")
        for idx, (user_id, email, full_name, is_active, role) in enumerate(users, 1):
            print(f"  {idx}. Email: {email}")
            print(f"     Nombre: {full_name}")
            print(f"     Rol: {role}")
            print(f"     Activo: {'Sí' if is_active else 'No'}")
            print()
            
except sqlite3.OperationalError as e:
    print(f"❌ Error al consultar tabla 'user': {e}")
    print("\n📊 Tablas disponibles:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")

conn.close()
