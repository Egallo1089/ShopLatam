-- ================================================================
-- SHOPLATAM — BASE DE DATOS COMPLETA
-- Ejecuta este archivo completo de una sola vez en:
-- Supabase → SQL Editor → New query → pegar → Run
--
-- INCLUYE:
--  1. Extensiones necesarias
--  2. Tablas principales (store_settings, categories, products, orders, order_items)
--  3. Columnas adicionales (ALTER TABLE)
--  4. Políticas RLS completas
--  5. Funciones y triggers automáticos
--  6. Las 22 categorías de ejemplo
--  7. Bucket de Storage para imágenes de productos
-- ================================================================

-- =============================================================
-- PASO 0 — Extensiones necesarias
-- =============================================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================
-- PASO 1 — TABLAS PRINCIPALES
-- =============================================================

-- ── TABLA: store_settings ────────────────────────────────────
-- Configuración de la tienda del vendedor
CREATE TABLE IF NOT EXISTS store_settings (
  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  -- Identidad
  name             text        NOT NULL DEFAULT 'Mi Tienda',
  slug             text        UNIQUE,
  description      text,
  logo_url         text,
  primary_color    text        DEFAULT '#E63B5A',
  -- Contacto
  whatsapp_number  text,
  whatsapp         text,       -- alias legacy
  phone            text,
  address          text,
  city             text        DEFAULT 'Ecuador',
  -- Redes sociales
  instagram        text,
  facebook         text,
  tiktok           text,
  youtube          text,
  -- Hero / Banner
  banner_text      text        DEFAULT '🚀 ENVÍO Gratis +$50 · 💬 Paga con WhatsApp · 🔥 Ofertas cada lunes',
  hero_title       text        DEFAULT 'Todo lo que necesitas,',
  hero_subtitle    text        DEFAULT 'Miles de productos seleccionados para ti. Entrega rápida y pago seguro por WhatsApp.',
  hero_cta_text    text        DEFAULT 'Ver catálogo',
  hero_image_url   text,
  -- Horario y moneda
  opening_hours    text        DEFAULT 'Lun-Vie 9:00-18:00 · Sáb 9:00-14:00',
  currency         text        DEFAULT 'USD',
  currency_symbol  text        DEFAULT '$',
  -- SEO
  meta_title       text,
  meta_description text,
  -- Políticas
  return_policy    text,
  shipping_policy  text,
  -- Inventario
  low_stock_threshold integer  DEFAULT 5,
  -- Timestamps
  created_at       timestamptz DEFAULT now(),
  updated_at       timestamptz DEFAULT now()
);

