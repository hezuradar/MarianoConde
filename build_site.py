# -*- coding: utf-8 -*-
"""Genera el rediseño multi-página de Mariano Conde desde el material descargado."""
from pathlib import Path
import re
import json
import unicodedata
import html as htmlmod

OUT = Path('.')
OUT_M = OUT / 'm'
ORIG = Path('contenido-original')
IMGPATH = Path('assets/img')
MODEL_DATA = json.loads(Path('model-data.json').read_text(encoding='utf-8'))
POEMA_DATA = json.loads(Path('poema-data.json').read_text(encoding='utf-8'))
NOTICIAS_DATA = json.loads(Path('noticias-data.json').read_text(encoding='utf-8'))
SITE_URL = 'https://hezuradar.github.io/MarianoConde/'
OUT_EN = OUT / 'en'
OUT_EN_M = OUT_EN / 'm'
TRANS_FILE = Path('translations-en.json')
TRANSLATIONS = (json.loads(TRANS_FILE.read_text(encoding='utf-8'))
                if TRANS_FILE.exists() else {})

REVERB_URL = (
    'https://reverb.com/shop/guitarras-mariano-conde-conde-hermanos-'
    'sobrinos-de-esteso-s-gear-outlet?utm_source=rev-ios-app&'
    'utm_medium=ios-share&utm_campaign=shop&utm_content=2288101')

# Vídeos documentados en el sitio original
VIDEOS = [
    ('Documental «Los guardianes de la tradición»', '0KmZT-WlaTs',
     '_ESTRENO-MUNDIAL-Mariano-Conde-Los-guitarreros-que-enamoraron-al-maestro-Paco-de-Lucia.webp', 'Documental'),
    ('La saga Conde', '_ImLFVl-9iQ', 'MC_Historia_11.webp', 'Historia'),
    ('Primer vídeo del taller de la calle Amnistía, 1', 'R8WobwVvmIU',
     'MC_Historia_4.webp', 'El taller'),
    ('Reacción a las falacias de «solera flamenca»', 'eLx-rtyg30U',
     'MC_Escenario_22.webp', 'Actualidad'),
    ('Leonard Cohen & Mariano Conde', 'glCERZfJTBc', 'MC_Historia_2.webp', 'Música'),
    ('Amós Lora en Telemadrid', 'wIEEt_3pAOk', 'MC_Escenario_13.webp', 'Prensa'),
    ('Entrevista por Íñigo Cifuentes', 'yuIomU2WYoQ', 'MC_Historia_9.webp', 'Entrevista'),
]

PRESS_EVENTS = [
    ('24 de septiembre · 19:00 h', 'Teatro Isabel la Católica',
     'Concierto y encuentro en el marco del Festival de Cine Flamenco de Granada.'),
    ('2011', 'Premio Príncipe de Asturias de las Letras y las Artes',
     'Reconocimiento a la guitarra española y a sus intérpretes.'),
    ('Suma Flamenca', 'Madrid',
     'Presencia de las guitarras de la casa en la programación del festival.'),
    ('Prensa y radio', 'Joaquín @culturas_indomitas, Gregorio Moya, José Viñas y Encarni',
     'Reportajes y entrevistas sobre el oficio guitarrero de Mariano Conde.'),
]

EDITORIAL = {
    'flamencas.html': [
        ('Un legado que nos inspira',
         'En Mariano Conde, llevamos más de un siglo dedicándonos con pasión y entrega a la construcción de guitarras flamencas, manteniendo vivo un legado que comenzó en 1915 y que hoy sigue latiendo en nuestro taller de la calle Amnistía, en pleno corazón de Madrid. Somos herederos de una tradición familiar que ha marcado la historia de la guitarra española y del flamenco.'),
        ('Artesanía y materiales de primera',
         'Seleccionamos personalmente maderas como el ciprés español, el palosanto de India, el arce, el sicomoro, la caoba y el palo santo de Brasil. Para la tapa armónica empleamos pino abeto alemán o cedro rojo, maderas que aportan brillo, proyección y una respuesta dinámica ideal para el toque flamenco. El mango, generalmente de cedro, y el diapasón de ébano aseguran comodidad y resistencia.'),
        ('Nuestros modelos emblemáticos',
         'Pozuelo Flamenco: un homenaje a nuestra tradición familiar, con tapa de abeto macizo y aros y fondo de arce, sicomoro, caoba o palo santo de India. A28: referente por su volumen, sustain y proyección, con ciprés español y tapa de abeto alemán o cedro rojo, y posibilidad de personalizar color y tiro de cuerdas.'),
        ('Nuestro sonido y sensaciones',
         'Vivo, brillante, con graves profundos y agudos cristalinos. La respuesta es inmediata y la pulsación media con acción baja facilita el rasgueo, el picado y el alzapúa. El peso equilibrado y la altura de cuerdas perfectamente medida permiten largas sesiones de toque sin fatiga.'),
        ('Reconocimiento internacional',
         'Artistas como Paco Cepero, Jesús Guerrero, Joni Jiménez, António Higuero, Ed Sheeran y Robe (Extremo Duro) han confiado en la calidad y el carácter único de nuestras guitarras flamencas.'),
        ('Personalización y exclusividad',
         'Cada guitarra puede personalizarse según las preferencias del guitarrista: maderas, color, tiro de cuerdas, clavijero mecánico o de palillos, roseta y acabado. Todas están numeradas y certificadas.'),
    ],
    'clasicas.html': [
        ('Nuestra filosofía artesanal',
         'Desde el primer corte de madera hasta el último pulido, cada guitarra clásica de concierto es una obra de arte hecha a mano. Mantienen la esencia de la escuela madrileña y de la legendaria casa Conde Hermanos, con la cabeza de media luna y las iniciales MC grabadas a fuego en la tapa y etiquetas escritas a mano.'),
        ('Selección de maderas y materiales',
         'Elegimos personalmente cada pieza de palosanto de India, arce, koa o Madagascar para aros y fondo. Para la tapa ofrecemos pino abeto alemán o cedro rojo: el abeto aporta brillo y proyección, el cedro calidez y profundidad. El mástil, generalmente de cedro, y el diapasón de ébano garantizan comodidad y estabilidad.'),
        ('Modelos de guitarras clásicas de concierto',
         'Pozuelo Clásica combina tradición y modernidad con tapa de abeto macizo y aros y fondo de palosanto de India o caoba. EC-1 y EC-3 destacan por elegancia y versatilidad. AC-23 y AC-23/R son nuestras joyas de gama alta, con maderas poco comunes como arce, koa o Madagascar.'),
        ('Sonido y sensaciones',
         'Buscamos equilibrio, proyección y riqueza tímbrica: graves profundos, agudos cristalinos y una respuesta dinámica que permita expresar toda la gama de emociones de la música clásica. La acción de las cuerdas, la ergonomía del mástil y el peso equilibrado se cuidan al detalle.'),
        ('Reconocimiento y trayectoria',
         'Nuestras guitarras han sido elegidas por grandes intérpretes de la música clásica y por músicos de todo el mundo que buscan un instrumento fiable, bello y con un sonido inconfundible.'),
        ('Personalización y exclusividad',
         'Cada guitarrista es único: se pueden elegir maderas y acabados, el tiro de cuerdas (650 mm o 664 mm), el tipo de clavijero y detalles como la roseta, inspirada en los modelos históricos del taller. Todas nuestras guitarras están numeradas y certificadas.'),
    ],
}

# ---------------------------------------------------------------- datos
NAV = [
    ('index.html', 'Inicio'),
    ('guitarras.html', 'Guitarras'),
    ('directo.html', 'Taller en directo'),
    ('poema.html', 'Guitarras del Poema'),
    ('galeria.html', 'Galería'),
    ('noticias.html', 'Noticias'),
    ('historia.html', 'Historia'),
    ('contacto.html', 'Contacto'),
]

FLAMENCAS = [
    ('Pozuelo Flamenco', 'PozueloFlamenco.webp', 'Sicomoro · abeto', 'Edición singular', 'Pieza de carácter propio, con ataque directo y una proyección pensada para el escenario.'),
    ('Pozuelo Flamenco Caoba', 'Pozuelo-Caoba_1-1.webp', 'Caoba · abeto', 'Edición singular', 'La misma cabeza de media luna con aros y fondo de caoba: timbre cálido, respuesta redonda y gran comodidad de toque.'),
    ('Pozuelo Flamenco Palo Santo', 'PozueloFlamencoPaloSanto_1.webp', 'Palo santo · abeto', 'Edición singular', 'Variante en palo santo de India, de ataque seco y cuerpo profundo, pensada para el toque de concierto.'),
    ('Pharaon', '02_Pharaon.webp', 'Ciprés', 'Concierto', 'Respuesta inmediata y un sonido seco, la voz tradicional de la guitarra flamenca.'),
    ('EF4/5', 'EF4_5.webp', 'Ciprés · abeto', 'Profesional', 'Equilibrio entre dinámica y cuerpo para el acompañamiento al cante y al baile.'),
    ('EF5/N', 'EF5_N_01.webp', 'Ciprés · abeto', 'Profesional', 'Tacto ágil y gran riqueza armónica en una construcción totalmente artesanal.'),
    ('A28', 'A28.webp', 'Ciprés', 'Estudio', 'Ligereza y comodidad para largas sesiones de práctica sin perder identidad.'),
    ('A26', 'A26.webp', 'Cedro · ciprés', 'Concierto', 'Compás preciso, ataque limpio y la media luna reconocible de la casa Conde.'),
    ('A27/N', 'A27_N.webp', 'Palo santo · ciprés', 'Concierto', 'Profundidad y sustain para quienes buscan una guitarra con alma flamenca.'),
    ('AF25', 'AF25.webp', 'Ciprés', 'Concierto', 'Maderas seleccionadas y barniz tradicional para un sonido abierto y claro.'),
    ('AF25/R', 'AF25_R.webp', 'Ciprés · rosa', 'Concierto', 'Una variante de la AF25 con un color más cálido y respuesta muy equilibrada.'),
    ('Dedicación Flamenco', 'DedicacionClasicoFlamenco.webp', 'Ciprés', 'Edición', 'Instrumento de dedicatoria, construido sin prisas para un músico concreto.'),
]

