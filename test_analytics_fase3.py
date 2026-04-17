#!/usr/bin/env python3
"""
FASE 3: Analytics y Dashboard de Ventas - Testing
Valida todas las métricas y genera reportes
"""

import requests
import json
from datetime import datetime, timedelta

API_URL = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*70}")
    print(f"  {title.center(66)}")
    print(f"{'='*70}")

def print_test(status, message):
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")

# ─────────────────────────────────────────────────────────────────

print_header("FASE 3: ANALYTICS Y DASHBOARD DE VENTAS")

# 1. Login
print("\n→ Obteniendo credenciales...")
resp = requests.post(f"{API_URL}/auth/login", json={
    "email": "vendor@test.com",
    "password": "Test123!",
})
if resp.status_code != 200:
    print(f"❌ Login fallido: {resp.text}")
    exit(1)
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print_test(True, "Autenticación exitosa")

# 2. Obtener analytics summary
print_header("1️⃣  MÉTRICAS RESUMEN")

print("→ Obteniendo datos analytics...")
resp = requests.get(f"{API_URL}/analytics/summary", headers=headers)
if resp.status_code != 200:
    print(f"❌ Error: {resp.text}")
    exit(1)

data = resp.json()
print_test(True, "Datos de analytics obtenidos")

# 3. Mostrar ingresos
print("\n📊 INGRESOS:")
print(f"  {'Período':<20} │ {'Ingresos':<15}")
print(f"  {'-'*20} │ {'-'*15}")
print(f"  {'Hoy':<20} │ ${data['revenue']['today']:>13.2f}")
print(f"  {'Esta semana':<20} │ ${data['revenue']['week']:>13.2f}")
print(f"  {'Este mes':<20} │ ${data['revenue']['month']:>13.2f}")

# 4. Mostrar pedidos
print("\n📦 PEDIDOS:")
print(f"  {'Período':<20} │ {'Cantidad':<15}")
print(f"  {'-'*20} │ {'-'*15}")
print(f"  {'Hoy':<20} │ {data['orders']['today']:>14}")
print(f"  {'Esta semana':<20} │ {data['orders']['week']:>14}")
print(f"  {'Este mes':<20} │ {data['orders']['month']:>14}")
print(f"  {'TOTAL':<20} │ {data['orders']['total']:>14}")

# 5. Mostrar estado de órdenes
print("\n🔄 ÓRDENES POR ESTADO:")
print(f"  {'Estado':<20} │ {'Cantidad':<15}")
print(f"  {'-'*20} │ {'-'*15}")
for status, count in data['orders']['by_status'].items():
    status_label = status.replace('_', ' ').title()
    print(f"  {status_label:<20} │ {count:>14}")

# 6. Mostrar productos top
print("\n🏆 TOP 5 PRODUCTOS MÁS VENDIDOS:")
if data['top_products']:
    print(f"  {'#':<3} {'Producto':<35} │ {'Vendidos':<8} │ {'% total':<8}")
    print(f"  {'-'*3} {'-'*35} │ {'-'*8} │ {'-'*8}")
    total_sold = sum(p['sold'] for p in data['top_products'])
    for i, p in enumerate(data['top_products'][:5], 1):
        pct = (p['sold'] / total_sold * 100) if total_sold > 0 else 0
        name = p['name'][:33]
        print(f"  {i:<3} {name:<35} │ {p['sold']:>7} │ {pct:>6.1f}%")
else:
    print("   (Sin ventas registradas aún)")

# 7. Mostrar datos semanales
print("\n📈 INGRESOS POR DÍA (últimos 7 días):")
if data['weekly_revenue']:
    print(f"  {'Día':<12} │ {'Ingresos':<12} │ {'Gráfico':<40}")
    print(f"  {'-'*12} │ {'-'*12} │ {'-'*40}")
    max_rev = max(d['revenue'] for d in data['weekly_revenue']) or 1
    for d in data['weekly_revenue']:
        pct = (d['revenue'] / max_rev) * 100 if max_rev > 0 else 0
        bar_len = int(pct / 5) if pct > 0 else 0
        bar = "█" * bar_len + "░" * (8 - bar_len)
        print(f"  {d['day']:<12} │ ${d['revenue']:>10.2f} │ {bar} {pct:>5.1f}%")

# ─────────────────────────────────────────────────────────────────

print_header("2️⃣  KPI CALCULADOS")

# Calcular métricas derivadas
total_revenue = data['revenue']['month']
total_orders = data['orders']['month']
avg_order = total_revenue / total_orders if total_orders > 0 else 0
total_products = data['total_products']
top_product = data['top_products'][0] if data['top_products'] else None

