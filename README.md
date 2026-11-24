# Mariano Conde — Rediseño completo (2026)

Rediseño integral del sitio de **Guitarras Mariano Conde**. Sitio estático, autocontenido y sin build step: **una página propia por sección, subcategoría y modelo**, construida a partir de todo el contenido descargado de `marianoconde.com`. Se genera en **dos versiones** (escritorio y móvil en `m/`) y se sirve automáticamente la correspondiente según el dispositivo que accede.

## Cómo verlo

Abre `index.html` directamente en el navegador, o levanta un servidor local:

```powershell
python -m http.server 3000
```

Visita `http://localhost:3000`. Al entrar desde un móvil se carga automáticamente `m/index.html`; desde un escritorio se carga `index.html`. No hay que elegir nada.

## Versión automática por dispositivo

Hay **dos juegos de 90 páginas**: el de escritorio en la raíz y el móvil en `m/`. Un script en el `<head>` de cada página detecta el dispositivo (user agent, `navigator.userAgentData.mobile` y `maxTouchPoints` para iPad) y redirige a la versión contraria sólo si procede:

- Móvil/tablet que abre una página de escritorio → va a `m/<misma-página>`.
- Escritorio que abre una página de `m/` → vuelve a `<misma-página>` en la raíz.
- El nombre de la página se conserva, así que no se pierde la sección.

La detección respeta la preferencia guardada en `localStorage` (`mc-view` = `mobile` o `desktop`), de modo que no hay bucles de redirección. En el pie de todas las páginas hay dos botones, **«Ver versión móvil»** y **«Ver versión escritorio»**, para forzar una u otra; la elección queda memorizada en ese navegador.

La versión móvil añade una **barra de navegación rápida fija abajo** con Inicio, Guitarras, Poema, Directo y Contacto, con el elemento activo marcado y espacio reservado para el «safe area» de iPhone. El menú de hamburguesa es un panel desplazable a pantalla completa, los botones y enlaces tienen un área táctil mínima de 44 px, los campos usan 16 px para evitar el zoom automático de iOS y las galerías, vídeos y tarjetas pasan a una sola columna. En pantallas táctiles se desactivan los efectos `hover` y en horizontal de poca altura se reduce el hero. El banner de cookies se coloca por encima de la barra inferior. Si se abre la versión móvil en un escritorio, se muestra centrada en una columna de 480 px.

## Mapa del sitio (90 páginas por versión, 180 HTML)

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
| `noticias.html` | 6 destacadas + 58 artículos filtrables con fecha y fuente + sección de prensa y reconocimientos |
| `noticia-*.html` | 58 páginas propias de noticia con el contenido íntegro recuperado del original, vídeos, imágenes, navegación anterior/siguiente y enlace a la fuente cuando procede |
| `galeria.html` | MC en pared (8 fotos con lightbox) y MC a escena (34 fotos 4K en carrusel automático con anterior/siguiente, puntitos, teclado, pausa y lightbox) |
| `contacto.html` | Dirección, horarios, teléfono, email, PDF de precios 2026, formulario con teléfono y mapa |
| `aviso-legal.html`, `privacidad.html`, `cookies.html` | Textos legales del original servidos localmente |
| `feed.xml` | Feed RSS con las 58 noticias; todos los enlaces apuntan a las páginas publicadas en GitHub Pages |

## Archivos principales

