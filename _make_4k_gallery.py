# -*- coding: utf-8 -*-
"""Genera versiones 4K de las fotos de «MC a escena» para el carrusel.

Las fotos originales descargadas del sitio anterior no superan los 1366 px de
ancho, así que no contienen detalle 4K real: se reescalan con Lanczos sobre un
lienzo 3840x2160, con relleno oscuro y un sharpen suave. Los archivos resultantes
son WebP para que el carrusel cargue rápido sin perder la resolución declarada.
"""
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

from build_site import ESCENA_IMAGES, IMGPATH

OUT = IMGPATH / '4k'
CANVAS = (3840, 2160)
BACKGROUND = (13, 12, 11)


def make_4k(name):
    src = IMGPATH / name
    if not src.exists():
        print(f'  omitida (no existe): {name}')
        return None
    with Image.open(src) as original:
        fitted = ImageOps.contain(original.convert('RGB'), CANVAS, Image.Resampling.LANCZOS)
        image = Image.new('RGB', CANVAS, BACKGROUND)
        image.paste(fitted, ((CANVAS[0] - fitted.width) // 2, (CANVAS[1] - fitted.height) // 2))
        image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=3))
    dst = OUT / f'{Path(name).stem}-4k.webp'
    image.save(dst, 'WEBP', quality=86, method=6)
    return dst


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for name in ESCENA_IMAGES:
        dst = make_4k(name)
        if dst:
            total += dst.stat().st_size
            print(f'  {dst.name}: {dst.stat().st_size / 1024 / 1024:.2f} MB')
    print(f'Generadas {len(list(OUT.glob("*-4k.webp")))} imágenes 4K ({total / 1024 / 1024:.1f} MB).')


if __name__ == '__main__':
    main()