-- ── TABLA: categories ────────────────────────────────────────
-- Departamentos / Categorías del catálogo
CREATE TABLE IF NOT EXISTS categories (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  name       text        NOT NULL,
  slug       text,
  emoji      text,
  active     boolean     DEFAULT true,
  position   integer     DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- ── TABLA: products ──────────────────────────────────────────
-- Catálogo de productos
CREATE TABLE IF NOT EXISTS products (
  id             uuid          PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id        uuid          REFERENCES auth.users(id) ON DELETE CASCADE,
  category_id    uuid          REFERENCES categories(id) ON DELETE SET NULL,
  -- Contenido
  name           text          NOT NULL,
  slug           text,
  description    text,
  -- Precios
  price          numeric(10,2) NOT NULL DEFAULT 0,
  compare_price  numeric(10,2),            -- precio tachado (antes: old_price)
  -- Inventario
  stock          integer       DEFAULT 0,
  sku            text,
  -- Media
  images         text[]        DEFAULT '{}',
  emoji          text,
  bg_color       text          DEFAULT '#0a1628',
  badge          text,                     -- ej: "NUEVO", "HOT", "OFERTA"
  -- Comportamiento
  is_featured    boolean       DEFAULT false,
  active         boolean       DEFAULT true,
  whatsapp_msg   text,                     -- mensaje personalizado para WhatsApp
  -- Fecha fin de oferta (para countdown real)
  sale_ends_at   timestamptz,
  -- Timestamps
  created_at     timestamptz   DEFAULT now(),
  updated_at     timestamptz   DEFAULT now()
);

-- ── TABLA: orders ────────────────────────────────────────────
-- Pedidos registrados (desde carrito o WhatsApp)
CREATE TABLE IF NOT EXISTS orders (
  id               uuid          PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          uuid          REFERENCES auth.users(id) ON DELETE SET NULL,
  order_number     text          UNIQUE DEFAULT ('ORD-' || upper(substring(gen_random_uuid()::text, 1, 8))),
  -- Cliente
  customer_name    text          NOT NULL,
  customer_phone   text,
  customer_email   text,
  customer_address text,
  -- Totales
  subtotal         numeric(10,2) DEFAULT 0,
  discount         numeric(10,2) DEFAULT 0,
  total            numeric(10,2) NOT NULL DEFAULT 0,
  -- Estado
  status           text          DEFAULT 'nuevo'
                   CHECK (status IN ('nuevo','confirmado','preparando','enviado','entregado','cancelado')),
  payment_method   text          DEFAULT 'whatsapp'
                   CHECK (payment_method IN ('whatsapp','contra_entrega','transferencia','tarjeta')),
  -- Cupones y notas
  coupon_code      text,
  notes            text,
  whatsapp_sent    boolean       DEFAULT false,
  -- Timestamps
  created_at       timestamptz   DEFAULT now(),
  updated_at       timestamptz   DEFAULT now()
);

-- ── TABLA: order_items ───────────────────────────────────────
-- Líneas de detalle de cada pedido
CREATE TABLE IF NOT EXISTS order_items (
  id           uuid          PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id     uuid          NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id   uuid          REFERENCES products(id) ON DELETE SET NULL,
  name         text          NOT NULL,   -- nombre snapshot al momento del pedido
  quantity     integer       NOT NULL DEFAULT 1,
  price        numeric(10,2) NOT NULL,   -- precio snapshot al momento del pedido
  image_url    text,
  created_at   timestamptz   DEFAULT now()
);

-- ── TABLA: promotions ────────────────────────────────────────
-- Cupones y descuentos configurables desde el dashboard
CREATE TABLE IF NOT EXISTS promotions (
  id               uuid          PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          uuid          REFERENCES auth.users(id) ON DELETE CASCADE,
  code             text          NOT NULL,
  description      text,
  discount_type    text          NOT NULL DEFAULT 'percentage'
                   CHECK (discount_type IN ('percentage','fixed')),
  discount_value   numeric(10,2) NOT NULL,
  min_order_amount numeric(10,2) DEFAULT 0,
  max_uses         integer,
  used_count       integer       DEFAULT 0,
  expires_at       timestamptz,
  active           boolean       DEFAULT true,
  created_at       timestamptz   DEFAULT now(),
  UNIQUE(code, user_id)
);

-- ── TABLA: reviews ───────────────────────────────────────────
-- Reseñas de productos (para mostrar en la tienda)
CREATE TABLE IF NOT EXISTS reviews (
  id         uuid          PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid          REFERENCES products(id) ON DELETE CASCADE,
  user_id    uuid          REFERENCES auth.users(id) ON DELETE SET NULL,
  -- Datos del cliente
  name       text          NOT NULL,
  rating     smallint      NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comment    text,
  verified   boolean       DEFAULT false,
  created_at timestamptz   DEFAULT now()
);


-- =============================================================
-- PASO 2 — FUNCIONES Y TRIGGERS
-- =============================================================

-- Función: actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- Triggers de updated_at
DROP TRIGGER IF EXISTS trg_store_settings_updated ON store_settings;
CREATE TRIGGER trg_store_settings_updated
  BEFORE UPDATE ON store_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS trg_products_updated ON products;
CREATE TRIGGER trg_products_updated
  BEFORE UPDATE ON products
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS trg_orders_updated ON orders;
CREATE TRIGGER trg_orders_updated
  BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Función: auto-crear store_settings cuando se registra un nuevo usuario
CREATE OR REPLACE FUNCTION create_store_for_new_user()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  INSERT INTO store_settings (user_id, name, slug)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1), 'Mi Tienda'),
    lower(regexp_replace(
      COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1), 'tienda'),
      '[^a-z0-9]+', '-', 'g'
    )) || '-' || substring(NEW.id::text, 1, 6)
  )
  ON CONFLICT DO NOTHING;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_create_store_on_signup ON auth.users;
CREATE TRIGGER trg_create_store_on_signup
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION create_store_for_new_user();

-- Vista: resumen de clientes (agrupado por teléfono)
CREATE OR REPLACE VIEW customer_summary AS
SELECT
  o.user_id,
  o.customer_phone,
  o.customer_name,
  COUNT(*)              AS total_orders,
  SUM(o.total)          AS total_spent,
  MAX(o.created_at)     AS last_order_at,
  MIN(o.created_at)     AS first_order_at