print(f"  {'KPI':<40} │ {'Valor':<20}")
print(f"  {'-'*40} │ {'-'*20}")
print(f"  {'Ingresos promedio por pedido':<40} │ ${avg_order:>18.2f}")
print(f"  {'Total de productos en catálogo':<40} │ {total_products:>19}")
if top_product:
    name = top_product['name'][:37]
    print(f"  {'Producto más vendido':<40} │ {name:>20}")
    print(f"  {'Unidades del top product':<40} │ {top_product['sold']:>19}")
else:
    print(f"  {'Producto más vendido':<40} │ {'N/A':>20}")
    print(f"  {'Unidades del top product':<40} │ {0:>19}")

# ─────────────────────────────────────────────────────────────────

print_header("3️⃣  ANÁLISIS Y RECOMENDACIONES")

print("\n💡 Insights basados en datos:\n")

# Análisis 1: Tendencia de ingresos
week_income = data['revenue']['week']
month_income = data['revenue']['month']
avg_daily_this_month = month_income / 30

print(f"1️⃣  Ingresos vs expectativa:")
if week_income > (month_income / 4) * 1.2:
    print(f"   ✅ Esta semana está 20%+ arriba del promedio mensual")
elif week_income < (month_income / 4) * 0.8:
    print(f"   ⚠️  Esta semana está 20%- debajo del promedio mensual")
else:
    print(f"   ➡️  Esta semana tiene un ritmo normal")

# Análisis 2: Diversificación de productos
if data['top_products']:
    top_pct = (data['top_products'][0]['sold'] / sum(p['sold'] for p in data['top_products'])) * 100
    print(f"\n2️⃣  Diversificación de ventas:")
    if top_pct > 40:
        print(f"   ⚠️  El top product representa {top_pct:.1f}% de ventas")
        print(f"      → Considera promocionar otros productos")
    else:
        print(f"   ✅ Ventas bien distribuidas ({top_pct:.1f}% en top product)")

# Análisis 3: Órdenes por estado
pending_orders = data['orders']['by_status'].get('nuevo', 0) + data['orders']['by_status'].get('confirmado', 0)
if pending_orders > 2:
    print(f"\n3️⃣  Órdenes pendientes:")
    print(f"   ⚠️  Tienes {pending_orders} órdenes sin preparar/enviar")
    print(f"      → Prioritiza estas órdenes")

# Análisis 4: Conversión
delivered = data['orders']['by_status'].get('entregado', 0)
total = data['orders']['total']
if total > 0:
    delivered_pct = (delivered / total) * 100
    print(f"\n4️⃣  Tasa de entrega:")
    print(f"   {delivered_pct:.1f}% de tus órdenes han sido entregadas")
    if delivered_pct < 50:
        print(f"      → Acelera tu proceso de entrega")

# ─────────────────────────────────────────────────────────────────

print_header("4️⃣  PROYECCIONES")

print("\n🔮 Estimaciones para fin de mes:\n")

days_passed = datetime.now().day
days_left = 30 - days_passed
daily_avg = month_income / days_passed if days_passed > 0 else 0
projected_revenue = month_income + (daily_avg * days_left)
orders_daily_avg = total_orders / days_passed if days_passed > 0 else 0
projected_orders = total_orders + int(orders_daily_avg * days_left)

proj_revenue_per_order = projected_revenue / projected_orders if projected_orders > 0 else 0

print(f"  {'Métrica':<35} │ {'Actual':<15} │ {'Proyectado':<15}")
print(f"  {'-'*35} │ {'-'*15} │ {'-'*15}")
print(f"  {'Ingresos mensuales':<35} │ ${month_income:>13.2f} │ ${projected_revenue:>13.2f}")
print(f"  {'Órdenes totales':<35} │ {total_orders:>14} │ {projected_orders:>14}")
print(f"  {'Promedio por orden':<35} │ ${avg_order:>13.2f} │ ${proj_revenue_per_order:>13.2f}")

print(f"\n📅 Basado en {days_passed} días de datos")

# ─────────────────────────────────────────────────────────────────

print_header("RESUMEN FINAL")

print(f"\n✨ ANALYTICS - Dashboard completo generado")
print(f"\n📊 Métricas principales:")
print(f"   • Ingresos mes: ${month_income:.2f}")
print(f"   • Total pedidos: {total_orders}")
print(f"   • Productos: {total_products}")
print(f"   • Orden promedio: ${avg_order:.2f}")

print(f"\n🎯 Estado de la tienda:")
if month_income > 100:
    print(f"   ✅ Excelente desempeño este mes")
elif month_income > 0:
    print(f"   ⚠️  Iniciando ventas")
else:
    print(f"   📍 Sin ventas aún - continúa promocionando")

print(f"\n🔗 Acceso al dashboard: http://localhost:3004/dashboard")
print(f"📱 WhatsApp: +593997475698")
print(f"\n{'='*70}\n")
