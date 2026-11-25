import ast,hashlib,json,re
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java');s=p.read_text()
if '// A_DAY_TO_KEEP_UI_73' not in s:raise RuntimeError('Apply working 7.3 amendments first')
module=ast.parse((repo/'scripts/integrate_artwork.py').read_text());namespace={}
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='end'],type_ignores=[]),'block_parser','exec'),namespace);end=namespace['end']
def edit(signature,fn):
 global s
 a=s.index(signature);b=end(s,a);s=s[:a]+fn(s[a:b])+s[b:]
def need(text,old,new):
 if text.count(old)!=1:raise RuntimeError('Expected exactly one hook: '+old[:100])
 return text.replace(old,new,1)
a=s.index('final ThemeSpec[] themes=');themes=s[a:end(s,a)]
keys={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('signing').rglob('*') if f.is_file()}
gradle=Path('app/build.gradle');g=gradle.read_text();identity=re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)
if '// A_DAY_TO_KEEP_LAYOUT_731' not in s:
 edit('void themedScrolls(View view){',lambda t:(repo/'scripts/scroll-gutter-731.java.inc').read_text())
 edit('void drawNotesSymbol(',lambda t:'void drawNotesSymbol(Canvas canvas,int width,int height){int save=canvas.save();canvas.scale(width/40f,height/40f);Paint pen=new Paint(Paint.ANTI_ALIAS_FLAG);pen.setStrokeWidth(1.9f);pen.setStrokeJoin(Paint.Join.ROUND);pen.setColor(LILAC);canvas.drawRoundRect(5,10,29,34,3,3,pen);pen.setStyle(Paint.Style.STROKE);pen.setColor(INK);canvas.drawRoundRect(5,10,29,34,3,3,pen);Path front=new Path();front.moveTo(14,5);front.lineTo(32,5);front.quadTo(35,5,35,8);front.lineTo(35,23);front.lineTo(29,29);front.lineTo(14,29);front.quadTo(11,29,11,26);front.lineTo(11,8);front.quadTo(11,5,14,5);front.close();pen.setStyle(Paint.Style.FILL);pen.setColor(WHITE);canvas.drawPath(front,pen);pen.setStyle(Paint.Style.STROKE);pen.setColor(INK);canvas.drawPath(front,pen);Path fold=new Path();fold.moveTo(29,29);fold.lineTo(29,23);fold.lineTo(35,23);fold.close();pen.setStyle(Paint.Style.FILL);pen.setColor(MINT);canvas.drawPath(fold,pen);pen.setStyle(Paint.Style.STROKE);pen.setColor(INK);canvas.drawPath(fold,pen);canvas.restoreToCount(save);}')
 edit('class ActionGlyph extends View {',lambda t:need(t,'protected void onDraw(Canvas c){','protected void onDraw(Canvas c){'+'if(kind.equals("refresh")){c.save();c.scale(getWidth()/40f,getHeight()/40f);p.setColor(INK);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.6f);p.setStrokeCap(Paint.Cap.ROUND);p.setStrokeJoin(Paint.Join.ROUND);c.drawArc(9,9,31,31,45,285,false,p);Path arrow=new Path();arrow.moveTo(23,8);arrow.lineTo(31,8);arrow.lineTo(31,16);c.drawPath(arrow,p);c.restore();return;}'))
 def home(t):
  old='work.addView(button("Work Schedule","calendar",WHITE,()->calendar("work",LocalDate.now(),null)),new LinearLayout.LayoutParams(-1,-2));space(work,8);'
  new='LinearLayout scheduleHeader=row();View openSchedule=button("Work Schedule","calendar",WHITE,()->calendar("work",LocalDate.now(),null));scheduleHeader.addView(openSchedule,new LinearLayout.LayoutParams(0,-2,1));work.addView(scheduleHeader,new LinearLayout.LayoutParams(-1,-2));space(work,8);'
  t=need(t,old,new)
  control='View resetSchedule=glyphButton("Back to today","refresh",WHITE,()->{if(todayCard[0]!=null){int target=Math.max(0,todayCard[0].getLeft()-dp(2));if(motionEnabled())strip.smoothScrollTo(target,0);else strip.scrollTo(target,0);}});LinearLayout.LayoutParams resetLp=new LinearLayout.LayoutParams(dp(56),dp(56));resetLp.leftMargin=dp(8);scheduleHeader.addView(resetSchedule,resetLp);'
  return need(t,'final View[] todayCard={null};','final View[] todayCard={null};'+control)
 edit('void home(){',home)
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// LAYOUT_VERSION_CODE:'+str(code)+'\n'
else:code=int(re.search(r'// LAYOUT_VERSION_CODE:(\d+)',s).group(1))
a=s.index('final ThemeSpec[] themes=')
if s[a:end(s,a)]!=themes:raise RuntimeError('Stored theme array changed')
if not keys or any(hashlib.sha256(Path(f).read_bytes()).hexdigest()!=digest for f,digest in keys.items()):raise RuntimeError('Signing changed')
s=s.replace('Version 7.3','Version 7.3.1') if 'Version 7.3.1' not in s else s
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.3.1"',g)
if re.findall(r'applicationId\s+[\'"]([^\'"]+)',g)!=identity:raise RuntimeError('Application ID changed')
p.write_text(s);gradle.write_text(g)
report=Path('ui-amendments-report.json');data=json.loads(report.read_text());data.update(version='7.3.1',version_code=code,scroll_gutter='only when full-width content exceeds viewport',notes_icon='overlapping sticky notes',schedule_reset='scroll to today only; no schedule data changes');report.write_text(json.dumps(data,indent=2))
print('7.3.1 layout changes prepared; Android build and device tests required')
