import json,re
from pathlib import Path
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java');s=p.read_text()
if '// A_DAY_TO_KEEP_ISLAND_74' not in s:raise RuntimeError('Island demo 7.4.0 required')
def need(text,old,new):
 if text.count(old)!=1:raise RuntimeError('Expected one hook: '+old[:100])
 return text.replace(old,new,1)
gradle=Path('app/build.gradle');g=gradle.read_text()
if '// ISLAND_SMOOTH_741' not in s:
 s=need(s,'int dir,scale=6,cx0,cy0;','int dir,scale=6;float cx0,cy0;')
 s=need(s,'void sh(Canvas c,int x,int y,int w){','float sn(float v){return Math.round(v*scale)/(float)scale;}\n  void sh(Canvas c,float x,float y,int w){')
 s=need(s,'int x=Math.round(px),y=Math.round(py);sh(c,x,y,10);','float x=sn(px),y=sn(py);sh(c,x,y,10);')
 s=need(s,'int x=Math.round(bx),y=Math.round(by);sh(c,x,y,10);','float x=sn(bx),y=sn(by);sh(c,x,y,10);')
 s=need(s,'cx0=Math.round(Math.max(0,Math.min(WW-vw,px-vw/2)));cy0=Math.round(Math.max(0,Math.min(WH-vh,py-vh/2)));','cx0=sn(Math.max(0,Math.min(WW-vw,px-vw/2)));cy0=sn(Math.max(0,Math.min(WH-vh,py-vh/2)));')
 s=need(s,'int x=Math.round(f[0]+(float)Math.sin(t*.5f+f[2])*22),y=Math.round(f[1]+(float)Math.cos(t*.8f+f[2])*14);','float x=sn(f[0]+(float)Math.sin(t*.5f+f[2])*22),y=sn(f[1]+(float)Math.cos(t*.8f+f[2])*14);')
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// ISLAND_SMOOTH_741 code '+str(code)+'\n'
else:code=int(re.search(r'// ISLAND_SMOOTH_741 code (\d+)',s).group(1))
s=s.replace('Version 7.4.0 demo','Version 7.4.1 demo')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.4.1"',g)
p.write_text(s);gradle.write_text(g)
report=Path('ui-amendments-report.json');data=json.loads(report.read_text());data.update(version='7.4.1',version_code=code,island_smoothing='camera and sprites snapped to whole screen pixels; no per-sprite rounding disagreement');report.write_text(json.dumps(data,indent=2))
print('7.4.1 smooth movement prepared')
