-- ================================================================
-- PASO 1: Ver todos los productos actuales y sus categorías
-- ================================================================
SELECT 
  name,
  category,
  price,
  stock,
  active
FROM products
ORDER BY category NULLS LAST, name;
