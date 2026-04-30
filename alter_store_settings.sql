-- ================================================================
-- AMPLIAR store_settings con campos de personalización completa
-- Ejecuta en Supabase SQL Editor
-- ================================================================

ALTER TABLE store_settings
  ADD COLUMN IF NOT EXISTS banner_text    text DEFAULT '🚀 ENVÍO Gratis +$50 · 💬 Paga con WhatsApp · 🔥 Ofertas cada lunes',
  ADD COLUMN IF NOT EXISTS hero_title     text DEFAULT 'Todo lo que necesitas, al mejor precio',
  ADD COLUMN IF NOT EXISTS hero_subtitle  text DEFAULT 'Miles de productos seleccionados para ti. Entrega rápida y pago seguro por WhatsApp.',
  ADD COLUMN IF NOT EXISTS hero_cta_text  text DEFAULT 'Ver catálogo',
  ADD COLUMN IF NOT EXISTS youtube        text,
  ADD COLUMN IF NOT EXISTS opening_hours  text DEFAULT 'Lun-Vie 9:00-18:00 · Sáb 9:00-14:00',
  ADD COLUMN IF NOT EXISTS currency       text DEFAULT 'USD',
  ADD COLUMN IF NOT EXISTS currency_symbol text DEFAULT '$';

-- Verificar
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'store_settings'
ORDER BY ordinal_position;
