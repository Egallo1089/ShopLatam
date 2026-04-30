#!/usr/bin/env python3
import sqlite3
import bcrypt
import json
from pathlib import Path

db_path = Path(__file__).parent / "backend" / "shoplatam_local.db"
conn = sqlite3.connect(str(db_path))
c = conn.cursor()

# Crear tablas
c.execute("CREATE TABLE user (id INTEGER PRIMARY KEY, email TEXT UNIQUE, full_name TEXT, hashed_password TEXT, phone TEXT, role TEXT, is_active BOOLEAN)")
c.execute("CREATE TABLE store (id INTEGER PRIMARY KEY, owner_id INTEGER, name TEXT, slug TEXT UNIQUE, description TEXT, whatsapp_number TEXT, primary_color TEXT, is_active BOOLEAN)")
c.execute("CREATE TABLE category (id INTEGER PRIMARY KEY, store_id INTEGER, name TEXT, slug TEXT, position INTEGER)")
c.execute("CREATE TABLE product (id INTEGER PRIMARY KEY, store_id INTEGER, category_id INTEGER, name TEXT, slug TEXT, description TEXT, price REAL, compare_price REAL, stock INTEGER, images TEXT, is_active BOOLEAN)")

# Hashear contraseñas
pwd1 = bcrypt.hashpw(b"demo1234", bcrypt.gensalt()).decode()
pwd2 = bcrypt.hashpw(b"Test123!", bcrypt.gensalt()).decode()

# Insertar usuarios
c.execute("INSERT INTO user (email, full_name, hashed_password, phone, role, is_active) VALUES (?, ?, ?, ?, ?, ?)", 
          ("demo@shoplatam.com", "Demo Owner", pwd1, "+593999999999", "vendedor", 1))
u1 = c.lastrowid

c.execute("INSERT INTO user (email, full_name, hashed_password, phone, role, is_active) VALUES (?, ?, ?, ?, ?, ?)",
          ("vendor@test.com", "Test Vendor", pwd2, "+593987654321", "vendedor", 1))
u2 = c.lastrowid

# Insertar tiendas
c.execute("INSERT INTO store (owner_id, name, slug, description, whatsapp_number, primary_color, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
          (u1, "Demo Store", "demo-store", "Demo", "+593999999999", "#6366f1", 1))
s1 = c.lastrowid

c.execute("INSERT INTO store (owner_id, name, slug, description, whatsapp_number, primary_color, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
          (u2, "Test Store", "test-store", "Test", "+593987654321", "#E63B5A", 1))
s2 = c.lastrowid

# Insertar categoría
c.execute("INSERT INTO category (store_id, name, slug, position) VALUES (?, ?, ?, ?)",
          (s1, "Ropa", "ropa", 0))
cat = c.lastrowid

# Insertar productos
products = [
    ("Camiseta", "camiseta", "Premium", 25.99, 35.00, 50),
    ("Pantalón", "pantalon", "Jogger", 49.99, 65.00, 30),
    ("Zapatillas", "zapatillas", "Urbanas", 79.99, 119.00, 20),
]

for name, slug, desc, price, cp, stock in products:
    c.execute("INSERT INTO product (store_id, category_id, name, slug, description, price, compare_price, stock, images, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (s1, cat, name, slug, desc, price, cp, stock, json.dumps(["img"]), 1))

conn.commit()
conn.close()

print("OK")
print(f"DB: {db_path}")
print("user: demo@shoplatam.com / demo1234")
print("user: vendor@test.com / Test123!")