CLASICAS = [
    ('Pozuelo clásica caoba', 'MarianoCondeGuitarras_102.webp', 'Caoba · abeto', 'Edición', 'Timbre dorado y cálido, con una proyección generosa en sala.'),
    ('Pozuelo clásica palo santo', 'PozueloPaloSanto_1.webp', 'Palo santo · abeto', 'Edición', 'Una de las piezas más singulares del taller, de gran profundidad sonora.'),
    ('EC-1', 'EC1.webp', 'Abeto · palo santo', 'Concierto', 'Tercera clásica de timbre redondo y respuesta cómoda para el recital.'),
    ('EC-3', 'EC3.webp', 'Abeto · palo santo', 'Concierto', 'Precisión y color en todos los registros, con la construcción tradicional de la casa.'),
    ('AC-23', 'AC23_01-1.webp', 'Abeto · palo santo', 'Concierto', 'Equilibrio entre ataque y cuerpo, pensada para una carrera de escenario.'),
    ('AC-23/R', 'AC23_R.webp', 'Abeto · palo santo', 'Concierto', 'Variante de la AC-23 con un carácter sonoro ligeramente más oscuro.'),
    ('Dedicación clásico', 'DedicacionClasicoFlamenco.webp', 'Abeto · palo santo', 'Edición', 'Construida para un intérprete concreto, con decisiones de madera a medida.'),
]

# Clave de cada ficha en el material original (precios, personalización y fotos)
MODEL_SOURCE = {
    'A26': 'guitarras_guitarras-flamencas_a26',
    'A27/N': 'guitarras_guitarras-flamencas_a27-n',
    'A28': 'guitarras_guitarras-flamencas_a28',
    'AF25': 'guitarras_guitarras-flamencas_af25',
    'AF25/R': 'guitarras_guitarras-flamencas_af25-r',
    'Dedicación Flamenco': 'guitarras_guitarras-flamencas_dedicacion-flamenco',
    'EF4/5': 'guitarras_guitarras-flamencas_ef4-5',
    'EF5/N': 'guitarras_guitarras-flamencas_ef5-n',
    'Pharaon': 'guitarras_guitarras-flamencas_pharaon',
    'Pozuelo Flamenco': 'guitarras_guitarras-flamencas_pozuelo-flamenco',
    'Pozuelo Flamenco Caoba': 'guitarras_guitarras-flamencas_pozuelo-flamenco-caoba',
    'Pozuelo Flamenco Palo Santo': 'guitarras_guitarras-flamencas_pozuelo-flamenco-palo-santo',
    'AC-23': 'guitarras_guitarras-clasicas-de-concierto_ac23',
    'AC-23/R': 'guitarras_guitarras-clasicas-de-concierto_ac23-r',
    'Dedicación clásico': 'guitarras_guitarras-clasicas-de-concierto_dedicacion-clasico',
    'EC-1': 'guitarras_guitarras-clasicas-de-concierto_ec1',
    'EC-3': 'guitarras_guitarras-clasicas-de-concierto_ec3',
    'Pozuelo clásica caoba': 'guitarras_guitarras-clasicas-de-concierto_pozuelo-clasica-caoba',
    'Pozuelo clásica palo santo': 'guitarras_guitarras-clasicas-de-concierto_pozuelo-clasica-palo-santo',
}

# Enlaces a la versión inglesa original, página por página
EN_MODELS = {
    'A26': 'a26', 'A27/N': 'a27-n', 'A28': 'a28',
    'AF25': 'af25', 'AF25/R': 'af25-r',
    'Dedicación Flamenco': 'dedication-flamenco',
    'EF4/5': 'ef4-5', 'EF5/N': 'ef5-n', 'Pharaon': 'pharoah',
    'Pozuelo Flamenco': 'pozuelo-flamenco-sycamore',
    'Pozuelo Flamenco Caoba': 'pozuelo-flamenco-mahogany',
    'Pozuelo Flamenco Palo Santo': 'pozuelo-flamenco-rosewood',
    'AC-23': 'ac23', 'AC-23/R': 'ac23-r',
    'Dedicación clásico': 'dedication-classical',
    'EC-1': 'ec1', 'EC-3': 'ec3',
    'Pozuelo clásica caoba': 'pozuelo-classical-mahogany',
    'Pozuelo clásica palo santo': 'pozuelo-classical-rosewood',
}

EN_PAGES = {
    'index.html': 'https://marianoconde.com/en/',
    'guitarras.html': 'https://marianoconde.com/en/guitars/',
    'flamencas.html': 'https://marianoconde.com/en/guitars/flamenco-guitars/',
    'clasicas.html': 'https://marianoconde.com/en/guitars/classical-concert-guitars/',
    'poema.html': 'https://marianoconde.com/en/poem-guitars/',
    'galeria.html': 'https://marianoconde.com/en/gallery/',
    'noticias.html': 'https://marianoconde.com/en/news/',
    'historia.html': 'https://marianoconde.com/en/history/',
    'contacto.html': 'https://marianoconde.com/en/contact/',
    'directo.html': 'https://marianoconde.com/en/live-workshop/',
}

HEROES = {
    'index.html': 'Carrousel01_01.webp',
    'guitarras.html': 'Guitarras-flamencas-Mariano-Conde.webp',
    'flamencas.html': 'PozueloFlamenco.webp',
    'clasicas.html': 'EC1.webp',
    'directo.html': 'MC_Historia_4.webp',
    'poema.html': 'PozueloPaloSanto_1.webp',
    'galeria.html': 'MCenPared_1.webp',
    'noticias.html': '_ESTRENO-MUNDIAL-Mariano-Conde-Los-guitarreros-que-enamoraron-al-maestro-Paco-de-Lucia.webp',
    'historia.html': 'MC_Historia_9.webp',
    'contacto.html': 'Carrousel02_01.webp',
}

SECTION_TITLES = {
    'index.html': ('Desde 1915', 'la guitarra española la firma <em>Conde.</em>'),
    'guitarras.html': ('Cada guitarra,', 'una voz <em>propia.</em>'),
    'flamencas.html': ('El compás', 'de la guitarra <em>flamenca.</em>'),
    'clasicas.html': ('La voz', 'de la guitarra <em>clásica.</em>'),
    'directo.html': ('El taller,', 'sin puertas <em>cerradas.</em>'),
    'poema.html': ('Cuando la guitarra', 'se vuelve <em>poesía.</em>'),
    'galeria.html': ('MC en pared.', 'MC a <em>escena.</em>'),
    'noticias.html': ('Lo que se dice', 'alrededor de una <em>guitarra.</em>'),
    'historia.html': ('Entre guitarras', 'se nos fueron los <em>dientes.</em>'),
    'contacto.html': ('Ven al taller.', 'Hablemos de <em>tu guitarra.</em>'),
}

# ---------------------------------------------------------------- utils
def sanitize(name):
    return re.sub(r'[^\w.\-áéíóúñÁÉÍÓÚÑ]', '_', name)

def img_exists(name):
    return (IMGPATH / name).exists()

def h(text):
    return htmlmod.escape(str(text), quote=True)

def slugify(text):
    text = unicodedata.normalize('NFKD', str(text))
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def model_data(name):
    return MODEL_DATA.get(MODEL_SOURCE.get(name), {})

def en_model_url(name):
    slug = EN_MODELS.get(name, '')
    if not slug:
        return EN_PAGES['guitarras.html']
    base = ('https://marianoconde.com/en/guitars/flamenco-guitars/'
            if name in FLAMENCAS else
            'https://marianoconde.com/en/guitars/classical-concert-guitars/')
    return base + slug + '/'

# ---------------------------------------------------------------- plantilla
def header(active, filename):
    links = []
    for href, label in NAV:
        cls = ' class="is-current"' if href == active else ''
        extra = ' nav-live' if href == 'directo.html' else ''
        if extra:
            label = '<span class="live-dot"></span> ' + label
        link_class = ' '.join(x for x in (cls.strip().replace('class="', '').replace('"', ''), extra.strip()) if x)
        class_attr = f' class="{link_class}"' if link_class else ''
        links.append(f'<a href="{href}"{class_attr}>{label}</a>')
    # La versión inglesa es interna: el selector cambia de idioma sin salir del sitio.
    en_link = 'en/' + filename
    lang_switch = f'''      <div class="lang-switch">
        <button class="lang-current" id="langToggle" type="button" aria-expanded="false" aria-controls="langMenu">Español <span aria-hidden="true">▾</span></button>
        <div class="lang-menu" id="langMenu" hidden>
          <span class="is-current">Español</span>
          <a href="{en_link}">Inglés</a>
        </div>
      </div>'''
    en_mobile = f'    <a href="{en_link}">English version</a>\n'
    return f'''<div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
<a class="skip-link" href="#main">Saltar al contenido principal</a>
<header class="site-header" id="siteHeader">
  <div class="header-inner">
    <a class="brand" href="index.html" aria-label="Mariano Conde — inicio">
      <img src="assets/img/Mariano-Conde-Logo.svg" alt="Mariano Conde" class="brand-logo">
      <span class="brand-meta">Madrid · desde 1915</span>
    </a>
    <nav class="nav-desktop" aria-label="Navegación principal">{''.join(links)}</nav>
    <div class="header-actions">
{lang_switch}
      <a class="btn btn-sm btn-outline" href="contacto.html">Encargos</a>
      <button class="menu-toggle" id="menuToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="navMobile"><span></span><span></span></button>
    </div>
  </div>
  <nav class="nav-mobile" id="navMobile" aria-label="Navegación móvil">
{''.join(f'    <a href="{a}">{l}</a>' for a, l in NAV)}
{en_mobile}  </nav>
</header>'''

def footer(active=None):
    tabs = [('index.html', 'Inicio', '⌂'), ('guitarras.html', 'Guitarras', '♪'),
            ('poema.html', 'Poema', '✦'), ('directo.html', 'Directo', '◉'),
            ('contacto.html', 'Contacto', '✉')]
    tab_links = []
    for href, label, icon in tabs:
        cur = ' class="is-current" aria-current="page"' if href == active else ''
        tab_links.append(f'<a href="{href}"{cur}><span class="tab-icon" aria-hidden="true">{icon}</span>{label}</a>')
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/img/MC-Logo.svg" alt="MC — Mariano Conde" class="footer-logo">
        <p>La guitarra española la firma Conde.<br>Madrid, desde 1915.</p>
      </div>
      <div class="footer-nav">
        <div><h4>Explora</h4><a href="guitarras.html">Guitarras</a><a href="flamencas.html">Flamencas</a><a href="clasicas.html">Clásicas</a><a href="poema.html">Del Poema</a></div>
        <div><h4>Descubre</h4><a href="directo.html">Taller en directo</a><a href="historia.html">Historia</a><a href="noticias.html">Noticias</a><a href="galeria.html">Galería</a><a href="contacto.html">Contacto</a></div>
        <div><h4>En directo</h4><a href="https://www.youtube.com/@Guitarras_MarianoConde/live" target="_blank" rel="noopener">YouTube ↗</a><a href="https://www.twitch.tv/guitarrasmarianoconde" target="_blank" rel="noopener">Twitch ↗</a><a href="https://www.instagram.com/guitarras_marianoconde/" target="_blank" rel="noopener">Instagram ↗</a><a href="https://www.facebook.com/GuitarrasMarianoConde/" target="_blank" rel="noopener">Facebook ↗</a><a href="https://www.tiktok.com/@guitarras_marianoconde" target="_blank" rel="noopener">TikTok ↗</a></div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span id="year"></span> Guitarras Mariano Conde · C. de la Amnistía, 1 · 28013 Madrid</p>
      <div><a href="aviso-legal.html">Aviso legal</a><a href="privacidad.html">Privacidad</a><a href="cookies.html">Cookies</a><a href="feed.xml" type="application/rss+xml">RSS</a><button class="footer-cookie-btn" id="cookieSettings" type="button">Gestionar cookies</button></div>
      <div class="view-switch"><button type="button" data-view="mobile">Ver versión móvil</button><button type="button" data-view="desktop">Ver versión escritorio</button></div>
    </div>
  </div>
