#!/usr/bin/env python3
"""Reiniciar servidor FastAPI"""
import os
import subprocess
import time
import psutil
import sys

def kill_process_on_port(port):
    """Matar el proceso que está escuchando en un puerto"""
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    print(f"Matando PID {proc.pid}...")
                    proc.kill()
                    proc.wait(timeout=3)
                    print(f"Proceso {proc.pid} matado")
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass
    return False

def start_server():
    """Iniciar el servidor FastAPI"""
    print("Iniciando servidor...")
    os.chdir(r"c:\Users\USUARIO 1\Desktop\AUTOFI\ShopLatam\backend")
    
    # Usar python -m uvicorn
    cmd = [
        sys.executable, 
        "-m", "uvicorn",
        "app.main_local:app",
        "--reload",
        "--port", "8000",
        "--host", "127.0.0.1"
    ]
    
    print(f"Comando: {' '.join(cmd)}")
    subprocess.Popen(cmd)
    time.sleep(2)
    print("✅ Servidor iniciado")

if __name__ == "__main__":
    print("🔄 Reiniciando servidor en puerto 8000...")
    kill_process_on_port(8000)
    time.sleep(2)
    try:
        start_server()
    except Exception as e:
        print(f"❌ Error: {e}")
