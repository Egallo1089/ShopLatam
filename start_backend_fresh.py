#!/usr/bin/env python3
import subprocess
import os
import time
import socket

def port_in_use(port):
    """Verificar si puerto está en uso"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def kill_by_port(port):
    """Matar proceso en puerto con taskkill"""
    import subprocess
    result = subprocess.run(
        f'for /f "tokens=5" %a in (\'netstat -ano ^| findstr ":{port}"\') do taskkill /PID %a /F',
        shell=True,
        capture_output=True
    )
    return result.returncode == 0

# Matar servidor viejo
print("🛑 Matando servidor antigu...")
os.chdir(r"c:\Users\USUARIO 1\Desktop\AUTOFI\ShopLatam")
kill_by_port(8000)
time.sleep(2)

# Verificar puerto libre
if port_in_use(8000):
    print("❌ Puerto 8000 aún está en uso")
    exit(1)

print("✅ Puerto liberado")

# Iniciar nuevo servidor
print("\n🚀 Iniciando nuevo servidor...")
log_file = open("server.log", "w")

cmd = [
    "python",
    "-m", "uvicorn",
    "backend.app.main_local:app",
    "--reload",
    "--port", "8000",
    "--host", "127.0.0.1"
]

proc = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT)
print(f"📋 PID: {proc.pid}")
print(f"📝 Logs en: server.log")

time.sleep(3)

# Verificar si está vivo
if port_in_use(8000):
    print(" ✅ Servidor iniciado correctamente")
else:
    print("❌ Servidor no respondió")
    log_file.close()
    with open("server.log", "r") as f:
        print(f.read())
