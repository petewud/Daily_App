import ast,hashlib,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import numpy as np
repo=Path(__file__).resolve().parents[1]
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text()
if '// A_DAY_TO_KEEP_ATLAS_72' not in s:raise RuntimeError('Working artwork integration required first')
module=ast.parse((repo/'scripts/integrate_artwork.py').read_text())
namespace={}
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='end'],type_ignores=[]),'block_parser','exec'),namespace)
end=namespace['end']
def edit(signature,fn):
 global s
 a=s.index(signature);b=end(s,a);s=s[:a]+fn(s[a:b])+s[b:]
def need(text,old,new):
 if text.count(old)!=1:raise RuntimeError('Expected exactly one hook: '+old[:100])
 return text.replace(old,new,1)
keys={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('signing').rglob('*') if f.is_file()}
a=s.index('final ThemeSpec[] themes=');theme_array=s[a:end(s,a)]
gradle=Path('app/build.gradle');g=gradle.read_text();identity=re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)
if '// A_DAY_TO_KEEP_UI_73' not in s:
 edit('void home(){',lambda t:need(need(need(t,'Make a little room for you','Take today at your own pace'),'Little plans. Lovely memories.','A little structure. A little space.'),'compactBanner.topMargin=-dp(18);','compactBanner.topMargin=-dp(24);').replace('root.addView(banner,compactBanner);space(root,5);','root.addView(banner,compactBanner);space(root,3);'))
 edit('void attachCharacterPlay(',lambda t:t.replace('{','{homeCharacter=mascot;',1))
 edit('void startCharacterParty(',lambda t:need(t,'celebrateStarted+650','celebrateStarted+1300'))
 edit('void releaseCharacterParty(',lambda t:need(t,'celebrateStarted+650','celebrateStarted+1300'))
 def tasks(t):
  t=need(t,'boolean checked=!task.optBoolean("done");','boolean wasComplete=dueTasksComplete();boolean checked=!task.optBoolean("done");')
  return need(t,'save();chime(checked?checkSound:softSound);home();','boolean justCompleted=checked&&!wasComplete&&dueTasksComplete();save();chime(checked?checkSound:softSound);home();if(justCompleted)root.post(()->celebrateChecklistCompletion());')
 edit('void buildTasks(',tasks)
 edit('void notes(){',lambda t:need(t,'add.setElevation(dp(12));','add.setElevation(dp(4));add.setTranslationZ(0);add.setOutlineAmbientShadowColor(0x35736680);add.setOutlineSpotShadowColor(0x24736680);'))
 def note(t):
  footer='FrameLayout noteFooter=new FrameLayout(this);View done=glyphButton("Done editing","tick",MINT,()->{save();android.view.inputmethod.InputMethodManager keyboard=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);if(keyboard!=null)keyboard.hideSoftInputFromWindow(body.getWindowToken(),0);notes();});FrameLayout.LayoutParams doneLp=new FrameLayout.LayoutParams(dp(52),dp(52),Gravity.RIGHT|Gravity.CENTER_VERTICAL);doneLp.setMargins(0,dp(4),dp(3),dp(4));noteFooter.addView(done,doneLp);root.addView(noteFooter,new LinearLayout.LayoutParams(-1,dp(64)));'
  t=need(t,'root.addView(body,new LinearLayout.LayoutParams(-1,0,1));','root.addView(body,new LinearLayout.LayoutParams(-1,0,1));'+footer)
  t,n=re.subn(r'body\.setHint\("[^"]*"\);','body.setHint("Keep a little note");',t)
  if n!=1:raise RuntimeError('Note placeholder hook changed')
  return t
 edit('void noteEditor(){',note)
 tick='if(kind.equals("tick")){c.save();c.scale(getWidth()/40f,getHeight()/40f);p.setColor(INK);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.8f);p.setStrokeCap(Paint.Cap.ROUND);p.setStrokeJoin(Paint.Join.ROUND);Path check=new Path();check.moveTo(9,21);check.lineTo(17,29);check.lineTo(31,12);c.drawPath(check,p);c.restore();return;}'
 edit('class ActionGlyph extends View {',lambda t:need(t,'protected void onDraw(Canvas c){','protected void onDraw(Canvas c){'+tick))
 edit('void showCute(AlertDialog d){',lambda t:t[:-1]+'semanticButtons(d);if(d.getWindow()!=null){themedScrolls(d.getWindow().getDecorView());d.getWindow().getDecorView().post(()->semanticButtons(d));}}')
 edit('void base(String title,boolean back){',lambda t:t[:-1]+'root.post(()->themedScrolls(root));}')
 edit('void showThemeMenu(',lambda t:need(t,'popup.showAsDropDown(anchor,0,dp(4));','themedScrolls(menu);popup.showAsDropDown(anchor,0,dp(4));'))
 edit('void refreshWidgetSnapshot(){',lambda t:need(t,'skin.put("pink",t.pink);','skin.put("pink",t.pink);skin.put("circleBackground",portraitCircleColor(t));'))
 edit('void viewer(LocalDate d,String file){',lambda t:(repo/'scripts/viewer-73.java.inc').read_text())
 anchor=' JSONObject data;'
 s=need(s,anchor,(repo/'scripts/ui-73.java.inc').read_text()+'\n'+anchor)
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// UI_VERSION_CODE:'+str(code)+'\n'
else:code=int(re.search(r'// UI_VERSION_CODE:(\d+)',s).group(1))
widget=Path('app/src/main/java/uk/co/littledays/KeepWidget.java');w=widget.read_text()
old='paint.setColor(pink);c.drawCircle(center,center,104,paint);';new='paint.setColor(skin.optInt("circleBackground",pink));c.drawCircle(center,center,104,paint);'
if old in w:w=need(w,old,new)
elif new not in w:raise RuntimeError('Widget background hook changed')
widget.write_text(w)
assets=Path('app/src/main/assets/artwork');metadata=json.loads((assets/'theme-map.json').read_text())
for name,item in metadata['themes'].items():
 image=Image.open(assets/item['portrait']).convert('RGBA');rgb=np.median(np.array(image.crop((219,9,229,15)))[:,:,:3].reshape(-1,3),axis=0).astype(int)
 item['circleBackground']=int(0xff000000|(int(rgb[0])<<16)|(int(rgb[1])<<8)|int(rgb[2]))-2**32
