import hashlib,json,re,shutil
from pathlib import Path
from PIL import Image

repo=Path(__file__).resolve().parents[1]
root=Path.cwd()
p=root/'app/src/main/java/uk/co/littledays/MainActivity.java'
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_CALENDAR_711' not in s:
    raise RuntimeError('Working 7.1.1 calendar repair must be present')
keys={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in (root/'signing').rglob('*') if f.is_file()}
if not keys: raise RuntimeError('Existing signing files missing')
gradle=root/'app/build.gradle'
g=gradle.read_text()
identity=re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)
if not identity: raise RuntimeError('Application ID missing')
def end(text,start):
    i=text.index('{',start)+1;depth=1;state='code'
    while i<len(text) and depth:
        c=text[i];pair=text[i:i+2]
        if state=='line':
            if c=='\n':state='code'
        elif state=='comment':
            if pair=='*/':state='code';i+=1
        elif state in ('"',"'"):
            if c=='\\':i+=1
            elif c==state:state='code'
        else:
            if pair=='//':state='line';i+=1
            elif pair=='/*':state='comment';i+=1
            elif c in ('"',"'"):state=c
            elif c=='{':depth+=1
            elif c=='}':depth-=1
        i+=1
    if depth:raise RuntimeError('Unbalanced source block')
    return i

def replace(signature,new):
    global s
    a=s.index(signature);b=end(s,a);s=s[:a]+new+s[b:]

a=s.index('final ThemeSpec[] themes=');b=end(s,a)
original=s[a:b]
themes=re.findall(r'new ThemeSpec\("([^"]+)","[^"]*","([^"]+)"',original)
lookup=json.loads((repo/'artwork/theme-cells.json').read_text())
if len(themes)!=43 or set(n for n,c in themes)!=set(lookup):
    raise RuntimeError('Actual theme inventory differs from reviewed mapping: '+str(themes))
if len(set(n for n,c in themes))!=42 or sum(n=='Apricot Hamster' for n,c in themes)!=2:
    raise RuntimeError('Unexpected duplicate inventory')
assets=root/'app/src/main/assets/artwork';assets.mkdir(parents=True,exist_ok=True)
manifest=json.loads((repo/'artwork/output-v3/character_manifest.json').read_text())
if manifest['meta']['version']!=3:raise RuntimeError('Approved v3 outputs required')
verified={(e['sheet'],e['cell']):e for e in manifest['characters']}
metadata={'themes':{},'props':{},'unused_artwork':[{'sheet':'character-atlas-01.png','cell':2,'description':'Mint-background flamingo; no separate named app theme'}],'saved_theme_indices_preserved':True}
for name,(sheet,index) in lookup.items():
    file=f'character-atlas-{sheet:02d}.png';entry=verified[(file,index)]
    if not entry.get('saved_alpha_mask_verified'):raise RuntimeError('Unverified portrait: '+name)
    image=Image.open(repo/'artwork/output-v3'/file).convert('RGBA')
    row,col=divmod(index,2);portrait=f'portrait_{sheet:02d}_{index}.png'
    image.crop((col*512+32,row*512+32,col*512+480,row*512+480)).save(assets/portrait)
    metadata['themes'][name]={'sheet':file,'cell':index,'portrait':portrait}
