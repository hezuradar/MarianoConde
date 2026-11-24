#!/usr/bin/env python3
"""Actualiza el ID del directo de YouTube en app.js mientras el canal está emitiendo.

Lo ejecuta .github/workflows/actualizar-directo.yml cada 10 minutos. Si no hay
emisión activa no cambia nada, así que se conserva el último directo visible.
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

LIVE_URL = "https://www.youtube.com/@Guitarras_MarianoConde/live"
APP_JS = Path(__file__).resolve().parent / "app.js"
LIVE_ID_RE = re.compile(r"const LIVE_VIDEO_ID = '([A-Za-z0-9_-]{11})';")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def live_video_id():
    """Devuelve el ID del vídeo en directo, o None si no hay emisión activa."""
    req = urllib.request.Request(
        LIVE_URL,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "es-ES,es;q=0.9"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode("utf-8", "ignore")

    marker = re.search(r"var ytInitialPlayerResponse\s*=\s*", html)
    if not marker:
        return None
    player, _ = json.JSONDecoder().raw_decode(html[marker.end():])
    if player.get("playabilityStatus", {}).get("status") != "OK":
        return None
    details = player.get("microformat", {}).get("playerMicroformatRenderer", {})
    if not details.get("liveBroadcastDetails", {}).get("isLiveNow"):
        return None
    video_id = player.get("videoDetails", {}).get("videoId", "")
    return video_id if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id) else None


def main():
    # newline='' conserva los saltos de línea originales de app.js.
    with APP_JS.open("r", encoding="utf-8", newline="") as fh:
        source = fh.read()
    match = LIVE_ID_RE.search(source)
    if not match:
        print("No se encontró LIVE_VIDEO_ID en app.js; no se hace nada.")
        return

    try:
        video_id = live_video_id()
    except Exception as exc:  # YouTube no responde o cambia el formato
        print(f"No se pudo consultar el directo ({exc}); se mantiene el ID actual.")
        return

    if not video_id:
        print("No hay emisión activa; se mantiene el ID actual.")
        return
    if video_id == match.group(1):
        print(f"Directo activo {video_id}: sin cambios.")
        return

    updated = source[:match.start(1)] + video_id + source[match.end(1):]
    with APP_JS.open("w", encoding="utf-8", newline="") as fh:
        fh.write(updated)
    print(f"Directo actualizado: {match.group(1)} -> {video_id}")


if __name__ == "__main__":
    main()
