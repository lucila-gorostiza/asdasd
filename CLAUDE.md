# El Parte — especificación estética y de maquetado

Guía para armar cada edición diaria. La referencia canónica de lo estético es
`plantilla.html`: **ante cualquier duda sobre CSS, paleta o tipografía, mirá ese
archivo antes que esta descripción.** Para el tono y el criterio editorial, mirá
el `cuerpo.html` de la última edición.

> Antes esta línea apuntaba al `index.html` del 5/9/2026. No servía como
> referencia estable: `index.html` se sobrescribe en cada corrida, así que
> "la edición del 5/9" dejaba de existir al día siguiente. Lo estable ahora
> vive en `plantilla.html`.

Base: sistema de diseño **riso** de typeui.sh. Los tokens ya están bajados, en
`DESIGN.md`, y el CSS derivado de ellos vive en `plantilla.html`.

> **No corras `npx typeui.sh` en la corrida diaria.** El diseño ya está hecho y
> congelado; no hay nada que traer. Volver a pullearlo agrega una dependencia de
> red por día a cambio de nada, y peor: invita a "corregir" los desvíos
> deliberados respecto de los tokens riso (§1, el fondo crema en lugar del
> blanco), que son justamente lo que le da el aire de papel al diario.
>
> Se corre sólo si alguna vez se rediseña el diario, como tarea puntual y
> deliberada. En ese caso usá `npx typeui.sh pull riso --format design`: la
> variante interactiva del CLI se cuelga esperando input.

---

## 0. Restricciones duras

Estas no se negocian, vienen del encargo. **Rigen sobre el archivo publicado**,
no sobre cómo esté organizado el repo (ver §0.1):

- **Un solo archivo**: el `index.html` que se publica es uno solo, con todo el
  CSS embebido en un `<style>` en el `<head>`. Se abre directo en un navegador,
  sin servidor ni nada alrededor.
- **Cero dependencias externas**: nada de Google Fonts, CDNs, frameworks ni
  imágenes remotas. Las tipografías se declaran con fallbacks del sistema
  (ver §2). Ninguna cadena de build: ni npm, ni bundlers, ni frameworks.
- **Cero JavaScript.** La página es HTML y CSS.
- **Solo modo claro.** El diario es papel: no hay dark mode ni
  `prefers-color-scheme`. El fondo se pinta explícito.
- `lang="es-AR"`.

### 0.1 El fuente está partido en dos; el entregable no

En el repo, lo que cambia y lo que no viven separados:

| archivo | qué es | cambia |
|---|---|---|
| `plantilla.html` | `<head>`, el `<style>` completo y el esqueleto del `<body>`. Marcadores `{{TITULO}}` y `{{CUERPO}}`. | casi nunca |
| `cuerpo.html` | la edición del día. Primera línea: `<!-- TITULO: ... -->`. | todos los días |
| `armar.py` | los junta y **valida** antes de escribir | casi nunca |
| `index.html` | **generado**. Es lo que se publica. | todos los días |

```
python3 armar.py     # plantilla.html + cuerpo.html -> index.html
```

No edites `index.html` a mano: lo pisa el próximo `armar.py`. Editá `cuerpo.html`
y volvé a armar.

Esto **no** contradice la regla de "un solo archivo": el publicado sigue siendo
uno solo y autocontenido, y `armar.py` verifica exactamente eso en cada corrida.
La razón de partirlo es que el CSS son ~10 KB idénticos todos los días: tenerlo
aparte evita reescribirlo en cada edición.

`armar.py` corre con Python 3 de la biblioteca estándar, sin instalar nada.
Si falla una validación **no escribe** `index.html` y sale con código 1: es
preferible no publicar a publicar una edición rota. Chequea las restricciones
de este §0 (JavaScript, recursos externos, `@import`, `prefers-color-scheme`,
`lang`, un solo `<style>`), la numeración 01–06 del §6.3, los 3 ítems exactos
del índice del §6.2, el máximo de una `.lead` por sección del §7, que ningún
`.why` caiga dentro de un `.brief` (§6.6), que las etiquetas cierren bien y que
no haya quedado ningún marcador `{{...}}` sin reemplazar.

