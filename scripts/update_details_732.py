import ast,hashlib,json,re
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java');s=p.read_text()
if '// A_DAY_TO_KEEP_LAYOUT_731' not in s:raise RuntimeError('Working 7.3.1 required')
module=ast.parse((repo/'scripts/integrate_artwork.py').read_text());namespace={}
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='end'],type_ignores=[]),'parser','exec'),namespace);end=namespace['end']
def edit(signature,fn):
 global s
 a=s.index(signature);b=end(s,a);s=s[:a]+fn(s[a:b])+s[b:]
def need(text,old,new):
 if text.count(old)!=1:raise RuntimeError('Expected one hook: '+old)
 return text.replace(old,new,1)
a=s.index('final ThemeSpec[] themes=');themes=s[a:end(s,a)]
keys={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('signing').rglob('*') if f.is_file()}
gradle=Path('app/build.gradle');g=gradle.read_text();identity=re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)
if '// A_DAY_TO_KEEP_DETAIL_732' not in s:
 edit('class ScrollGutter731 ',lambda t:need(t,'int right=baseRight+(needed?dp(7):0);','int right=baseRight+(needed?dp(12):0);'))
 def scrolls(t):
  if t.count('view.setScrollbarFadingEnabled(true);')!=2:raise RuntimeError('Scrollbar fading hooks changed')
  return t.replace('view.setScrollbarFadingEnabled(true);','view.setScrollbarFadingEnabled(false);')
 edit('void themedScrolls(View view){',scrolls)
 def notes(t):
  if t.count('pen.setColor(INK);')!=3:raise RuntimeError('Sticky note stroke hooks changed')
  return t.replace('pen.setColor(INK);','pen.setColor(blend(INK,WHITE,.40f));').replace('pen.setStrokeWidth(1.9f);','pen.setStrokeWidth(1.6f);')
 edit('void drawNotesSymbol(',notes)
 def glyph(t):
  a=t.index('if(kind.equals("refresh"))');b=end(t,a)
  return t[:a]+'if(kind.equals("refresh")){c.save();c.scale(getWidth()/40f,getHeight()/40f);p.setColor(settingsCogTint732());p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.6f);p.setStrokeCap(Paint.Cap.ROUND);c.drawArc(9,9,31,31,45,270,false,p);p.setStyle(Paint.Style.FILL);Path arrow=new Path();arrow.moveTo(28.84f,13.28f);arrow.lineTo(21.77f,11.87f);arrow.lineTo(27.43f,6.21f);arrow.close();c.drawPath(arrow,p);c.restore();return;}'+t[b:]
 edit('class ActionGlyph extends View {',glyph)
 s=need(s,' JSONObject data;',' // A_DAY_TO_KEEP_DETAIL_732\n String cogTintKey732="";int cogTintValue732;\n int settingsCogTint732(){String key=(theme==null?"":theme.name)+":"+INK+":"+LILAC;if(!key.equals(cogTintKey732)){Bitmap sample=Bitmap.createBitmap(80,80,Bitmap.Config.ARGB_8888);try{Icon cog=new Icon("gear");cog.layout(0,0,80,80);cog.draw(new Canvas(sample));int[] pixels=new int[6400];sample.getPixels(pixels,0,80,0,0,80,80);HashMap<Integer,Integer> counts=new HashMap<>();int best=0,selected=blend(LILAC,INK,.25f);for(int color:pixels){if(Color.alpha(color)<240)continue;int count=counts.containsKey(color)?counts.get(color)+1:1;counts.put(color,count);if(count>best){best=count;selected=color;}}cogTintValue732=selected;cogTintKey732=key;}finally{sample.recycle();}}return cogTintValue732;}\n'+'\n JSONObject data;')
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// DETAIL_VERSION_CODE:'+str(code)+'\n'
else:code=int(re.search(r'// DETAIL_VERSION_CODE:(\d+)',s).group(1))
a=s.index('final ThemeSpec[] themes=')
if s[a:end(s,a)]!=themes:raise RuntimeError('Stored theme array changed')
if not keys or any(hashlib.sha256(Path(f).read_bytes()).hexdigest()!=digest for f,digest in keys.items()):raise RuntimeError('Signing changed')
s=s.replace('Version 7.3.1','Version 7.3.2')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.3.2"',g)
if re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)!=identity:raise RuntimeError('Application ID changed')
p.write_text(s);gradle.write_text(g)
report=Path('ui-amendments-report.json');data=json.loads(report.read_text());data.update(version='7.3.2',version_code=code,scrollbar_visibility='persistent when overflow exists',scroll_gutter_dp=12,no_scroll_gutter_dp=0,refresh_icon='redrawn arrow; dominant settings cog colour per theme',notes_outline='40 percent white blend and 1.6 unit stroke');report.write_text(json.dumps(data,indent=2))
print('7.3.2 detail refinements prepared; Android build and device checks required')
