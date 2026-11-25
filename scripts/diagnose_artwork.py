import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

source = Path('artwork/source')
out = Path('artwork/diagnostics')
out.mkdir(parents=True, exist_ok=True)
results = []
lines = ['# Original artwork diagnostics', '', 'No source images were changed. Cell numbers are 0=top-left, 1=top-right, 2=bottom-left, 3=bottom-right.', 'Alpha ranges from 0 (transparent) to 255 (opaque). Measurements below are diagnostics, not artwork approval.', '']
for number in range(1, 12):
    path = source / f'character-atlas-{number:02d}.png'
    with Image.open(path) as opened:
        mode = opened.mode
        im = opened.convert('RGBA')
    if im.size != (1024, 1024):
        lines.append(f'{path.name}: unexpected dimensions {im.size}')
        continue
    preview = Image.new('RGB', (2048, 512), '#cccccc')
    for index in range(4):
        row, col = divmod(index, 2)
        cell = im.crop((col*512,row*512,col*512+512,row*512+512))
        a = np.array(cell.getchannel('A'))
        entry = {'sheet':path.name, 'cell':index, 'original_mode':mode, 'nonzero_pixels':int(np.count_nonzero(a)), 'max_alpha':int(a.max()), 'alpha_histogram':np.bincount(a.ravel(), minlength=256).tolist(), 'bounds_by_alpha_threshold':{str(t):cell.getchannel('A').point(lambda v:255 if v>t else 0).getbbox() for t in [0,8,127,249]}}
        box = entry['bounds_by_alpha_threshold']['8']
        if box:
            tile = cell.crop(box).resize((448,448), Image.Resampling.LANCZOS)
            ta = np.array(tile.getchannel('A'))
            yy, xx = np.mgrid[:448,:448]
            radius = np.sqrt((xx-223.5)**2+(yy-223.5)**2)
            entry['regions_after_tight_resize'] = {}
            for name, region in [('centre_r200',radius<200),('test_core_r220',radius<220),('edge_ring_r200_to224',(radius>=200)&(radius<224))]:
                values = ta[region]
                entry['regions_after_tight_resize'][name] = {'pixels':int(values.size),'alpha_min':int(values.min()),'alpha_percentiles':np.percentile(values,[1,5,50,95,99]).tolist(),'pixels_below_250':int(np.count_nonzero(values<250)),'percent_below_250':float(100*np.mean(values<250))}
            bad_y, bad_x = np.where((ta<250)&(radius<220))
            entry['first_20_low_alpha_core_pixels'] = [{'x':int(x),'y':int(y),'alpha':int(ta[y,x])} for y,x in zip(bad_y[:20],bad_x[:20])]
        results.append(entry)
        preview.paste(cell,(index*512,0),cell)
        heat = np.zeros((512,512,3),dtype='uint8')
        heat[:,:,0] = 255-a
        heat[:,:,1] = a
        Image.fromarray(heat).save(out / f'{path.stem}-cell-{index}-alpha.png')
        ImageDraw.Draw(preview).text((index*512+5,5),f'cell {index}',fill='black')
        regions = entry.get('regions_after_tight_resize',{})
        lines.append(f'{path.name} cell {index}: bounds(alpha>8)={box}; max alpha={entry["max_alpha"]}; nonzero pixels={entry["nonzero_pixels"]}')
        for name, stats in regions.items():
            lines.append(f'  {name}: min={stats["alpha_min"]}, below 250={stats["pixels_below_250"]}/{stats["pixels"]} ({stats["percent_below_250"]:.4f}%)')
    preview.save(out / f'{path.stem}-original-preview.jpg',quality=95)
(out / 'diagnostics.json').write_text(json.dumps(results,indent=2))
(out / 'report.md').write_text('\n'.join(lines))