</footer>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Imagen ampliada" hidden>
  <button class="lightbox-close" id="lightboxClose" aria-label="Cerrar">×</button>
  <button class="lightbox-nav lightbox-prev" id="lightboxPrev" aria-label="Imagen anterior">‹</button>
  <img id="lightboxImg" src="" alt="">
  <button class="lightbox-nav lightbox-next" id="lightboxNext" aria-label="Imagen siguiente">›</button>
</div>
<div class="cookie-banner" id="cookieBanner" role="dialog" aria-modal="false" aria-labelledby="cookieTitle" hidden>
  <div class="cookie-inner">
    <div><h3 id="cookieTitle">Gestionar el consentimiento de las cookies</h3>
    <p>Usamos cookies funcionales, de preferencias y estadísticas para ofrecerte la mejor experiencia. Puedes aceptarlas, rechazarlas o elegir tus preferencias. <a href="cookies.html">Leer más ↗</a></p></div>
    <div class="cookie-actions"><button class="btn btn-ghost-light btn-sm" id="cookieDeny" type="button">Denegar</button><button class="btn btn-ghost-light btn-sm" id="cookiePrefs" type="button">Ver preferencias</button><button class="btn btn-gold btn-sm" id="cookieAccept" type="button">Aceptar</button></div>
  </div>
  <div class="cookie-prefs" id="cookiePrefsPanel" hidden>
    <label><input type="checkbox" checked disabled> Funcionales <span>siempre activo</span></label>
    <label><input type="checkbox" id="cookiePrefsPrefs"> Preferencias</label>
    <label><input type="checkbox" id="cookiePrefsStats"> Estadísticas</label>
    <label><input type="checkbox" id="cookiePrefsMarketing"> Marketing</label>
    <button class="btn btn-outline btn-sm" id="cookieSave" type="button">Guardar preferencias</button>
  </div>
</div>
<nav class="mobile-tabbar" aria-label="Navegación rápida móvil">
  {''.join(tab_links)}
</nav>
<script src="app.js"></script>'''

def subnav(items, current):
    links = ''.join(f'<a href="{a}"{" class=\'is-current\'" if a == current else ""}>{l}</a>' for a, l in items)
    return f'<nav class="subnav" aria-label="Subsección"><div class="container">{links}</div></nav>'

def hero(active, kicker, lead, index):
    t1, t2 = SECTION_TITLES[active]
    return f'''<section class="page-hero" style="--hero-img:url('assets/img/{HEROES[active]}')">
  <div class="container">
    <p class="crumb"><a href="index.html">Inicio</a> &nbsp;/&nbsp; {kicker}</p>
    <h1>{t1}<br>{t2}</h1>
    <p class="lead">{lead}</p>
  </div>
  <div class="hero-index">{index}</div>
</section>'''

def next_section(label, href, title):
    return f'''<div class="container"><div class="next-section reveal">
  <span>Siguiente sección · {label}</span>
  <a href="{href}">{title} <em>↗</em></a>
</div></div>'''

# Detección de dispositivo: cada versión se autodirige a la contraria sólo
# cuando el dispositivo y la preferencia manual lo indican (sin bucles).
_DETECT_JS = r'''(function(){
  try{
    if(localStorage.getItem('mc-view')==='__PREFERRED__') return;
    var ua=navigator.userAgent||'';
    var mobile=(navigator.userAgentData&&navigator.userAgentData.mobile===true)||
      /Android|iPhone|iPod|Windows Phone|Mobile|Silk|BlackBerry|Opera Mini/i.test(ua)||
      (/iPad|Macintosh/.test(ua)&&navigator.maxTouchPoints>1);
    if(mobile!==__ISMOBILE__) return;
    var p=location.pathname.split('/').pop()||'index.html';
    if(!/\.html$/.test(p)) p='index.html';
    location.replace('__TARGET__'+p);
  }catch(e){}
})();'''
DESKTOP_BOOT = '<script>' + (_DETECT_JS.replace('__PREFERRED__', 'desktop')
                             .replace('__ISMOBILE__', 'true')
                             .replace('__TARGET__', 'm/')) + '</script>'
MOBILE_BOOT = '<script>' + (_DETECT_JS.replace('__PREFERRED__', 'mobile')
                            .replace('__ISMOBILE__', 'false')
                            .replace('__TARGET__', '../')) + '</script>'

def relocate_doc(doc, prefix):
    """Reescribe las rutas locales para una carpeta más profunda."""
    d = doc.replace('href="assets/', f'href="{prefix}assets/')
    d = d.replace('src="assets/', f'src="{prefix}assets/')
    d = d.replace('data-full="assets/', f'data-full="{prefix}assets/')
    d = d.replace("url('assets/", f"url('{prefix}assets/")
    d = d.replace('href="styles.css"', f'href="{prefix}styles.css"')
    d = d.replace('src="app.js"', f'src="{prefix}app.js"')
    d = d.replace('href="feed.xml"', f'href="{prefix}feed.xml"')
    return d

def mobile_base(doc):
    """Cambia sólo el dispositivo y el detector, sin tocar rutas."""
    d = doc.replace('data-device="desktop"', 'data-device="mobile"', 1)
    return d.replace(DESKTOP_BOOT, MOBILE_BOOT, 1)


def prefix_links(doc, prefix):
    """Prefija los enlaces internos y el selector de idioma."""
    d = _I18N_LINK.sub(lambda m: f'href="{prefix}{m.group(1)}"', doc)
    return d.replace('href="en/', f'href="{prefix}en/')


def mobile_doc(doc, prefix='../'):
    """Adapta una página escritorio a la versión servida desde m/."""
    return prefix_links(relocate_doc(mobile_base(doc), prefix), prefix)

# ---------------------------------------------------------------- inglés
def norm(text):
    """Normalización compartida con _translate_site.py."""
    return ' '.join(htmlmod.unescape(text).split())


_I18N_ATTRS = re.compile(r'\b(alt|title|aria-label|placeholder|content)="([^"]*)"')
_I18N_LINK = re.compile(r'href="((?!(?:https?:|mailto:|tel:|#|//|en/))[^"]*?\.html(?:\?[^"]*)?)"')
_TAG_RE = re.compile(r'(<[^>]+>)')


def translate_document(doc):
    """Sustituye textos y atributos por su traducción sin tocar etiquetas ni scripts."""
    out, in_raw = [], False
    for piece in _TAG_RE.split(doc):
        if not piece:
            continue
        if piece.startswith('<'):
            if re.match(r'<(script|style)\b', piece, re.I):
                in_raw = True
            elif re.match(r'</(script|style)\b', piece, re.I):
                in_raw = False

            def replace_attr(match):
                value = TRANSLATIONS.get(norm(match.group(2)))
                if value is None:
                    return match.group(0)
                return f'{match.group(1)}="{htmlmod.escape(value, quote=True)}"'

            out.append(_I18N_ATTRS.sub(replace_attr, piece))
            continue
        if in_raw:
            out.append(piece)
            continue
        key = norm(piece)
        if not key or key not in TRANSLATIONS:
            out.append(piece)
            continue
        out.append(htmlmod.escape(TRANSLATIONS[key], quote=False))
    return ''.join(out)


def english_doc(doc, filename, prefix):
    """Versión inglesa de una página ya generada en español."""
    d = translate_document(doc)
    d = d.replace('<html lang="es"', '<html lang="en"', 1)
    # El selector vuelve al español de la misma página, sin salir del sitio.
    d = d.replace('>Spanish<span', '>English <span', 1)
    d = d.replace('>Spanish <span', '>English <span', 1)
    d = d.replace('<span class="is-current">Spanish</span>',
                  '<span class="is-current">English</span>', 1)
    # Enlaces internos a páginas: se prefijan con ../ (en/) o ../../ (en/m/).
    d = _I18N_LINK.sub(lambda m: f'href="{prefix}{m.group(1)}"', d)
    # El enlace al español se reescribe después para no prefijarlo dos veces.
    d = d.replace(f'href="en/{filename}">English</a>',
                  f'href="{prefix}{filename}">Español</a>', 1)
    d = d.replace('href="en/', f'href="{prefix}')
    return relocate_doc(d, prefix)


def page(filename, title, description, active, body, en_url=None):
    doc = f'''<!doctype html>
<html lang="es" data-device="desktop">
<head>
{DESKTOP_BOOT}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{h(title)} · Mariano Conde</title>
  <meta name="description" content="{h(description)}">
  <meta name="theme-color" content="#0d0c0b">
  <link rel="icon" type="image/svg+xml" href="assets/img/MC_Favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body data-section="{h(active)}">
{header(active, filename)}
<main id="main">
{body}
</main>
{footer(active)}
</body>
</html>
'''
    (OUT / filename).write_text(doc, encoding='utf-8')
    (OUT_M / filename).write_text(mobile_doc(doc), encoding='utf-8')
    en_doc = english_doc(doc, filename, '../')
    (OUT_EN / filename).write_text(en_doc, encoding='utf-8')
    (OUT_EN_M / filename).write_text(english_doc(mobile_base(doc), filename, '../../'),
                                     encoding='utf-8')

# ---------------------------------------------------------------- bloques reutilizables
def cards(models, cat):
    out = []
    slug = cat
    for name, im, wood, kind, desc in models:
        key = slugify(name)
        href = f'modelo-{key}.html'
        price = model_data(name).get('price', '')
        price_html = f'<span class="model-from">Desde {h(price)} €</span>' if price else ''
        out.append(f'''<a class="model-card reveal" href="{href}">
  <img src="assets/img/{im}" alt="Guitarra {h(name)} Mariano Conde" loading="lazy">
  <span class="arrow" aria-hidden="true">↗</span>
  <div class="model-info"><span class="model-tag">{h(kind)} · {h(wood)}</span><h3>{h(name)}</h3><p>{h(desc)}</p>{price_html}</div>
