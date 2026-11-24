# -*- coding: utf-8 -*-
"""Construye el diccionario ES→EN usado por build_site.py para la web inglesa.

Las cadenas se extraen de las páginas españolas ya generadas, se traducen en
lotes con el endpoint público de Google Translate y se guardan en
``translations-en.json``. El archivo queda versionado: regenerar la web nunca
necesita red, y las correcciones manuales se conservan en
``i18n-overrides.json``.

Uso:  python _translate_site.py
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'translations-en.json'
OVERRIDES_FILE = ROOT / 'i18n-overrides.json'
ENDPOINT = ('https://translate.googleapis.com/translate_a/single'
            '?client=gtx&sl=es&tl=en&dt=t&q=')
ATTRS = ('alt', 'title', 'aria-label', 'placeholder', 'content')

# Nombres propios y dirección: el traductor automático los deforma
# ("Conde Hermanos" → "Count Brothers", "Amnistía" → "Amnesty"...).
PROTECT = [
    'Mariano Conde Cavia', 'Conde Hermanos', 'Mariano Conde', 'Conde',
    'Paco de Lucía', 'Ed Sheeran', 'Leonard Cohen', 'Pozuelo', 'Pharaon',
    'Amnistía', 'Gravina', 'Felipe V', 'Madrid', 'España',
    'Domingo Esteso', 'Íñigo Cifuentes', 'Amós Lora', 'Samuel del Río',
    'Joaquín', 'Gregorio Moya', 'José Viñas', 'Encarni', 'ExpoFlamenco',
    'Telemadrid', 'Teatro Isabel la Católica', 'Isabel la Católica',
    'Uztai', 'AEPD', 'CIF', 'MC', 'RGPD', 'LOPDGDD',
]


def norm(text: str) -> str:
    return ' '.join(html.unescape(text).split())


def extract() -> set[str]:
    found: set[str] = set()
    tag_re = re.compile(r'(<[^>]+>)')
    attr_re = re.compile(r'\b(' + '|'.join(ATTRS) + r')="([^"]*)"')
    for path in sorted(ROOT.glob('*.html')):
        doc = path.read_text(encoding='utf-8')
        pieces = tag_re.split(doc)
        in_raw = False
        for i, piece in enumerate(pieces):
            if i % 2 == 1:
                if re.match(r'<(script|style)\b', piece, re.I):
                    in_raw = True
                elif re.match(r'</(script|style)\b', piece, re.I):
                    in_raw = False
                for _, value in attr_re.findall(piece):
                    key = norm(value)
                    if key:
                        found.add(key)
                continue
            if in_raw:
                continue
            key = norm(piece)
            if key:
                found.add(key)
    return found


def protect(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def sub(match: re.Match) -> str:
        saved.append(match.group(0))
        return f'\ue000{len(saved) - 1}\ue001'

    pattern = '|'.join(re.escape(token) for token in sorted(PROTECT, key=len, reverse=True))
    return re.sub(pattern, sub, text), saved


def restore(text: str, saved: list[str]) -> str:
    def sub(match: re.Match) -> str:
        index = int(match.group(1))
        return saved[index] if index < len(saved) else match.group(0)
    return re.sub('\ue000(\\d+)\ue001', sub, text)


SEPARATOR = '\ue100'


def translate_batch(items: list[str]) -> list[str]:
    wrapped, saved = zip(*(protect(item) for item in items))
    # El traductor parte los párrafos con varios puntos en varios fragmentos,
    # así que no podemos aparearfragmento por cadena. Un separador de uso
    # privado sobrevive al traductor y nos permite reconstruir cada cadena.
    query = urllib.parse.quote(('\n' + SEPARATOR + '\n').join(wrapped))
    for attempt in range(4):
        try:
            req = urllib.request.Request(ENDPOINT + query,
                                         headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=45) as response:
                data = json.loads(response.read().decode('utf-8'))
            stream = ''.join(chunk[0] for chunk in data[0])
            pieces = stream.split(SEPARATOR)
            if len(pieces) != len(items):
                raise ValueError(f'{len(pieces)} traducciones para {len(items)} frases')
            return [restore(piece.replace('\n', ' '), list(saved[i])).strip()
                    for i, piece in enumerate(pieces)]
        except Exception as exc:  # noqa: BLE001 - reintentos con backoff
            if attempt == 3:
                print(f'  fallo definitivo en lote de {len(items)}: {exc}', file=sys.stderr)
                return list(items)
            time.sleep(1.5 * (attempt + 1))
    return list(items)


def batches(items: list[str], limit: int = 3500, count: int = 60) -> list[list[str]]:
    current: list[str] = []
    size = 0
    for item in items:
        extra = len(item) + 1
        if current and (size + extra > limit or len(current) >= count):
            yield current
            current, size = [], 0
        current.append(item)
        size += extra
    if current:
        yield current


def main() -> None:
    translations: dict[str, str] = {}
    if CACHE.exists():
        translations = json.loads(CACHE.read_text(encoding='utf-8'))
    if OVERRIDES_FILE.exists():
        translations.update(json.loads(OVERRIDES_FILE.read_text(encoding='utf-8')))

    strings = extract()
    pending = sorted(s for s in strings if s not in translations)
    print(f'Cadenas detectadas: {len(strings)} · ya traducidas: {len(strings) - len(pending)}'
          f' · pendientes: {len(pending)}')
    done = 0
    for group in batches(pending):
        for source, target in zip(group, translate_batch(group)):
            if target and target != source:
                translations[source] = target
        done += len(group)
        print(f'  {done}/{len(pending)}', flush=True)
    if OVERRIDES_FILE.exists():
        translations.update(json.loads(OVERRIDES_FILE.read_text(encoding='utf-8')))
    CACHE.write_text(json.dumps(dict(sorted(translations.items())), ensure_ascii=False,
                                indent=1) + '\n', encoding='utf-8')
    print(f'Guardadas {len(translations)} traducciones en {CACHE.name}.')


if __name__ == '__main__':
    main()
