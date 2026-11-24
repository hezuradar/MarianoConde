/* ============================================================
   MARIANO CONDE — Interacciones (multi-página)
   ============================================================ */
(function () {
  'use strict';

  const $  = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  const EN = document.documentElement.lang === 'en';
  const DOCUMENTARY = EN ? 'documentary «The guardians of tradition»'
                         : 'documental «Los guardianes de la tradición»';
  const T = {
    openMenu: EN ? 'Open menu' : 'Abrir menú',
    closeMenu: EN ? 'Close menu' : 'Cerrar menú',
    liveIdle: EN
      ? 'Live broadcast from the workshop. When it is not live, YouTube shows the latest broadcast; use the link below to open the channel.'
      : 'Emisión en directo del taller. Si no hay emisión activa, YouTube mostrará el último directo; usa el enlace inferior para abrir el canal.',
    liveOpen: EN ? 'Open live on YouTube ↗' : 'Abrir directo en YouTube ↗',
    now: EN ? 'Now: ' : 'Ahora: ',
    nowDocumentary: EN
      ? 'Ahora: documental «Los guardianes de la tradición». Pulsa en directo para conectarte en cuanto comience.'
      : '',
    watchYouTube: EN ? 'Watch on YouTube ↗' : 'Ver en YouTube ↗',
    twitchIdle: EN
      ? 'Workshop broadcast on Twitch. If it does not load from a local file, use the “Open on Twitch” link.'
      : 'Emisión del taller en Twitch. Si no carga desde un archivo local, usa el enlace «Abrir en Twitch».',
    openTwitch: EN ? 'Open on Twitch ↗' : 'Abrir en Twitch ↗',
    pauseCarousel: EN ? 'Pause carousel' : 'Pausar carrusel',
    resumeCarousel: EN ? 'Resume carousel' : 'Reanudar carrusel',
    formRequired: EN ? 'Please fill in all fields and accept the privacy policy.'
                     : 'Completa todos los campos y acepta la política de privacidad.',
    formEmail: EN ? 'Please enter a valid email address.'
                  : 'Introduce un correo electrónico válido.',
    formReady: EN ? 'Your email app will open with the message ready to send.'
                  : 'Se abrirá tu aplicación de correo con el mensaje listo para enviar.',
    subject: EN ? 'General enquiry' : 'Consulta general',
    name: EN ? 'Name' : 'Nombre',
    phone: EN ? 'Phone' : 'Teléfono',
    email: EN ? 'Email' : 'Email',
    topic: EN ? 'Subject' : 'Asunto',
    configuration: EN ? 'Selected configuration:' : 'Configuración elegida:',
    estimatedTotal: EN ? 'Estimated total price:' : 'Precio total estimado:'
  };
  if (EN) {
    T.nowDocumentary = `Now: ${DOCUMENTARY}. Press Live to connect as soon as it starts.`;
  }

  /* ---------- Año en el footer ---------- */
  const yearEl = $('#year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Conmutador de versión escritorio / móvil ---------- */
  $$('[data-view]').forEach(btn => {
    btn.addEventListener('click', () => {
      const view = btn.dataset.view;
      try { localStorage.setItem('mc-view', view); } catch (e) {}
      const path = location.pathname;
      const inMobile = /(^|\/)m\//.test(path);
      const last = path.split('/').pop() || 'index.html';
      const file = /\.html$/.test(last) ? last : 'index.html';
      const target = view === 'mobile'
        ? (inMobile ? path : 'm/' + file)
        : (inMobile ? '../' + file : path);
      location.href = target;
    });
  });

  /* ---------- Header: scroll + barra de progreso ---------- */
  const header = $('#siteHeader');
  const progress = $('#scrollProgress');
  function onScroll() {
    const y = window.scrollY || document.documentElement.scrollTop;
    if (header) header.classList.toggle('is-scrolled', y > 40);
    if (progress) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menú móvil ---------- */
  const menuToggle = $('#menuToggle');
  const navMobile = $('#navMobile');
  if (menuToggle && navMobile) {
    function closeMenu() {
      navMobile.classList.remove('is-open');
      menuToggle.setAttribute('aria-expanded', 'false');
      menuToggle.setAttribute('aria-label', T.openMenu);
      document.body.style.overflow = '';
    }
    menuToggle.addEventListener('click', () => {
      const open = navMobile.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? T.closeMenu : T.openMenu);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    $$('a', navMobile).forEach(a => a.addEventListener('click', closeMenu));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && navMobile.classList.contains('is-open')) {
        closeMenu();
        menuToggle.focus();
      }
    });
    window.addEventListener('resize', () => { if (window.innerWidth > 900) closeMenu(); });
  }

  /* ---------- Selector de idioma ---------- */
  const langToggle = $('#langToggle');
  const langMenu = $('#langMenu');
  if (langToggle && langMenu) {
    const setLang = open => {
      langMenu.hidden = !open;
      langToggle.setAttribute('aria-expanded', String(open));
    };
    langToggle.addEventListener('click', () => setLang(langMenu.hidden));
    document.addEventListener('click', e => {
      if (!langMenu.hidden && !e.target.closest('.lang-switch')) setLang(false);
    });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') setLang(false); });
  }

  /* ---------- Animaciones de entrada ---------- */
  const revealEls = $$('.reveal');
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach((el, i) => {
      el.style.transitionDelay = (i % 4) * 60 + 'ms';
      revealObserver.observe(el);
    });
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  /* ---------- Filtros genéricos ---------- */
  function setupFilters(buttonSelector, cardSelector, attr) {
    const buttons = $$(buttonSelector);
    const cards = $$(cardSelector);
    if (!buttons.length || !cards.length) return;
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => {
          b.classList.remove('is-active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('is-active');
        btn.setAttribute('aria-pressed', 'true');
        const filter = btn.dataset[attr];
        cards.forEach(card => {
          const show = filter === 'all' || card.dataset.cat === filter;
          card.classList.toggle('is-hidden', !show);
          if (show) card.classList.add('is-visible');
        });
      });
    });
  }
  setupFilters('.filter-btn[data-filter]', '.guitar-card', 'filter');
  setupFilters('.filter-btn[data-news-filter]', '.article-row[data-cat]', 'newsFilter');

  /* ---------- Reproductor ---------- */
  const playerFrame = $('#playerFrame');
  if (playerFrame) {
    const playerCaption = $('#playerCaption');
    const openPlatform = $('#openPlatform');
    const tabs = $$('.player-tab');
    const thumbs = $$('.video-thumb, .video-card-play');
    const goLiveBtn = $('#goLiveBtn');
    const YT_VIDEO = id => `https://www.youtube-nocookie.com/embed/${id}?rel=0&modestbranding=1`;
    // YouTube retiró embed/live_stream (mostraba «Este vídeo no está disponible»).
    // Se incrusta el ID de la emisión vigente; se obtiene en
    // https://www.youtube.com/@Guitarras_MarianoConde/live (URL del vídeo en directo).
    // El enlace «Abrir en YouTube» apunta siempre al directo del canal.
    const LIVE_VIDEO_ID = 'ELvwXjxxZjM';
    const YT_LIVE = YT_VIDEO(LIVE_VIDEO_ID);
    const host = window.location.hostname;
    const parent = host && host !== 'localhost' && host !== '127.0.0.1' ? host : 'marianoconde.com';
    const TWITCH = `https://player.twitch.tv/?channel=guitarrasmarianoconde&parent=${parent}&muted=true`;
    let platform = 'youtube';

    function setActiveTab(name) {
      platform = name;
      tabs.forEach(t => {
        const active = t.dataset.platform === name;
        t.classList.toggle('is-active', active);
        t.setAttribute('aria-selected', String(active));
      });
    }
    function loadVideo(id, label) {
      setActiveTab('youtube');
      if (id === 'live') {
        playerFrame.src = YT_LIVE;
        if (playerCaption) playerCaption.textContent = T.liveIdle;
        if (openPlatform) { openPlatform.href = 'https://www.youtube.com/@Guitarras_MarianoConde/live'; openPlatform.textContent = T.liveOpen; }
      } else {
        playerFrame.src = YT_VIDEO(id);
        if (playerCaption) playerCaption.textContent = label ? `${T.now}${label}.` : T.nowDocumentary;
        if (openPlatform) { openPlatform.href = `https://www.youtube.com/watch?v=${id}`; openPlatform.textContent = T.watchYouTube; }
      }
      thumbs.forEach(t => t.classList.toggle('is-active', t.dataset.video === id));
    }
    tabs.forEach(tab => tab.addEventListener('click', () => {
      const name = tab.dataset.platform;
      setActiveTab(name);
      if (name === 'youtube') {
        loadVideo('0KmZT-WlaTs', DOCUMENTARY);
      } else {
        playerFrame.src = TWITCH;
        if (playerCaption) playerCaption.textContent = T.twitchIdle;
        if (openPlatform) { openPlatform.href = 'https://www.twitch.tv/guitarrasmarianoconde'; openPlatform.textContent = T.openTwitch; }
        thumbs.forEach(t => t.classList.remove('is-active'));
      }
    }));
    thumbs.forEach(thumb => thumb.addEventListener('click', () => {
      const id = thumb.dataset.video;
      const label = thumb.dataset.title || thumb.textContent.trim().replace(/^▶\s*|^●\s*/, '');
      loadVideo(id, id === 'live' ? null : label);
    }));
    if (goLiveBtn) goLiveBtn.addEventListener('click', () => loadVideo('live'));
  }

  /* ---------- Pestañas de galería ---------- */
  const galleryTabs = $$('.gallery-tab');
  if (galleryTabs.length) {
    galleryTabs.forEach(tab => tab.addEventListener('click', () => {
      galleryTabs.forEach(t => { t.classList.remove('is-active'); t.setAttribute('aria-pressed','false'); });
      tab.classList.add('is-active');
      tab.setAttribute('aria-pressed','true');
      const target = tab.dataset.gallery;
      $$('.gallery-panel').forEach(p => p.classList.toggle('is-active', p.id === target));
      // El lightbox debe usar solo las imágenes visibles
      if (typeof window.__mcGalleryRefresh === 'function') window.__mcGalleryRefresh();
      window.dispatchEvent(new CustomEvent('mc:gallery-tab', { detail: { target } }));
    }));
  }

  /* ---------- Lightbox ---------- */
  const lightbox = $('#lightbox');
  if (lightbox) {
    const lbImg = $('#lightboxImg');
    const lbClose = $('#lightboxClose');
    const lbPrev = $('#lightboxPrev');
    const lbNext = $('#lightboxNext');
    let galleryItems = $$('.gallery-panel.is-active .gallery-item');
    if (!galleryItems.length) galleryItems = $$('.gallery-item');
    let currentIndex = 0;
    let lastFocused = null;

    function showImage(index) {
      if (!galleryItems.length) return;
      currentIndex = (index + galleryItems.length) % galleryItems.length;
      lbImg.src = galleryItems[currentIndex].dataset.full;
      lbImg.alt = $('img', galleryItems[currentIndex]).alt;
    }
    window.__mcGalleryRefresh = () => {
      galleryItems = $$('.gallery-panel.is-active .gallery-item');
      if (!galleryItems.length) galleryItems = $$('.gallery-item');
    };
    document.addEventListener('click', e => {
      const item = e.target.closest('.gallery-item');
      if (!item) return;
      window.__mcGalleryRefresh();
      lastFocused = document.activeElement;
      lightbox.hidden = false;
      document.body.style.overflow = 'hidden';
      showImage(galleryItems.indexOf(item));
      lbClose.focus();
      window.dispatchEvent(new CustomEvent('mc:lightbox-open'));
    });
    function closeLightbox() {
      if (lightbox.hidden) return;
      lightbox.hidden = true;
      lbImg.src = '';
      document.body.style.overflow = '';
      window.dispatchEvent(new CustomEvent('mc:lightbox-close'));
      if (lastFocused) lastFocused.focus();
    }
    lbClose.addEventListener('click', closeLightbox);
    lbPrev.addEventListener('click', () => showImage(currentIndex - 1));
    lbNext.addEventListener('click', () => showImage(currentIndex + 1));
    lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
    document.addEventListener('keydown', e => {
      if (lightbox.hidden) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') showImage(currentIndex - 1);
      if (e.key === 'ArrowRight') showImage(currentIndex + 1);
    });
  }

  /* ---------- Carrusel 4K de «MC a escena» ---------- */
  const carousel = $('[data-carousel]');
  if (carousel) {
    const slides = $$('.escena-slide', carousel);
    const dots = $$('.escena-dot', carousel);
    const countEl = $('.escena-count strong', carousel);
    const prevBtn = $('.escena-prev', carousel);
    const nextBtn = $('.escena-next', carousel);
    const toggleBtn = $('.escena-toggle', carousel);
    const track = $('.escena-track', carousel);
    const panel = carousel.closest('.gallery-panel');
    const INTERVAL = 5000;
    const reasons = new Set();
    let current = 0;
    const instanceId = (carousel.__mcCarouselId || 0) + 1;
    carousel.__mcCarouselId = instanceId;

    if (slides.length < 2 && toggleBtn) toggleBtn.hidden = true;

    function setReason(reason, active) {
      if (active) reasons.add(reason);
      else reasons.delete(reason);
      syncPlayback();
    }
    function syncPlayback() {
      carousel.classList.toggle('is-paused', reasons.size > 0);
      if (toggleBtn) {
        const paused = reasons.has('manual');
        toggleBtn.setAttribute('aria-pressed', paused ? 'true' : 'false');
        toggleBtn.setAttribute('aria-label', paused ? T.resumeCarousel : T.pauseCarousel);
        toggleBtn.title = paused ? T.resumeCarousel : T.pauseCarousel;
      }
    }
    function goTo(index) {
      if (!slides.length) return;
      current = ((index % slides.length) + slides.length) % slides.length;
      if (track) track.style.transform = 'translate3d(-' + (current * 100) + '%, 0, 0)';
      slides.forEach((slide, i) => {
        const active = i === current;
        slide.classList.toggle('is-active', active);
        slide.setAttribute('tabindex', active ? '0' : '-1');
        slide.setAttribute('aria-hidden', active ? 'false' : 'true');
      });
      dots.forEach((dot, i) => {
        const active = i === current;
        dot.classList.toggle('is-active', active);
        dot.setAttribute('aria-current', active ? 'true' : 'false');
      });
      if (countEl) countEl.textContent = String(current + 1);
    }

    if (prevBtn) prevBtn.addEventListener('click', () => goTo(current - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => goTo(current + 1));
    dots.forEach(dot => dot.addEventListener('click', () => goTo(Number(dot.dataset.slide) || 0)));
    if (toggleBtn) toggleBtn.addEventListener('click', () => setReason('manual', !reasons.has('manual')));

    carousel.addEventListener('mouseenter', () => setReason('hover', true));
    carousel.addEventListener('mouseleave', () => setReason('hover', false));
    carousel.addEventListener('focusin', () => setReason('focus', true));
    carousel.addEventListener('focusout', e => {
      if (!carousel.contains(e.relatedTarget)) setReason('focus', false);
    });
    carousel.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1); }
    });

    document.addEventListener('visibilitychange', () => setReason('hidden', document.hidden));
    window.addEventListener('mc:lightbox-open', () => setReason('lightbox', true));
    window.addEventListener('mc:lightbox-close', () => setReason('lightbox', false));
    window.addEventListener('mc:gallery-tab', e => {
      setReason('inactive', !e.detail || e.detail.target !== 'escena');
    });

    if (document.hidden) reasons.add('hidden');
    if (panel && !panel.classList.contains('is-active')) reasons.add('inactive');
    const reducedQuery = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
    function onReduced(e) { setReason('reduced', e.matches); }
    if (reducedQuery) {
      if (reducedQuery.matches) reasons.add('reduced');
      if (reducedQuery.addEventListener) reducedQuery.addEventListener('change', onReduced);
      else if (reducedQuery.addListener) reducedQuery.addListener(onReduced);
    }

    goTo(0);
    syncPlayback();
    setInterval(() => {
      if (carousel.__mcCarouselId !== instanceId || reasons.size > 0) return;
      goTo(current + 1);
    }, INTERVAL);
  }

  /* ---------- Configurador de guitarra ---------- */
  $$('form[data-base]').forEach(form => {
    const totalEl = $('[data-config-total]', form);
    const selects = $$('select[data-config]', form);
    if (!totalEl || !selects.length) return;
    const base = Number(form.dataset.base) || 0;
    const format = n => new Intl.NumberFormat(EN ? 'en-GB' : 'es-ES').format(n);
    function updateTotal() {
      const extra = selects.reduce((sum, select) => {
        const opt = select.selectedOptions[0];
        return sum + (opt ? Number(opt.dataset.price || 0) : 0);
      }, 0);
      totalEl.textContent = format(base + extra);
    }
    selects.forEach(select => select.addEventListener('change', updateTotal));
    updateTotal();
  });

  /* ---------- Formularios (contacto y configurador) ---------- */
  $$('form[data-mailform], #contactForm').forEach(form => {
    const formStatus = $('.form-status', form) || $('#formStatus');
    form.addEventListener('submit', e => {
      e.preventDefault();
      const data = new FormData(form);
      const nombre = String(data.get('nombre') || '').trim();
      const email = String(data.get('email') || '').trim();
      const mensaje = String(data.get('mensaje') || '').trim();
      if (!nombre || !email || !data.get('privacidad')) {
        if (formStatus) {
          formStatus.textContent = T.formRequired;
          formStatus.style.color = '#a63d2f';
        }
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        if (formStatus) {
          formStatus.textContent = T.formEmail;
          formStatus.style.color = '#a63d2f';
        }
        return;
      }
      const asunto = String(data.get('asunto') || T.subject);
      const subject = encodeURIComponent(`[Web Mariano Conde] ${asunto} — ${nombre}`);
      let bodyText = `${T.name}: ${nombre}\n${T.phone}: ${String(data.get('telefono') || '—')}\n${T.email}: ${email}\n${T.topic}: ${asunto}\n\n${mensaje}`;
      const config = $$('select[data-config]', form).map(select =>
        `${select.name}: ${select.value}${Number(select.selectedOptions[0]?.dataset.price || 0) ? ` (+${select.selectedOptions[0].dataset.price} €)` : ''}`);
      if (config.length) {
        const totalEl = $('[data-config-total]', form);
        bodyText += `\n\n${T.configuration}\n${config.join('\n')}\n${T.estimatedTotal} ${totalEl ? totalEl.textContent : ''} €`;
      }
      if (formStatus) {
        formStatus.textContent = T.formReady;
        formStatus.style.color = '#9a7434';
      }
      window.location.href = `mailto:Info@marianoconde.com?subject=${subject}&body=${encodeURIComponent(bodyText)}`;
    });
  });

  /* ---------- Aviso de cookies ---------- */
  const cookieBanner = $('#cookieBanner');
  if (cookieBanner) {
    const KEY = 'mc-cookie-consent';
    const open = () => { cookieBanner.hidden = false; };
    const close = () => { cookieBanner.hidden = true; };
    let saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) { /* modo privado */ }
    if (!saved) open();
    const accept = (value) => {
      try { localStorage.setItem(KEY, value); } catch (e) { /* ignorar */ }
      close();
    };
    const acceptBtn = $('#cookieAccept');
    const denyBtn = $('#cookieDeny');
    const prefsBtn = $('#cookiePrefs');
    const prefsPanel = $('#cookiePrefsPanel');
    const saveBtn = $('#cookieSave');
    if (acceptBtn) acceptBtn.addEventListener('click', () => accept('all'));
    if (denyBtn) denyBtn.addEventListener('click', () => accept('none'));
    if (prefsBtn && prefsPanel) prefsBtn.addEventListener('click', () => {
      prefsPanel.hidden = !prefsPanel.hidden;
      prefsBtn.setAttribute('aria-expanded', String(!prefsPanel.hidden));
    });
    if (saveBtn) saveBtn.addEventListener('click', () => accept('custom'));
    const settings = $('#cookieSettings');
    if (settings) settings.addEventListener('click', open);
  }
})();
