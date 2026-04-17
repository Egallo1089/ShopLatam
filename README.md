# ShopLatam

Plataforma SaaS de ventas online para emprendedores en Ecuador y LATAM.

**Dueño:** Eduardo Gallo — Guayaquil, Ecuador

---

## Levantar todo con un solo comando

```bash
cd "C:\Users\USUARIO 1\Desktop\AUTOFI\ShopLatam"
docker-compose up --build
```

### URLs una vez levantado

| Servicio       | URL                          |
|----------------|------------------------------|
| Tienda pública | http://localhost/tienda/{slug} |
| Panel vendedor | http://localhost/dashboard   |
| API docs       | http://localhost/docs        |
| Backend directo| http://localhost:8000        |
| Frontend directo| http://localhost:3000       |

---

## Stack

- **Backend:** Python 3.11 + FastAPI + PostgreSQL + Redis + Celery
- **Frontend:** React 18 + TypeScript + Tailwind CSS + Vite
- **WhatsApp:** Meta WhatsApp Business API
- **Pagos:** PayPhone Ecuador
- **Deploy:** Docker Compose + Nginx

## Estructura

```
ShopLatam/
├── docker-compose.yml
├── .env                    ← Variables de entorno
├── nginx/nginx.conf
├── backend/
│   ├── main.py             ← FastAPI app entry point
│   ├── requirements.txt
│   ├── alembic/            ← Migraciones de base de datos
│   └── app/
│       ├── config.py       ← Settings desde .env
│       ├── database.py     ← SQLAlchemy engine
│       ├── models/         ← User, Store, Product, Order, Customer
│       ├── schemas/        ← Pydantic schemas
│       ├── routers/        ← auth, products, orders, whatsapp, analytics, store
│       ├── middleware/      ← JWT auth
│       └── tasks.py        ← Celery tasks
└── frontend/
    └── src/
        ├── pages/
        │   ├── auth/       ← Login, Register
        │   ├── store/      ← StorePage, CatalogPage, ProductPage
        │   └── dashboard/  ← Overview, Products, Orders, Analytics, StoreSettings
        ├── api/client.ts   ← Axios + todos los endpoints
        └── store/auth.ts   ← Zustand auth state
```

## Endpoints principales

### Auth
- `POST /auth/register` — Crear cuenta vendedor
- `POST /auth/login` — Login → JWT token

### Tienda
- `GET  /stores/{slug}` — Tienda pública por slug
- `GET  /stores/me` — Mi tienda (auth)
- `POST /stores` — Crear tienda (auth)

### Productos
- `GET  /products?store_id=` — Listar productos (público)
- `POST /products` — Crear producto (auth)
- `PUT  /products/{id}` — Editar producto (auth)
- `DELETE /products/{id}` — Eliminar (auth)

### Pedidos
- `GET  /orders` — Mis pedidos (auth)
- `POST /orders` — Crear pedido
- `PATCH /orders/{id}` — Actualizar estado
- `GET  /orders/{id}/factura` — Descargar PDF

### Analytics
- `GET  /analytics/summary` — KPIs del panel

### WhatsApp
- `GET  /webhook/whatsapp` — Verificación Meta
- `POST /webhook/whatsapp` — Mensajes entrantes

## Variables .env a configurar en producción

```
WHATSAPP_TOKEN=        ← Meta Business API token
WHATSAPP_PHONE_NUMBER_ID=
PAYPHONE_TOKEN=        ← PayPhone Ecuador
CLOUDINARY_CLOUD_NAME= ← Almacenamiento de imágenes
SECRET_KEY=            ← Cambiar por clave aleatoria segura
```