Además de `{{TITULO}}` y `{{CUERPO}}`, `armar.py` reemplaza `{{HORA_CIERRE}}`
por la hora real de esa corrida en ART (ver §6.1): es el único de los tres que
no viene de `cuerpo.html` tal cual, sino que se calcula en el momento de armar.

---

## 1. Paleta

```css
--pink:#F237A1;   /* primary riso  — acento, atención, voz editorial */
--blue:#2C40A7;   /* secondary riso — estructura, institucional */
--green:#16A34A;  /* success */
--amber:#D97706;  /* warning */
--red:#DC2626;    /* danger */
--ink:#111827;    /* texto y barras de sección */
--paper:#FBF7F0;  /* fondo: crema, NO el blanco del token riso */
--surface:#FFFFFF;/* fondo de tarjetas */
--muted:#5B6474;
--line:rgba(17,24,39,.14);
```

**Desvío deliberado del token riso:** riso define `surface: #FFFFFF`. Acá el
*fondo de página* es crema `#FBF7F0` y el blanco queda reservado para las
tarjetas. Eso es lo que da el aire de papel de diario y el contraste tarjeta
sobre papel. **No lo "corrijas" a blanco.**

### Disciplina de dos tintas

La estética riso imita impresión con dos tintas superpuestas. Respetá los roles:

- **Rosa** = lo que llama la atención: kicker, "Por qué importa", nota principal,
  numeritos de sección, acentos del pie, sombras de desfase.
- **Azul** = lo que estructura: borde izquierdo de las notas comunes, cabecera,
  encabezados de tabla, etiquetas de los `.brief`.
- **Ink** = texto y las barras de sección.
- **Verde / ámbar / rojo** = solo semántica de estado: chips y semáforo de
  transporte. Nunca decorativos.

---

## 2. Tipografía

```css
--sans:"Space Grotesk","Space Grotesk Variable",-apple-system,BlinkMacSystemFont,
       "Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
--mono:"Overpass Mono","Roboto Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
```

Se nombran las fuentes riso primero y el sistema cubre el resto: así se respeta
el sistema de diseño sin romper la regla de "sin dependencias externas".

| Rol | Familia | Tamaño | Peso | Detalle |
|---|---|---|---|---|
| Logo | sans | `clamp(44px,11vw,88px)` | 900 | `line-height:.86`, `letter-spacing:-.035em` |
| Titular (`h3`) | sans | `clamp(21px,3.1vw,27px)` | 700 | `line-height:1.22`, `letter-spacing:-.02em` |
| Cuerpo | sans | 16px | 400 | `line-height:1.6`, color `#1F2937` |
| "Por qué importa" | sans | 15px | 400 | `line-height:1.55` |
| Etiquetas mono | mono | 11–12px | 700 | MAYÚSCULAS, `letter-spacing:.1em`–`.14em` |
| Número gigante (semáforo) | sans | 30px | 900 | `letter-spacing:-.03em` |

**Regla de oro:** la mono va **siempre** en mayúsculas y con tracking ancho. Es
la voz institucional del diario — kickers, chips, encabezados de sección, fecha,
captions de tabla, títulos y colofón del pie. La sans **nunca** va en mayúsculas
con tracking. Si dudás de qué familia usar: ¿es una etiqueta o un metadato? mono.
¿Es contenido que se lee? sans.

---

## 3. Espaciado, radios y sombras

```css
--s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px;
--r-sm:4px; --r-md:8px;
```

Escala 4/8/12/16/24/32 de riso. Usá siempre las variables, nunca px sueltos.

- **Ningún radio mayor a 8px.** El riso es de bordes duros.
- **Ninguna sombra con blur.** Las sombras son de *desfase de registro*
  (el error de impresión que define la estética): offset sólido, blur 0, en la
  otra tinta.
  - Logo: `text-shadow:3px 3px 0 var(--pink)`
  - `.lede`: `box-shadow:5px 5px 0 var(--pink)`
  - `article.item.lead`: `box-shadow:4px 4px 0 rgba(44,64,167,.16)`

