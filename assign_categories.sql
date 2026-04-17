-- ================================================================
-- ASIGNAR CATEGORÍAS CORRECTAS A LOS PRODUCTOS DE EJEMPLO
-- Basado en las 22 categorías oficiales del catálogo
-- ================================================================

-- ── Electrónicos ─────────────────────────────────────────────────
UPDATE products SET category = 'Electrónicos'
WHERE name ILIKE '%cámara%'
   OR name ILIKE '%camara%'
   OR name ILIKE '%audífono%'
   OR name ILIKE '%audifonos%'
   OR name ILIKE '%auricular%'
   OR name ILIKE '%smartwatch%'
   OR name ILIKE '%cable usb%'
   OR name ILIKE '%cable tipo%'
   OR name ILIKE '%cargador%'
   OR name ILIKE '%adaptador%'
   OR name ILIKE '%parlante%'
   OR name ILIKE '%bocina%'
   OR name ILIKE '%televisor%'
   OR name ILIKE '%tv %'
   OR name ILIKE '%drone%'
   OR name ILIKE '%tablet%'
   OR name ILIKE '%celular%'
   OR name ILIKE '%teléfono%'
   OR name ILIKE '%linterna%';

-- ── Computadoras ─────────────────────────────────────────────────
UPDATE products SET category = 'Computadoras'
WHERE name ILIKE '%laptop%'
   OR name ILIKE '%computador%'
   OR name ILIKE '%teclado%'
   OR name ILIKE '%mouse%'
   OR name ILIKE '%monitor%'
   OR name ILIKE '%impresora%'
   OR name ILIKE '%disco duro%'
   OR name ILIKE '%memoria ram%'
   OR name ILIKE '%webcam%';

-- ── Videojuegos ──────────────────────────────────────────────────
UPDATE products SET category = 'Videojuegos'
WHERE name ILIKE '%gaming%'
   OR name ILIKE '%gamer%'
   OR name ILIKE '%control%'
   OR name ILIKE '%playstation%'
   OR name ILIKE '%xbox%'
   OR name ILIKE '%silla gaming%'
   OR name ILIKE '%headset%';

-- ── Deportes y aire libre ────────────────────────────────────────
UPDATE products SET category = 'Deportes y aire libre'
WHERE name ILIKE '%zapatilla%'
   OR name ILIKE '%tenis%'
   OR name ILIKE '%deportiv%'
   OR name ILIKE '%running%'
   OR name ILIKE '%bicicleta%'
   OR name ILIKE '%yoga%'
   OR name ILIKE '%gym%'
   OR name ILIKE '%pesas%'
   OR name ILIKE '%balón%'
   OR name ILIKE '%balon%'
   OR name ILIKE '%futbol%'
   OR name ILIKE '%patineta%'
   OR name ILIKE '%caminadora%';

-- ── Hogar y cocina ───────────────────────────────────────────────
UPDATE products SET category = 'Hogar y cocina'
WHERE name ILIKE '%cocina%'
   OR name ILIKE '%olla%'
   OR name ILIKE '%sartén%'
   OR name ILIKE '%licuadora%'
   OR name ILIKE '%microondas%'
   OR name ILIKE '%cafetera%'
   OR name ILIKE '%vajilla%'
   OR name ILIKE '%set cocina%'
   OR name ILIKE '%cubiertos%'
   OR name ILIKE '%batidora%'
   OR name ILIKE '%freidora%'
   OR name ILIKE '%tostadora%'
   OR name ILIKE '%exprimidor%';

-- ── Moda para mujer ──────────────────────────────────────────────
UPDATE products SET category = 'Moda para mujer'
WHERE name ILIKE '%bolso%'
   OR name ILIKE '%cartera%'
   OR name ILIKE '%vestido%'
   OR name ILIKE '%blusa%'
   OR name ILIKE '%falda%'
   OR name ILIKE '%tacón%'
   OR name ILIKE '%sandalias mujer%'
   OR name ILIKE '%joyería%'
   OR name ILIKE '%collar%'
   OR name ILIKE '%aretes%'
   OR name ILIKE '%pulsera%';

-- ── Moda para hombre ─────────────────────────────────────────────
UPDATE products SET category = 'Moda para hombre'
WHERE name ILIKE '%camisa%'
   OR name ILIKE '%camiseta%'
   OR name ILIKE '%corbata%'
   OR name ILIKE '%jean%'
   OR name ILIKE '%pantalón hombre%'
   OR name ILIKE '%bermuda%'
   OR name ILIKE '%cinturón%';

