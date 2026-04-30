#!/usr/bin/env python3
"""
Script para verificar qué usuarios están registrados en la base de datos.
"""

import sys
sys.path.insert(0, './backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User

DATABASE_URL = "sqlite:///./backend/shoplatam_local.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
users = db.query(User).all()

print("📋 Usuarios registrados en la base de datos:\n")
if not users:
    print("❌ No hay usuarios registrados")
else:
    for user in users:
        print(f"  📧 Email: {user.email}")
        print(f"     Nombre: {user.full_name}")
        print(f"     Rol: {user.role}")
        print(f"     Activo: {user.is_active}")
        print()

db.close()
