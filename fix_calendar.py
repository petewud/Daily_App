#!/usr/bin/env python3
"""7.1.1: recognise the Unicode calendar chevrons and restore both accessible controls."""
from pathlib import Path
import re
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_COMFORT_71' not in s or 'class CalendarChevron' not in s:raise SystemExit('Run update_comfort.py before fix_calendar.py.')
MARK='// A_DAY_TO_KEEP_CALENDAR_711'
def span(text,signature):
 a=text.find(signature)
 if a<0:raise RuntimeError('Missing Java method: '+signature)
 start=text.find('{',a);i=start+1;depth=1;state='code'
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
 if depth:raise RuntimeError('Unclosed Java method')
 return a,i
symbols=set(re.findall(r'calendarArrow\(\s*"([^"\n]+)"',s))
if not symbols or not symbols.issubset({'<','>','‹','›'}):raise RuntimeError('Unexpected calendar-arrow symbols: '+repr(symbols))
replacement='View calendarArrow(String symbol,Runnable action){boolean previous=symbol.equals("<")||symbol.equals("‹");FrameLayout arrow=new FrameLayout(this);arrow.setBackground(shape(WHITE));arrow.setMinimumWidth(dp(56));arrow.setMinimumHeight(dp(56));arrow.setContentDescription(previous?"Previous month":"Next month");arrow.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_YES);arrow.setFocusable(true);CalendarChevron chevron=new CalendarChevron(previous);chevron.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);arrow.addView(chevron,new FrameLayout.LayoutParams(dp(30),dp(30),Gravity.CENTER));arrow.setOnClickListener(v->{chime(softSound);action.run();});wirePress(arrow);return arrow;}'
check=span(replacement,'View calendarArrow(')
if check!=(0,len(replacement)):raise RuntimeError('Invalid replacement method boundary')
a,b=span(s,'View calendarArrow(');s=s[:a]+replacement+s[b:]
gradle=Path('app/build.gradle');g=gradle.read_text()
if MARK not in s:
 code=re.search(r'versionCode\s+(\d+)',g)
 if not code:raise RuntimeError('versionCode missing')
 s=s.replace('// A_DAY_TO_KEEP_COMFORT_71','// A_DAY_TO_KEEP_COMFORT_71\n'+MARK+'\n// CALENDAR_VERSION_CODE:'+str(int(code.group(1))+1),1)
 s=re.sub(r'Version 7\.1(?![\d.])','Version 7.1.1',s)
code=re.search(r'// CALENDAR_VERSION_CODE:(\d+)',s)
if not code:raise RuntimeError('Calendar version marker missing')
g=re.sub(r'versionCode\s+\d+','versionCode '+code.group(1),g)
g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "7.1.1"',g)
p.write_text(s,encoding='utf-8');gradle.write_text(g,encoding='utf-8')
print('Calendar arrow direction and accessibility labels repaired; existing navigation tests remain enabled.')
