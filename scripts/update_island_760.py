import json,re
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java');s=p.read_text()
if '// A_DAY_TO_KEEP_ISLAND_75' not in s:raise RuntimeError('Island game 7.5.0 required')
def need(text,old,new):
 if text.count(old)!=1:raise RuntimeError('Expected one hook: '+old[:100])
 return text.replace(old,new,1)
gradle=Path('app/build.gradle');g=gradle.read_text()
if '// A_DAY_TO_KEEP_ISLAND_76' not in s:
 s=need(s,'chime(softSound);openIsland75();','chime(softSound);openIsland76();')
 game=''.join((repo/('scripts/island-game-76'+part+'.java.inc')).read_text() for part in 'abcd')
 s=need(s,' JSONObject data;',game+'\n JSONObject data;')
 code=int(re.search(r'versionCode\s+(\d+)',g).group(1))+1
 s+='\n// ISLAND_GAME_76 code '+str(code)+'\n'
else:code=int(re.search(r'// ISLAND_GAME_76 code (\d+)',s).group(1))
s=s.replace('Version 7.5.0 demo','Version 7.6.0 demo')
g=re.sub(r'versionCode\s+\d+','versionCode '+str(code),g);g=re.sub(r'versionName\s+[\'"][^\'"]+[\'"]','versionName "7.6.0"',g)
p.write_text(s);gradle.write_text(g)
report=Path('ui-amendments-report.json');data=json.loads(report.read_text());data.update(version='7.6.0',version_code=code,island_game='tool animations, pond-only water, owned-items pockets, axe and trees, foraging, shop stall and daily bunny requests');report.write_text(json.dumps(data,indent=2))
print('7.6.0 island game prepared')