---

## 4. Trama de semitono (el sello de la estética)

Puntos de tinta en dos superficies, y solo en esas dos:

```css
/* body: puntos azules sobre crema */
background-image:radial-gradient(circle at 1px 1px, rgba(44,64,167,.09) 1px, transparent 0);
background-size:7px 7px;

/* masthead: puntos rosas sobre azul */
background-image:radial-gradient(circle at 1px 1px, rgba(242,55,161,.5) 1px, transparent 0);
background-size:8px 8px;
```

Las tarjetas van blancas y lisas: el contraste entre la trama del papel y la
tarjeta limpia es lo que hace legible la página. No tramar las tarjetas.

---

## 5. Layout

Una sola columna. `.wrap { max-width:940px; margin:0 auto; padding:0 16px 32px }`,
repetido en la cabecera, el cuerpo y el pie. Secciones separadas por 32px.
Sin barras laterales ni grillas de columnas — la única grilla es la del semáforo
de transporte.

---

## 6. Componentes

Orden de la página: `masthead` → `.lede` → 6 `section` → `footer`.

### 6.1 `header.masthead`
Ancho completo en azul con trama rosa, `border-bottom:4px solid var(--pink)`.
Adentro, `.brandrow` en flex con `justify-content:space-between`:
- izquierda: `h1.logo` "EL PARTE" en blanco con desfase rosa + `.tagline` mono;
- derecha: `.dateblock` mono alineado a la derecha, con `border-left:3px solid var(--pink)`,
  fecha completa en `<strong>` y la hora de cierre en ART.

  **La hora de cierre nunca se tipea a mano.** En `cuerpo.html` va el marcador
  `{{HORA_CIERRE}}` (tanto en el `.dateblock` como en el `.colofon` del pie,
  §6.10) y `armar.py` lo reemplaza por la hora real, tomada del reloj en el
  momento de esa corrida, en ART (UTC-3 fijo). Escribir una hora fija ahí —o
  copiarla de la edición anterior— es exactamente el bug que este mecanismo
  vino a resolver: la hora que mostraba el diario no era la hora real en que
  se había armado la edición.

### 6.2 `.lede` — "Lo que ordena el día"
Tarjeta blanca, `border:2px solid var(--ink)`, radio 8, desfase rosa de 5px.
Contiene una `<ol class="index">` con **exactamente 3 ítems**: los tres títulos
que ordenan la jornada, a 17px/500. Los marcadores van en rosa y mono.

### 6.3 `.sechead` — barra de sección
`position:sticky; top:0`, fondo ink, radio 4. Tres partes:
`.secnum` (chip rosa con número de dos dígitos, **01 a 06**) + `h2` mono en
mayúsculas + `.secmeta` empujado a la derecha con `margin-left:auto`, en mono
tenue, listando los subtemas.

Numeración fija de las secciones:
`01 Nacional` · `02 Internacional` · `03 Deporte · Fórmula 1` · `04 Música` ·
`05 Mi Barrio · Belgrano / Núñez` · `06 Servicios · Transporte`.

### 6.4 `article.item` — la nota
Tarjeta blanca, borde fino `--line`, radio 8, padding `16px 24px`, y sobre todo
un **borde izquierdo de 5px**: azul por defecto, **rosa** cuando lleva `.lead`.
`.lead` suma además el desfase azul.

Orden interno, siempre el mismo:

1. `.kicker` — mono rosa, mayúsculas. Formato `Tema · Subtema`.
2. `h3` — el titular.
3. uno o dos `.chip` de estado.
4. párrafos de contexto.
5. `.why` — "Por qué importa".

### 6.5 `.chip` — etiqueta de estado
Mono 11px en mayúsculas, `border:1px solid currentColor`, fondo de la misma
tinta al 10–14%, radio 4. Variantes: `.blue .pink .green .amber .red .grey`.

### 6.6 `.why` — "Por qué importa"
`border-left:4px solid var(--pink)`, fondo rosa al 5,5%, radio solo en las
esquinas derechas (`0 4px 4px 0`), label mono rosa y una idea en 15px.
**Una sola por nota**, y solo en `article.item` — nunca en un `.brief`.

