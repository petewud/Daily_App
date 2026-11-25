import ast,hashlib,json,re
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java');s=p.read_text()
if '// A_DAY_TO_KEEP_DETAIL_732' not in s:raise RuntimeError('Working 7.3.2 required')
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
if '// A_DAY_TO_KEEP_NOTES_WIDGET_733' not in s:
 def notes(t):
  t=need(t,'ScrollView scroll=new ScrollView(this);','NotesScroll733 scroll=new NotesScroll733();')
  overlay='NotesThumb733 notesThumb=new NotesThumb733(scroll);FrameLayout.LayoutParams thumbLp=new FrameLayout.LayoutParams(dp(3),-1,Gravity.RIGHT);thumbLp.setMargins(0,dp(8),dp(1),dp(80));area.addView(notesThumb,thumbLp);'
  return need(t,'area.addView(scroll,new FrameLayout.LayoutParams(-1,-1));','area.addView(scroll,new FrameLayout.LayoutParams(-1,-1));'+overlay)
 edit('void notes(){',notes)
 edit('void themedScrolls(View view){',lambda t:t[:-1]+'if(view instanceof NotesScroll733)view.setVerticalScrollbarThumbDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));}')
 s=need(s,' JSONObject data;',(repo/'scripts/notes-thumb-733.java.inc').read_text()+'\n JSONObject data;')
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// NOTES_WIDGET_VERSION_CODE:'+str(code)+'\n'
else:code=int(re.search(r'// NOTES_WIDGET_VERSION_CODE:(\d+)',s).group(1))
widget=Path('app/src/main/java/uk/co/littledays/KeepWidget.java');w=widget.read_text()
if '// COUNT_BAND_733' not in w:
 w=need(w,'if(character!=null){c.drawBitmap(character,null,characterBounds,paint);character.recycle();}','float characterInkBottom=characterBounds.bottom;if(character!=null){int[] inkRow=new int[character.getWidth()];boolean foundInk=false;for(int y=character.getHeight()-1;y>=0&&!foundInk;y--){character.getPixels(inkRow,0,character.getWidth(),0,y,character.getWidth(),1);for(int pixel:inkRow)if(Color.alpha(pixel)>8){characterInkBottom=characterBounds.top+(y+1)*characterBounds.height()/character.getHeight();foundInk=true;break;}}c.drawBitmap(character,null,characterBounds,paint);character.recycle();}')
 w=need(w,'c.drawText(completed+"/"+total,128,216,paint);','String countLabel=completed+"/"+total;Rect countBounds=new Rect();float countTop=characterInkBottom+3f,countBottom=center+radius-6.5f-3f;float bandHeight=Math.max(1,countBottom-countTop);float innerRadius=radius-6.5f;for(int attempt=0;attempt<3;attempt++){paint.getTextBounds(countLabel,0,countLabel.length(),countBounds);float baseline=(countTop+countBottom-countBounds.top-countBounds.bottom)/2;float dy=Math.max(Math.abs(baseline+countBounds.top-center),Math.abs(baseline+countBounds.bottom-center));float width=Math.max(1,2*(float)Math.sqrt(Math.max(0,innerRadius*innerRadius-dy*dy))-6f);float factor=Math.min(1,Math.min(bandHeight/Math.max(1,countBounds.height()),width/Math.max(1,countBounds.width())));if(factor>=1)break;paint.setTextSize(paint.getTextSize()*factor*.98f);}paint.getTextBounds(countLabel,0,countLabel.length(),countBounds);float countBaseline=(countTop+countBottom-countBounds.top-countBounds.bottom)/2;c.drawText(countLabel,128,countBaseline,paint);')
 w+='\n// COUNT_BAND_733\n'
widget.write_text(w)
a=s.index('final ThemeSpec[] themes=')
if s[a:end(s,a)]!=themes:raise RuntimeError('Stored theme array changed')
if not keys or any(hashlib.sha256(Path(f).read_bytes()).hexdigest()!=digest for f,digest in keys.items()):raise RuntimeError('Signing changed')
s=s.replace('Version 7.3.2','Version 7.3.3')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.3.3"',g)
if re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)!=identity:raise RuntimeError('Application ID changed')
p.write_text(s);gradle.write_text(g)
report=Path('ui-amendments-report.json');data=json.loads(report.read_text());data.update(version='7.3.3',version_code=code,notes_scrollbar='persistent sibling thumb while overflow exists; no fade',widget_count='glyph-centred below actual character alpha bounds and above inner radial ring, with 3px minimum padding in 256px canvas');report.write_text(json.dumps(data,indent=2))
print('7.3.3 Notes scrollbar and widget count prepared; Android and device checks required')