(assets/'theme-map.json').write_text(json.dumps(metadata,indent=2))
res=Path('app/src/main/res');(res/'values/polish_ids.xml').write_text('<resources><item type="id" name="polish_scroll_tag"/></resources>')
bunny=Image.open(assets/metadata['themes']['Strawberry Bunny']['portrait']).convert('RGBA')
color=metadata['themes']['Strawberry Bunny']['circleBackground']&0xffffff
background='#'+format(color,'06x')
icon=Image.new('RGBA',(432,432));thumb=bunny.resize((264,264),Image.Resampling.LANCZOS);icon.paste(thumb,(84,84))
(res/'drawable-nodpi').mkdir(exist_ok=True);icon.save(res/'drawable-nodpi/strawberry_launcher.png')
(res/'drawable/launcher_foreground.xml').write_text('<bitmap xmlns:android="http://schemas.android.com/apk/res/android" android:src="@drawable/strawberry_launcher" android:gravity="fill" android:filter="true"/>')
colors=res/'values/icon_colors.xml';tree=ET.parse(colors);found=False
for item in tree.getroot():
 if item.attrib.get('name')=='launcher_background':item.text=background;found=True
if not found:raise RuntimeError('Launcher background resource missing')
tree.write(colors,encoding='utf-8',xml_declaration=True)
for folder,size in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
 dest=res/('mipmap-'+folder);dest.mkdir(exist_ok=True);legacy=Image.new('RGBA',(size,size),background);small=bunny.resize((size,size),Image.Resampling.LANCZOS);legacy.alpha_composite(small)
 for name in ['ic_launcher','ic_launcher_round']:legacy.save(dest/(name+'.png'))
a=s.index('final ThemeSpec[] themes=')
if s[a:end(s,a)]!=theme_array:raise RuntimeError('Stored theme array changed')
s=s.replace('Version 7.2','Version 7.3')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.3"',g)
if re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)!=identity:raise RuntimeError('Application ID changed')
if not keys or any(hashlib.sha256(Path(f).read_bytes()).hexdigest()!=digest for f,digest in keys.items()):raise RuntimeError('Signing changed')
p.write_text(s);gradle.write_text(g)
Path('ui-amendments-report.json').write_text(json.dumps({'version':'7.3','version_code':code,'theme_array_unchanged':True,'signing_unchanged':True,'launcher':'Strawberry Bunny','checklist_celebration':'only direct transition to complete','rain_emission_ms':1300,'note_hint':'Keep a little note'},indent=2))
print('7.3 amendments prepared; compile and emulator/device checks required')
