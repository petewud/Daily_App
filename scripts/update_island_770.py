import json,re
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java');s=p.read_text()
if '// A_DAY_TO_KEEP_ISLAND_76' not in s:raise RuntimeError('Island game 7.6.0 required')
def need(text,old,new):
 if text.count(old)!=1:raise RuntimeError('Expected one hook: '+old[:100])
 return text.replace(old,new,1)
gradle=Path('app/build.gradle');g=gradle.read_text()
if '// A_DAY_TO_KEEP_ISLAND_77' not in s:
 s=need(s,'chime(softSound);openIsland76();','chime(softSound);openIsland77();')
 game=''.join((repo/('scripts/island-game-77'+part+'.java.inc')).read_text() for part in 'abcde')
 s=need(s,' JSONObject data;',game+'\n JSONObject data;')
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// ISLAND_GAME_77 code '+str(code)+'\n'
else:code=int(re.search(r'// ISLAND_GAME_77 code (\d+)',s).group(1))
s=s.replace('Version 7.6.0 demo','Version 7.7.0 demo')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.7.0"',g)
p.write_text(s);gradle.write_text(g)
report=Path('ui-amendments-report.json');data=json.loads(report.read_text());data.update(version='7.7.0',version_code=code,island_game='pixel water drops, stump digging, kicking holes closed, one-sided axe, item names, sell and buy popups, saplings, bug net and bug log, rock lifting, tap-to-unequip chip');report.write_text(json.dumps(data,indent=2))
print('7.7.0 island game prepared')
