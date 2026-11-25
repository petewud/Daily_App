import ast,hashlib,json,re
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java');s=p.read_text()
if '// A_DAY_TO_KEEP_NOTES_WIDGET_733' not in s:raise RuntimeError('Working 7.3.3 required')
module=ast.parse((repo/'scripts/integrate_artwork.py').read_text());namespace={}
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='end'],type_ignores=[]),'parser','exec'),namespace);end=namespace['end']
def edit(signature,fn):
 global s
 a=s.index(signature);b=end(s,a);s=s[:a]+fn(s[a:b])+s[b:]
def need(text,old,new):
 if text.count(old)!=1:raise RuntimeError('Expected one hook: '+old[:100])
 return text.replace(old,new,1)
a=s.index('final ThemeSpec[] themes=');themes=s[a:end(s,a)]
keys={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('signing').rglob('*') if f.is_file()}
gradle=Path('app/build.gradle');g=gradle.read_text();identity=re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)
switch='LinearLayout gameBox=section(WHITE);gameBox.addView(label("Game mode (demo)",22));Switch gameSwitch=new Switch(this);gameSwitch.setText("Island game");gameSwitch.setTextColor(INK);gameSwitch.setTypeface(bodyFont);gameSwitch.setPadding(dp(3),dp(10),dp(3),dp(10));gameSwitch.setChecked(data.optBoolean("gameMode",false));gameSwitch.setOnCheckedChangeListener((v,on)->{try{data.put("gameMode",on);save();}catch(Exception ignored){}});wirePress(gameSwitch);gameBox.addView(gameSwitch);gameBox.addView(text("When on, tap your character on the home page to visit a little pixel island. Early demo: every sprite is drawn by code, with no sprite sheets.",13));content.addView(gameBox);space(content,16);'
if '// A_DAY_TO_KEEP_ISLAND_74' not in s:
 edit('void settings(){',lambda t:need(t,'LinearLayout backup=section(LILAC);',switch+'LinearLayout backup=section(LILAC);'))
 edit('void attachCharacterPlay(',lambda t:t[:-1]+'installGameTap74();}')
 s=need(s,' JSONObject data;',(repo/'scripts/island-demo-74.java.inc').read_text()+'\n JSONObject data;')
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// ISLAND_VERSION_CODE:'+str(code)+'\n'
else:code=int(re.search(r'// ISLAND_VERSION_CODE:(\d+)',s).group(1))
a=s.index('final ThemeSpec[] themes=')
if s[a:end(s,a)]!=themes:raise RuntimeError('Stored theme array changed')
if not keys or any(hashlib.sha256(Path(f).read_bytes()).hexdigest()!=digest for f,digest in keys.items()):raise RuntimeError('Signing changed')
s=s.replace('Version 7.3.3','Version 7.4.0 demo')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.4.0"',g)
if re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)!=identity:raise RuntimeError('Application ID changed')
p.write_text(s);gradle.write_text(g)
report=Path('ui-amendments-report.json');data=json.loads(report.read_text());data.update(version='7.4.0',version_code=code,island_demo='procedural pixel island, no sprite sheets; off by default via gameMode setting');report.write_text(json.dumps(data,indent=2))
print('7.4.0 island demo prepared; Android build and device checks required')
