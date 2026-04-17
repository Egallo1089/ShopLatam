-- ============================================================
-- PRIMERO: Agregar columnas que faltan (slug y emoji)
-- Ejecuta esto primero, luego el INSERT de abajo
-- ============================================================

ALTER TABLE categories ADD COLUMN IF NOT EXISTS slug text;
ALTER TABLE categories ADD COLUMN IF NOT EXISTS emoji text;
ALTER TABLE categories ADD COLUMN IF NOT EXISTS position integer DEFAULT 0;
ALTER TABLE categories ADD COLUMN IF NOT EXISTS active boolean DEFAULT true;

-- ============================================================
-- SEGUNDO: Limpiar e insertar las 22 categorías
-- ============================================================

DELETE FROM categories;

INSERT INTO categories (id, name, slug, emoji, active, position)
VALUES
  (gen_random_uuid(), 'Electrónicos',                          'electronicos',                          '📱', true,  1),
  (gen_random_uuid(), 'Computadoras',                          'computadoras',                          '💻', true,  2),
  (gen_random_uuid(), 'Smart Home',                            'smart-home',                            '🏠', true,  3),
  (gen_random_uuid(), 'Arte y artesanías',                     'arte-y-artesanias',                     '🎨', true,  4),
  (gen_random_uuid(), 'Automotriz',                            'automotriz',                            '🚗', true,  5),
  (gen_random_uuid(), 'Bebé',                                  'bebe',                                  '👶', true,  6),
  (gen_random_uuid(), 'Belleza y cuidado personal',            'belleza-y-cuidado-personal',            '💄', true,  7),
  (gen_random_uuid(), 'Moda para mujer',                       'moda-para-mujer',                       '👗', true,  8),
  (gen_random_uuid(), 'Moda para hombre',                      'moda-para-hombre',                      '👔', true,  9),
  (gen_random_uuid(), 'Moda para niña',                        'moda-para-nina',                        '🎀', true, 10),
  (gen_random_uuid(), 'Moda para niño',                        'moda-para-nino',                        '🧒', true, 11),
  (gen_random_uuid(), 'Salud y hogar',                         'salud-y-hogar',                         '💊', true, 12),
  (gen_random_uuid(), 'Hogar y cocina',                        'hogar-y-cocina',                        '🍳', true, 13),
  (gen_random_uuid(), 'Industrial y científico',               'industrial-y-cientifico',               '🔬', true, 14),
  (gen_random_uuid(), 'Equipaje',                              'equipaje',                              '🧳', true, 15),
  (gen_random_uuid(), 'Películas y televisión',                'peliculas-y-television',                '🎬', true, 16),
  (gen_random_uuid(), 'Insumos para mascotas',                 'insumos-para-mascotas',                 '🐾', true, 17),
  (gen_random_uuid(), 'Software',                              'software',                              '💾', true, 18),
  (gen_random_uuid(), 'Deportes y aire libre',                 'deportes-y-aire-libre',                 '⚽', true, 19),
  (gen_random_uuid(), 'Herramientas y mejoramiento del hogar', 'herramientas-y-mejoramiento-del-hogar', '🔨', true, 20),
  (gen_random_uuid(), 'Juguetes y juegos',                     'juguetes-y-juegos',                     '🎮', true, 21),
  (gen_random_uuid(), 'Videojuegos',                           'videojuegos',                           '🕹️', true, 22);

-- ============================================================
-- VERIFICAR: Muestra las 22 categorías insertadas
-- ============================================================
SELECT position, emoji, name FROM categories ORDER BY position;
