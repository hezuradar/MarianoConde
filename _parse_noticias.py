# -*- coding: utf-8 -*-
"""Extrae todas las noticias descargadas a noticias-data.json.

Lee el inventario canónico (_noticias_todas.json), reconstruye el contenido
de cada artículo desde contenido-original/*.html y añade las noticias de
prensa externa que aparecen destacadas en la web. El resultado lo consume
build_site.py para generar una página propia por noticia en las dos versiones.
"""
from pathlib import Path
from html.parser import HTMLParser
import html as htmlmod
import json
import re
from urllib.parse import unquote

ORIG = Path('contenido-original')
IMGDIR = Path('assets/img')

MESES = ('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
         'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre')

VOID = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'wbr',
        'area', 'base', 'col', 'embed', 'param', 'track'}
ALLOWED = {'p', 'h2', 'h3', 'h4', 'h5', 'ul', 'ol', 'li', 'blockquote',
           'figure', 'figcaption', 'img', 'iframe', 'a', 'strong', 'em',
           'b', 'i', 'br', 'hr'}

# Páginas del rediseño a las que deben apuntar los enlaces internos del original
LOCAL_PAGES = {
    'guitarras': 'guitarras.html',
    'guitarras-flamencas': 'flamencas.html',
    'guitarras-clasicas-de-concierto': 'clasicas.html',
    'guitarras-del-poema': 'poema.html',
    'poem-guitars': 'poema.html',
    'galeria': 'galeria.html',
    'gallery': 'galeria.html',
    'historia': 'historia.html',
    'history': 'historia.html',
    'noticias': 'noticias.html',
    'news': 'noticias.html',
    'contacto': 'contacto.html',
    'contact': 'contacto.html',
    'taller-en-directo': 'directo.html',
    'live-workshop': 'directo.html',
}

# Noticias de fuentes externas que aparecen en el bloque de destacadas
EXTERNAL = [
    {
        'original_slug': 'expoflamenco-115-anos',
        'title': '115 años de una saga de guitarreros de Madrid',
        'description': 'ExpoFlamenco repasa la historia de cinco generaciones de guitarreros de la familia Conde en Madrid.',
        'date': '2026-01-01',
        'date_label': '2026',
        'image': 'MC_Historia_9.webp',
        'category': 'oficio',
        'source': 'ExpoFlamenco',
        'source_url': 'https://expoflamenco.com/revista/mariano-conde-ciento-quince-anos-de-una-saga-de-guitarreros-de-madrid/',
        'featured': True,
    },
    {
        'original_slug': 'abc-ed-sheeran',
        'title': 'El secreto de la guitarra «madrileña» de Ed Sheeran',
        'description': 'ABC cuenta la relación entre el artista británico y una guitarra construida en el taller de la calle Amnistía.',
        'date': '2017-01-27',
        'image': 'MC_Escenario_22-768x330.webp',
        'category': 'oficio',
        'source': 'ABC',
        'source_url': 'https://www.abc.es/espana/madrid/abci-secreto-guitarra-madrilena-sheeran-201701270021_noticia.html',
        'featured': True,
    },
    {
        'original_slug': 'confidencial-cuatro-generaciones',
        'title': 'Cuatro generaciones de luthiers',
        'description': 'El Confidencial retrata el oficio de los luthiers de la familia Conde y la vida del taller madrileño.',
        'date': '2016-08-07',
        'image': 'MC_Historia_4.webp',
        'category': 'oficio',
        'source': 'El Confidencial',
        'source_url': 'https://www.elconfidencial.com/cultura/2016-08-07/luthier-mariano-conde-guitarra-oficios-cultura_1243339/',
        'featured': True,
    },
    {
        'original_slug': 'elmundo-60-guitarras',
        'title': 'Unas 60 guitarras al año y maderas secadas hasta 30 años',
        'description': 'El Mundo se adentra en un taller donde el tiempo de secado de la madera marca el ritmo de cada instrumento.',
        'date': '2018-04-28',
        'image': 'barnizado-guitarras.webp',
        'category': 'maderas',
        'source': 'El Mundo',
        'source_url': 'https://www.elmundo.es/papel/historias/2018/04/28/5ae3061046163f25178b4629.html',
        'featured': True,
    },
]