</a>''')
    return '\n'.join(out)

# ---------------------------------------------------------------- páginas
def build_guitarras():
    body = hero('guitarras.html', 'Guitarras', 'Flamencas de concierto, clásicas de tercera y modelos criados para el poema. Todas con etiqueta numerada escrita a mano, cabeza de media luna e iniciales MC grabadas a fuego en la tapa.', '02 / 08')
    body += subnav([('guitarras.html','Catálogo'),('flamencas.html','Flamencas'),('clasicas.html','Clásicas'),('poema.html','Del Poema')], 'guitarras.html')
    body += f'''<section class="section-cream">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">El catálogo</p><h2 class="display">Dos caminos,<br><em>una misma firma.</em></h2>
    <p class="section-intro">Madera maciza y secado natural de 20 años mínimo en adelante, según el modelo. Cada guitarra se construye a mano en el taller de la calle Amnistía, Madrid.</p></div>
    <div class="split reverse reveal">
      <div><h3>Guitarras flamencas</h3><p>Compás seco, ataque directo y ciprés como seña de identidad. Instrumentos pensados para el cante, el baile y el toque de concierto.</p><a class="btn btn-dark btn-sm" href="flamencas.html">Ver {len(FLAMENCAS)} modelos ↗</a></div>
      <figure><img src="assets/img/Guitarras-flamencas-Mariano-Conde.webp" alt="Guitarras flamencas Mariano Conde" loading="lazy"><figcaption>Flamencas · taller de Madrid</figcaption></figure>
    </div>
    <div class="split reveal" style="margin-top:4rem">
      <figure><img src="assets/img/Guitarras-clasicas-Mariano-Conde.webp" alt="Guitarras clásicas Mariano Conde" loading="lazy"><figcaption>Clásicas de concierto</figcaption></figure>
      <div><h3>Guitarras clásicas de concierto</h3><p>Tercera, timbre redondo y proyección para sala. Abeto, palo santo, caoba y otras maderas seleccionadas una a una.</p><a class="btn btn-dark btn-sm" href="clasicas.html">Ver {len(CLASICAS)} modelos ↗</a></div>
    </div>
    <div class="spec-grid reveal">
      <div class="spec"><span>Etiqueta</span><strong>Numerada a mano</strong></div>
      <div class="spec"><span>Cabeza</span><strong>Media luna</strong></div>
      <div class="spec"><span>Iniciales</span><strong>MC a fuego</strong></div>
    </div>
  </div>
</section>'''
    body += '<section class="section-dark"><div class="container"><div class="section-head reveal"><p class="eyebrow">Selección</p><h2 class="display">Modelos<br><em>destacados.</em></h2></div><div class="model-grid">' + cards(FLAMENCAS[:4] + CLASICAS[:4], 'destacados') + '</div></div></section>'
    body += f'''<section class="section-dark" id="segunda-mano"><div class="container">
  <div class="split reveal">
    <div><p class="eyebrow">Guitarras de segunda mano</p><h2 class="display">Una oportunidad<br><em>con historia.</em></h2>
    <p>Descubre las oportunidades que ofrece nuestro apartado de antiguas guitarras flamencas y clásicas. Instrumentos que han vivido otra vida y que siguen afinados en la misma tradición.</p>
    <a class="btn btn-gold" href="{REVERB_URL}" target="_blank" rel="noopener">Segunda mano ↗</a></div>
    <figure><img src="assets/img/MC_Historia_3.webp" alt="Guitarras antiguas en el taller de Mariano Conde" loading="lazy"><figcaption>Archivo del taller · Madrid</figcaption></figure>
  </div>
</div></section>'''
    body += next_section('Guitarras del Poema', 'poema.html', 'Cuando la guitarra se vuelve poesía')
    page('guitarras.html', 'Catálogo de guitarras', 'Guitarras flamencas y clásicas artesanales de Mariano Conde. Modelos, maderas y acabados del taller de Madrid.', 'guitarras.html', body)

def editorial_html(file):
    items = EDITORIAL.get(file, [])
    if not items:
        return ''
    blocks = '\n'.join(
        f'<div class="editorial-block reveal"><h3>{h(heading)}</h3><p>{h(text)}</p></div>'
        for heading, text in items)
    return f'''<section class="section-cream"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">El oficio</p><h2 class="display">Lo que hay<br><em>detrás.</em></h2></div>
  <div class="editorial-grid">{blocks}</div>
</div></section>'''

def build_category(file, title, kicker, desc, models, idx):
    body = hero(file, kicker, desc, idx)
    body += subnav([('guitarras.html','Catálogo'),('flamencas.html','Flamencas'),('clasicas.html','Clásicas'),('poema.html','Del Poema')], file)
    body += f'''<section class="section-dark"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">{kicker}</p><h2 class="display">{len(models)} modelos,<br><em>una sola mano.</em></h2>
  <p class="section-intro">Construidas artesanalmente, numeradas consecutivamente, con cabeza de media luna e iniciales MC a fuego en la tapa.</p></div>
  <div class="model-grid">{cards(models, kicker)}</div>
</div></section>'''
    body += editorial_html(file)
    body += next_section('Catálogo general', 'guitarras.html', 'Volver a todas las guitarras')
    page(file, title, desc, file, body)

def configurator_html(name, price_text):
    """Reproduce el configurador original: opciones, suplementos y precio total."""
    data = model_data(name)
    groups = data.get('groups', [])
    if not groups:
        return ''
    base = int(price_text.replace('.', '')) if price_text else 0
    fields = []
    for group in groups:
        label = group['label'].replace('Cutway', 'Cutaway')
        opts = []
        for opt in group['options']:
            opts.append(f'<option value="{h(opt["label"])}" data-price="{opt["price"]}">{h(opt["label"])}</option>')
        fields.append(f'<label>{h(label)}<select name="{h(label)}" data-config>{"".join(opts)}</select></label>')
    return f'''<section class="section-cream" id="personalizacion"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Personalización</p><h2 class="display">Hazla <em>tuya.</em></h2>
  <p class="section-intro">Elige maderas, tapa, barnizado y clavijero. El precio total se calcula con los suplementos de cada opción, como en el configurador original del taller.</p></div>
  <form class="config-form reveal" data-mailform data-base="{base}" novalidate>
    <div class="config-grid">{''.join(fields)}</div>
    <div class="config-total"><span>Precio total estimado · IVA incluido</span><strong><span data-config-total>{h(price_text)}</span> €</strong></div>
    <div class="config-contact">
      <label>Nombre <input type="text" name="nombre" required autocomplete="name"></label>
      <label>Teléfono <input type="tel" name="telefono" autocomplete="tel"></label>
      <label>Correo electrónico <input type="email" name="email" required autocomplete="email"></label>
      <label>Asunto <input type="text" name="asunto" value="Encargo de guitarra · {h(name)}" readonly></label>
      <label class="config-wide">Mensaje <textarea name="mensaje" rows="3" placeholder="Cuéntanos qué necesitas saber sobre esta guitarra..."></textarea></label>
      <label class="checkbox config-wide"><input type="checkbox" name="privacidad" required> Acepto la <a href="privacidad.html">política de privacidad</a></label>
    </div>
    <button type="submit" class="btn btn-dark">Solicitar ↗</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>'''

def model_gallery_html(name):
    imgs = [im for im in model_data(name).get('gallery', []) if img_exists(im)]
    if not imgs:
        return ''
    items = '\n'.join(
        f'<button class="gallery-item reveal" data-full="assets/img/{im}" aria-label="Ampliar imagen de {h(name)}"><img src="assets/img/{im}" alt="{h(name)} — vista {i + 1}" loading="lazy"></button>'
        for i, im in enumerate(imgs))
    return f'''<section class="section-dark"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Detalles del instrumento</p><h2 class="display">{h(name)},<br><em>en imágenes.</em></h2>
  <p class="section-intro"><em>Fotos orientativas. No se corresponden con el producto final.</em></p></div>
  <div class="masonry model-gallery">{items}</div>
</div></section>'''

def build_models():
    for models in (FLAMENCAS, CLASICAS):
        for name, im, wood, kind, desc in models:
            key = slugify(name)
            file = f'modelo-{key}.html'
            price = model_data(name).get('price', '')
            price_html = f'<p class="model-price">Desde <strong>{h(price)} €</strong> · IVA incluido</p>' if price else ''
            body = f'''<section class="page-hero" style="--hero-img:url('assets/img/{im}')">
  <div class="container">
    <p class="crumb"><a href="index.html">Inicio</a> / <a href="guitarras.html">Guitarras</a> / {h(name)}</p>
    <h1>{h(name)}</h1>
    <p class="lead">{h(desc)}</p>
  </div>
</section>
<section class="section-dark"><div class="container">
  <a class="back-link" href="guitarras.html">← Volver al catálogo</a>
  <div class="model-detail reveal">
    <div class="model-photo"><img src="assets/img/{im}" alt="Guitarra {h(name)} Mariano Conde" loading="lazy"></div>
    <div>
      <p class="eyebrow">Ficha del modelo</p>
      <h2>{h(name)}</h2>
      {price_html}
      <p class="model-desc">{h(desc)} Todas nuestras guitarras se construyen a mano en el taller de la calle Amnistía, en Madrid, con maderas macizas secadas de forma natural.</p>
      <p class="model-disclaimer">Fotos orientativas. No se corresponden con el producto final.</p>
      <ul class="detail-list">
        <li><span>Categoría</span><strong>{h(kind)}</strong></li>
        <li><span>Maderas</span><strong>{h(wood)}</strong></li>
        <li><span>Cabeza</span><strong>Media luna</strong></li>
        <li><span>Marcado</span><strong>Iniciales MC a fuego</strong></li>
        <li><span>Etiqueta</span><strong>Numerada a mano</strong></li>
        <li><span>Secado</span><strong>Natural · 20 años mínimo</strong></li>
      </ul>
      <p style="margin-top:2rem"><a class="btn btn-gold" href="#personalizacion">Personalizar y consultar ↗</a></p>
    </div>
  </div>