for image in (repo/'artwork/output-v3').glob('character-atlas-*.png'):shutil.copy2(image,assets/image.name)
props=json.loads((repo/'artwork/source/props_atlas_manifest.json').read_text())
if len(props['sprites'])!=39:raise RuntimeError('Expected 39 props')
for r in props['sprites']:metadata['props'][r['name']]=r
shutil.copy2(repo/'artwork/source/props_atlas.png',assets/'props_atlas.png')
shutil.copy2(repo/'artwork/source/props_atlas_manifest.json',assets/'props_atlas_manifest.json')
(assets/'theme-map.json').write_text(json.dumps(metadata,indent=2))
if '// A_DAY_TO_KEEP_ATLAS_72' not in s:
    start=s.index('String[] motifs(');motifs=s[start:end(s,start)]
    names=set(re.findall(r'"([a-z_]+)"',motifs))
    if names-set(metadata['props']):raise RuntimeError('Unmapped motifs: '+str(names-set(metadata['props'])))
    java=(repo/'scripts/artwork-renderer.java.inc').read_text()
    replace('class Mascot extends AnimatedArt {',java)
    replace('void draw(Canvas canvas,String name,float x,float y,float size,int alpha){','void draw(Canvas canvas,String name,float x,float y,float size,int alpha){drawArtProp(canvas,name,x,y,size,alpha);}')
    s=re.sub(r'new Mascot\((\w+)\.character,\s*(?:\1\.pink|PINK)\)',r'new Mascot(\1)',s)
    for args in re.findall(r'new Mascot\(([^()]*)\)',s):
        if not re.fullmatch(r'\w+',args):raise RuntimeError('Unresolved mascot constructor: '+args)
    old='for(int i=0;i<themes.length;i++)order.add(i);'
    new='LinkedHashMap<String,Integer> uniqueThemes=new LinkedHashMap<>();for(int i=0;i<themes.length;i++){String name=themes[i].name;if(!uniqueThemes.containsKey(name)||i==themeIndex)uniqueThemes.put(name,i);}order.addAll(uniqueThemes.values());'
    if s.count(old)!=1:raise RuntimeError('Theme dropdown ordering hook changed')
    s=s.replace(old,new,1)
    replace('boolean applyThemePolicy(boolean opening){',r'''boolean applyThemePolicy(boolean opening){if(data==null)return false;String mode=data.optString("themeMode","manual"),today=LocalDate.now().toString();boolean choose=(mode.equals("daily")&&!today.equals(data.optString("themeDay")))||(mode.equals("eachUse")&&opening);if(!choose)return false;int current=Math.max(0,Math.min(themes.length-1,data.optInt("theme",0)));LinkedHashMap<String,Integer> unique=new LinkedHashMap<>();for(int i=0;i<themes.length;i++)if(!themes[i].name.equals(themes[current].name)&&!unique.containsKey(themes[i].name))unique.put(themes[i].name,i);if(unique.isEmpty())return false;ArrayList<Integer> candidates=new ArrayList<>(unique.values());int selected=candidates.get(new Random().nextInt(candidates.size()));try{data.put("theme",selected);data.put("themeDay",today);save();return true;}catch(Exception error){android.util.Log.w("ADayToKeep","Could not change theme",error);return false;}}''')
    code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
    s+='\n// ARTWORK_VERSION_CODE:'+str(code)+'\n'
else:
    code=int(re.search(r'// ARTWORK_VERSION_CODE:(\d+)',s).group(1))
a=s.index('final ThemeSpec[] themes=');b=end(s,a)
if s[a:b]!=original:raise RuntimeError('Theme definitions or indices changed')
s=s.replace('Version 7.1.1','Version 7.2').replace('Version 7.1','Version 7.2')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g)
g=re.sub(r'versionName\s+[\'"][^\'"]+[\'\"]','versionName "7.2"',g)
if re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)!=identity:raise RuntimeError('Application identity changed')
if any(hashlib.sha256(Path(f).read_bytes()).hexdigest()!=digest for f,digest in keys.items()):raise RuntimeError('Signing material changed')
p.write_text(s,encoding='utf-8');gradle.write_text(g)
report={'version':'7.2','version_code':code,'stored_theme_entries':len(themes),'visible_unique_themes':42,'theme_array_unchanged':True,'application_id':identity[0],'signing_files_unchanged':True,'mappings':[{'stored_index':i,'name':name,**metadata['themes'][name]} for i,(name,character) in enumerate(themes)],'spare':metadata['unused_artwork']}
(root/'artwork-integration-report.json').write_text(json.dumps(report,indent=2))
print('Artwork integrated; compile and emulator checks still required.')
