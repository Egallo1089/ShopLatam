-- ================================================================
-- SHOPLATAM - CREAR TABLAS UNA POR UNA
-- Ejecuta en Supabase SQL Editor
-- ================================================================

-- ── TABLA 1: store_settings ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS store_settings (
  id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name            text        NOT NULL DEFAULT 'Mi Tienda',
  slug            text        UNIQUE,
  description     text,
  logo_url        text,
  primary_color   text        DEFAULT '#6366f1',
  whatsapp_number text,
  whatsapp        text,
  phone           text,
  address         text,
  city            text,
  instagram       text,
  facebook        text,
  tiktok          text,
  created_at      timestamptz DEFAULT now(),
  updated_at      timestamptz DEFAULT now()
);

-- ── TABLA 2: categories ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  name       text        NOT NULL,
  slug       text,
  emoji      text,
  active     boolean     DEFAULT true,
  position   integer     DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- ── TABLA 3: products ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products (
  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       uuid        REFERENCES auth.users(id) ON DELETE CASCADE,
  category_id   uuid        REFERENCES categories(id) ON DELETE SET NULL,
  name          text        NOT NULL,
  description   text,
  price         numeric(10,2) NOT NULL DEFAULT 0,
  compare_price numeric(10,2),
  stock         integer     DEFAULT 0,
  sku           text,
  images        text[]      DEFAULT '{}',
  is_featured   boolean     DEFAULT false,
  active        boolean     DEFAULT true,
  created_at    timestamptz DEFAULT now(),
  updated_at    timestamptz DEFAULT now()
);

-- ── TABLA 4: orders ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          uuid        REFERENCES auth.users(id) ON DELETE SET NULL,
  order_number     text        UNIQUE DEFAULT ('ORD-' || upper(substring(gen_random_uuid()::text, 1, 8))),
  customer_name    text        NOT NULL,
  customer_phone   text,
  customer_address text,
  total            numeric(10,2) NOT NULL DEFAULT 0,
  status           text        DEFAULT 'nuevo',
  payment_method   text        DEFAULT 'contra_entrega',
  notes            text,
  created_at       timestamptz DEFAULT now(),
  updated_at       timestamptz DEFAULT now()
);

-- ── TABLA 5: order_items ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS order_items (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id   uuid        NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id uuid        REFERENCES products(id) ON DELETE SET NULL,
  name       text        NOT NULL,
  quantity   integer     NOT NULL DEFAULT 1,
  price      numeric(10,2) NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- ── VERIFICAR ───────────────────────────────────────────────────
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('store_settings','categories','products','orders','order_items')
ORDER BY table_name;