</div></section>'''
            body += configurator_html(name, price)
            body += model_gallery_html(name)
            body += next_section('Consultas y encargos', 'contacto.html', 'Hablemos de tu guitarra')
            page(file, name, f'{name}: guitarra {kind.lower()} de {wood}. Desde {price} € (IVA incluido). Construida a mano por Mariano Conde en Madrid.', 'guitarras.html', body, en_model_url(name))

def build_directo():
    body = hero('directo.html', 'Taller en directo', 'Viaja a nuestro pasado y presente guitarrero de forma presencial o viéndonos en directo en el taller a través de Twitch y YouTube. Lunes a viernes, 09:00–14:00 y 17:00–19:00; sábados, 10:00–14:00.', '03 / 08')
    body += subnav([('directo.html','En directo'),('noticias.html','Documental'),('historia.html','El taller'),('contacto.html','Ven a vernos')], 'directo.html')
    video_strip = '\n'.join(
        f'<button class="video-thumb{ " is-active" if vid == "0KmZT-WlaTs" else "" }" data-video="{h(vid)}" data-title="{h(title)}"><img src="assets/img/{im}" alt="{h(title)}" loading="lazy"><span>▶ {h(label)}</span></button>'
        for title, vid, im, label in VIDEOS)
    video_grid = '\n'.join(
        f'<article class="video-card reveal"><button class="video-card-play" data-video="{h(vid)}" data-title="{h(title)}" aria-label="Reproducir {h(title)}"><img src="assets/img/{im}" alt="{h(title)}" loading="lazy"><span aria-hidden="true">▶</span></button><div><span class="video-label">{h(label)}</span><h3>{h(title)}</h3></div></article>'
        for title, vid, im, label in VIDEOS)
    body += f'''<section class="section-dark"><div class="container">
  <div class="live-player reveal">
    <div class="player-tabs" role="tablist" aria-label="Elegir plataforma de directo">
      <button class="player-tab is-active" role="tab" aria-selected="true" data-platform="youtube"><span class="play-icon">▶</span> YouTube</button>
      <button class="player-tab" role="tab" aria-selected="false" data-platform="twitch"><span class="play-icon">◆</span> Twitch</button>
      <div class="player-status"><span class="live-dot"></span> EN DIRECTO CUANDO ESTAMOS EN EL TALLER</div>
    </div>
    <div class="player-frame-wrap"><iframe id="playerFrame" title="Taller en directo de Mariano Conde" src="https://www.youtube-nocookie.com/embed/0KmZT-WlaTs?rel=0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe></div>
    <div class="player-footer">
      <p id="playerCaption">Ahora: documental «Los guardianes de la tradición». Pulsa en directo para conectarte a la emisión en cuanto comience.</p>
      <div class="player-links">
        <button class="btn btn-gold btn-sm" id="goLiveBtn">Ver emisión en directo</button>
        <a class="text-link" id="openPlatform" href="https://www.youtube.com/@Guitarras_MarianoConde/live" target="_blank" rel="noopener">Abrir en YouTube ↗</a>
      </div>
    </div>
  </div>
  <div class="video-strip reveal" style="margin-top:1.5rem">
 {video_strip}
    <button class="video-thumb" data-video="live" data-title="Taller en directo"><img src="assets/img/MC_Historia_4.webp" alt="Taller de Mariano Conde en directo" loading="lazy"><span>● Taller en directo</span></button>
  </div>
</div></section>
<section class="section-cream"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Videos del taller</p><h2 class="display">Historias<br><em>en movimiento.</em></h2>
  <p class="section-intro">Documentales, entrevistas y actuaciones recogidas en el archivo de Mariano Conde. Pulsa cualquiera para reproducirlo en el reproductor de arriba.</p></div>
  <div class="video-grid">
 {video_grid}
  </div>
</div></section>
<section class="section-dark"><div class="container">
  <div class="split reveal"><figure><img src="assets/img/MC_Historia_4.webp" alt="Mariano Conde trabajando en el taller" loading="lazy"><figcaption>Calle Amnistía, 1 · Madrid</figcaption></figure>
  <div><p class="eyebrow">Presencial o en pantalla</p><h3>Un taller con las puertas abiertas</h3>
  <p>Desde 2018, Mariano y su hijo trabajan juntos sin obreros ajenos a la familia. Puedes seguir el proceso de construcción de una guitarra en directo o visitarnos en el centro de Madrid.</p>
  <p>El canal de YouTube (@Guitarras_MarianoConde) y Twitch (guitarrasmarianoconde) mantienen el directo del taller como una ventana permanente al oficio.</p>
  <a class="btn btn-dark btn-sm" href="contacto.html">Reservar una visita ↗</a></div></div>
</div></section>'''
    body += next_section('Historia de la casa', 'historia.html', 'Una familia, una tradición')
    page('directo.html', 'Taller en directo', 'Sigue el taller de Mariano Conde en directo por YouTube y Twitch, y descubre el documental Los guardianes de la tradición.', 'directo.html', body)

def poema_essay_html():
    paras = [
        'Desde mi infancia he tenido inquietudes literarias. Prosa, y especialmente verso, me han acompañado en todas las etapas de mi vida. Desde aquella niñez en el colegio de las Escuelas Pías de San Antón, donde capitaneé un equipo de compañeros al que instaba a escribir diariamente un corto relato, hasta que en 2009 surgiera «Anhelo», la primera de las Guitarras del Poema.',
        'Lo primero fue descabezado y disuelto tras ser llamado al despacho del rector por las quejas de los padres de mis compañeros, que alegaban no hacer los deberes por tener que escribir los relatos que a la mañana siguiente me presentaban. Lo segundo ya va por el verso número 58 exhibido en la etiqueta de una Guitarra del Poema Mariano Conde, tras un pausado y constante goteo numérico al alza.',
        'A las Guitarras del Poema las sitúo en el vértice superior de un imaginario rombo, según explico en el verso de «Rombo», la guitarra número 56 de la serie. Vértice y crisol de las buenas guitarras donde no hay distinción entre flamencas y clásicas de concierto, donde tienen cabida el pop, el jazz y los ritmos brasileños, entre otras corrientes musicales.',
        'En la construcción de estas guitarras está la clave de todo lo anterior: una artesanía exhaustiva en la que cada guitarra tiene su propia personalidad constructiva, teniendo en cuenta la flexibilidad o rigidez de las maderas que la componen, algunas centenarias. Pruebas, comprobaciones y finísimo trabajo artesano que demoran su construcción durante meses.',
        'La madera habla, y escucharla y lograr entenderla es la meta. No hay maderas mejores ni maderas peores. La madera está ahí, esperando, y cuantos más años espere, mejor. «De Todo», la número 33, está elaborada con once maderas diferentes e inicia la metamorfosis de la media luna en «luna entera».',
        'En cuanto a la temática de los versos puedo decir que es muy variada: hay sentencias flamencas, breves biografías, descripciones, de matiz romántico y escatológicas. Las Guitarras del Poema están en manos de guitarristas profesionales y aficionados, normalmente con una o dos unidades, y coleccionistas con hasta cuatro. Sus poseedores se encuentran en España, Australia, Alemania, Turquía, Holanda, Francia, Nicaragua o Tailandia, entre otros países. Entre los profesionales destacan Amós Lora, Jesús Guerrero, Ed Sheeran, Raimundo Amador, Joni Jiménez y Antonio Sánchez.',
    ]
    blocks = '\n'.join(f'<p class="poema-para reveal">{h(p)}</p>' for p in paras)
    return f'''<section class="section-dark" id="inspiracion"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">¿Cómo las trabajamos?</p><h2 class="display">Lo que nos <em>inspira.</em></h2></div>
  <div class="poema-essay">{blocks}</div>
</div></section>'''

def poema_catalog_html():
    groups = {}
    for e in POEMA_DATA:
        decade = (e['year'][:3] + '0') if e['year'] and len(e['year']) >= 3 else 'Sin fecha'
        groups.setdefault(decade, []).append(e)
    first = sorted(groups)[0]
    sections = []
    for decade in sorted(groups, key=lambda x: (x == 'Sin fecha', x)):
        rows = []
        for e in groups[decade]:
            verse = f'<blockquote>{h(e["verse"])}</blockquote>' if e['verse'] else ''
            mats = f'<p class="poema-materials"><span>Materiales</span> {h(e["materials"])}</p>' if e['materials'] else ''
            year = f'<span class="poema-year">{h(e["year"])}</span>' if e['year'] else ''
            owner = h(e['owner'] + ((' · ' + e['place']) if e['place'] else ''))
            rows.append(f'''<article class="poema-entry reveal">
      <h4>Nº{e['num']} · {h(e['name'])} {year}</h4>
      <p class="poema-owner">{owner}</p>{verse}{mats}
    </article>''')
        sections.append(f'''<details class="poema-decade" {"open" if decade == first else ""}>
      <summary>{h(decade)} <span>{len(groups[decade])} guitarras</span></summary>
      <div class="poema-entries">{''.join(rows)}</div>
    </details>''')
    return f'''<section class="section-cream" id="catalogo"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Catálogo · Nº1 a Nº58</p><h2 class="display">Cincuenta y ocho<br><em>versos afinados.</em></h2>
  <p class="section-intro">Año, título, propietario, verso y materiales de cada una de las Guitarras del Poema construidas hasta hoy.</p></div>
  {''.join(sections)}
</div></section>'''

def poema_request_form(edition, price, anchor):
    return f'''<section class="section-dark" id="{anchor}"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Encargos</p><h2 class="display">Solicita tu<br><em>{h(edition)}.</em></h2>
  <p class="section-intro">{h(price)} · IVA incluido. Cuéntanos qué te gustaría saber y nos pondremos en contacto contigo.</p></div>
  <form class="poema-form reveal" data-mailform novalidate>
    <div class="config-grid">
      <label>Nombre <input type="text" name="nombre" required autocomplete="name"></label>
      <label>Número de teléfono <input type="tel" name="telefono" autocomplete="tel"></label>
      <label>Correo electrónico <input type="email" name="email" required autocomplete="email"></label>
      <label>Asunto <input type="text" name="asunto" value="Solicitud Guitarra del Poema · {h(edition)}" readonly></label>
      <label class="config-wide">Mensaje <textarea name="mensaje" rows="4" placeholder="Cuéntanos sobre tu encargo..."></textarea></label>
      <label class="checkbox config-wide"><input type="checkbox" name="privacidad" required> Acepto la <a href="privacidad.html">política de privacidad</a></label>
    </div>
    <button type="submit" class="btn btn-gold">Encargar ↗</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>'''

def build_poema():
    body = hero('poema.html', 'Guitarras del Poema', 'Una colección concebida para coleccionistas y músicos que buscan algo más que un instrumento: una pieza única, numerada y firmada a mano.', '04 / 08')
    body += subnav([('guitarras.html','Catálogo'),('poema.html','Colección'),('#inspiracion','Inspiración'),('#catalogo','Catálogo Nº1–58'),('#solicita-poema','Encargos')], 'poema.html')
    body += '''<section class="section-cream"><div class="container">
  <div class="split reverse reveal">
    <div><p class="eyebrow">Edición del Poema</p><h3>Una guitarra para coleccionar</h3>
    <p>Serie especial de piezas únicas. Cada una es un prototipo de una línea constructiva nueva con maderas que pueden llegar a ser centenarias. Valoradas en 48.400 € (IVA inc.). Fotos orientativas. No se corresponden con producto final.</p>
    <div class="poema-prices"><div><span class="price">48.400 €</span><span class="price-label">IVA incluido</span></div></div>
    <p><a class="btn btn-dark btn-sm" href="#solicita-poema">Solicita tu Guitarra del poema ↗</a></p></div>
    <figure><img src="assets/img/PozueloPaloSanto_1.webp" alt="Guitarra del Poema" loading="lazy"><figcaption>Edición del Poema</figcaption></figure>
  </div>
  <div class="split reveal" style="margin-top:5rem">
    <figure><img src="assets/img/DedicacionClasicoFlamenco.webp" alt="Guitarra del Poema doble tapa" loading="lazy"><figcaption>Edición Doble Tapa</figcaption></figure>
    <div><p class="eyebrow">Edición Doble Tapa</p><h3>El instrumento extremo de la casa</h3>
    <p>La doble tapa es la expresión más ambiciosa del taller: más proyección, más color y una construcción que exige decisiones críticas en cada capa. Valorada en 121.000 € (IVA inc.).</p>
    <div class="poema-prices"><div><span class="price">121.000 €</span><span class="price-label">IVA incluido</span></div></div>
    <p><a class="btn btn-dark btn-sm" href="#solicita-doble-tapa">Solicita tu Guitarra de Doble Tapa ↗</a></p></div>
  </div>
