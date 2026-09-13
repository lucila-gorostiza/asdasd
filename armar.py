#!/usr/bin/env python3
"""
Ensambla index.html a partir de plantilla.html (estable) y cuerpo.html (diario).

Antes de escribir, valida las restricciones duras del §0 de CLAUDE.md y la
estructura fija del §6. Si algo falla, NO escribe el archivo y sale con código 1:
el diario no se publica a medias.

Uso:  python3 armar.py
"""
import re
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PLANTILLA = RAIZ / "plantilla.html"
CUERPO = RAIZ / "cuerpo.html"
SALIDA = RAIZ / "index.html"

# Argentina está en UTC-3 fijo (sin horario de verano desde 2009): un offset
# fijo es más confiable acá que zoneinfo, que depende de que el sistema tenga
# la base tzdata instalada.
ART = timezone(timedelta(hours=-3))


def hora_cierre_art():
    """Hora real de cierre en ART, HH:MM, tomada del reloj al correr armar.py.

    cuerpo.html no debe hardcodear una hora: va el marcador {{HORA_CIERRE}},
    que se reemplaza acá con la hora real de esta corrida. Así el dateblock y
    el colofón siempre reflejan cuándo se armó la edición, en vez de arrastrar
    el valor de la edición anterior (lo que pasaba antes de este cambio)."""
    return datetime.now(ART).strftime("%H:%M")


def leer_cuerpo():
    """Devuelve (titulo, cuerpo). El título va en la primera línea de cuerpo.html
    como <!-- TITULO: ... --> para no tener que pasarlo por línea de comandos."""
    txt = CUERPO.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--\s*TITULO:\s*(.+?)\s*-->\s*\n", txt)
    if not m:
        salir(["cuerpo.html debe empezar con una línea <!-- TITULO: ... -->"])
    return m.group(1), txt[m.end():].strip("\n")


def bloques(html, apertura, cierre):
    """Trozos entre apertura y cierre, sin anidamiento (suficiente para <section>)."""
    return re.findall(apertura + r".*?" + cierre, html, re.S)


def validar(html):
    e = []

    # --- §0: restricciones duras ---
    if re.search(r"<script", html, re.I):
        e.append("§0: hay <script>; la página es HTML y CSS, sin JavaScript")
    externos = re.findall(r'(?:src|href)\s*=\s*["\']https?://[^"\']+', html, re.I)
    externos += re.findall(r"url\(\s*['\"]?https?://[^)]+", html, re.I)
    if externos:
        e.append(f"§0: recursos externos ({len(externos)}): {externos[:3]}")
    if "@import" in html:
        e.append("§0: @import en el CSS; todo va embebido")
    if "prefers-color-scheme" in html:
        e.append("§0: prefers-color-scheme; el diario es papel, solo modo claro")
    if 'lang="es-AR"' not in html:
        e.append('§0: falta lang="es-AR"')
    if html.count("<style") != 1:
        e.append("§0: debe haber exactamente un bloque <style> embebido")

    # --- marcadores: ninguno debe quedar sin reemplazar ---
    sin_reemplazar = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if sin_reemplazar:
        e.append(f"quedaron marcadores sin reemplazar: {sorted(set(sin_reemplazar))}")

    # --- §6.3: numeración fija de secciones ---
    nums = re.findall(r'class="secnum">(\d+)<', html)
    esperado = [f"{i:02d}" for i in range(1, 7)]
    if nums != esperado:
        e.append(f"§6.3: secciones {nums}, se esperaba {esperado}")

    # --- §6.2: el índice lleva exactamente 3 ítems ---
    lede = re.search(r'<ol class="index">(.*?)</ol>', html, re.S)
    if not lede:
        e.append("§6.2: falta la <ol class='index'> del .lede")
    else:
        n = len(re.findall(r"<li\b", lede.group(1)))
        if n != 3:
            e.append(f"§6.2: el índice tiene {n} ítems, deben ser exactamente 3")

    # --- §7: como máximo una nota .lead por sección ---
    for sec in bloques(html, r"<section\b", r"</section>"):
        num = re.search(r'class="secnum">(\d+)<', sec)
        etiqueta = num.group(1) if num else "?"
        leads = len(re.findall(r'class="item lead"', sec))
        if leads > 1:
            e.append(f"§7: la sección {etiqueta} tiene {leads} notas .lead, máximo 1")

    # --- §6.6: el .why va solo dentro de article.item, nunca en un .brief ---
    for m in re.finditer(r'class="why"', html):
        art = html.rfind("<article", 0, m.start())
        bri = html.rfind('<div class="brief"', 0, m.start())
        if bri > art:
            e.append("§6.6: hay un .why dentro de un .brief; va solo en article.item")
            break

    # --- estructura: etiquetas balanceadas ---
    e += desbalanceadas(html)
    return e


def desbalanceadas(html):
    huerfanas = {"meta", "br", "img", "input", "hr", "link", "source", "col"}

    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.pila = []
            self.malas = []

        def handle_starttag(self, tag, attrs):
            if tag not in huerfanas:
                self.pila.append(tag)

        def handle_endtag(self, tag):
            if self.pila and self.pila[-1] == tag:
                self.pila.pop()
            else:
                self.malas.append(tag)

    p = P()
    p.feed(html)
    problemas = []
    if p.pila:
        problemas.append(f"estructura: etiquetas sin cerrar: {p.pila[:5]}")
    if p.malas:
        problemas.append(f"estructura: cierres sin apertura: {p.malas[:5]}")
    return problemas


def salir(errores):
    print("El índice NO se escribió. Problemas encontrados:\n", file=sys.stderr)
    for x in errores:
        print(f"  ✗ {x}", file=sys.stderr)
    sys.exit(1)


def main():
    for f in (PLANTILLA, CUERPO):
        if not f.exists():
            salir([f"falta {f.name}"])

    titulo, cuerpo = leer_cuerpo()
    html = (
        PLANTILLA.read_text(encoding="utf-8")
        .replace("{{TITULO}}", titulo)
        .replace("{{CUERPO}}", cuerpo)
        .replace("{{HORA_CIERRE}}", hora_cierre_art())
    )

    errores = validar(html)
    if errores:
        salir(errores)

    SALIDA.write_text(html, encoding="utf-8")
    print(f"index.html armado · {len(html)} chars · {titulo}")
    print("Validaciones §0 y §6: todo en orden.")


if __name__ == "__main__":
    main()