### 6.7 `.brief` — la línea de "sin novedades"
Fila flex con **borde punteado**: etiqueta mono azul (`min-width:96px`) y una
sola oración. Es el componente que sostiene la regla de no rellenar: un tema sin
novedad del día es un `.brief`, no una nota estirada. En mobile se apila.

### 6.8 Tablas (`.tablewrap` + `table`)
Envueltas en `overflow-x:auto` con `min-width:460px`, para que scrolleen solas
sin romper la página. `caption` mono tenue arriba a la izquierda. `thead` azul
con mono en mayúsculas. `td.pos` mono rosa; `td.pts` mono a la derecha.
`tr.hl` con tinte rosa marca **las filas que le importan al lector**: Ferrari y
Colapinto.

### 6.9 `.lines` — semáforo de transporte
`grid-template-columns:repeat(auto-fit,minmax(210px,1fr))`. Cada `.line` es una
tarjeta cuyo **borde superior de 5px** carga el estado: verde por defecto,
`.watch` ámbar, `.alert` rojo. Adentro: número gigante (900), estado en mono con
un `●` adelante, y una línea de detalle.

Las líneas **130** y **67** llevan tarjeta propia siempre, aunque no pase nada.
Si están afectadas, van en `.alert` (rojo).

### 6.10 `footer`
Fondo ink, `border-top:4px solid var(--pink)`, texto `#E5E7EB`. Lleva:
- `h2` mono rosa "Fuentes consultadas" + `.sources`, chips mono con borde tenue;
- `h2` "Sobre el equilibrio de esta edición" + `.balance` con barra rosa a la izquierda;
- `.colofon`, línea mono tenue con fecha y hora de cierre.

---

## 7. Cómo el contenido decide el diseño

Esta es la parte que importa más que los píxeles.

- **`.lead` = jerarquía editorial.** Como máximo una nota `.lead` por sección, y
  solo si de verdad hubo un hecho principal. Una sección sin novedad fuerte no
  tiene `.lead`.
- **El color del chip es la temperatura del tema**, no decoración:
  | chip | cuándo |
  |---|---|
  | `pink` | novedad del día, lo que pasó hoy |
  | `blue` | contexto, estado neutro, en curso |
  | `amber` | tensión, a confirmar, punto de vigilancia |
  | `red` | crisis, conflicto abierto, servicio afectado |
  | `green` | resuelto, normal, positivo |
  | `grey` | sin novedades |
- **Día flojo = edición más corta.** Más `.brief`, menos `article.item`. La
  página tiene que *verse* más corta, no rellenarse. Está explícitamente
  prohibido inflar.
- **Cuando las fuentes no coinciden**, decilo en la página con un `.brief` de
  etiqueta "Aclaración" (así se resolvió la diferencia de puntos de Hamilton en
  la tabla de F1) en vez de inventar una cifra prolija.
- El pie de equilibrio y el bloque de fuentes van **siempre**, en todas las
  ediciones.

---

## 8. Responsive e impresión

```css
@media (max-width:640px){
  .brandrow{align-items:flex-start;flex-direction:column}
  .dateblock{text-align:left}
  article.item{padding:var(--s4)}
  .brief{flex-direction:column;gap:var(--s1)}
  .sechead{position:static}   /* la barra pegajosa molesta en pantalla chica */
}
@media print{
  body{background:#fff}
  .sechead{position:static}
}
```

---

## 9. Qué se mantiene y qué cambia entre ediciones

**Estable** (el lector reconoce el diario por esto): masthead, paleta, trama,
tipografía, numeración 01–06 de las secciones, `.lede` de tres ítems, pie de
fuentes y equilibrio.

**Cambia todos los días**: fecha en el `.dateblock`, el `<title>`, el `.colofon`,
los tres ítems del índice, y qué nota lleva `.lead` en cada sección. La *hora*
de cierre también cambia todos los días, pero no la escribís vos: es el
marcador `{{HORA_CIERRE}}` (§6.1), que `armar.py` completa solo con la hora
real de esa corrida.

