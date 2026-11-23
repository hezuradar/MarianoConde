from pathlib import Path
import re
import json

lines = Path('_poema_text.txt').read_text(encoding='utf-8').splitlines()
start = next(i for i, l in enumerate(lines) if l == 'Nº1')

blocks = []
cur = None
for l in lines[start:]:
    if l.startswith('Solicita tu Guitarra'):
        break
    m = re.fullmatch(r'Nº\s*(\d+)', l)
    if m:
        if cur:
            blocks.append(cur)
        cur = {'num': int(m.group(1)), 'lines': []}
    elif cur is not None:
        if l.startswith('Fotos orientativas') or l.startswith('Guitarra del Poema Nº'):
            continue
        cur['lines'].append(l)
if cur:
    blocks.append(cur)

entries = []
for b in blocks:
    ls = [x for x in b['lines'] if x]
    year = ''
    if ls and re.fullmatch(r'(?:19|20)\d{2}(?:/\d{2})?', ls[0]):
        year = ls.pop(0)
    name = ls.pop(0) if ls else ''
    mi = ls.index('Materiales') if 'Materiales' in ls else len(ls)
    meta = ls[:mi]
    materials = ' '.join(ls[mi + 1:]) if mi < len(ls) else ''
    owner = meta[0] if meta else ''
    rest = meta[1:]
    place = ''
    if rest and rest[0].startswith(('–', '-')):
        place = rest.pop(0).lstrip('–- ').strip()
    verse = ' '.join(rest)
    if b['num'] == 56:
        name = 'Rombo'
        owner = 'Colección particular'
        place = 'España'
        materials = 'En construcción'
    entries.append({
        'num': b['num'], 'year': year, 'name': name, 'owner': owner,
        'place': place, 'verse': verse, 'materials': materials,
    })

Path('poema-data.json').write_text(
    json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
print('ENTRADAS:', len(entries))
for e in entries:
    if e['num'] in (47, 48, 56, 57, 58):
        print(e)