FROM orders o
WHERE o.customer_phone IS NOT NULL
GROUP BY o.user_id, o.customer_phone, o.customer_name;


-- =============================================================
-- PASO 3 — POLÍTICAS RLS
-- =============================================================

-- Activar RLS en todas las tablas
ALTER TABLE store_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories     ENABLE ROW LEVEL SECURITY;
ALTER TABLE products       ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders         ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items    ENABLE ROW LEVEL SECURITY;
ALTER TABLE promotions     ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews        ENABLE ROW LEVEL SECURITY;

-- ─── Limpiar políticas anteriores ────────────────────────────
DROP POLICY IF EXISTS "store_owner_all"              ON store_settings;
DROP POLICY IF EXISTS "products_owner_all"           ON products;
DROP POLICY IF EXISTS "products_public_read"         ON products;
DROP POLICY IF EXISTS "orders_owner_all"             ON orders;
DROP POLICY IF EXISTS "orders_public_insert"         ON orders;
DROP POLICY IF EXISTS "order_items_public_insert"    ON order_items;
DROP POLICY IF EXISTS "order_items_owner_read"       ON order_items;
DROP POLICY IF EXISTS "categories_public_read"       ON categories;
DROP POLICY IF EXISTS "categories_auth_write"        ON categories;
DROP POLICY IF EXISTS "promotions_owner_all"         ON promotions;
DROP POLICY IF EXISTS "reviews_public_read"          ON reviews;
DROP POLICY IF EXISTS "reviews_public_insert"        ON reviews;
DROP POLICY IF EXISTS "reviews_owner_manage"         ON reviews;

-- ─── store_settings: solo el dueño puede gestionar su tienda ──
CREATE POLICY "store_owner_all" ON store_settings
  FOR ALL USING (auth.uid() = user_id);

-- ─── categories: todos pueden leer; solo autenticados escriben ─
CREATE POLICY "categories_public_read" ON categories
  FOR SELECT USING (active = true);
CREATE POLICY "categories_auth_write" ON categories
  FOR ALL USING (auth.role() = 'authenticated');

-- ─── products: dueño gestiona; público lee activos ────────────
CREATE POLICY "products_owner_all" ON products
  FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "products_public_read" ON products
  FOR SELECT USING (active = true);

-- ─── orders: dueño ve sus pedidos; clientes pueden crear ──────
CREATE POLICY "orders_owner_all" ON orders
  FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "orders_public_insert" ON orders
  FOR INSERT WITH CHECK (true);

-- ─── order_items: clientes insertan; dueño lee los suyos ──────
CREATE POLICY "order_items_public_insert" ON order_items
  FOR INSERT WITH CHECK (true);
CREATE POLICY "order_items_owner_read" ON order_items
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM orders o
      WHERE o.id = order_id
        AND o.user_id = auth.uid()
    )
  );

-- ─── promotions: solo el dueño gestiona ───────────────────────
CREATE POLICY "promotions_owner_all" ON promotions
  FOR ALL USING (auth.uid() = user_id);

-- ─── reviews: todos leen; público inserta; dueño gestiona ─────
CREATE POLICY "reviews_public_read" ON reviews
  FOR SELECT USING (true);
CREATE POLICY "reviews_public_insert" ON reviews
  FOR INSERT WITH CHECK (true);
CREATE POLICY "reviews_owner_manage" ON reviews
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM products p
      WHERE p.id = product_id
        AND p.user_id = auth.uid()
    )
  );


-- =============================================================
-- PASO 4 — STORAGE: bucket para imágenes de productos
-- =============================================================

INSERT INTO storage.buckets (id, name, public)
VALUES ('products', 'products', true)
ON CONFLICT (id) DO NOTHING;

-- Política de storage: cualquiera puede ver las imágenes
DROP POLICY IF EXISTS "products_images_public_read" ON storage.objects;
CREATE POLICY "products_images_public_read" ON storage.objects
  FOR SELECT USING (bucket_id = 'products');

-- Política de storage: solo autenticados suben imágenes
DROP POLICY IF EXISTS "products_images_auth_upload" ON storage.objects;
CREATE POLICY "products_images_auth_upload" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'products'
    AND auth.role() = 'authenticated'
  );

