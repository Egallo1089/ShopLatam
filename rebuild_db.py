import os
import sys

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "backend", "shoplatam_local.db")

print("=" * 80)
print("♻️  RECONSTRUYENDO BASE DE DATOS Y USUARIOS DESDE CERO")
print("=" * 80)

# 1. Eliminar la base de datos vieja
if os.path.exists(DB_PATH):
    try:
        os.remove(DB_PATH)
        print("✅ Base de datos anterior eliminada correctamente.")
    except Exception as e:
        print(f"❌ ERROR: No se pudo eliminar la base de datos: {e}")
        print("\n⚠️  POR FAVOR DETÉN EL SERVIDOR BACKEND PRIMERO (Ctrl+C en la terminal) ⚠️")
        sys.exit(1)
else:
    print("✅ No había base de datos anterior (creando una nueva).")

# 2. Ejecutar main_local.py para crear todo de nuevo
print("\n⚙️  Generando nuevas tablas y usuarios genéricos...")
import subprocess

try:
    # Llamamos a main_local.py para que inicialice la base de datos con los datos semilla
    subprocess.run([sys.executable, "backend/main_local.py", "--seed-only"], check=True)
    print("\n" + "=" * 80)
    print("🎉 ÉXITO: Todo el sistema ha sido reseteado y purgado.")
    print("=" * 80)
    print("\nTus usuarios de prueba son:")
    print("👨‍💼 ADMIN:    admin@shoplatam.com  |  Admin2026!")
    print("🏪 VENDEDOR: demo@shoplatam.com   |  demo1234")
    print("\n👉 AHORA DEBES INICIAR TUS SERVIDORES NUEVAMENTE:")
    print("1. En una terminal: cd backend && python main_local.py")
    print("2. En otra terminal: cd frontend && npm run dev")
    print("\n(Nota: Si te sale 'Failed to fetch', significa que olvidaste iniciar el backend)")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Error al crear la base de datos: {e}")
