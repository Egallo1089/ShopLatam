import os
import sys

# Asegurar que importamos desde el backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import SessionLocal
from app.models.user import User, UserRole, SellerStatus
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

print("=" * 80)
print("🔐 RESETEANDO USUARIOS Y CONTRASEÑAS (COMPATIBLE CON FASTAPI)")
print("=" * 80)

db = SessionLocal()

try:
    # 1. Resetear Admin
    admin = db.query(User).filter(User.email == "admin@shoplatam.com").first()
    if not admin:
        print("Creando SuperAdmin...")
        admin = User(
            email="admin@shoplatam.com",
            full_name="Administrador ShopLatam",
            hashed_password=hash_password("Admin2026!"),
            role=UserRole.superadmin,
            phone="+593999000000",
            is_active=True,
            seller_status=None,
        )
        db.add(admin)
    else:
        print("Actualizando SuperAdmin existente...")
        admin.hashed_password = hash_password("Admin2026!")
        admin.role = UserRole.superadmin
        admin.is_active = True
    
    # 2. Resetear Vendedor Demo
    demo = db.query(User).filter(User.email == "demo@shoplatam.com").first()
    if not demo:
        print("Creando Vendedor Demo...")
        demo = User(
            email="demo@shoplatam.com",
            full_name="Eduardo Gallo",
            hashed_password=hash_password("demo1234"),
            role=UserRole.vendedor,
            phone="+593999999999",
            is_active=True,
            seller_status=SellerStatus.approved,
        )
        db.add(demo)
    else:
        print("Actualizando Vendedor Demo existente...")
        demo.hashed_password = hash_password("demo1234")
        demo.role = UserRole.vendedor
        demo.is_active = True

    # 3. Eliminar otros usuarios de prueba si es necesario
    otros = db.query(User).filter(User.email.not_in(["admin@shoplatam.com", "demo@shoplatam.com"])).all()
    for u in otros:
        print(f"Borrando usuario de pruebas antiguo: {u.email}")
        db.delete(u)

    db.commit()
    
    print("\n" + "=" * 80)
    print("✅ CREDENCIALES RESETEADAS CON ÉXITO")
    print("=" * 80)
    print("\n🚀 AHORA PUEDES INICIAR SESIÓN CON:")
    print("\n  Para Administrador (http://localhost:3000/admin):")
    print("    Email: admin@shoplatam.com")
    print("    Contraseña: Admin2026!")
    print("\n  Para Vendedor (http://localhost:3000/dashboard):")
    print("    Email: demo@shoplatam.com")
    print("    Contraseña: demo1234")
    print("\n")

except Exception as e:
    db.rollback()
    print(f"\n❌ Error al resetear: {e}")
finally:
    db.close()