-- Política de storage: el dueño puede eliminar sus imágenes
DROP POLICY IF EXISTS "products_images_owner_delete" ON storage.objects;
CREATE POLICY "products_images_owner_delete" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'products'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );


-- =============================================================
-- PASO 5 — CATEGORÍAS: las 22 de ejemplo (mismas que Amazon Latam)
-- =============================================================

-- Nota: se borran las existentes para insertar las 22 limpias
-- COMENTAR ESTE BLOQUE si ya tienes categorías que quieres conservar
-- DELETE FROM categories;

INSERT INTO categories (name, slug, emoji, active, position)
VALUES
  ('Electrónicos',                          'electronicos',                           '📱', true,   1),
  ('Computadoras',                          'computadoras',                           '💻', true,   2),
  ('Smart Home',                            'smart-home',                             '🏠', true,   3),
  ('Arte y artesanías',                     'arte-y-artesanias',                      '🎨', true,   4),
  ('Automotriz',                            'automotriz',                             '🚗', true,   5),
  ('Bebé',                                  'bebe',                                   '👶', true,   6),
  ('Belleza y cuidado personal',            'belleza-y-cuidado-personal',             '💄', true,   7),
  ('Moda para mujer',                       'moda-para-mujer',                        '👗', true,   8),
  ('Moda para hombre',                      'moda-para-hombre',                       '👔', true,   9),
  ('Moda para niña',                        'moda-para-nina',                         '🎀', true,  10),
  ('Moda para niño',                        'moda-para-nino',                         '🧒', true,  11),
  ('Salud y hogar',                         'salud-y-hogar',                          '💊', true,  12),
  ('Hogar y cocina',                        'hogar-y-cocina',                         '🍳', true,  13),
  ('Industrial y científico',               'industrial-y-cientifico',                '🔬', true,  14),
  ('Equipaje',                              'equipaje',                               '🧳', true,  15),
  ('Películas y televisión',                'peliculas-y-television',                 '🎬', true,  16),
  ('Insumos para mascotas',                 'insumos-para-mascotas',                  '🐾', true,  17),
  ('Software',                              'software',                               '💾', true,  18),
  ('Deportes y aire libre',                 'deportes-y-aire-libre',                  '⚽', true,  19),
  ('Herramientas y mejoramiento del hogar', 'herramientas-y-mejoramiento-del-hogar',  '🔨', true,  20),
  ('Juguetes y juegos',                     'juguetes-y-juegos',                      '🎮', true,  21),
  ('Videojuegos',                           'videojuegos',                            '🕹️', true,  22)
ON CONFLICT DO NOTHING;


-- ── TABLA: audit_logs ───────────────────────────────────────
-- Log de auditoría obligatorio SRI (7 años de retención)
CREATE TABLE IF NOT EXISTS audit_logs (
  id              serial      PRIMARY KEY,
  user_id         integer     REFERENCES users(id),
  action          text        NOT NULL,
  resource_type   text        NOT NULL,
  resource_id     integer,
  old_values      jsonb,
  new_values      jsonb,
  ip_address      text,
  user_agent      text,
  notes           text,
  created_at      timestamptz DEFAULT now()
);

-- Políticas RLS para audit_logs
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Solo superadmin puede leer audit logs
CREATE POLICY "Superadmin can read audit_logs" ON audit_logs
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()::text::integer
      AND users.role = 'superadmin'
    )
  );

-- Sistema puede insertar audit logs
CREATE POLICY "System can insert audit_logs" ON audit_logs
  FOR INSERT WITH CHECK (true);

-- ── ÍNDICES DE PERFORMANCE ───────────────────────────────────
-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_store_id ON products(store_id);
CREATE INDEX IF NOT EXISTS idx_orders_store_id ON orders(store_id);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_commissions_seller_id ON commissions(seller_id);
CREATE INDEX IF NOT EXISTS idx_commissions_status ON commissions(status);

-- =============================================================
-- PASO 6 — VERIFICACIÓN FINAL
-- =============================================================

-- Muestra las tablas creadas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'store_settings','categories','products',
    'orders','order_items','promotions','reviews','audit_logs'
  )
ORDER BY table_name;

-- Muestra las 22 categorías
SELECT position, emoji, name FROM categories ORDER BY position;

-- Muestra las políticas activas
SELECT tablename, policyname, cmd
FROM pg_policies
WHERE tablename IN (
  'store_settings','categories','products',
  'orders','order_items','promotions','reviews','audit_logs'
)
ORDER BY tablename, policyname;
