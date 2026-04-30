-- ================================================================
-- CREAR SOLO LA TABLA store_settings
-- Las otras tablas (products, categories, orders) ya existen
-- ================================================================

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

-- Politica: cada vendedor gestiona su propia tienda
ALTER TABLE store_settings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "store_owner_all" ON store_settings;
CREATE POLICY "store_owner_all" ON store_settings
  FOR ALL USING (auth.uid() = user_id);

-- Lectura publica del store (para que la tienda cargue sin login)
DROP POLICY IF EXISTS "store_public_read" ON store_settings;
CREATE POLICY "store_public_read" ON store_settings
  FOR SELECT USING (true);

-- VERIFICAR
SELECT 'store_settings creada correctamente' as resultado;
SELECT column_name FROM information_schema.columns
WHERE table_name = 'store_settings' ORDER BY ordinal_position;
