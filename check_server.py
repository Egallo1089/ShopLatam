#!/usr/bin/env python3
import requests

try:
    r = requests.get('http://localhost:8000/docs', timeout=2)
    print(f'✅ Servidor activo - HTTP {r.status_code}')
except:
    print('❌ Servidor caído - No responde')
