#!/usr/bin/env python3
"""6.4: sofa artwork, denser collision-safe animation, flat theme previews and 12 themes."""
from pathlib import Path
import re
p=Path('app/src/main/java/uk/co/littledays/MainActivity.java')
s=p.read_text(encoding='utf-8')
if '// A_DAY_TO_KEEP_PREFERENCES_63' not in s:raise SystemExit('Run update_preferences.py before update_bloom.py.')
MARK='// A_DAY_TO_KEEP_BLOOM_64'
def bounds(text,signature):
 a=text.find(signature)
 if a<0:raise RuntimeError('Source section missing: '+signature)
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
 if depth:raise RuntimeError('Unbalanced Java section: '+signature)
 return a,i

def replace(signature,new):
 global s
 a,b=bounds(s,signature);s=s[:a]+new+s[b:]
def edit(signature,fn):
 global s
 a,b=bounds(s,signature);s=s[:a]+fn(s[a:b])+s[b:]
if MARK not in s:
 extra=r""",
 new ThemeSpec("Eucalyptus Koala","Sage leaves, cosy tea & a sleepy koala","koala","Mali","PatrickHand",0xFF586E66,0xFFD5E5DC,0xFFE2E4DE,0xFFCDE6D7,0xFFF3F9F1,0xFFFDFFFA),
 new ThemeSpec("Maple Red Panda","Maple treasures, apricots & woodland paws","redpanda","Chewy","Mali",0xFF805B4D,0xFFF2D0B8,0xFFE9DAD1,0xFFDDE5C8,0xFFFFF6EC,0xFFFFFDFA),
 new ThemeSpec("Lilac Elephant","Soft lilac clouds, rainbows & gentle giants","elephant","PatrickHand","Mali",0xFF706486,0xFFE5D8EE,0xFFDCDFF4,0xFFDDEADB,0xFFF9F3FD,0xFFFFFCFF),
 new ThemeSpec("Bluebell Mouse","Bluebell petals, little stars & tiny whiskers","mouse","Mali","PatrickHand",0xFF5D6883,0xFFDAE0F3,0xFFE6DDF2,0xFFDDEBDF,0xFFF5F7FF,0xFFFEFDFF),
 new ThemeSpec("Matcha Turtle","Lotus ponds, mint ripples & unhurried days","turtle","Chewy","Mali",0xFF5C755A,0xFFD8E8C9,0xFFD8E7DA,0xFFCDE5CF,0xFFF7FBEF,0xFFFDFFF8),
 new ThemeSpec("Cocoa Sloth","Warm cocoa, leafy naps & a slower little day","sloth","PatrickHand","Mali",0xFF7A6557,0xFFEBD9C7,0xFFE7DFD4,0xFFDCE5CE,0xFFFFF9F0,0xFFFFFDFA),
 new ThemeSpec("Midnight Raccoon","Moonlit leaves, soft grey paws & tiny stars","raccoon","Mali","PatrickHand",0xFF60667D,0xFFDDE1EE,0xFFE5DEF0,0xFFDDE7DF,0xFFF5F6FC,0xFFFDFEFF),
 new ThemeSpec("Sugarplum Unicorn","Pastel rainbows, crystals & little wishes","unicorn","Chewy","Mali",0xFF826283,0xFFF0D6EC,0xFFE3DDF5,0xFFDDECE8,0xFFFFF4FD,0xFFFFFCFF),
 new ThemeSpec("Tropical Parrot","Tropical leaves, peach blossoms & bright beaks","parrot","Mali","PatrickHand",0xFF507B74,0xFFCEEAE0,0xFFD7E8EA,0xFFF1E2BC,0xFFF1FCF7,0xFFFCFFFD),
 new ThemeSpec("Ocean Whale","Drifting bubbles, shells & peaceful blue seas","whale","PatrickHand","Mali",0xFF526E8A,0xFFD2E5F4,0xFFDEE3F5,0xFFD7EDE7,0xFFF0FAFF,0xFFFCFEFF),
 new ThemeSpec("Meadow Fawn","Meadow flowers, woodland leaves & tiny antlers","fawn","Mali","PatrickHand",0xFF7A6851,0xFFEEDBC1,0xFFE8E0D1,0xFFD9E8CE,0xFFFFFAEF,0xFFFFFEFA),
 new ThemeSpec("Buttercup Chick","Buttercup flowers, honey bees & sunny cheeks","chick","Chewy","Mali",0xFF887344,0xFFF6E5AD,0xFFF1E3CF,0xFFDFE9CD,0xFFFFFCEB,0xFFFFFFF8)
 """
 match=re.search(r'(final ThemeSpec\[\] themes=\{)(.*?)(\n\s*\};)',s,re.S)
 if not match:raise RuntimeError('Theme array missing')
 s=s[:match.start()]+match.group(1)+match.group(2).rstrip()+extra+match.group(3)+s[match.end():]
 # Explicit backed sofa silhouette: two back cushions, seat, raised arms and feet.
 def sofa(text):
  a,b=bounds(text,'else if(kind.equals("off"))')
  new=r"""else if(kind.equals("off")){
   int edge=0xFF896D66,upholstery=0xFFE9B9A6,cushion=0xFFF6D6C5,arm=0xFFDAA18E;
   p.setStyle(Paint.Style.FILL);p.setColor(edge);canvas.drawRoundRect(6,6,34,28,5,5,p);p.setColor(upholstery);canvas.drawRoundRect(7.5f,7.5f,32.5f,27,4,4,p);
   p.setColor(cushion);canvas.drawRoundRect(9,9,19.3f,23,3,3,p);canvas.drawRoundRect(20.7f,9,31,23,3,3,p);
   p.setColor(edge);canvas.drawRoundRect(5,23,35,34,3,3,p);p.setColor(upholstery);canvas.drawRoundRect(6.5f,24,33.5f,32.5f,2,2,p);
   p.setColor(cushion);canvas.drawRoundRect(10,23,19.4f,29,2,2,p);canvas.drawRoundRect(20.6f,23,30,29,2,2,p);
   p.setColor(edge);canvas.drawRoundRect(2,17,11,33,3,3,p);canvas.drawRoundRect(29,17,38,33,3,3,p);p.setColor(arm);canvas.drawRoundRect(3.4f,18.4f,9.6f,31.7f,2,2,p);canvas.drawRoundRect(30.4f,18.4f,36.6f,31.7f,2,2,p);
   p.setColor(cushion);canvas.drawRoundRect(3.8f,18.7f,9.2f,22,1.5f,1.5f,p);canvas.drawRoundRect(30.8f,18.7f,36.2f,22,1.5f,1.5f,p);
   p.setColor(edge);canvas.drawRoundRect(7,33,11,37,1,1,p);canvas.drawRoundRect(29,33,33,37,1,1,p);p.setStyle(Paint.Style.FILL);
  }"""
  return text[:a]+new+text[b:]
 edit('boolean drawScheduleSymbol(',sofa)
 # A transparent border must NOT be passed through the opaque colour-blending gradient helper.
 def menu_changes(text):
  old='GradientDrawable border=shape(Color.TRANSPARENT);'
  if old not in text:raise RuntimeError('Theme preview border expression missing')
  text=text.replace(old,'GradientDrawable border=new GradientDrawable();border.setColor(Color.TRANSPARENT);border.setCornerRadius(dp(22));',1)
  text=text.replace('scroll.setPadding(dp(7),dp(7),dp(7),dp(7));','scroll.setPadding(dp(7),dp(2),dp(7),dp(2));scroll.setVerticalFadingEdgeEnabled(false);scroll.setHorizontalFadingEdgeEnabled(false);',1)
  old='PopupWindow popup=new PopupWindow(scroll,width,height,true);'
  if old not in text:raise RuntimeError('Theme menu popup expression missing')
  text=text.replace(old,'ThemeMenuViewport menu=new ThemeMenuViewport();menu.addView(scroll,new FrameLayout.LayoutParams(-1,-1));PopupWindow popup=new PopupWindow(menu,width,height,true);',1)
  text=text.replace('selected.getTop()-dp(5)','selected.getTop()')
  return text
 edit('void showThemeMenu(',menu_changes)
 helper=r"""
 // A_DAY_TO_KEEP_BLOOM_64
 class ThemeMenuViewport extends FrameLayout {
  ThemeMenuViewport(){super(MainActivity.this);setPadding(0,dp(12),0,dp(12));setClipChildren(true);setClipToPadding(true);}
  @Override protected void dispatchDraw(Canvas canvas){int save=canvas.save();canvas.clipRect(0,getPaddingTop(),getWidth(),Math.max(getPaddingTop(),getHeight()-getPaddingBottom()));super.dispatchDraw(canvas);canvas.restoreToCount(save);}
 }
 """
 anchor=' JSONObject data;'
 if anchor not in s:raise RuntimeError('Activity field anchor missing')
 s=s.replace(anchor,helper+'\n'+anchor,1)
 # Denser scenes: smaller drift envelopes leave substantially more room for artwork.
 replace('ArrayList<MotionSticker> packedStickers(',r"""ArrayList<MotionSticker> packedStickers(Rect b,int index,int seed,boolean panel){String key="dense64:"+b.width()+":"+b.height()+":"+index+":"+seed+":"+panel;ArrayList<MotionSticker> cached=scatterCache.get(key);if(cached!=null)return cached;ArrayList<MotionSticker> placed=new ArrayList<>();Random random=new Random(seed);String[] names=motifs(index);float area=b.width()/(float)dp(90)*b.height()/dp(90);int target=Math.max(5,Math.min(panel?48:100,(int)(area*(panel?2.6f:2.1f))));int tries=0;while(placed.size()<target&&tries++<8000){MotionSticker item=new MotionSticker();item.size=dp((panel?19:23)+random.nextInt(panel?11:12));
  // Includes maximum 15% scale, arbitrary rotation, all translation and a gap.
  item.radius=item.size*.98f+dp(14);float edge=item.radius+dp(2);if(b.width()<=edge*2||b.height()<=edge*2)continue;item.cx=edge+random.nextFloat()*(b.width()-edge*2);item.cy=edge+random.nextFloat()*(b.height()-edge*2);boolean clear=true;for(MotionSticker other:placed){float dx=item.cx-other.cx,dy=item.cy-other.cy,minimum=item.radius+other.radius+dp(3);if(dx*dx+dy*dy<minimum*minimum){clear=false;break;}}if(!clear)continue;item.offset=random.nextFloat()*(float)Math.PI*2;item.tilt=random.nextFloat()*36-18;item.name=names[random.nextInt(names.length)];placed.add(item);}scatterCache.put(key,placed);return placed;}""")
 replace('void drawScattered(',r"""void drawScattered(Canvas c,Rect b,int index,int seed,boolean panel,boolean animate){if(b.width()<=0||b.height()<=0)return;ArrayList<MotionSticker> items=packedStickers(b,index,seed,panel);StickerPainter painter=new StickerPainter();float phase=animate?(float)((SystemClock.uptimeMillis()%32000L)*(Math.PI*2/32000.0)):0;for(MotionSticker item:items){float cx=b.left+item.cx,cy=b.top+item.cy,angle=item.tilt,scale=1;if(animate){cx+=(float)Math.sin(phase*2+item.offset)*dp(5.5f);cy+=(float)Math.cos(phase*3+item.offset)*dp(7);angle+=(float)Math.sin(phase*2+item.offset)*18;scale=1+(float)Math.sin(phase*2+item.offset)*.15f;}int save=c.save();c.rotate(angle,cx,cy);c.scale(scale,scale,cx,cy);painter.draw(c,item.name,cx-item.size/2,cy-item.size/2,item.size,panel?84:90);c.restoreToCount(save);}}""")
 def character_changes(text):
  text=text.replace('Math.sin(phase())*6','Math.sin(phase()*2)*6').replace('Math.sin(phase()*2)*5.5f','Math.sin(phase()*2)*3.5f')
  old='int fur='
  if old not in text:raise RuntimeError('Mascot fur expression missing')
  prefix='int fur=animal.equals("koala")?0xFFB5C6BF:animal.equals("redpanda")?0xFFD49770:animal.equals("elephant")?0xFFD1C1E1:animal.equals("mouse")?0xFFC2C9DD:animal.equals("turtle")?0xFFB6D59B:animal.equals("sloth")?0xFFC7B29A:animal.equals("raccoon")?0xFFB5BECE:animal.equals("unicorn")?0xFFFFF8F3:animal.equals("parrot")?0xFF9CCFBB:animal.equals("whale")?0xFFA5C9E4:animal.equals("fawn")?0xFFD8B18A:animal.equals("chick")?0xFFF7DF94:'
  text=text.replace(old,prefix,1)
  head='c.drawOval(14,29,86,86,p);'
  if head not in text:raise RuntimeError('Mascot face drawing missing')
  before=r"""if(animal.equals("koala")){c.drawCircle(20,34,19,p);c.drawCircle(80,34,19,p);fill(0xFFDDE5DD);c.drawCircle(20,34,11,p);c.drawCircle(80,34,11,p);fill(fur);}
   if(animal.equals("redpanda")){Path ears=new Path();ears.moveTo(16,47);ears.lineTo(19,10);ears.lineTo(42,35);ears.lineTo(58,35);ears.lineTo(81,10);ears.lineTo(84,47);ears.close();c.drawPath(ears,p);}
   if(animal.equals("elephant")){c.drawOval(0,31,31,79,p);c.drawOval(69,31,100,79,p);fill(0xFFE7D8ED);c.drawOval(6,40,24,70,p);c.drawOval(76,40,94,70,p);fill(fur);}
   if(animal.equals("mouse")){c.drawCircle(23,25,20,p);c.drawCircle(77,25,20,p);fill(0xFFE9D3E6);c.drawCircle(23,25,12,p);c.drawCircle(77,25,12,p);fill(fur);}
   if(animal.equals("raccoon")){c.drawCircle(25,27,13,p);c.drawCircle(75,27,13,p);}
   if(animal.equals("unicorn")){fill(0xFFE0BFD9);c.drawOval(20,25,82,93,p);Path horn=new Path();horn.moveTo(42,33);horn.lineTo(50,1);horn.lineTo(58,33);horn.close();fill(0xFFF0D596);c.drawPath(horn,p);fill(fur);c.drawOval(23,10,36,44,p);c.drawOval(64,10,77,44,p);}
   if(animal.equals("parrot")){c.drawOval(4,52,28,85,p);c.drawOval(72,52,96,85,p);}
   if(animal.equals("whale")){c.drawOval(2,58,29,80,p);c.drawOval(71,58,98,80,p);fill(0xFFC4E2F1);c.drawOval(43,4,52,22,p);c.drawOval(55,9,64,22,p);fill(fur);}
   if(animal.equals("fawn")){c.drawOval(13,15,34,46,p);c.drawOval(66,15,87,46,p);p.setStyle(Paint.Style.STROKE);p.setColor(0xFFAA886D);p.setStrokeWidth(4);c.drawLine(34,31,29,7,p);c.drawLine(29,17,21,12,p);c.drawLine(66,31,71,7,p);c.drawLine(71,17,79,12,p);fill(fur);}
   if(animal.equals("chick")){c.drawOval(36,15,49,40,p);c.drawOval(49,11,61,39,p);}
   """
  after=r"""
   if(animal.equals("redpanda")){fill(0xFFFFE8D6);c.drawOval(20,43,44,66,p);c.drawOval(56,43,80,66,p);c.drawOval(31,57,69,84,p);}
   if(animal.equals("elephant")){fill(fur);c.drawRoundRect(43,59,57,92,7,7,p);}
   if(animal.equals("sloth")){fill(0xFF9E8A7B);c.save();c.rotate(-20,35,53);c.drawOval(21,43,45,65,p);c.restore();c.save();c.rotate(20,65,53);c.drawOval(55,43,79,65,p);c.restore();}
   if(animal.equals("raccoon")){fill(0xFF788598);c.drawOval(21,43,46,65,p);c.drawOval(54,43,79,65,p);}
   if(animal.equals("unicorn")){fill(0xFFE3C4E5);c.drawOval(34,27,60,42,p);}
   if(animal.equals("turtle")){fill(0xFFD9E8B7);c.drawOval(25,66,75,87,p);}
   if(animal.equals("fawn")){fill(0xFFFFEDD4);c.drawOval(25,35,31,41,p);c.drawOval(69,35,75,41,p);c.drawOval(33,30,39,36,p);c.drawOval(61,30,67,36,p);}
   """
  text=text.replace(head,before+head+after,1)
  text=text.replace('animal.equals("panda")?Color.WHITE:', '(animal.equals("panda")||animal.equals("raccoon")||animal.equals("sloth"))?Color.WHITE:')
  text=text.replace('if(animal.equals("duck"))','if(animal.equals("duck")||animal.equals("chick")||animal.equals("parrot"))')
  text=text.replace('fill(0xFFEAA5B5);c.drawOval(22,64,35,70,p);','if(animal.equals("koala")){fill(0xFF65756E);c.drawOval(43,57,57,74,p);}fill(0xFFEAA5B5);c.drawOval(22,64,35,70,p);')
  return text
 edit('class Mascot extends AnimatedArt {',character_changes)
 edit('class Doodle extends AnimatedArt {',lambda t:t.replace('Math.sin(phase+i)','Math.sin(phase*2+i)').replace('*dp(3.2f)','*dp(2.2f)'))
 def add_motifs(text):
  key='default:return new String[]{"flower","heart","star"};'
  if key not in text:raise RuntimeError('Motif switch fallback missing')
  extra=r"""case 19:return new String[]{"leaf","flower","teacup"};case 20:return new String[]{"leaf","acorn","orange"};case 21:return new String[]{"cloud","rainbow","flower"};case 22:return new String[]{"flower","star","heart"};case 23:return new String[]{"lily","lotus","seaweed"};case 24:return new String[]{"teacup","leaf","flower"};case 25:return new String[]{"moon","leaf","star"};case 26:return new String[]{"rainbow","crystal","sparkle"};case 27:return new String[]{"leaf","orange","flower"};case 28:return new String[]{"bubble","shell","seaweed"};case 29:return new String[]{"flower","leaf","mushroom"};case 30:return new String[]{"flower","bee","honey"};"""
  return text.replace(key,extra+key,1)
 edit('String[] motifs(',add_motifs)
 s=s.replace('Version 6.3','Version 6.4')
 p.write_text(s,encoding='utf-8')
