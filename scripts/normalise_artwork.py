import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
import process_artwork as old

SOURCE = Path('artwork/source')
OUTPUT = Path('artwork/output')

def normalise(cell):
    a = np.array(cell.getchannel('A'))
    ys, xs = np.where(a > 8)
    if not len(xs):
        if a.any():
            raise ValueError('Faint pixels in supposedly empty cell')
        return Image.new('RGBA', (512, 512)), None
    box = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
    w, h = box[2]-box[0], box[3]-box[1]
    if min(box[:2]) == 0 or box[2] == 512 or box[3] == 512:
        raise ValueError('Artwork touches cell boundary; manual review required')
    if max(w/h, h/w) > 1.04:
        raise ValueError('Boundary too oval; manual review required')
    tile = cell.crop(box).resize((448, 448), Image.Resampling.LANCZOS)
    yy, xx = np.mgrid[:448, :448]
    core = (xx-223.5)**2 + (yy-223.5)**2 < 220**2
    alpha = np.array(tile.getchannel('A'))
    if np.any(alpha[core] < 250):
        raise ValueError('Non-opaque interior; manual review required')
    mask = Image.new('L', (1792, 1792))
    ImageDraw.Draw(mask).ellipse((0, 0, 1791, 1791), fill=255)
    mask = mask.resize((448, 448), Image.Resampling.LANCZOS)
    reference = np.array(mask)
    if np.count_nonzero((alpha > 127) != (reference > 127)) / np.count_nonzero(reference > 127) > 0.01:
        raise ValueError('Boundary differs from a circle; manual review required')
    tile.putalpha(Image.fromarray(np.minimum(alpha, reference).astype('uint8')))
    out = Image.new('RGBA', (512, 512))
    out.paste(tile, (32, 32))
    return out, box

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    entries, failures = [], []
    sheets = [SOURCE / f'character-atlas-{i:02d}.png' for i in range(1, 12)]
    preview = Image.new('RGB', (1024, 11*280), '#eeeeee')
    draw = ImageDraw.Draw(preview)
    for number, path in enumerate(sheets):
        source = Image.open(path).convert('RGBA')
        if source.size != (1024, 1024):
            raise ValueError(f'{path.name}: dimensions must be 1024x1024')
        out = Image.new('RGBA', (1024, 1024))
        for index in range(4):
            row, col = divmod(index, 2)
            cell = source.crop((col*512, row*512, col*512+512, row*512+512))
            entry = {'sheet': path.name, 'cell': index, 'grid_row': row, 'grid_column': col}
            try:
                tile, box = normalise(cell)
                entry.update(status='processed' if box else 'empty', source_bounds=box)
                out.paste(tile, (col*512, row*512))
            except ValueError as error:
                entry.update(status='needs_review', reason=str(error))
                failures.append(f'{path.name} cell {index}: {error}')
            entries.append(entry)
        destination = OUTPUT / path.name
        out.save(destination)
        saved = Image.open(destination).convert('RGBA')
        for entry in entries[-4:]:
            if entry['status'] != 'processed':
                continue
            col, row = entry['grid_column'], entry['grid_row']
            cell = saved.crop((col*512, row*512, col*512+512, row*512+512))
            measured = cell.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
            entry['measured_bounds_at_alpha_gt_8'] = measured
            entry['verified'] = measured == (32, 32, 480, 480)
            if not entry['verified']:
                failures.append(f'{path.name} cell {entry["cell"]}: saved bounds {measured}')
            if measured:
                l, t, r, b = measured
                entry.update(measured_width=r-l, measured_height=b-t, centre=[(l+r)/2, (t+b)/2], margins=[l,t,512-r,512-b])
        for index in range(4):
            row, col = divmod(index, 2)
            thumb = saved.crop((col*512,row*512,col*512+512,row*512+512)).resize((248,248))
            preview.paste(thumb, (index*256,number*280+24), thumb)
        draw.text((4, number*280+4), path.name, fill='black')
    preview.save(OUTPUT / 'character-contact-sheet.jpg', quality=95)
    props = old.validate_props()
    mismatches = sum(item['status'] != 'match' for item in props['results'])
    processed = sum(e['status'] == 'processed' for e in entries)
    empty = sum(e['status'] == 'empty' for e in entries)
    if processed != 43 or empty != 1 or entries[-1]['status'] != 'empty':
        failures.append('Expected exactly 43 portraits and only sheet 11 bottom-right empty')
    (OUTPUT / 'character_manifest.json').write_text(json.dumps({'meta': {'version': 2, 'target_diameter':448, 'measurement_alpha_threshold':8, 'cell_size':512, 'theme_mapping':'not yet verified'}, 'characters':entries}, indent=2))
    (OUTPUT / 'props_validation.json').write_text(json.dumps(props, indent=2))
    for name in ['props_atlas.png', 'props_atlas_manifest.json']:
        shutil.copy2(SOURCE / name, OUTPUT / name)
    report = ['# Artwork report v2', f'- Portraits processed: {processed}', f'- Empty cells: {empty}', f'- Saved portraits with verified 448x448 bounds: {sum(e.get("verified", False) for e in entries)}', f'- Prop mismatches: {mismatches}', f'- Review issues: {len(failures)}', '', 'Slight width/height adjustment corrects oval proportions. Source alpha is retained within an antialiased circle. Bounds are measured after reopening saved PNGs at alpha > 8; this is not proof of a mathematically perfect circle. Theme mappings require separate verification.', '', *failures]
    (OUTPUT / 'report.md').write_text('\n'.join(report))
    if failures or mismatches:
        raise SystemExit('Review required; inspect the uploaded report before using outputs')

if __name__ == '__main__':
    main()