</div></section>'''
    body += poema_essay_html()
    body += poema_catalog_html()
    body += poema_request_form('Edición del Poema', '48.400 €', 'solicita-poema')
    body += poema_request_form('Doble Tapa', '121.000 €', 'solicita-doble-tapa')
    body += next_section('Galería de imágenes', 'galeria.html', 'MC en pared, MC a escena')
    page('poema.html', 'Guitarras del Poema', 'Ediciones del Poema y Doble Tapa de Mariano Conde (48.400 € y 121.000 €, IVA incluido), con ensayo, catálogo numerado del Nº1 al Nº58 y formularios de encargo.', 'poema.html', body)

def build_historia():
    items = [
        ('1915','Domingo Esteso abre el taller','El abuelo funda en Madrid la dinastía de guitarreros que dará origen a Conde Hermanos.'),
        ('1976','Mariano Conde, primera guitarra completa','Tras años de observar y preguntar a su padre Mariano y a su tío Faustino, construye su primer instrumento entero.'),
        ('1980','Calle Felipe V','El taller se traslada a un nuevo espacio en el corazón de Madrid.'),
        ('1983','Mariano toma las riendas','Se hace cargo del negocio familiar junto a Faustino, manteniendo el método de construcción tradicional.'),
        ('1986','Conde Hermanos C.B.','Se constituye la sociedad que llevará las guitarras de la casa a los grandes escenarios del mundo.'),
        ('2009 / 2010','Una nueva etapa','Tras la disolución de la sociedad, Mariano Conde continúa su propio camino con la marca que lleva su nombre.'),
        ('Hoy','Padre e hijo, sin obreros','Desde 2018 trabajan juntos, sin personal ajeno a la familia. Las iniciales MC y la auténtica media luna siguen siendo su seña de identidad.'),
    ]
    lis = '\n'.join(f'<li class="reveal"><span class="year">{h(y)}</span><div><h3>{h(t)}</h3><p>{h(d)}</p></div></li>' for y,t,d in items)
    body = hero('historia.html', 'Historia', 'Haberte criado enfrente de la calle Gravina, 7 de Madrid da el privilegio de poder decir que «entre guitarras me salieron los dientes».', '06 / 08')
    body += subnav([('historia.html','Cronología'),('directo.html','El taller hoy'),('noticias.html','Noticias'),('guitarras.html','Guitarras')], 'historia.html')
    body += f'''<section class="section-dark"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Una familia, una tradición</p><h2 class="display">Más de un siglo<br><em>de oficio.</em></h2></div>
  <ol class="timeline">{lis}</ol>
  <div class="history-quote reveal"><blockquote>«Cada guitarra es una conversación entre el árbol, las manos y quien la va a tocar.»</blockquote><cite>— Taller Mariano Conde, Madrid</cite></div>
</div></section>
<section class="section-dark"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Relato de Mariano Conde</p><h2 class="display">«Entre guitarras<br><em>me salieron los dientes.»</em></h2></div>
  <div class="poema-essay">
    <p class="poema-para reveal">Trabajos manuales escolares, observación y preguntas dirigidas a mi padre Mariano y a mi tío Faustino acerca de cómo, por qué y para qué de las diferentes herramientas. Observación y preguntas. Muchas preguntas. Curiosidad por saber cómo se construye una guitarra desde que la materia prima, el árbol, cae al suelo en un más que apasionante «latín» guitarrero.</p>
    <p class="poema-para reveal">Poco a poco fui conociendo maderas, el manejo de limas, formones, cepillos y garlopas, el corte y secado de la madera, las plantillas y marcadores, reglas y medidas, las diferentes formas de montaje y una exhaustiva familiarización con pegamentos, herramientas y materiales. Todo ello dio como resultado que la primera guitarra construida íntegramente por mí viera la luz allá por 1976.</p>
    <p class="poema-para reveal">El 23 de diciembre de 1980 recogí en el Ayuntamiento de Madrid la licencia de apertura del nuevo taller familiar sito en la calle de Felipe V, y abrí sus puertas. Como solicitante figuraba mi tío Faustino. En esos primeros años las guitarras que construí con mi padre llevaban la etiqueta de Gravina número 7, ya que Gravina continuaba siendo la casa matriz; en 1984 unas pocas llevaban ya la etiqueta de Felipe V, 2.</p>
    <p class="poema-para reveal">En 1983, a la jubilación de mi padre, fue decisión suya y de mi tío Faustino que yo, aun siendo el más joven, me hiciera cargo del negocio: se rompía así con el mayorazgo. En 1986 tomé la decisión de crear la comunidad de bienes Conde Hermanos, materializada el 30 de diciembre, en la que incorporé a mi hermano de forma voluntaria. De 1986 a 1989 construí doce guitarras con mi firma autógrafa, las iniciales M y F de Mariano Félix, como acto reivindicativo de autoría.</p>
    <p class="poema-para reveal">Conde Hermanos, C.B. se mantuvo operativa hasta el acuerdo de disolución en 2009 y con carácter definitivo el 30 de abril de 2010. Tras la disolución me instalé con mi hijo Mariano y los empleados de la extinta empresa en el local de la calle Amnistía, 1 de Madrid. Desde la primera, las etiquetas de todas las guitarras Mariano Conde están hechas y escritas a mano: indican nombre, calle, modelo, número de serie y año de terminación.</p>
    <p class="poema-para reveal">Aquí se desarrollaron las Guitarras del Poema y se comenzó a marcar los instrumentos con las iniciales «MC», primero a rotulador y después a fuego, para que no hubiera lugar a error sobre la autoría: la cabeza de media luna la utilizaba mi familia y era preciso identificar su origen. Estas ideas y sus razonamientos están registrados con el nombre de «Iniciales» en el Registro de la Propiedad Intelectual de Madrid.</p>
    <p class="poema-para reveal">Desde 2018, Mariano Conde padre e hijo trabajan sus guitarras sin ayuda de ningún oficial ni operario, propio o externo. Nuestras raíces se anclan en la más antigua escuela guitarrera madrileña: somos guitarras de auténtica media luna y antigua tradición Esteso–Conde.</p>
  </div>
</div></section>
<section class="section-cream"><div class="container">
  <div class="split reveal"><figure><img src="assets/img/MC_Historia_9.webp" alt="Historia familiar de los Conde" loading="lazy"><figcaption>Archivo de la familia Conde</figcaption></figure>
  <div><p class="eyebrow">La auténtica media luna</p><h3>Una forma que no se ha movido en un siglo</h3>
  <p>La cabeza de media luna, las iniciales MC grabadas a fuego y la etiqueta numerada a mano son la firma de una casa que ha preferido crecer despacio antes que perder su identidad.</p>
  <p>La guitarra de Mariano Conde ha acompañado a Paco de Lucía, Paco Cepero, Rafael Riqueni, Raimundo Amador, Leonard Cohen, Bob Dylan, Lenny Kravitz y Ed Sheeran, entre otros.</p></div></div>
</div></section>'''
    body += next_section('Noticias y actualidad', 'noticias.html', 'Lo que se dice alrededor de una guitarra')
    page('historia.html', 'Historia', 'La historia de Mariano Conde: de Domingo Esteso en 1915 al taller actual de la calle Amnistía en Madrid.', 'historia.html', body)

# ---------------------------------------------------------------- noticias
CAT_LABELS = {'maderas': 'Maderas', 'sonido': 'Sonido', 'oficio': 'Oficio'}

def build_news_articles():
    """Una página propia por noticia, en escritorio y móvil, con el contenido original."""
    total = len(NOTICIAS_DATA)
    for i, item in enumerate(NOTICIAS_DATA):
        older = NOTICIAS_DATA[i + 1] if i + 1 < total else None
        newer = NOTICIAS_DATA[i - 1] if i > 0 else None
        older_html = (f'<a class="article-nav-link" href="{older["file"]}">'
                      f'<span>← Anterior</span><strong>{h(older["title"])}</strong></a>'
                      if older else '<span></span>')
        newer_html = (f'<a class="article-nav-link is-next" href="{newer["file"]}">'
                      f'<span>Siguiente →</span><strong>{h(newer["title"])}</strong></a>'
                      if newer else '<span></span>')
        source_html = ''
        if item['external']:
            source_html = (f'<p class="article-source">Publicado originalmente por '
                           f'<a href="{h(item["source_url"])}" target="_blank" rel="noopener">'
                           f'{h(item["source"])} ↗</a></p>')
        body = f'''<section class="article-hero">
  <div class="article-hero-media"><img src="{h(item['image'])}" alt="{h(item['title'])}"></div>
  <div class="container article-hero-inner">
    <nav class="breadcrumb" aria-label="Migas de pan"><a href="index.html">Inicio</a><span>/</span><a href="noticias.html">Noticias</a><span>/</span><span>{h(CAT_LABELS[item['category']])}</span></nav>
    <p class="eyebrow">{h(item['date_label'])} · {h(CAT_LABELS[item['category']])}</p>
    <h1 class="display">{h(item['title'])}</h1>
    <p class="article-lead">{h(item['description'])}</p>
    <p class="article-by">{h(item['source'])}</p>
  </div>
</section>
<section class="section-cream"><div class="container article-layout">
  <article class="article-prose reveal">
{item['body']}
{source_html}
  </article>
  <aside class="article-aside">
    <div class="article-aside-box">
      <p class="eyebrow">Mariano Conde</p>
      <p>Guitarras artesanales desde 1915 en Madrid.</p>
      <a class="btn btn-sm btn-outline" href="noticias.html">Volver a noticias</a>
    </div>
  </aside>
</div></section>
<nav class="article-nav" aria-label="Más noticias"><div class="container article-nav-inner">
  {older_html}
  {newer_html}
</div></nav>'''
        page(item['file'], item['title'], item['description'], 'noticias.html', body, en_url='')

def build_noticias():
    featured = [e for e in NOTICIAS_DATA if e['featured']]
    cards_html = '\n'.join(f'''<article class="news-card reveal">
  <a href="{h(e['file'])}">
    <div class="news-img"><img src="{h(e['image'])}" alt="{h(e['title'])}" loading="lazy"></div>
    <div class="news-body"><div class="news-meta"><span>{h(e['date_label'])} · {h(CAT_LABELS[e['category']])}</span></div><h3>{h(e['title'])}</h3>
    <span class="news-source">{h(e['source'])} →</span></div>
  </a></article>''' for e in featured)
    real_rows = '\n'.join(f'''<a class="article-row" data-cat="{h(e['category'])}" href="{h(e['file'])}">
  <time>{h(e['date_label'])}</time><h3>{h(e['title'])}</h3><span class="source">{h(e['source'])}</span><span class="go">↗</span>
