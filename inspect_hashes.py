#!/usr/bin/env python3
"""
Script para inspeccionar los hashes de contraseña y verificar si las credenciales funcionan.
"""

import sqlite3
import os

db_path = "backend/shoplatam_local.db"

if not os.path.exists(db_path):
    print(f"❌ Base de datos no encontrada: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("🔐 VERIFICACIÓN DE HASHES Y CREDENCIALES EN LA BASE DE DATOS")
print("=" * 80)

try:
    cursor.execute("""
        SELECT id, email, full_name, hashed_password, is_active 
        FROM users 
        ORDER BY id
    """)
    users = cursor.fetchall()
    
    if not users:
        print("\n❌ NO HAY USUARIOS EN LA BASE DE DATOS\n")
    else:
        print(f"\n✅ Encontrados {len(users)} usuario(s):\n")
        for user_id, email, full_name, hashed_pw, is_active in users:
            print(f"  ID: {user_id}")
            print(f"  📧 Email: {email}")
            print(f"  👤 Nombre: {full_name}")
            print(f"  🔒 Hash (primeros 50 chars): {hashed_pw[:50]}...")
            print(f"  ✅ Activo: {'Sí' if is_active else 'No'}")
            print(f"  Hash Length: {len(hashed_pw)} caracteres")
            print()
            
except sqlite3.OperationalError as e:
    print(f"❌ Error al consultar: {e}")

conn.close()

print("\n" + "=" * 80)
print("📝 INSTRUCCIONES PARA ARREGLAR LAS CREDENCIALES:")
print("=" * 80)
print("""
OPCIÓN 1: Resetear la base de datos completamente
  1. Elimina: backend/shoplatam_local.db
  2. Vuelve a ejecutar el backend (creará nueva BD con seed)
  
OPCIÓN 2: Crear un nuevo usuario manualmente verificado
  1. Ejecuta: python create_test_user.py
  2. Te mostrará las credenciales que se crearon
  
OPCIÓN 3: Verificar en el API directamente
  1. Abre: http://localhost:8000/docs
  2. Expande el endpoint POST /auth/register
  3. Crea un usuario nuevo desde allí

¿Cuál prefieres intentar?
""")