-- ── Belleza y cuidado personal ───────────────────────────────────
UPDATE products SET category = 'Belleza y cuidado personal'
WHERE name ILIKE '%perfume%'
   OR name ILIKE '%crema%'
   OR name ILIKE '%shampoo%'
   OR name ILIKE '%maquillaje%'
   OR name ILIKE '%labial%'
   OR name ILIKE '%serum%'
   OR name ILIKE '%hidratante%'
   OR name ILIKE '%desodorante%'
   OR name ILIKE '%rasuradora%';

-- ── Bebé ─────────────────────────────────────────────────────────
UPDATE products SET category = 'Bebé'
WHERE name ILIKE '%bebé%'
   OR name ILIKE '%bebe%'
   OR name ILIKE '%pañal%'
   OR name ILIKE '%cuna%'
   OR name ILIKE '%carriola%'
   OR name ILIKE '%mamadera%'
   OR name ILIKE '%chupete%';

-- ── Juguetes y juegos ────────────────────────────────────────────
UPDATE products SET category = 'Juguetes y juegos'
WHERE name ILIKE '%juguete%'
   OR name ILIKE '%lego%'
   OR name ILIKE '%muñeca%'
   OR name ILIKE '%rompecabezas%'
   OR name ILIKE '%juego de mesa%';

-- ── Insumos para mascotas ────────────────────────────────────────
UPDATE products SET category = 'Insumos para mascotas'
WHERE name ILIKE '%mascota%'
   OR name ILIKE '%perro%'
   OR name ILIKE '%gato%'
   OR name ILIKE '%collar para%'
   OR name ILIKE '%veterinario%'
   OR name ILIKE '%croquetas%'
   OR name ILIKE '%arena para%';

-- ── Herramientas y mejoramiento del hogar ─────────────────────────
UPDATE products SET category = 'Herramientas y mejoramiento del hogar'
WHERE name ILIKE '%taladro%'
   OR name ILIKE '%sierra%'
   OR name ILIKE '%martillo%'
   OR name ILIKE '%destornillador%'
   OR name ILIKE '%llave inglesa%'
   OR name ILIKE '%escalera%'
   OR name ILIKE '%pintura para%'
   OR name ILIKE '%herramienta%';

-- ── Salud y hogar ────────────────────────────────────────────────
UPDATE products SET category = 'Salud y hogar'
WHERE name ILIKE '%tensiómetro%'
   OR name ILIKE '%termómetro%'
   OR name ILIKE '%oxímetro%'
   OR name ILIKE '%vitamina%'
   OR name ILIKE '%suplemento%'
   OR name ILIKE '%botiquín%'
   OR name ILIKE '%masajeador%';

-- ── Equipaje ─────────────────────────────────────────────────────
UPDATE products SET category = 'Equipaje'
WHERE name ILIKE '%maleta%'
   OR name ILIKE '%mochila%'
   OR name ILIKE '%maletín%'
   OR name ILIKE '%bolsa de viaje%'
   OR name ILIKE '%valija%';

-- ── Software ─────────────────────────────────────────────────────
UPDATE products SET category = 'Software'
WHERE name ILIKE '%antivirus%'
   OR name ILIKE '%office%'
   OR name ILIKE '%windows%'
   OR name ILIKE '%licencia%'
   OR name ILIKE '%software%';

-- ── Smart Home ───────────────────────────────────────────────────
UPDATE products SET category = 'Smart Home'
WHERE name ILIKE '%foco inteligente%'
   OR name ILIKE '%bombillo smart%'
   OR name ILIKE '%cámara seguridad%'
   OR name ILIKE '%alexa%'
   OR name ILIKE '%google home%'
   OR name ILIKE '%smart plug%'
   OR name ILIKE '%timbre inteligente%';

-- ================================================================
-- VERIFICAR RESULTADO FINAL
-- ================================================================
SELECT 
  COALESCE(category, '⚠️ SIN CATEGORÍA') as categoria,
  count(*) as total_productos,
  string_agg(name, ', ' ORDER BY name) as productos
FROM products
GROUP BY category
ORDER BY category NULLS LAST;