# Both widget variants share this renderer. Reapply after the older resource generators.
widget=Path('app/src/main/java/uk/co/littledays/KeepWidget.java')
w=widget.read_text(encoding='utf-8')
old='paint.setColor(cream);c.drawCircle(center,center,104,paint);'
new='paint.setColor(pink);c.drawCircle(center,center,104,paint);'
if old in w:w=w.replace(old,new,1)
elif new not in w:raise RuntimeError('Shared widget face-background drawing not found')
widget.write_text(w,encoding='utf-8')
gradle=Path('app/build.gradle');g=gradle.read_text();g=re.sub(r'versionCode\s+\d+','versionCode 10',g);g=re.sub(r'versionName\s+[\'\"][^\'\"]+[\'\"]','versionName "6.4"',g);gradle.write_text(g)
Path('VERSION-6.4-NOTES.txt').write_text("""A Day To Keep 6.4
Clearer sofa Day Off symbol. Both widgets now use theme.pink behind the face, matching
the top-left Home character rather than theme.cream. Existing progress contrast,
outline and optional task-count variant remain intact.
Theme preview borders use a genuinely transparent solid fill and a stroke, not the
opaque colour-mixed gradient helper. Popup list has an explicit 12dp inset clipping
boundary at top and bottom, plus small inner padding. Scroll-edge fading is disabled.
Artwork density increased with smaller motion envelopes; full scale/rotation/translation
safety spacing is retained. Translation is 5.5/7dp rather than 9/12dp. Background rotation
frequency doubled (16-second rocking cycle within the same seamless 32-second period).
Character drift is reduced and character rocking is faster. Motion preferences retained.
Twelve new themes appended without reindexing earlier themes: Eucalyptus Koala, Maple Red
Panda, Lilac Elephant, Bluebell Mouse, Matcha Turtle, Cocoa Sloth, Midnight Raccoon,
Sugarplum Unicorn, Tropical Parrot, Ocean Whale, Meadow Fawn, Buttercup Chick. 31 total.
Theme policies, button-press option, PDF/image viewer, keyboard repair, due-date schedule,
backup/restore, existing data and signing identity preserved. Open once to refresh widgets.
Generated with static checks only. GitHub compiles and runs the retained emulator tests;
visual motion, density, popup clip points and real widget colours need device testing.
""",encoding='utf-8')
print('Version 6.4 sofa, denser artwork, widget colours, flat dropdown previews and twelve themes prepared.')