| Archivo | Contenido |
|---|---|
| `build_site.py` | Generador de las 90 páginas escritorio, las 90 móviles y el feed a partir del material descargado |
| `model-data.json` | Precios, opciones de personalización y galerías de los 19 modelos |
| `poema-data.json` | 58 entradas limpias del catálogo del Poema (año, título, propietario, verso y materiales) |
| `noticias-data.json` | 58 noticias estructuradas: título, fecha, imagen, categoría, fuente y contenido completo extraído del original |
| `_parse_noticias.py` | Parser que reconstruye `noticias-data.json` desde los artículos descargados y el inventario `_noticias_todas.json` |
| `_make_4k_gallery.py` | Genera las 34 versiones 4K (WebP 3840×2160) de «MC a escena» a partir de las fotos originales |
| `_parse_poema.py` | Parser que reconstruye `poema-data.json` desde `_poema_text.txt` |
| `styles.css` | Sistema visual editorial carbón / crema / oro, responsive, carrusel 4K y versión móvil (barra inferior, áreas táctiles, safe area, sin hover en táctil) |
| `app.js` | Filtros, reproductor, galerías, carrusel 4K, lightbox, configurador, selector Español/Inglés, menú móvil, conmutador de versión, formularios y cookies |
| `m/` | Versión móvil: las mismas 90 páginas con rutas relativas `../assets/`, `../styles.css` y `../app.js` |
| `assets/img/` | 590 imágenes, logos y fuentes visuales del original |
| `assets/img/4k/` | 34 fotos de escena reescaladas a 3840×2160 en WebP para el carrusel |
| `assets/docs/lista-precios-2026.pdf` | Lista de precios 2026 alojada localmente |
| `contenido-original/` | 308 páginas HTML originales y `_assets/` con 162 CSS/JS archivados |
| `image-urls.txt` | Inventario de 233 URLs de imágenes extraídas |

## Regenerar el sitio

Edita siempre `build_site.py` (no los HTML generados) y ejecuta:

```powershell
python _parse_noticias.py
python _make_4k_gallery.py   # solo si cambian las fotos de escena
python build_site.py
```

El parser actualiza `noticias-data.json` con el contenido de los artículos descargados; el generador 4K reescribe `assets/img/4k/`; el generador sobrescribe las páginas HTML de la raíz y de `m/`, y `feed.xml`, pero no toca `styles.css`, `app.js` ni el resto de `assets/`.

## Notas

- Las fotos de «MC a escena» se entregan como WebP de 3840×2160, pero las originales descargadas miden como máximo 1366 px de ancho: el 4K es un reescalado con Lanczos y sharpen suave, no detalle capturado en 4K. Si se consiguen originales mayores, basta con reemplazarlos en `assets/img/` y volver a ejecutar `_make_4k_gallery.py`.
- El carrusel avanza cada 5 segundos y se controla con ‹/›, puntitos, flechas del teclado y el botón de pausa. Se detiene al pasar el ratón, al enfocarlo, al abrir el lightbox, al cambiar de pestaña del navegador, al salir de la pestaña «MC a escena» y cuando el sistema pide reducir movimiento.
- El selector «Español / Inglés» del header abre la versión inglesa original en pestaña nueva con `rel="noopener"`. Las páginas de noticia no muestran ese selector porque su contenido se sirve íntegramente en esta nueva web.
- El reproductor de Twitch puede no cargar si el archivo se abre con `file://`; usa el enlace «Abrir en Twitch» o sirve el sitio por HTTP.
- El directo de YouTube muestra el último vídeo o el aviso de emisión no activa cuando no hay directo en curso.
- Los formularios abren la aplicación de correo del visitante con el mensaje y las opciones elegidas pre-rellenadas (no requieren backend).
- Todas las fuentes externas se abren en pestaña nueva con `rel="noopener"`.
- Validación aplicada: 180/180 páginas (90 + 90) con HTML balanceado, sin enlaces internos rotos ni recursos ausentes (incluidas las 34 rutas 4K en ambas versiones), `feed.xml` con 58 ítems y URLs de GitHub Pages, 0 enlaces al dominio antiguo en noticias/feed, `py_compile` y `node --check` correctos, carrusel comprobado en navegador (avance cada 5 s, anterior/siguiente, puntitos, pausa, lightbox y pestaña «MC a escena») y 0 apariciones de texto de investigación no publicado.
- La barra de navegación móvil y el conmutador de versión se generan en `build_site.py` (función `footer()`); la detección automática vive en `DESKTOP_BOOT` / `MOBILE_BOOT`. No editar los HTML generados.