FEATURED_OWN = {
    'estreno-mundial-mariano-conde-los-guitarreros-que-enamoraron-al-maestro-paco-de-lucia',
    'la-emocion-de-una-guitarra-con-alma-samuel-del-rio-carmona-primer-ganador-del-premio-mariano-conde-en-el-festival-internacional-del-cante-de-las-minas',
}


def sanitize_name(name):
    return re.sub(r'[^\w.\-áéíóúñÁÉÍÓÚÑ]', '_', name)


def local_image(url, fallback):
    """Convierte una URL de imagen remota en una ruta assets/img/ si existe."""
    if not url:
        return fallback
    name = unquote(url.rsplit('/', 1)[-1]).split('?')[0].split('#')[0]
    for candidate in (name, sanitize_name(name)):
        if candidate and (IMGDIR / candidate).exists():
            return 'assets/img/' + candidate
    return fallback


def find_fallback_image(raw):
    for url in re.findall(r'https://marianoconde\.com/wp-content/uploads/[^"\s\)]+?\.(?:webp|jpg|jpeg|png)', raw):
        name = unquote(url.rsplit('/', 1)[-1])
        if 'logo' in name.lower():
            continue
        found = local_image(url, None)
        if found:
            return found
    return 'assets/img/Carrousel03_01.webp'


def meta_content(raw, pattern):
    m = re.search(pattern, raw, re.S | re.I)
    return htmlmod.unescape(m.group(1)).strip() if m else ''


def label_date(date):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', date or '')
    if not m:
        return 'Archivo'
    y, mo, d = m.groups()
    try:
        return f'{int(d)} de {MESES[int(mo) - 1]} de {y}'
    except (ValueError, IndexError):
        return y


def category_of(title):
    low = title.lower()
    if any(k in low for k in ('madera', 'abeto', 'cedro', 'koa', 'caoba', 'ébano',
                              'ebano', 'palo santo', 'palosanto', 'arce', 'barniz')):
        return 'maderas'
    if any(k in low for k in ('sonido', 'sustain', 'cuerda', 'desafina', 'seco',
                              'boca', 'tapa', 'resonancia', 'diapasón', 'trastes')):
        return 'sonido'
    return 'oficio'


