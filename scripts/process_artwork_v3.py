import json
import shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt
import process_artwork as old

SOURCE = Path('artwork/source')
OUT = Path('artwork/output-v3')
yy, xx = np.mgrid[:1792, :1792]
mask = Image.fromarray((((xx+.5-896)**2+(yy+.5-896)**2 <= 896**2)*255).astype('uint8')).resize((448,448), Image.Resampling.BOX)
expected = Image.new('L',(512,512))
expected.paste(mask,(32,32))

def correct(cell):
    alpha = np.array(cell.getchannel('A'))
    box = cell.getchannel('A').point(lambda v:255 if v>127 else 0).getbbox()
    if box is None:
        if alpha.max()>8:
            raise ValueError('Unexpected faint artwork, not an empty cell')
        return Image.new('RGBA',(512,512)), None
    w,h = box[2]-box[0], box[3]-box[1]
    if max(w/h,h/w)>1.04:
        raise ValueError('Excessive oval distortion; review required')
    crop = np.array(cell.crop(box))
    good = crop[:,:,3]>=250
    sy,sx = np.mgrid[:h,:w]
    inner = ((sx+.5-w/2)/(w/2))**2+((sy+.5-h/2)/(h/2))**2 < 0.8**2
    if not good.any() or np.any(crop[:,:,3][inner]<250):
        raise ValueError('Unexpected central transparency; review required')
    indices = distance_transform_edt(~good,return_distances=False,return_indices=True)
    rgb = crop[:,:,:3].copy()
    rgb[~good] = rgb[tuple(indices[:,~good])]
    tile = Image.fromarray(rgb).resize((448,448),Image.Resampling.LANCZOS).convert('RGBA')
    tile.putalpha(mask)
    result = Image.new('RGBA',(512,512))
    result.paste(tile,(32,32))
    return result,box

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    entries=[]
    preview=Image.new('RGB',(1024,3080),'#eeeeee')
    draw=ImageDraw.Draw(preview)
    for number in range(1,12):
        name=f'character-atlas-{number:02d}.png'
        source=Image.open(SOURCE/name).convert('RGBA')
        if source.size!=(1024,1024):
            raise ValueError(f'{name}: incorrect sheet dimensions')
        atlas=Image.new('RGBA',(1024,1024))
        sheet_entries=[]
        for index in range(4):
            row,col=divmod(index,2)
            cell=source.crop((col*512,row*512,col*512+512,row*512+512))
            tile,box=correct(cell)
            if (box is None)!=(number==11 and index==3):
                raise ValueError(f'{name} cell {index}: unexpected occupancy')
            atlas.paste(tile,(col*512,row*512))
            sheet_entries.append({'sheet':name,'cell':index,'source_bounds_alpha_gt_127':box,'status':'processed' if box else 'empty'})
        atlas.save(OUT/name)
        saved=Image.open(OUT/name).convert('RGBA')
        for entry in sheet_entries:
            index=entry['cell']
            row,col=divmod(index,2)
            cell=saved.crop((col*512,row*512,col*512+512,row*512+512))
            a=cell.getchannel('A')
            target=expected if entry['status']=='processed' else Image.new('L',(512,512))
            if not np.array_equal(np.array(a),np.array(target)):
                raise ValueError(f'{name} cell {index}: saved mask mismatch')
            box=a.getbbox()
            entry.update(saved_alpha_mask_verified=True,measured_bounds=box)
            if box:
                l,t,r,b=box
                entry.update(measured_width=r-l,measured_height=b-t,centre=[(l+r)/2,(t+b)/2],margins=[l,t,512-r,512-b])
                if box!=(32,32,480,480):
                    raise ValueError('Saved bounds incorrect')
            thumb=cell.resize((248,248))
            preview.paste(thumb,(index*256,(number-1)*280+24),thumb)
        entries.extend(sheet_entries)
        draw.text((4,(number-1)*280+4),name,fill='black')
    props=old.validate_props()
    mismatches=sum(e['status']!='match' for e in props['results'])
    (OUT/'props_validation.json').write_text(json.dumps(props,indent=2))
    for name in ['props_atlas.png','props_atlas_manifest.json']:
        shutil.copy2(SOURCE/name,OUT/name)
    preview.save(OUT/'character-contact-sheet.jpg',quality=95)
    (OUT/'character_manifest.json').write_text(json.dumps({'meta':{'version':3,'cell_size':512,'diameter':448,'theme_mapping':'not yet verified','method':'Tight alpha>127 bounds; slight independent axis scaling; extend edge colours from nearest alpha>=250 pixel; replace alpha with identical antialiased circle'},'characters':entries},indent=2))
    lines=['# Artwork report v3','- Portraits processed and saved masks verified: 43','- Fully transparent empty cells verified: 1','- Measured portrait bounds: 448 x 448 pixels','- Measured centres within cells: 256, 256','- Transparent margins: 32 pixels on all four sides',f'- Prop crop-check mismatches: {mismatches}','','Original files unchanged. Interior alpha is 255 except the antialiased perimeter. Edge colours were extended from nearby near-opaque source pixels; inspect the preview before integration. Theme-to-cell mapping is not yet verified.']
    (OUT/'report.md').write_text('\n'.join(lines))
    if mismatches:
        raise SystemExit('Review prop crop checks')

if __name__=='__main__':
    main()
