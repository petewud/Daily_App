#!/usr/bin/env python3
"""7.0.2: repair the malformed edgeToEdge replacement and defer system-bar styling."""
from pathlib import Path
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_STUDIO_70' not in s:raise SystemExit('Run update_studio.py before update_edgefix.py.')
MARK='// A_DAY_TO_KEEP_EDGEFIX_702'
def bounds(text,signature):
 a=text.find(signature)
 if a<0:raise RuntimeError('Missing source section: '+signature)
 brace=text.find('{',a);i=brace+1;depth=1;state='code'
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
 if depth:raise RuntimeError('Unbalanced source: '+signature)
 return a,i
def replace(signature,new):
 global s
 a,b=bounds(s,signature);s=s[:a]+new+s[b:]
if MARK not in s:
 # The prior repair inserted a lambda arrow but omitted its enclosing parentheses,
 # leaving `->` outside a valid Java expression and corrupting the source.
 replace('void edgeToEdge(){',r"""void edgeToEdge(){Window w=getWindow();w.setDecorFitsSystemWindows(false);w.clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);w.setStatusBarColor(Color.TRANSPARENT);w.setNavigationBarColor(Color.TRANSPARENT);w.setStatusBarContrastEnforced(false);w.setNavigationBarContrastEnforced(false);w.getDecorView().post(() -> {try{WindowInsetsController controller=w.getInsetsController();if(controller!=null)controller.setSystemBarsAppearance(WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS,WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS);}catch(RuntimeException error){android.util.Log.w("ADayToKeep","Could not apply system bar appearance",error);}});""")
 s=s.replace('// A_DAY_TO_KEEP_STUDIO_70','// A_DAY_TO_KEEP_STUDIO_70\n// A_DAY_TO_KEEP_EDGEFIX_702',1)
 p.write_text(s,encoding='utf-8')
print('Repaired edgeToEdge lambda syntax and deferred system-bar appearance changes.')
