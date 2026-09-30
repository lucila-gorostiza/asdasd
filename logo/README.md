# El Parte — ícono (variante 1e)

P serif (DM Serif Display, convertida a trazo) en tinta #141827 sobre blanco, con punto rosa #F23B98.

## Archivos
- icon.svg — vectorial con borde redondeado (favicon moderno)
- favicon.ico — 16/32/48 px
- favicon-16.png, favicon-32.png, favicon-48.png
- apple-touch-icon.png — 180 px, sin esquinas (iOS las recorta)
- icon-192.png, icon-512.png — PWA / Android
- icon-maskable-512.png — PWA maskable (glifo en zona segura)
- app-icon-1024.png — App Store / Play Store (sin esquinas ni transparencia)
- icon-fullbleed.svg — vectorial para íconos de app
- site.webmanifest

## Colores
Tinta #141827 · Rosa #F23B98 · Fondo #FFFFFF

## Integración en El Parte

Ya está integrado; no hay que copiar nada a mano (ver CLAUDE.md §6.0 y §10):

- `plantilla.html` lleva en el `<head>` `icon.svg` y `favicon-32.png` embebidos
  como `data:` (el `index.html` sigue siendo un solo archivo), más
  `apple-touch-icon`, `manifest` y `theme-color` `#141827`.
- El workflow de deploy publica junto al `index.html`: `favicon.ico`,
  `icon.svg`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`,
  `icon-maskable-512.png` y `site.webmanifest` (con rutas relativas).
- `armar.py` falla si falta el ícono en el `<head>` o alguno de esos archivos.

Si se cambia el logo: reemplazar estos archivos y regenerar los `data:` del
`<head>` de `plantilla.html`.
