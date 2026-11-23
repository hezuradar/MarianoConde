# Mariano Conde — Rediseño completo (2026)

Rediseño integral del sitio de **Guitarras Mariano Conde**. Sitio estático, autocontenido y sin build step: **una página propia por sección, subcategoría y modelo**, construida a partir de todo el contenido descargado de `marianoconde.com`. Se genera en **dos versiones** (escritorio y móvil en `m/`) y se sirve automáticamente la correspondiente según el dispositivo que accede.

## Cómo verlo

Abre `index.html` directamente en el navegador, o levanta un servidor local:

```powershell
python -m http.server 3000
```

Visita `http://localhost:3000`. Al entrar desde un móvil se carga automáticamente `m/index.html`; desde un escritorio se carga `index.html`. No hay que elegir nada.

## Versión automática por dispositivo

Hay **dos juegos de 32 páginas**: el de escritorio en la raíz y el móvil en `m/`. Un script en el `<head>` de cada página detecta el dispositivo (user agent, `navigator.userAgentData.mobile` y `maxTouchPoints` para iPad) y redirige a la versión contraria sólo si procede:

- Móvil/tablet que abre una página de escritorio → va a `m/<misma-página>`.
- Escritorio que abre una página de `m/` → vuelve a `<misma-página>` en la raíz.
- El nombre de la página se conserva, así que no se pierde la sección.

La detección respeta la preferencia guardada en `localStorage` (`mc-view` = `mobile` o `desktop`), de modo que no hay bucles de redirección. En el pie de todas las páginas hay dos botones, **«Ver versión móvil»** y **«Ver versión escritorio»**, para forzar una u otra; la elección queda memorizada en ese navegador.

La versión móvil añade una **barra de navegación rápida fija abajo** con Inicio, Guitarras, Poema, Directo y Contacto, con el elemento activo marcado y espacio reservado para el «safe area» de iPhone. El menú de hamburguesa es un panel desplazable a pantalla completa, los botones y enlaces tienen un área táctil mínima de 44 px, los campos usan 16 px para evitar el zoom automático de iOS y las galerías, vídeos y tarjetas pasan a una sola columna. En pantallas táctiles se desactivan los efectos `hover` y en horizontal de poca altura se reduce el hero. El banner de cookies se coloca por encima de la barra inferior. Si se abre la versión móvil en un escritorio, se muestra centrada en una columna de 480 px.

## Mapa del sitio (32 páginas por versión, 64 HTML)

| Página | Contenido |
|---|---|
| `index.html` | Hub: hero, legado, cifras y accesos a todas las secciones |
| `guitarras.html` | Catálogo general: flamencas vs. clásicas, segunda mano y modelos destacados |
| `flamencas.html` | 12 modelos flamencos y 6 bloques editoriales del original |
| `clasicas.html` | 7 clásicas de concierto y 6 bloques editoriales del original |
| `modelo-*.html` | 19 fichas de modelo: maderas, precio «Desde», configurador con total, galería y enlace EN |
| `directo.html` | Reproductor YouTube/Twitch, 8 vídeos del archivo, galería de vídeos y taller en directo |
| `poema.html` | Ediciones Poema (48.400 €) y Doble Tapa (121.000 €), ensayo, catálogo Nº1–58 y formularios de encargo |
| `historia.html` | Cronología y relato en primera persona: Gravina 7, Felipe V 2, Conde Hermanos C.B. y Amnistía 1 |
| `noticias.html` | 6 destacadas verificadas + 57 artículos filtrables + sección de prensa y reconocimientos |
| `galeria.html` | 42 fotos en dos pestañas (MC en pared / MC a escena), con lightbox y teclado |
| `contacto.html` | Dirección, horarios, teléfono, email, PDF de precios 2026, formulario con teléfono y mapa |
| `aviso-legal.html`, `privacidad.html`, `cookies.html` | Textos legales del original servidos localmente |
| `feed.xml` | Feed RSS con las 6 noticias destacadas y el archivo de artículos |

## Archivos principales

| Archivo | Contenido |
|---|---|
| `build_site.py` | Generador de las 32 páginas escritorio, las 32 móviles y el feed a partir del material descargado |
| `model-data.json` | Precios, opciones de personalización y galerías de los 19 modelos |
| `poema-data.json` | 58 entradas limpias del catálogo del Poema (año, título, propietario, verso y materiales) |
| `_parse_poema.py` | Parser que reconstruye `poema-data.json` desde `_poema_text.txt` |
| `styles.css` | Sistema visual editorial carbón / crema / oro, responsive y con la versión móvil (barra inferior, áreas táctiles, safe area, sin hover en táctil) |
| `app.js` | Filtros, reproductor, galerías, lightbox, configurador, selector Español/Inglés, menú móvil, conmutador de versión, formularios y cookies |
| `m/` | Versión móvil: las mismas 32 páginas con rutas relativas `../assets/`, `../styles.css` y `../app.js` |
| `assets/img/` | 590 imágenes, logos y fuentes visuales del original |
| `assets/docs/lista-precios-2026.pdf` | Lista de precios 2026 alojada localmente |
| `contenido-original/` | 308 páginas HTML originales y `_assets/` con 162 CSS/JS archivados |
| `image-urls.txt` | Inventario de 233 URLs de imágenes extraídas |

## Regenerar el sitio

Edita siempre `build_site.py` (no los HTML generados) y ejecuta:

```powershell
python build_site.py
```

El generador sobrescribe las páginas HTML de la raíz y de `m/`, y `feed.xml`, pero no toca `styles.css`, `app.js` ni `assets/`.

## Notas

- El selector «Español / Inglés» del header abre la versión inglesa original en pestaña nueva con `rel="noopener"`.
- El reproductor de Twitch puede no cargar si el archivo se abre con `file://`; usa el enlace «Abrir en Twitch» o sirve el sitio por HTTP.
- El directo de YouTube muestra el último vídeo o el aviso de emisión no activa cuando no hay directo en curso.
- Los formularios abren la aplicación de correo del visitante con el mensaje y las opciones elegidas pre-rellenadas (no requieren backend).
- Todas las fuentes externas se abren en pestaña nueva con `rel="noopener"`.
- Validación aplicada: 64/64 páginas (32 + 32) con HTML balanceado, sin IDs duplicados, sin anclas rotas, sin enlaces locales ni recursos ausentes, `feed.xml` well-formed, HTTP 200 en las 15 rutas comprobadas, 8/8 pruebas de redirección y 0 apariciones de texto de investigación no publicado.
- La barra de navegación móvil y el conmutador de versión se generan en `build_site.py` (función `footer()`); la detección automática vive en `DESKTOP_BOOT` / `MOBILE_BOOT`. No editar los HTML generados.