</a>''' for e in NOTICIAS_DATA)
    total = len(NOTICIAS_DATA)
    body = hero('noticias.html', 'Noticias', 'Estrenos, premios, artículos de prensa y todas las historias que explican por qué una guitarra de Mariano Conde es diferente.', '05 / 08')
    body += subnav([('noticias.html','Destacadas'),('directo.html','Documental'),('historia.html','Historia'),('contacto.html','Prensa')], 'noticias.html')
    body += f'''<section class="section-cream"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Destacadas</p><h2 class="display">La actualidad<br><em>de la casa.</em></h2></div>
  <div class="news-grid">{cards_html}</div>
</div></section>
<section class="section-dark"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Archivo · {total} artículos</p><h2 class="display">Historias sobre<br><em>el oficio.</em></h2>
  <p class="section-intro">Maderas, barnices, varetaje, sustain, mantenimiento y todo lo que hay detrás de una guitarra artesanal, publicado por el taller.</p></div>
  <div class="filter-bar reveal" role="group" aria-label="Filtrar artículos">
    <button class="filter-btn is-active" data-news-filter="all" aria-pressed="true">Todos <span>{total}</span></button>
    <button class="filter-btn" data-news-filter="maderas" aria-pressed="false">Maderas</button>
    <button class="filter-btn" data-news-filter="oficio" aria-pressed="false">Oficio</button>
    <button class="filter-btn" data-news-filter="sonido" aria-pressed="false">Sonido</button>
  </div>
  <div class="article-list" id="newsGrid">
{real_rows}
  </div>
</div></section>'''
    press_rows = '\n'.join(
        f'''<article class="press-event reveal"><span class="press-date">{h(date)}</span><div><h3>{h(name)}</h3><p>{h(desc)}</p></div></article>'''
        for date, name, desc in PRESS_EVENTS)
    body += f'''<section class="section-cream"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Prensa y reconocimientos</p><h2 class="display">Fuera del<br><em>taller.</em></h2>
  <p class="section-intro">Conciertos, premios y reconocimientos a una forma de entender la guitarra española.</p></div>
  <div class="press-list">{press_rows}</div>
</div></section>'''
    body += next_section('Historia', 'historia.html', 'Una familia, una tradición')
    page('noticias.html', 'Noticias', 'Noticias, premios, documentales y artículos sobre Mariano Conde y la construcción artesanal de guitarras en Madrid.', 'noticias.html', body, en_url='')

PARED_IMAGES = ['MCenPared_1.webp','MCenPared_2.webp','MCenPared_3.webp','Galeria_1.webp',
                'MC_Historia_4.webp','Mariano-Conde-Joss.fernandez__-6.webp','MC_Historia_3.webp',
                'MarianoCondeGuitarras_102.webp']
ESCENA_IMAGES = [
    'MC_Escenario_2.webp','MC_Escenario_3.webp','MC_Escenario_4.webp','MC_Escenario_5.webp',
    'MC_Escenario_6.webp','MC_Escenario_7.webp','MC_Escenario_8.webp','MC_Escenario_9.webp',
    'MC_Escenario_10.webp','MC_Escenario_11.webp','MC_Escenario_12.webp','MC_Escenario_13.webp',
    'MC_Escenario_14.webp','MC_Escenario_15.webp','MC_Escenario_16.webp','MC_Escenario_17.webp',
    'MC_Escenario_18.webp','MC_Escenario_19.webp','MC_Escenario_20.webp','MC_Escenario_21.webp',
    'MC_Escenario_22.webp','MC_Escenario_23.webp','MC_Escenario_24.webp','MC_Escenario_25.webp',
    'MC_Escenario_26.webp','MC_Escenario_27.webp','MC_Escenario_28.webp','MC_Esecnario_29.webp',
    'MC_Esecnario_30.webp','Escena_13.webp','Escena_32.webp','Escena_33.webp','Escena_34.webp',
    'Escena_35.webp',
]

def escena_4k(name):
    """Ruta de la versión 4K de una foto de escena."""
    return f'assets/img/4k/{Path(name).stem}-4k.webp'

def build_galeria():
    pared = [im for im in PARED_IMAGES if img_exists(im)]
    escena = [im for im in ESCENA_IMAGES
              if img_exists(im) and (IMGPATH / '4k' / (Path(im).stem + '-4k.webp')).exists()]
    def items(arr, label):
        return '\n'.join(f'<button class="gallery-item reveal" data-full="assets/img/{im}" aria-label="Ampliar imagen: {label}"><img src="assets/img/{im}" alt="{label} — Mariano Conde" loading="lazy"></button>' for im in arr)
    panel1 = f'<div class="gallery-panel is-active" id="pared"><div class="masonry">{items(pared,"Taller y pared")}</div></div>'
    slides = []
    dots = []
    for i, im in enumerate(escena):
        full = escena_4k(im)
        is_first = i == 0
        slides.append(
            f'<button class="escena-slide gallery-item{" is-active" if is_first else ""}" '
            f'type="button" data-full="{full}" data-index="{i}" '
            f'tabindex="{0 if is_first else -1}" '
            f'aria-label="Ampliar foto {i + 1} de {len(escena)}">'
            f'<img src="{full}" alt="Guitarra en escena — Mariano Conde {i + 1}" '
            f'loading="{"eager" if is_first else "lazy"}" decoding="async"></button>')
        dots.append(
            f'<button class="escena-dot{" is-active" if is_first else ""}" type="button" '
            f'data-slide="{i}" aria-label="Ir a la foto {i + 1}" '
            f'aria-current="{"true" if is_first else "false"}"></button>')
    panel2 = f'''<div class="gallery-panel" id="escena">
  <div class="escena-carousel" data-carousel aria-roledescription="carrusel" aria-label="Guitarra en escena">
    <div class="escena-viewport"><div class="escena-track">{''.join(slides)}</div></div>
    <button class="escena-nav escena-prev" type="button" aria-label="Foto anterior">‹</button>
    <button class="escena-nav escena-next" type="button" aria-label="Foto siguiente">›</button>
    <button class="escena-toggle" type="button" aria-label="Pausar carrusel" aria-pressed="false"><span class="pause-icon" aria-hidden="true"></span></button>
    <div class="escena-caption"><span class="escena-count" aria-live="polite"><strong>1</strong> / {len(escena)}</span><span class="escena-label">Guitarra en escena</span></div>
    <div class="escena-dots" role="group" aria-label="Elegir foto">{''.join(dots)}</div>
  </div>
</div>'''
    body = hero('galeria.html', 'Galería', 'Un recorrido visual por el taller de la calle Amnistía y por los escenarios donde han sonado las guitarras de Mariano Conde.', '07 / 08')
    body += subnav([('galeria.html','Todas'),('directo.html','En vídeo'),('historia.html','Archivo histórico'),('poema.html','Ediciones')], 'galeria.html')
    body += f'''<section class="section-dark"><div class="container">
  <div class="gallery-tabs reveal" role="group" aria-label="Filtrar galería">
    <button class="gallery-tab is-active" data-gallery="pared" aria-pressed="true">MC en pared</button>
    <button class="gallery-tab" data-gallery="escena" aria-pressed="false">MC a escena</button>
  </div>
  {panel1}{panel2}
</div></section>'''
    body += next_section('Contacto', 'contacto.html', 'Ven al taller')
    page('galeria.html', 'Galería', 'Galería de fotos de Mariano Conde: el taller, las herramientas y las guitarras en escena.', 'galeria.html', body)

def build_contacto():
    body = hero('contacto.html', 'Contacto y encargos', 'Calle de la Amnistía, 1 · 28013 Madrid. Consultas, visitas y encargos de guitarra. Lunes a viernes de 09:00 a 14:00 y de 17:00 a 19:00; sábados de 10:00 a 14:00.', '08 / 08')
    body += subnav([('contacto.html','Datos y formulario'),('guitarras.html','Catálogo'),('poema.html','Del Poema'),('directo.html','Directo')], 'contacto.html')
    body += '''<section class="section-cream"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Escríbenos</p><h2 class="display">Estamos<br><em>en Madrid.</em></h2></div>
  <div class="contact-layout">
    <div class="contact-info reveal">
      <div class="contact-block"><h3>Dirección</h3><p>C. de la Amnistía, 1<br>28013 Madrid, España</p><a class="text-link" href="https://www.google.com/maps/search/?api=1&query=C.+de+la+Amnist%C3%ADa+1+28013+Madrid" target="_blank" rel="noopener">Cómo llegar ↗</a></div>
      <div class="contact-block"><h3>Horarios</h3><p>Lunes – viernes<br>09:00 – 14:00 · 17:00 – 19:00<br><br>Sábado<br>10:00 – 14:00</p></div>
      <div class="contact-block"><h3>Teléfono y correo</h3><p><a href="tel:+34915218155">915 218 155</a><br><a href="mailto:Info@marianoconde.com">Info@marianoconde.com</a></p><a class="btn btn-outline btn-sm" href="assets/docs/lista-precios-2026.pdf" target="_blank" rel="noopener">Lista de precios 2026 (PDF) ↗</a></div>
      <div class="contact-social"><a href="https://www.youtube.com/@Guitarras_MarianoConde" target="_blank" rel="noopener">YouTube</a><a href="https://www.twitch.tv/guitarrasmarianoconde" target="_blank" rel="noopener">Twitch</a><a href="https://www.instagram.com/guitarras_marianoconde/" target="_blank" rel="noopener">Instagram</a><a href="https://www.facebook.com/GuitarrasMarianoConde/" target="_blank" rel="noopener">Facebook</a><a href="https://www.tiktok.com/@guitarras_marianoconde" target="_blank" rel="noopener">TikTok</a></div>
    </div>
    <form class="contact-form reveal" id="contactForm" novalidate>
      <div class="form-row"><label>Nombre <input type="text" name="nombre" required autocomplete="name"></label><label>Email <input type="email" name="email" required autocomplete="email"></label></div>
      <label>Número de teléfono <input type="tel" name="telefono" autocomplete="tel"></label>
      <label>Asunto <select name="asunto"><option>Consulta general</option><option>Encargo de guitarra</option><option>Visita al taller</option><option>Guitarras del Poema</option><option>Prensa y medios</option></select></label>
      <label>Mensaje <textarea name="mensaje" rows="5" required placeholder="Cuéntanos qué guitarra buscas, qué estilo tocas o qué necesitas saber..."></textarea></label>
      <label class="checkbox"><input type="checkbox" name="privacidad" required> Acepto la <a href="privacidad.html">política de privacidad</a></label>
      <button type="submit" class="btn btn-dark">Enviar mensaje ↗</button>
      <p class="form-status" id="formStatus" role="status" aria-live="polite"></p>
    </form>
  </div>
  <div class="map-wrap reveal"><iframe title="Mapa: Guitarras Mariano Conde, calle Amnistía 1, Madrid" src="https://www.google.com/maps?q=C.%20de%20la%20Amnist%C3%ADa%201%2C%2028013%20Madrid&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''
    page('contacto.html', 'Contacto y encargos', 'Dirección, horarios, teléfono, email, lista de precios y formulario de contacto de Guitarras Mariano Conde en Madrid.', 'contacto.html', body)

