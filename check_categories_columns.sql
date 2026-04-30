-- ============================================================
-- PASO 1: Ver qué columnas tiene tu tabla categories
-- ============================================================
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'categories' 
ORDER BY ordinal_position;