Lo estable vive en `plantilla.html` y lo diario en `cuerpo.html` (§0.1), así que
en la práctica **una edición nueva toca `cuerpo.html` y nada más**.

### 9.1 Leer la edición anterior

Antes de escribir, leé el `cuerpo.html` de la edición anterior — no el
`index.html` entero: los ~10 KB de CSS son siempre los mismos y no aportan nada.

Leerlo no es opcional ni es sólo por el tono. Es lo que permite **detectar que un
dato de ayer quedó viejo o estaba mal**, y corregirlo con un `.brief` de
"Aclaración" como manda el §7, en vez de arrastrar el error o de cambiar una
cifra en silencio. La edición del 6/9/2026 corrigió así dos cosas de la víspera:
la tabla del campeonato de F1 (los valores publicados correspondían a un corte
anterior al GP de Países Bajos) y la fecha de salida del disco de Dillom.

---

## 10. Publicación

Primero `python3 armar.py` (§0.1). Si falla, **no se publica**: se arregla
`cuerpo.html` y se vuelve a armar.

Deploy a Vercel con `deploy_to_vercel`, **proyecto `el-parte`** (siempre el
mismo, nunca uno nuevo), `target: "production"`, `projectSettings` con
`framework: null` y los comandos en `null` — es HTML estático, no hay build.

La herramienta manda el contenido **inline**: no acepta una ruta de archivo, así
que el HTML entero viaja en el parámetro `data`. Mandá el `index.html` ya
generado, nunca `plantilla.html` (que tiene los marcadores sin reemplazar) ni un
placeholder.

Se evaluó conectar el proyecto al repo con `create_git_project` para que el push
fuera el deploy y ahorrarse esos ~45 KB inline. **Se descartó a propósito**: el
deploy por git es asincrónico y haría perder el `READY`, que —con `*.vercel.app`
bloqueado y el token sin permiso de lectura sobre el scope— es la única señal de
que la edición salió. En una rutina desatendida, saber que se publicó vale más
que el ahorro. No lo "optimices" sin volver a plantearlo.

En esta sesión el proxy de red bloquea el dominio `*.vercel.app` y el token no
tiene permiso de lectura sobre el scope de la cuenta, así que **no se puede
verificar la URL publicada desde acá**: el único indicador confiable es el
`READY` que devuelve la herramienta de deploy. Decilo así en el resumen, sin
afirmar que la viste.

---

## 11. Cierre de la corrida: la edición tiene que quedar en `main`

Cada ejecución de la rutina trabaja sobre una rama autogenerada distinta
(`claude/algo-aleatorio`). **Si la edición se queda ahí, `main` no avanza**, y la
corrida del día siguiente lee como "la edición de ayer" una que en realidad es
de hace días: repite correcciones ya hechas y arrastra datos viejos. Pasó el
6/9/2026, cuando `main` había quedado en la edición del 5/9.

Por eso, después de publicar:

```bash
git add -A && git commit -m "Edición del <día> de <mes> de <año>"
git push -u origin <rama-de-la-corrida>

git fetch origin main
git merge-base --is-ancestor origin/main HEAD \
  && git push origin <rama-de-la-corrida>:main \
  || echo "divergencia: NO mergear, reportarlo en el resumen"
```

**El dueño del repo autorizó este merge de forma permanente** (6/9/2026), así que
no hace falta volver a pedirlo en cada corrida. La autorización cubre exactamente
esto y nada más:

- **Sólo fast-forward.** Verificá primero que `origin/main` sea ancestro del HEAD,
  como en el comando de arriba. Si divergieron, **frená**: no mergees, no fuerces,
  y contalo en el resumen.
- **Nunca** `--force`, `--force-with-lease` ni reescritura de historia sobre `main`.
- Si el `armar.py` no pasó o el deploy no devolvió `READY`, igual commiteá y
  pusheá el trabajo, pero **decí claramente en el resumen que la edición no se
  publicó**, para que no parezca una corrida normal.