# ---------------------------------------------------------------- HOME
def build_home():
    body = '''<section class="hero" id="inicio" aria-labelledby="hero-title">
  <div class="hero-media"><img src="assets/img/Carrousel01_01.webp" alt="Guitarra artesanal Mariano Conde" fetchpriority="high"></div>
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="hero-content">
    <div class="hero-kicker"><span class="kicker-line"></span><span>Guitarreros de Madrid · desde 1915</span></div>
    <h1 id="hero-title">La guitarra española<br><em>la firma Conde.</em></h1>
    <p class="hero-text">Cinco generaciones construyendo instrumentos que han acompañado a Paco de Lucía, Leonard Cohen, Bob Dylan y Ed Sheeran. Madera maciza, secado natural y una media luna reconocible en cualquier escenario del mundo.</p>
    <div class="hero-actions"><a href="guitarras.html" class="btn btn-gold">Descubrir las guitarras ↗</a><a href="directo.html" class="btn btn-ghost-light"><span class="live-dot"></span> Entrar al taller</a></div>
    <div class="hero-seal"><span class="seal-top">Guitarreros de Madrid</span><span class="seal-mid">MC</span><span class="seal-bottom">desde 1915</span></div>
  </div>
  <a class="scroll-cue" href="#legado" aria-label="Desplazarse"><span>Desliza</span><span class="scroll-line"></span></a>
  <div class="hero-counter" aria-hidden="true">01 / 08</div>
</section>
<section class="legacy section-dark" id="legado"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">01 — El legado</p><h2 class="display">Una familia.<br><em>Una tradición.</em></h2>
  <p class="section-intro">Cada instrumento nace de una decisión tomada a mano, en un taller de la calle Amnistía donde el tiempo se mide en años de secado de la madera.</p></div>
  <div class="stats-grid"><div class="stat reveal"><span class="stat-number">1915</span><span class="stat-label">Año de fundación</span></div><div class="stat reveal"><span class="stat-number">5</span><span class="stat-label">Generaciones de guitarreros</span></div><div class="stat reveal"><span class="stat-number">20+</span><span class="stat-label">Años mínimos de secado natural</span></div><div class="stat reveal"><span class="stat-number">~60</span><span class="stat-label">Guitarras al año, una a una</span></div></div>
  <div class="pillars"><article class="pillar reveal"><span class="pillar-num">01</span><h3>Cabeza de media luna</h3><p>El rasgo más reconocible de la casa Conde, heredado de Domingo Esteso.</p></article><article class="pillar reveal"><span class="pillar-num">02</span><h3>Iniciales a fuego</h3><p>Las letras MC marcan la tapa junto a una etiqueta numerada escrita a mano.</p></article><article class="pillar reveal"><span class="pillar-num">03</span><h3>Madera maciza</h3><p>Cinco o seis maderas por guitarra, secadas entre 10 y 30 años.</p></article></div>
</div></section>
<section class="section-cream"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Explora por secciones</p><h2 class="display">Todo el mundo<br><em>Mariano Conde.</em></h2></div>
  <div class="model-grid">
    <a class="model-card reveal" href="guitarras.html"><img src="assets/img/Guitarras-flamencas-Mariano-Conde.webp" alt="Guitarras" loading="lazy"><div class="model-info"><span class="model-tag">01 · Catálogo</span><h3>Guitarras</h3><p>Flamencas, clásicas y modelos singulares.</p></div></a>
    <a class="model-card reveal" href="directo.html"><img src="assets/img/MC_Historia_4.webp" alt="Taller en directo" loading="lazy"><div class="model-info"><span class="model-tag">02 · En vivo</span><h3>Taller en directo</h3><p>YouTube, Twitch y documental.</p></div></a>
    <a class="model-card reveal" href="poema.html"><img src="assets/img/PozueloPaloSanto_1.webp" alt="Del Poema" loading="lazy"><div class="model-info"><span class="model-tag">03 · Colección</span><h3>Del Poema</h3><p>Ediciones únicas y numeradas.</p></div></a>
    <a class="model-card reveal" href="historia.html"><img src="assets/img/MC_Historia_9.webp" alt="Historia" loading="lazy"><div class="model-info"><span class="model-tag">04 · Legado</span><h3>Historia</h3><p>De 1915 a la actualidad.</p></div></a>
    <a class="model-card reveal" href="noticias.html"><img src="assets/img/_ESTRENO-MUNDIAL-Mariano-Conde-Los-guitarreros-que-enamoraron-al-maestro-Paco-de-Lucia.webp" alt="Noticias" loading="lazy"><div class="model-info"><span class="model-tag">05 · Actualidad</span><h3>Noticias</h3><p>Estrenos, premios y prensa.</p></div></a>
    <a class="model-card reveal" href="galeria.html"><img src="assets/img/MCenPared_1.webp" alt="Galería" loading="lazy"><div class="model-info"><span class="model-tag">06 · Imágenes</span><h3>Galería</h3><p>MC en pared y a escena.</p></div></a>
    <a class="model-card reveal" href="contacto.html"><img src="assets/img/Carrousel02_01.webp" alt="Contacto" loading="lazy"><div class="model-info"><span class="model-tag">07 · Encargos</span><h3>Contacto</h3><p>Visítanos en Madrid.</p></div></a>
  </div>
</div></section>'''
    body += next_section('Catálogo de guitarras', 'guitarras.html', 'Cada guitarra, una voz propia')
    page('index.html', 'Mariano Conde · Guitarras españolas desde 1915', 'Guitarras flamencas y clásicas artesanales de Mariano Conde en Madrid desde 1915. Taller en directo, catálogo y noticias.', 'index.html', body)

# ---------------------------------------------------------------- legales y feed
def legal_blocks(lines):
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        heading = (
            (len(line) <= 95 and line.upper() == line
             and any(c.isalpha() for c in line) and not line.endswith('.'))
            or (bool(re.match(r'^\d+\.\s', line)) and len(line) < 95)
        )
        if heading:
            out.append(f'<h2>{h(line)}</h2>')
            i += 1
        elif line.endswith(':') and i + 1 < len(lines):
            out.append(f'<p><strong>{h(line)}</strong> {h(lines[i + 1].strip())}</p>')
            i += 2
        else:
            out.append(f'<p>{h(line)}</p>')
            i += 1
    return '\n'.join(out)

def build_legal(file, title, source, desc):
    lines = Path(source).read_text(encoding='utf-8').splitlines()
    body = f'''<section class="section-cream"><div class="container">
  <div class="section-head reveal"><p class="eyebrow">Información legal</p><h1 class="display">{h(title)}</h1></div>
  <div class="legal-content">{legal_blocks(lines)}</div>
</div></section>'''
    page(file, title, desc, 'index.html', body)

def build_feed():
    esc = lambda s: htmlmod.escape(str(s), quote=True)
    items = []
    for item in NOTICIAS_DATA:
        url = SITE_URL + item['file']
        items.append(f'''  <item>
    <title>{esc(item['title'])}</title>
    <link>{esc(url)}</link>
    <guid isPermaLink="true">{esc(url)}</guid>
    <pubDate>{esc(item['date'])}</pubDate>
    <description>{esc(item['description'])} — {esc(item['source'])}.</description>
  </item>''')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Mariano Conde · Noticias</title>
  <link>{SITE_URL}noticias.html</link>
  <description>Estrenos, premios y artículos sobre las guitarras de Mariano Conde.</description>
  <language>es</language>
{chr(10).join(items)}
</channel>
</rss>
'''
    (OUT / 'feed.xml').write_text(xml, encoding='utf-8')

    en_items = []
    for item in NOTICIAS_DATA:
        url = SITE_URL + 'en/' + item['file']
        title = TRANSLATIONS.get(item['title'], item['title'])
        desc = TRANSLATIONS.get(item['description'], item['description'])
        source = TRANSLATIONS.get(item['source'], item['source'])
        en_items.append(f'''  <item>
    <title>{esc(title)}</title>
    <link>{esc(url)}</link>
    <guid isPermaLink="true">{esc(url)}</guid>
    <pubDate>{esc(item['date'])}</pubDate>
    <description>{esc(desc)} — {esc(source)}.</description>
  </item>''')
    en_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Mariano Conde · News</title>
  <link>{SITE_URL}en/noticias.html</link>
  <description>Premieres, awards and articles about Mariano Conde guitars.</description>
  <language>en</language>
{chr(10).join(en_items)}
</channel>
</rss>
'''
    (OUT_EN / 'feed.xml').write_text(en_xml, encoding='utf-8')

# ---------------------------------------------------------------- run
if __name__ == '__main__':
    OUT_M.mkdir(exist_ok=True)
    OUT_EN.mkdir(exist_ok=True)
    OUT_EN_M.mkdir(exist_ok=True)
    build_home()
    build_guitarras()
    build_category('flamencas.html', 'Guitarras flamencas', 'Flamencas', 'Más de un siglo dedicados a la construcción de guitarras flamencas en el taller de la calle Amnistía, en pleno Madrid.', FLAMENCAS, '02 / 08')
    build_category('clasicas.html', 'Guitarras clásicas de concierto', 'Clásicas', 'Guitarras clásicas de concierto construidas en Madrid con la misma dedicación y pasión que nos ha caracterizado desde 1915.', CLASICAS, '02 / 08')
    build_models()
    build_directo()
    build_poema()
    build_historia()
    build_noticias()
    build_news_articles()
    build_galeria()
    build_contacto()
    build_legal('aviso-legal.html', 'Aviso legal', '_legal_text.txt',
                'Condiciones de uso y datos identificativos de Guitarras Mariano Conde.')
    build_legal('privacidad.html', 'Política de privacidad', '_política-privacidad_text.txt',
                'Tratamiento de datos personales conforme al RGPD y la LOPDGDD en marianoconde.com.')
    build_legal('cookies.html', 'Política de cookies', '_cookies_text.txt',
                'Uso de cookies técnicas, estadísticas y de marketing en el sitio web de Mariano Conde.')
    build_feed()
    print('Páginas inglesas:', len(list(OUT_EN.glob('*.html'))),
          'escritorio +', len(list(OUT_EN_M.glob('*.html'))), 'móvil')
    print('Páginas generadas:', len(list(OUT.glob('*.html'))),
          'escritorio +', len(list(OUT_M.glob('*.html'))), 'móvil')
