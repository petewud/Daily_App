#!/usr/bin/env python3
"""Repair version-6 journal keyboard state delivery, without weakening the UI test."""
from pathlib import Path
import re
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_V6' not in s:raise SystemExit('Run update_polish.py before fix_writing.py.')
MARK='// A_DAY_TO_KEEP_WRITING_FIX_61'
def method_end(text,start):
 brace=text.find('{',start);i=brace+1;depth=1;state='code'
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
 if depth:raise RuntimeError('Could not safely locate journal method end')
 return i
helper='\n // A_DAY_TO_KEEP_WRITING_FIX_61\n void installWritingMode(LinearLayout journalRoot,EditText note,View dateHeader,View nav,View prompt,View attachments,View footer,ScrollView scroll){\n  // Read the window\'s original IME insets, not an inset object already consumed by a parent.\n  getWindow().setDecorFitsSystemWindows(false);\n  getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_NOTHING);\n  final boolean[] initialized={false},expandedBefore={false};final int[] reserveBefore={-1};\n  final Runnable[] check=new Runnable[1];\n  check[0]=()->{\n   journalRoot.removeCallbacks(check[0]);\n   if(isFinishing()||isDestroyed()||root!=journalRoot||!screen.equals("cpd")||!journalRoot.isAttachedToWindow())return;\n   try{\n    View decor=getWindow().getDecorView();WindowInsets raw=decor.getRootWindowInsets();\n    if(raw==null)raw=journalRoot.getRootWindowInsets();\n    android.graphics.Insets bars=raw==null?android.graphics.Insets.NONE:raw.getInsets(WindowInsets.Type.systemBars()|WindowInsets.Type.displayCutout());\n    int left=dp(16)+bars.left,top=dp(10)+bars.top,right=dp(16)+bars.right,bottom=dp(16)+bars.bottom;\n    if(journalRoot.getPaddingLeft()!=left||journalRoot.getPaddingTop()!=top||journalRoot.getPaddingRight()!=right||journalRoot.getPaddingBottom()!=bottom)journalRoot.setPadding(left,top,right,bottom);\n    boolean imeVisible=raw!=null&&raw.isVisible(WindowInsets.Type.ime());\n    int imeHeight=raw==null?0:raw.getInsets(WindowInsets.Type.ime()).bottom;\n    // A secondary visible-frame measurement covers delayed visibility/inset delivery.\n    Rect frame=new Rect();decor.getWindowVisibleDisplayFrame(frame);int[] location=new int[2];decor.getLocationOnScreen(location);int covered=Math.max(0,location[1]+decor.getHeight()-frame.bottom);\n    if(covered>Math.max(dp(120),bars.bottom+dp(80))){imeVisible=true;imeHeight=Math.max(imeHeight,covered);}\n    boolean expanded=imeVisible&&note.hasFocus();\n    int reserve=expanded?Math.max(0,imeHeight-journalRoot.getPaddingBottom()-footer.getHeight()):0;\n    if(!initialized[0]||expandedBefore[0]!=expanded||reserveBefore[0]!=reserve){\n     initialized[0]=true;expandedBefore[0]=expanded;reserveBefore[0]=reserve;\n     dateHeader.setVisibility(expanded?View.GONE:View.VISIBLE);nav.setVisibility(expanded?View.GONE:View.VISIBLE);prompt.setVisibility(expanded?View.GONE:View.VISIBLE);attachments.setVisibility(expanded?View.GONE:View.VISIBLE);\n     // The full-height window is not resized. The footer stays at its original bottom,\n     // covered by the IME, while only the journal editor reserves space above the IME.\n     footer.setVisibility(expanded?View.INVISIBLE:View.VISIBLE);\n     LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)scroll.getLayoutParams();lp.bottomMargin=reserve;scroll.setLayoutParams(lp);\n     final boolean writing=expanded;\n     scroll.post(()->{if(root!=journalRoot||isDestroyed()||expandedBefore[0]!=writing)return;LinearLayout.LayoutParams np=(LinearLayout.LayoutParams)note.getLayoutParams();np.height=writing?Math.max(dp(90),scroll.getHeight()-scroll.getPaddingTop()-scroll.getPaddingBottom()):-2;note.setMinHeight(writing?dp(90):dp(240));note.setLayoutParams(np);if(writing){scroll.scrollTo(0,0);int cursor=note.getSelectionEnd();if(cursor>=0)note.bringPointIntoView(cursor);}});\n     android.util.Log.i("ADayToKeep","Writing mode="+expanded+" imeVisible="+imeVisible+" imeHeight="+imeHeight+" reserve="+reserve+" focused="+note.hasFocus());\n    }\n   }catch(RuntimeException error){android.util.Log.e("ADayToKeep","Journal keyboard layout failed",error);}\n   if(root==journalRoot&&screen.equals("cpd"))journalRoot.postDelayed(check[0],journalRoot.getWindowVisibility()==View.VISIBLE?120:500);\n  };\n  journalRoot.setOnApplyWindowInsetsListener((view,insets)->{journalRoot.removeCallbacks(check[0]);journalRoot.post(check[0]);return insets;});\n  note.setOnFocusChangeListener((view,focused)->{journalRoot.removeCallbacks(check[0]);journalRoot.post(check[0]);});\n  journalRoot.requestApplyInsets();journalRoot.post(check[0]);\n }\n'

if MARK not in s:
 start=s.find('void journal(){')
 if start<0:raise RuntimeError('Journal source not found')
 end=method_end(s,start)
 old=s[start:end]
 tail=old.find('final boolean[] writing=')
 if tail<0:raise RuntimeError('Expected version-6 writing-mode block not found')
 updated=old[:tail]+'installWritingMode(root,note,dateHeader,nav,prompt,attachments,exportFooter,scroll);\n }'
 s=s[:start]+updated+s[end:]
 anchor=' JSONObject data;'
 if anchor not in s:raise RuntimeError('Activity field anchor missing')
 s=s.replace(anchor,helper+'\n'+anchor,1)
 s=s.replace('Version 6.0','Version 6.1')
 p.write_text(s,encoding='utf-8')
gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode 7',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "6.1"',g);gradle.write_text(g)
Path('VERSION-6.1-NOTES.txt').write_text('Journal writing-mode repair. Uses window-root IME insets, visible-frame fallback, inset/focus events and a journal-scoped lifecycle-checked observer. Footer stays at the bottom while editor occupies available keyboard space. Original tests remain enforced. Actual emulator and device validation still required.\n',encoding='utf-8')
print('Version 6.1 keyboard fix applied. The writing-mode smoke-test assertion is unchanged.')
