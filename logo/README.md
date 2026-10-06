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
  `logo/favicon.ico`, `logo/apple-touch-icon.png`, `logo/site.webmanifest` y
  `theme-color` `#141827`.
- **Las rutas llevan el prefijo `logo/` a propósito.** El sitio es un Worker de
  Cloudflare que sirve el repo tal cual, así que estos archivos viven en
  `logo/` y no en la raíz. Con rutas en la raíz daban 404 y el ícono de
  celular no aparecía. **No mover esta carpeta ni quitar el prefijo.**
- `site.webmanifest` usa rutas relativas (`icon-192.png`, …): resuelven dentro
  de `logo/`, donde está el manifest.
  Por eso `start_url`, `scope` e `id` valen `"../"`: apuntan a la raíz, donde
  está el diario. Con `"./"` la app instalada abría `logo/` y daba error.
  Verificado el 6/10/2026: así la app instalada abre el diario. Si se cambia
  el manifest, la app ya instalada no se entera: hay que reinstalarla.
- Se publican tal cual en `logo/` del Worker de Cloudflare (`wrangler.jsonc` +
  `.assetsignore`, CLAUDE.md §10). Ya no hay workflow de Pages.
- `armar.py` falla si falta el ícono en el `<head>`, si las rutas no son las
  de arriba, si falta alguno de estos archivos o si `start_url`/`scope` del
  manifest no son `"../"`.

Si se cambia el logo: reemplazar estos archivos (mismos nombres) y regenerar
los `data:` del `<head>` de `plantilla.html`.