class WidgetCapture(HTMLParser):
    """Captura los tokens HTML del contenido real del artículo."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.depth = 0
        self.ignore_depth = 0
        self.tokens = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.active:
            classes = (attrs.get('class') or '').split()
            if 'elementor-widget-theme-post-content' in classes:
                self.active = True
                self.depth = 1
            return
        if tag in ('script', 'style', 'noscript'):
            self.ignore_depth += 1
            return
        if self.ignore_depth:
            return
        if tag not in VOID:
            self.depth += 1
        self.tokens.append(('start', tag, attrs))

    def handle_endtag(self, tag):
        if not self.active:
            return
        if tag in ('script', 'style', 'noscript'):
            self.ignore_depth = max(0, self.ignore_depth - 1)
            return
        if self.ignore_depth:
            return
        self.tokens.append(('end', tag, {}))
        if tag not in VOID:
            self.depth -= 1
            if self.depth <= 0:
                self.active = False

    def handle_data(self, data):
        if self.active and not self.ignore_depth:
            self.tokens.append(('data', data, {}))


def youtube_id(src):
    m = re.search(r'youtube(?:-nocookie)?\.com/embed/([\w-]+)', src or '')
    if m:
        return m.group(1)
    m = re.search(r'youtube\.com/watch\?(?:.*&)?v=([\w-]+)', src or '')
    return m.group(1) if m else None


def resolve_link(href, slugs_map, source_url):
    """Reescribe enlaces del contenido para que apunten a la nueva web."""
    if not href:
        return '#', False
    href = htmlmod.unescape(href)
    if href.startswith('https://marianoconde.com/') or href.startswith('http://marianoconde.com/'):
        path = href.split('marianoconde.com/', 1)[1].split('?')[0].split('#')[0].strip('/')
        if path.startswith('en/'):
            return href, True
        parts = [p for p in path.split('/') if p]
        if not parts:
            return 'index.html', False
        if parts[0] == 'guitarras-del-poema':
            return 'poema.html', False
        if parts[0] == 'guitarras':
            if len(parts) >= 3 and parts[1] in (
                    'guitarras-flamencas', 'guitarras-clasicas-de-concierto'):
                slug = parts[-1]
                special = {'ac23': 'modelo-ac-23.html', 'ac23-r': 'modelo-ac-23-r.html'}
                return special.get(slug, f'modelo-{slug}.html'), False
            return 'guitarras.html', False
        last = parts[-1]
        if last in slugs_map:
            return slugs_map[last], False
        if last in LOCAL_PAGES:
            return LOCAL_PAGES[last], False
        if len(parts) == 1 and not last.endswith(('.html', '.php', '.xml')):
            return 'noticias.html', False
        return href, True
    if href.startswith(('http://', 'https://', '//')):
        return href, True
    if href.startswith('mailto:') or href.startswith('tel:'):
        return href, False
    return href, False


def render_tokens(tokens, fallback_image, slugs_map, source_url):
    out = []
    for kind, tag, attrs in tokens:
        if kind == 'data':
            # Las menciones en texto se convierten en la marca; el correo se respeta
            text = re.sub(r'(?<!@)(?:www\.)?marianoconde\.com', 'Mariano Conde', tag)
            out.append(htmlmod.escape(text, quote=False))
            continue
        if kind == 'end':
            # El iframe se escribe completo en su etiqueta de apertura
            if tag in ALLOWED and tag not in VOID and tag != 'iframe':
                out.append(f'</{tag}>')
            continue
        if tag == 'img':
            src = local_image(attrs.get('src'), fallback_image)
            alt = htmlmod.escape(attrs.get('alt') or '', quote=True)
            out.append(f'<img src="{src}" alt="{alt}" loading="lazy">')
        elif tag == 'iframe':
            vid = youtube_id(attrs.get('src'))
            if vid:
                out.append(
                    '<iframe src="https://www.youtube-nocookie.com/embed/'
                    f'{vid}?rel=0&amp;modestbranding=1" title="Vídeo de Mariano Conde" '
                    'loading="lazy" allow="accelerometer; autoplay; clipboard-write; '
                    'encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
        elif tag == 'a':
            href, external = resolve_link(attrs.get('href'), slugs_map, source_url)
            extra = ' target="_blank" rel="noopener"' if external else ''
            out.append(f'<a href="{htmlmod.escape(href, quote=True)}"{extra}>')
        elif tag in ALLOWED:
            out.append(f'<{tag}>')
    raw = ''.join(out)
    # El original tiene etiquetas mal anidadas (<p></li>, <li></p>): se limpian
    raw = re.sub(r'<p>\s*(?=</(?:li|ul|ol|div|h[1-6]|blockquote|figure)>)', '', raw)
    raw = re.sub(r'(<(?:li|ul|ol|div|h[1-6]|blockquote|figure)>)\s*</p>', r'\1', raw)
    raw = re.sub(r'</p>\s*(?=</(?:li|ul|ol|div|h[1-6]|blockquote|figure)>)', '', raw)
    raw = re.sub(r'<p>\s*</p>', '', raw)
    raw = re.sub(r'[ \t]+', ' ', raw)
    raw = re.sub(r'\n\s*\n+', '\n', raw)
    return raw.strip()


def file_name(slug):
    if len(slug) <= 78:
        return 'noticia-' + slug + '.html'
    import hashlib
    suffix = hashlib.sha1(slug.encode('utf-8')).hexdigest()[:6]
    return 'noticia-' + slug[:72].rstrip('-') + '-' + suffix + '.html'


def external_body(entry):
    source = htmlmod.escape(entry['source'])
    url = htmlmod.escape(entry['source_url'], quote=True)
    return (f'<p>{htmlmod.escape(entry["description"])}</p>'
            f'<p>Esta noticia procede de <strong>{source}</strong>. '
            'El texto completo está disponible en su publicación original.</p>'
            f'<p><a href="{url}" target="_blank" rel="noopener">'
            f'Leer en {source} ↗</a></p>')


def main():
    inventory = json.loads(Path('_noticias_todas.json').read_text(encoding='utf-8'))
    slugs = []
    for item in inventory:
        url = item['url']
        slug = url.rstrip('/').rsplit('/', 1)[-1]
        if slug and slug not in slugs:
            slugs.append(slug)
    # Dos artículos del original sin <h1> que no están en el inventario
    for extra in ('ed-sheeran-mariano-conde-periodico-abc', 'leonard-cohen-mariano-conde'):
        if extra not in slugs and (ORIG / (extra + '.html')).exists():
            slugs.append(extra)

    entries = []
    for slug in slugs:
        path = ORIG / (slug + '.html')
        if not path.exists():
            print('FALTA:', slug)
            continue
        raw = path.read_text(encoding='utf-8', errors='ignore')
        title = meta_content(raw, r'<h1[^>]*>(.*?)</h1>')
        title = re.sub(r'<[^>]+>', '', title)
        title = re.sub(r'\s+', ' ', htmlmod.unescape(title)).strip()
        if not title:
            title = meta_content(raw, r'<title>(.*?)</title>').split('|')[0].strip()
        description = meta_content(raw, r'<meta\s+name="description"\s+content="([^"]*)"')
        description = re.sub(r'\s+', ' ', description)
        description = re.sub(r'(?<!@)(?:www\.)?marianoconde\.com', 'Mariano Conde', description)
        date = meta_content(raw, r'<meta\s+property="article:published_time"\s+content="([^"]*)"')
        if not date:
            date = meta_content(raw, r'<meta\s+property="og:updated_time"\s+content="([^"]*)"')
        og = meta_content(raw, r'<meta\s+property="og:image"\s+content="([^"]*)"')
        fallback = find_fallback_image(raw)
        image = local_image(og, fallback)
        capture = WidgetCapture()
        capture.feed(raw)
        entries.append({
            'original_slug': slug,
            'file': file_name(slug),
            'title': title,
            'description': description or title,
            'date': date[:10] if date else '',
            'date_label': label_date(date),
            'image': image,
            'category': category_of(title),
            'source': 'Taller Mariano Conde',
            'source_url': f'https://marianoconde.com/{slug}/',
            'en_url': '',
            'featured': slug in FEATURED_OWN,
            'external': False,
            'body': render_tokens(capture.tokens, fallback, {}, ''),
        })

    slugs_map = {e['original_slug']: e['file'] for e in entries}
    for e in entries:  # segunda pasada ya con el mapa completo
        path = ORIG / (e['original_slug'] + '.html')
        raw = path.read_text(encoding='utf-8', errors='ignore')
        capture = WidgetCapture()
        capture.feed(raw)
        e['body'] = render_tokens(capture.tokens, e['image'], slugs_map, e['source_url'])

    for item in EXTERNAL:
        e = dict(item)
        e['file'] = file_name(item['original_slug'])
        e['title'] = item['title']
        e['description'] = item['description']
        e['image'] = local_image(item['image'], 'assets/img/Carrousel03_01.webp')
        e['date_label'] = item.get('date_label') or label_date(item['date'])
        e['en_url'] = ''
        e['external'] = True
        e['body'] = external_body(item)
        entries.append(e)

    entries.sort(key=lambda e: (e['date'] or '0000'), reverse=True)
    Path('noticias-data.json').write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print('NOTICIAS:', len(entries))
    print('DESTACADAS:', sum(1 for e in entries if e['featured']))
    print('CON TEXTO:', sum(1 for e in entries if len(e['body']) > 40))
    for e in entries[:3]:
        print(' -', e['title'][:70], '|', e['date_label'])


if __name__ == '__main__':
    main()
