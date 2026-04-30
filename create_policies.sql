-- ============================================================
-- SHOPLATAM - POLÍTICAS RLS (versión corregida)
-- Ejecuta esto DESPUÉS de haber creado las tablas
-- ============================================================

-- ── Eliminar políticas anteriores si existen ─────────────────
DROP POLICY IF EXISTS "store_owner_all"       ON store_settings;
DROP POLICY IF EXISTS "products_owner_all"    ON products;
DROP POLICY IF EXISTS "products_public_read"  ON products;
DROP POLICY IF EXISTS "orders_owner_all"      ON orders;
DROP POLICY IF EXISTS "orders_public_insert"  ON orders;
DROP POLICY IF EXISTS "order_items_public_insert" ON order_items;
DROP POLICY IF EXISTS "order_items_owner_read"    ON order_items;
DROP POLICY IF EXISTS "categories_public_read"    ON categories;
DROP POLICY IF EXISTS "categories_auth_write"     ON categories;

-- ── Activar RLS ───────────────────────────────────────────────
ALTER TABLE store_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE products        ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders          ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items     ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories      ENABLE ROW LEVEL SECURITY;

-- ── Crear políticas ───────────────────────────────────────────

-- store_settings: solo el dueño accede a su tienda
CREATE POLICY "store_owner_all" ON store_settings
  FOR ALL USING (auth.uid() = user_id);

-- products: dueño gestiona, público lee activos
CREATE POLICY "products_owner_all" ON products
  FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "products_public_read" ON products
  FOR SELECT USING (active = true);

-- orders: dueño ve sus pedidos; clientes pueden crear pedidos
CREATE POLICY "orders_owner_all" ON orders
  FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "orders_public_insert" ON orders
  FOR INSERT WITH CHECK (true);

-- order_items: clientes insertan; dueño lee los suyos
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

-- categories: todos pueden leer; autenticados pueden escribir
CREATE POLICY "categories_public_read" ON categories
  FOR SELECT USING (true);
CREATE POLICY "categories_auth_write" ON categories
  FOR ALL USING (auth.role() = 'authenticated');

-- ── Verificar que todo quedó bien ────────────────────────────
SELECT 
  schemaname,
  tablename,
  policyname,
  cmd
FROM pg_policies
WHERE tablename IN ('store_settings','categories','products','orders','order_items')
ORDER BY tablename, policyname;
