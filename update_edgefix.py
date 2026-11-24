#!/usr/bin/env python3
"""7.0.3: restore the valid edgeToEdge method and defer system-bar styling safely."""
from pathlib import Path
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_STUDIO_70' not in s:raise SystemExit('Run update_studio.py before update_edgefix.py.')
MARK='// A_DAY_TO_KEEP_EDGEFIX_703'
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
 # Replace the entire prior malformed edgeToEdge method, whether it is the original
 # immediate call or either earlier attempted repair. Do not rely on a partial edit.
 original=r"""void edgeToEdge(){Window w=getWindow();w.setDecorFitsSystemWindows(false);w.clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);w.setStatusBarColor(Color.TRANSPARENT);w.setNavigationBarColor(Color.TRANSPARENT);w.setStatusBarContrastEnforced(false);w.setNavigationBarContrastEnforced(false);WindowInsetsController controller=w.getInsetsController();if(controller!=null)controller.setSystemBarsAppearance(WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS,WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS);}"""
 repaired=r"""void edgeToEdge(){Window w=getWindow();w.setDecorFitsSystemWindows(false);w.clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);w.setStatusBarColor(Color.TRANSPARENT);w.setNavigationBarColor(Color.TRANSPARENT);w.setStatusBarContrastEnforced(false);w.setNavigationBarContrastEnforced(false);w.getDecorView().post(() -> {try{WindowInsetsController controller=w.getInsetsController();if(controller!=null)controller.setSystemBarsAppearance(WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS,WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS|WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS);}catch(RuntimeException error){android.util.Log.w("ADayToKeep","Could not apply system bar appearance",error);}});}"""
 if original in s:s=s.replace(original,repaired,1)
 elif 'w.getDecorView().post(()->{try{' in s:
  # Remove the malformed 7.0.1/7.0.2 replacement before inserting the valid method.
  a,b=bounds(s,'void edgeToEdge(){');s=s[:a]+repaired+s[b:]
 else:
  a,b=bounds(s,'void edgeToEdge(){');s=s[:a]+repaired+s[b:]
 s=s.replace('// A_DAY_TO_KEEP_STUDIO_70','// A_DAY_TO_KEEP_STUDIO_70\n// A_DAY_TO_KEEP_EDGEFIX_703',1)
 p.write_text(s,encoding='utf-8')
print('Restored a valid edgeToEdge method and deferred system-bar appearance changes.')
